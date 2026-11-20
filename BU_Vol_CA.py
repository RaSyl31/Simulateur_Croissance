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
# TABLEAU 2 - MIX SEGMENT (%) PAR DÉFAUT
# =====================================================
st.subheader("2️⃣ Mix Segment (%)")

# Mix exacts issus de votre tableau de référence (image_59e874.png)
# Ordre : Alcomix, BG, BIERES, EAUX, Energy
if "mix" not in st.session_state:
    st.session_state.mix = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy", "TOTAL"],
        "2027": [
            45969 / 4600000 * 100,    # 1.00 % -> 45 969
            1258992 / 4600000 * 100,  # 27.37 % -> 1 258 992
            2369000 / 4600000 * 100,  # 51.50 % -> 2 369 000
            855039 / 4600000 * 100,   # 18.59 % -> 855 039
            71000 / 4600000 * 100,    # 1.54 % -> 71 000
            100.00,
        ],
        "2028": [1.00, 26.60, 51.50, 19.25, 1.65, 100.00],
        "2029": [1.00, 27.80, 51.50, 18.00, 1.70, 100.00],
        "2030": [1.00, 27.90, 51.50, 17.75, 1.80, 99.95],
        "2031": [1.00, 28.00, 51.50, 17.50, 2.00, 100.00],
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
        annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.05
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

    if not np.isclose(total_annee, 100.0, atol=0.06):
        erreurs_mix.append(f"**{annee}** ({total_annee:.2f} %)")

if erreurs_mix:
    st.error(
        f"⚠️ **Attention : Le total du Mix Segment doit être égal à 100 %.** "
        f"Années en erreur : {', '.join(erreurs_mix)}."
    )
else:
    st.success(
        "✅ **Validation OK :** Tous les totaux du Mix Segment sont conformes."
    )

