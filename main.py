import tkinter as tk
from tkinter import ttk, messagebox
import pycountry
import random
from faker import Faker

from data import generate_riders, generate_teams
from race import simulate_race
from economy import calculate_income, pay_salaries, upgrade_bike
from save_load import save_game, load_game

from manager import roll_skills, generate_ai_managers, apply_trait_effect, TRAITS

# ================= STATE =================
riders = []
teams = []
ai_managers = []
season = 1
manager = {}
player_team_index = 0

countries = sorted([c.name for c in pycountry.countries])

# ================= LOCALE =================
COUNTRY_LOCALE_MAP = {
    "Italy": "it_IT", "Spain": "es_ES", "France": "fr_FR",
    "Germany": "de_DE", "United Kingdom": "en_GB",
    "United States": "en_US", "Indonesia": "id_ID",
    "Japan": "ja_JP", "Brazil": "pt_BR"
}

def get_locale(country):
    return COUNTRY_LOCALE_MAP.get(country, "en_US")

# ================= UI BASE =================
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

# ================= MANAGER SETUP =================
def show_manager_setup():
    clear_window()

    tk.Label(root, text="Create Manager", font=("Arial",18,"bold")).pack(pady=10)

    box = tk.Frame(root)
    box.pack()

    left = tk.Frame(box)
    left.grid(row=0, column=0, padx=30)

    right = tk.Frame(box)
    right.grid(row=0, column=1, padx=30)

    # INPUT
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
    rep_var = tk.StringVar(value="Newcomer")
    rep_box = ttk.Combobox(left, textvariable=rep_var, width=18,
                           values=["Newcomer", "Known Manager", "Elite Manager"])
    rep_box.grid(row=7, column=0)

    tk.Label(left, text="Trait").grid(row=8, column=0, sticky="w")
    trait_var = tk.StringVar(value="No Trait")
    ttk.Combobox(left, textvariable=trait_var, width=18,
                 values=list(TRAITS.keys())).grid(row=9, column=0)

    # SKILL DISPLAY
    tk.Label(right, text="Manager Skills", font=("Arial",12,"bold")).grid(row=0, column=0)

    skill_text = tk.Label(right, font=("Arial",11), justify="left")
    skill_text.grid(row=1, column=0)

    skills_ui = {}
    skills_real = {}

    def roll():
        nonlocal skills_ui, skills_real
        skills_ui, skills_real = roll_skills(rep_var.get())

        skill_text.config(text=
            f"{'Negotiation':<18}: {skills_ui['negotiation']}\n"
            f"{'Engineering':<18}: {skills_ui['engineering']}\n"
            f"{'Rider Management':<18}: {skills_ui['rider_management']}\n"
            f"{'Feedback':<18}: {skills_ui['feedback']}"
        )

    # AUTO ROLL
    roll()

    # AUTO REROLL SAAT GANTI REPUTASI
    rep_var.trace_add("write", lambda *args: roll())

    tk.Button(right, text="Reroll", command=roll).grid(row=2, column=0, pady=10)

    # ================= START =================
    def start_game():
        global riders, teams, manager, ai_managers, season

        try:
            name = name_entry.get().strip()
            country = country_var.get().strip()

            # AUTO COUNTRY
            if not country:
                country = random.choice(countries)

            # AUTO NAME VIA FAKER
            locale = get_locale(country)
            fake = Faker(locale)

            if not name:
                name = fake.name()

            # INIT GAME
            riders = generate_riders()
            teams = generate_teams()

            manager = {
                "name": name,
                "age": int(age_entry.get() or 30),
                "country": country,
                "trait": trait_var.get(),
                "reputation": rep_var.get(),
                "skills": skills_real
            }

            apply_trait_effect(manager)
            ai_managers = generate_ai_managers(teams)

            season = 1

            show_team_selection()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Start", command=start_game).pack(pady=10)
    tk.Button(root, text="Back", command=show_menu).pack()

# ================= TEAM SELECT =================
def get_player_team():
    return teams[player_team_index]

