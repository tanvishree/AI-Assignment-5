TOURIST_PLACES_KB = {
    "Paris": {
        "country": "France",
        "category": ["art", "history", "romance"],
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre Dame Cathedral",
                        "Champs-Elysees", "Versailles"],
        "best_season": "Spring (Apr–Jun)"
    },
    "Kyoto": {
        "country": "Japan",
        "category": ["culture", "history", "nature"],
        "attractions": ["Fushimi Inari Shrine", "Arashiyama Bamboo Grove",
                        "Kinkakuji Temple", "Geisha district Gion"],
        "best_season": "Spring (Mar–May) or Autumn (Oct–Nov)"
    },
    "New York": {
        "country": "USA",
        "category": ["urban", "shopping", "entertainment"],
        "attractions": ["Statue of Liberty", "Central Park", "Times Square",
                        "The Met Museum", "Brooklyn Bridge"],
        "best_season": "Autumn (Sep–Nov)"
    },
    "Goa": {
        "country": "India",
        "category": ["beach", "relaxation", "nightlife"],
        "attractions": ["Baga Beach", "Old Goa Churches", "Dudhsagar Falls",
                        "Anjuna Flea Market", "Calangute Beach"],
        "best_season": "Winter (Nov–Feb)"
    },
    "Tuscany": {
        "country": "Italy",
        "category": ["wine", "art", "nature", "history"],
        "attractions": ["Florence", "Siena", "Chianti wine region",
                        "San Gimignano", "Pisa"],
        "best_season": "Spring or Autumn"
    }
}

FOOD_KB = {
    "Paris":    ["Croissants", "French Onion Soup", "Crêpes", "Escargot", "Macarons"],
    "Kyoto":    ["Kaiseki (multi-course)", "Matcha desserts", "Tofu dishes",
                 "Ramen", "Yudofu (hot tofu)"],
    "New York": ["New York Pizza", "Bagels with cream cheese", "Cheesecake",
                 "Pastrami sandwich", "Hot dogs"],
    "Goa":      ["Fish Curry Rice", "Prawn Balchão", "Bebinca (dessert)",
                 "Xacuti", "Feni cocktails"],
    "Tuscany":  ["Ribollita soup", "Bistecca Fiorentina (steak)", "Pici pasta",
                 "Cantucci biscuits", "Pecorino cheese"]
}

WINE_KB = {
    "Paris":    ["Bordeaux", "Champagne", "Burgundy Pinot Noir"],
    "Tuscany":  ["Chianti Classico", "Brunello di Montalcino", "Vernaccia"],
    "Kyoto":    ["Sake (rice wine)", "Umeshu (plum wine)"],
    "New York": ["Finger Lakes Riesling", "Long Island Merlot"],
    "Goa":      ["Feni (local cashew/coconut spirit)", "Imported wines in beach shacks"]
}

# Cost per day in USD for different budget levels
COST_KB = {
    "Paris":    {"budget": 80,  "mid": 180, "luxury": 400},
    "Kyoto":    {"budget": 60,  "mid": 130, "luxury": 350},
    "New York": {"budget": 100, "mid": 200, "luxury": 500},
    "Goa":      {"budget": 30,  "mid": 70,  "luxury": 200},
    "Tuscany":  {"budget": 70,  "mid": 150, "luxury": 380}
}

# Interest → best matching destinations
INTEREST_MATCH_KB = {
    "art":        ["Paris", "Tuscany", "New York"],
    "history":    ["Paris", "Kyoto", "Tuscany"],
    "nature":     ["Kyoto", "Goa"],
    "beach":      ["Goa"],
    "food":       ["Kyoto", "Paris", "Tuscany"],
    "wine":       ["Tuscany", "Paris"],
    "shopping":   ["New York", "Paris"],
    "culture":    ["Kyoto", "Paris"],
    "adventure":  ["Goa", "New York"],
    "relaxation": ["Goa", "Kyoto"]
}


# ─────────────────────────────────────────────
# Planner logic
# ─────────────────────────────────────────────

def recommend_destinations(interests):
    """Recommend destinations matching the user's interests."""
    scores = {}
    for interest in interests:
        for dest in INTEREST_MATCH_KB.get(interest.lower(), []):
            scores[dest] = scores.get(dest, 0) + 1
    # Sort by match score (highest first)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [dest for dest, _ in ranked]


