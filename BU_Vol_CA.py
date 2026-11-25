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
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 1005 !important;
    }
    #sop-fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1002;
        padding: 0.9rem 3rem 0.5rem 3rem;
        background-color: #ffffff !important;
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
    }
    #sop-fixed-header h1 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
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
            mix_2027_calcul.get("Alcomix", 0),
            mix_2027_calcul.get("BG", 0),
            mix_2027_calcul.get("BIERES", 0),
            mix_2027_calcul.get("EAUX", 0),
            mix_2027_calcul.get("Energy", 0),
            100.00,
        ],
        "2028": [1.00, 27.37, 51.50, 18.59, 1.54, 100.00],
        "2029": [1.00, 27.80, 51.50, 18.00, 1.70, 100.00],
        "2030": [1.00, 27.90, 51.50, 17.75, 1.80, 99.95],
        "2031": [1.00, 28.00, 51.50, 17.50, 2.00, 100.00],
    })

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

colonnes_prix_attendues = ["Segment", "Marque", "SKU", "Contenance_hl"] + ANNEES_ALL
if (
    "prix_skus" not in st.session_state
    or not all(col in st.session_state.prix_skus.columns for col in colonnes_prix_attendues)
):
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


def calculer_taux_evolution(df_agg, id_cols):
    rows = []
    for _, r in df_agg.iterrows():
        for i in range(1, len(ANNEES_ALL)):
            an_curr = ANNEES_ALL[i]
            an_prev = ANNEES_ALL[i - 1]
            v_curr = r[an_curr]
            v_prev = r[an_prev]
            taux = ((v_curr - v_prev) / v_prev * 100.0) if v_prev > 0 else np.nan
            item = {col: r[col] for col in id_cols}
            item["Année"] = an_curr
            item["Taux Évo (%)"] = taux
            item["Label (%)"] = f"{taux:+.1f}%" if not pd.isna(taux) else "N/A"
            rows.append(item)
    return pd.DataFrame(rows)


def generer_html_fusionne(df_source, cols_annees, segments_cibles, afficher_evo=False):
    df_sub = df_source[df_source["Segment"].isin(segments_cibles)]
    label_total = (
        "TOTAL ANNEE"
        if len(segments_cibles) == len(ORDRE_SEGMENTS)
        else "TOTAL SÉLECTION"
    )

    css = """
    <style>
    .sop-container { max-height: 900px; overflow-y: auto; border: 1px solid #d0d0d0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 13px; }
    table.sop-table { width: 100%; border-collapse: collapse; text-align: right; }
    table.sop-table thead th { position: sticky; top: 0; background-color: #262626; color: white; padding: 8px 10px; border: 1px solid #595959; z-index: 2; text-align: center; }
    table.sop-table td { padding: 5px 10px; border: 1px solid #d9d9d9; }
    .row-total td { background-color: #FFF2CC; color: #000000; font-weight: bold; font-size: 14px; }
    .row-eco-total td { background-color: #FFF2CC; color: #000000; font-weight: bold; font-size: 13px; font-style: italic; }
    .cell-seg-side { background-color: #C00000; color: white; font-weight: bold; text-align: center; vertical-align: middle; font-size: 15px; width: 110px; }
    .row-seg-top td { background-color: #C00000; color: white; font-weight: bold; }
    .cell-marque-side { background-color: #F8CBAD; color: #000000; font-weight: bold; text-align: center; vertical-align: middle; width: 130px; }
    .row-marque-top td { background-color: #F8CBAD; color: #000000; font-weight: bold; }
    .cell-sku { background-color: #FFFFFF; color: #1a1a1a; text-align: left; }
    .cell-val { background-color: #FFFFFF; color: #1a1a1a; }
    </style>
    """

    html = [css, '<div class="sop-container"><table class="sop-table">']
    html.append("<thead><tr>")
    html.append('<th colspan="3">Segment / Marque / SKU</th>')
    for annee in cols_annees:
        html.append(f"<th>{annee}</th>")
    html.append("</tr></thead><tbody>")

    html.append('<tr class="row-total">')
    html.append(f'<td colspan="3" style="text-align:center;">{label_total}</td>')
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
        html.append('<tr class="row-seg-top">')
        html.append(f'<td rowspan="{total_rows_seg}" class="cell-seg-side">{segment}</td>')
        html.append(f'<td colspan="2" style="text-align:center;">{segment}</td>')
        for annee in cols_annees:
            html.append(f"<td>{fmt_val(seg_data[annee].sum())}</td>")
        html.append("</tr>")
        for marque in marques:
            marq_data = seg_data[seg_data["Marque"] == marque]
            total_rows_marque = 1 + len(marq_data)
            html.append('<tr class="row-marque-top">')
            html.append(f'<td rowspan="{total_rows_marque}" class="cell-marque-side">{marque}</td>')
            html.append('<td style="text-align:left;"></td>')
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
        html.append('<tr class="row-eco-total">')
        html.append('<td colspan="3" style="text-align:center;">Évolution vs N-1 (%)</td>')
        for i, annee in enumerate(cols_annees):
            if i == 0:
                html.append("<td>-</td>")
            else:
                an_prev = cols_annees[i-1]
                v_curr = df_sub[annee].sum()
                v_prev = df_sub[an_prev].sum()
                taux = ((v_curr - v_prev) / v_prev * 100.0) if v_prev > 0 else 0
                signe = "+" if taux >= 0 else ""
                html.append(f"<td>{signe}{taux:.1f}%</td>")
        html.append("</tr>")

    html.append("</tbody></table></div>")
    return "".join(html)


