import random

TRAITS = {
    "No Trait": {},

    "Former Businessman": {
        "income_bonus": 1.15
    },

    "Technical Genius": {
        "upgrade_bonus": 1.15
    },

    "Ex MotoGP Rider": {
        "race_bonus": 1.05
    },

    "People Person": {
        "morale_bonus": 1.1
    },

    "Data Driven": {
        "consistency_bonus": 1.05
    }
}

def generate_pattern():
    patterns = [
        [6,6,6,6],
        [9,5,5,3],
        [8,8,4,3],
        [8,7,7,3],
        [10,6,4,2]
    ]
    return random.choice(patterns)

def roll_skills(reputation):
    base = generate_pattern()
    random.shuffle(base)

    skills_ui = {
        "negotiation": base[0],
        "engineering": base[1],
        "rider_management": base[2],
        "feedback": base[3]
    }

    multiplier = 2
    variance = 1
    max_cap = 20

    if reputation == "Newcomer":
        multiplier = 2
        variance = 1
        max_cap = 12

    elif reputation == "Known Manager":
        multiplier = 2
        variance = 2
        max_cap = 16

    elif reputation == "Elite Manager":
        multiplier = 2
        variance = 3
        max_cap = 20

    skills_real = {
        k: max(1, min(max_cap, v * multiplier + random.randint(-variance, variance)))
        for k, v in skills_ui.items()
    }

    return skills_ui, skills_real

def apply_trait_effect(manager):
    trait = manager.get("trait", "No Trait")
    manager["effects"] = TRAITS.get(trait, {})

def apply_income_bonus(base_income, manager):
    bonus = manager.get("effects", {}).get("income_bonus", 1.0)
    return int(base_income * bonus)

def apply_upgrade_bonus(base_gain, manager):
    bonus = manager.get("effects", {}).get("upgrade_bonus", 1.0)
    return int(base_gain * bonus)

REAL_MANAGERS = {
    "Ducati": {
        "name": "Gigi Dall'Igna",
        "skills": {"negotiation":12,"engineering":20,"rider_management":12,"feedback":18},
        "trait": "Technical Genius",
        "reputation": "Elite Manager"
    },
    "Aprilia": {
        "name": "Massimo Rivola",
        "skills": {"negotiation":14,"engineering":16,"rider_management":13,"feedback":15},
        "trait": "Technical Genius",
        "reputation": "Elite Manager"
    }
}

def generate_ai_managers(teams):
    result = []

    for t in teams:
        name = t["name"]

        if name in REAL_MANAGERS:
            m = REAL_MANAGERS[name]
            apply_trait_effect(m)
            result.append(m)
        else:
            rep = random.choice(["Newcomer","Known Manager","Elite Manager"])
            _, skills = roll_skills(rep)

            m = {
                "name": f"{name} Manager",
                "skills": skills,
                "trait": random.choice(list(TRAITS.keys())),
                "reputation": rep
            }

            apply_trait_effect(m)
            result.append(m)

    return result