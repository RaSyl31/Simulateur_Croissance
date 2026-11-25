import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# =====================================================
# CONFIGURATION & EN-TÊTE + ONGLETS FIGÉS
# =====================================================
st.set_page_config(page_title="Simulateur S&OP & CA", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { background: transparent !important; z-index: 1005 !important; }
    #sop-fixed-header { position: fixed; top: 0; left: 0; right: 0; z-index: 1002; padding: 0.9rem 3rem 0.5rem 3rem; background-color: #ffffff !important; border-bottom: 1px solid rgba(128, 128, 128, 0.15); }
    #sop-fixed-header h1 { margin: 0 !important; padding: 0 !important; font-size: 1.65rem !important; font-weight: 700 !important; line-height: 1.2 !important; }
    </style>
    <div id="sop-fixed-header">
        <h1>📈 Simulateur S&amp;OP — Volumes &amp; Chiffre d'Affaires (2026–2031)</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

ANNEES = ["2027", "2028", "2029", "2030", "2031"]
ANNEES_ALL = ["2026"] + ANNEES
ORDRE_SEGMENTS = ["Alcomix", "BG", "BIERES", "EAUX", "Energy"]

COULEURS_SEGMENTS = {
    "Alcomix": "#C00000",
    "BG": "#1F4E78",
    "BIERES": "#D97706",
    "EAUX": "#0284C7",
    "Energy": "#15803D",
}

# =====================================================
# BASE DETAILLEE
# =====================================================
detail = [
    ["Alcomix", "Booster", "Booster Appel-Mix 50CL VER", 21855, 26734, 3250, 0.005],
    ["Alcomix", "Booster", "Booster Tornado 50CL VER VER", 15616, 19235, 3250, 0.005],
    ["Alcomix", "BOTA Fresh", "BOTA Fresh 50 cl VER", 1005, 0, 3225, 0.005],
    ["Alcomix", "Racines", "Racines 33 cl VER", 2220, 0, 2170, 0.0033],
    ["BG", "Caprice", "Caprice Ananas 100 cl VER", 4386, 4610, 2180, 0.01],
    ["BG", "Caprice", "Caprice Ananas 150 cl PET", 22050, 23158, 3650, 0.015],
    ["BG", "Caprice", "Caprice Ananas 30 cl VER", 4496, 4677, 875, 0.003],
    ["BG", "Caprice", "Caprice Bonbon Anglais 100 cl VER", 57580, 57945, 2180, 0.01],
    ["BG", "Caprice", "Caprice Bonbon Anglais 150 cl PET", 308042, 311525, 3650, 0.015],
    ["BG", "Caprice", "Caprice Bonbon Anglais 20L FUT", 79, 79, 54170, 0.2],
    ["BG", "Caprice", "Caprice Bonbon Anglais 30 cl VER", 41261, 41451, 875, 0.003],
    ["BG", "Caprice", "Caprice Bonbon Anglais 33 cl CAN", 4990, 5875, 1850, 0.0033],
    ["BG", "Caprice", "Caprice Bonbon Anglais 35 cl PET", 19424, 20120, 1080, 0.0035],
    ["BG", "Caprice", "Caprice Bonbon Anglais 50 cl PET", 137932, 143366, 1465, 0.005],
    ["BG", "Caprice", "Caprice Grenadine 100 cl VER", 11739, 12276, 2180, 0.01],
    ["BG", "Caprice", "Caprice Grenadine 150 cl PET", 34088, 35514, 3650, 0.015],
    ["BG", "Caprice", "Caprice Grenadine 30 cl VER", 4720, 4993, 875, 0.003],
    ["BG", "Caprice", "Caprice Grenadine 33 cl CAN", 2897, 3449, 1850, 0.0033],
    ["BG", "Caprice", "Caprice Grenadine 35 cl PET", 1886, 3344, 1080, 0.0035],
    ["BG", "Caprice", "Caprice Grenadine 50 cl PET", 11792, 13307, 1465, 0.005],
    ["BG", "Caprice", "Caprice Orange 100 cl VER", 33262, 34729, 2180, 0.01],
    ["BG", "Caprice", "Caprice Orange 150 cl PET", 161382, 178106, 3650, 0.015],
    ["BG", "Caprice", "Caprice Orange 20L FUT", 75, 76, 54170, 0.2],
    ["BG", "Caprice", "Caprice Orange 30 cl VER", 26172, 26994, 875, 0.003],
    ["BG", "Caprice", "Caprice Orange 33 cl CAN", 3875, 4631, 1850, 0.0033],
    ["BG", "Caprice", "Caprice Orange 35 cl PET", 5943, 9585, 1080, 0.0035],
    ["BG", "Caprice", "Caprice Orange 50 cl PET", 59297, 65206, 1465, 0.005],
    ["BG", "Caprice", "Caprice Pomme 100 cl VER", 958, 0, 2180, 0.01],
    ["BG", "Caprice", "Caprice Pomme 150 cl PET", 4128, 0, 3650, 0.015],
    ["BG", "Caprice", "Caprice Pomme 30 cl VER", 1595, 0, 875, 0.003],
    ["BG", "Caprice", "Caprice Pomme 50 cl PET", 0, 0, 0, 0.005],
    ["BG", "Tonic", "Tonic 100 cl VER", 7958, 8478, 2180, 0.01],
    ["BG", "Tonic", "Tonic 30 cl VER", 17921, 19004, 875, 0.003],
    ["BG", "World Cola", "World Cola 100cl VER", 4368, 4555, 2180, 0.01],
    ["BG", "World Cola", "World Cola 100cl WOCO VER", 24276, 25066, 2180, 0.01],
    ["BG", "World Cola", "World Cola 150cl PET", 100927, 101555, 3650, 0.015],
    ["BG", "World Cola", "World Cola 30cl VER", 1967, 2059, 875, 0.003],
    ["BG", "World Cola", "World Cola 30cl WOCO VER", 26387, 27082, 875, 0.003],
    ["BG", "World Cola", "World Cola 33 cl CAN", 2832, 3169, 1850, 0.0033],
    ["BG", "World Cola", "World Cola 35cl PET", 6866, 8792, 1080, 0.0035],
    ["BG", "World Cola", "World Cola 50cl PET", 54263, 53936, 1465, 0.005],
    ["BG", "World Cola", "World Cola 20L FUT", 281, 278, 54170, 0.2],
    ["BIERES", "Beaufort", "Beaufort 33 CL CAN", 13986, 14655, 3800, 0.0033],
    ["BIERES", "Beaufort", "Beaufort 33CL VER", 34851, 36111, 2900, 0.0033],
    ["BIERES", "FRESH", "FRESH 33 cl CAN", 3254, 3771, 2650, 0.0033],
    ["BIERES", "FRESH", "FRESH 33 cl EXPORT CAN", 25, 0, 2107, 0.0033],
    ["BIERES", "FRESH", "THB Fresh 33 cl VER", 1881, 2053, 1900, 0.0033],
    ["BIERES", "FRESH", "THB Fresh 65 cl VER", 35712, 38205, 3000, 0.0065],
    ["BIERES", "Gold", "Gold 8 50 cl CAN", 1159, 1245, 4500, 0.005],
    ["BIERES", "Gold", "Gold 8 50 cl VER", 8661, 9342, 3200, 0.005],
    ["BIERES", "Gold", "Gold Blanche 33cl VER", 24605, 26461, 2580, 0.0033],
    ["BIERES", "Gold", "Gold Blanche 50 cl CAN", 43538, 46334, 4500, 0.005],
    ["BIERES", "Gold", "Gold Blanche 50 cl VER", 92121, 101303, 3200, 0.005],
    ["BIERES", "Gold", "Gold Amigo 33cl VER", 1463, 0, 2575, 0.0033],
    ["BIERES", "Gold", "Gold Blonde 50 cl CAN", 8531, 9402, 4500, 0.005],
    ["BIERES", "Gold", "Gold Blonde 50 cl VER", 15872, 17066, 3200, 0.005],
    ["BIERES", "Gold", "Gold Blonde 65 cl VER", 58077, 60555, 3600, 0.0065],
    ["BIERES", "Gold", "Gold Blanche 20L FUT", 1464, 1287, 109170, 0.2],
    ["BIERES", "Queen", "Queen s 65 cl VER", 153975, 163506, 3000, 0.0065],
    ["BIERES", "THB", "THB Pilsener 33 cl VER", 96836, 102631, 1900, 0.0033],
    ["BIERES", "THB", "THB Pilsener 50 cl CAN", 60246, 63913, 3800, 0.005],
    ["BIERES", "THB", "THB Pilsener 65 cl VER", 1513573, 1668377, 3250, 0.0065],
    ["BIERES", "THB", "THB Pilsener 20L FUT", 2228, 2122, 100000, 0.2],
    ["BIERES", "THB", "THB Pilsener 30L FUT", 0, 662, 170000, 0.3],
    ["BIERES", "THB", "THB Speciale NOEL 33 cl VER", 736, 0, 1900, 0.0033],
    ["BIERES", "THB", "THB Pilsener 20L Export FUT", 450, 0, 56500, 0.2],
    ["BIERES", "THB", "THB Blanche 20L Export FUT", 47, 0, 64000, 0.2],
    ["BIERES", "THB", "THB Pilsener 30L Export FUT", 602, 0, 141670, 0.3],
    ["BIERES", "THB", "THB 8 20L Export FUT", 40, 0, 62000, 0.2],
    ["EAUX", "Cristal", "Cristal 100 cl VER", 1004, 1113, 2750, 0.01],
    ["EAUX", "Cristal", "Cristal 150 cl PET", 4516, 4634, 4265, 0.015],
    ["EAUX", "Cristal", "Cristal 30 cl VER", 689, 743, 1130, 0.003],
    ["EAUX", "Cristal", "Cristal 50 cl VER", 4206, 4439, 1600, 0.005],
    ["EAUX", "Cristalline", "Cristalline 100 cl PET", 272844, 285962, 1550, 0.01],
    ["EAUX", "Cristalline", "Cristalline 200 cl PET", 268234, 273125, 2680, 0.02],
    ["EAUX", "Eau vive", "Eau vive 150 cl PET", 210612, 211467, 2465, 0.015],
    ["EAUX", "Eau vive", "Eau vive 50 cl PET", 67919, 71556, 1235, 0.005],
    ["EAUX", "Eau vive", "Eau vive 50 cl VER", 364, 2000, 1600, 0.005],
    ["Energy", "FOSA", "FOSA 50 cl CAN", 3265, 15000, 3830, 0.005],
    ["Energy", "XXL", "XXL 30cl BOB VER", 19433, 21385, 1750, 0.003],
    ["Energy", "XXL", "XXL 30cl VER", 571, 764, 1750, 0.003],
    ["Energy", "XXL", "XXL 33 cl CAN", 3001, 4273, 3000, 0.0033],
    ["Energy", "XXL", "XXL 35cl PET", 16357, 29578, 2600, 0.0035],
]

df_base = pd.DataFrame(detail, columns=["Segment", "Marque", "SKU", "2026", "Base_2027", "Prix_2026_Fixe", "Contenance_hl"])

df_base["Vol_Segment_2027"] = df_base.groupby("Segment")["Base_2027"].transform("sum")
df_base["Vol_Marque_2027"] = df_base.groupby(["Segment", "Marque"])["Base_2027"].transform("sum")
df_base["Poids_Marque_Init"] = np.where(df_base["Vol_Segment_2027"] > 0, (df_base["Vol_Marque_2027"] / df_base["Vol_Segment_2027"]) * 100.0, 0.0)
df_base["Poids_SKU_Init"] = np.where(df_base["Vol_Marque_2027"] > 0, (df_base["Base_2027"] / df_base["Vol_Marque_2027"]) * 100.0, 0.0)

TOTAL_2027 = df_base["Base_2027"].sum()
mix_2027_calcul = (df_base.groupby("Segment")["Base_2027"].sum() / TOTAL_2027) * 100

# =====================================================
# DONNEES AGENCES ET DISPATCH
# =====================================================
AGENCES = ["01-Tanjombato", "03-Usine-Diego", "04-Tulear", "05-Fianarantsoa", "09-Tamatave", "11-Andranomahery"]
MOIS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

np.random.seed(42)
dispatch_data = []
for _, row in df_base.iterrows():
    if row["Base_2027"] == 0:
        continue
    poids_ag = np.random.dirichlet(np.ones(len(AGENCES)), size=1)[0]
    poids_mois = np.random.dirichlet(np.ones(len(MOIS)), size=1)[0]
    for i_ag, ag in enumerate(AGENCES):
        for i_m, m in enumerate(MOIS):
            dispatch_data.append({
                "Segment": row["Segment"], "Marque": row["Marque"], "Article": row["SKU"],
                "Agence": ag, "Mois": m, "Poids_Dispatch": poids_ag[i_ag] * poids_mois[i_m]
            })
df_dispatch_base = pd.DataFrame(dispatch_data)

# =====================================================
# INITIALISATION DES SESSION STATES
# =====================================================
if "objectifs" not in st.session_state:
    st.session_state.objectifs = pd.DataFrame({"Année": ANNEES, "Volume": [4600000, 4900000, 5250000, 5600000, 6000000]})
if "mix" not in st.session_state:
    st.session_state.mix = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy", "TOTAL"],
        "2027": [mix_2027_calcul.get(s, 0) for s in ["Alcomix", "BG", "BIERES", "EAUX", "Energy"]] + [100.00],
        "2028": [1.00, 27.37, 51.50, 18.59, 1.54, 100.00], "2029": [1.00, 27.80, 51.50, 18.00, 1.70, 100.00],
        "2030": [1.00, 27.90, 51.50, 17.75, 1.80, 99.95], "2031": [1.00, 28.00, 51.50, 17.50, 2.00, 100.00],
    })
