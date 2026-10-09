# ==========================================
# 0. IMPORTATION DE TOUTES LES LIBRAIRIES
# ==========================================


from tkinter import *
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# 1. CONFIGURATION
# ==========================================

DOSSIER_IMAGES = r"C:\Users\fortu\Desktop\Livrable Greensky\Images"  # Chemin du dossier image

THEME_COLOR = "#4DAA5A"  # Vert Greensky


POLICE_TITRE = "Elephant Pro"  # Pour le gros titre en haut
POLICE_CORPS = "Aptos Display"  # Pour le texte, les questions, les boutons

# ==========================================
# 2. DONNÉES
# ==========================================

DATA_DB = {  # Defini tout le dictionnaire qui traduit notre base de donnée
    "MATERIAUX": {
        "Métal": {
            "Acier Standard": 2,  #
            "Acier Inox": 6.1,
            "Aluminium (Vierge)": 17,  #
            "Aluminium (Recyclé)": 2.0,
            "Cuivre": 4,  #
        },
        "Plastique": {
            "PET (Bouteille)": 2.2,  #
            "PVC": 3,  #
            "ABS": 3.1,
            "Polypropylène": 2.0,
            "Plastique Recyclé": 0.5,
        },
        "Bois": {  #
            "Pin/Sapin": 0.4,
            "Chêne": 0.6,
            "Contreplaqué": 0.9,
            "Bois Recyclé": 0.1,
        },
        "Textile": {
            "Coton": 16,  #
            "Polyester": 2.1,
            "Laine": 15.0,
            "Chanvre": 1.5,
        },
        "Autre": {"Verre": 0.9, "Céramique": 0.8, "Papier/Carton": 0.9},
    },
    "FABRICATION": {
        "Inconnue / Aucune": 0.0,
        "Moulage Injection": 3,  #
        "Usinage CNC (Métal)": 0.1,  #
        "Forge": 0.5,  #
        "Assemblage Manuel": 0.1,
        "Impression 3D": 1.2,
    },
    "TRANSPORT": {
        "Camion (Routier)": 0.1,  #
        "Bateau (Maritime)": 0.009,  #
        "Avion (Cargo)": 1.25,  #
        "Train (Fret)": 0.0175,  #
        "Camionnette": 0.2,
    },
    "ENERGIE": {
        "Électricité (Mix France)": 0.06,
        "Électricité (Mix Europe)": 0.40,
        "Électricité (Charbon/Monde)": 1,  #
        "Gaz Naturel": 0.443,  #
        "Fioul": 0.7,  #
        "Solaire": 0.04,
    },
}

# ==========================================
# 3. DEFINITION DES FONCTIONS
# ==========================================


# Genère les conseils de fin
def generer_conseils(details, choix_utilisateurs):
    conseils = []
    pire_etape = max(details, key=details.get)
    conseils.append(
        f"⚠️ Votre impact principal vient de : {pire_etape.upper()}."
    )

    mat = choix_utilisateurs["materiau"]
    if "Aluminium (Vierge)" in mat:
        conseils.append("💡 Utilisez de l'Aluminium Recyclé.")
    if "Inox" in mat:
        conseils.append(
            "💡 L'Inox a un impact fort. L'Acier Standard est mieux."
        )

    trans = choix_utilisateurs["transport"]
    if "Avion" in trans:
        conseils.append("✈️ ALERTE : L'avion émet 60x plus que le bateau.")

    ener = choix_utilisateurs["energie"]
    if "Charbon" in ener or "Fioul" in ener:
        conseils.append("⚡ Passez aux EnR.")

    return conseils


# Met à jour le 2e menu déroulant selon le 1er
def update_materiau_combo(event):
    cat = combo_cat_mat.get()
    choix = list(DATA_DB["MATERIAUX"].get(cat, {}).keys())
    combo_mat["values"] = choix
    if choix:
        combo_mat.current(0)


