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
    "Alcomix": {"Booster": {"Booster Appel-Mix 50CL VER": 21855, "Booster Tornado 50CL VER VER": 15616}, "BOTA Fresh": {"BOTA Fresh 50 cl VER": 1005}, "Racines": {"Racines 33 cl VER": 2220}},
    "BG": {"Caprice": {"Caprice Ananas 100 cl VER": 4386, "Caprice Ananas 150 cl PET": 22050, "Caprice Ananas 30 cl VER": 4496, "Caprice Bonbon Anglais 100 cl VER": 57580, "Caprice Bonbon Anglais 150 cl PET": 308042, "Caprice Bonbon Anglais 20L FUT": 79, "Caprice Bonbon Anglais 30 cl VER": 41261, "Caprice Bonbon Anglais 33 cl CAN": 4990, "Caprice Bonbon Anglais 35 cl PET": 19424, "Caprice Bonbon Anglais 50 cl PET": 137932, "Caprice Grenadine 100 cl VER": 11739, "Caprice Grenadine 150 cl PET": 34088, "Caprice Grenadine 30 cl VER": 4720, "Caprice Grenadine 33 cl CAN": 2897, "Caprice Grenadine 35 cl PET": 1886, "Caprice Grenadine 50 cl PET": 11792, "Caprice Orange 100 cl VER": 33262, "Caprice Orange 150 cl PET": 161382, "Caprice Orange 20L FUT": 75, "Caprice Orange 30 cl VER": 26172, "Caprice Orange 33 cl CAN": 3875, "Caprice Orange 35 cl PET": 5943, "Caprice Orange 50 cl PET": 59297, "Caprice Pomme 100 cl VER": 958, "Caprice Pomme 150 cl PET": 4128, "Caprice Pomme 30 cl VER": 1595, "Caprice Pomme 50 cl PET": 0}, "Tonic": {"Tonic 100 cl VER": 7958, "Tonic 30 cl VER": 17921}, "World Cola": {"World Cola 100cl VER": 4368, "World Cola 100cl WOCO VER": 24276, "World Cola 150cl PET": 100927, "World Cola 30cl VER": 1967, "World Cola 30cl WOCO VER": 26387, "World Cola 33 cl CAN": 2832, "World Cola 35cl PET": 6866, "World Cola 50cl PET": 54263, "World Cola 20L FUT": 281}},
    "BIERES": {"Beaufort": {"Beaufort 33 CL CAN": 13986, "Beaufort 33CL VER": 34851}, "FRESH": {"FRESH 33 cl CAN": 3254, "FRESH 33 cl EXPORT CAN": 25, "THB Fresh 33 cl VER": 1881, "THB Fresh 65 cl VER": 35712}, "Gold": {"Gold 8 50 cl CAN": 1159, "Gold 8 50 cl VER": 8661, "Gold Blanche 33cl VER": 24605, "Gold Blanche 50 cl CAN": 43538, "Gold Blanche 50 cl VER": 92121, "Gold Amigo 33cl VER": 1463, "Gold Blonde 50 cl CAN": 8531, "Gold Blonde 50 cl VER": 15872, "Gold Blonde 65 cl VER": 58077, "Gold Blanche 20L FUT": 1464}, "Queen": {"Queen s 65 cl VER": 153975}, "THB": {"THB Pilsener 33 cl VER": 96836, "THB Pilsener 50 cl CAN": 60246, "THB Pilsener 65 cl VER": 1513573, "THB Pilsener 20L FUT": 2228, "THB Pilsener 30L FUT": 0, "THB Speciale NOEL 33 cl VER": 736, "THB Pilsener 20L Export FUT": 450, "THB Blanche 20L Export FUT": 47, "THB Pilsener 30L Export FUT": 602, "THB 8 20L Export FUT": 40}},
    "EAUX": {"Cristal": {"Cristal 100 cl VER": 1004, "Cristal 150 cl PET": 4516, "Cristal 30 cl VER": 689, "Cristal 50 cl VER": 4206}, "Cristalline": {"Cristalline 100 cl PET": 272844, "Cristalline 200 cl PET": 268234}, "Eau vive": {"Eau vive 150 cl PET": 210612, "Eau vive 50 cl PET": 67919, "Eau vive 50 cl VER": 364}},
    "Energy": {"FOSA": {"FOSA 50 cl CAN": 3265}, "XXL": {"XXL 30cl BOB VER": 19433, "XXL 30cl VER": 571, "XXL 33 cl CAN": 3001, "XXL 35cl PET": 16357}},
}
PRODUITS_ARRETES = ["BOTA Fresh 50 cl VER", "Racines 33 cl VER"]

# ============================================================
# PREPARATION DES DONNÉES ET CALCUL DU MIX INITIAL
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
    
    # Calcul des poids (Mix)
    total_2026 = df["2026"].sum()
    df["Poids_Segment"] = df.groupby("Segment")["2026"].transform("sum") / total_2026
    df["Poids_Marque"] = df.groupby(["Segment", "Marque"])["2026"].transform("sum") / df.groupby("Segment")["2026"].transform("sum")
    df["Poids_Article"] = df["2026"] / df.groupby(["Segment", "Marque"])["2026"].transform("sum")
    
    return df, total_2026

df_base, TOTAL_2026 = preparer_donnees()