if "poids_marques" not in st.session_state:
    df_pm_init = df_base[["Segment", "Marque", "Poids_Marque_Init"]].drop_duplicates().reset_index(drop=True)
    for annee in ANNEES:
        df_pm_init[annee] = df_pm_init["Poids_Marque_Init"]
    st.session_state.poids_marques = df_pm_init.drop(columns=["Poids_Marque_Init"])
if "poids_skus" not in st.session_state:
    df_ps_init = df_base[["Segment", "Marque", "SKU", "Poids_SKU_Init"]].copy()
    for annee in ANNEES:
        df_ps_init[annee] = df_ps_init["Poids_SKU_Init"]
    st.session_state.poids_skus = df_ps_init.drop(columns=["Poids_SKU_Init"])
colonnes_prix_attendues = ["Segment", "Marque", "SKU", "Contenance_hl"] + ANNEES_ALL
if ("prix_skus" not in st.session_state or not all(col in st.session_state.prix_skus.columns for col in colonnes_prix_attendues)):
    df_prix_init = df_base[["Segment", "Marque", "SKU", "Contenance_hl"]].copy()
    for annee in ANNEES_ALL:
        df_prix_init[annee] = df_base["Prix_2026_Fixe"].astype(float)
    st.session_state.prix_skus = df_prix_init

