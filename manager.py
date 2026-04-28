import random

REAL_MANAGERS = {
    "Aprilia": {
        "name": "Massimo Rivola",
        "skills": {"negotiation":14,"engineering":16,"rider_management":13,"feedback":15},
        "trait": "Technical Genius",
        "fixed": True
    },
    "Ducati": {
        "name": "Gigi Dall'Igna",
        "skills": {"negotiation":12,"engineering":20,"rider_management":12,"feedback":18},
        "trait": "Technical Genius",
        "fixed": True
    }
}

TRAITS = {
    "No Trait": {},
    "Former Businessman": {"negotiation": 2},
    "Technical Genius": {"engineering": 3},
    "Ex MotoGP Rider": {"rider_management": 2},
    "People Person": {"rider_management": 2},
    "Data Driven": {"feedback": 2}
}

def generate_skill_pattern():
    patterns = [
        [6,6,6,6],
        [9,5,5,3],
        [8,8,4,3],
        [8,7,7,3],
        [10,6,4,2]
    ]
    return random.choice(patterns)

def roll_skills():
    base = generate_skill_pattern()
    random.shuffle(base)

    ui = {
        "negotiation": base[0],
        "engineering": base[1],
        "rider_management": base[2],
        "feedback": base[3]
    }

    real = {
        k: min(20, max(1, v*2 + random.randint(-1,1)))
        for k,v in ui.items()
    }

    return ui, real

def apply_trait_effect(manager):
    trait = manager.get("trait", "No Trait")
    bonus = TRAITS.get(trait, {})

    for k, v in bonus.items():
        manager["skills"][k] = min(20, manager["skills"][k] + v)

def generate_ai_managers(teams):
    result = []

    for t in teams:
        name = t["name"]

        if name in REAL_MANAGERS:
            result.append(REAL_MANAGERS[name])
        else:
            _, skills = roll_skills()

            m = {
                "name": f"{name} Manager",
                "skills": skills,
                "trait": random.choice(list(TRAITS.keys()))
            }

            apply_trait_effect(m)
            result.append(m)

    return result