from trait_effects import get_trait_modifier

def calculate_income(team, riders, manager=None):
    base_income = 1000000

    if manager:
        mod = get_trait_modifier(manager)
        base_income *= mod.get("sponsor", 1.0)

    return int(base_income)


def pay_salaries(team, riders):
    return 300000


def upgrade_bike(team, manager=None):
    cost = 500000
    gain = 2

    if manager:
        mod = get_trait_modifier(manager)
        gain = int(gain * mod.get("upgrade", 1.0))

    if team["budget"] >= cost:
        team["budget"] -= cost

        if "performance" not in team:
            team["performance"] = 70

        team["performance"] += gain
        return f"Upgrade success +{gain}"
    else:
        return "Not enough money"