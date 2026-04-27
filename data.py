import random

def generate_riders():
    return [
        {"name": "Francesco Bagnaia", "team": "Ducati", "skill": 92, "trait": "Champion", "points": 0, "age": 27, "salary": 300000},
        {"name": "Jorge Martin", "team": "Aprilia", "skill": 90, "trait": "Aggressive", "points": 0, "age": 26, "salary": 250000},
        {"name": "Marc Marquez", "team": "Ducati", "skill": 93, "trait": "GOAT", "points": 0, "age": 31, "salary": 320000},
        {"name": "Fabio Quartararo", "team": "Yamaha", "skill": 89, "trait": "Smooth", "points": 0, "age": 25, "salary": 280000},
        {"name": "Brad Binder", "team": "KTM", "skill": 87, "trait": "Consistent", "points": 0, "age": 28, "salary": 220000},
        {"name": "Enea Bastianini", "team": "Tech3", "skill": 88, "trait": "Late Braker", "points": 0, "age": 26, "salary": 240000},
    ]

def generate_teams():
    return [
        {"name": "Ducati", "budget": 5000000, "bike": {"engine": 80, "aero": 78, "reliability": 75}, "factory": True},
        {"name": "Aprilia", "budget": 3000000, "bike": {"engine": 75, "aero": 74, "reliability": 70}, "factory": True},
        {"name": "Tech3", "budget": 7000000, "bike": {"engine": 90, "aero": 88, "reliability": 85}, "factory": False},
        {"name": "Yamaha", "budget": 6800000, "bike": {"engine": 89, "aero": 87, "reliability": 84}, "factory": True},
        {"name": "KTM", "budget": 4000000, "bike": {"engine": 85, "aero": 82, "reliability": 80}, "factory": True},
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