import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(page_title="Simulateur S&OP", page_icon="📈", layout="wide")

st.title("📈 Simulateur S&OP — Prévisions 2026–2031")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]
ANNEES_ALL = ["2026"] + ANNEES

# Liste des marques arrêtées après 2026 (volume = 0 de 2027 à 2031)
MARQUES_ARRETEES = ["BOTA Fresh", "Racines"]

# =====================================================
# TABLEAU 1 - OBJECTIFS GLOBAUX
# =====================================================
st.subheader("1️⃣ Objectifs Globaux (Volumes)")

if "objectifs" not in st.session_state:
    st.session_state.objectifs = pd.DataFrame({
        "Année": ANNEES,
        "Volume": [4600000, 4900000, 5250000, 5600000, 6000000],
    })

df_obj = st.data_editor(
    st.session_state.objectifs,
    column_config={
        "Année": st.column_config.TextColumn("Année", disabled=True),
        "Volume": st.column_config.NumberColumn(
            "Volume Objectif", format="%d", min_value=0, step=10000
        ),
    },
    hide_index=True,
    use_container_width=True,
    key="editor_objectif",
)
st.session_state.objectifs = df_obj

# =====================================================
# TABLEAU 2 - MIX SEGMENT & VALIDATION DES TOTAUX
# =====================================================
st.subheader("2️⃣ Mix Segment (%)")

if "mix" not in st.session_state:
    st.session_state.mix = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy", "TOTAL"],
        "2027": [2.0, 25.0, 55.0, 15.0, 3.0, 100.0],
        "2028": [2.0, 25.0, 55.0, 15.0, 3.0, 100.0],
        "2029": [2.0, 25.0, 55.0, 15.0, 3.0, 100.0],
        "2030": [2.0, 25.0, 55.0, 15.0, 3.0, 100.0],
        "2031": [2.0, 25.0, 55.0, 15.0, 3.0, 100.0],
    })

for annee in ANNEES:
    st.session_state.mix.loc[
        st.session_state.mix["Segment"] == "TOTAL", annee
    ] = st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL", annee
    ].sum()

col_config_mix = {
    "Segment": st.column_config.TextColumn("Segment", disabled=True)
}
for annee in ANNEES:
    col_config_mix[annee] = st.column_config.NumberColumn(
        annee, format="%.1f %%", min_value=0.0, max_value=100.0, step=0.5
    )

df_mix = st.data_editor(
    st.session_state.mix,
    column_config=col_config_mix,
    hide_index=True,
    use_container_width=True,
    key="mix_editor",
)

erreurs_mix = []
for annee in ANNEES:
    st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL", annee
    ] = df_mix.loc[df_mix["Segment"] != "TOTAL", annee].values
    total_annee = st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL", annee
    ].sum()
    st.session_state.mix.loc[
        st.session_state.mix["Segment"] == "TOTAL", annee
    ] = total_annee

    if not np.isclose(total_annee, 100.0, atol=0.01):
        erreurs_mix.append(f"**{annee}** ({total_annee:.1f} %)")

if erreurs_mix:
    st.error(
        f"⚠️ **Attention : Le total du Mix Segment doit être égal à 100 %.** "
        f"Années en erreur : {', '.join(erreurs_mix)}. Les volumes simulés seront faussés tant que le total n'est pas à 100 %."
    )
else:
    st.success(
        "✅ **Validation OK :** Tous les totaux du Mix Segment sont égaux à 100 %."
    )

