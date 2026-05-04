import random
class BayesNode:
    """
    A node in a Bayesian Network.

    name     : variable name (string)
    parents  : list of parent node names
    cpt      : dict mapping parent-value-tuples → P(node=True)

    If no parents, cpt = {(): probability_of_true}
    """

    def __init__(self, name, parents, cpt):
        self.name    = name
        self.parents = parents  # list of strings
        self.cpt     = cpt      # dict: tuple_of_parent_vals → P(True)

    def probability(self, value, parent_values):
        """
        Return P(node = value | parent_values).
        parent_values is a tuple of booleans matching self.parents order.
        """
        p_true = self.cpt[parent_values]
        return p_true if value else (1 - p_true)

class BayesianNetwork:
    """
    A simple Bayesian Network.
    Nodes must be added in topological order (parents before children).
    """

    def __init__(self):
        self.nodes = {}       # name → BayesNode
        self.order = []       # topological order of node names

    def add_node(self, node):
        self.nodes[node.name] = node
        self.order.append(node.name)

    # ── Prior sampling ────────────────────────

    def sample(self):
        """
        Generate one random sample from the joint distribution
        by sampling each node in topological order.
        Returns a dict of {name: True/False}.
        """
        sample = {}
        for name in self.order:
            node = self.nodes[name]
            parent_vals = tuple(sample[p] for p in node.parents)
            p_true = node.cpt[parent_vals]
            sample[name] = random.random() < p_true
        return sample

    # ── Rejection Sampling (approximate inference) ────

    def rejection_sampling(self, query, evidence, n_samples=10000):
        """
        Estimate P(query=True | evidence) using rejection sampling:
          1. Draw many samples from the prior.
          2. Reject samples inconsistent with evidence.
          3. Count how many consistent samples have query=True.

        query    : string – name of the variable to query
        evidence : dict {name: bool} – observed values
        n_samples: how many samples to draw
        """
        consistent = 0
        query_true  = 0

        for _ in range(n_samples):
            s = self.sample()
            # Check if this sample matches all evidence
            if all(s[var] == val for var, val in evidence.items()):
                consistent += 1
                if s[query]:
                    query_true += 1

        if consistent == 0:
            return None   # no consistent samples (very rare evidence)
        return query_true / consistent

    # ── Exact inference (enumerate all combinations) ──

    def enumerate_all(self, variables, evidence):
        """
        Exact inference: sum over all hidden variables.
        Returns P(query | evidence) exactly.

        This is the enumeration-ask algorithm from AIMA (Russell & Norvig).
        """
        if not variables:
            prob = 1.0
            for name in self.order:
                node = self.nodes[name]
                if name in evidence:
                    parent_vals = tuple(evidence[p] for p in node.parents)
                    prob *= node.probability(evidence[name], parent_vals)
            return prob

        var = variables[0]
        rest = variables[1:]
        total = 0.0
        for val in [True, False]:
            ext_evidence = dict(evidence)
            ext_evidence[var] = val
            total += self.enumerate_all(rest, ext_evidence)
        return total

    def query_exact(self, query_var, query_val, evidence):
        """
        P(query_var = query_val | evidence) using exact enumeration.
        """
        hidden = [n for n in self.order
                  if n != query_var and n not in evidence]

        # P(query=True, evidence)
        ev_true = dict(evidence)
        ev_true[query_var] = True
        p_true = self.enumerate_all(hidden, ev_true)

        # P(query=False, evidence)
        ev_false = dict(evidence)
        ev_false[query_var] = False
        p_false = self.enumerate_all(hidden, ev_false)

        # Normalise
        total = p_true + p_false
        if total == 0:
            return None
        return (p_true / total) if query_val else (p_false / total)

def build_weather_bn():
    bn = BayesianNetwork()

    # P(Cloudy = True) = 0.5
    cloudy = BayesNode(
        name="Cloudy",
        parents=[],
        cpt={(): 0.5}
    )
    rain = BayesNode(
        name="Rain",
        parents=["Cloudy"],
        cpt={
            (True,):  0.8,
            (False,): 0.2
        }
    )

    sprinkler = BayesNode(
        name="Sprinkler",
        parents=["Cloudy"],
        cpt={
            (True,):  0.1,
            (False,): 0.5
        }
    )

    # P(WetGrass | Rain, Sprinkler)
    wet_grass = BayesNode(
        name="WetGrass",
        parents=["Rain", "Sprinkler"],
        cpt={
            (True,  True):  0.99,
            (True,  False): 0.9,
            (False, True):  0.9,
            (False, False): 0.0
        }
    )

    bn.add_node(cloudy)
    bn.add_node(rain)
    bn.add_node(sprinkler)
    bn.add_node(wet_grass)
    return bn
  
def test_bayesian_network():
    random.seed(42)
    bn = build_weather_bn()

    print("=" * 50)
    print("TEST 1 – Prior sample (sanity check)")
    print("=" * 50)
    s = bn.sample()
    print(f"Sample: {s}")
    assert set(s.keys()) == {"Cloudy", "Rain", "Sprinkler", "WetGrass"}
    print("PASS\n")

    print("=" * 50)
    print("TEST 2 – Exact: P(Rain=True | Cloudy=True)")
    print("=" * 50)
    p = bn.query_exact("Rain", True, evidence={"Cloudy": True})
    print(f"P(Rain=True | Cloudy=True) = {p:.4f}  (expected ~0.80)")
    assert abs(p - 0.80) < 0.01, f"Expected 0.80, got {p}"
    print("PASS\n")

    print("=" * 50)
    print("TEST 3 – Exact: P(Sprinkler=True | Cloudy=False)")
    print("=" * 50)
    p = bn.query_exact("Sprinkler", True, evidence={"Cloudy": False})
    print(f"P(Sprinkler=True | Cloudy=False) = {p:.4f}  (expected 0.50)")
    assert abs(p - 0.50) < 0.01
    print("PASS\n")

    print("=" * 50)
    print("TEST 4 – Rejection: P(Rain | WetGrass=True)")
    print("=" * 50)
    p = bn.rejection_sampling("Rain", {"WetGrass": True}, n_samples=20000)
    print(f"P(Rain=True | WetGrass=True) ≈ {p:.4f}  (expected ~0.71)")
    assert 0.60 < p < 0.85, f"Out of expected range: {p}"
    print("PASS\n")

    print("=" * 50)
    print("TEST 5 – Grass wet if no rain and no sprinkler")
    print("=" * 50)
    p = bn.query_exact("WetGrass", True,
                       evidence={"Rain": False, "Sprinkler": False})
    print(f"P(WetGrass=True | Rain=False, Sprinkler=False) = {p:.4f}  (expected 0.0)")
    assert p == 0.0
    print("PASS\n")


if __name__ == "__main__":
    test_bayesian_network()
    print("All Bayesian Network tests passed!")
