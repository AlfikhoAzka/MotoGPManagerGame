def get_trait_modifier(manager):
    trait = manager.get("trait", "No Trait")

    mod = {
        "sponsor": 1.0,
        "upgrade": 1.0,
        "race": 1.0
    }

    if trait == "Former Businessman":
        mod["sponsor"] = 1.15

    elif trait == "Technical Genius":
        mod["upgrade"] = 1.2

    elif trait == "Ex MotoGP Rider":
        mod["race"] = 1.05

    elif trait == "People Person":
        mod["sponsor"] = 1.1

    elif trait == "Data Driven":
        mod["race"] = 1.03

    return mod