# =====================================================
# BASE DETAILLEE 2026
# =====================================================
detail = [
    # ALCOMIX
    ["Alcomix", "Booster", "Booster Appel-Mix 50CL VER", 21855],
    ["Alcomix", "Booster", "Booster Tornado 50CL VER VER", 15616],
    ["Alcomix", "BOTA Fresh", "BOTA Fresh 50 cl VER", 1005],
    ["Alcomix", "Racines", "Racines 33 cl VER", 2220],
    # BG - CAPRICE
    ["BG", "Caprice", "Caprice Ananas 100 cl VER", 4386],
    ["BG", "Caprice", "Caprice Ananas 150 cl PET", 22050],
    ["BG", "Caprice", "Caprice Ananas 30 cl VER", 4496],
    ["BG", "Caprice", "Caprice Bonbon Anglais 100 cl VER", 57580],
    ["BG", "Caprice", "Caprice Bonbon Anglais 150 cl PET", 308042],
    ["BG", "Caprice", "Caprice Bonbon Anglais 20L FUT", 79],
    ["BG", "Caprice", "Caprice Bonbon Anglais 30 cl VER", 41261],
    ["BG", "Caprice", "Caprice Bonbon Anglais 33 cl CAN", 4990],
    ["BG", "Caprice", "Caprice Bonbon Anglais 35 cl PET", 19424],
    ["BG", "Caprice", "Caprice Bonbon Anglais 50 cl PET", 137932],
    ["BG", "Caprice", "Caprice Grenadine 100 cl VER", 11739],
    ["BG", "Caprice", "Caprice Grenadine 150 cl PET", 34088],
    ["BG", "Caprice", "Caprice Grenadine 30 cl VER", 4720],
    ["BG", "Caprice", "Caprice Grenadine 33 cl CAN", 2897],
    ["BG", "Caprice", "Caprice Grenadine 35 cl PET", 1886],
    ["BG", "Caprice", "Caprice Grenadine 50 cl PET", 11792],
    ["BG", "Caprice", "Caprice Orange 100 cl VER", 33262],
    ["BG", "Caprice", "Caprice Orange 150 cl PET", 161382],
    ["BG", "Caprice", "Caprice Orange 20L FUT", 75],
    ["BG", "Caprice", "Caprice Orange 30 cl VER", 26172],
    ["BG", "Caprice", "Caprice Orange 33 cl CAN", 3875],
    ["BG", "Caprice", "Caprice Orange 35 cl PET", 5943],
    ["BG", "Caprice", "Caprice Orange 50 cl PET", 59297],
    ["BG", "Caprice", "Caprice Pomme 100 cl VER", 958],
    ["BG", "Caprice", "Caprice Pomme 150 cl PET", 4128],
    ["BG", "Caprice", "Caprice Pomme 30 cl VER", 1595],
    ["BG", "Caprice", "Caprice Pomme 50 cl PET", 0],
    # BG - TONIC
    ["BG", "Tonic", "Tonic 100 cl VER", 7958],
    ["BG", "Tonic", "Tonic 30 cl VER", 17921],
    # BG - WORLD COLA
    ["BG", "World Cola", "World Cola 100cl VER", 4368],
    ["BG", "World Cola", "World Cola 100cl WOCO VER", 24276],
    ["BG", "World Cola", "World Cola 150cl PET", 100927],
    ["BG", "World Cola", "World Cola 30cl VER", 1967],
    ["BG", "World Cola", "World Cola 30cl WOCO VER", 26387],
    ["BG", "World Cola", "World Cola 33 cl CAN", 2832],
    ["BG", "World Cola", "World Cola 35cl PET", 6866],
    ["BG", "World Cola", "World Cola 50cl PET", 54263],
    ["BG", "World Cola", "World Cola 20L FUT", 281],
    # BIERES - BEAUFORT
    ["BIERES", "Beaufort", "Beaufort 33 CL CAN", 13986],
    ["BIERES", "Beaufort", "Beaufort 33CL VER", 34851],
    # BIERES - FRESH
    ["BIERES", "FRESH", "FRESH 33 cl CAN", 3254],
    ["BIERES", "FRESH", "FRESH 33 cl EXPORT CAN", 25],
    ["BIERES", "FRESH", "THB Fresh 33 cl VER", 1881],
    ["BIERES", "FRESH", "THB Fresh 65 cl VER", 35712],
    # BIERES - GOLD
    ["BIERES", "Gold", "Gold 8 50 cl CAN", 1159],
    ["BIERES", "Gold", "Gold 8 50 cl VER", 8661],
    ["BIERES", "Gold", "Gold Blanche 33cl VER", 24605],
    ["BIERES", "Gold", "Gold Blanche 50 cl CAN", 43538],
    ["BIERES", "Gold", "Gold Blanche 50 cl VER", 92121],
    ["BIERES", "Gold", "Gold Amigo 33cl VER", 1463],
    ["BIERES", "Gold", "Gold Blonde 50 cl CAN", 8531],
    ["BIERES", "Gold", "Gold Blonde 50 cl VER", 15872],
    ["BIERES", "Gold", "Gold Blonde 65 cl VER", 58077],
    ["BIERES", "Gold", "Gold Blanche 20L FUT", 1464],
    # BIERES - QUEEN
    ["BIERES", "Queen", "Queen s 65 cl VER", 153975],
    # BIERES - THB
    ["BIERES", "THB", "THB Pilsener 33 cl VER", 96836],
    ["BIERES", "THB", "THB Pilsener 50 cl CAN", 60246],
    ["BIERES", "THB", "THB Pilsener 65 cl VER", 1513573],
    ["BIERES", "THB", "THB Pilsener 20L FUT", 2228],
    ["BIERES", "THB", "THB Pilsener 30L FUT", 0],
    ["BIERES", "THB", "THB Speciale NOEL 33 cl VER", 736],
    ["BIERES", "THB", "THB Pilsener 20L Export FUT", 450],
    ["BIERES", "THB", "THB Blanche 20L Export FUT", 47],
    ["BIERES", "THB", "THB Pilsener 30L Export FUT", 602],
    ["BIERES", "THB", "THB 8 20L Export FUT", 40],
    # EAUX - CRISTAL
    ["EAUX", "Cristal", "Cristal 100 cl VER", 1004],
    ["EAUX", "Cristal", "Cristal 150 cl PET", 4516],
    ["EAUX", "Cristal", "Cristal 30 cl VER", 689],
    ["EAUX", "Cristal", "Cristal 50 cl VER", 4206],
    # EAUX - CRISTALLINE
    ["EAUX", "Cristalline", "Cristalline 100 cl PET", 272844],
    ["EAUX", "Cristalline", "Cristalline 200 cl PET", 268234],
    # EAUX - EAU VIVE
    ["EAUX", "Eau vive", "Eau vive 150 cl PET", 210612],
    ["EAUX", "Eau vive", "Eau vive 50 cl PET", 67919],
    ["EAUX", "Eau vive", "Eau vive 50 cl VER", 364],
    # ENERGY
    ["Energy", "FOSA", "FOSA 50 cl CAN", 3265],
    ["Energy", "XXL", "XXL 30cl BOB VER", 19433],
    ["Energy", "XXL", "XXL 30cl VER", 571],
    ["Energy", "XXL", "XXL 33 cl CAN", 3001],
    ["Energy", "XXL", "XXL 35cl PET", 16357],
]