# Affichage de la fenêtre de réponse
def show_result_window(nom, total, details, conseils_liste):
    res_win = Toplevel(root)
    res_win.title(f"Résultat : {nom}")
    try:
        res_win.state("zoomed")
    except:
        res_win.attributes("-fullscreen", True)

    # Titre de la page de resultat
    header_frame = Frame(res_win, bg=THEME_COLOR, height=80)
    header_frame.pack(fill="x", side="top")
    Label(
        header_frame,
        text=f"RÉSULTAT ACV : {nom.upper()}",
        font=(POLICE_TITRE, 24),
        bg=THEME_COLOR,
        fg="white",
    ).pack(pady=20)

    main_content = ttk.Frame(res_win)
    main_content.pack(fill=BOTH, expand=True, padx=30, pady=20)  # $

    # Travail sur la fenêtre de gauche (graphe)
    left_frame = ttk.Frame(main_content)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 20))

    # Zone où l'on affiche le resultat de l'ACV
    ttk.Label(
        left_frame,
        text="TOTAL IMPACT CARBONE",
        font=(POLICE_CORPS, 14, "bold"),
        foreground="grey",
    ).pack(pady=(10, 5))
    ttk.Label(
        left_frame,
        text=f"{total:.2f} kg CO2e",
        font=(POLICE_CORPS, 30, "bold"),
        foreground="#d9534f",
    ).pack(pady=(0, 20))

    # Création de notre craphique + affichage de ce dernier sur la fenetre de resultat
    plt.rcParams["font.family"] = POLICE_CORPS

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(
        list(details.keys()),
        list(details.values()),
        color=["#3498db", "#9b59b6", "#f1c40f", "#2ecc71"],
    )
    ax.bar_label(bars, fmt="%.1f")
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Travail sur la fenêtre de droite
    right_frame = Frame(main_content, bg="white")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Affichage de l'image dans la fenetre de resultat
    try:
        chemin_complet = f"{DOSSIER_IMAGES}/{nom.strip()}.jpg"
        pil_img = Image.open(chemin_complet)
        base_width = 300
        w_percent = base_width / float(pil_img.size[0])
        h_size = int((float(pil_img.size[1]) * float(w_percent)))
        pil_img = pil_img.resize(
            (base_width, h_size), Image.Resampling.LANCZOS
        )
        tk_img = ImageTk.PhotoImage(pil_img)
        img_lbl = Label(right_frame, image=tk_img, bg="white")
        img_lbl.image = tk_img
        img_lbl.pack(pady=20)
    except:
        pass

    # Affichage des conseils
    advice_frame = LabelFrame(
        right_frame,
        text=" 💡 CONSEILS ",
        font=(POLICE_CORPS, 16, "bold"),
        bg="#f0fdf4",
        fg="#166534",
        bd=2,
        relief="flat",
    )
    advice_frame.pack(fill="both", expand=True, pady=20, padx=10)

    for conseil in conseils_liste:
        lbl = Label(
            advice_frame,
            text=conseil,
            font=(POLICE_CORPS, 14),
            bg="#f0fdf4",
            fg="#333",
            justify="left",
            wraplength=400,
            anchor="w",
        )
        lbl.pack(fill="x", pady=10, padx=20)
    # Bouton pour fermé la page de resultat
    Button(
        res_win,
        text="FERMER",
        bg="#555",
        fg="white",
        font=(POLICE_CORPS, 12),
        command=res_win.destroy,
    ).pack(pady=10)


