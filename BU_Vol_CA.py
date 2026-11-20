import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os
from datetime import datetime

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Budget Alcomix",
    page_icon="🍹",
    layout="wide"
)

# ============================================================
# CATALOGUE (intégré)
# ============================================================
CATALOGUE = {
    "Alcomix": {
        "Booster": ["Booster Appel-Mix 50CL VER", "Booster Tornado 50CL VER VER"],
        "BOTA Fresh": ["BOTA Fresh 50 cl VER"],
        "Racines": ["Racines 33 cl VER"],
    },
    "BG": {
        "Caprice": [
            "Caprice Ananas 100 cl VER", "Caprice Ananas 150 cl PET", "Caprice Ananas 30 cl VER",
            "Caprice Bonbon Anglais 100 cl VER", "Caprice Bonbon Anglais 150 cl PET",
            "Caprice Bonbon Anglais 20L FUT", "Caprice Bonbon Anglais 30 cl VER",
            "Caprice Bonbon Anglais 33 cl CAN", "Caprice Bonbon Anglais 35 cl PET",
            "Caprice Bonbon Anglais 50 cl PET", "Caprice Grenadine 100 cl VER",
            "Caprice Grenadine 150 cl PET", "Caprice Grenadine 30 cl VER",
            "Caprice Grenadine 33 cl CAN", "Caprice Grenadine 35 cl PET",
            "Caprice Grenadine 50 cl PET", "Caprice Orange 100 cl VER",
            "Caprice Orange 150 cl PET", "Caprice Orange 20L FUT", "Caprice Orange 30 cl VER",
            "Caprice Orange 33 cl CAN", "Caprice Orange 35 cl PET", "Caprice Orange 50 cl PET",
            "Caprice Pomme 100 cl VER", "Caprice Pomme 150 cl PET",
            "Caprice Pomme 30 cl VER", "Caprice Pomme 50 cl PET",
        ],
        "Tonic": ["Tonic 100 cl VER", "Tonic 30 cl VER"],
        "World Cola": [
            "World Cola 100cl VER", "World Cola 100cl WOCO VER", "World Cola 150cl PET",
            "World Cola 30cl VER", "World Cola 30cl WOCO VER", "World Cola 33 cl CAN",
            "World Cola 35cl PET", "World Cola 50cl PET", "World Cola 20L FUT",
        ],
    },
    "BIERES": {
        "Beaufort": ["Beaufort 33 CL CAN", "Beaufort 33CL VER"],
        "FRESH": ["FRESH 33 cl CAN", "FRESH 33 cl EXPORT CAN", "THB Fresh 33 cl VER", "THB Fresh 65 cl VER"],
        "Gold": [
            "Gold 8 50 cl CAN", "Gold 8 50 cl VER", "Gold Blanche 33cl VER",
            "Gold Blanche 50 cl CAN", "Gold Blanche 50 cl VER", "Gold Amigo 33cl VER",
            "Gold Blonde 50 cl CAN", "Gold Blonde 50 cl VER", "Gold Blonde 65 cl VER",
            "Gold Blanche 20L FUT",
        ],
        "Queen": ["Queen s 65 cl VER"],
        "THB": [
            "THB Pilsener 33 cl VER", "THB Pilsener 50 cl CAN", "THB Pilsener 65 cl VER",
            "THB Pilsener 20L FUT", "THB Pilsener 30L FUT", "THB Speciale NOEL 33 cl VER",
            "THB Pilsener 20L Export FUT", "THB Blanche 20L Export FUT",
            "THB Pilsener 30L Export FUT", "THB 8 20L Export FUT",
        ],
    },
    "EAUX": {
        "Cristal": ["Cristal 100 cl VER", "Cristal 150 cl PET", "Cristal 30 cl VER", "Cristal 50 cl VER"],
        "Cristalline": ["Cristalline 100 cl PET", "Cristalline 200 cl PET"],
        "Eau vive": ["Eau vive 150 cl PET", "Eau vive 50 cl PET", "Eau vive 50 cl VER"],
    },
    "Energy": {
        "FOSA": ["FOSA 50 cl CAN"],
        "XXL": ["XXL 30cl BOB VER", "XXL 30cl VER", "XXL 33 cl CAN", "XXL 35cl PET"],
    },
}