# =====================================================
# BASE DETAILLEE : VOLUMES 2026 & BASE DE POIDS 2027
# Colonnes : [Segment, Marque, SKU, Vol_2026, Base_2027]
# =====================================================
detail = [
    # ALCOMIX
    ["Alcomix", "Booster", "Booster Appel-Mix 50CL VER", 21855, 26734],
    ["Alcomix", "Booster", "Booster Tornado 50CL VER VER", 15616, 19234],
    ["Alcomix", "BOTA Fresh", "BOTA Fresh 50 cl VER", 1005, 0],
    ["Alcomix", "Racines", "Racines 33 cl VER", 2220, 0],
    # BG - CAPRICE
    ["BG", "Caprice", "Caprice Ananas 100 cl VER", 4386, 4614],
    ["BG", "Caprice", "Caprice Ananas 150 cl PET", 22050, 22156],
    ["BG", "Caprice", "Caprice Ananas 30 cl VER", 4496, 4677],
    ["BG", "Caprice", "Caprice Bonbon Anglais 100 cl VER", 57580, 57543],
    ["BG", "Caprice", "Caprice Bonbon Anglais 150 cl PET", 308042, 311325],
    ["BG", "Caprice", "Caprice Bonbon Anglais 20L FUT", 79, 76],
    ["BG", "Caprice", "Caprice Bonbon Anglais 30 cl VER", 41261, 41451],
    ["BG", "Caprice", "Caprice Bonbon Anglais 33 cl CAN", 4990, 5872],
    ["BG", "Caprice", "Caprice Bonbon Anglais 35 cl PET", 19424, 20125],
    ["BG", "Caprice", "Caprice Bonbon Anglais 50 cl PET", 137932, 143586],
    ["BG", "Caprice", "Caprice Grenadine 100 cl VER", 11739, 13276],
    ["BG", "Caprice", "Caprice Grenadine 150 cl PET", 34088, 35314],
    ["BG", "Caprice", "Caprice Grenadine 30 cl VER", 4720, 4988],
    ["BG", "Caprice", "Caprice Grenadine 33 cl CAN", 2897, 3445],
    ["BG", "Caprice", "Caprice Grenadine 35 cl PET", 1886, 3514],
    ["BG", "Caprice", "Caprice Grenadine 50 cl PET", 11792, 13307],
    ["BG", "Caprice", "Caprice Orange 100 cl VER", 33262, 34726],
    ["BG", "Caprice", "Caprice Orange 150 cl PET", 161382, 172106],
    ["BG", "Caprice", "Caprice Orange 20L FUT", 75, 76],
    ["BG", "Caprice", "Caprice Orange 30 cl VER", 26172, 26934],
    ["BG", "Caprice", "Caprice Orange 33 cl CAN", 3875, 4631],
    ["BG", "Caprice", "Caprice Orange 35 cl PET", 5943, 5583],
    ["BG", "Caprice", "Caprice Orange 50 cl PET", 59297, 61398],
    ["BG", "Caprice", "Caprice Pomme 100 cl VER", 958, 0],
    ["BG", "Caprice", "Caprice Pomme 150 cl PET", 4128, 0],
    ["BG", "Caprice", "Caprice Pomme 30 cl VER", 1595, 0],
    ["BG", "Caprice", "Caprice Pomme 50 cl PET", 0, 0],
    # BG - TONIC
    ["BG", "Tonic", "Tonic 100 cl VER", 7958, 8472],
    ["BG", "Tonic", "Tonic 30 cl VER", 17921, 19010],
    # BG - WORLD COLA
    ["BG", "World Cola", "World Cola 100cl VER", 4368, 4251],
    ["BG", "World Cola", "World Cola 100cl WOCO VER", 24276, 21268],
    ["BG", "World Cola", "World Cola 150cl PET", 100927, 101951],
    ["BG", "World Cola", "World Cola 30cl VER", 1967, 2232],
    ["BG", "World Cola", "World Cola 30cl WOCO VER", 26387, 27030],
    ["BG", "World Cola", "World Cola 33 cl CAN", 2832, 3192],
    ["BG", "World Cola", "World Cola 35cl PET", 6866, 8700],
    ["BG", "World Cola", "World Cola 50cl PET", 54263, 57596],
    ["BG", "World Cola", "World Cola 20L FUT", 281, 272],
    # BIERES - BEAUFORT
    ["BIERES", "Beaufort", "Beaufort 33 CL CAN", 13986, 14650],
    ["BIERES", "Beaufort", "Beaufort 33CL VER", 34851, 36111],
    # BIERES - FRESH
    ["BIERES", "FRESH", "FRESH 33 cl CAN", 3254, 3771],
    ["BIERES", "FRESH", "FRESH 33 cl EXPORT CAN", 25, 0],
    ["BIERES", "FRESH", "THB Fresh 33 cl VER", 1881, 2058],
    ["BIERES", "FRESH", "THB Fresh 65 cl VER", 35712, 38200],
    # BIERES - GOLD
    ["BIERES", "Gold", "Gold 8 50 cl CAN", 1159, 1242],
    ["BIERES", "Gold", "Gold 8 50 cl VER", 8661, 9342],
    ["BIERES", "Gold", "Gold Blanche 33cl VER", 24605, 26491],
    ["BIERES", "Gold", "Gold Blanche 50 cl CAN", 43538, 46234],
    ["BIERES", "Gold", "Gold Blanche 50 cl VER", 92121, 101300],
    ["BIERES", "Gold", "Gold Amigo 33cl VER", 1463, 0],
    ["BIERES", "Gold", "Gold Blonde 50 cl CAN", 8531, 9400],
    ["BIERES", "Gold", "Gold Blonde 50 cl VER", 15872, 17086],
    ["BIERES", "Gold", "Gold Blonde 65 cl VER", 58077, 60603],
    ["BIERES", "Gold", "Gold Blanche 20L FUT", 1464, 1297],
    # BIERES - QUEEN
    ["BIERES", "Queen", "Queen s 65 cl VER", 153975, 163506],
    # BIERES - THB
    ["BIERES", "THB", "THB Pilsener 33 cl VER", 96836, 102020],
    ["BIERES", "THB", "THB Pilsener 50 cl CAN", 60246, 63912],
    ["BIERES", "THB", "THB Pilsener 65 cl VER", 1513573, 1668977],
    ["BIERES", "THB", "THB Pilsener 20L FUT", 2228, 2129],
    ["BIERES", "THB", "THB Pilsener 30L FUT", 0, 652],
    ["BIERES", "THB", "THB Speciale NOEL 33 cl VER", 736, 0],
    ["BIERES", "THB", "THB Pilsener 20L Export FUT", 450, 0],
    ["BIERES", "THB", "THB Blanche 20L Export FUT", 47, 0],
    ["BIERES", "THB", "THB Pilsener 30L Export FUT", 602, 0],
    ["BIERES", "THB", "THB 8 20L Export FUT", 40, 0],
    # EAUX - CRISTAL
    ["EAUX", "Cristal", "Cristal 100 cl VER", 1004, 1113],
    ["EAUX", "Cristal", "Cristal 150 cl PET", 4516, 4684],
    ["EAUX", "Cristal", "Cristal 30 cl VER", 689, 743],
    ["EAUX", "Cristal", "Cristal 50 cl VER", 4206, 4480],
    # EAUX - CRISTALLINE
    ["EAUX", "Cristalline", "Cristalline 100 cl PET", 272844, 292992],
    ["EAUX", "Cristalline", "Cristalline 200 cl PET", 268234, 287015],
    # EAUX - EAU VIVE
    ["EAUX", "Eau vive", "Eau vive 150 cl PET", 210612, 192457],
    ["EAUX", "Eau vive", "Eau vive 50 cl PET", 67919, 71266],
    ["EAUX", "Eau vive", "Eau vive 50 cl VER", 364, 2296],
    # ENERGY
    ["Energy", "FOSA", "FOSA 50 cl CAN", 3265, 15000],
    ["Energy", "XXL", "XXL 30cl BOB VER", 19433, 21868],
    ["Energy", "XXL", "XXL 30cl VER", 571, 794],
    ["Energy", "XXL", "XXL 33 cl CAN", 3001, 4275],
    ["Energy", "XXL", "XXL 35cl PET", 16357, 29070],
]

