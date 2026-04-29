import tkinter as tk
from tkinter import ttk, messagebox
from turtle import color
import pycountry
import random
from faker import Faker

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

COUNTRY_LOCALE_MAP = {
    "Italy": "it_IT", "Spain": "es_ES", "France": "fr_FR",
    "Germany": "de_DE", "United Kingdom": "en_GB",
    "United States": "en_US", "Indonesia": "id_ID",
    "Japan": "ja_JP", "Brazil": "pt_BR"
}

def get_locale(country):
    return COUNTRY_LOCALE_MAP.get(country, "en_US")

root = tk.Tk()
default_font = ("Segoe UI", 10)
root.option_add("*Font", default_font)
BG_MAIN   = "#181818"
BG_PANEL  = "#202020"
BG_CARD   = "#262626"
BG_INNER  = "#2a2a2a"
BG_HOVER  = "#303030"

TEXT_MAIN = "#d0d0d0"
TEXT_DIM  = "#9a9a9a"

ACCENT    = "#e53935"
BORDER    = "#2f2f2f"

# apply ke root
root.configure(bg=BG_MAIN)

# ttk fix
style = ttk.Style()
style.theme_use("default")

style.configure("TCombobox",
    fieldbackground=BG_PANEL,
    background=BG_PANEL,
    foreground=TEXT_MAIN
)

def create_layout():
    clear_window()

    container = tk.Frame(root, bg=BG_MAIN, bd=0, highlightthickness=0)
    container.pack(fill="both", expand=True)
 
    sidebar = tk.Frame(container, width=200, bg=BG_PANEL, bd=0, highlightthickness=0)
    sidebar.pack(side="left", fill="y")

    content = tk.Frame(container, bg=BG_MAIN, bd=0, highlightthickness=0)
    content.pack(side="right", fill="both", expand=True)

    return sidebar, content
root.title("MotoGP Manager")
root.geometry("750x600")
root.resizable(True, True)

def clear_window():
    for w in root.winfo_children():
        w.destroy()

def create_center_frame():
    wrap = tk.Frame(root, bg=BG_MAIN, bd=0, highlightthickness=0)
    wrap.pack(expand=True)
    f = tk.Frame(wrap, bg=BG_MAIN, bd=0, highlightthickness=0)
    f.pack()
    return f