# =====================================================
# FONCTIONS COMMUNES
# =====================================================
def fmt_val(val):
    if pd.isna(val) or val == 0:
        return "-"
    return f"{val:,.0f}".replace(",", " ")

def styler_graphe(fig, titre, yaxis_titre):
    fig.update_layout(
        template="plotly_white",
        title={"text": titre, "font": {"size": 15, "family": "Segoe UI, Tahoma, sans-serif"}},
        yaxis_title=yaxis_titre,
        legend_title_text="Segment",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Segoe UI, Tahoma, sans-serif", size=12),
    )
    return fig

def generer_html_fusionne(df_source, cols_annees, segments_cibles, afficher_evo=False):
    df_sub = df_source[df_source["Segment"].isin(segments_cibles)]
    label_total = "TOTAL ANNEE" if len(segments_cibles) == len(ORDRE_SEGMENTS) else "TOTAL SÉLECTION"
    css = """<style>.sop-container{max-height:900px;overflow-y:auto;border:1px solid #d0d0d0;font-family:'Segoe UI',Tahoma,sans-serif;font-size:13px}table.sop-table{width:100%;border-collapse:collapse;text-align:right}table.sop-table thead th{position:sticky;top:0;background-color:#262626;color:white;padding:8px;border:1px solid #595959;z-index:2;text-align:center}table.sop-table td{padding:5px 10px;border:1px solid #d9d9d9}.row-total td{background-color:#FFF2CC;font-weight:bold;font-size:14px}.row-eco-total td{background-color:#FFF2CC;font-weight:bold;font-size:13px;font-style:italic}.cell-seg-side{background-color:#C00000;color:white;font-weight:bold;text-align:center;vertical-align:middle;font-size:15px;width:110px}.row-seg-top td{background-color:#C00000;color:white;font-weight:bold}.cell-marque-side{background-color:#F8CBAD;font-weight:bold;text-align:center;vertical-align:middle;width:130px}.row-marque-top td{background-color:#F8CBAD;font-weight:bold}.cell-sku{background-color:#FFFFFF;text-align:left}.cell-val{background-color:#FFFFFF}</style>"""
    html = [css, '<div class="sop-container"><table class="sop-table"><thead><tr><th colspan="3">Segment / Marque / SKU</th>']
    for annee in cols_annees:
        html.append(f"<th>{annee}</th>")
    html.append("</tr></thead><tbody>")
    html.append(f'<tr class="row-total"><td colspan="3" style="text-align:center;">{label_total}</td>')
    for annee in cols_annees:
        html.append(f"<td>{fmt_val(df_sub[annee].sum())}</td>")
    html.append("</tr>")
    for segment in ORDRE_SEGMENTS:
        if segment not in segments_cibles:
            continue
        seg_data = df_sub[df_sub["Segment"] == segment]
        if len(seg_data) == 0:
            continue
        marques = seg_data["Marque"].unique()
        total_rows_seg = 1 + sum(1 + len(seg_data[seg_data["Marque"] == m]) for m in marques)
        html.append(f'<tr class="row-seg-top"><td rowspan="{total_rows_seg}" class="cell-seg-side">{segment}</td><td colspan="2" style="text-align:center;">{segment}</td>')
        for annee in cols_annees:
            html.append(f"<td>{fmt_val(seg_data[annee].sum())}</td>")
        html.append("</tr>")
        for marque in marques:
            marq_data = seg_data[seg_data["Marque"] == marque]
            html.append(f'<tr class="row-marque-top"><td rowspan="{1 + len(marq_data)}" class="cell-marque-side">{marque}</td><td style="text-align:left;"></td>')
            for annee in cols_annees:
                html.append(f"<td>{fmt_val(marq_data[annee].sum())}</td>")
            html.append("</tr>")
            for _, row in marq_data.iterrows():
                html.append("<tr>")
                html.append(f'<td class="cell-sku">{row["SKU"]}</td>')
                for annee in cols_annees:
                    html.append(f'<td class="cell-val">{fmt_val(row[annee])}</td>')
                html.append("</tr>")
    if afficher_evo:
        html.append('<tr class="row-eco-total"><td colspan="3" style="text-align:center;">Évolution vs N-1 (%)</td>')
        for i, annee in enumerate(cols_annees):
            if i == 0:
                html.append("<td>-</td>")
            else:
                v_curr, v_prev = df_sub[annee].sum(), df_sub[cols_annees[i - 1]].sum()
                taux = ((v_curr - v_prev) / v_prev * 100.0) if v_prev > 0 else 0
                html.append(f"<td>{'+' if taux >= 0 else ''}{taux:.1f}%</td>")
        html.append("</tr>")
    html.append("</tbody></table></div>")
    return "".join(html)

