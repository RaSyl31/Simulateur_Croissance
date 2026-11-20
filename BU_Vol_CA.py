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

# Style personnalisé pour se rapprocher de l'Excel (Rouge Alcomix)
st.markdown("""
<style>
    .stDataFrame { border: 1px solid #b30000; }
    h1, h2, h3 { color: #b30000; }
    div[data-testid="stMetricValue"] { color: #b30000; }
</style>
""", unsafe_allow_html=True)

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
# INITIALISATION DES DONNÉES ET POIDS (CASCADE)
# ============================================================
@st.cache_data
def preparer_donnees():
    rows = []
    for segment, marques in DONNEES_2026.items():
        for marque, articles in marques.items():
            for article, volume in articles.items():
                rows.append({"Segment": segment, "Marque": marque, "Article": article, "Volume_2026": volume})
    df = pd.DataFrame(rows)
    
    # Arrêt des produits
    df["Volume_2026_Ajuste"] = df.apply(lambda row: 0 if row["Article"] in PRODUITS_ARRETES else row["Volume_2026"], axis=1)
    
    # 1. Poids du Segment dans le Total
    total_global = df["Volume_2026_Ajuste"].sum()
    df["Poids_Seg_Total"] = df["Volume_2026_Ajuste"] / total_global
    
    # 2. Poids de la Marque dans le Segment
    vol_par_seg = df.groupby("Segment")["Volume_2026_Ajuste"].transform("sum")
    df["Poids_Marq_Seg"] = df["Volume_2026_Ajuste"] / vol_par_seg
    
    # 3. Poids de l'Article dans la Marque
    vol_par_marq = df.groupby("Marque")["Volume_2026_Ajuste"].transform("sum")
    df["Poids_Art_Marq"] = df["Volume_2026_Ajuste"] / vol_par_marq
    
    return df, total_global

df_base, TOTAL_2026 = preparer_donnees()

# ============================================================
# SIDEBAR : PILOTAGE DES OBJECTIFS
# ============================================================
st.sidebar.header("🎯 Objectifs Annuels Globaux")
obj_2027 = st.sidebar.number_input("Objectif 2027", min_value=0, value=4600000, step=100000)
obj_2028 = st.sidebar.number_input("Objectif 2028", min_value=0, value=4900000, step=100000)
obj_2029 = st.sidebar.number_input("Objectif 2029", min_value=0, value=5250000, step=100000)
obj_2030 = st.sidebar.number_input("Objectif 2030", min_value=0, value=5600000, step=100000)
obj_2031 = st.sidebar.number_input("Objectif 2031", min_value=0, value=6000000, step=100000)

objectifs = {2027: obj_2027, 2028: obj_2028, 2029: obj_2029, 2030: obj_2030, 2031: obj_2031}

# ============================================================
# CALCULS DE LA CASCADE POUR LA SIMULATION
# ============================================================
df_sim = df_base.copy()
df_sim.rename(columns={"Volume_2026_Ajuste": "2026"}, inplace=True)

for annee, objectif in objectifs.items():
    # CASCADE : On applique le poids du segment au total, etc.
    df_sim[str(annee)] = objectif * df_sim["Poids_Seg_Total"] * df_sim["Poids_Marq_Seg"] * df_sim["Poids_Art_Marq"]

# ============================================================
# AFFICHAGE DU DASHBOARD
# ============================================================
st.title("📈 Simulateur de Croissance Annuelle - Alcomix")

# --- KPIs ---
cagr_global = ((obj_2031 / TOTAL_2026) ** (1/5) - 1) * 100 if TOTAL_2026 > 0 else 0
col1, col2, col3 = st.columns(3)
col1.metric("Volume 2026", f"{TOTAL_2026:,.0f}")
col2.metric("Volume 2031 (Cible)", f"{obj_2031:,.0f}")
col3.metric("CAGR Global 26-31", f"{cagr_global:.2f} %")

st.divider()

# --- TABLEAU 1 : DEMANDE PAR SEGMENT (ANNUEL) ---
st.markdown("### 📊 Demande par Segment (Vue Annuelle)")
df_seg = df_sim.groupby("Segment").sum(numeric_only=True).reset_index()

# Ajout CAGR
df_seg["CAGR 26-31"] = ((df_seg["2031"] / df_seg["2026"].replace(0, 1)) ** (1/5) - 1) * 100
df_seg["CAGR 26-31"] = df_seg["CAGR 26-31"].apply(lambda x: f"{x:.1f} %" if pd.notnull(x) else "-")

# Formatage
cols_annees = [str(y) for y in range(2026, 2032)]
df_seg_display = df_seg.set_index("Segment")[cols_annees + ["CAGR 26-31"]].copy()
for col in cols_annees:
    df_seg_display[col] = df_seg_display[col].apply(lambda x: f"{x:,.0f}".replace(",", " ") if pd.notnull(x) else "-")

st.dataframe(df_seg_display, use_container_width=True)

# --- TABLEAU 2 : OBJECTIFS MENSUELS ET MIX (Nouveau !) ---
st.markdown("### 📅 Objectifs Mensuels et Mix (Par Segment)")

annee_cible = st.selectbox("Sélectionnez l'année cible pour la vue mensuelle :", [2027, 2028, 2029, 2030, 2031], index=0)

# Calcul du mix global par segment pour l'année choisie
mix_seg_an = df_sim.groupby("Segment")[str(annee_cible)].sum().reset_index()
mix_seg_an["Mix %"] = (mix_seg_an[str(annee_cible)] / mix_seg_an[str(annee_cible)].sum()) * 100
mix_seg_an[str(annee_cible)] = mix_seg_an[str(annee_cible)].apply(lambda x: f"{x:,.0f}".replace(",", " "))
mix_seg_an["Mix %"] = mix_seg_an["Mix %"].apply(lambda x: f"{x:.1f} %")

# On calcule la répartition mensuelle linéaire (Total / 12)
objectif_annuel = objectifs[annee_cible]
objectif_mensuel_moyen = objectif_annuel / 12

# Création du tableau
df_mensuel = pd.DataFrame({
    "Segment": mix_seg_an["Segment"],
    "Objectif Annuel": mix_seg_an[str(annee_cible)],
    "Mix %": mix_seg_an["Mix %"],
    "Moyenne Mensuelle": (mix_seg_an[str(annee_cible)].str.replace(" ", "").astype(float) / 12).apply(lambda x: f"{x:,.0f}".replace(",", " "))
})

st.dataframe(df_mensuel.set_index("Segment"), use_container_width=True)
st.caption(f"* Objectif mensuel moyen basé sur un total de {objectif_annuel:,.0f} unités pour {annee_cible}.*")

# --- TABLEAU 3 : DÉTAIL PAR SEGMENT ET MARQUE ---
st.markdown("### 📦 Détail par Segment et Marque")
for segment in df_sim["Segment"].unique():
    with st.expander(f"🔹 Segment : {segment}"):
        df_detail = df_sim[df_sim["Segment"] == segment].copy()
        
        # Vue Marque
        df_marque = df_detail.groupby("Marque").sum(numeric_only=True).reset_index()
        cols_affichage = ["Marque"] + cols_annees
        df_marque_display = df_marque[cols_affichage].set_index("Marque")
        
        for col in cols_annees:
            df_marque_display[col] = df_marque_display[col].apply(lambda x: f"{x:,.0f}".replace(",", " ") if pd.notnull(x) else "-")
            
        st.markdown(f"**Marques**")
        st.dataframe(df_marque_display, use_container_width=True)
