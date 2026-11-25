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

df_base = pd.DataFrame(
    detail,
    columns=["Segment", "Marque", "SKU", "2026", "Base_2027", "Prix_2026_Fixe", "Contenance_hl"],
)

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

TOTAL_2027 = df_base["Base_2027"].sum()
mix_2027_calcul = (df_base.groupby("Segment")["Base_2027"].sum() / TOTAL_2027) * 100

# =====================================================
# DONNEES AGENCES (Exemple basé sur le fichier)
# =====================================================
# Dans une vraie application, vous liriez "Vol par AG.xlsx" avec pd.read_excel().
# Ici, j'ai recréé une structure réaliste pour que l'interface fonctionne.
AGENCES = ["01-Tanjombato", "03-Usine-Diego", "04-Tulear", "05-Fianarantsoa", "09-Tamatave", "11-Andranomahery"]
MOIS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

# Génération de données aléatoires basées sur vos totaux pour simuler l'agence
np.random.seed(42)
agence_data = []
for _, row in df_base.iterrows():
    if row["Base_2027"] == 0: continue
    # On répartit le volume de l'article sur les agences et les mois
    for ag in AGENCES:
        # Poids aléatoire de l'agence (somme = 1)
        poids_ag = np.random.dirichlet(np.ones(len(AGENCES)), size=1)[0]
        vol_ag = row["Base_2027"] * poids_ag[AGENCES.index(ag)]
        
        for m in MOIS:
            # Poids aléatoire du mois (somme = 1)
            poids_mois = np.random.dirichlet(np.ones(12), size=1)[0]
            vol_mois = vol_ag * poids_mois[MOIS.index(m)]
            
            agence_data.append({
                "Segment": row["Segment"],
                "Marque": row["Marque"],
                "Article": row["SKU"],
                "Agence": ag,
                "Mois": m,
                "Volume": vol_mois
            })

df_agences = pd.DataFrame(agence_data)

# =====================================================
# INITIALISATION DES SESSION STATES
# =====================================================
if "objectifs" not in st.session_state:
    st.session_state.objectifs = pd.DataFrame({
        "Année": ANNEES,
        "Volume": [4600000, 4900000, 5250000, 5600000, 6000000],
    })

if "mix" not in st.session_state:
    st.session_state.mix = pd.DataFrame({
        "Segment": ["Alcomix", "BG", "BIERES", "EAUX", "Energy", "TOTAL"],
        "2027": [
            mix_2027_calcul.get("Alcomix", 0), mix_2027_calcul.get("BG", 0), mix_2027_calcul.get("BIERES", 0),
            mix_2027_calcul.get("EAUX", 0), mix_2027_calcul.get("Energy", 0), 100.00,
        ],
        "2028": [1.00, 27.37, 51.50, 18.59, 1.54, 100.00],
        "2029": [1.00, 27.80, 51.50, 18.00, 1.70, 100.00],
        "2030": [1.00, 27.90, 51.50, 17.75, 1.80, 99.95],
        "2031": [1.00, 28.00, 51.50, 17.50, 2.00, 100.00],
    })

if "poids_marques" not in st.session_state:
    df_pm_init = df_base[["Segment", "Marque", "Poids_Marque_Init"]].drop_duplicates().reset_index(drop=True)
    for annee in ANNEES: df_pm_init[annee] = df_pm_init["Poids_Marque_Init"]
    st.session_state.poids_marques = df_pm_init.drop(columns=["Poids_Marque_Init"])

if "poids_skus" not in st.session_state:
    df_ps_init = df_base[["Segment", "Marque", "SKU", "Poids_SKU_Init"]].copy()
    for annee in ANNEES: df_ps_init[annee] = df_ps_init["Poids_SKU_Init"]
    st.session_state.poids_skus = df_ps_init.drop(columns=["Poids_SKU_Init"])

colonnes_prix_attendues = ["Segment", "Marque", "SKU", "Contenance_hl"] + ANNEES_ALL
if ("prix_skus" not in st.session_state or not all(col in st.session_state.prix_skus.columns for col in colonnes_prix_attendues)):
    df_prix_init = df_base[["Segment", "Marque", "SKU", "Contenance_hl"]].copy()
    for annee in ANNEES_ALL: df_prix_init[annee] = df_base["Prix_2026_Fixe"].astype(float)
    st.session_state.prix_skus = df_prix_init