def generer_html_agences_par_mois(df_source, agences_cibles):
    """Génère un tableau dépliable qui montre les mois pour une ou plusieurs agences"""
    df_grp = df_source[df_source["Agence"].isin(agences_cibles)].groupby(["Segment", "Marque", "Article", "Agence", "Mois"])["Volume"].sum().reset_index()

    css = """<style>.ag-container{font-family:'Segoe UI',Tahoma,sans-serif;font-size:13px}details{margin-bottom:5px;border:1px solid #d0d0d0;border-radius:4px}summary{padding:8px 12px;background-color:#f8f9fa;cursor:pointer;font-weight:bold;color:#333;border-bottom:1px solid #d0d0d0}summary:hover{background-color:#e9ecef}summary::-webkit-details-marker{display:none}summary::before{content:'▶';display:inline-block;margin-right:10px;font-size:10px;color:#666;transition:transform 0.2s}details[open]>summary::before{transform:rotate(90deg)}.ag-table{width:100%;border-collapse:collapse;text-align:right;margin-top:5px}.ag-table th{background-color:#f1f3f5;padding:6px 10px;border-bottom:2px solid #dee2e6;text-align:center;font-weight:600}.ag-table td{padding:5px 10px;border-bottom:1px solid #eee}.ag-table tr:hover{background-color:#f8f9fa}.ag-row-total td{font-weight:bold;background-color:#fff3cd}</style>"""
    html = [css, '<div class="ag-container">']

    for segment in ORDRE_SEGMENTS:
        df_seg = df_grp[df_grp["Segment"] == segment]
        if df_seg.empty:
            continue

        seg_total = df_seg["Volume"].sum()
        html.append(f'<details><summary>{segment} (Total : {seg_total:,.0f} hl)</summary>')

        html.append('<table class="ag-table"><thead><tr><th style="text-align:left;">Marque / Article / Agence</th>')
        for m in MOIS:
            html.append(f"<th>{m}</th>")
        html.append("<th>Total</th></tr></thead><tbody>")

        html.append('<tr class="ag-row-total"><td style="text-align:left;">Total Segment</td>')
        for m in MOIS:
            val_mois = df_seg[df_seg["Mois"] == m]["Volume"].sum()
            html.append(f"<td>{fmt_val(val_mois)}</td>")
        html.append(f"<td>{fmt_val(seg_total)}</td></tr>")

        for marque in df_seg["Marque"].unique():
            df_marq = df_seg[df_seg["Marque"] == marque]
            marq_total = df_marq["Volume"].sum()

            html.append(f'<tr><td colspan="{len(MOIS)+2}" style="padding:0;"><details><summary style="background:none;border:none;padding:5px 10px;font-weight:bold;color:#555;">{marque}</summary>')
            html.append('<table class="ag-table" style="margin:0;"><tbody>')

            html.append('<tr class="ag-row-total"><td style="text-align:left;">Total Marque</td>')
            for m in MOIS:
                val_mois = df_marq[df_marq["Mois"] == m]["Volume"].sum()
                html.append(f"<td>{fmt_val(val_mois)}</td>")
            html.append(f"<td>{fmt_val(marq_total)}</td></tr>")

            for article in df_marq["Article"].unique():
                df_art = df_marq[df_marq["Article"] == article]
                for agence in df_art["Agence"].unique():
                    df_ag = df_art[df_art["Agence"] == agence]
                    art_ag_total = df_ag["Volume"].sum()
                    html.append(f'<tr><td style="text-align:left;">{article} - {agence}</td>')
                    for m in MOIS:
                        val_m = df_ag[df_ag["Mois"] == m]["Volume"].sum()
                        html.append(f"<td>{fmt_val(val_m)}</td>")
                    html.append(f"<td>{fmt_val(art_ag_total)}</td></tr>")

            html.append("</tbody></table></details></td></tr>")
        html.append("</tbody></table></details>")
    html.append("</div>")
    return "".join(html)

# =====================================================
# NAVIGATION PRINCIPALE
# =====================================================
onglet_vol, onglet_ca, onglet_agences, onglet_dispatch = st.tabs([
    "📦 Simulation Volumes (2026–2031)",
    "💰 Chiffre d'Affaires (2026–2031)",
    "📍 Volume par Agence (Vue Globale)",
    "🚚 Dispatch Agence & Mois (Détail)"
])

