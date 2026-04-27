import tkinter as tk
from tkinter import ttk
import pycountry
import random

from data import generate_riders, generate_teams
from race import simulate_race
from economy import calculate_income, pay_salaries, upgrade_bike
from save_load import save_game, load_game

riders = []
teams = []
season = 1
manager = {}

countries = sorted([c.name for c in pycountry.countries])

root = tk.Tk()
root.title("MotoGP Manager")
root.geometry("750x600")
root.resizable(False, False)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def create_center_frame():
    wrapper = tk.Frame(root)
    wrapper.pack(expand=True)
    frame = tk.Frame(wrapper)
    frame.pack()
    return frame

def roll_skills():
    return {
        "negotiation": random.randint(2, 5),
        "engineering": random.randint(2, 5),
        "rider_management": random.randint(2, 5),
        "feedback": random.randint(2, 5)
    }

def show_manager_setup():
    clear_window()

    tk.Label(root, text="Create Manager", font=("Arial", 18, "bold")).pack(pady=10)

    container = tk.Frame(root)
    container.pack(pady=10)

    left = tk.Frame(container)
    left.grid(row=0, column=0, padx=30)

    right = tk.Frame(container)
    right.grid(row=0, column=1, padx=30)

    tk.Label(left, text="Name").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(left)
    name_entry.grid(row=1, column=0, pady=5)

    tk.Label(left, text="Age").grid(row=2, column=0, sticky="w")
    age_entry = tk.Entry(left)
    age_entry.insert(0, "30")
    age_entry.grid(row=3, column=0, pady=5)

    tk.Label(left, text="Country").grid(row=4, column=0, sticky="w")
    country_var = tk.StringVar()
    ttk.Combobox(left, textvariable=country_var, values=countries, width=18).grid(row=5, column=0)

    tk.Label(left, text="Reputation").grid(row=6, column=0, sticky="w")
    rep_var = tk.StringVar()
    rep_box = ttk.Combobox(left, textvariable=rep_var, width=18)
    rep_box["values"] = ["Newcomer", "Known Manager", "Elite Manager"]
    rep_box.current(0)
    rep_box.grid(row=7, column=0)

    tk.Label(left, text="Trait").grid(row=8, column=0, sticky="w")
    trait_var = tk.StringVar()
    trait_box = ttk.Combobox(left, textvariable=trait_var, width=18)
    trait_box["values"] = [
        "No Trait",
        "Former F1 Employee",
        "Ex MotoGP Rider",
        "Former Businessman",
        "Technical Genius",
        "People Person",
        "Data Driven"
    ]
    trait_box.current(0)
    trait_box.grid(row=9, column=0)

    tk.Label(right, text="Manager Skills", font=("Arial", 12, "bold")).grid(row=0, column=0)

    skill_text = tk.Label(right, text="", justify="left", font=("Arial", 11))
    skill_text.grid(row=1, column=0)

    rolled_skills = {}

    def roll():
        nonlocal rolled_skills
        rolled_skills = roll_skills()

        skill_text.config(
            text=
            f"Negotiation: {rolled_skills['negotiation']}\n"
            f"Engineering: {rolled_skills['engineering']}\n"
            f"Rider Mgmt: {rolled_skills['rider_management']}\n"
            f"Feedback: {rolled_skills['feedback']}"
        )

    roll()

    tk.Button(right, text="Reroll", command=roll).grid(row=2, column=0, pady=10)

    def start_game():
        global riders, teams, season, manager

        manager = {
            "name": name_entry.get(),
            "age": int(age_entry.get() or 30),
            "country": country_var.get(),
            "trait": trait_var.get(),
            "reputation": rep_var.get(),
            "skills": rolled_skills
        }

        riders = generate_riders()
        teams = generate_teams()
        season = 1

        show_game()

    tk.Button(root, text="Start Career", command=start_game).pack(pady=10)
    tk.Button(root, text="Back", command=show_menu).pack()

def get_player_team():
    return teams[0]

def next_race():
    global season
    simulate_race(riders, teams, manager)

    for t in teams:
        income = calculate_income(t, riders, manager)
        salary = pay_salaries(t, riders)
        t["budget"] += income - salary

    season += 1
    update_ui()

def do_upgrade():
    msg = upgrade_bike(get_player_team(), manager)
    log.insert(tk.END, msg + "\n")
    update_ui()

def save():
    save_game({
        "riders": riders,
        "teams": teams,
        "season": season,
        "manager": manager
    })
    log.insert(tk.END, "Saved\n")

def update_ui():
    text.delete("1.0", tk.END)

    sorted_riders = sorted(riders, key=lambda x: x["points"], reverse=True)

    for i, r in enumerate(sorted_riders, 1):
        text.insert(tk.END, f"{i}. {r['name']} - {r['points']} pts\n")

    team = get_player_team()

    info.config(
        text=f"{manager.get('name')} | {manager.get('trait')} | Season {season} | Budget {team['budget']}"
    )

def show_game():
    clear_window()
    main = create_center_frame()

    top = tk.Frame(main)
    top.grid(row=0, column=0, pady=10)

    tk.Button(top, text="Next Race", command=next_race).grid(row=0, column=0, padx=5)
    tk.Button(top, text="Upgrade", command=do_upgrade).grid(row=0, column=1, padx=5)
    tk.Button(top, text="Save", command=save).grid(row=0, column=2, padx=5)
    tk.Button(top, text="Menu", command=show_menu).grid(row=0, column=3, padx=5)

    global info, text, log

    info = tk.Label(main, text="")
    info.grid(row=1, column=0)

    content = tk.Frame(main)
    content.grid(row=2, column=0)

    text = tk.Text(content, width=40, height=15)
    text.grid(row=0, column=0, padx=10)

    log = tk.Text(content, width=30, height=15)
    log.grid(row=0, column=1, padx=10)

    update_ui()

def new_game():
    show_manager_setup()

def resume_game():
    global riders, teams, season, manager
    data = load_game()
    if data:
        riders = data["riders"]
        teams = data["teams"]
        season = data["season"]
        manager = data.get("manager", {})
    show_game()

def show_settings():
    clear_window()
    f = create_center_frame()
    tk.Label(f, text="Settings").grid(row=0, column=0)
    tk.Button(f, text="Back", command=show_menu).grid(row=1, column=0)

def show_editor():
    clear_window()
    f = create_center_frame()

    editor = tk.Text(f, width=60, height=20)
    editor.grid(row=0, column=0)

    data = load_game()
    if data:
        import json
        editor.insert(tk.END, json.dumps(data, indent=2))

    def save_edit():
        import json
        save_game(json.loads(editor.get("1.0", tk.END)))

    tk.Button(f, text="Save", command=save_edit).grid(row=1, column=0)
    tk.Button(f, text="Back", command=show_menu).grid(row=2, column=0)

def show_menu():
    clear_window()
    f = create_center_frame()

    tk.Label(f, text="MotoGP Manager", font=("Arial", 20)).grid(row=0, column=0, pady=20)

    tk.Button(f, text="New Game", width=25, command=new_game).grid(row=1, column=0, pady=5)

    if load_game():
        tk.Button(f, text="Resume", width=25, command=resume_game).grid(row=2, column=0, pady=5)

    tk.Button(f, text="Quit", width=25, command=root.quit).grid(row=3, column=0, pady=5)

show_menu()
root.mainloop()