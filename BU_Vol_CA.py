import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(page_title="Simulateur Alcomix", layout="wide")

# ============================================================
# DONNÉES 2026
# ============================================================
DONNEES_2026 = {
    "Alcomix": {
        "Booster": {"Booster Appel-Mix 50CL VER": 21855, "Booster Tornado 50CL VER VER": 15616},
        "BOTA Fresh": {"BOTA Fresh 50 cl VER": 1005},
        "Racines": {"Racines 33 cl VER": 2220},
    },
    "BG": {
        "Caprice": {
            "Caprice Ananas 100 cl VER": 4386, "Caprice Ananas 150 cl PET": 22050, "Caprice Ananas 30 cl VER": 4496,
            "Caprice Bonbon Anglais 100 cl VER": 57580, "Caprice Bonbon Anglais 150 cl PET": 308042,
            "Caprice Bonbon Anglais 20L FUT": 79, "Caprice Bonbon Anglais 30 cl VER": 41261,
            "Caprice Bonbon Anglais 33 cl CAN": 4990, "Caprice Bonbon Anglais 35 cl PET": 19424,
            "Caprice Bonbon Anglais 50 cl PET": 137932, "Caprice Grenadine 100 cl VER": 11739,
            "Caprice Grenadine 150 cl PET": 34088, "Caprice Grenadine 30 cl VER": 4720,
            "Caprice Grenadine 33 cl CAN": 2897, "Caprice Grenadine 35 cl PET": 1886,
            "Caprice Grenadine 50 cl PET": 11792, "Caprice Orange 100 cl VER": 33262,
            "Caprice Orange 150 cl PET": 161382, "Caprice Orange 20L FUT": 75,
            "Caprice Orange 30 cl VER": 26172, "Caprice Orange 33 cl CAN": 3875,
            "Caprice Orange 35 cl PET": 5943, "Caprice Orange 50 cl PET": 59297,
            "Caprice Pomme 100 cl VER": 958, "Caprice Pomme 150 cl PET": 4128,
            "Caprice Pomme 30 cl VER": 1595, "Caprice Pomme 50 cl PET": 0,
        },
        "Tonic": {"Tonic 100 cl VER": 7958, "Tonic 30 cl VER": 17921},
        "World Cola": {
            "World Cola 100cl VER": 4368, "World Cola 100cl WOCO VER": 24276, "World Cola 150cl PET": 100927,
            "World Cola 30cl VER": 1967, "World Cola 30cl WOCO VER": 26387, "World Cola 33 cl CAN": 2832,
            "World Cola 35cl PET": 6866, "World Cola 50cl PET": 54263, "World Cola 20L FUT": 281,
        },
    },
    "BIERES": {
        "Beaufort": {"Beaufort 33 CL CAN": 13986, "Beaufort 33CL VER": 34851},
        "FRESH": {"FRESH 33 cl CAN": 3254, "FRESH 33 cl EXPORT CAN": 25, "THB Fresh 33 cl VER": 1881, "THB Fresh 65 cl VER": 35712},
        "Gold": {
            "Gold 8 50 cl CAN": 1159, "Gold 8 50 cl VER": 8661, "Gold Blanche 33cl VER": 24605,
            "Gold Blanche 50 cl CAN": 43538, "Gold Blanche 50 cl VER": 92121, "Gold Amigo 33cl VER": 1463,
            "Gold Blonde 50 cl CAN": 8531, "Gold Blonde 50 cl VER": 15872, "Gold Blonde 65 cl VER": 58077,
            "Gold Blanche 20L FUT": 1464,
        },
        "Queen": {"Queen s 65 cl VER": 153975},
        "THB": {
            "THB Pilsener 33 cl VER": 96836, "THB Pilsener 50 cl CAN": 60246, "THB Pilsener 65 cl VER": 1513573,
            "THB Pilsener 20L FUT": 2228, "THB Pilsener 30L FUT": 0, "THB Speciale NOEL 33 cl VER": 736,
            "THB Pilsener 20L Export FUT": 450, "THB Blanche 20L Export FUT": 47,
            "THB Pilsener 30L Export FUT": 602, "THB 8 20L Export FUT": 40,
        },
    },
    "EAUX": {
        "Cristal": {"Cristal 100 cl VER": 1004, "Cristal 150 cl PET": 4516, "Cristal 30 cl VER": 689, "Cristal 50 cl VER": 4206},
        "Cristalline": {"Cristalline 100 cl PET": 272844, "Cristalline 200 cl PET": 268234},
        "Eau vive": {"Eau vive 150 cl PET": 210612, "Eau vive 50 cl PET": 67919, "Eau vive 50 cl VER": 364},
    },
    "Energy": {
        "FOSA": {"FOSA 50 cl CAN": 3265},
        "XXL": {"XXL 30cl BOB VER": 19433, "XXL 30cl VER": 571, "XXL 33 cl CAN": 3001, "XXL 35cl PET": 16357},
    },
}

