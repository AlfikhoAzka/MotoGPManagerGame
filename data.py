import random

def generate_riders():
    return [
        {"name": "Francesco Bagnaia", "team": "Ducati", "skill": 93, "trait": "Champion", "points": 0, "age": 29, "salary": 320000},
        {"name": "Marc Marquez", "team": "Ducati", "skill": 95, "trait": "GOAT", "points": 0, "age": 33, "salary": 350000},

        {"name": "Alex Marquez", "team": "Gresini", "skill": 88, "trait": "Aggressive", "points": 0, "age": 30, "salary": 240000},
        {"name": "Fermin Aldeguer", "team": "Gresini", "skill": 85, "trait": "Rookie", "points": 0, "age": 21, "salary": 180000},

        {"name": "Franco Morbidelli", "team": "VR46", "skill": 87, "trait": "Consistent", "points": 0, "age": 31, "salary": 230000},
        {"name": "Fabio Di Giannantonio", "team": "VR46", "skill": 88, "trait": "Late Braker", "points": 0, "age": 27, "salary": 240000},

        {"name": "Jorge Martin", "team": "Aprilia", "skill": 92, "trait": "Aggressive", "points": 0, "age": 28, "salary": 300000},
        {"name": "Marco Bezzecchi", "team": "Aprilia", "skill": 90, "trait": "Fast Learner", "points": 0, "age": 27, "salary": 270000},

        {"name": "Raul Fernandez", "team": "Trackhouse", "skill": 85, "trait": "Potential", "points": 0, "age": 25, "salary": 200000},
        {"name": "Ai Ogura", "team": "Trackhouse", "skill": 84, "trait": "Rookie", "points": 0, "age": 25, "salary": 180000},

        {"name": "Pedro Acosta", "team": "KTM", "skill": 91, "trait": "Prodigy", "points": 0, "age": 21, "salary": 280000},
        {"name": "Brad Binder", "team": "KTM", "skill": 89, "trait": "Consistent", "points": 0, "age": 30, "salary": 260000},

        {"name": "Maverick Vinales", "team": "Tech3", "skill": 88, "trait": "Unpredictable", "points": 0, "age": 31, "salary": 250000},
        {"name": "Enea Bastianini", "team": "Tech3", "skill": 89, "trait": "Late Braker", "points": 0, "age": 28, "salary": 260000},

        {"name": "Fabio Quartararo", "team": "Yamaha", "skill": 90, "trait": "Smooth", "points": 0, "age": 27, "salary": 300000},
        {"name": "Alex Rins", "team": "Yamaha", "skill": 87, "trait": "Technical", "points": 0, "age": 30, "salary": 240000},

        {"name": "Toprak Razgatlioglu", "team": "Pramac", "skill": 88, "trait": "Superbike Star", "points": 0, "age": 29, "salary": 250000},
        {"name": "Jack Miller", "team": "Pramac", "skill": 86, "trait": "Aggressive", "points": 0, "age": 31, "salary": 230000},

        {"name": "Joan Mir", "team": "Honda", "skill": 86, "trait": "Calm", "points": 0, "age": 28, "salary": 230000},
        {"name": "Luca Marini", "team": "Honda", "skill": 85, "trait": "Analytical", "points": 0, "age": 28, "salary": 210000},

        {"name": "Johann Zarco", "team": "LCR", "skill": 87, "trait": "Veteran", "points": 0, "age": 35, "salary": 220000},
        {"name": "Diogo Moreira", "team": "LCR", "skill": 83, "trait": "Rookie", "points": 0, "age": 21, "salary": 170000},
    ]

def generate_teams():
    return [
        {"name": "Ducati", "budget": 8000000,
         "bike": {"engine": 92, "aero": 90, "reliability": 88},
         "factory": True,
         "test_rider": "Michele Pirro",
         "color": "#AA0000"},

        {"name": "Gresini", "budget": 5000000,
         "bike": {"engine": 90, "aero": 88, "reliability": 85},
         "factory": False,
         "test_rider": None,
         "color": "#6EC1E4"},

        {"name": "VR46", "budget": 5200000,
         "bike": {"engine": 90, "aero": 87, "reliability": 85},
         "factory": False,
         "test_rider": None,
         "color": "#D9FF00"},

        {"name": "Aprilia", "budget": 6000000,
         "bike": {"engine": 88, "aero": 87, "reliability": 84},
         "factory": True,
         "test_rider": "Lorenzo Savadori",
         "color": "#111111"},

        {"name": "Trackhouse", "budget": 4000000,
         "bike": {"engine": 86, "aero": 84, "reliability": 82},
         "factory": False,
         "test_rider": None,
         "color": "#118EF5"},

        {"name": "KTM", "budget": 6500000,
         "bike": {"engine": 89, "aero": 86, "reliability": 83},
         "factory": True,
         "test_rider": "Dani Pedrosa",
         "color": "#FF6600"},

        {"name": "Tech3", "budget": 4800000,
         "bike": {"engine": 88, "aero": 85, "reliability": 82},
         "factory": False,
         "test_rider": "Pol Espargaro",
         "color": "#FF6600"},

        {"name": "Yamaha", "budget": 6200000,
         "bike": {"engine": 87, "aero": 85, "reliability": 83},
         "factory": True,
         "test_rider": "Augusto Fernandez",
         "color": "#0A1E5E"},

        {"name": "Pramac", "budget": 5000000,
         "bike": {"engine": 87, "aero": 84, "reliability": 82},
         "factory": False,
         "test_rider": None,
         "color": "#6B21A8"},

        {"name": "Honda", "budget": 5800000,
         "bike": {"engine": 85, "aero": 82, "reliability": 80},
         "factory": True,
         "test_rider": "Aleix Espargaro",
         "color": "#FF0000"},

        {"name": "LCR", "budget": 4200000,
         "bike": {"engine": 84, "aero": 81, "reliability": 79},
         "factory": False,
         "test_rider": "Takaaki Nakagami",
         "color": "#FFFFFF"},
    ]

def regen_rider():
    names = ["R. Diaz", "M. Rossi", "K. Tanaka", "J. Smith"]
    return {
        "name": random.choice(names),
        "team": None,
        "skill": random.randint(65, 80),
        "trait": "Rookie",
        "points": 0,
        "age": 20,
        "salary": 80000
    }