# =====================================================
# FONCTIONS COMMUNES
# =====================================================
def fmt_val(val):
    if pd.isna(val) or val == 0: return "-"
    return f"{val:,.0f}".replace(",", " ")

def calculer_taux_evolution(df_agg, id_cols):
    rows = []
    for _, r in df_agg.iterrows():
        for i in range(1, len(ANNEES_ALL)):
            an_curr, an_prev = ANNEES_ALL[i], ANNEES_ALL[i - 1]
            v_curr, v_prev = r[an_curr], r[an_prev]
            taux = ((v_curr - v_prev) / v_prev * 100.0) if v_prev > 0 else np.nan
            item = {col: r[col] for col in id_cols}
            item["Année"], item["Taux Évo (%)"], item["Label (%)"] = an_curr, taux, f"{taux:+.1f}%" if not pd.isna(taux) else "N/A"
            rows.append(item)
    return pd.DataFrame(rows)

def generer_html_fusionne(df_source, cols_annees, segments_cibles, afficher_evo=False):
    df_sub = df_source[df_source["Segment"].isin(segments_cibles)]
    label_total = "TOTAL ANNEE" if len(segments_cibles) == len(ORDRE_SEGMENTS) else "TOTAL SÉLECTION"
    
    # CSS pour le style Excel
    css = """
    <style>
    .sop-container { max-height: 900px; overflow-y: auto; border: 1px solid #d0d0d0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 13px; }
    table.sop-table { width: 100%; border-collapse: collapse; text-align: right; }
    table.sop-table thead th { position: sticky; top: 0; background-color: #262626; color: white; padding: 8px; border: 1px solid #595959; z-index: 2; text-align: center; }
    table.sop-table td { padding: 5px 10px; border: 1px solid #d9d9d9; }
    .row-total td { background-color: #FFF2CC; font-weight: bold; font-size: 14px; }
    .row-eco-total td { background-color: #FFF2CC; font-weight: bold; font-size: 13px; font-style: italic; }
    .cell-seg-side { background-color: #C00000; color: white; font-weight: bold; text-align: center; vertical-align: middle; font-size: 15px; width: 110px; }
    .row-seg-top td { background-color: #C00000; color: white; font-weight: bold; }
    .cell-marque-side { background-color: #F8CBAD; font-weight: bold; text-align: center; vertical-align: middle; width: 130px; }
    .row-marque-top td { background-color: #F8CBAD; font-weight: bold; }
    .cell-sku { background-color: #FFFFFF; text-align: left; }
    .cell-val { background-color: #FFFFFF; }
    </style>
    """
    html = [css, '<div class="sop-container"><table class="sop-table"><thead><tr><th colspan="3">Segment / Marque / SKU</th>']
    for annee in cols_annees: html.append(f"<th>{annee}</th>")
    html.append("</tr></thead><tbody>")
    
    # Ligne Total Haut
    html.append(f'<tr class="row-total"><td colspan="3" style="text-align:center;">{label_total}</td>')
    for annee in cols_annees: html.append(f"<td>{fmt_val(df_sub[annee].sum())}</td>")
    html.append("</tr>")
    
    # Données
    for segment in ORDRE_SEGMENTS:
        if segment not in segments_cibles: continue
        seg_data = df_sub[df_sub["Segment"] == segment]
        if len(seg_data) == 0: continue
        marques = seg_data["Marque"].unique()
        total_rows_seg = 1 + sum(1 + len(seg_data[seg_data["Marque"] == m]) for m in marques)
        
        html.append(f'<tr class="row-seg-top"><td rowspan="{total_rows_seg}" class="cell-seg-side">{segment}</td><td colspan="2" style="text-align:center;">{segment}</td>')
        for annee in cols_annees: html.append(f"<td>{fmt_val(seg_data[annee].sum())}</td>")
        html.append("</tr>")
        
        for marque in marques:
            marq_data = seg_data[seg_data["Marque"] == marque]
            html.append(f'<tr class="row-marque-top"><td rowspan="{1 + len(marq_data)}" class="cell-marque-side">{marque}</td><td style="text-align:left;"></td>')
            for annee in cols_annees: html.append(f"<td>{fmt_val(marq_data[annee].sum())}</td>")
            html.append("</tr>")
            
            for _, row in marq_data.iterrows():
                html.append("<tr>")
                html.append(f'<td class="cell-sku">{row["SKU"]}</td>')
                for annee in cols_annees: html.append(f'<td class="cell-val">{fmt_val(row[annee])}</td>')
                html.append("</tr>")
                
    if afficher_evo:
        html.append('<tr class="row-eco-total"><td colspan="3" style="text-align:center;">Évolution vs N-1 (%)</td>')
        for i, annee in enumerate(cols_annees):
            if i == 0: html.append("<td>-</td>")
            else:
                v_curr, v_prev = df_sub[annee].sum(), df_sub[cols_annees[i-1]].sum()
                taux = ((v_curr - v_prev) / v_prev * 100.0) if v_prev > 0 else 0
                html.append(f"<td>{'+' if taux >= 0 else ''}{taux:.1f}%</td>")
        html.append("</tr>")

    html.append("</tbody></table></div>")
    return "".join(html)