def show_manager_setup():
    clear_window()

    tk.Label(root, text="Create Manager", bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI",18,"bold")).pack(pady=10)

    box = tk.Frame(root, bg=BG_MAIN, bd=0, highlightthickness=0)
    box.pack()

    left = tk.Frame(box, bg=BG_MAIN, bd=0, highlightthickness=0)
    left.grid(row=0, column=0, padx=30)

    right = tk.Frame(box, bg=BG_MAIN, bd=0, highlightthickness=0)
    right.grid(row=0, column=1, padx=30)

    tk.Label(left, text="Name", bg=BG_MAIN, fg=TEXT_MAIN).grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(left, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN)
    name_entry.grid(row=1, column=0)

    tk.Label(left, text="Age", bg=BG_MAIN, fg=TEXT_MAIN).grid(row=2, column=0, sticky="w")
    age_entry = tk.Entry(left, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN)
    age_entry.insert(0, "30")
    age_entry.grid(row=3, column=0)

    tk.Label(left, text="Country", bg=BG_MAIN, fg=TEXT_MAIN).grid(row=4, column=0, sticky="w")
    country_var = tk.StringVar()
    ttk.Combobox(left, textvariable=country_var, values=countries, width=18).grid(row=5, column=0)

    tk.Label(left, text="Reputation", bg=BG_MAIN, fg=TEXT_MAIN).grid(row=6, column=0, sticky="w")
    rep_var = tk.StringVar(value="Newcomer")
    rep_box = ttk.Combobox(left, textvariable=rep_var, width=18,
                           values=["Newcomer", "Known Manager", "Elite Manager"])
    rep_box.grid(row=7, column=0)

    tk.Label(left, text="Trait", bg=BG_MAIN, fg=TEXT_MAIN).grid(row=8, column=0, sticky="w")
    trait_var = tk.StringVar(value="No Trait")
    ttk.Combobox(left, textvariable=trait_var, width=18,
                 values=list(TRAITS.keys())).grid(row=9, column=0)

    tk.Label(right, text="Manager Skills", bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI",12,"bold")).grid(row=0, column=0)

    skill_text = tk.Label(right, bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI",11), justify="left")
    skill_text.grid(row=1, column=0)

    skills_ui = {}
    skills_real = {}

    def roll():
        nonlocal skills_ui, skills_real
        skills_ui, skills_real = roll_skills(rep_var.get())

        skill_text.config(text=
            f"{'Negotiation':<20}: {skills_ui['negotiation']}\n"
            f"{'Engineering':<20}: {skills_ui['engineering']}\n"
            f"{'Rider Management':<20}: {skills_ui['rider_management']}\n"
            f"{'Feedback':<20}: {skills_ui['feedback']}"
        )

    roll()

    rep_var.trace_add("write", lambda *args: roll())

    tk.Button(right, text="Reroll", command=roll).grid(row=2, column=0, pady=10)

    def start_game():
        global riders, teams, manager, ai_managers, season

        try:
            name = name_entry.get().strip()
            country = country_var.get().strip()

            if not country:
                country = random.choice(countries)

            locale = get_locale(country)
            fake = Faker(locale)

            if not name:
                name = fake.name()

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

    tk.Button(root, text="Start", bg= BG_PANEL, fg=TEXT_MAIN, command=start_game).pack(pady=10)
    tk.Button(root, text="Back", bg= BG_PANEL, fg=TEXT_MAIN, command=show_menu).pack()

def get_player_team():
    return teams[player_team_index]

def show_team_selection():
    clear_window()

    index = [0]

    TITLE_FONT = ("Segoe UI", 16, "bold")
    TEAM_FONT = ("Segoe UI", 18, "bold")
    TEXT_FONT = ("Segoe UI", 10)

    # ======================
    # MAIN CONTAINER
    # ======================
    container = tk.Frame(root, bg=BG_MAIN)
    container.pack(fill="both", expand=True)

    # ======================
    # LEFT PANEL
    # ======================
    left_panel = tk.Frame(container, width=220, bg=BG_PANEL)
    left_panel.pack(side="left", fill="y")

    tk.Label(left_panel, text="Teams",
             fg="white", bg=BG_PANEL,
             font=TITLE_FONT).pack(pady=10)

    card_container = tk.Frame(left_panel, bg=BG_INNER)
    card_container.pack(fill="y", expand=True)

    # ======================
    # RIGHT PANEL
    # ======================
    right_panel = tk.Frame(container, bg=BG_MAIN, bd=0, highlightthickness=0)
    right_panel.pack(side="right", fill="both", expand=True)

    top_bar = tk.Frame(right_panel, bg=BG_MAIN, bd=0, highlightthickness=0)
    top_bar.pack(fill="x")

    btn_select = tk.Button(top_bar, text="Select Team", width=15, bg=ACCENT, fg="white", activebackground="#b71c1c", relief="flat")
    btn_select.pack(side="right", padx=10, pady=10)

    content = tk.Frame(right_panel, bg=BG_MAIN, bd=0, highlightthickness=0)
    content.pack(fill="both", expand=True)

    # ======================
    # HELPER
    # ======================
    def get_text_color(bg):
        bg = bg.lstrip("#")
        r, g, b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
        brightness = (r*299 + g*587 + b*114) / 1000
        return "black" if brightness > 128 else "white"

    # ======================
    # RENDER CARD
    # ======================
    def render():
        for w in content.winfo_children():
            w.destroy()

        i = index[0]
        t = teams[i]

        color = t.get("color", "#444444")
        text_color = get_text_color(color)

        btn_select.configure(bg=color, fg=text_color)

        # SHADOW
        shadow = tk.Frame(content, bg="#000000")
        shadow.place(relx=0.5, rely=0.5, anchor="center",
                     width=420, height=440)

        # CARD
        card = tk.Frame(content, bg=BG_CARD, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center",
                   width=400, height=420)

        inner = tk.Frame(card, bg=BG_INNER, bd=0, highlightthickness=0)
        inner.pack(expand=True)

        # DATA
        team_riders = [r["name"] for r in riders if r["team"] == t["name"]]

        rider1 = team_riders[0] if len(team_riders) > 0 else "-"
        rider2 = team_riders[1] if len(team_riders) > 1 else "-"
        test_rider = t.get("test_rider") or "-"

        manager_name = ai_managers[i]["name"] if i < len(ai_managers) else "Unknown"

        status = "Factory" if t.get("factory") else "Satellite"

        if t["budget"] > 6000000:
            target = "Win Championship"
        elif t["budget"] > 4000000:
            target = "Podium Fight"
        else:
            target = "Midfield"

        # TITLE
        tk.Label(inner, text=t["name"],
                 font=TEAM_FONT,
                 bg=BG_INNER,
                 fg=color).pack(pady=(15, 10))

        def add(text):
            tk.Label(inner,
                     text=text,
                     font=TEXT_FONT,
                     bg=BG_INNER,
                     fg=TEXT_MAIN).pack(pady=2)

        add(f"Engine: {t['bike']['engine']}")
        add(f"Aero: {t['bike']['aero']}")
        add(f"Reliability: {t['bike']['reliability']}")
        add(f"Budget: {t['budget']}")

        tk.Label(inner, text="", bg="#2f2f2f").pack()

        add(f"Rider 1: {rider1}")
        add(f"Rider 2: {rider2}")
        add(f"Test Rider: {test_rider}")

        tk.Label(inner, text="", bg="#2f2f2f").pack()

        add(f"Manager: {manager_name}")
        add(f"Status: {status}")
        add(f"Target: {target}")

    # ======================
    # TEAM LIST
    # ======================
    def create_team_card(parent, team_name, idx):
        card = tk.Frame(parent, bg=BG_PANEL, padx=10, pady=8, bd=0, highlightthickness=0)
        card.pack(fill="x", padx=10, pady=5)

        label = tk.Label(card, text=team_name, bg=BG_PANEL, fg=TEXT_MAIN)
        label.pack(anchor="w")

        def on_enter(e):
            card.configure(bg=BG_HOVER)
            label.configure(bg=BG_HOVER)

        def on_leave(e):
            card.configure(bg=BG_PANEL)
            label.configure(bg=BG_PANEL)

        def on_click(e):
            index[0] = idx
            render()

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", on_click)

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Button-1>", on_click)

    for i, t in enumerate(teams):
        create_team_card(card_container, t["name"], i)

    # ======================
    # SELECT BUTTON
    # ======================
    def select_team():
        global player_team_index
        player_team_index = index[0]
        show_game()

    btn_select.configure(command=select_team)

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
    sidebar, content = create_layout()

    TITLE_FONT = ("Segoe UI", 14, "bold")
    TEXT_FONT = ("Segoe UI", 10)

    tk.Label(sidebar, text="Menu", fg="white", bg=BG_PANEL, font=TITLE_FONT).pack(pady=10)

    tk.Button(sidebar, text="Next Race", width=20, bg=BG_PANEL, fg=TEXT_MAIN, command=next_race).pack(pady=5)

    tk.Button(sidebar, text="Upgrade Bike", width=20, bg=BG_PANEL, fg=TEXT_MAIN, command=do_upgrade).pack(pady=5)

    tk.Button(sidebar, text="Save", width=20, bg=BG_PANEL, fg=TEXT_MAIN, command=save).pack(pady=5)

    tk.Button(sidebar, text="Main Menu", width=20, bg=BG_PANEL, fg=TEXT_MAIN, command=show_menu).pack(pady=5)

    top = tk.Frame(content, bg=BG_MAIN, bd=0, highlightthickness=0)
    top.pack(fill="x")

    global info, text, log

    info = tk.Label(top, font=TEXT_FONT, bg=BG_MAIN, fg=TEXT_MAIN)
    info.pack(anchor="w", padx=10, pady=10)

    main_area = tk.Frame(content, bg=BG_MAIN, bd=0, highlightthickness=0)
    main_area.pack(fill="both", expand=True)

    text = tk.Text(main_area, width=40, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN)
    text.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    log = tk.Text(main_area, width=30, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN)
    log.pack(side="right", fill="y", padx=10, pady=10)

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
        manager = data["manager"]
        ai_managers = data["ai_managers"]
        player_team_index = data["player_team_index"]

    show_game()

def show_menu():
    clear_window()

    TITLE_FONT = ("Segoe UI", 24, "bold")
    BTN_FONT = ("Segoe UI", 11)

    wrapper = tk.Frame(root, bg=BG_MAIN, bd=0, highlightthickness=0)
    wrapper.pack(expand=True)

    container = tk.Frame(wrapper, bg=BG_MAIN, bd=0, highlightthickness=0)
    container.pack()

    tk.Label(container,
        text="MotoGP Manager",
        font=TITLE_FONT,
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(0, 20))

    tk.Button(container,
        text="New Game",
        width=25,
        font=BTN_FONT,
        bg=BG_PANEL,
        fg=TEXT_MAIN,
        activebackground=BG_HOVER,
        activeforeground=TEXT_MAIN,
        relief="flat",
        command=new_game
    ).pack(pady=5)

    if load_game():
        tk.Button(container,
                  text="Resume",
                  width=25,
                  font=BTN_FONT,
                  bg=BG_PANEL,
                  fg=TEXT_MAIN,
                  activebackground=BG_HOVER,
                  activeforeground=TEXT_MAIN,
                  relief="flat",
                  command=resume_game)\
            .pack(pady=5)

    tk.Button(container,
              text="Quit",
              width=25,
              font=BTN_FONT,
              bg=BG_PANEL,
              fg=TEXT_MAIN,
              activebackground=BG_HOVER,
              activeforeground=TEXT_MAIN,
              relief="flat",
              command=root.quit)\
        .pack(pady=5)

show_menu()
root.mainloop()