# #####################################################
# ONGLET 1 : SIMULATION DES VOLUMES
# #####################################################
with onglet_vol:
    st.subheader("1️⃣ Objectifs Globaux (Volumes en hl)")
    df_obj = st.data_editor(st.session_state.objectifs, column_config={"Année": st.column_config.TextColumn("Année", disabled=True), "Volume": st.column_config.NumberColumn("Volume Objectif (hl)", format="%d", min_value=0, step=10000)}, hide_index=True, use_container_width=True, key="editor_objectif")
    st.session_state.objectifs = df_obj

    st.subheader("2️⃣ Mix Segment (%)")
    for annee in ANNEES:
        st.session_state.mix.loc[st.session_state.mix["Segment"] == "TOTAL", annee] = st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee].sum()
    col_config_mix = {"Segment": st.column_config.TextColumn("Segment", disabled=True)}
    for annee in ANNEES:
        col_config_mix[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.05)
    df_mix = st.data_editor(st.session_state.mix, column_config=col_config_mix, hide_index=True, use_container_width=True, key="mix_editor")
    erreurs_mix = []
    for annee in ANNEES:
        st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee] = df_mix.loc[df_mix["Segment"] != "TOTAL", annee].values
        total_annee = st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee].sum()
        st.session_state.mix.loc[st.session_state.mix["Segment"] == "TOTAL", annee] = total_annee
        if not np.isclose(total_annee, 100.0, atol=0.06):
            erreurs_mix.append(f"**{annee}** ({total_annee:.2f} %)")
    if erreurs_mix:
        st.error(f"⚠️ **Attention : Le total du Mix Segment doit être égal à 100 %.** Années en erreur : {', '.join(erreurs_mix)}.")
    else:
        st.success("✅ **Validation OK :** Tous les totaux du Mix Segment sont conformes.")

    st.divider()
    st.subheader("3️⃣ Paramétrage des Poids : Marques & Articles (%)")
    if st.button("🔄 Réinitialiser tous les poids (Base 2027)"):
        del st.session_state["poids_marques"]
        del st.session_state["poids_skus"]
        st.rerun()

    tab_pm, tab_ps = st.tabs(["🏷️ Poids des Marques", "📦 Poids des Articles (SKU)"])
    with tab_pm:
        seg_filtre_pm = st.selectbox("Sélectionner un Segment à modifier :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="sel_seg_pm")
        df_pm_view = st.session_state.poids_marques.copy()
        if seg_filtre_pm != "Tous les segments":
            df_pm_view = df_pm_view[df_pm_view["Segment"] == seg_filtre_pm]
        col_cfg_pm = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True)}
        for annee in ANNEES:
            col_cfg_pm[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1)
        df_pm_edited = st.data_editor(df_pm_view, column_config=col_cfg_pm, hide_index=True, use_container_width=True, key="editor_poids_marques")
        for idx, row in df_pm_edited.iterrows():
            mask = (st.session_state.poids_marques["Segment"] == row["Segment"]) & (st.session_state.poids_marques["Marque"] == row["Marque"])
            for annee in ANNEES:
                st.session_state.poids_marques.loc[mask, annee] = row[annee]
        erreurs_pm = []
        segs_a_verifier = ORDRE_SEGMENTS if seg_filtre_pm == "Tous les segments" else [seg_filtre_pm]
        for seg in segs_a_verifier:
            sub_pm = st.session_state.poids_marques[st.session_state.poids_marques["Segment"] == seg]
            for annee in ANNEES:
                somme = sub_pm[annee].sum()
                if not np.isclose(somme, 100.0, atol=0.05):
                    erreurs_pm.append(f"**{seg} ({annee})** : {somme:.2f} %")
        if erreurs_pm:
            st.warning(f"⚠️ Écarts détectés : {', '.join(erreurs_pm)}")
        else:
            st.success("✅ Somme des poids des marques = 100 % pour chaque segment.")

    with tab_ps:
        with st.expander("📤 Importer les poids SKU via fichier (Excel / CSV) — Colonnes : Article | mix", expanded=False):
            col_up1, col_up2, col_up3 = st.columns([2, 1, 1])
            with col_up1:
                uploaded_sku_file = st.file_uploader("Charger un fichier (.xlsx ou .csv) avec 2 colonnes : 'Article' et 'mix'", type=["xlsx", "xls", "csv"], key="upload_sku_mix")
            with col_up2:
                cible_annees_upload = st.selectbox("Appliquer sur :", options=["Toutes les années (2027–2031)"] + ANNEES, key="upload_target_years")
            with col_up3:
                df_template = st.session_state.poids_skus[["SKU", "2027"]].rename(columns={"SKU": "Article", "2027": "mix"})
                buf_tpl = io.BytesIO()
                with pd.ExcelWriter(buf_tpl, engine="openpyxl") as w_tpl:
                    df_template.to_excel(w_tpl, sheet_name="Poids_SKU", index=False)
                buf_tpl.seek(0)
                st.write("")
                st.download_button("📄 Modèle Excel (.xlsx)", data=buf_tpl, file_name="Modele_Poids_SKU.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
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
                        cols_norm = {str(c).strip().lower(): c for c in df_up.columns}
                        if "article" not in cols_norm or "mix" not in cols_norm:
                            st.error(f"❌ Colonnes attendues : **Article** et **mix**. Colonnes trouvées : {list(df_up.columns)}")
                        else:
                            col_art = cols_norm["article"]
                            col_mix = cols_norm["mix"]
                            df_up_clean = df_up[[col_art, col_mix]].dropna(subset=[col_art]).copy()
                            df_up_clean["Article_clean"] = df_up_clean[col_art].astype(str).str.strip()
                            def parse_mix_val(v):
                                if pd.isna(v):
                                    return np.nan
                                if isinstance(v, str):
                                    return float(v.replace("%", "").replace(",", ".").strip())
                                return float(v)
                            df_up_clean["mix_num"] = df_up_clean[col_mix].apply(parse_mix_val)
                            if df_up_clean["mix_num"].max() <= 1.0 and df_up_clean["mix_num"].sum() > 0:
                                df_up_clean["mix_num"] = df_up_clean["mix_num"] * 100.0
                            annees_cibles = ANNEES if cible_annees_upload == "Toutes les années (2027–2031)" else [cible_annees_upload]
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
                            st.success(f"✅ **{nb_maj} article(s)** mis à jour sur **{cible_annees_upload}**.")
                            if non_trouves:
                                st.warning(f"⚠️ {len(non_trouves)} article(s) non reconnu(s) ignoré(s) : {', '.join(non_trouves[:10])}")
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")

        st.markdown("**Édition manuelle des poids SKU (%) :**")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            seg_filtre_ps = st.selectbox("1. Filtrer par Segment :", options=ORDRE_SEGMENTS, key="sel_seg_ps")
        marques_dispo = st.session_state.poids_skus[st.session_state.poids_skus["Segment"] == seg_filtre_ps]["Marque"].unique().tolist()
        with col_f2:
            marque_filtre_ps = st.selectbox("2. Filtrer par Marque :", options=marques_dispo, key="sel_marque_ps")
        df_ps_view = st.session_state.poids_skus[(st.session_state.poids_skus["Segment"] == seg_filtre_ps) & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)].copy()
        col_cfg_ps = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True), "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True)}
        for annee in ANNEES:
            col_cfg_ps[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1)
        df_ps_edited = st.data_editor(df_ps_view, column_config=col_cfg_ps, hide_index=True, use_container_width=True, key="editor_poids_skus")
        for idx, row in df_ps_edited.iterrows():
            mask = (st.session_state.poids_skus["Segment"] == row["Segment"]) & (st.session_state.poids_skus["Marque"] == row["Marque"]) & (st.session_state.poids_skus["SKU"] == row["SKU"])
            for annee in ANNEES:
                st.session_state.poids_skus.loc[mask, annee] = row[annee]
        erreurs_ps = []
        sub_ps = st.session_state.poids_skus[(st.session_state.poids_skus["Segment"] == seg_filtre_ps) & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)]
        for annee in ANNEES:
            somme_sku = sub_ps[annee].sum()
            poids_m = st.session_state.poids_marques.loc[(st.session_state.poids_marques["Segment"] == seg_filtre_ps) & (st.session_state.poids_marques["Marque"] == marque_filtre_ps), annee].iloc[0]
            if poids_m > 0 and not np.isclose(somme_sku, 100.0, atol=0.05):
                erreurs_ps.append(f"**{annee}** ({somme_sku:.2f} %)")
        if erreurs_ps:
            st.warning(f"⚠️ Écarts : {', '.join(erreurs_ps)}")
        else:
            st.success(f"✅ Somme des poids des articles de **{marque_filtre_ps}** conforme.")

    df_detail = df_base[["Segment", "Marque", "SKU", "2026", "Contenance_hl"]].copy()
    pm_renamed = st.session_state.poids_marques.rename(columns={a: f"PM_{a}" for a in ANNEES})
    ps_renamed = st.session_state.poids_skus.rename(columns={a: f"PS_{a}" for a in ANNEES})
    df_detail = df_detail.merge(pm_renamed, on=["Segment", "Marque"], how="left").merge(ps_renamed, on=["Segment", "Marque", "SKU"], how="left")
    for annee in ANNEES:
        objectif = df_obj.loc[df_obj["Année"] == annee, "Volume"].iloc[0]
        mix_map = st.session_state.mix.query("Segment != 'TOTAL'").set_index("Segment")[annee].to_dict()
        volume_segment = {seg: (objectif * pct / 100.0) for seg, pct in mix_map.items()}
        df_detail[f"MARQUE_{annee}"] = df_detail["Segment"].map(volume_segment) * (df_detail[f"PM_{annee}"] / 100.0)
        df_detail[annee] = df_detail[f"MARQUE_{annee}"] * (df_detail[f"PS_{annee}"] / 100.0)

    st.divider()
    st.subheader("4️⃣ Volumes Simulés Détaillés (hl)")
    segments_selectionnes_vol = st.multiselect("🔍 Filtrer par Segment (Volumes) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_vol_seg")
    if not segments_selectionnes_vol:
        st.info("Veuillez sélectionner au moins un segment.")
    else:
        st.markdown(generer_html_fusionne(df_detail, ANNEES_ALL, segments_selectionnes_vol, afficher_evo=False), unsafe_allow_html=True)

        st.divider()
        st.subheader("5️⃣ Graphiques Volumes & Mix (4 Graphes — 2026–2031)")

        df_vol_seg = (
            df_detail[df_detail["Segment"].isin(segments_selectionnes_vol)]
            .groupby("Segment", as_index=False)[ANNEES_ALL]
            .sum()
            .melt(id_vars="Segment", value_vars=ANNEES_ALL, var_name="Année", value_name="Volume")
        )
        totaux_vol_annee = df_vol_seg.groupby("Année")["Volume"].transform("sum")
        df_vol_seg["Mix_Pct"] = np.where(totaux_vol_annee > 0, (df_vol_seg["Volume"] / totaux_vol_annee) * 100.0, 0.0)

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            fig_v1 = px.line(
                df_vol_seg,
                x="Année",
                y="Volume",
                color="Segment",
                markers=True,
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v1, "1. Évolution des Volumes par Segment", "Volume (hl)"), use_container_width=True)

        with col_v2:
            fig_v2 = px.bar(
                df_vol_seg,
                x="Année",
                y="Volume",
                color="Segment",
                barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v2, "2. Graphe Empilé des Volumes par Segment", "Volume (hl)"), use_container_width=True)

        col_v3, col_v4 = st.columns(2)
        with col_v3:
            fig_v3 = px.line(
                df_vol_seg,
                x="Année",
                y="Mix_Pct",
                color="Segment",
                markers=True,
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v3, "3. Évolution du Mix Volume (%) par Segment", "Mix (%)"), use_container_width=True)

        with col_v4:
            fig_v4 = px.bar(
                df_vol_seg,
                x="Année",
                y="Mix_Pct",
                color="Segment",
                barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v4, "4. Graphe Empilé du Mix Volume (%)", "Part du volume (%)"), use_container_width=True)