# Focntion qui pemet de calculer notre ACV
def calculer():
    try:
        # Vérification des champs de valeurs (float ou non) + récupération des données de l'utilisateur
        nom = nom_var.get()
        masse = float(masse_var.get())
        dist = float(dist_var.get())
        conso = float(conso_var.get())
        duree = int(duree_var.get())

        c_cat, c_mat = combo_cat_mat.get(), combo_mat.get()
        c_fab, c_trans, c_ener = (
            combo_fab.get(),
            combo_trans.get(),
            combo_ener.get(),
        )
        # Verification de si l'utilisateur a bien renseigner le materiau
        if not c_mat or not c_cat:
            raise ValueError("Matériau")

        f_mat = DATA_DB["MATERIAUX"][c_cat][c_mat]
        f_fab = DATA_DB["FABRICATION"][c_fab]
        f_trans = DATA_DB["TRANSPORT"][c_trans]
        f_ener = DATA_DB["ENERGIE"][c_ener]
        # calcul des 4 etapes de l'ACV
        i_mat = f_mat * masse
        i_fab = f_fab * masse
        i_trans = f_trans * dist * masse
        i_usage = f_ener * conso * duree

        total = i_mat + i_fab + i_trans + i_usage
        # enregistrement des caracteristique de l'objet
        details = {
            "Matière": i_mat,
            "Fabrication": i_fab,
            "Transport": i_trans,
            "Usage": i_usage,
        }
        choix = {
            "materiau": c_mat,
            "transport": c_trans,
            "energie": c_ener,
            "distance": dist,
            "conso": conso,
        }
        # on appele la fonction qui affiche notre page de resultat
        show_result_window(
            nom, total, details, generer_conseils(details, choix)
        )

    except ValueError:
        messagebox.showerror("Erreur", "Vérifiez les champs.")
    except KeyError:
        messagebox.showerror("Erreur", "Sélection invalide.")


def _on_mousewheel(event):  # fonction qui nous permet de scroll
    if event.num == 5 or event.delta == -120:
        canvas.yview_scroll(1, "units")
    if event.num == 4 or event.delta == 120:
        canvas.yview_scroll(-1, "units")


def configure_canvas_width(event):  # focntion qui permt aussi de scroll
    canvas.itemconfig(canvas_window, width=event.width)


# ==========================================
# 4. INTERFACE
# ==========================================
# on crée notre interface tkinter et on l'initialise
root = Tk()
root.title("Calculateur ACV")
try:
    root.state("zoomed")
except:
    root.attributes("-zoomed", True)

# Police globale
style = ttk.Style()
style.configure("TLabel", font=(POLICE_CORPS, 14))
style.configure("TEntry", font=(POLICE_CORPS, 14))
style.configure("TCombobox", font=(POLICE_CORPS, 12))

# Titre + bandeau
header_frame = Frame(root, bg=THEME_COLOR, height=90)
header_frame.pack(fill="x", side="top")
Label(
    header_frame,
    text="CALCULATEUR ACV",
    font=(POLICE_TITRE, 36),
    bg=THEME_COLOR,
    fg="white",
).pack(pady=25)

# Scroll zone
main_container = Frame(root)
main_container.pack(fill="both", expand=True)

canvas = Canvas(main_container)
scrollbar = ttk.Scrollbar(
    main_container, orient="vertical", command=canvas.yview
)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas_window = canvas.create_window(
    (0, 0), window=scrollable_frame, anchor="n"
)
canvas.bind("<Configure>", configure_canvas_width)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.bind_all("<MouseWheel>", _on_mousewheel)
root.bind_all("<Button-4>", _on_mousewheel)
root.bind_all("<Button-5>", _on_mousewheel)

# Definition de la zone de quesion
content_frame = ttk.Frame(scrollable_frame, padding=(50, 20, 50, 150))
content_frame.pack(expand=True, fill="both")
form_frame = ttk.Frame(content_frame, relief="groove", borderwidth=2)
form_frame.pack(anchor="center", ipadx=20, ipady=20)

list_cat_mat = list(DATA_DB["MATERIAUX"].keys())
list_fab = list(DATA_DB["FABRICATION"].keys())
list_trans = list(DATA_DB["TRANSPORT"].keys())
list_ener = list(DATA_DB["ENERGIE"].keys())

nom_var = StringVar()
masse_var = StringVar()
dist_var = StringVar()
conso_var = StringVar()
duree_var = StringVar()

r = 0
PAD_Y = 20
PAD_X = 20
ENTRY_WIDTH = 35
COMBO_WIDTH = 33

