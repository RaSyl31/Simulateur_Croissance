import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Simulateur Croissance - Alcomix",
    page_icon="📈",
    layout="wide"
)

# Style personnalisé pour se rapprocher de l'Excel
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    h1, h2, h3 {
        color: #b30000;
    }
    .stDataFrame {
        border: 1px solid #b30000;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DONNÉES 2026 (Catalogue complet avec Volumes)
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

# Produits à arrêter (Volume mis à 0 à partir de 2027)
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
                rows.append({
                    "Segment": segment,
                    "Marque": marque,
                    "Article": article,
                    "Volume_2026": volume
                })
    df = pd.DataFrame(rows)
    
    # Calcul des poids initiaux
    df["Poids_Art"] = df.groupby("Marque")["Volume_2026"].transform(lambda x: x / x.sum() if x.sum() > 0 else 0)
    
    # Application de l'arrêt des produits
    df["Volume_2026_Ajuste"] = df.apply(
        lambda row: 0 if row["Article"] in PRODUITS_ARRETES else row["Volume_2026"], axis=1
    )
    return df

df_base = preparer_donnees()
TOTAL_2026 = df_base["Volume_2026_Ajuste"].sum() # ~4,297,000

# ============================================================
# SIDEBAR : PILOTAGE DES OBJECTIFS
# ============================================================
st.sidebar.header("🎯 Objectifs Annuels")

st.sidebar.markdown("Définissez le volume total visé pour chaque année :")
obj_2027 = st.sidebar.number_input("Objectif 2027", min_value=0, value=4600000, step=100000)
obj_2028 = st.sidebar.number_input("Objectif 2028", min_value=0, value=4900000, step=100000)
obj_2029 = st.sidebar.number_input("Objectif 2029", min_value=0, value=5250000, step=100000)
obj_2030 = st.sidebar.number_input("Objectif 2030", min_value=0, value=5600000, step=100000)
obj_2031 = st.sidebar.number_input("Objectif 2031", min_value=0, value=6000000, step=100000)

objectifs = {2027: obj_2027, 2028: obj_2028, 2029: obj_2029, 2030: obj_2030, 2031: obj_2031}

# ============================================================
# CALCULS DE SIMULATION
# ============================================================
# Création d'un DataFrame de simulation avec les années en colonnes
df_sim = df_base[["Segment", "Marque", "Article", "Volume_2026_Ajuste", "Poids_Art"]].copy()
df_sim.rename(columns={"Volume_2026_Ajuste": "2026"}, inplace=True)

for annee, objectif in objectifs.items():
    # Répartition proportionnelle basée sur le poids de l'article dans sa marque
    # (On multiplie le poids par le volume total cible)
    df_sim[str(annee)] = df_sim["Poids_Art"] * objectif

# ============================================================
# AFFICHAGE DU DASHBOARD
# ============================================================
st.title("📈 Simulateur de Croissance Annuelle - Alcomix")

# --- CALCUL DES CAGR GLOBAUX ---
cagr_global = ((obj_2031 / TOTAL_2026) ** (1/5) - 1) * 100 if TOTAL_2026 > 0 else 0

# Bandeau supérieur
col1, col2, col3 = st.columns(3)
col1.metric("Volume 2026", f"{TOTAL_2026:,.0f}")
col2.metric("Volume 2031 (Cible)", f"{obj_2031:,.0f}")
col3.metric("CAGR Global 26-31", f"{cagr_global:.2f} %")

# --- TABLEAU CROSSTAB (Segments) ---
st.markdown("### 📊 Demande par Segment")
df_seg = df_sim.groupby("Segment").sum(numeric_only=True).reset_index()
df_seg = df_seg.drop(columns=["Poids_Art"])

# Formatage pour l'affichage
df_seg_display = df_seg.copy()
for col in df_seg_display.columns[1:]:
    df_seg_display[col] = df_seg_display[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))

st.dataframe(df_seg_display.set_index("Segment"), use_container_width=True)

# --- TABLEAUX DÉTAILLÉS PAR SEGMENT ---
st.markdown("### 📦 Détail par Segment et Marque")

# On ajoute le CAGR par segment
df_seg_cagr = df_seg.copy()
df_seg_cagr["CAGR 26-31"] = ((df_seg_cagr["2031"] / df_seg_cagr["2026"]) ** (1/5) - 1) * 100
df_seg_cagr["CAGR 26-31"] = df_seg_cagr["CAGR 26-31"].apply(lambda x: f"{x:.1f} %")

for segment in df_sim["Segment"].unique():
    with st.expander(f"🔹 Segment : {segment}"):
        df_detail = df_sim[df_sim["Segment"] == segment].copy()
        
        # Affichage par Marque
        df_marque = df_detail.groupby("Marque").sum(numeric_only=True).reset_index()
        df_marque = df_marque.drop(columns=["Poids_Art"])
        
        # Formatage
        df_marque_display = df_marque.copy()
        for col in df_marque_display.columns[1:]:
            df_marque_display[col] = df_marque_display[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))
            
        st.markdown(f"**Marques du segment {segment}**")
        st.dataframe(df_marque_display.set_index("Marque"), use_container_width=True)
        
        # Affichage par Article
        st.markdown(f"**Articles du segment {segment}**")
        df_art = df_detail[["Marque", "Article"] + [str(y) for y in range(2026, 2032)]].copy()
        
        # Formatage
        for col in df_art.columns[2:]:
            df_art[col] = df_art[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))
            
        st.dataframe(df_art.set_index(["Marque", "Article"]), use_container_width=True)

# --- GRAPHIQUE D'ÉVOLUTION ---
st.markdown("### 📈 Évolution Globale 2026 - 2031")
df_evol = pd.DataFrame({
    "Année": [2026, 2027, 2028, 2029, 2030, 2031],
    "Volume": [TOTAL_2026] + list(objectifs.values())
})
fig = px.bar(df_evol, x="Année", y="Volume", text="Volume", title="Objectif de Volume Global")
fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig.update_layout(yaxis_title="Volume (unités)", xaxis_title="Année")
st.plotly_chart(fig, use_container_width=True)
