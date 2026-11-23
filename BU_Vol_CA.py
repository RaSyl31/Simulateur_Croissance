import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(page_title="Simulateur S&OP", page_icon="📈", layout="wide")

st.title("📈 Simulateur S&OP — Prévisions 2026–2031")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]
ANNEES_ALL = ["2026"] + ANNEES
ORDRE_SEGMENTS = ["Alcomix", "BG", "BIERES", "EAUX", "Energy"]

# =====================================================
# BASE DETAILLEE : VOLUMES 2026 & BASE DE POIDS 2027
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

# Calcul des poids initiaux 2027 (en %)
df_base["Vol_Segment_2027"] = df_base.groupby("Segment")["Base_2027"].transform("sum")
df_base["Vol_Marque_2027"] = df_base.groupby(["Segment", "Marque"])["Base_2027"].transform("sum")

df_base["Poids_Marque_Init"] = np.where(
    df_base["Vol_Segment_2027"] > 0,
    (df_base["Vol_Marque_2027"] / df_base["Vol_Segment_2027"]) * 100.0,
    0.0,
)
df_base["Poids_SKU_Init"] = np.where(
    df_base["Vol_Marque_2027"] > 0,
    (df_base["Base_2027"] / df_base["Vol_Marque_2027"]) * 100.0,
    0.0,
)

