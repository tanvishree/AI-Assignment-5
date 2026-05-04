"""
Knowledge Graphs – Description and Builder
===========================================
A Knowledge Graph (KG) represents real-world entities and the
relationships between them as a graph.

  Nodes = entities  (e.g. "Paris", "France", "Eiffel Tower")
  Edges = relationships (e.g. "isCapitalOf", "locatedIn", "builtIn")

Each fact is stored as a TRIPLE:  (subject, predicate, object)
  e.g. ("Eiffel Tower", "locatedIn", "Paris")

We build a simple KG using Python's built-in data structures and
then add a lightweight query interface.
"""

from collections import defaultdict


# ─────────────────────────────────────────────
# KnowledgeGraph class
# ─────────────────────────────────────────────

class KnowledgeGraph:
    """
    A simple Knowledge Graph stored as a list of (subject, predicate, object)
    triples.  Supports adding, querying, and visualising the graph.
    """

    def __init__(self):
        # Store triples as a set to avoid duplicates
        self.triples = set()
        # Index for fast lookup: subject → {predicate → [objects]}
        self._index = defaultdict(lambda: defaultdict(list))

    # ── Adding facts ──────────────────────────

    def add(self, subject, predicate, obj):
        """Add a single triple to the graph."""
        triple = (subject, predicate, obj)
        if triple not in self.triples:
            self.triples.add(triple)
            self._index[subject][predicate].append(obj)

    def add_many(self, triples_list):
        """Add multiple triples at once."""
        for s, p, o in triples_list:
            self.add(s, p, o)

    # ── Querying ──────────────────────────────

    def query(self, subject=None, predicate=None, obj=None):
        """
        Flexible query: pass any combination of subject / predicate / object.
        Unspecified arguments act as wildcards.
        Returns a list of matching triples.
        """
        results = []
        for s, p, o in self.triples:
            if (subject   is None or s == subject) and \
               (predicate is None or p == predicate) and \
               (obj       is None or o == obj):
                results.append((s, p, o))
        return results

    def get_related(self, subject, predicate):
        """Return all objects for a given subject + predicate."""
        return self._index[subject].get(predicate, [])

    def get_all_predicates(self):
        """Return a sorted list of all unique relationship types."""
        return sorted({p for _, p, _ in self.triples})

    def get_all_entities(self):
        """Return a sorted list of all unique entity names."""
        entities = set()
        for s, _, o in self.triples:
            entities.add(s)
            entities.add(o)
        return sorted(entities)

    # ── Display ───────────────────────────────

    def print_graph(self):
        """Print all triples in a readable format."""
        print(f"\nKnowledge Graph ({len(self.triples)} triples)")
        print("-" * 50)
        for s, p, o in sorted(self.triples):
            print(f"  ({s})  --[{p}]-->  ({o})")
        print()

    def describe(self, entity):
        """Print everything known about an entity."""
        print(f"\nFacts about '{entity}':")
        found = False
        for s, p, o in sorted(self.triples):
            if s == entity:
                print(f"  {entity}  --[{p}]-->  {o}")
                found = True
            elif o == entity:
                print(f"  {s}  --[{p}]-->  {entity}")
                found = True
        if not found:
            print(f"  No facts found for '{entity}'.")


# ─────────────────────────────────────────────
# Build a sample Travel Domain KG
# ─────────────────────────────────────────────

def build_travel_kg():
    kg = KnowledgeGraph()
    kg.add_many([
        # Countries
        ("France",  "isA",         "Country"),
        ("Japan",   "isA",         "Country"),
        ("India",   "isA",         "Country"),
        ("Italy",   "isA",         "Country"),

        # Cities
        ("Paris",   "isA",         "City"),
        ("Kyoto",   "isA",         "City"),
        ("Goa",     "isA",         "City"),
        ("Florence","isA",         "City"),

        # City → Country
        ("Paris",   "locatedIn",   "France"),
        ("Kyoto",   "locatedIn",   "Japan"),
        ("Goa",     "locatedIn",   "India"),
        ("Florence","locatedIn",   "Italy"),

        # Attractions
        ("Eiffel Tower",    "isA",         "Attraction"),
        ("Louvre Museum",   "isA",         "Attraction"),
        ("Fushimi Inari",   "isA",         "Attraction"),
        ("Baga Beach",      "isA",         "Attraction"),

        # Attraction → City
        ("Eiffel Tower",    "locatedIn",   "Paris"),
        ("Louvre Museum",   "locatedIn",   "Paris"),
        ("Fushimi Inari",   "locatedIn",   "Kyoto"),
        ("Baga Beach",      "locatedIn",   "Goa"),

        # Food
        ("Croissants",      "isA",         "Food"),
        ("Ramen",           "isA",         "Food"),
        ("Fish Curry",      "isA",         "Food"),
        ("Bistecca",        "isA",         "Food"),

        # Food → City
        ("Croissants",      "popularIn",   "Paris"),
        ("Ramen",           "popularIn",   "Kyoto"),
        ("Fish Curry",      "popularIn",   "Goa"),
        ("Bistecca",        "popularIn",   "Florence"),

        # Wine
        ("Chianti",         "isA",         "Wine"),
        ("Champagne",       "isA",         "Wine"),
        ("Sake",            "isA",         "Wine"),

        # Wine → Region
        ("Chianti",         "producedIn",  "Italy"),
        ("Champagne",       "producedIn",  "France"),
        ("Sake",            "producedIn",  "Japan"),

        # Interests
        ("Paris",           "suitableFor", "Art lovers"),
        ("Kyoto",           "suitableFor", "Culture lovers"),
        ("Goa",             "suitableFor", "Beach lovers"),
        ("Florence",        "suitableFor", "Wine lovers"),
    ])
    return kg


# ─────────────────────────────────────────────
# Test cases
# ─────────────────────────────────────────────

def test_knowledge_graph():
    kg = build_travel_kg()

    print("=" * 50)
    print("TEST 1 – Print full graph")
    print("=" * 50)
    kg.print_graph()

    print("=" * 50)
    print("TEST 2 – Describe 'Paris'")
    print("=" * 50)
    kg.describe("Paris")

    print("\n" + "=" * 50)
    print("TEST 3 – Query: what is locatedIn Paris?")
    print("=" * 50)
    results = kg.query(predicate="locatedIn", obj="Paris")
    print(f"Things in Paris: {[s for s,_,_ in results]}")
    assert len(results) == 2   # Eiffel Tower + Louvre
    print("PASS\n")

    print("=" * 50)
    print("TEST 4 – What is Paris suitable for?")
    print("=" * 50)
    suitable = kg.get_related("Paris", "suitableFor")
    print(f"Paris is suitable for: {suitable}")
    assert "Art lovers" in suitable
    print("PASS\n")

    print("=" * 50)
    print("TEST 5 – All predicates (relationship types) in the graph")
    print("=" * 50)
    preds = kg.get_all_predicates()
    print(f"Predicates: {preds}")
    assert "locatedIn" in preds
    print("PASS\n")

    print("=" * 50)
    print("TEST 6 – All entities in the graph")
    print("=" * 50)
    entities = kg.get_all_entities()
    print(f"Total entities: {len(entities)}")
    assert "Eiffel Tower" in entities
    assert "Japan" in entities
    print("PASS\n")


if __name__ == "__main__":
    test_knowledge_graph()
    print("All Knowledge Graph tests passed!")
