import streamlit as st
import pandas as pd

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Simulateur S&OP",
    layout="wide"
)

st.title("📈 Simulateur S&OP THB")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]

# ======================================================
# DONNEES HISTORIQUES 2026
# Remplacer par votre base complète
# ======================================================

df_2026 = pd.DataFrame({
    "Segment": [
        "Alcomix",
        "BG",
        "BIERES",
        "EAUX",
        "Energy"
    ],
    "Volume_2026": [
        37471,
        1081747,
        2071848,
        825388,
        42627
    ]
})

TOTAL_2026 = df_2026["Volume_2026"].sum()

# ======================================================
# TABLEAU 1
# OBJECTIFS GLOBAUX
# ======================================================

st.subheader("1️⃣ Objectifs globaux")

if "obj" not in st.session_state:

    st.session_state.obj = pd.DataFrame({
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
    st.session_state.obj,
    hide_index=True,
    use_container_width=True,
    key="obj_editor"
)

st.session_state.obj = df_obj

# ======================================================
# TABLEAU 2
# MIX SEGMENTS
# ======================================================

st.subheader("2️⃣ Mix Segment (%)")

if "mix" not in st.session_state:

    st.session_state.mix = pd.DataFrame({
        "Segment": [
            "Alcomix",
            "BG",
            "BIERES",
            "EAUX",
            "Energy"
        ],
        "2027": [2, 25, 55, 15, 3],
        "2028": [2, 25, 55, 15, 3],
        "2029": [2, 25, 55, 15, 3],
        "2030": [2, 25, 55, 15, 3],
        "2031": [2, 25, 55, 15, 3],
    })

df_mix = st.data_editor(
    st.session_state.mix,
    hide_index=True,
    use_container_width=True,
    key="mix_editor"
)

st.session_state.mix = df_mix

# Contrôle des sommes

for annee in ANNEES:

    total_mix = df_mix[annee].sum()

    if round(total_mix, 2) == 100:
        st.success(f"{annee} : 100 %")
    else:
        st.warning(
            f"{annee} : {total_mix:.2f}% (doit être égal à 100%)"
        )

# ======================================================
# TABLEAU 3
# CALCUL VOLUMES SEGMENTS
# ======================================================

st.subheader("3️⃣ Volumes calculés")

df_result = pd.DataFrame()

df_result["Segment"] = df_mix["Segment"]

df_result["2026"] = df_result["Segment"].map(
    dict(
        zip(
            df_2026["Segment"],
            df_2026["Volume_2026"]
        )
    )
)

for annee in ANNEES:

    volume_total = (
        df_obj
        .loc[
            df_obj["Année"] == annee,
            "Volume"
        ]
        .iloc[0]
    )

    df_result[annee] = (
        df_mix[annee] / 100
    ) * volume_total

st.dataframe(
    df_result.style.format("{:,.0f}"),
    use_container_width=True
)

# ======================================================
# EVOLUTION
# ======================================================

st.subheader("📊 Evolution par segment")

df_graph = df_result.set_index("Segment")

st.line_chart(
    df_graph[ANNEES].T
)

# ======================================================
# EXPORT EXCEL
# ======================================================

excel_file = "Simulation_SOP.xlsx"

with pd.ExcelWriter(excel_file) as writer:

    df_obj.to_excel(
        writer,
        sheet_name="Objectifs",
        index=False
    )

    df_mix.to_excel(
        writer,
        sheet_name="Mix",
        index=False
    )

    df_result.to_excel(
        writer,
        sheet_name="Volumes",
        index=False
    )

with open(excel_file, "rb") as f:

    st.download_button(
        label="📥 Télécharger Excel",
        data=f,
        file_name="Simulation_SOP.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