def ecrire_feuille_fusionnee_excel(writer, sheet_title, df_source, cols_annees, afficher_evo=False):
    ws = writer.book.create_sheet(title=sheet_title)
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

    ws.cell(row=1, column=1, value="Segment / Marque / SKU")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=3)
    for col_i in range(1, 4):
        c = ws.cell(row=1, column=col_i); c.fill = fill_header; c.font = font_header; c.alignment = align_center; c.border = border_cell
    for idx_a, annee in enumerate(cols_annees, start=4):
        c = ws.cell(row=1, column=idx_a, value=annee); c.fill = fill_header; c.font = font_header; c.alignment = align_center; c.border = border_cell

    curr_row = 2
    ws.cell(row=curr_row, column=1, value="TOTAL ANNEE")
    ws.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=3)
    for col_i in range(1, 4):
        c = ws.cell(row=curr_row, column=col_i); c.fill = fill_total; c.font = font_total; c.alignment = align_center; c.border = border_cell
    for idx_a, annee in enumerate(cols_annees, start=4):
        c = ws.cell(row=curr_row, column=idx_a, value=float(df_source[annee].sum())); c.fill = fill_total; c.font = font_total; c.alignment = align_right; c.number_format = "#,##0"; c.border = border_cell
    curr_row += 1

    for segment in ORDRE_SEGMENTS:
        seg_data = df_source[df_source["Segment"] == segment]
        if len(seg_data) == 0: continue
        seg_start_row = curr_row
        ws.cell(row=curr_row, column=2, value=segment)
        ws.merge_cells(start_row=curr_row, start_column=2, end_row=curr_row, end_column=3)
        for col_i in range(2, 4):
            c = ws.cell(row=curr_row, column=col_i); c.fill = fill_seg; c.font = font_seg; c.alignment = align_center; c.border = border_cell
        for idx_a, annee in enumerate(cols_annees, start=4):
            c = ws.cell(row=curr_row, column=idx_a, value=float(seg_data[annee].sum())); c.fill = fill_seg; c.font = font_seg; c.alignment = align_right; c.number_format = "#,##0"; c.border = border_cell
        curr_row += 1
        for marque in seg_data["Marque"].unique():
            marq_data = seg_data[seg_data["Marque"] == marque]
            marq_start_row = curr_row
            c_sku_empty = ws.cell(row=curr_row, column=3, value=""); c_sku_empty.fill = fill_marque; c_sku_empty.border = border_cell
            for idx_a, annee in enumerate(cols_annees, start=4):
                c = ws.cell(row=curr_row, column=idx_a, value=float(marq_data[annee].sum())); c.fill = fill_marque; c.font = font_marque; c.alignment = align_right; c.number_format = "#,##0"; c.border = border_cell
            curr_row += 1
            for _, row in marq_data.iterrows():
                c_sku = ws.cell(row=curr_row, column=3, value=row["SKU"]); c_sku.font = font_sku; c_sku.alignment = align_left; c_sku.border = border_cell
                for idx_a, annee in enumerate(cols_annees, start=4):
                    val = float(row[annee]); c = ws.cell(row=curr_row, column=idx_a, value=val if val != 0 else None); c.font = font_sku; c.alignment = align_right; c.number_format = "#,##0"; c.border = border_cell
                curr_row += 1
            marq_end_row = curr_row - 1
            ws.cell(row=marq_start_row, column=2, value=marque)
            if marq_end_row > marq_start_row:
                ws.merge_cells(start_row=marq_start_row, start_column=2, end_row=marq_end_row, end_column=2)
            for r_i in range(marq_start_row, marq_end_row + 1):
                c = ws.cell(row=r_i, column=2); c.fill = fill_marque; c.font = font_marque; c.alignment = align_center; c.border = border_cell
        seg_end_row = curr_row - 1
        ws.cell(row=seg_start_row, column=1, value=segment)
        if seg_end_row > seg_start_row:
            ws.merge_cells(start_row=seg_start_row, start_column=1, end_row=seg_end_row, end_column=1)
        for r_i in range(seg_start_row, seg_end_row + 1):
            c = ws.cell(row=r_i, column=1); c.fill = fill_seg; c.font = font_seg; c.alignment = align_center; c.border = border_cell

    if afficher_evo:
        ws.cell(row=curr_row, column=1, value="Évolution (%)")
        ws.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=3)
        for col_i in range(1, 4):
            c = ws.cell(row=curr_row, column=col_i); c.fill = fill_total; c.font = font_total; c.alignment = align_center; c.border = border_cell
        for idx_a, annee in enumerate(cols_annees, start=4):
            if idx_a == 4:
                c = ws.cell(row=curr_row, column=idx_a, value="-")
            else:
                an_prev = cols_annees[idx_a - 4 - 1]
                v_curr = df_source[annee].sum()
                v_prev = df_source[an_prev].sum()
                taux = ((v_curr - v_prev) / v_prev) if v_prev > 0 else 0
                c = ws.cell(row=curr_row, column=idx_a, value=taux); c.number_format = "+0.0%;-0.0%;0.0%"
            c.fill = fill_total; c.font = font_total; c.alignment = align_right; c.border = border_cell
        curr_row += 1

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 36
    for col_letter in ["D", "E", "F", "G", "H", "I"]:
        ws.column_dimensions[col_letter].width = 18