# #####################################################
# ONGLET 2 : CALCUL CHIFFRE D'AFFAIRES (CA EN AR)
# #####################################################
with onglet_ca:
    st.subheader("1️⃣ Gestion des Prix Unitaires (2026 fixé — Upload & Édition 2027 → 2031)")
    st.caption("Formule appliquée : **CA (Ar) = (Volume en hl / Contenance unitaire en hl) × Prix Unitaire (Ar)**")

    with st.expander("📤 Importer les Prix via fichier (Excel / CSV) — Période 2027 → 2031 uniquement", expanded=True):
        st.markdown("""
            **Le prix 2026 est déjà fixé.** L'import met à jour uniquement les années **2027 à 2031** :
            * **Format 2 colonnes** : `Article` | `Prix` → applique le prix à l'année sélectionnée (`2027` à `2031`) ou à toutes les années `2027 → 2031`.
            * **Format multi-années** : `Article` | `2027` | `2028` | `2029` | `2030` | `2031` → met à jour directement chaque colonne d'année correspondante.
        """)
        col_up_p1, col_up_p2, col_up_p3 = st.columns([2, 1, 1])
        with col_up_p1:
            uploaded_prix_file = st.file_uploader("Charger le fichier des Prix 2027–2031 (.xlsx ou .csv)", type=["xlsx", "xls", "csv"], key="upload_prix_file")
        with col_up_p2:
            cible_annees_prix = st.selectbox("Si fichier 2 colonnes, appliquer sur :", options=["Toutes les années (2027–2031)"] + ANNEES, key="upload_prix_target")
        with col_up_p3:
            df_tpl_prix = st.session_state.prix_skus[["SKU"] + ANNEES].rename(columns={"SKU": "Article"})
            buf_tpl_p = io.BytesIO()
            with pd.ExcelWriter(buf_tpl_p, engine="openpyxl") as w_p:
                df_tpl_prix.to_excel(w_p, sheet_name="Modele_Prix_2027_2031", index=False)
            buf_tpl_p.seek(0)
            st.write("")
            st.download_button("📄 Modèle Prix 2027–2031 (.xlsx)", data=buf_tpl_p, file_name="Modele_Prix_SKU_2027_2031.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_tpl_prix")

        if uploaded_prix_file is not None:
            if st.button("✅ Appliquer les Prix importés (2027–2031)", type="primary", key="btn_apply_prix"):
                try:
                    if uploaded_prix_file.name.endswith(".csv"):
                        try:
                            df_p_up = pd.read_csv(uploaded_prix_file, sep=None, engine="python")
                        except Exception:
                            uploaded_prix_file.seek(0)
                            df_p_up = pd.read_csv(uploaded_prix_file, sep=";")
                    else:
                        df_p_up = pd.read_excel(uploaded_prix_file)
                    cols_norm_p = {str(c).strip().lower(): c for c in df_p_up.columns}
                    col_art_key = next((k for k in ["article", "sku", "produit"] if k in cols_norm_p), None)
                    if col_art_key is None:
                        st.error(f"❌ Colonne **Article** (ou **SKU**) introuvable. Colonnes détectées : {list(df_p_up.columns)}")
                    else:
                        col_art_p = cols_norm_p[col_art_key]
                        df_p_up = df_p_up.dropna(subset=[col_art_p]).copy()
                        df_p_up["Article_clean"] = df_p_up[col_art_p].astype(str).str.strip()
                        def parse_prix_val(v):
                            if pd.isna(v):
                                return np.nan
                            if isinstance(v, str):
                                s = (v.replace("Ar", "").replace("MGA", "").replace(" ", "").replace("\u202f", "").replace(",", ".").strip())
                                return float(s) if s != "" else np.nan
                            return float(v)
                        annees_dans_fichier = [a for a in ANNEES if a in cols_norm_p]
                        skus_connus_p = set(st.session_state.prix_skus["SKU"].str.strip())
                        nb_maj_p = 0
                        non_trouves_p = []
                        if annees_dans_fichier:
                            for _, r_p in df_p_up.iterrows():
                                art = r_p["Article_clean"]
                                if art in skus_connus_p:
                                    mask_s = st.session_state.prix_skus["SKU"].str.strip() == art
                                    for a_f in annees_dans_fichier:
                                        val_px = parse_prix_val(r_p[cols_norm_p[a_f]])
                                        if not pd.isna(val_px):
                                            st.session_state.prix_skus.loc[mask_s, a_f] = val_px
                                    nb_maj_p += 1
                                else:
                                    non_trouves_p.append(art)
                            st.success(f"✅ **{nb_maj_p} article(s)** mis à jour sur : {', '.join(annees_dans_fichier)} (2026 conservé).")
                        else:
                            col_val_key = next((k for k in ["prix", "tarif", "pu", "price", "mix", "valeur"] if k in cols_norm_p), None)
                            if col_val_key is not None:
                                col_val_p = cols_norm_p[col_val_key]
                            elif len(df_p_up.columns) >= 2:
                                col_val_p = [c for c in df_p_up.columns if c != col_art_p][0]
                            else:
                                st.error("❌ Aucune colonne de prix trouvée.")
                                col_val_p = None
                            if col_val_p is not None:
                                annees_cibles_p = ANNEES if cible_annees_prix == "Toutes les années (2027–2031)" else [cible_annees_prix]
                                for _, r_p in df_p_up.iterrows():
                                    art = r_p["Article_clean"]
                                    val_px = parse_prix_val(r_p[col_val_p])
                                    if pd.isna(val_px):
                                        continue
                                    if art in skus_connus_p:
                                        mask_s = st.session_state.prix_skus["SKU"].str.strip() == art
                                        for a_c in annees_cibles_p:
                                            st.session_state.prix_skus.loc[mask_s, a_c] = val_px
                                        nb_maj_p += 1
                                    else:
                                        non_trouves_p.append(art)
                                st.success(f"✅ **{nb_maj_p} article(s)** mis à jour sur **{cible_annees_prix}**.")
                        if non_trouves_p:
                            st.warning(f"⚠️ {len(non_trouves_p)} article(s) non reconnu(s) : {', '.join(non_trouves_p[:10])}")
                except Exception as e:
                    st.error(f"❌ Erreur de lecture : {e}")

    seg_filtre_prix = st.selectbox("🔍 Filtrer la grille des Prix par Segment :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="sel_seg_prix")
    df_prix_view = st.session_state.prix_skus.copy()
    if seg_filtre_prix != "Tous les segments":
        df_prix_view = df_prix_view[df_prix_view["Segment"] == seg_filtre_prix]
    col_cfg_prix = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True), "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True), "Contenance_hl": st.column_config.NumberColumn("Conv. hl", format="%.4f", disabled=True), "2026": st.column_config.NumberColumn("Prix 2026 (Fixé)", format="%.0f", disabled=True)}
    for annee in ANNEES:
        col_cfg_prix[annee] = st.column_config.NumberColumn(f"Prix {annee}", format="%.0f", min_value=0.0, step=10.0)
    df_prix_edited = st.data_editor(df_prix_view, column_config=col_cfg_prix, hide_index=True, use_container_width=True, height=350, key="editor_prix_skus")
    for idx, row in df_prix_edited.iterrows():
        mask = (st.session_state.prix_skus["Segment"] == row["Segment"]) & (st.session_state.prix_skus["Marque"] == row["Marque"]) & (st.session_state.prix_skus["SKU"] == row["SKU"])
        for annee in ANNEES:
            st.session_state.prix_skus.loc[mask, annee] = row[annee]

    df_ca = df_detail[["Segment", "Marque", "SKU"]].copy()
    contenance = df_detail["Contenance_hl"]
    for annee in ANNEES_ALL:
        nb_cols = np.where(contenance > 0, df_detail[annee] / contenance, 0.0)
        df_ca[annee] = nb_cols * st.session_state.prix_skus[annee]

    st.divider()
    st.subheader("2️⃣ Synthèse & Évolution du CA (2026–2031)")
    cols_kpi = st.columns(len(ANNEES_ALL))
    for i, annee in enumerate(ANNEES_ALL):
        ca_tot = df_ca[annee].sum()
        if i == 0:
            cols_kpi[i].metric(f"CA {annee}", fmt_val(ca_tot))
        else:
            ca_prev = df_ca[ANNEES_ALL[i - 1]].sum()
            delta_pct = ((ca_tot - ca_prev) / ca_prev * 100.0) if ca_prev > 0 else 0.0
            cols_kpi[i].metric(f"CA {annee}", fmt_val(ca_tot), f"{delta_pct:+.1f}%")

    st.divider()
    st.subheader("3️⃣ Chiffre d'Affaires Détaillé (Ar)")
    segments_selectionnes_ca = st.multiselect("🔍 Filtrer par Segment (CA) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_ca_seg")
    if not segments_selectionnes_ca:
        st.info("Veuillez sélectionner au moins un segment.")
    else:
        st.markdown(generer_html_fusionne(df_ca, ANNEES_ALL, segments_selectionnes_ca, afficher_evo=True), unsafe_allow_html=True)

        st.divider()
        st.subheader("4️⃣ Graphiques CA (3 Graphes — Évolution & Part en %)")

        df_ca_seg = (
            df_ca[df_ca["Segment"].isin(segments_selectionnes_ca)]
            .groupby("Segment", as_index=False)[ANNEES_ALL]
            .sum()
            .melt(id_vars="Segment", value_vars=ANNEES_ALL, var_name="Année", value_name="CA")
        )
        totaux_ca_annee = df_ca_seg.groupby("Année")["CA"].transform("sum")
        df_ca_seg["Part_Pct"] = np.where(totaux_ca_annee > 0, (df_ca_seg["CA"] / totaux_ca_annee) * 100.0, 0.0)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_c1 = px.line(
                df_ca_seg,
                x="Année",
                y="CA",
                color="Segment",
                markers=True,
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_c1, "1. Évolution du CA par Segment (Ar)", "CA (Ar)"), use_container_width=True)

        with col_c2:
            fig_c2 = px.bar(
                df_ca_seg,
                x="Année",
                y="CA",
                color="Segment",
                barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS,
                category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_c2, "2. Répartition Empilée du CA par Segment (Ar)", "CA (Ar)"), use_container_width=True)

        fig_c3 = px.bar(
            df_ca_seg,
            x="Année",
            y="Part_Pct",
            color="Segment",
            barmode="stack",
            color_discrete_map=COULEURS_SEGMENTS,
            category_orders={"Segment": ORDRE_SEGMENTS},
        )
        st.plotly_chart(styler_graphe(fig_c3, "3. Part du CA en (%) par Segment (2026–2031)", "Part du CA (%)"), use_container_width=True)