def generer_html_agences(df_source):
    """Génère un tableau HTML dépliable par Segment > Marque > Article avec les colonnes Agences"""
    # On agrège par Segment, Marque, Article, et par Agence
    df_grp = df_source.groupby(["Segment", "Marque", "Article", "Agence"])["Volume"].sum().reset_index()
    
    css = """
    <style>
    .ag-container { font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 13px; }
    details { margin-bottom: 5px; border: 1px solid #d0d0d0; border-radius: 4px; }
    summary { padding: 8px 12px; background-color: #f8f9fa; cursor: pointer; font-weight: bold; color: #333; border-bottom: 1px solid #d0d0d0; }
    summary:hover { background-color: #e9ecef; }
    summary::-webkit-details-marker { display: none; }
    summary::before { content: '▶'; display: inline-block; margin-right: 10px; font-size: 10px; color: #666; transition: transform 0.2s; }
    details[open] > summary::before { transform: rotate(90deg); }
    .ag-table { width: 100%; border-collapse: collapse; text-align: right; margin-top: 5px; }
    .ag-table th { background-color: #f1f3f5; padding: 6px 10px; border-bottom: 2px solid #dee2e6; text-align: center; font-weight: 600; }
    .ag-table td { padding: 5px 10px; border-bottom: 1px solid #eee; }
    .ag-table tr:hover { background-color: #f8f9fa; }
    .ag-row-total td { font-weight: bold; background-color: #fff3cd; }
    </style>
    """
    html = [css, '<div class="ag-container">']
    
    # Boucle sur les segments
    for segment in ORDRE_SEGMENTS:
        df_seg = df_grp[df_grp["Segment"] == segment]
        if df_seg.empty: continue
        
        # Agrégation par Agence pour le segment
        seg_ag = df_seg.groupby("Agence")["Volume"].sum()
        
        html.append(f'<details><summary>{segment} (Total : {seg_ag.sum():,.0f} hl)</summary>')
        html.append('<table class="ag-table"><thead><tr><th style="text-align:left;">Marque / Article</th>')
        for ag in AGENCES: html.append(f"<th>{ag}</th>")
        html.append("<th>Total</th></tr></thead><tbody>")
        
        # Ligne total segment
        html.append('<tr class="ag-row-total"><td style="text-align:left;">Total Segment</td>')
        for ag in AGENCES: html.append(f"<td>{fmt_val(seg_ag.get(ag, 0))}</td>")
        html.append(f"<td>{fmt_val(seg_ag.sum())}</td></tr>")
        
        # Boucle sur les marques
        for marque in df_seg["Marque"].unique():
            df_marq = df_seg[df_seg["Marque"] == marque]
            marq_ag = df_marq.groupby("Agence")["Volume"].sum()
            
            # Sous-détails par marque
            html.append(f'<tr><td colspan="{len(AGENCES)+2}" style="padding:0;"><details><summary style="background:none; border:none; padding:5px 10px; font-weight:bold; color:#555;">{marque}</summary>')
            html.append('<table class="ag-table" style="margin:0;"><tbody>')
            
            # Ligne Total Marque
            html.append('<tr class="ag-row-total"><td style="text-align:left;">Total Marque</td>')
            for ag in AGENCES: html.append(f"<td>{fmt_val(marq_ag.get(ag, 0))}</td>")
            html.append(f"<td>{fmt_val(marq_ag.sum())}</td></tr>")
            
            # Lignes Articles
            for article in df_marq["Article"].unique():
                df_art = df_marq[df_marq["Article"] == article]
                art_ag = df_art.groupby("Agence")["Volume"].sum()
                html.append(f'<tr><td style="text-align:left;">{article}</td>')
                for ag in AGENCES: html.append(f"<td>{fmt_val(art_ag.get(ag, 0))}</td>")
                html.append(f"<td>{fmt_val(art_ag.sum())}</td></tr>")
                
            html.append("</tbody></table></details></td></tr>")
            
        html.append("</tbody></table></details>")
        
    html.append("</div>")
    return "".join(html)

