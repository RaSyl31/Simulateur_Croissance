import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Simulateur S&OP",
    layout="wide"
)

st.title("📈 Simulateur S&OP THB")

ANNEES = ["2027", "2028", "2029", "2030", "2031"]

# =====================================================
# TABLEAU 1 - OBJECTIFS GLOBAUX
# =====================================================

st.subheader("1️⃣ Objectifs Globaux")

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
    use_container_width=True
)

st.session_state.obj = df_obj

# =====================================================
# TABLEAU 2 - MIX SEGMENTS
# =====================================================

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

st.session_state.mix = df_mix

# =====================================================
# CONTROLE 100%
# =====================================================

st.markdown("### ✅ Contrôle des Mix")

for annee in ANNEES:

    total_mix = df_mix[annee].sum()

    if round(total_mix, 2) == 100:

        st.success(
            f"{annee} : {total_mix:.0f} %"
        )

    else:

        st.error(
            f"{annee} : {total_mix:.2f} % (doit être égal à 100 %)"
        )

# =====================================================
# TABLEAU 3 - RESULTATS
# =====================================================

st.subheader("3️⃣ Volumes calculés")

df_result = pd.DataFrame()

df_result["Segment"] = df_mix["Segment"]

for annee in ANNEES:

    volume_total = (
        df_obj
        .loc[df_obj["Année"] == annee, "Volume"]
        .iloc[0]
    )

    df_result[annee] = (
        volume_total *
        df_mix[annee] / 100
    )

st.dataframe(
    df_result.style.format({
        "2027": "{:,.0f}",
        "2028": "{:,.0f}",
        "2029": "{:,.0f}",
        "2030": "{:,.0f}",
        "2031": "{:,.0f}",
    }),
    hide_index=True,
    use_container_width=True
)

# =====================================================
# GRAPHIQUE
# =====================================================

st.subheader("📊 Evolution")

df_graph = (
    df_result
    .set_index("Segment")
    .T
)

st.line_chart(df_graph)

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

    df_mix.to_excel(
        writer,
        sheet_name="Mix",
        index=False
    )

    df_result.to_excel(
        writer,
        sheet_name="Résultats",
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
