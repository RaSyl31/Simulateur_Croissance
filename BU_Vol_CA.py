import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Simulateur Croissance - Alcomix",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .stDataFrame { border: 1px solid #b30000; }
    h1, h2, h3 { color: #b30000; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DONNÉES 2026 (Valeurs Nettes)
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
# INITIALISATION DES DONNÉES
# ============================================================
@st.cache_data
def preparer_donnees():
    rows = []
    for segment, marques in DONNEES_2026.items():
        for marque, articles in marques.items():
            for article, volume in articles.items():
                rows.append({"Segment": segment, "Marque": marque, "Article": article, "Volume_2026": volume})
    df = pd.DataFrame(rows)
    
    # Gestion des arrêts de produits
    df["Volume_2026_Ajuste"] = df.apply(lambda row: 0 if row["Article"] in PRODUITS_ARRETES else row["Volume_2026"], axis=1)
    
    # CALCUL DES POIDS STABLES (Part de l'article dans le Total Global)
    total_global = df["Volume_2026_Ajuste"].sum()
    df["Poids_Global"] = df["Volume_2026_Ajuste"] / total_global
    
    return df, total_global

df_base, TOTAL_2026 = preparer_donnees()

# ============================================================
# SIDEBAR : PILOTAGE GLOBAL
# ============================================================
st.sidebar.header("🎯 Objectif Global (Total Entreprise)")
objectif_global_2031 = st.sidebar.number_input(
    "Objectif Total 2031 (unités)", 
    min_value=int(TOTAL_2026), 
    value=6000000, 
    step=100000
)

# ============================================================
# CALCULS DE LA SIMULATION
# ============================================================
# On calcule les objectifs globaux par année (avec une croissance lissée)
# Ex: 2026 = 4.3M, 2027 = +5%, 2028 = +5%, etc.
# Mais on laisse l'utilisateur modifier le tableau pour écraser ces valeurs.

df_sim = df_base.copy()
df_sim.rename(columns={"Volume_2026_Ajuste": "2026"}, inplace=True)

# Calcul de la répartition initiale basée sur l'objectif 2031
df_sim["2031"] = df_sim["Poids_Global"] * objectif_global_2031

# Interpolation pour les années intermédiaires (Croissance linéaire)
df_sim["2027"] = df_sim["2026"] + (df_sim["2031"] - df_sim["2026"]) * (1/5)
df_sim["2028"] = df_sim["2026"] + (df_sim["2031"] - df_sim["2026"]) * (2/5)
df_sim["2029"] = df_sim["2026"] + (df_sim["2031"] - df_sim["2026"]) * (3/5)
df_sim["2030"] = df_sim["2026"] + (df_sim["2031"] - df_sim["2026"]) * (4/5)

# ============================================================
# AFFICHAGE DU DASHBOARD
# ============================================================
st.title("📈 Simulateur de Croissance - Alcomix")

st.markdown("### 🎛️ Tableau de Bord des Objectifs (Modifiable)")
st.info("💡 **Astuce :** Vous pouvez double-cliquer sur une cellule des années 2026 à 2031 pour ajuster manuellement l'objectif d'un segment. Les marques et articles se recalculeront automatiquement.")

# --- TABLEAU MODIFIABLE PAR SEGMENT ---
df_seg_initial = df_sim.groupby("Segment")[["2026", "2027", "2028", "2029", "2030", "2031"]].sum().reset_index()

# Affichage avec st.data_editor (rend les cellules éditables)
edited_seg_df = st.data_editor(
    df_seg_initial,
    column_config={
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "2026": st.column_config.NumberColumn("2026", format="%d"),
        "2027": st.column_config.NumberColumn("2027", format="%d"),
        "2028": st.column_config.NumberColumn("2028", format="%d"),
        "2029": st.column_config.NumberColumn("2029", format="%d"),
        "2030": st.column_config.NumberColumn("2030", format="%d"),
        "2031": st.column_config.NumberColumn("2031", format="%d"),
    },
    hide_index=True,
    use_container_width=True,
    key="editor_segments"
)

# Recalcul des sous-niveaux (Marques et Articles) en fonction des modifications du tableau Segment
# 1. On calcule le nouveau total global par année à partir du tableau modifié
nouveaux_totaux_an = edited_seg_df[["2026", "2027", "2028", "2029", "2030", "2031"]].sum()

# 2. On recalcule les poids de chaque segment dans le nouveau total
poids_seg_an = edited_seg_df.set_index("Segment").div(nouveaux_totaux_an, axis=1)

# 3. On applique ces nouveaux poids aux articles pour la vue détaillée
df_sim_ajuste = df_sim.copy()
for annee in ["2026", "2027", "2028", "2029", "2030", "2031"]:
    # Pour chaque segment, on applique le poids de l'article dans son segment initial
    poids_art_dans_seg = df_sim.groupby("Segment")[annee].transform(lambda x: x / x.sum())
    
    # Le nouveau volume de l'article = Nouveau volume du segment * Poids de l'article dans le segment
    nouveau_vol_seg = edited_seg_df.set_index("Segment")[annee]
    df_sim_ajuste[annee] = df_sim["Segment"].map(nouveau_vol_seg) * poids_art_dans_seg


# --- TABLEAU MENSUEL ---
st.markdown("### 📅 Répartition Mensuelle (Mix)")
annee_cible = st.selectbox("Sélectionnez l'année à projeter :", [2027, 2028, 2029, 2030, 2031], index=0)
annee_str = str(annee_cible)

# Calcul du mix et de la moyenne mensuelle basé sur les données modifiées
mix_mensuel = edited_seg_df[["Segment", annee_str]].copy()
mix_mensuel["Mix %"] = (mix_mensuel[annee_str] / mix_mensuel[annee_str].sum()) * 100
mix_mensuel["Moyenne Mensuelle"] = mix_mensuel[annee_str] / 12

st.dataframe(
    mix_mensuel.set_index("Segment").style.format({
        annee_str: "{:,.0f}",
        "Mix %": "{:.1f} %",
        "Moyenne Mensuelle": "{:,.0f}"
    }),
    use_container_width=True
)

st.divider()

# --- DÉTAIL PAR SEGMENT (Accordéons) ---
st.markdown("### 📦 Détail par Segment et Marque")
for segment in df_sim_ajuste["Segment"].unique():
    with st.expander(f"🔹 Segment : {segment}"):
        df_detail = df_sim_ajuste[df_sim_ajuste["Segment"] == segment]
        
        # Affichage par marque
        df_marque = df_detail.groupby("Marque")[["2026", "2027", "2028", "2029", "2030", "2031"]].sum()
        st.markdown("**Par Marque**")
        st.dataframe(
            df_marque.style.format("{:,.0f}"),
            use_container_width=True
        )
        
        # Affichage par article
        df_article = df_detail.set_index(["Marque", "Article"])[["2026", "2027", "2028", "2029", "2030", "2031"]]
        st.markdown("**Par Article (SKU)**")
        st.dataframe(
            df_article.style.format("{:,.0f}"),
            use_container_width=True
        )