# =====================================================
# NAVIGATION PRINCIPALE
# =====================================================
onglet_vol, onglet_ca, onglet_agences = st.tabs([
    "📦 Simulation Volumes en hl (2026–2031)",
    "💰 Calcul Chiffre d'Affaires en Ar — CA (2026–2031)",
    "📍 Volume par Agence (2027)"
])

components.html(
    """
    <script>
    (function() {
        const parentDoc = window.parent.document;
        function figeHeaderEtOnglets() {
            const headerDiv = parentDoc.getElementById("sop-fixed-header");
            const mainBlock = parentDoc.querySelector('[data-testid="stMainBlockContainer"]') || parentDoc.querySelector('.block-container');
            const tabLists = parentDoc.querySelectorAll('[data-baseweb="tab-list"]');
            if (!headerDiv || !tabLists.length) return;
            headerDiv.style.backgroundColor = "#ffffff";
            const headerHeight = headerDiv.getBoundingClientRect().height || 58;
            const mainTabList = tabLists[0];
            mainTabList.style.position = "fixed"; mainTabList.style.top = headerHeight + "px";
            mainTabList.style.left = "0px"; mainTabList.style.right = "0px"; mainTabList.style.width = "100%";
            mainTabList.style.backgroundColor = "#ffffff"; mainTabList.style.zIndex = "1001";
            mainTabList.style.padding = "0.5rem 3rem 0.5rem 3rem"; mainTabList.style.borderBottom = "1px solid #e0e0e0";
            mainTabList.style.boxShadow = "0 4px 6px -6px rgba(0, 0, 0, 0.1)";
            const tabsHeight = mainTabList.getBoundingClientRect().height || 44;
            if (mainBlock) mainBlock.style.paddingTop = (headerHeight + tabsHeight + 20) + "px";
        }
        figeHeaderEtOnglets(); setTimeout(figeHeaderEtOnglets, 150);
        setTimeout(figeHeaderEtOnglets, 500); setTimeout(figeHeaderEtOnglets, 1000);
        window.parent.addEventListener("resize", figeHeaderEtOnglets);
        const observer = new MutationObserver(figeHeaderEtOnglets);
        if (parentDoc.body) observer.observe(parentDoc.body, { childList: true, subtree: true });
    })();
    </script>
    """,
    height=0,
)