# definition de tout les widget qui formule le questionnaire
ttk.Label(form_frame, text="Nom de l'objet :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
ttk.Entry(form_frame, textvariable=nom_var, width=ENTRY_WIDTH).grid(
    row=r, column=1, sticky="w"
)
r += 1
ttk.Label(form_frame, text="Masse totale (kg) :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
ttk.Entry(form_frame, textvariable=masse_var, width=15).grid(
    row=r, column=1, sticky="w"
)
r += 1
ttk.Separator(form_frame, orient="horizontal").grid(
    row=r, columnspan=2, sticky="ew", pady=30
)
r += 1

ttk.Label(form_frame, text="Type de Matériau :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
combo_cat_mat = ttk.Combobox(
    form_frame,
    values=list_cat_mat,
    state="readonly",
    width=COMBO_WIDTH,
    font=(POLICE_CORPS, 12),
)
combo_cat_mat.grid(row=r, column=1, sticky="w")
combo_cat_mat.current(0)
combo_cat_mat.bind("<<ComboboxSelected>>", update_materiau_combo)
r += 1
ttk.Label(form_frame, text="Matériau spécifique :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
combo_mat = ttk.Combobox(
    form_frame,
    values=[],
    state="readonly",
    width=COMBO_WIDTH,
    font=(POLICE_CORPS, 12),
)
combo_mat.grid(row=r, column=1, sticky="w")
r += 1
ttk.Label(form_frame, text="Procédé Fabrication :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
combo_fab = ttk.Combobox(
    form_frame,
    values=list_fab,
    state="readonly",
    width=COMBO_WIDTH,
    font=(POLICE_CORPS, 12),
)
combo_fab.grid(row=r, column=1, sticky="w")
combo_fab.current(0)
r += 1
# crée les ligne qui separe la page
ttk.Separator(form_frame, orient="horizontal").grid(
    row=r, columnspan=2, sticky="ew", pady=30
)
r += 1

ttk.Label(form_frame, text="Distance Transport (km) :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
ttk.Entry(form_frame, textvariable=dist_var, width=15).grid(
    row=r, column=1, sticky="w"
)
r += 1
ttk.Label(form_frame, text="Mode de Transport :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
combo_trans = ttk.Combobox(
    form_frame,
    values=list_trans,
    state="readonly",
    width=COMBO_WIDTH,
    font=(POLICE_CORPS, 12),
)
combo_trans.grid(row=r, column=1, sticky="w")
combo_trans.current(0)
r += 1
ttk.Separator(form_frame, orient="horizontal").grid(
    row=r, columnspan=2, sticky="ew", pady=30
)
r += 1

ttk.Label(form_frame, text="Conso Électrique (kWh/an) :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
ttk.Entry(form_frame, textvariable=conso_var, width=15).grid(
    row=r, column=1, sticky="w"
)
r += 1
ttk.Label(form_frame, text="Source d'Énergie :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
combo_ener = ttk.Combobox(
    form_frame,
    values=list_ener,
    state="readonly",
    width=COMBO_WIDTH,
    font=(POLICE_CORPS, 12),
)
combo_ener.grid(row=r, column=1, sticky="w")
combo_ener.current(0)
r += 1
ttk.Label(form_frame, text="Durée de vie (années) :").grid(
    row=r, column=0, sticky="e", pady=PAD_Y, padx=PAD_X
)
ttk.Entry(form_frame, textvariable=duree_var, width=15).grid(
    row=r, column=1, sticky="w"
)
r += 1
ttk.Separator(form_frame, orient="horizontal").grid(
    row=r, columnspan=2, sticky="ew", pady=40
)
r += 1
# création du bouton de fin qui permet d'effectuer le calcul.
btn_calcul = Button(
    form_frame,
    text="CALCULER L'IMPACT",
    command=calculer,
    bg=THEME_COLOR,
    fg="white",
    font=(POLICE_CORPS, 16, "bold"),
    activebackground="#267345",
    activeforeground="white",
    relief="raised",
    bd=3,
    padx=30,
    pady=10,
    cursor="hand2",
)
btn_calcul.grid(row=r, columnspan=2, pady=20)

update_materiau_combo(None)
root.mainloop()
# ======================================