def build_itinerary(destination, days):
    """
    Build a simple day-by-day itinerary.
    Spreads attractions evenly across days.
    """
    info = TOURIST_PLACES_KB.get(destination)
    if not info:
        return []

    attractions = info["attractions"]
    itinerary = []
    per_day = max(1, len(attractions) // days)

    for day in range(1, days + 1):
        start = (day - 1) * per_day
        end   = start + per_day
        day_attractions = attractions[start:end]
        if not day_attractions:
            day_attractions = ["Free exploration / rest day"]
        itinerary.append((day, day_attractions))

    return itinerary


def estimate_cost(destination, days, budget_level="mid"):
    """Return total estimated cost in USD."""
    costs = COST_KB.get(destination, {})
    daily = costs.get(budget_level, 100)
    return daily * days


def generate_travel_plan(user_name, interests, destination, days,
                         budget_level="mid"):
    """
    Main function: generate a complete personalised travel plan.
    """
    print("=" * 50)
    print(f"   PERSONALISED TRAVEL PLAN FOR {user_name.upper()}")
    print("=" * 50)

    # 1. Recommendation
    recommended = recommend_destinations(interests)
    print(f"\nBased on your interests ({', '.join(interests)}),")
    print(f"top recommended destinations: {', '.join(recommended[:3])}")

    if destination not in TOURIST_PLACES_KB:
        print(f"\n'{destination}' not in knowledge base. "
              f"Defaulting to top recommendation: {recommended[0]}")
        destination = recommended[0]

    info = TOURIST_PLACES_KB[destination]
    print(f"\nYou chose: {destination}, {info['country']}")
    print(f"Best season to visit: {info['best_season']}")

    # 2. Itinerary
    print(f"\n--- {days}-Day Itinerary ---")
    itinerary = build_itinerary(destination, days)
    for day, spots in itinerary:
        print(f"  Day {day}: {', '.join(spots)}")

    # 3. Food recommendations
    foods = FOOD_KB.get(destination, ["Local cuisine"])
    print(f"\n--- Must-Try Foods ---")
    for food in foods:
        print(f"  • {food}")

    # 4. Wine suggestions
    wines = WINE_KB.get(destination, ["Local beverages"])
    print(f"\n--- Wine / Drink Suggestions ---")
    for wine in wines:
        print(f"  • {wine}")

    # 5. Cost assessment
    total_cost = estimate_cost(destination, days, budget_level)
    daily_cost = COST_KB[destination][budget_level]
    print(f"\n--- Cost Assessment ({budget_level.title()} budget) ---")
    print(f"  Daily estimate : ~${daily_cost} USD")
    print(f"  Total ({days} days): ~${total_cost} USD")

    print("\n" + "=" * 50)
    print("Bon voyage! Have a wonderful trip!")
    print("=" * 50 + "\n")

    return {
        "destination": destination,
        "days": days,
        "itinerary": itinerary,
        "foods": foods,
        "wines": wines,
        "total_cost_usd": total_cost
    }


# ─────────────────────────────────────────────
# Test cases
# ─────────────────────────────────────────────

def test_travel_planner():
    print("\n===== TEST 1: Alice loves art and wine =====\n")
    plan = generate_travel_plan(
        user_name="Alice",
        interests=["art", "wine", "history"],
        destination="Tuscany",
        days=5,
        budget_level="mid"
    )
    assert plan["destination"] == "Tuscany"
    assert plan["total_cost_usd"] == 750
    print("TEST 1 PASS\n")

    print("\n===== TEST 2: Bob loves beach and relaxation =====\n")
    plan = generate_travel_plan(
        user_name="Bob",
        interests=["beach", "relaxation", "food"],
        destination="Goa",
        days=4,
        budget_level="budget"
    )
    assert plan["destination"] == "Goa"
    assert plan["total_cost_usd"] == 120
    print("TEST 2 PASS\n")

    print("\n===== TEST 3: Unknown destination falls back =====\n")
    plan = generate_travel_plan(
        user_name="Carol",
        interests=["culture", "history"],
        destination="Atlantis",   # not in KB
        days=3,
        budget_level="luxury"
    )
    # Should fall back to top recommendation
    assert plan["destination"] in TOURIST_PLACES_KB
    print("TEST 3 PASS\n")

    print("\n===== TEST 4: Recommendation engine =====\n")
    recs = recommend_destinations(["wine", "art"])
    print(f"Recommendations for wine+art lover: {recs}")
    assert "Tuscany" in recs
    assert "Paris" in recs
    print("TEST 4 PASS\n")


if __name__ == "__main__":
    test_travel_planner()
    print("All Travel Planner tests passed!")
