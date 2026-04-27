from trait_effects import get_trait_modifier

def simulate_race(riders, teams, manager=None):
    for r in riders:
        base = r["skill"] + r["bike"]

        if manager:
            mod = get_trait_modifier(manager)
            base *= mod["race"]

        r["race_score"] = base

    riders.sort(key=lambda x: x["race_score"], reverse=True)

    for i, r in enumerate(riders):
        r["points"] += max(0, 25 - i)

    return riders