def show_team_selection():
    clear_window()

    index = [0]

    main = create_center_frame()

    title = tk.Label(main, text="Choose Your Team", font=("Arial", 18, "bold"))
    title.grid(row=0, column=0, columnspan=3, pady=10)

    team_frame = tk.Frame(main, bd=2, relief="solid", padx=20, pady=15)
    team_frame.grid(row=1, column=0, columnspan=3, pady=10)

    def get_team_riders(team_name):
        team_riders = [r["name"] for r in riders if r["team"] == team_name]
        if len(team_riders) == 0:
            return "-", "-", "-"
        if len(team_riders) == 1:
            return team_riders[0], "-", "-"
        if len(team_riders) == 2:
            return team_riders[0], team_riders[1], "-"
        return team_riders[0], team_riders[1], team_riders[2]

    def get_manager_name(i):
        if i < len(ai_managers):
            return ai_managers[i].get("name", "Unknown")
        return "Unknown"

    def render():
        for w in team_frame.winfo_children():
            w.destroy()

        i = index[0]
        t = teams[i]

        rider1, rider2, test_rider = get_team_riders(t["name"])

        manager_name = get_manager_name(i)

        color = t.get("color", "gray")

        status = "Factory" if t.get("factory") else "Satellite"

        if t["budget"] > 6000000:
            target = "Win Championship"
        elif t["budget"] > 4000000:
            target = "Podium Fight"
        else:
            target = "Midfield"

        tk.Label(team_frame, text=t["name"], font=("Arial", 16, "bold")).pack()

        tk.Label(team_frame, text=f"Color            : {color}").pack(anchor="w")
        tk.Label(team_frame, text=f"Engine           : {t['bike']['engine']}").pack(anchor="w")
        tk.Label(team_frame, text=f"Aero             : {t['bike']['aero']}").pack(anchor="w")
        tk.Label(team_frame, text=f"Reliability      : {t['bike']['reliability']}").pack(anchor="w")
        tk.Label(team_frame, text=f"Budget           : {t['budget']}").pack(anchor="w")

        tk.Label(team_frame, text="").pack()

        tk.Label(team_frame, text=f"Rider 1          : {rider1}").pack(anchor="w")
        tk.Label(team_frame, text=f"Rider 2          : {rider2}").pack(anchor="w")
        tk.Label(team_frame, text=f"Test Rider       : {test_rider}").pack(anchor="w")

        tk.Label(team_frame, text="").pack()

        tk.Label(team_frame, text=f"Manager          : {manager_name}").pack(anchor="w")
        tk.Label(team_frame, text=f"Status           : {status}").pack(anchor="w")
        tk.Label(team_frame, text=f"Target           : {target}").pack(anchor="w")

    def next_team():
        index[0] = (index[0] + 1) % len(teams)
        render()

    def prev_team():
        index[0] = (index[0] - 1) % len(teams)
        render()

    def select_team():
        global player_team_index
        player_team_index = index[0]
        show_game()

    tk.Button(main, text="<", width=5, command=prev_team).grid(row=2, column=0)
    tk.Button(main, text="Select", width=15, command=select_team).grid(row=2, column=1)
    tk.Button(main, text=">", width=5, command=next_team).grid(row=2, column=2)

    render()

def next_race():
    global season

    simulate_race(riders, teams, manager)

    for i, t in enumerate(teams):
        m = manager if i == player_team_index else ai_managers[i]
        t["budget"] += calculate_income(t, riders, m) - pay_salaries(t, riders)

    season += 1
    update_ui()

def do_upgrade():
    log.insert(tk.END, upgrade_bike(get_player_team(), manager) + "\n")

def save():
    save_game({
        "player_team_index": player_team_index,
        "riders": riders,
        "teams": teams,
        "season": season,
        "manager": manager,
        "ai_managers": ai_managers
    })

def update_ui():
    text.delete("1.0", tk.END)

    for i, r in enumerate(sorted(riders, key=lambda x: x["points"], reverse=True), 1):
        text.insert(tk.END, f"{i}. {r['name']} - {r['points']} pts\n")

    team = get_player_team()
    info.config(text=f"{manager['name']} | {team['name']} | Season {season} | {team['budget']}")

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

# ================= MENU =================
def new_game():
    show_manager_setup()

def resume_game():
    global riders, teams, season, manager, ai_managers, player_team_index

    data = load_game()
    if data:
        riders = data["riders"]
        teams = data["teams"]
        season = data["season"]
        manager = data["manager"]
        ai_managers = data["ai_managers"]
        player_team_index = data["player_team_index"]

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