PRODUITS_ARRETES = ["BOTA Fresh 50 cl VER", "Racines 33 cl VER"]

# ============================================================
# PREPARATION DES DONNÉES ET CALCUL DU MIX
# ============================================================
@st.cache_data
def preparer_donnees():
    rows = []
    for segment, marques in DONNEES_2026.items():
        for marque, articles in marques.items():
            for article, volume in articles.items():
                rows.append({"Segment": segment, "Marque": marque, "Article": article, "2026": volume})
    df = pd.DataFrame(rows)
    
    # Arrêt des produits
    df["2026"] = df.apply(lambda row: 0 if row["Article"] in PRODUITS_ARRETES else row["2026"], axis=1)
    
    # Calcul des poids
    total_2026 = df["2026"].sum()
    df["Poids_Segment"] = df.groupby("Segment")["2026"].transform("sum") / total_2026
    df["Poids_Marque"] = df.groupby(["Segment", "Marque"])["2026"].transform("sum") / df.groupby("Segment")["2026"].transform("sum")
    df["Poids_Article"] = df["2026"] / df.groupby(["Segment", "Marque"])["2026"].transform("sum")
    
    return df, total_2026

df_base, TOTAL_2026 = preparer_donnees()

# ============================================================
# INITIALISATION DE L'ÉTAT
# ============================================================
if "objets_seg" not in st.session_state:
    st.session_state.objets_seg = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy"],
        "2027": [45969, 1258992, 2250000, 850000, 44000],
        "2028": [49000, 1303400, 2400000, 900000, 46000],
        "2029": [52500, 1459500, 2600000, 950000, 48000],
        "2030": [56000, 1562400, 2800000, 1000000, 50000],
        "2031": [60000, 1680000, 3000000, 1100000, 52000],
    })

# ============================================================
# INTERFACE
# ============================================================
st.title("📈 Simulateur de Croissance - Alcomix")

st.markdown("### 🎛️ 1. Définir les objectifs par Segment (Modifiable)")
edited_df = st.data_editor(
    st.session_state.objets_seg,
    column_config={
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "2027": st.column_config.NumberColumn("2027", format="%d"),
        "2028": st.column_config.NumberColumn("2028", format="%d"),
        "2029": st.column_config.NumberColumn("2029", format="%d"),
        "2030": st.column_config.NumberColumn("2030", format="%d"),
        "2031": st.column_config.NumberColumn("2031", format="%d"),
    },
    hide_index=True,
    use_container_width=True,
    key="editeur_segments"
)
st.session_state.objets_seg = edited_df

# ============================================================
# CALCUL DES VOLUMES ET CREATION DU TABLEAU FINAL
# ============================================================
df_final = df_base.copy()
annees = ["2026", "2027", "2028", "2029", "2030", "2031"]

# On applique les objectifs saisis
for annee in annees[1:]:
    dict_obj = edited_df.set_index("Segment")[annee].to_dict()
    df_final[annee] = df_final["Segment"].map(dict_obj) * df_final["Poids_Marque"] * df_final["Poids_Article"]

# --- AGRÉGATION POUR LE TABLEAU ---
# 1. Par Article
df_art = df_final[["Segment", "Marque", "Article"] + annees].copy()

# 2. Par Marque
df_marq = df_final.groupby(["Segment", "Marque"])[annees].sum().reset_index()

# 3. Par Segment
df_seg = df_final.groupby("Segment")[annees].sum().reset_index()