# #####################################################
# ONGLET 3 : VOLUME PAR AGENCE (FILTRES INTERACTIFS)
# #####################################################
with onglet_agences:
    st.subheader("📍 Volumes par Agence & par Mois")

    col_ag1, col_ag2, col_ag3 = st.columns(3)
    with col_ag1:
        annee_agence = st.selectbox("Sélectionnez l'Année :", ANNEES, index=0, key="ag_annee")
    with col_ag2:
        agence_filtre = st.selectbox("Sélectionnez l'Agence :", ["Toutes les agences"] + AGENCES, key="ag_agence")
    with col_ag3:
        segment_filtre_ag = st.selectbox("Sélectionnez le Segment :", ["Tous les segments"] + ORDRE_SEGMENTS, key="ag_segment")

    st.markdown("---")

    df_ag_vol = df_dispatch_base.copy()
    df_ag_vol = df_ag_vol.merge(df_detail[["Segment", "Marque", "SKU", annee_agence]], left_on=["Segment", "Marque", "Article"], right_on=["Segment", "Marque", "SKU"], how="left")
    df_ag_vol = df_ag_vol.rename(columns={annee_agence: "Volume_Annuel"}).drop(columns=["SKU"])
    df_ag_vol["Volume"] = df_ag_vol["Volume_Annuel"] * df_ag_vol["Poids_Dispatch"]

    if agence_filtre != "Toutes les agences":
        df_ag_vol = df_ag_vol[df_ag_vol["Agence"] == agence_filtre]
    if segment_filtre_ag != "Tous les segments":
        df_ag_vol = df_ag_vol[df_ag_vol["Segment"] == segment_filtre_ag]

    if df_ag_vol.empty:
        st.warning("Aucune donnée pour ces filtres.")
    else:
        agences_a_afficher = [agence_filtre] if agence_filtre != "Toutes les agences" else AGENCES
        st.markdown(generer_html_agences_par_mois(df_ag_vol, agences_a_afficher), unsafe_allow_html=True)


