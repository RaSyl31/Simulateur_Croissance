import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Simulateur S&OP",
    layout="wide"
)

st.title("📈 Simulateur S&OP")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]

# =====================================================
# DONNEES EXEMPLE 2026
# =====================================================

df_seg_2026 = pd.DataFrame({
    "Segment": [
        "Alcomix",
        "BG",
        "BIERES",
        "EAUX",
        "Energy"
    ],
    "2026": [
        37471,
        1081747,
        2071848,
        825388,
        42627
    ]
})

# =====================================================
# TABLEAU 1 - OBJECTIFS
# =====================================================

st.subheader("1️⃣ Objectifs Globaux")

if "objectifs" not in st.session_state:

    st.session_state.objectifs = pd.DataFrame({
        "Année": ANNEES,
        "Volume": [
            4600000,
            4900000,
            5250000,
            5600000,
            6000000
        ]
    })

df_obj = st.data_editor(
    st.session_state.objectifs,
    hide_index=True,
    use_container_width=True,
    key="objectifs_editor"
)

st.session_state.objectifs = df_obj

# =====================================================
# TABLEAU 2 - MIX SEGMENT
# =====================================================

st.subheader("2️⃣ Mix Segment (%)")

if "mix" not in st.session_state:

    st.session_state.mix = pd.DataFrame({
        "Segment": [
            "Alcomix",
            "BG",
            "BIERES",
            "EAUX",
            "Energy",
            "TOTAL"
        ],
        "2027": [2, 25, 55, 15, 3, 100],
        "2028": [2, 25, 55, 15, 3, 100],
        "2029": [2, 25, 55, 15, 3, 100],
        "2030": [2, 25, 55, 15, 3, 100],
        "2031": [2, 25, 55, 15, 3, 100]
    })

df_mix_affichage = st.session_state.mix.copy()

for annee in ANNEES:

    total = df_mix_affichage.loc[
        df_mix_affichage["Segment"] != "TOTAL",
        annee
    ].sum()

    df_mix_affichage.loc[
        df_mix_affichage["Segment"] == "TOTAL",
        annee
    ] = total

df_mix = st.data_editor(
    df_mix_affichage,

    column_config={

        "Segment": st.column_config.TextColumn(
            "Segment",
            disabled=True
        ),

        "2027": st.column_config.NumberColumn(
            "2027",
            format="%d %%"
        ),

        "2028": st.column_config.NumberColumn(
            "2028",
            format="%d %%"
        ),

        "2029": st.column_config.NumberColumn(
            "2029",
            format="%d %%"
        ),

        "2030": st.column_config.NumberColumn(
            "2030",
            format="%d %%"
        ),

        "2031": st.column_config.NumberColumn(
            "2031",
            format="%d %%"
        )

    },

    hide_index=True,
    use_container_width=True,
    key="mix_editor"
)

for annee in ANNEES:

    st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL",
        annee
    ] = df_mix.loc[
        df_mix["Segment"] != "TOTAL",
        annee
    ].values

for annee in ANNEES:

    st.session_state.mix.loc[
        st.session_state.mix["Segment"] == "TOTAL",
        annee
    ] = st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL",
        annee
    ].sum()

# =====================================================
# CALCUL SEGMENT
# =====================================================

df_segment = pd.DataFrame()

segments = (
    st.session_state.mix
    .query("Segment != 'TOTAL'")
    ["Segment"]
)

df_segment["Segment"] = segments

df_segment["2026"] = df_segment["Segment"].map(
    df_seg_2026.set_index("Segment")["2026"]
)

for annee in ANNEES:

    objectif = (
        df_obj
        .loc[
            df_obj["Année"] == annee,
            "Volume"
        ]
        .iloc[0]
    )

    mix = (
        st.session_state.mix
        .query("Segment != 'TOTAL'")
        [annee]
    )

    df_segment[annee] = objectif * mix / 100

ligne_total = {"Segment": "TOTAL"}

for col in ["2026"] + ANNEES:
    ligne_total[col] = df_segment[col].sum()

df_segment = pd.concat(
    [
        df_segment,
        pd.DataFrame([ligne_total])
    ],
    ignore_index=True
)

# =====================================================
# DONNEES MARQUES (EXEMPLE)
# =====================================================

df_marque = pd.DataFrame({
    "Segment": [
        "BG",
        "BG",
        "BIERES",
        "BIERES",
        "BIERES"
    ],

    "Marque": [
        "Caprice",
        "World Cola",
        "THB",
        "Gold",
        "Queen's"
    ],

    "2026": [
        600000,
        481747,
        1700000,
        240000,
        131848
    ]
})

# =====================================================
# DONNEES ARTICLES (EXEMPLE)
# =====================================================

df_article = pd.DataFrame({

    "Segment": [
        "BIERES",
        "BIERES",
        "BG"
    ],

    "Marque": [
        "THB",
        "THB",
        "Caprice"
    ],

    "Article": [
        "THB Pilsener 65 cl VER",
        "THB Pilsener 33 cl VER",
        "Caprice Orange 150 cl PET"
    ],

    "2026": [
        1200000,
        500000,
        150000
    ]
})

# =====================================================
# ONGLETS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Segment",
        "🏷️ Marque",
        "📦 Article"
    ]
)

# =====================================================
# ONGLET SEGMENT
# =====================================================

with tab1:

    st.subheader("Volume par Segment")

    st.dataframe(
        df_segment.style.format("{:,.0f}"),
        hide_index=True,
        use_container_width=True
    )

# =====================================================
# ONGLET MARQUE
# =====================================================

with tab2:

    st.subheader("Volume par Marque")

    st.dataframe(
        df_marque.style.format("{:,.0f}"),
        hide_index=True,
        use_container_width=True
    )

# =====================================================
# ONGLET ARTICLE
# =====================================================

with tab3:

    st.subheader("Volume par Article")

    st.dataframe(
        df_article.style.format("{:,.0f}"),
        hide_index=True,
        use_container_width=True
    )

# =====================================================
# EXPORT EXCEL
# =====================================================

with pd.ExcelWriter(
    "Simulation_SOP.xlsx"
) as writer:

    df_obj.to_excel(
        writer,
        sheet_name="Objectifs",
        index=False
    )

    st.session_state.mix.to_excel(
        writer,
        sheet_name="Mix Segment",
        index=False
    )

    df_segment.to_excel(
        writer,
        sheet_name="Segment",
        index=False
    )

    df_marque.to_excel(
        writer,
        sheet_name="Marque",
        index=False
    )

    df_article.to_excel(
        writer,
        sheet_name="Article",
        index=False
    )

with open(
    "Simulation_SOP.xlsx",
    "rb"
) as fichier:

    st.download_button(
        "📥 Télécharger Excel",
        data=fichier,
        file_name="Simulation_SOP.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