# =====================================================
# INITIALISATION DES TABLES DE POIDS EDITABLES EN SESSION
# =====================================================
if "poids_marques" not in st.session_state:
    df_pm_init = (
        df_base[["Segment", "Marque", "Poids_Marque_Init"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    for annee in ANNEES:
        df_pm_init[annee] = df_pm_init["Poids_Marque_Init"]
    st.session_state.poids_marques = df_pm_init.drop(columns=["Poids_Marque_Init"])

if "poids_skus" not in st.session_state:
    df_ps_init = df_base[["Segment", "Marque", "SKU", "Poids_SKU_Init"]].copy()
    for annee in ANNEES:
        df_ps_init[annee] = df_ps_init["Poids_SKU_Init"]
    st.session_state.poids_skus = df_ps_init.drop(columns=["Poids_SKU_Init"])

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

if "mix" not in st.session_state:
    st.session_state.mix = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy", "TOTAL"],
        "2027": [
            45969 / 4600000 * 100,
            1258992 / 4600000 * 100,
            2369000 / 4600000 * 100,
            855039 / 4600000 * 100,
            71000 / 4600000 * 100,
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
# SECTION 3 - MODIFICATION DES POIDS MARQUES & ARTICLES
# =====================================================
st.divider()
st.subheader("3️⃣ Paramétrage des Poids : Marques & Articles (%)")

if st.button("🔄 Réinitialiser tous les poids (Base 2027)"):
    del st.session_state["poids_marques"]
    del st.session_state["poids_skus"]
    st.rerun()

tab_pm, tab_ps = st.tabs([
    "🏷️ Poids des Marques dans chaque Segment (%)",
    "📦 Poids des Articles (SKU) dans chaque Marque (%)",
])

# --- ONGLET A : POIDS DES MARQUES DANS UN SEGMENT ---
with tab_pm:
    seg_filtre_pm = st.selectbox(
        "Sélectionner un Segment à modifier :",
        options=["Tous les segments"] + ORDRE_SEGMENTS,
        key="sel_seg_pm",
    )

    df_pm_view = st.session_state.poids_marques.copy()
    if seg_filtre_pm != "Tous les segments":
        df_pm_view = df_pm_view[df_pm_view["Segment"] == seg_filtre_pm]

    col_cfg_pm = {
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "Marque": st.column_config.TextColumn("Marque", disabled=True),
    }
    for annee in ANNEES:
        col_cfg_pm[annee] = st.column_config.NumberColumn(
            annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1
        )

    df_pm_edited = st.data_editor(
        df_pm_view,
        column_config=col_cfg_pm,
        hide_index=True,
        use_container_width=True,
        key="editor_poids_marques",
    )

    for idx, row in df_pm_edited.iterrows():
        mask = (st.session_state.poids_marques["Segment"] == row["Segment"]) & (
            st.session_state.poids_marques["Marque"] == row["Marque"]
        )
        for annee in ANNEES:
            st.session_state.poids_marques.loc[mask, annee] = row[annee]

    erreurs_pm = []
    segs_a_verifier = (
        ORDRE_SEGMENTS if seg_filtre_pm == "Tous les segments" else [seg_filtre_pm]
    )
    for seg in segs_a_verifier:
        sub_pm = st.session_state.poids_marques[
            st.session_state.poids_marques["Segment"] == seg
        ]
        for annee in ANNEES:
            somme = sub_pm[annee].sum()
            if not np.isclose(somme, 100.0, atol=0.05):
                erreurs_pm.append(f"**{seg} ({annee})** : {somme:.2f} %")

    if erreurs_pm:
        st.warning(
            f"⚠️ La somme des poids des marques d'un segment doit faire 100 %. Écarts détectés : {', '.join(erreurs_pm)}"
        )
    else:
        st.success("✅ Somme des poids des marques = 100 % pour chaque segment.")

# --- ONGLET B : POIDS DES ARTICLES (SKU) DANS UNE MARQUE (UPLOAD + MANUEL) ---
with tab_ps:
    with st.expander("📤 Importer les poids SKU via fichier (Excel / CSV) — Colonnes : Article | mix", expanded=False):
        col_up1, col_up2, col_up3 = st.columns([2, 1, 1])

        with col_up1:
            uploaded_sku_file = st.file_uploader(
                "Charger un fichier (.xlsx ou .csv) avec 2 colonnes : 'Article' et 'mix'",
                type=["xlsx", "xls", "csv"],
                key="upload_sku_mix",
            )

        with col_up2:
            cible_annees_upload = st.selectbox(
                "Appliquer sur :",
                options=["Toutes les années (2027–2031)"] + ANNEES,
                key="upload_target_years",
            )

        with col_up3:
            # Bouton pour télécharger un modèle Excel prêt à remplir
            df_template = st.session_state.poids_skus[["SKU", "2027"]].rename(
                columns={"SKU": "Article", "2027": "mix"}
            )
            buf_tpl = io.BytesIO()
            with pd.ExcelWriter(buf_tpl, engine="openpyxl") as w_tpl:
                df_template.to_excel(w_tpl, sheet_name="Poids_SKU", index=False)
            buf_tpl.seek(0)
            st.write("")
            st.download_button(
                "📄 Modèle Excel (.xlsx)",
                data=buf_tpl,
                file_name="Modele_Poids_SKU.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        if uploaded_sku_file is not None:
            if st.button("✅ Appliquer le fichier importé", type="primary", key="btn_apply_upload"):
                try:
                    if uploaded_sku_file.name.endswith(".csv"):
                        try:
                            df_up = pd.read_csv(uploaded_sku_file, sep=None, engine="python")
                        except Exception:
                            uploaded_sku_file.seek(0)
                            df_up = pd.read_csv(uploaded_sku_file, sep=";")
                    else:
                        df_up = pd.read_excel(uploaded_sku_file)

                    # Normalisation des noms de colonnes (insensible à la casse / espaces)
                    cols_norm = {str(c).strip().lower(): c for c in df_up.columns}
                    if "article" not in cols_norm or "mix" not in cols_norm:
                        st.error(
                            f"❌ Colonnes attendues : **Article** et **mix**. Colonnes trouvées : {list(df_up.columns)}"
                        )
                    else:
                        col_art = cols_norm["article"]
                        col_mix = cols_norm["mix"]

                        df_up_clean = df_up[[col_art, col_mix]].dropna(subset=[col_art]).copy()
                        df_up_clean["Article_clean"] = df_up_clean[col_art].astype(str).str.strip()

                        # Nettoyage des valeurs numériques (gestion virgule, symbole %, ou décimal 0..1)
                        def parse_mix_val(v):
                            if pd.isna(v):
                                return np.nan
                            if isinstance(v, str):
                                s = v.replace("%", "").replace(",", ".").strip()
                                val = float(s)
                            else:
                                val = float(v)
                            return val

                        df_up_clean["mix_num"] = df_up_clean[col_mix].apply(parse_mix_val)

                        # Si toutes les valeurs sont <= 1.0 (format ratio Excel 0.45 pour 45%), convertir en %
                        if df_up_clean["mix_num"].max() <= 1.0 and df_up_clean["mix_num"].sum() > 0:
                            df_up_clean["mix_num"] = df_up_clean["mix_num"] * 100.0

                        annees_cibles = (
                            ANNEES
                            if cible_annees_upload == "Toutes les années (2027–2031)"
                            else [cible_annees_upload]
                        )

                        skus_connus = set(st.session_state.poids_skus["SKU"].str.strip())
                        nb_maj = 0
                        non_trouves = []

                        for _, r_up in df_up_clean.iterrows():
                            art = r_up["Article_clean"]
                            val_m = r_up["mix_num"]
                            if pd.isna(val_m):
                                continue
                            if art in skus_connus:
                                mask_sku = st.session_state.poids_skus["SKU"].str.strip() == art
                                for a_cible in annees_cibles:
                                    st.session_state.poids_skus.loc[mask_sku, a_cible] = val_m
                                nb_maj += 1
                            else:
                                non_trouves.append(art)

                        st.success(
                            f"✅ **{nb_maj} article(s)** mis à jour sur **{cible_annees_upload}**."
                        )
                        if non_trouves:
                            st.warning(
                                f"⚠️ {len(non_trouves)} article(s) non reconnu(s) ignoré(s) : {', '.join(non_trouves[:10])}"
                            )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la lecture du fichier : {e}")

    st.markdown("**Édition manuelle des poids SKU (%) :**")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        seg_filtre_ps = st.selectbox(
            "1. Filtrer par Segment :",
            options=ORDRE_SEGMENTS,
            key="sel_seg_ps",
        )
    marques_dispo = (
        st.session_state.poids_skus[
            st.session_state.poids_skus["Segment"] == seg_filtre_ps
        ]["Marque"]
        .unique()
        .tolist()
    )
    with col_f2:
        marque_filtre_ps = st.selectbox(
            "2. Filtrer par Marque :",
            options=marques_dispo,
            key="sel_marque_ps",
        )

    df_ps_view = st.session_state.poids_skus[
        (st.session_state.poids_skus["Segment"] == seg_filtre_ps)
        & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)
    ].copy()

    col_cfg_ps = {
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "Marque": st.column_config.TextColumn("Marque", disabled=True),
        "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True),
    }
    for annee in ANNEES:
        col_cfg_ps[annee] = st.column_config.NumberColumn(
            annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1
        )

    df_ps_edited = st.data_editor(
        df_ps_view,
        column_config=col_cfg_ps,
        hide_index=True,
        use_container_width=True,
        key="editor_poids_skus",
    )

    for idx, row in df_ps_edited.iterrows():
        mask = (
            (st.session_state.poids_skus["Segment"] == row["Segment"])
            & (st.session_state.poids_skus["Marque"] == row["Marque"])
            & (st.session_state.poids_skus["SKU"] == row["SKU"])
        )
        for annee in ANNEES:
            st.session_state.poids_skus.loc[mask, annee] = row[annee]

    erreurs_ps = []
    sub_ps = st.session_state.poids_skus[
        (st.session_state.poids_skus["Segment"] == seg_filtre_ps)
        & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)
    ]
    for annee in ANNEES:
        somme_sku = sub_ps[annee].sum()
        poids_m = st.session_state.poids_marques.loc[
            (st.session_state.poids_marques["Segment"] == seg_filtre_ps)
            & (st.session_state.poids_marques["Marque"] == marque_filtre_ps),
            annee,
        ].iloc[0]
        if poids_m > 0 and not np.isclose(somme_sku, 100.0, atol=0.05):
            erreurs_ps.append(f"**{annee}** ({somme_sku:.2f} %)")

    if erreurs_ps:
        st.warning(
            f"⚠️ La somme des poids des articles de **{marque_filtre_ps}** doit faire 100 %. Écarts : {', '.join(erreurs_ps)}"
        )
    else:
        st.success(
            f"✅ Somme des poids des articles de **{marque_filtre_ps}** conforme (100 % sur les années actives)."
        )

# =====================================================
# CALCUL DES VOLUMES (2027 - 2031) AVEC LES POIDS ÉDITÉS
# =====================================================
df_detail = df_base[["Segment", "Marque", "SKU", "2026"]].copy()

pm_renamed = st.session_state.poids_marques.rename(
    columns={a: f"PM_{a}" for a in ANNEES}
)
ps_renamed = st.session_state.poids_skus.rename(
    columns={a: f"PS_{a}" for a in ANNEES}
)

df_detail = df_detail.merge(pm_renamed, on=["Segment", "Marque"], how="left")
df_detail = df_detail.merge(ps_renamed, on=["Segment", "Marque", "SKU"], how="left")

for annee in ANNEES:
    objectif = df_obj.loc[df_obj["Année"] == annee, "Volume"].iloc[0]

    mix_map = (
        st.session_state.mix.query("Segment != 'TOTAL'")
        .set_index("Segment")[annee]
        .to_dict()
    )

    volume_segment = {seg: (objectif * pct / 100.0) for seg, pct in mix_map.items()}

    df_detail[f"MARQUE_{annee}"] = df_detail["Segment"].map(volume_segment) * (
        df_detail[f"PM_{annee}"] / 100.0
    )
    df_detail[annee] = df_detail[f"MARQUE_{annee}"] * (
        df_detail[f"PS_{annee}"] / 100.0
    )

# =====================================================
# GRAPHIQUES D'EVOLUTION (VOLUMES & MIX % PAR AN)
# =====================================================
st.divider()
st.subheader("📊 Visualisation des Évolutions (2026–2031)")

df_chart_seg = df_detail.groupby("Segment", as_index=False)[ANNEES_ALL].sum()
df_chart_seg_melt = df_chart_seg.melt(
    id_vars="Segment", var_name="Année", value_name="Volume"
)

# Calcul du Mix réel (%) par Segment et par Année (y compris 2026)
totaux_annuels = df_chart_seg_melt.groupby("Année")["Volume"].transform("sum")
df_chart_seg_melt["Mix (%)"] = np.where(
    totaux_annuels > 0,
    (df_chart_seg_melt["Volume"] / totaux_annuels) * 100.0,
    0.0,
)

# Ligne 1 : Graphiques Volumes
col_g1, col_g2 = st.columns(2)

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
        title="Trajectoire de Croissance des Volumes par Segment",
    )
    fig_line.update_layout(yaxis_title="Volume", xaxis_title="Année")
    st.plotly_chart(fig_line, use_container_width=True)

# Ligne 2 : Graphiques Évolution du Mix (%) par an
col_m1, col_m2 = st.columns(2)

with col_m1:
    fig_mix_bar = px.bar(
        df_chart_seg_melt,
        x="Année",
        y="Mix (%)",
        color="Segment",
        title="Évolution du Mix Segment (%) par An (Base 100 %)",
        text=df_chart_seg_melt["Mix (%)"].apply(lambda x: f"{x:.1f}%"),
    )
    fig_mix_bar.update_traces(textposition="inside")
    fig_mix_bar.update_layout(
        yaxis_title="Part de Mix (%)",
        xaxis_title="Année",
        yaxis=dict(range=[0, 100]),
    )
    st.plotly_chart(fig_mix_bar, use_container_width=True)

with col_m2:
    fig_mix_line = px.line(
        df_chart_seg_melt,
        x="Année",
        y="Mix (%)",
        color="Segment",
        markers=True,
        title="Évolution Comparative des Parts de Mix (%) par Segment",
        text=df_chart_seg_melt["Mix (%)"].apply(lambda x: f"{x:.1f}%"),
    )
    fig_mix_line.update_traces(textposition="top center")
    fig_mix_line.update_layout(yaxis_title="Part de Mix (%)", xaxis_title="Année")
    st.plotly_chart(fig_mix_line, use_container_width=True)

# =====================================================
# RENDU HTML AVEC FUSION VERTICALE SUR SEGMENT ET MARQUE
# =====================================================
def fmt_val(val):
    if pd.isna(val) or val == 0:
        return "-"
    return f"{val:,.0f}".replace(",", " ")

def generer_html_fusionne(segments_cibles):
    df_sub = df_detail[df_detail["Segment"].isin(segments_cibles)]
    label_total = (
        "TOTAL ANNEE"
        if len(segments_cibles) == len(ORDRE_SEGMENTS)
        else "TOTAL SÉLECTION"
    )

    css = """
    <style>
    .sop-container {
        max-height: 900px;
        overflow-y: auto;
        border: 1px solid #d0d0d0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
    }
    table.sop-table {
        width: 100%;
        border-collapse: collapse;
        text-align: right;
    }
    table.sop-table thead th {
        position: sticky;
        top: 0;
        background-color: #262626;
        color: white;
        padding: 8px 10px;
        border: 1px solid #595959;
        z-index: 2;
        text-align: center;
    }
    table.sop-table td {
        padding: 5px 10px;
        border: 1px solid #d9d9d9;
    }
    .row-total td {
        background-color: #FFF2CC;
        color: #000000;
        font-weight: bold;
        font-size: 14px;
    }
    .cell-seg-side {
        background-color: #C00000;
        color: white;
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
        font-size: 15px;
        width: 110px;
    }
    .row-seg-top td {
        background-color: #C00000;
        color: white;
        font-weight: bold;
    }
    .cell-marque-side {
        background-color: #F8CBAD;
        color: #000000;
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
        width: 130px;
    }
    .row-marque-top td {
        background-color: #F8CBAD;
        color: #000000;
        font-weight: bold;
    }
    .cell-sku {
        background-color: #FFFFFF;
        color: #1a1a1a;
        text-align: left;
    }
    .cell-val {
        background-color: #FFFFFF;
        color: #1a1a1a;
    }
    </style>
    """

    html = [css, '<div class="sop-container"><table class="sop-table">']
    html.append("<thead><tr>")
    html.append('<th colspan="3">Segment / Marque / SKU</th>')
    for annee in ANNEES_ALL:
        html.append(f"<th>{annee}</th>")
    html.append("</tr></thead><tbody>")

    html.append('<tr class="row-total">')
    html.append(f'<td colspan="3" style="text-align:center;">{label_total}</td>')
    for annee in ANNEES_ALL:
        html.append(f"<td>{fmt_val(df_sub[annee].sum())}</td>")
    html.append("</tr>")

    for segment in ORDRE_SEGMENTS:
        if segment not in segments_cibles:
            continue
        seg_data = df_sub[df_sub["Segment"] == segment]
        if len(seg_data) == 0:
            continue

        marques = seg_data["Marque"].unique()
        total_rows_seg = 1 + sum(
            1 + len(seg_data[seg_data["Marque"] == m]) for m in marques
        )

        html.append('<tr class="row-seg-top">')
        html.append(f'<td rowspan="{total_rows_seg}" class="cell-seg-side">{segment}</td>')
        html.append(f'<td colspan="2" style="text-align:center;">{segment}</td>')
        for annee in ANNEES_ALL:
            html.append(f"<td>{fmt_val(seg_data[annee].sum())}</td>")
        html.append("</tr>")

        for marque in marques:
            marq_data = seg_data[seg_data["Marque"] == marque]
            total_rows_marque = 1 + len(marq_data)

            html.append('<tr class="row-marque-top">')
            html.append(f'<td rowspan="{total_rows_marque}" class="cell-marque-side">{marque}</td>')
            html.append('<td style="text-align:left;"></td>')
            for annee in ANNEES_ALL:
                html.append(f"<td>{fmt_val(marq_data[annee].sum())}</td>")
            html.append("</tr>")

            for _, row in marq_data.iterrows():
                html.append("<tr>")
                html.append(f'<td class="cell-sku">{row["SKU"]}</td>')
                for annee in ANNEES_ALL:
                    html.append(f'<td class="cell-val">{fmt_val(row[annee])}</td>')
                html.append("</tr>")

    html.append("</tbody></table></div>")
    return "".join(html)

# =====================================================
# AFFICHAGE DU TABLEAU FUSIONNÉ AVEC FILTRE SEGMENT
# =====================================================
st.divider()
st.subheader("4️⃣ Volumes Simulés Détaillés")

segments_selectionnes = st.multiselect(
    "🔍 Filtrer par Segment :",
    options=ORDRE_SEGMENTS,
    default=ORDRE_SEGMENTS,
    placeholder="Choisissez un ou plusieurs segments...",
)

if not segments_selectionnes:
    st.info("Veuillez sélectionner au moins un segment dans le filtre ci-dessus.")
else:
    st.markdown(generer_html_fusionne(segments_selectionnes), unsafe_allow_html=True)

# =====================================================
# EXPORT EXCEL COMPLET (AVEC FUSIONS & ONGLETS DE POIDS)
# =====================================================
st.divider()

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_obj.to_excel(writer, sheet_name="1_Objectifs", index=False)
    st.session_state.mix.to_excel(writer, sheet_name="2_Mix_Segment", index=False)
    st.session_state.poids_marques.to_excel(writer, sheet_name="3_Poids_Marques", index=False)
    st.session_state.poids_skus.to_excel(writer, sheet_name="4_Poids_SKU", index=False)

    ws = writer.book.create_sheet(title="5_Simulation_SKU")

    fill_header = PatternFill(start_color="262626", end_color="262626", fill_type="solid")
    fill_total = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    fill_seg = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    fill_marque = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid")

    font_header = Font(bold=True, color="FFFFFF")
    font_total = Font(bold=True, color="000000", size=11)
    font_seg = Font(bold=True, color="FFFFFF", size=11)
    font_marque = Font(bold=True, color="000000")
    font_sku = Font(color="000000")

    thin = Side(border_style="thin", color="BFBFBF")
    border_cell = Border(left=thin, right=thin, top=thin, bottom=thin)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # En-têtes
    ws.cell(row=1, column=1, value="Segment / Marque / SKU")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=3)
    for col_i in range(1, 4):
        c = ws.cell(row=1, column=col_i)
        c.fill = fill_header
        c.font = font_header
        c.alignment = align_center
        c.border = border_cell

    for idx_a, annee in enumerate(ANNEES_ALL, start=4):
        c = ws.cell(row=1, column=idx_a, value=annee)
        c.fill = fill_header
        c.font = font_header
        c.alignment = align_center
        c.border = border_cell

    # Ligne TOTAL ANNEE
    curr_row = 2
    ws.cell(row=curr_row, column=1, value="TOTAL ANNEE")
    ws.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=3)
    for col_i in range(1, 4):
        c = ws.cell(row=curr_row, column=col_i)
        c.fill = fill_total
        c.font = font_total
        c.alignment = align_center
        c.border = border_cell

    for idx_a, annee in enumerate(ANNEES_ALL, start=4):
        c = ws.cell(row=curr_row, column=idx_a, value=float(df_detail[annee].sum()))
        c.fill = fill_total
        c.font = font_total
        c.alignment = align_right
        c.number_format = "#,##0"
        c.border = border_cell

    curr_row += 1

    # Lignes hiérarchiques avec fusions verticales
    for segment in ORDRE_SEGMENTS:
        seg_data = df_detail[df_detail["Segment"] == segment]
        if len(seg_data) == 0:
            continue

        seg_start_row = curr_row

        ws.cell(row=curr_row, column=2, value=segment)
        ws.merge_cells(start_row=curr_row, start_column=2, end_row=curr_row, end_column=3)
        for col_i in range(2, 4):
            c = ws.cell(row=curr_row, column=col_i)
            c.fill = fill_seg
            c.font = font_seg
            c.alignment = align_center
            c.border = border_cell

        for idx_a, annee in enumerate(ANNEES_ALL, start=4):
            c = ws.cell(row=curr_row, column=idx_a, value=float(seg_data[annee].sum()))
            c.fill = fill_seg
            c.font = font_seg
            c.alignment = align_right
            c.number_format = "#,##0"
            c.border = border_cell

        curr_row += 1

        for marque in seg_data["Marque"].unique():
            marq_data = seg_data[seg_data["Marque"] == marque]
            marq_start_row = curr_row

            c_sku_empty = ws.cell(row=curr_row, column=3, value="")
            c_sku_empty.fill = fill_marque
            c_sku_empty.border = border_cell

            for idx_a, annee in enumerate(ANNEES_ALL, start=4):
                c = ws.cell(row=curr_row, column=idx_a, value=float(marq_data[annee].sum()))
                c.fill = fill_marque
                c.font = font_marque
                c.alignment = align_right
                c.number_format = "#,##0"
                c.border = border_cell

            curr_row += 1

            for _, row in marq_data.iterrows():
                c_sku = ws.cell(row=curr_row, column=3, value=row["SKU"])
                c_sku.font = font_sku
                c_sku.alignment = align_left
                c_sku.border = border_cell

                for idx_a, annee in enumerate(ANNEES_ALL, start=4):
                    val = float(row[annee])
                    c = ws.cell(row=curr_row, column=idx_a, value=val if val != 0 else None)
                    c.font = font_sku
                    c.alignment = align_right
                    c.number_format = "#,##0"
                    c.border = border_cell

                curr_row += 1

            marq_end_row = curr_row - 1
            ws.cell(row=marq_start_row, column=2, value=marque)
            if marq_end_row > marq_start_row:
                ws.merge_cells(
                    start_row=marq_start_row,
                    start_column=2,
                    end_row=marq_end_row,
                    end_column=2,
                )
            for r_i in range(marq_start_row, marq_end_row + 1):
                c = ws.cell(row=r_i, column=2)
                c.fill = fill_marque
                c.font = font_marque
                c.alignment = align_center
                c.border = border_cell

        seg_end_row = curr_row - 1
        ws.cell(row=seg_start_row, column=1, value=segment)
        if seg_end_row > seg_start_row:
            ws.merge_cells(
                start_row=seg_start_row,
                start_column=1,
                end_row=seg_end_row,
                end_column=1,
            )
        for r_i in range(seg_start_row, seg_end_row + 1):
            c = ws.cell(row=r_i, column=1)
            c.fill = fill_seg
            c.font = font_seg
            c.alignment = align_center
            c.border = border_cell

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 36
    for col_letter in ["D", "E", "F", "G", "H", "I"]:
        ws.column_dimensions[col_letter].width = 14

buffer.seek(0)

st.download_button(
    label="📥 Télécharger le fichier Excel complet (.xlsx)",
    data=buffer,
    file_name="Simulation_SOP_2026_2031.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary",
)