# =====================================================
# NAVIGATION PRINCIPALE
# =====================================================
onglet_vol, onglet_ca = st.tabs([
    "📦 Simulation Volumes en hl (2026–2031)",
    "💰 Calcul Chiffre d'Affaires en Ar — CA (2026–2031)",
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
            mainTabList.style.position = "fixed";
            mainTabList.style.top = headerHeight + "px";
            mainTabList.style.left = "0px";
            mainTabList.style.right = "0px";
            mainTabList.style.width = "100%";
            mainTabList.style.backgroundColor = "#ffffff";
            mainTabList.style.zIndex = "1001";
            mainTabList.style.padding = "0.5rem 3rem 0.5rem 3rem";
            mainTabList.style.borderBottom = "1px solid #e0e0e0";
            mainTabList.style.boxShadow = "0 4px 6px -6px rgba(0, 0, 0, 0.1)";
            const tabsHeight = mainTabList.getBoundingClientRect().height || 44;
            if (mainBlock) {
                mainBlock.style.paddingTop = (headerHeight + tabsHeight + 20) + "px";
            }
        }
        figeHeaderEtOnglets();
        setTimeout(figeHeaderEtOnglets, 150);
        setTimeout(figeHeaderEtOnglets, 500);
        setTimeout(figeHeaderEtOnglets, 1000);
        window.parent.addEventListener("resize", figeHeaderEtOnglets);
        const observer = new MutationObserver(figeHeaderEtOnglets);
        if (parentDoc.body) {
            observer.observe(parentDoc.body, { childList: true, subtree: true });
        }
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
    df_obj = st.data_editor(
        st.session_state.objectifs,
        column_config={
            "Année": st.column_config.TextColumn("Année", disabled=True),
            "Volume": st.column_config.NumberColumn("Volume Objectif (hl)", format="%d", min_value=0, step=10000),
        },
        hide_index=True,
        use_container_width=True,
        key="editor_objectif",
    )
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

    tab_pm, tab_ps = st.tabs(["🏷️ Poids des Marques dans chaque Segment (%)", "📦 Poids des Articles (SKU) dans chaque Marque (%)"])
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
            st.warning(f"⚠️ La somme des poids des marques d'un segment doit faire 100 %. Écarts détectés : {', '.join(erreurs_pm)}")
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
                                    s = v.replace("%", "").replace(",", ".").strip()
                                    return float(s)
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
            st.warning(f"⚠️ La somme des poids des articles de **{marque_filtre_ps}** doit faire 100 %. Écarts : {', '.join(erreurs_ps)}")
        else:
            st.success(f"✅ Somme des poids des articles de **{marque_filtre_ps}** conforme (100 % sur les années actives).")

    df_detail = df_base[["Segment", "Marque", "SKU", "2026", "Contenance_hl"]].copy()
    pm_renamed = st.session_state.poids_marques.rename(columns={a: f"PM_{a}" for a in ANNEES})
    ps_renamed = st.session_state.poids_skus.rename(columns={a: f"PS_{a}" for a in ANNEES})
    df_detail = df_detail.merge(pm_renamed, on=["Segment", "Marque"], how="left")
    df_detail = df_detail.merge(ps_renamed, on=["Segment", "Marque", "SKU"], how="left")
    
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
        fig_bar.update_layout(yaxis_title="Volume (hl)", xaxis_title="Année")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_g2:
        fig_line = px.line(df_chart_seg_melt, x="Année", y="Volume", color="Segment", markers=True, title="Trajectoire de Croissance des Volumes (hl) par Segment")
        fig_line.update_layout(yaxis_title="Volume (hl)", xaxis_title="Année")
        st.plotly_chart(fig_line, use_container_width=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_mix_bar = px.bar(df_chart_seg_melt, x="Année", y="Mix (%)", color="Segment", title="Évolution du Mix Segment (%) par An (Base 100 %)", text=df_chart_seg_melt["Mix (%)"].apply(lambda x: f"{x:.1f}%"))
        fig_mix_bar.update_traces(textposition="inside")
        fig_mix_bar.update_layout(yaxis_title="Part de Mix (%)", xaxis_title="Année", yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_mix_bar, use_container_width=True)
    with col_m2:
        fig_mix_line = px.line(df_chart_seg_melt, x="Année", y="Mix (%)", color="Segment", markers=True, title="Évolution Comparative des Parts de Mix (%) par Segment", text=df_chart_seg_melt["Mix (%)"].apply(lambda x: f"{x:.1f}%"))
        fig_mix_line.update_traces(textposition="top center")
        fig_mix_line.update_layout(yaxis_title="Part de Mix (%)", xaxis_title="Année")
        st.plotly_chart(fig_mix_line, use_container_width=True)

    st.divider()
    st.subheader("4️⃣ Volumes Simulés Détaillés (hl)")
    segments_selectionnes_vol = st.multiselect("🔍 Filtrer par Segment (Volumes) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_vol_seg")
    if not segments_selectionnes_vol:
        st.info("Veuillez sélectionner au moins un segment dans le filtre ci-dessus.")
    else:
        st.markdown(generer_html_fusionne(df_detail, ANNEES_ALL, segments_selectionnes_vol, afficher_evo=False), unsafe_allow_html=True)


# #####################################################
# ONGLET 2 : CALCUL CHIFFRE D'AFFAIRES (CA EN AR)
# #####################################################
with onglet_ca:
    st.subheader("1️⃣ Gestion des Prix Unitaires par Col / Fût (2026 fixé — Upload & Édition 2027 → 2031)")
    st.caption("Formule appliquée : **CA (Ar) = (Volume en hl / Contenance unitaire en hl) × Prix Unitaire (Ar)**")

    col_p_reset, _ = st.columns([1, 4])
    with col_p_reset:
        if st.button("🔄 Réinitialiser les prix 2027–2031 (Base 2026)", key="btn_reset_prix"):
            del st.session_state["prix_skus"]
            st.rerun()

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
                            st.success(f"✅ **{nb_maj_p} article(s)** mis à jour sur : {', '.join(annees_dans_fichier)} (2026 conservé tel quel).")
                        else:
                            col_val_key = next((k for k in ["prix", "tarif", "pu", "price", "mix", "valeur"] if k in cols_norm_p), None)
                            if col_val_key is not None:
                                col_val_p = cols_norm_p[col_val_key]
                            elif len(df_p_up.columns) >= 2:
                                col_val_p = [c for c in df_p_up.columns if c != col_art_p][0]
                            else:
                                st.error("❌ Aucune colonne de prix trouvée dans le fichier.")
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
                            st.warning(f"⚠️ {len(non_trouves_p)} article(s) non reconnu(s) ignoré(s) : {', '.join(non_trouves_p[:10])}")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la lecture du fichier de prix : {e}")

    seg_filtre_prix = st.selectbox("🔍 Filtrer la grille des Prix par Segment :", options=["Tous les segments"] + ORDRE_SEGMENTS, key="sel_seg_prix")
    df_prix_view = st.session_state.prix_skus.copy()
    
    # --- NOUVEAU : Diagnostic visuel FOSA 2026 ---
    fosa_row = df_prix_view[df_prix_view["SKU"] == "FOSA 50 cl CAN"]
    vol_fosa = 3265
    conv_fosa = 0.005
    prix_fosa = fosa_row["2026"].values[0] if not fosa_row.empty else 3830
    ca_fosa = (vol_fosa / conv_fosa) * prix_fosa
    st.info(f"🧪 **Test de calcul (FOSA 2026) :** {vol_fosa:,.0f} hl / {conv_fosa} hl = {vol_fosa/conv_fosa:,.0f} unités. CA = {vol_fosa/conv_fosa:,.0f} × {prix_fosa:,.0f} Ar = **{ca_fosa:,.0f} Ar**")
    
    if seg_filtre_prix != "Tous les segments":
        df_prix_view = df_prix_view[df_prix_view["Segment"] == seg_filtre_prix]
    col_cfg_prix = {
        "Segment": st.column_config.TextColumn("Segment", disabled=True),
        "Marque": st.column_config.TextColumn("Marque", disabled=True),
        "SKU": st.column_config.TextColumn("Article (SKU)", disabled=True),
        "Contenance_hl": st.column_config.NumberColumn("Conv. hl", format="%.4f", disabled=True),
        "2026": st.column_config.NumberColumn("Prix 2026 (Fixé)", format="%.0f", disabled=True),
    }
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
    st.subheader("2️⃣ Synthèse & Évolution du Chiffre d'Affaires en Ar (2026–2031)")
    cols_kpi = st.columns(len(ANNEES_ALL))
    for i, annee in enumerate(ANNEES_ALL):
        ca_tot = df_ca[annee].sum()
        if i == 0:
            cols_kpi[i].metric(f"CA {annee}", fmt_val(ca_tot))
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
        fig_ca_bar = px.bar(df_chart_ca_melt, x="Année", y="Chiffre d'Affaires", color="Segment", title="Évolution du Chiffre d'Affaires (Ar) par Segment (Empilé)", text_auto=".3s")
        fig_ca_bar.update_layout(yaxis_title="Chiffre d'Affaires (Ar)", xaxis_title="Année")
        st.plotly_chart(fig_ca_bar, use_container_width=True)
    with col_ca2:
        fig_ca_mix = px.bar(df_chart_ca_melt, x="Année", y="Mix CA (%)", color="Segment", title="Évolution du Mix Valeur / CA (%) par An", text=df_chart_ca_melt["Mix CA (%)"].apply(lambda x: f"{x:.1f}%"))
        fig_ca_mix.update_traces(textposition="inside")
        fig_ca_mix.update_layout(yaxis_title="Part de CA (%)", xaxis_title="Année", yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_ca_mix, use_container_width=True)

    st.divider()
    st.subheader("📈 Taux d'Évolution Annuel du Chiffre d'Affaires (% vs N-1)")
    df_ca_global = pd.DataFrame([{"Périmètre": "CA Global", **{a: df_ca[a].sum() for a in ANNEES_ALL}}])
    df_evo_global = calculer_taux_evolution(df_ca_global, ["Périmètre"])
    df_evo_seg = calculer_taux_evolution(df_chart_ca, ["Segment"])
    col_evo1, col_evo2 = st.columns(2)
    with col_evo1:
        fig_evo_global = px.bar(df_evo_global, x="Année", y="Taux Évo (%)", text="Label (%)", title="Taux d'Évolution du CA Global (% / an)", color="Taux Évo (%)", color_continuous_scale=["#d9534f", "#f0ad4e", "#2e7d32"])
        fig_evo_global.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_evo_global.update_traces(textposition="outside")
        fig_evo_global.update_layout(yaxis_title="Croissance CA (%)", xaxis_title="Année", coloraxis_showscale=False)
        st.plotly_chart(fig_evo_global, use_container_width=True)
    with col_evo2:
        fig_evo_seg = px.line(df_evo_seg, x="Année", y="Taux Évo (%)", color="Segment", markers=True, text="Label (%)", title="Taux d'Évolution du CA par Segment (% / an)")
        fig_evo_seg.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_evo_seg.update_traces(textposition="top center")
        fig_evo_seg.update_layout(yaxis_title="Croissance CA (%)", xaxis_title="Année")
        st.plotly_chart(fig_evo_seg, use_container_width=True)

    st.divider()
    st.subheader("3️⃣ Chiffre d'Affaires Détaillé en Ar par Segment / Marque / SKU")
    segments_selectionnes_ca = st.multiselect("🔍 Filtrer par Segment (CA) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_ca_seg")
    if not segments_selectionnes_ca:
        st.info("Veuillez sélectionner au moins un segment dans le filtre ci-dessus.")
    else:
        st.markdown(generer_html_fusionne(df_ca, ANNEES_ALL, segments_selectionnes_ca, afficher_evo=True), unsafe_allow_html=True)


# =====================================================
# EXPORT EXCEL GLOBAL (VOLUMES + PRIX + CA)
# =====================================================
st.divider()
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_obj.to_excel(writer, sheet_name="1_Objectifs_Vol_hl", index=False)
    st.session_state.mix.to_excel(writer, sheet_name="2_Mix_Segment", index=False)
    st.session_state.poids_marques.to_excel(writer, sheet_name="3_Poids_Marques", index=False)
    st.session_state.poids_skus.to_excel(writer, sheet_name="4_Poids_SKU", index=False)
    ecrire_feuille_fusionnee_excel(writer, "5_Simulation_Volumes_hl", df_detail, ANNEES_ALL, afficher_evo=False)
    st.session_state.prix_skus.to_excel(writer, sheet_name="6_Prix_et_Conv_hl", index=False)
    ecrire_feuille_fusionnee_excel(writer, "7_Simulation_CA_Ar", df_ca, ANNEES_ALL, afficher_evo=True)
buffer.seek(0)
st.download_button(
    label="📥 Télécharger le fichier Excel complet — Volumes (hl) & CA (Ar) (.xlsx)",
    data=buffer,
    file_name="Simulation_SOP_Volumes_et_CA_2026_2031.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary",
)