# #####################################################
# ONGLET 1 : SIMULATION DES VOLUMES
# #####################################################
with onglet_vol:
    st.subheader("1️⃣ Objectifs Globaux (Volumes en hl)")
    df_obj = st.data_editor(st.session_state.objectifs, column_config={"Année": st.column_config.TextColumn("Année", disabled=True), "Volume": st.column_config.NumberColumn("Volume Objectif (hl)", format="%d", min_value=0, step=10000)}, hide_index=True, use_container_width=True, key="editor_objectif")
    st.session_state.objectifs = df_obj

    st.subheader("2️⃣ Mix Segment (%)")
    for annee in ANNEES: st.session_state.mix.loc[st.session_state.mix["Segment"] == "TOTAL", annee] = st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee].sum()
    col_config_mix = {"Segment": st.column_config.TextColumn("Segment", disabled=True)}
    for annee in ANNEES: col_config_mix[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.05)
    df_mix = st.data_editor(st.session_state.mix, column_config=col_config_mix, hide_index=True, use_container_width=True, key="mix_editor")
    erreurs_mix = []
    for annee in ANNEES:
        st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee] = df_mix.loc[df_mix["Segment"] != "TOTAL", annee].values
        total_annee = st.session_state.mix.loc[st.session_state.mix["Segment"] != "TOTAL", annee].sum()
        st.session_state.mix.loc[st.session_state.mix["Segment"] == "TOTAL", annee] = total_annee
        if not np.isclose(total_annee, 100.0, atol=0.06): erreurs_mix.append(f"**{annee}** ({total_annee:.2f} %)")
    if erreurs_mix: st.error(f"⚠️ **Attention : Le total du Mix Segment doit être égal à 100 %.** Années en erreur : {', '.join(erreurs_mix)}.")
    else: st.success("✅ **Validation OK :** Tous les totaux du Mix Segment sont conformes.")

    st.divider()
    st.subheader("3️⃣ Paramétrage des Poids : Marques & Articles (%)")
    if st.button("🔄 Réinitialiser tous les poids (Base 2027)"):
        del st.session_state["poids_marques"]; del st.session_state["poids_skus"]; st.rerun()

    tab_pm, tab_ps = st.tabs(["🏷️ Poids des Marques", "📦 Poids des Articles (SKU)"])
    with tab_pm:
        seg_filtre_pm = st.selectbox("Sélectionner un Segment à modifier :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="sel_seg_pm")
        df_pm_view = st.session_state.poids_marques.copy()
        if seg_filtre_pm != "Tous les segments": df_pm_view = df_pm_view[df_pm_view["Segment"] == seg_filtre_pm]
        col_cfg_pm = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True)}
        for annee in ANNEES: col_cfg_pm[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1)
        df_pm_edited = st.data_editor(df_pm_view, column_config=col_cfg_pm, hide_index=True, use_container_width=True, key="editor_poids_marques")
        for idx, row in df_pm_edited.iterrows():
            mask = (st.session_state.poids_marques["Segment"] == row["Segment"]) & (st.session_state.poids_marques["Marque"] == row["Marque"])
            for annee in ANNEES: st.session_state.poids_marques.loc[mask, annee] = row[annee]
        erreurs_pm = []
        segs_a_verifier = ORDRE_SEGMENTS if seg_filtre_pm == "Tous les segments" else [seg_filtre_pm]
        for seg in segs_a_verifier:
            sub_pm = st.session_state.poids_marques[st.session_state.poids_marques["Segment"] == seg]
            for annee in ANNEES:
                somme = sub_pm[annee].sum()
                if not np.isclose(somme, 100.0, atol=0.05): erreurs_pm.append(f"**{seg} ({annee})** : {somme:.2f} %")
        if erreurs_pm: st.warning(f"⚠️ Écarts détectés : {', '.join(erreurs_pm)}")
        else: st.success("✅ Somme des poids des marques = 100 % pour chaque segment.")
        
    with tab_ps:
        st.markdown("**Édition manuelle des poids SKU (%) :**")
        col_f1, col_f2 = st.columns(2)
        with col_f1: seg_filtre_ps = st.selectbox("1. Filtrer par Segment :", options=ORDRE_SEGMENTS, key="sel_seg_ps")
        marques_dispo = st.session_state.poids_skus[st.session_state.poids_skus["Segment"] == seg_filtre_ps]["Marque"].unique().tolist()
        with col_f2: marque_filtre_ps = st.selectbox("2. Filtrer par Marque :", options=marques_dispo, key="sel_marque_ps")
        df_ps_view = st.session_state.poids_skus[(st.session_state.poids_skus["Segment"] == seg_filtre_ps) & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)].copy()
        col_cfg_ps = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True), "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True)}
        for annee in ANNEES: col_cfg_ps[annee] = st.column_config.NumberColumn(annee, format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1)
        df_ps_edited = st.data_editor(df_ps_view, column_config=col_cfg_ps, hide_index=True, use_container_width=True, key="editor_poids_skus")
        for idx, row in df_ps_edited.iterrows():
            mask = (st.session_state.poids_skus["Segment"] == row["Segment"]) & (st.session_state.poids_skus["Marque"] == row["Marque"]) & (st.session_state.poids_skus["SKU"] == row["SKU"])
            for annee in ANNEES: st.session_state.poids_skus.loc[mask, annee] = row[annee]
        erreurs_ps = []
        sub_ps = st.session_state.poids_skus[(st.session_state.poids_skus["Segment"] == seg_filtre_ps) & (st.session_state.poids_skus["Marque"] == marque_filtre_ps)]
        for annee in ANNEES:
            somme_sku = sub_ps[annee].sum()
            poids_m = st.session_state.poids_marques.loc[(st.session_state.poids_marques["Segment"] == seg_filtre_ps) & (st.session_state.poids_marques["Marque"] == marque_filtre_ps), annee].iloc[0]
            if poids_m > 0 and not np.isclose(somme_sku, 100.0, atol=0.05): erreurs_ps.append(f"**{annee}** ({somme_sku:.2f} %)")
        if erreurs_ps: st.warning(f"⚠️ Écarts : {', '.join(erreurs_ps)}")
        else: st.success(f"✅ Somme des poids des articles de **{marque_filtre_ps}** conforme.")

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
    st.subheader("📊 Visualisation des Évolutions Volumes (2026–2031)")
    df_chart_seg = df_detail.groupby("Segment", as_index=False)[ANNEES_ALL].sum()
    df_chart_seg_melt = df_chart_seg.melt(id_vars="Segment", var_name="Année", value_name="Volume")
    totaux_annuels = df_chart_seg_melt.groupby("Année")["Volume"].transform("sum")
    df_chart_seg_melt["Mix (%)"] = np.where(totaux_annuels > 0, (df_chart_seg_melt["Volume"] / totaux_annuels) * 100.0, 0.0)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_bar = px.bar(df_chart_seg_melt, x="Année", y="Volume", color="Segment", title="Évolution des Volumes (hl) par Segment (Empilé)", text_auto=".2s")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_g2:
        fig_line = px.line(df_chart_seg_melt, x="Année", y="Volume", color="Segment", markers=True, title="Trajectoire de Croissance des Volumes (hl) par Segment")
        st.plotly_chart(fig_line, use_container_width=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_mix_bar = px.bar(df_chart_seg_melt, x="Année", y="Mix (%)", color="Segment", title="Évolution du Mix Segment (%) par An", text=df_chart_seg_melt["Mix (%)"].apply(lambda x: f"{x:.1f}%"))
        fig_mix_bar.update_traces(textposition="inside"); fig_mix_bar.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_mix_bar, use_container_width=True)
    with col_m2:
        fig_mix_line = px.line(df_chart_seg_melt, x="Année", y="Mix (%)", color="Segment", markers=True, title="Évolution Comparative des Parts de Mix (%)")
        fig_mix_line.update_traces(textposition="top center")
        st.plotly_chart(fig_mix_line, use_container_width=True)

    st.divider()
    st.subheader("4️⃣ Volumes Simulés Détaillés (hl)")
    segments_selectionnes_vol = st.multiselect("🔍 Filtrer par Segment (Volumes) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_vol_seg")
    if not segments_selectionnes_vol: st.info("Veuillez sélectionner au moins un segment.")
    else: st.markdown(generer_html_fusionne(df_detail, ANNEES_ALL, segments_selectionnes_vol, afficher_evo=False), unsafe_allow_html=True)


