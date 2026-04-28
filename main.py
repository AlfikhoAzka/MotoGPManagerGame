import tkinter as tk
from tkinter import ttk
import pycountry

from data import generate_riders, generate_teams
from race import simulate_race
from economy import calculate_income, pay_salaries, upgrade_bike
from save_load import save_game, load_game

from manager import roll_skills, generate_ai_managers, apply_trait_effect, TRAITS

riders = []
teams = []
ai_managers = []
season = 1
manager = {}
player_team_index = 0

countries = sorted([c.name for c in pycountry.countries])

root = tk.Tk()
root.title("MotoGP Manager")
root.geometry("750x600")
root.resizable(False, False)

def clear_window():
    for w in root.winfo_children():
        w.destroy()

def create_center_frame():
    wrap = tk.Frame(root)
    wrap.pack(expand=True)
    f = tk.Frame(wrap)
    f.pack()
    return f

def show_manager_setup():
    clear_window()

    tk.Label(root, text="Create Manager", font=("Arial",18,"bold")).pack(pady=10)

    box = tk.Frame(root)
    box.pack()

    left = tk.Frame(box)
    left.grid(row=0, column=0, padx=30)

    right = tk.Frame(box)
    right.grid(row=0, column=1, padx=30)

    tk.Label(left, text="Name").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(left)
    name_entry.grid(row=1, column=0)

    tk.Label(left, text="Age").grid(row=2, column=0, sticky="w")
    age_entry = tk.Entry(left)
    age_entry.insert(0, "30")
    age_entry.grid(row=3, column=0)

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
    trait_box["values"] = list(TRAITS.keys())
    trait_box.current(0)
    trait_box.grid(row=9, column=0)

    tk.Label(right, text="Manager Skills", font=("Arial",12,"bold")).grid(row=0, column=0)

    skill_text = tk.Label(right, font=("Arial",11), justify="left")
    skill_text.grid(row=1, column=0)

    skills_ui = {}
    skills_real = {}

    def roll():
        nonlocal skills_ui, skills_real

        skills_ui, skills_real = roll_skills()

        rep = rep_var.get()

        if rep == "Known Manager":
            skills_real = {k: min(20, v+2) for k,v in skills_real.items()}
        elif rep == "Elite Manager":
            skills_real = {k: min(20, v+4) for k,v in skills_real.items()}

        skill_text.config(
            text=
            f"{'Negotiation':<18}: {skills_ui['negotiation']}\n"
            f"{'Engineering':<18}: {skills_ui['engineering']}\n"
            f"{'Rider Management':<18}: {skills_ui['rider_management']}\n"
            f"{'Feedback':<18}: {skills_ui['feedback']}"
        )

    roll()

    tk.Button(right, text="Reroll", command=roll).grid(row=2, column=0, pady=10)

    def start_game():
        global riders, teams, manager, ai_managers, season

        riders = generate_riders()
        teams = generate_teams()

        manager = {
            "name": name_entry.get(),
            "age": int(age_entry.get() or 30),
            "country": country_var.get(),
            "trait": trait_var.get(),
            "reputation": rep_var.get(),
            "skills": skills_real
        }

        apply_trait_effect(manager)

        ai_managers = generate_ai_managers(teams)

        season = 1
        show_team_selection()

    tk.Button(root, text="Start", command=start_game).pack(pady=10)
    tk.Button(root, text="Back", command=show_menu).pack()

def get_player_team():
    return teams[player_team_index]

def show_team_selection():
    clear_window()

    tk.Label(root, text="Choose Your Team", font=("Arial",18,"bold")).pack(pady=10)

    container = tk.Frame(root)
    container.pack()

    for i, t in enumerate(teams):
        frame = tk.Frame(container, bd=1, relief="solid", padx=10, pady=5)
        frame.pack(pady=5, fill="x")

        tk.Label(frame, text=t["name"], font=("Arial",12,"bold")).pack(anchor="w")
        tk.Label(frame, text=f"Budget: {t['budget']}").pack(anchor="w")

        def select_team(index=i):
            global player_team_index
            player_team_index = index
            show_game()

        tk.Button(frame, text="Select", command=select_team).pack(anchor="e")

def next_race():
    global season

    simulate_race(riders, teams, manager)

    for i, t in enumerate(teams):
        if i == player_team_index:
            m = manager
        elif i < len(ai_managers):
            m = ai_managers[i]
        else:
            m = manager

        income = calculate_income(t, riders, m)
        salary = pay_salaries(t, riders)
        t["budget"] += income - salary

    season += 1
    update_ui()

def do_upgrade():
    msg = upgrade_bike(get_player_team(), manager)
    log.insert(tk.END, msg + "\n")

def save():
    save_game({
        "player_team_index": player_team_index,
        "riders": riders,
        "teams": teams,
        "season": season,
        "manager": manager,
        "ai_managers": ai_managers
    })
    log.insert(tk.END, "Saved\n")

def update_ui():
    text.delete("1.0", tk.END)

    sorted_riders = sorted(riders, key=lambda x: x["points"], reverse=True)

    for i, r in enumerate(sorted_riders, 1):
        text.insert(tk.END, f"{i}. {r['name']} - {r['points']} pts\n")

    team = get_player_team()

    info.config(
        text=f"{manager.get('name')} | Team: {team['name']} | Season {season} | Budget {team['budget']}"
    )

def show_game():
    clear_window()
    main = create_center_frame()

    top = tk.Frame(main)
    top.grid(row=0, column=0)

    tk.Button(top, text="Next Race", command=next_race).grid(row=0, column=0)
    tk.Button(top, text="Upgrade", command=do_upgrade).grid(row=0, column=1)
    tk.Button(top, text="Save", command=save).grid(row=0, column=2)
    tk.Button(top, text="Menu", command=show_menu).grid(row=0, column=3)

    global info, text, log

    info = tk.Label(main)
    info.grid(row=1, column=0)

    content = tk.Frame(main)
    content.grid(row=2, column=0)

    text = tk.Text(content, width=40, height=15)
    text.grid(row=0, column=0)

    log = tk.Text(content, width=30, height=15)
    log.grid(row=0, column=1)

    update_ui()

def new_game():
    show_manager_setup()

def resume_game():
    global riders, teams, season, manager, ai_managers, player_team_index

    data = load_game()
    if data:
        riders = data["riders"]
        teams = data["teams"]
        season = data["season"]
        manager = data.get("manager", {})
        ai_managers = data.get("ai_managers", [])
        player_team_index = data.get("player_team_index", 0)

    show_game()

def show_menu():
    clear_window()
    f = create_center_frame()

    tk.Label(f, text="MotoGP Manager", font=("Arial",20)).grid(row=0, column=0, pady=20)

    tk.Button(f, text="New Game", width=25, command=new_game).grid(row=1, column=0)

    if load_game():
        tk.Button(f, text="Resume", width=25, command=resume_game).grid(row=2, column=0)

    tk.Button(f, text="Quit", width=25, command=root.quit).grid(row=3, column=0)

show_menu()
root.mainloop()