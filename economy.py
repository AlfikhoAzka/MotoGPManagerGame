from trait_effects import get_trait_modifier

def calculate_income(team, riders, manager=None):
    base_income = 1000000

    if manager:
        mod = get_trait_modifier(manager)
        base_income *= mod["sponsor"]

    return int(base_income)

def pay_salaries(team, riders):
    return 300000

def upgrade_bike(team, manager=None):
    cost = 500000
    gain = 2

    if manager:
        mod = get_trait_modifier(manager)
        gain = int(gain * mod["upgrade"])

    if team["budget"] >= cost:
        team["budget"] -= cost
        team["performance"] += gain
        return f"Upgrade success +{gain}"
    else:
        return "Not enough money"