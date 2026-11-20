import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Simulateur S&OP THB",
    layout="wide"
)

st.title("📈 Simulateur S&OP THB")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]

# =====================================================
# TABLEAU 1 - OBJECTIFS GLOBAUX
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
    column_config={
        "Année": st.column_config.TextColumn(
            "Année",
            disabled=True
        ),
        "Volume": st.column_config.NumberColumn(
            "Volume",
            format="%d"
        )
    },
    hide_index=True,
    use_container_width=True,
    key="editor_objectif"
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

# --------------------------------------
# Recalcul automatique du TOTAL
# --------------------------------------

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

# --------------------------------------
# Tableau modifiable
# --------------------------------------

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
        ),
    },

    hide_index=True,
    use_container_width=True,
    key="mix_editor"
)

# --------------------------------------
# Sauvegarde sans la ligne TOTAL
# --------------------------------------

for annee in ANNEES:

    st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL",
        annee
    ] = df_mix.loc[
        df_mix["Segment"] != "TOTAL",
        annee
    ].values

# --------------------------------------
# Recalcul TOTAL
# --------------------------------------

for annee in ANNEES:

    st.session_state.mix.loc[
        st.session_state.mix["Segment"] == "TOTAL",
        annee
    ] = st.session_state.mix.loc[
        st.session_state.mix["Segment"] != "TOTAL",
        annee
    ].sum()

# =====================================================
# TABLEAU 3 - RESULTATS
# =====================================================

st.subheader("3️⃣ Volumes Calculés")

df_result = pd.DataFrame()

segments = (
    st.session_state.mix
    .query("Segment != 'TOTAL'")
    ["Segment"]
    .tolist()
)

df_result["Segment"] = segments

for annee in ANNEES:

    volume_total = (
        df_obj.loc[
            df_obj["Année"] == annee,
            "Volume"
        ].iloc[0]
    )

    mix_segment = (
        st.session_state.mix
        .query("Segment != 'TOTAL'")
        [annee]
        .values
    )

    df_result[annee] = (
        volume_total *
        mix_segment / 100
    )

# --------------------------------------
# Ligne TOTAL
# --------------------------------------

ligne_total = {
    "Segment": "TOTAL"
}

for annee in ANNEES:

    ligne_total[annee] = df_result[annee].sum()

df_result = pd.concat(
    [
        df_result,
        pd.DataFrame([ligne_total])
    ],
    ignore_index=True
)

# --------------------------------------
# Affichage
# --------------------------------------

st.dataframe(
    df_result.style.format({
        "2027": "{:,.0f}",
        "2028": "{:,.0f}",
        "2029": "{:,.0f}",
        "2030": "{:,.0f}",
        "2031": "{:,.0f}"
    }),
    hide_index=True,
    use_container_width=True
)

# =====================================================
# GRAPHIQUE
# =====================================================

st.subheader("📊 Evolution par Segment")

graph_df = df_result.copy()

graph_df = graph_df[
    graph_df["Segment"] != "TOTAL"
]

graph_df = graph_df.set_index("Segment")

st.line_chart(
    graph_df[ANNEES].T
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
        sheet_name="Mix",
        index=False
    )

    df_result.to_excel(
        writer,
        sheet_name="Volumes",
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