df_base = pd.DataFrame(
    detail, columns=["Segment", "Marque", "SKU", "2026", "Base_2027"]
)

# =====================================================
# CALCUL DES POIDS 2027 (MARQUE DANS SEGMENT + SKU DANS MARQUE)
# =====================================================
# 1. Volume total de chaque Segment sur la base 2027
df_base["Vol_Segment_2027"] = df_base.groupby("Segment")["Base_2027"].transform("sum")

# 2. Volume total de chaque Marque (au sein de son Segment) sur la base 2027
df_base["Vol_Marque_2027"] = df_base.groupby(["Segment", "Marque"])["Base_2027"].transform("sum")

# 3. Poids de chaque Marque dans son Segment (base 2027) -> somme = 100% par segment
df_base["Poids_Marque_2027"] = np.where(
    df_base["Vol_Segment_2027"] > 0,
    df_base["Vol_Marque_2027"] / df_base["Vol_Segment_2027"],
    0.0,
)

# 4. Poids de chaque SKU dans sa Marque (base 2027) -> somme = 100% par marque
df_base["Poids_SKU_2027"] = np.where(
    df_base["Vol_Marque_2027"] > 0,
    df_base["Base_2027"] / df_base["Vol_Marque_2027"],
    0.0,
)

# =====================================================
# CALCUL DES VOLUMES (2027 - 2031)
# =====================================================
df_detail = df_base.copy()

for annee in ANNEES:
    objectif = df_obj.loc[df_obj["Année"] == annee, "Volume"].iloc[0]

    mix_map = (
        st.session_state.mix.query("Segment != 'TOTAL'")
        .set_index("Segment")[annee]
        .to_dict()
    )

    # Volume du Segment = Objectif Annuel * Mix Segment (%)
    volume_segment = {seg: (objectif * pct / 100.0) for seg, pct in mix_map.items()}

    # Volume de la Marque = Volume Segment * Poids Marque dans Segment (2027)
    df_detail[f"MARQUE_{annee}"] = (
        df_detail["Segment"].map(volume_segment) * df_detail["Poids_Marque_2027"]
    )

    # Volume du SKU = Volume Marque * Poids SKU dans Marque (2027)
    df_detail[annee] = df_detail[f"MARQUE_{annee}"] * df_detail["Poids_SKU_2027"]

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
        return ["background-color: #FFF2CC; color: black; font-weight: bold"] * len(row)
    elif row["Niveau"] == "SEGMENT":
        return ["background-color: #C00000; color: white; font-weight: bold"] * len(row)
    elif row["Niveau"] == "MARQUE":
        return ["background-color: #F8CBAD; color: black; font-weight: bold"] * len(row)
    return [""] * len(row)

def format_cellule(val):
    if pd.isna(val) or val == 0:
        return "-"
    return f"{val:,.0f}".replace(",", " ")

if not segments_selectionnes:
    st.info("Veuillez sélectionner au moins un segment dans le filtre ci-dessus.")
else:
    df_affichage_filtre = construire_tableau_hierarchique(segments_selectionnes)
    st.dataframe(
        df_affichage_filtre.style.apply(style_hierarchie, axis=1).format(
            {annee: format_cellule for annee in ANNEES_ALL}
        ),
        column_order=["Segment", "Marque", "SKU"] + ANNEES_ALL,
        hide_index=True,
        use_container_width=True,
        height=950,
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