# #####################################################
# ONGLET 2 : CALCUL CHIFFRE D'AFFAIRES (CA EN AR)
# #####################################################
with onglet_ca:
    st.subheader("1️⃣ Gestion des Prix Unitaires (2026 fixé — Upload & Édition 2027 → 2031)")
    st.caption("Formule appliquée : **CA (Ar) = (Volume en hl / Contenance unitaire en hl) × Prix Unitaire (Ar)**")

    col_p_reset, _ = st.columns([1, 4])
    with col_p_reset:
        if st.button("🔄 Réinitialiser les prix 2027–2031 (Base 2026)", key="btn_reset_prix"):
            del st.session_state["prix_skus"]; st.rerun()

    seg_filtre_prix = st.selectbox("🔍 Filtrer la grille des Prix par Segment :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="sel_seg_prix")
    df_prix_view = st.session_state.prix_skus.copy()
    
    # --- Test de calcul FOSA 2026 ---
    fosa_row = df_prix_view[df_prix_view["SKU"] == "FOSA 50 cl CAN"]
    vol_fosa, conv_fosa = 3265, 0.005
    prix_fosa = fosa_row["2026"].values[0] if not fosa_row.empty else 3830
    ca_fosa = (vol_fosa / conv_fosa) * prix_fosa
    st.info(f"🧪 **Test de calcul (FOSA 2026) :** {vol_fosa:,.0f} hl / {conv_fosa} hl = {vol_fosa/conv_fosa:,.0f} unités. CA = {vol_fosa/conv_fosa:,.0f} × {prix_fosa:,.0f} Ar = **{ca_fosa:,.0f} Ar**")
    
    if seg_filtre_prix != "Tous les segments": df_prix_view = df_prix_view[df_prix_view["Segment"] == seg_filtre_prix]
    col_cfg_prix = {"Segment": st.column_config.TextColumn("Segment", disabled=True), "Marque": st.column_config.TextColumn("Marque", disabled=True), "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True), "Contenance_hl": st.column_config.NumberColumn("Conv. hl", format="%.4f", disabled=True), "2026": st.column_config.NumberColumn("Prix 2026 (Fixé)", format="%.0f", disabled=True)}
    for annee in ANNEES: col_cfg_prix[annee] = st.column_config.NumberColumn(f"Prix {annee}", format="%.0f", min_value=0.0, step=10.0)
    df_prix_edited = st.data_editor(df_prix_view, column_config=col_cfg_prix, hide_index=True, use_container_width=True, height=350, key="editor_prix_skus")
    for idx, row in df_prix_edited.iterrows():
        mask = (st.session_state.prix_skus["Segment"] == row["Segment"]) & (st.session_state.prix_skus["Marque"] == row["Marque"]) & (st.session_state.prix_skus["SKU"] == row["SKU"])
        for annee in ANNEES: st.session_state.prix_skus.loc[mask, annee] = row[annee]

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
        if i == 0: cols_kpi[i].metric(f"CA {annee}", fmt_val(ca_tot))
        else:
            ca_prev = df_ca[ANNEES_ALL[i - 1]].sum()
            delta_pct = ((ca_tot - ca_prev) / ca_prev * 100.0) if ca_prev > 0 else 0.0
            cols_kpi[i].metric(f"CA {annee}", fmt_val(ca_tot), f"{delta_pct:+.1f}%")

    df_chart_ca = df_ca.groupby("Segment", as_index=False)[ANNEES_ALL].sum()
    df_chart_ca_melt = df_chart_ca.melt(id_vars="Segment", var_name="Année", value_name="Chiffre d'Affaires")
    totaux_ca_annuels = df_chart_ca_melt.groupby("Année")["Chiffre d'Affaires"].transform("sum")
    df_chart_ca_melt["Mix CA (%)"] = np.where(totaux_ca_annuels > 0, (df_chart_ca_melt["Chiffre d'Affaires"] / totaux_ca_annuels) * 100.0, 0.0)

    col_ca1, col_ca2 = st.columns(2)
    with col_ca1:
        fig_ca_bar = px.bar(df_chart_ca_melt, x="Année", y="Chiffre d'Affaires", color="Segment", title="Évolution du CA (Ar) par Segment", text_auto=".3s")
        st.plotly_chart(fig_ca_bar, use_container_width=True)
    with col_ca2:
        fig_ca_mix = px.bar(df_chart_ca_melt, x="Année", y="Mix CA (%)", color="Segment", title="Évolution du Mix Valeur / CA (%)", text=df_chart_ca_melt["Mix CA (%)"].apply(lambda x: f"{x:.1f}%"))
        fig_ca_mix.update_traces(textposition="inside"); fig_ca_mix.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_ca_mix, use_container_width=True)

    st.divider()
    st.subheader("3️⃣ Chiffre d'Affaires Détaillé (Ar)")
    segments_selectionnes_ca = st.multiselect("🔍 Filtrer par Segment (CA) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_ca_seg")
    if not segments_selectionnes_ca: st.info("Veuillez sélectionner au moins un segment.")
    else: st.markdown(generer_html_fusionne(df_ca, ANNEES_ALL, segments_selectionnes_ca, afficher_evo=True), unsafe_allow_html=True)


# #####################################################
# ONGLET 3 : VOLUME PAR AGENCE
# #####################################################
with onglet_agences:
    st.subheader("📍 Volumes par Agence (Base 2027)")
    st.caption("Cette vue présente la répartition géographique des volumes. Cliquez sur un segment ou une marque pour déplier le détail par article et par agence.")
    
    # Filtre pour choisir le Segment (optionnel, mais utile si beaucoup de données)
    seg_agence_filtre = st.selectbox("🔍 Filtrer par Segment :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="filter_agence_seg")
    
    df_agences_filtre = df_agences.copy()
    if seg_agence_filtre != "Tous les segments":
        df_agences_filtre = df_agences_filtre[df_agences_filtre["Segment"] == seg_agence_filtre]
        
    st.markdown(generer_html_agences(df_agences_filtre), unsafe_allow_html=True)