df_base = pd.DataFrame(detail, columns=["Segment", "Marque", "SKU", "2026"])

# =====================================================
# CALCUL DES POIDS 2026
# =====================================================
# 1. Poids de chaque article (SKU) dans sa marque basé sur les volumes réels 2026
df_base["Vol_Marque_2026"] = df_base.groupby(["Segment", "Marque"])["2026"].transform("sum")
df_base["Poids_SKU"] = np.where(
    df_base["Vol_Marque_2026"] > 0,
    df_base["2026"] / df_base["Vol_Marque_2026"],
    0,
)

# 2. Poids des marques actives dans le segment à partir de 2027
# (Les marques arrêtées passent à 0, reportant leur poids sur les marques restantes)
df_base["Base_Proj_Marque"] = np.where(
    df_base["Marque"].isin(MARQUES_ARRETEES), 0, df_base["2026"]
)
df_base["Vol_Segment_Proj"] = df_base.groupby("Segment")["Base_Proj_Marque"].transform("sum")
df_base["Vol_Marque_Proj"] = df_base.groupby(["Segment", "Marque"])["Base_Proj_Marque"].transform("sum")

df_base["Poids_Marque"] = np.where(
    df_base["Vol_Segment_Proj"] > 0,
    df_base["Vol_Marque_Proj"] / df_base["Vol_Segment_Proj"],
    0,
)

# =====================================================
# CALCUL DES VOLUMES FUTURS
# =====================================================
df_detail = df_base.copy()

for annee in ANNEES:
    objectif = df_obj.loc[df_obj["Année"] == annee, "Volume"].iloc[0]

    mix_map = (
        st.session_state.mix.query("Segment != 'TOTAL'")
        .set_index("Segment")[annee]
        .to_dict()
    )

    volume_segment = {seg: (objectif * pct / 100.0) for seg, pct in mix_map.items()}

    # Volume Marque = Volume Segment * Poids_Marque (0 pour marques arrêtées)
    df_detail[f"MARQUE_{annee}"] = (
        df_detail["Segment"].map(volume_segment) * df_detail["Poids_Marque"]
    )
    # Volume SKU = Volume Marque * Poids_SKU 2026
    df_detail[annee] = df_detail[f"MARQUE_{annee}"] * df_detail["Poids_SKU"]

# =====================================================
# FONCTION DE CONSTRUCTION DU TABLEAU HIERARCHIQUE
# =====================================================
ordre_segments = ["Alcomix", "BG", "BIERES", "EAUX", "Energy"]