# ============================================================
# INITIALISATION DE L'ÉTAT (Session State)
# ============================================================
if "objets_seg" not in st.session_state:
    # On initialise les objectifs de base avec une croissance de +5% par an pour l'exemple
    st.session_state.objets_seg = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy"],
        "2027": [40700, 1270000, 2280000, 870000, 44700],
        "2028": [42700, 1330000, 2390000, 910000, 46900],
        "2029": [44900, 1400000, 2510000, 955000, 49200],
        "2030": [47100, 1470000, 2630000, 1000000, 51600],
    })

# ============================================================
# TABLEAU 1 : SAISIE DES OBJECTIFS
# ============================================================
st.title("🎯 Pilotage des Objectifs")

st.markdown("### 1. Saisie des objectifs par Segment (Modifiable)")
st.caption("Double-cliquez sur les cellules pour ajuster les objectifs.")

# Le Data Editor permet de modifier les valeurs
edited_df = st.data_editor(
    st.session_state.objets_seg,
    column_config={
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "2027": st.column_config.NumberColumn("2027", format="%d"),
        "2028": st.column_config.NumberColumn("2028", format="%d"),
        "2029": st.column_config.NumberColumn("2029", format="%d"),
        "2030": st.column_config.NumberColumn("2030", format="%d"),
    },
    hide_index=True,
    use_container_width=True,
    key="editeur_segments"
)

# Mise à jour de l'état
st.session_state.objets_seg = edited_df

# Calcul des totaux par année
totaux_annuels = edited_df[["2027", "2028", "2029", "2030"]].sum().to_dict()

# Affichage du tableau formaté avec les totaux en bas
df_affichage = edited_df.copy()
ligne_total = pd.DataFrame([{"Segment": "TOTAL OBJECTIF", "2027": totaux_annuels["2027"], "2028": totaux_annuels["2028"], "2029": totaux_annuels["2029"], "2030": totaux_annuels["2030"]}])
df_affichage = pd.concat([df_affichage, ligne_total], ignore_index=True)

st.markdown("**Tableau de synthèse des objectifs :**")
st.dataframe(
    df_affichage.style.format({
        "2027": "{:,.0f}", "2028": "{:,.0f}", "2029": "{:,.0f}", "2030": "{:,.0f}"
    }).apply(lambda x: ['background: #f0f2f6' if x.name == len(df_affichage)-1 else '' for _ in x], axis=1),
    hide_index=True,
    use_container_width=True
)

# ============================================================
# TABLEAU 2 : MIX MENSUEL
# ============================================================
st.markdown("---")
st.markdown("### 2. Répartition Mensuelle (Mix et Moyenne)")
st.caption("Le mix est calculé en fonction des poids de 2026, et le volume est basé sur les objectifs saisis ci-dessus.")

# Choix de l'année pour le tableau mensuel
annee_cible = st.selectbox("Sélectionnez l'année :", ["2027", "2028", "2029", "2030"])

# Création du tableau mensuel
df_mensuel = edited_df[["Segment", annee_cible]].copy()
df_mensuel.rename(columns={annee_cible: "Objectif Annuel"}, inplace=True)

# Calcul du Mix %
df_mensuel["Mix %"] = (df_mensuel["Objectif Annuel"] / df_mensuel["Objectif Annuel"].sum()) * 100

# Calcul de la moyenne mensuelle (Objectif / 12)
df_mensuel["Moyenne Mensuelle"] = df_mensuel["Objectif Annuel"] / 12

# Affichage
st.dataframe(
    df_mensuel.style.format({
        "Objectif Annuel": "{:,.0f}",
        "Mix %": "{:.1f} %",
        "Moyenne Mensuelle": "{:,.0f}"
    }),
    hide_index=True,
    use_container_width=True
)

# ============================================================
# TABLEAU 3 : IMPACT DÉTAILLÉ (Calculé automatiquement)
# ============================================================
st.markdown("---")
st.markdown("### 3. Impact sur les Marques et Articles")

# On recalcule les volumes des marques et articles en fonction des nouveaux objectifs saisis
df_calcul = df_base.copy()

for annee in ["2027", "2028", "2029", "2030"]:
    # On crée un dictionnaire des objectifs par segment pour cette année
    objectifs_dict = edited_df.set_index("Segment")[annee].to_dict()
    
    # Nouveau volume de l'article = (Objectif du segment) * (Poids de la marque dans le segment) * (Poids de l'article dans la marque)
    df_calcul[annee] = df_calcul["Segment"].map(objectifs_dict) * df_calcul["Poids_Marque"] * df_calcul["Poids_Article"]

# Affichage des accordéons par segment
for segment in df_calcul["Segment"].unique():
    with st.expander(f"Voir le détail pour le segment : {segment}"):
        df_seg = df_calcul[df_calcul["Segment"] == segment]
        
        # Vue par Marque
        df_marques = df_seg.groupby("Marque")[["2027", "2028", "2029", "2030"]].sum()
        st.markdown("**Volumes par Marque**")
        st.dataframe(df_marques.style.format("{:,.0f}"), use_container_width=True)
        
        # Vue par Article
        df_articles = df_seg.set_index(["Marque", "Article"])[["2027", "2028", "2029", "2030"]]
        st.markdown("**Volumes par Article (SKU)**")
        st.dataframe(df_articles.style.format("{:,.0f}"), use_container_width=True)