# #####################################################
# ONGLET 4 : DISPATCH AGENCE & MOIS (EXPORT)
# #####################################################
with onglet_dispatch:
    st.subheader("🚚 Dispatch Détaillé (Agence & Mois)")
    st.caption("Ce tableau détaille la répartition mensuelle et géographique du volume pour l'année sélectionnée, avec possibilité d'exporter les données.")

    annee_dispatch = st.selectbox("Sélectionnez l'année à ventiler :", ANNEES, index=0, key="disp_annee")

    df_disp_annee = df_dispatch_base.copy()
    df_disp_annee = df_disp_annee.merge(df_detail[["Segment", "Marque", "SKU", annee_dispatch]], left_on=["Segment", "Marque", "Article"], right_on=["Segment", "Marque", "SKU"], how="left")
    df_disp_annee = df_disp_annee.rename(columns={annee_dispatch: "Volume_Annuel"}).drop(columns=["SKU"])
    df_disp_annee["Volume_Dispatch"] = df_disp_annee["Volume_Annuel"] * df_disp_annee["Poids_Dispatch"]

    df_pivot = df_disp_annee.groupby(["Agence", "Mois"])["Volume_Dispatch"].sum().reset_index()
    df_pivot_wide = df_pivot.pivot(index="Agence", columns="Mois", values="Volume_Dispatch").fillna(0)
    df_pivot_wide["Total Annuel"] = df_pivot_wide.sum(axis=1)

    st.markdown(f"#### 📊 Volume dispatché par Agence et par Mois pour {annee_dispatch}")
    st.dataframe(df_pivot_wide.style.format("{:,.0f}").background_gradient(cmap="Blues", axis=None), use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Télécharger le Dispatch")

    df_export = df_disp_annee.copy()
    df_export["Année"] = annee_dispatch
    df_export["Ag"] = df_export["Agence"].str.extract(r'^(\d+)').astype(int)
    df_export["Attribut"] = df_export["Mois"] + " Hecto"
    df_export["Valeur"] = df_export["Volume_Dispatch"]
    df_export["Col/Hl"] = "Hecto"
    df_export["Mois_Num"] = df_export["Mois"]

    df_export = df_export[["Année", "Segment", "Marque", "Article", "Agence", "Ag", "Attribut", "Valeur", "Col/Hl", "Mois_Num"]]
    df_export.columns = ["Année", "Segment", "Marque", "Article", "Agence", "AG", "Attribut", "Valeur", "Col/Hl", "Mois"]

    buffer_disp = io.BytesIO()
    with pd.ExcelWriter(buffer_disp, engine="openpyxl") as writer_disp:
        df_export.to_excel(writer_disp, sheet_name=f"Dispatch_{annee_dispatch}", index=False)
        ws = writer_disp.sheets[f"Dispatch_{annee_dispatch}"]
        for col in ws.columns:
            max_length = max([len(str(cell.value)) for cell in col])
            ws.column_dimensions[col[0].column_letter].width = max(max_length + 2, 12)

    buffer_disp.seek(0)
    st.download_button(
        label="📥 Télécharger le Fichier de Dispatch (Excel)",
        data=buffer_disp,
        file_name=f"Dispatch_Volumes_{annee_dispatch}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