FICHIER_BUDGET = "budget_alcomix.json"

# ============================================================
# GESTION DES DONNÉES (avec pandas)
# ============================================================
def charger_donnees():
    if os.path.exists(FICHIER_BUDGET):
        with open(FICHIER_BUDGET, "r", encoding="utf-8") as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(columns=["segment", "marque", "article", "mois", "volume", "prix_unitaire"])

def sauvegarder_donnees(df):
    # On sauvegarde en convertissant le DataFrame en liste de dicts
    df.to_json(FICHIER_BUDGET, orient="records", indent=2, force_ascii=False)

# On utilise st.session_state pour garder les données en mémoire
if "df" not in st.session_state:
    st.session_state.df = charger_donnees()

# ============================================================
# INTERFACE
# ============================================================
st.title("🍹 Budget Alcomix — Volume & CA")
st.markdown("Suivez et simulez votre budget par segment, marque et article.")

# --- SIDEBAR : Ajout de ligne ---
with st.sidebar:
    st.header("➕ Ajouter une ligne")
    
    segment = st.selectbox("Segment", list(CATALOGUE.keys()))
    marque = st.selectbox("Marque", list(CATALOGUE[segment].keys()))
    article = st.selectbox("Article", CATALOGUE[segment][marque])
    
    mois = st.text_input("Mois (YYYY-MM)", value="2025-01")
    volume = st.number_input("Volume", min_value=0, step=100, value=1000)
    prix_unitaire = st.number_input("Prix unitaire (€)", min_value=0.0, step=0.5, value=10.0)
    
    if st.button("Ajouter", type="primary"):
        if len(mois) == 7 and mois[4] == "-":
            nouvelle_ligne = {
                "segment": segment,
                "marque": marque,
                "article": article,
                "mois": mois,
                "volume": volume,
                "prix_unitaire": prix_unitaire
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
            sauvegarder_donnees(st.session_state.df)
            st.success(f"✅ Ajouté : {article} ({mois})")
            st.rerun()
        else:
            st.error("❌ Format du mois invalide. Utilisez YYYY-MM.")

# --- MAIN : Affichage et Analyses ---
df = st.session_state.df

if df.empty:
    st.info("📭 Aucune donnée pour le moment. Ajoutez une ligne via la barre latérale.")
else:
    # Calcul du CA
    df["CA"] = df["volume"] * df["prix_unitaire"]
    
    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Volume Total", f"{df['volume'].sum():,.0f}")
    col2.metric("Chiffre d'Affaires Total", f"{df['CA'].sum():,.2f} €")
    col3.metric("Nombre d'articles", len(df))

    st.divider()

    # --- ONGLETS ---
    tab1, tab2, tab3 = st.tabs(["📊 Visualisation", "📋 Données Brutes", "⚙️ Gestion"])

    with tab1:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("CA par Segment")
            ca_seg = df.groupby("segment")["CA"].sum().reset_index()
            fig1 = px.pie(ca_seg, values="CA", names="segment", hole=0.3)
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_b:
            st.subheader("CA par Mois")
            ca_mois = df.groupby("mois")["CA"].sum().reset_index().sort_values("mois")
            fig2 = px.bar(ca_mois, x="mois", y="CA", text_auto='.2s')
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Top 10 Articles par CA")
        top_art = df.groupby("article")["CA"].sum().nlargest(10).reset_index()
        fig3 = px.bar(top_art, x="CA", y="article", orientation="h")
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Données du Budget")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False, sep=";").encode("utf-8-sig")
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name="budget_alcomix.csv",
            mime="text/csv"
        )

    with tab3:
        st.subheader("Supprimer une ligne")
        index_a_supprimer = st.selectbox(
            "Sélectionnez la ligne à supprimer",
            df.index,
            format_func=lambda i: f"{df.loc[i, 'article']} ({df.loc[i, 'mois']})"
        )
        if st.button("🗑️ Supprimer", type="secondary"):
            st.session_state.df = df.drop(index_a_supprimer).reset_index(drop=True)
            sauvegarder_donnees(st.session_state.df)
            st.success("Ligne supprimée.")
            st.rerun()