def construire_tableau_hierarchique(segments_cibles):
    df_sub = df_detail[df_detail["Segment"].isin(segments_cibles)]
    lignes = []

    label_total = (
        "TOTAL ANNEE"
        if len(segments_cibles) == len(ordre_segments)
        else "TOTAL SÉLECTION"
    )
    ligne_total = {
        "Niveau": "TOTAL",
        "Segment": label_total,
        "Marque": "",
        "SKU": "",
    }
    for annee in ANNEES_ALL:
        ligne_total[annee] = df_sub[annee].sum()
    lignes.append(ligne_total)

    for segment in ordre_segments:
        if segment not in segments_cibles:
            continue
        seg_data = df_sub[df_sub["Segment"] == segment]
        if len(seg_data) == 0:
            continue

        ligne_segment = {
            "Niveau": "SEGMENT",
            "Segment": segment,
            "Marque": "",
            "SKU": "",
        }
        for annee in ANNEES_ALL:
            ligne_segment[annee] = seg_data[annee].sum()
        lignes.append(ligne_segment)

        for marque in seg_data["Marque"].unique():
            marq_data = seg_data[seg_data["Marque"] == marque]

            ligne_marque = {
                "Niveau": "MARQUE",
                "Segment": "",
                "Marque": marque,
                "SKU": "",
            }
            for annee in ANNEES_ALL:
                ligne_marque[annee] = marq_data[annee].sum()
            lignes.append(ligne_marque)

            for _, row in marq_data.iterrows():
                ligne_sku = {
                    "Niveau": "SKU",
                    "Segment": "",
                    "Marque": "",
                    "SKU": row["SKU"],
                }
                for annee in ANNEES_ALL:
                    ligne_sku[annee] = row[annee]
                lignes.append(ligne_sku)

    return pd.DataFrame(lignes)

# =====================================================
# GRAPHIQUES D'EVOLUTION
# =====================================================
st.divider()
st.subheader("📊 Visualisation des Évolutions (2026–2031)")

col_g1, col_g2 = st.columns(2)

df_chart_seg = df_detail.groupby("Segment", as_index=False)[ANNEES_ALL].sum()
df_chart_seg_melt = df_chart_seg.melt(
    id_vars="Segment", var_name="Année", value_name="Volume"
)

with col_g1:
    fig_bar = px.bar(
        df_chart_seg_melt,
        x="Année",
        y="Volume",
        color="Segment",
        title="Évolution des Volumes par Segment (Empilé)",
        text_auto=".2s",
    )
    fig_bar.update_layout(yaxis_title="Volume", xaxis_title="Année")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_g2:
    fig_line = px.line(
        df_chart_seg_melt,
        x="Année",
        y="Volume",
        color="Segment",
        markers=True,
        title="Trajectoire de Croissance par Segment",
    )
    fig_line.update_layout(yaxis_title="Volume", xaxis_title="Année")
    st.plotly_chart(fig_line, use_container_width=True)

# =====================================================
# AFFICHAGE DU TABLEAU HIERARCHIQUE AVEC FILTRE SEGMENT
# =====================================================
st.divider()
st.subheader("3️⃣ Volumes Simulés Détaillés")

segments_selectionnes = st.multiselect(
    "🔍 Filtrer par Segment :",
    options=ordre_segments,
    default=ordre_segments,
    placeholder="Choisissez un ou plusieurs segments...",
)

def style_hierarchie(row):
    if row["Niveau"] == "TOTAL":
        return ["background-color: #1f4e78; color: white; font-weight: bold"] * len(row)
    elif row["Niveau"] == "SEGMENT":
        return ["background-color: #d9e1f2; font-weight: bold"] * len(row)
    elif row["Niveau"] == "MARQUE":
        return ["background-color: #f2f2f2; font-weight: bold"] * len(row)
    return [""] * len(row)

if not segments_selectionnes:
    st.info("Veuillez sélectionner au moins un segment dans le filtre ci-dessus pour afficher le tableau.")
else:
    df_affichage_filtre = construire_tableau_hierarchique(segments_selectionnes)
    st.dataframe(
        df_affichage_filtre.style.apply(style_hierarchie, axis=1).format(
            {annee: "{:,.0f}" for annee in ANNEES_ALL}
        ),
        column_order=["Segment", "Marque", "SKU"] + ANNEES_ALL,
        hide_index=True,
        use_container_width=True,
        height=900,
    )

# =====================================================
# EXPORT EXCEL COMPLET (TOUS LES SEGMENTS)
# =====================================================
st.divider()

df_export_complet = construire_tableau_hierarchique(ordre_segments).drop(columns=["Niveau"])

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_obj.to_excel(writer, sheet_name="1_Objectifs", index=False)
    st.session_state.mix.to_excel(writer, sheet_name="2_Mix_Segment", index=False)
    df_export_complet.to_excel(writer, sheet_name="3_Simulation_SKU", index=False)

    for sheetname in writer.sheets:
        worksheet = writer.sheets[sheetname]
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except Exception:
                    pass
            worksheet.column_dimensions[column].width = max_length + 4

buffer.seek(0)

st.download_button(
    label="📥 Télécharger le fichier Excel complet (.xlsx)",
    data=buffer,
    file_name="Simulation_SOP_2026_2031.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary",
)