# 4. Total Annuel
df_total = df_final[annees].sum().to_frame().T
df_total.insert(0, "Segment", "TOTAL ANNEE")
df_total.insert(1, "Marque", "")
df_total.insert(2, "Article", "")

# --- FUSION POUR AVOIR L'ORDRE EXACT ---
lignes_finales = []
for seg in ["Alcomix", "BG", "BIERES", "EAUX", "Energy"]:
    # Ligne Segment
    row_seg = df_seg[df_seg["Segment"] == seg].iloc[0].to_dict()
    row_seg["Marque"] = ""
    row_seg["Article"] = ""
    lignes_finales.append(row_seg)
    
    # Lignes Marques et Articles
    marques = df_marq[df_marq["Segment"] == seg]
    for _, marq in marques.iterrows():
        row_marq = marq.to_dict()
        row_marq["Article"] = ""
        lignes_finales.append(row_marq)
        
        articles = df_art[(df_art["Segment"] == seg) & (df_art["Marque"] == marq["Marque"])]
        for _, art in articles.iterrows():
            lignes_finales.append(art.to_dict())

# Ajout de la ligne Total à la fin
lignes_finales.append(df_total.iloc[0].to_dict())

df_affichage = pd.DataFrame(lignes_finales)

# ============================================================
# STYLISATION (Reproduction de l'Excel)
# ============================================================
def style_tableau(df):
    # Styles de base
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    
    # Couleurs
    RED_BG = "background-color: #b30000; color: white; font-weight: bold;"
    LIGHT_RED_BG = "background-color: #f4cccc; color: black;"
    GREY_BG = "background-color: #d9d9d9; font-weight: bold;"
    WHITE_BG = "background-color: white;"
    
    # Appliquer les couleurs selon la hiérarchie
    for i, row in df.iterrows():
        if row["Segment"] == "TOTAL ANNEE":
            styles.loc[i, ["Segment", "Marque", "Article"]] = RED_BG
            styles.loc[i, annees] = "background-color: #b30000; color: white; font-weight: bold;"
            
        elif row["Marque"] == "" and row["Article"] == "": # C'est un Segment
            styles.loc[i, ["Segment", "Marque", "Article"]] = LIGHT_RED_BG + " font-weight: bold;"
            styles.loc[i, annees] = LIGHT_RED_BG + " font-weight: bold;"
            
        elif row["Article"] == "": # C'est une Marque
            styles.loc[i, ["Segment", "Marque", "Article"]] = GREY_BG
            styles.loc[i, annees] = GREY_BG
            
        else: # C'est un Article
            styles.loc[i, ["Segment", "Marque", "Article"]] = WHITE_BG
            # Mise en évidence du "BOTA Fresh" et "Racines" (arrêtés)
            if row["Article"] in PRODUITS_ARRETES:
                styles.loc[i, annees] = "background-color: #d9ead3; color: black;" # Vert clair
                
    return styles

# Formatage des nombres
format_dict = {annee: "{:,.0f}" for annee in annees}

# Application du style
styled_df = df_affichage.style.apply(style_tableau, axis=None).format(format_dict)

# ============================================================
# AFFICHAGE DU TABLEAU
# ============================================================
st.markdown("### 📊 2. Tableau de Bord Détaillé (Vue Excel)")
st.dataframe(styled_df, use_container_width=True, height=800)

# ============================================================
# TABLEAU MENSUEL (Bonus)
# ============================================================
st.markdown("---")
st.markdown("### 📅 3. Répartition Mensuelle")
annee_cible = st.selectbox("Sélectionnez l'année pour voir la répartition mensuelle :", annees[1:])
df_mensuel = df_seg[["Segment", annee_cible]].copy()
df_mensuel["Mix %"] = (df_mensuel[annee_cible] / df_mensuel[annee_cible].sum()) * 100
df_mensuel["Moyenne Mensuelle"] = df_mensuel[annee_cible] / 12

st.dataframe(
    df_mensuel.style.format({
        annee_cible: "{:,.0f}",
        "Mix %": "{:.1f} %",
        "Moyenne Mensuelle": "{:,.0f}"
    }),
    hide_index=True,
    use_container_width=True
)
