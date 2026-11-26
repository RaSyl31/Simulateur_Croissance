import io
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

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

SEGMENT_REAL_MAP = {
    "1-BIERES": "BIERES",
    "BIERES": "BIERES",
    "BIERE": "BIERES",
    "BI": "BIERES",
    "2-BG": "BG",
    "BG": "BG",
    "3-ENERGY": "Energy",
    "ENERGY": "Energy",
    "4-EAUX": "EAUX",
    "EAUX": "EAUX",
    "EAU": "EAUX",
    "5-ALCOMIX": "Alcomix",
    "ALCOMIX": "Alcomix",
}

COULEURS_SEGMENTS = {
    "Alcomix": "#C00000",
    "BG": "#1F4E78",
    "BIERES": "#D97706",
    "EAUX": "#0284C7",
    "Energy": "#15803D",
}

MOIS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
MOIS_FR_MAP = {
    "janvier": "01", "janv": "01", "jan": "01", "1": "01", "01": "01",
    "février": "02", "fevrier": "02", "févr": "02", "fevr": "02", "fév": "02", "fev": "02", "2": "02", "02": "02",
    "mars": "03", "mar": "03", "3": "03", "03": "03",
    "avril": "04", "avr": "04", "4": "04", "04": "04",
    "mai": "05", "5": "05", "05": "05",
    "juin": "06", "jun": "06", "6": "06", "06": "06",
    "juillet": "07", "juil": "07", "jul": "07", "7": "07", "07": "07",
    "août": "08", "aout": "08", "aoû": "08", "aou": "08", "8": "08", "08": "08",
    "septembre": "09", "sept": "09", "sep": "09", "9": "09", "09": "09",
    "octobre": "10", "oct": "10", "10": "10",
    "novembre": "11", "nov": "11", "11": "11",
    "décembre": "12", "decembre": "12", "déc": "12", "dec": "12", "12": "12",
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
# DISPATCH PAR AGENCE & SAISONNALITÉ MENSUELLE
# =====================================================
def _to_float_safe(v):
    if pd.isna(v):
        return np.nan
    if isinstance(v, (int, float, np.number)):
        return float(v)
    s = str(v).replace(" ", "").replace("\u202f", "").replace(",", ".").strip()
    if s == "" or s.lower() in {"ventehldirect", "total", "agences", "segments", "marque", "moisannée"}:
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan

def _to_float(v):
    val = _to_float_safe(v)
    return 0.0 if pd.isna(val) else val

def _detecter_colonnes_mois(columns):
    mapping = {}
    for col in columns:
        key = str(col).strip().lower()
        if key in MOIS_FR_MAP:
            mapping[col] = MOIS_FR_MAP[key]
        else:
            prefix = key.split()[0].rstrip(".")
            if prefix in MOIS_FR_MAP:
                mapping[col] = MOIS_FR_MAP[prefix]
    return mapping

def _normaliser_segment(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s in SEGMENT_REAL_MAP:
        return SEGMENT_REAL_MAP[s]
    s_up = s.upper()
    if s_up in SEGMENT_REAL_MAP:
        return SEGMENT_REAL_MAP[s_up]
    for k, v in SEGMENT_REAL_MAP.items():
        if s_up.endswith("-" + k.upper()) or k.upper() in s_up:
            return v
    return None

def _extraire_mois_code(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    m = pd.Series([s]).str.extract(r"^(\d{1,2})\b")[0].iloc[0]
    if pd.notna(m):
        code = f"{int(m):02d}"
        if code in MOIS:
            return code
    if s in MOIS_FR_MAP:
        return MOIS_FR_MAP[s]
    prefix = s.split()[0].rstrip(".")
    return MOIS_FR_MAP.get(prefix)

def charger_ventes_realisees(uploaded_file):
    """Charge et normalise un fichier Excel/CSV de ventes réalisées (avec hiérarchie Mois année / Segments / Marque / Agences)."""
    if uploaded_file.name.lower().endswith(".csv"):
        try:
            df_raw = pd.read_csv(uploaded_file, sep=None, engine="python")
        except Exception:
            uploaded_file.seek(0)
            df_raw = pd.read_csv(uploaded_file, sep=";")
    else:
        xls = pd.ExcelFile(uploaded_file)
        feuille = "Export" if "Export" in xls.sheet_names else xls.sheet_names[0]
        df_raw = pd.read_excel(uploaded_file, sheet_name=feuille)

    cols_lower = {str(c).strip().lower(): c for c in df_raw.columns}

    # Format hiérarchique type Export ('Total genéral' = Mois année, 'Unnamed: 1' = Segments, 'Unnamed: 2' = Marque, 'Unnamed: 3' = Agences)
    if "total genéral" in cols_lower and "unnamed: 1" in cols_lower and "unnamed: 3" in cols_lower:
        c_ma = cols_lower["total genéral"]
        c_seg = cols_lower["unnamed: 1"]
        c_marq = cols_lower.get("unnamed: 2")
        c_ag = cols_lower["unnamed: 3"]
        c_vol = cols_lower.get("toutes agences") or cols_lower.get("total")
        if c_vol is None:
            raise ValueError("Colonne de volume ('Toutes agences' ou 'Total') introuvable.")

        df_sub = df_raw.copy()
        df_sub["Mois"] = df_sub[c_ma].apply(_extraire_mois_code)
        df_sub["Segment"] = df_sub[c_seg].apply(_normaliser_segment)
        df_sub["Marque_Raw"] = df_sub[c_marq].astype(str).str.strip() if c_marq else ""
        df_sub["Agence"] = df_sub[c_ag].astype(str).str.strip()
        df_sub["Vol_Real"] = df_sub[c_vol].apply(_to_float_safe)

        df_clean = df_sub[
            df_sub["Mois"].isin(MOIS)
            & df_sub["Segment"].isin(ORDRE_SEGMENTS)
            & df_sub["Agence"].str.contains("-", na=False)
            & (~df_sub["Marque_Raw"].str.lower().isin({"total", "nan", "none", ""}))
            & df_sub["Vol_Real"].notna()
        ].copy()

        if df_clean.empty:
            raise ValueError("Aucune ligne d'agence valide détectée dans le fichier.")

        return df_clean.groupby(["Mois", "Segment", "Agence"], as_index=False)["Vol_Real"].sum()

    # Format hiérarchique 3 niveaux sans colonne marque ('Total genéral', 'Unnamed: 1', 'Unnamed: 2')
    if "total genéral" in cols_lower and "unnamed: 1" in cols_lower and "unnamed: 2" in cols_lower:
        c_ma = cols_lower["total genéral"]
        c_seg = cols_lower["unnamed: 1"]
        c_ag = cols_lower["unnamed: 2"]
        c_vol = cols_lower.get("toutes agences") or cols_lower.get("total")
        if c_vol is None:
            raise ValueError("Colonne de volume introuvable.")

        df_sub = df_raw.copy()
        df_sub["Mois"] = df_sub[c_ma].apply(_extraire_mois_code)
        df_sub["Segment"] = df_sub[c_seg].apply(_normaliser_segment)
        df_sub["Agence"] = df_sub[c_ag].astype(str).str.strip()
        df_sub["Vol_Real"] = df_sub[c_vol].apply(_to_float_safe)

        df_clean = df_sub[
            df_sub["Mois"].isin(MOIS)
            & df_sub["Segment"].isin(ORDRE_SEGMENTS)
            & df_sub["Agence"].str.contains("-", na=False)
            & df_sub["Vol_Real"].notna()
        ].copy()

        if df_clean.empty:
            raise ValueError("Aucune ligne d'agence valide détectée dans le fichier.")

        return df_clean.groupby(["Mois", "Segment", "Agence"], as_index=False)["Vol_Real"].sum()

    # Format tabulaire explicite (Mois, Segment, Agence, Volume)
    c_m = next((cols_lower[k] for k in ["mois", "mois année", "periode", "période"] if k in cols_lower), None)
    c_s = next((cols_lower[k] for k in ["segment", "segments"] if k in cols_lower), None)
    c_a = next((cols_lower[k] for k in ["agence", "agences"] if k in cols_lower), None)
    c_v = next((cols_lower[k] for k in ["volume", "vente", "vente hl direct", "réalisé", "realise", "valeur", "toutes agences"] if k in cols_lower), None)

    if c_m and c_s and c_a and c_v:
        df_sub = df_raw.copy()
        df_sub["Mois"] = df_sub[c_m].apply(_extraire_mois_code)
        df_sub["Segment"] = df_sub[c_s].apply(_normaliser_segment)
        df_sub["Agence"] = df_sub[c_a].astype(str).str.strip()
        df_sub["Vol_Real"] = df_sub[c_v].apply(_to_float_safe)
        df_clean = df_sub[
            df_sub["Mois"].isin(MOIS)
            & df_sub["Segment"].isin(ORDRE_SEGMENTS)
            & df_sub["Agence"].str.contains("-", na=False)
            & df_sub["Vol_Real"].notna()
        ].copy()
        if df_clean.empty:
            raise ValueError("Aucune ligne exploitable après filtrage.")
        return df_clean.groupby(["Mois", "Segment", "Agence"], as_index=False)["Vol_Real"].sum()

    raise ValueError(f"Format de colonnes non reconnu : {list(df_raw.columns)}")

def construire_dispatch_depuis_excel():
    candidats = [
        "Disp par AG_2.xlsx",
        "Disp par AG.xlsx",
        "Vol par AG_7.xlsx",
        "Vol par AG_6.xlsx",
        "Vol par AG_5.xlsx",
        "Vol par AG_4.xlsx",
        "Vol par AG_3.xlsx",
        "Vol par AG.xlsx",
    ]
    fichier_trouve = next((fn for fn in candidats if os.path.exists(fn)), None)

    if fichier_trouve is not None:
        xls = pd.ExcelFile(fichier_trouve)
        feuille = "Feuil2" if "Feuil2" in xls.sheet_names else xls.sheet_names[0]
        df_xl = pd.read_excel(fichier_trouve, sheet_name=feuille)

        cols_lower = {str(c).strip().lower(): c for c in df_xl.columns}
        col_art = cols_lower.get("article")
        col_ag = cols_lower.get("agence")
        if col_art is None or col_ag is None:
            raise ValueError(f"Colonnes 'Article' et 'Agence' requises dans {fichier_trouve}.")

        df_v = df_xl[
            df_xl[col_ag].notna()
            & df_xl[col_ag].astype(str).str.contains("-", na=False)
        ].copy()

        df_v["Article_Norm"] = df_v[col_art].astype(str).str.strip()
        df_v["Agence_Norm"] = df_v[col_ag].astype(str).str.strip()

        mois_cols_map = _detecter_colonnes_mois(df_v.columns)
        if mois_cols_map:
            raw_cols = list(mois_cols_map.keys())
            for c in raw_cols:
                df_v[c] = df_v[c].apply(_to_float)
            df_long = df_v.melt(
                id_vars=["Article_Norm", "Agence_Norm"],
                value_vars=raw_cols,
                var_name="Col_Mois",
                value_name="Vol_Mois",
            )
            df_long["Mois"] = df_long["Col_Mois"].map(mois_cols_map)
            df_long = df_long.groupby(["Article_Norm", "Agence_Norm", "Mois"], as_index=False)["Vol_Mois"].sum()
        elif "volume" in cols_lower and "mois" in cols_lower:
            col_vol = cols_lower["volume"]
            col_m = cols_lower["mois"]
            df_v["Vol_Num"] = df_v[col_vol].apply(_to_float)
            df_v["Mois"] = df_v[col_m].astype(str).str.strip().str.lower().map(lambda s: MOIS_FR_MAP.get(s, "01"))
            df_long = df_v.groupby(["Article_Norm", "Agence_Norm", "Mois"], as_index=False)["Vol_Num"].sum().rename(columns={"Vol_Num": "Vol_Mois"})
        else:
            raise ValueError(f"Aucune colonne mensuelle détectée dans {fichier_trouve}.")

        s_mois = df_long.groupby("Mois")["Vol_Mois"].sum().reindex(MOIS).fillna(0.0)
        poids_mois_map = (s_mois / s_mois.sum()).to_dict() if s_mois.sum() > 0 else {m: 1.0 / 12.0 for m in MOIS}

        df_art_ag = df_long.groupby(["Article_Norm", "Agence_Norm"], as_index=False)["Vol_Mois"].sum()
        art_tot = df_art_ag.groupby("Article_Norm", as_index=False)["Vol_Mois"].sum().rename(columns={"Vol_Mois": "Vol_Art"})
        df_art_ag = df_art_ag.merge(art_tot, on="Article_Norm", how="left")
        df_art_ag["Part_Ag"] = np.where(df_art_ag["Vol_Art"] > 0, df_art_ag["Vol_Mois"] / df_art_ag["Vol_Art"], 0.0)

        ag_ordre = (
            df_art_ag.groupby("Agence_Norm", as_index=False)["Vol_Mois"]
            .sum()
            .sort_values("Vol_Mois", ascending=False)["Agence_Norm"]
            .tolist()
        )
        part_ag_map = {(r["Article_Norm"], r["Agence_Norm"]): float(r["Part_Ag"]) for _, r in df_art_ag.iterrows()}
        ag_glob = df_art_ag.groupby("Agence_Norm")["Vol_Mois"].sum()
        ag_glob_map = (ag_glob / ag_glob.sum()).to_dict() if ag_glob.sum() > 0 else {}

        rows_final = []
        for _, r in df_base.iterrows():
            seg, marq, art = r["Segment"], r["Marque"], r["SKU"]
            somme_part_art = sum(part_ag_map.get((art, ag), 0.0) for ag in ag_ordre)
            for ag in ag_ordre:
                p_ag = part_ag_map.get((art, ag), 0.0) if somme_part_art > 0 else ag_glob_map.get(ag, 0.0)
                for m in MOIS:
                    rows_final.append({
                        "Segment": seg,
                        "Marque": marq,
                        "Article": art,
                        "Agence": ag,
                        "Mois": m,
                        "Poids_Dispatch": p_ag * float(poids_mois_map.get(m, 1.0 / 12.0)),
                    })

        return ag_ordre, pd.DataFrame(rows_final), f"Fichier Excel : {fichier_trouve}"

    poids_ag_init = {
        "01-Tanjombato": 0.19845707, "11-Andranomahery": 0.18959447,
        "09-Tamatave": 0.11506422, "07-Majunga": 0.07485790,
        "12-Antsirabe": 0.07011798, "18-Ambanja": 0.05089633,
        "04-Tulear": 0.04659311, "08-Manakara": 0.04615074,
        "03-Usine-Diego": 0.03955769, "19-Sambava": 0.03488484,
        "21-Nosy-Be": 0.03263303, "05-Fianarantsoa": 0.03164114,
        "24-Fort-Dauphin": 0.02726957, "06-Ihosy": 0.02129984,
        "23-Morondava": 0.02098209,
    }
    saison_init = np.array([
        294936.69, 264148.77, 364258.80, 339354.06, 362445.88, 445053.03,
        349151.73, 417918.00, 385069.91, 404413.73, 488013.95, 485235.44,
    ])
    saison_init = saison_init / saison_init.sum()
    agences_liste = list(poids_ag_init.keys())
    rows_final = []
    for _, r in df_base.iterrows():
        for ag in agences_liste:
            for idx_m, m in enumerate(MOIS):
                rows_final.append({
                    "Segment": r["Segment"],
                    "Marque": r["Marque"],
                    "Article": r["SKU"],
                    "Agence": ag,
                    "Mois": m,
                    "Poids_Dispatch": poids_ag_init[ag] * float(saison_init[idx_m]),
                })
    return agences_liste, pd.DataFrame(rows_final), "Poids intégrés (Base 2027)"

if "dispatch_agences" not in st.session_state or "dispatch_df" not in st.session_state:
    ag_init, df_init, lbl_init = construire_dispatch_depuis_excel()
    st.session_state.dispatch_agences = ag_init
    st.session_state.dispatch_df = df_init
    st.session_state.source_poids_label = lbl_init

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

def styler_graphe(fig, titre, yaxis_titre, legend_titre="Segment"):
    fig.update_layout(
        template="plotly_white",
        title={"text": titre, "font": {"size": 15, "family": "Segoe UI, Tahoma, sans-serif"}},
        yaxis_title=yaxis_titre,
        legend_title_text=legend_titre,
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

def styler_pivot_dispatch(df_wide):
    """Ajoute la ligne 'Total par mois' en dernière ligne et stylise le tableau."""
    df_res = df_wide.copy()
    mois_cols = [c for c in MOIS if c in df_res.columns]
    total_mois = df_res[mois_cols].sum(axis=0)
    total_row = {c: total_mois[c] for c in mois_cols}
    if "Total Annuel" in df_res.columns:
        total_row["Total Annuel"] = total_mois.sum()
    df_res.loc["Total par mois"] = total_row

    def highlight_rows(row):
        if row.name == "Total par mois":
            styles = ["background-color: #FFF2CC; font-weight: bold; color: #111827; border-top: 2px solid #374151;"] * len(row)
            if "Total Annuel" in row.index:
                idx_tot = list(row.index).index("Total Annuel")
                styles[idx_tot] = "background-color: #FDE68A; font-weight: bold; color: #111827; border-top: 2px solid #374151;"
            return styles
        styles = [""] * len(row)
        if "Total Annuel" in row.index:
            idx_tot = list(row.index).index("Total Annuel")
            styles[idx_tot] = "background-color: #DBEAFE; font-weight: 600; color: #1E3A8A;"
        return styles

    return df_res.style.format("{:,.0f}").apply(highlight_rows, axis=1)

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
        for k in ["poids_marques", "poids_skus", "dispatch_agences", "dispatch_df", "source_poids_label"]:
            if k in st.session_state:
                del st.session_state[k]
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
    st.subheader("4️⃣ Graphiques Volumes & Mix (4 Graphes — 2026–2031)")
    segments_selectionnes_vol = st.multiselect("🔍 Filtrer par Segment (Volumes & Graphes) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_vol_seg")

    if not segments_selectionnes_vol:
        st.info("Veuillez sélectionner au moins un segment.")
    else:
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
                df_vol_seg, x="Année", y="Volume", color="Segment", markers=True,
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v1, "1. Évolution des Volumes par Segment", "Volume (hl)"), use_container_width=True)

        with col_v2:
            fig_v2 = px.bar(
                df_vol_seg, x="Année", y="Volume", color="Segment", barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v2, "2. Graphe Empilé des Volumes par Segment", "Volume (hl)"), use_container_width=True)

        col_v3, col_v4 = st.columns(2)
        with col_v3:
            fig_v3 = px.line(
                df_vol_seg, x="Année", y="Mix_Pct", color="Segment", markers=True,
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v3, "3. Évolution du Mix Volume (%) par Segment", "Mix (%)"), use_container_width=True)

        with col_v4:
            fig_v4 = px.bar(
                df_vol_seg, x="Année", y="Mix_Pct", color="Segment", barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_v4, "4. Graphe Empilé du Mix Volume (%)", "Part du volume (%)"), use_container_width=True)

        st.divider()
        st.subheader("5️⃣ Volumes Simulés Détaillés (hl)")
        st.markdown(generer_html_fusionne(df_detail, ANNEES_ALL, segments_selectionnes_vol, afficher_evo=False), unsafe_allow_html=True)


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
    st.subheader("3️⃣ Graphiques CA (3 Graphes — Évolution & Part en %)")
    segments_selectionnes_ca = st.multiselect("🔍 Filtrer par Segment (CA & Graphes) :", options=ORDRE_SEGMENTS, default=ORDRE_SEGMENTS, key="filter_ca_seg")

    if not segments_selectionnes_ca:
        st.info("Veuillez sélectionner au moins un segment.")
    else:
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
                df_ca_seg, x="Année", y="CA", color="Segment", markers=True,
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_c1, "1. Évolution du CA par Segment (Ar)", "CA (Ar)"), use_container_width=True)

        with col_c2:
            fig_c2 = px.bar(
                df_ca_seg, x="Année", y="CA", color="Segment", barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_c2, "2. Répartition Empilée du CA par Segment (Ar)", "CA (Ar)"), use_container_width=True)

        fig_c3 = px.bar(
            df_ca_seg, x="Année", y="Part_Pct", color="Segment", barmode="stack",
            color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
        )
        st.plotly_chart(styler_graphe(fig_c3, "3. Part du CA en (%) par Segment (2026–2031)", "Part du CA (%)"), use_container_width=True)

        st.divider()
        st.subheader("4️⃣ Chiffre d'Affaires Détaillé (Ar)")
        st.markdown(generer_html_fusionne(df_ca, ANNEES_ALL, segments_selectionnes_ca, afficher_evo=True), unsafe_allow_html=True)


# #####################################################
# ONGLET 3 : VOLUME PAR AGENCE (FILTRES INTERACTIFS)
# #####################################################
with onglet_agences:
    AGENCES = st.session_state.dispatch_agences
    df_dispatch_base = st.session_state.dispatch_df

    st.subheader(f"📍 Volumes par Agence & par Mois ({len(AGENCES)} Agences)")
    st.caption(f"Source active : **{st.session_state.source_poids_label}**")

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
        fig_ag = px.bar(
            df_ag_vol.groupby(["Agence", "Segment"], as_index=False)["Volume"].sum(),
            x="Agence", y="Volume", color="Segment", barmode="stack",
            color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS, "Agence": AGENCES},
        )
        st.plotly_chart(styler_graphe(fig_ag, f"Répartition des Volumes par Agence ({annee_agence})", "Volume (hl)"), use_container_width=True)

        agences_a_afficher = [agence_filtre] if agence_filtre != "Toutes les agences" else AGENCES
        st.markdown(generer_html_agences_par_mois(df_ag_vol, agences_a_afficher), unsafe_allow_html=True)


# #####################################################
# ONGLET 4 : DISPATCH AGENCE & MOIS (UPLOAD EN HAUT + EMPILEMENT PAR SEGMENT)
# #####################################################
with onglet_dispatch:
    AGENCES = st.session_state.dispatch_agences
    df_dispatch_base = st.session_state.dispatch_df

    st.subheader("🚚 Dispatch Détaillé (Agence & Mois)")
    st.caption(f"Source active : **{st.session_state.source_poids_label}** — Répartition mensuelle et géographique.")

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        annee_dispatch = st.selectbox("Sélectionnez l'année à ventiler :", ANNEES, index=0, key="disp_annee")
    with col_d2:
        filtre_seg_disp = st.selectbox("Filtrer par Segment :", ["Tous les segments"] + ORDRE_SEGMENTS, key="disp_seg")
    marques_disp_opts = (
        sorted(df_dispatch_base["Marque"].unique().tolist())
        if filtre_seg_disp == "Tous les segments"
        else sorted(df_dispatch_base[df_dispatch_base["Segment"] == filtre_seg_disp]["Marque"].unique().tolist())
    )
    with col_d3:
        filtre_marque_disp = st.selectbox("Filtrer par Marque :", ["Toutes les marques"] + marques_disp_opts, key="disp_marque")
    with col_d4:
        filtre_agence_disp = st.selectbox("Filtrer par Agence :", ["Toutes les agences"] + AGENCES, key="disp_agence")

    # Upload placé en haut de la section
    uploaded_real_file = st.file_uploader(
        "📤 Charger le fichier Excel / CSV des ventes réalisées (réalisé arrêté à un mois — Budget vs Réalisé & Reste à faire) :",
        type=["xlsx", "xls", "csv"],
        key="upload_ventes_realisees",
    )

    df_real_norm = None
    erreur_real = None
    if uploaded_real_file is not None:
        try:
            df_real_norm = charger_ventes_realisees(uploaded_real_file)
        except Exception as e:
            erreur_real = str(e)

    if erreur_real:
        st.error(f"❌ Erreur lors du traitement du fichier des ventes réalisées : {erreur_real}")

    df_disp_annee = df_dispatch_base.copy()
    df_disp_annee = df_disp_annee.merge(df_detail[["Segment", "Marque", "SKU", annee_dispatch]], left_on=["Segment", "Marque", "Article"], right_on=["Segment", "Marque", "SKU"], how="left")
    df_disp_annee = df_disp_annee.rename(columns={annee_dispatch: "Volume_Annuel"}).drop(columns=["SKU"])
    df_disp_annee["Volume_Dispatch"] = df_disp_annee["Volume_Annuel"] * df_disp_annee["Poids_Dispatch"]

    if filtre_seg_disp != "Tous les segments":
        df_disp_annee = df_disp_annee[df_disp_annee["Segment"] == filtre_seg_disp]
    if filtre_marque_disp != "Toutes les marques":
        df_disp_annee = df_disp_annee[df_disp_annee["Marque"] == filtre_marque_disp]
    if filtre_agence_disp != "Toutes les agences":
        df_disp_annee = df_disp_annee[df_disp_annee["Agence"] == filtre_agence_disp]

    if df_disp_annee.empty:
        st.warning("Aucune donnée disponible pour la combinaison de filtres sélectionnée.")
    else:
        if df_real_norm is not None:
            mode_vue_comp = st.radio(
                "Mode d'affichage du graphe (empilé par Segment) :",
                options=[
                    "Comparaison Budget vs Réalisé (Mois réalisés)",
                    "Budget vs Réalisé + Reste à faire (Mois réalisés)",
                    "Dispatch Budget Complet (12 mois)",
                ],
                horizontal=True,
                key="mode_vue_comp",
            )

            df_real_filt = df_real_norm.copy()
            if filtre_seg_disp != "Tous les segments":
                df_real_filt = df_real_filt[df_real_filt["Segment"] == filtre_seg_disp]
            if filtre_agence_disp != "Toutes les agences":
                df_real_filt = df_real_filt[df_real_filt["Agence"] == filtre_agence_disp]

            mois_presents = sorted([m for m in MOIS if m in set(df_real_filt["Mois"].unique())])
            mois_cibles = MOIS if mode_vue_comp.startswith("Dispatch Budget Complet") or not mois_presents else mois_presents

            segs_dispo = [s for s in ORDRE_SEGMENTS if filtre_seg_disp == "Tous les segments" or s == filtre_seg_disp]

            idx_grid = pd.MultiIndex.from_product([mois_cibles, segs_dispo], names=["Mois", "Segment"])
            df_grid = pd.DataFrame(index=idx_grid).reset_index()

            df_b_seg = (
                df_disp_annee[df_disp_annee["Mois"].isin(mois_cibles)]
                .groupby(["Mois", "Segment"], as_index=False)["Volume_Dispatch"]
                .sum()
                .rename(columns={"Volume_Dispatch": "Budget"})
            )
            df_r_seg = (
                df_real_filt[df_real_filt["Mois"].isin(mois_cibles)]
                .groupby(["Mois", "Segment"], as_index=False)["Vol_Real"]
                .sum()
                .rename(columns={"Vol_Real": "Réalisé"})
            )

            df_ms = df_grid.merge(df_b_seg, on=["Mois", "Segment"], how="left").merge(df_r_seg, on=["Mois", "Segment"], how="left").fillna(0.0)
            df_ms["Reste à faire"] = (df_ms["Budget"] - df_ms["Réalisé"]).clip(lower=0.0)
            df_ms["Écart (hl)"] = df_ms["Réalisé"] - df_ms["Budget"]

            if mode_vue_comp.startswith("Dispatch Budget Complet"):
                fig_stack = px.bar(
                    df_ms.sort_values(["Mois", "Segment"]),
                    x="Mois",
                    y="Budget",
                    color="Segment",
                    barmode="stack",
                    color_discrete_map=COULEURS_SEGMENTS,
                    category_orders={"Segment": ORDRE_SEGMENTS},
                )
                st.plotly_chart(
                    styler_graphe(fig_stack, f"Dispatch Budget Complet ({annee_dispatch}) — Empilé par Segment", "Volume (hl)"),
                    use_container_width=True,
                )
            elif mode_vue_comp.startswith("Budget vs Réalisé + Reste à faire"):
                df_rea_p = df_ms[["Mois", "Segment", "Réalisé"]].copy()
                df_rea_p["Colonne"] = "Réalisé"
                df_rea_p = df_rea_p.rename(columns={"Réalisé": "Volume"})

                df_rem_p = df_ms[["Mois", "Segment", "Reste à faire"]].copy()
                df_rem_p["Colonne"] = "Reste à faire"
                df_rem_p = df_rem_p.rename(columns={"Reste à faire": "Volume"})

                df_bud_p = df_ms[["Mois", "Segment", "Budget"]].copy()
                df_bud_p["Colonne"] = "Budget"
                df_bud_p = df_bud_p.rename(columns={"Budget": "Volume"})

                df_plot_3 = pd.concat([df_rea_p, df_rem_p, df_bud_p], ignore_index=True)
                fig_stack3 = px.bar(
                    df_plot_3,
                    x="Colonne",
                    y="Volume",
                    color="Segment",
                    facet_col="Mois",
                    barmode="stack",
                    color_discrete_map=COULEURS_SEGMENTS,
                    category_orders={"Segment": ORDRE_SEGMENTS, "Mois": mois_cibles, "Colonne": ["Réalisé", "Reste à faire", "Budget"]},
                )
                st.plotly_chart(
                    styler_graphe(fig_stack3, f"Budget vs Réalisé & Reste à faire ({annee_dispatch}) — Empilé par Segment", "Volume (hl)"),
                    use_container_width=True,
                )
            else:
                df_b_c = df_ms[["Mois", "Segment", "Budget"]].copy()
                df_b_c["Type_Barre"] = "Budget"
                df_b_c = df_b_c.rename(columns={"Budget": "Volume"})

                df_r_c = df_ms[["Mois", "Segment", "Réalisé"]].copy()
                df_r_c["Type_Barre"] = "Réalisé"
                df_r_c = df_r_c.rename(columns={"Réalisé": "Volume"})

                df_plot_2 = pd.concat([df_b_c, df_r_c], ignore_index=True)
                fig_stack2 = px.bar(
                    df_plot_2,
                    x="Type_Barre",
                    y="Volume",
                    color="Segment",
                    facet_col="Mois",
                    barmode="stack",
                    color_discrete_map=COULEURS_SEGMENTS,
                    category_orders={"Segment": ORDRE_SEGMENTS, "Mois": mois_cibles, "Type_Barre": ["Budget", "Réalisé"]},
                )
                st.plotly_chart(
                    styler_graphe(fig_stack2, f"Comparaison Budget ({annee_dispatch}) vs Réalisé — Empilé par Segment", "Volume (hl)"),
                    use_container_width=True,
                )

            # Synthèse mensuelle (Budget, Réalisé, Reste à faire, % Réalisé)
            df_sum_m = (
                df_ms.groupby("Mois", as_index=False)[["Budget", "Réalisé", "Reste à faire", "Écart (hl)"]]
                .sum()
            )
            df_sum_m["% Réalisé"] = np.where(df_sum_m["Budget"] > 0, (df_sum_m["Réalisé"] / df_sum_m["Budget"]) * 100.0, 0.0)

            tot_b = df_sum_m["Budget"].sum()
            tot_r = df_sum_m["Réalisé"].sum()
            tot_rem = max(tot_b - tot_r, 0.0)
            tot_pct_r = (tot_r / tot_b * 100.0) if tot_b > 0 else 0.0

            k1, k2, k3, k4 = st.columns(4)
            k1.metric(f"Budget ({annee_dispatch})", fmt_val(tot_b))
            k2.metric("Réalisé", fmt_val(tot_r), f"{tot_pct_r:.1f}% du budget")
            k3.metric("Reste à faire", fmt_val(tot_rem))
            k4.metric("Écart net (hl)", f"{(tot_r - tot_b):+,.0f}".replace(",", " "))

            df_sum_show = df_sum_m.copy()
            df_sum_show.loc[len(df_sum_show)] = {
                "Mois": "TOTAL",
                "Budget": tot_b,
                "Réalisé": tot_r,
                "Reste à faire": tot_rem,
                "Écart (hl)": tot_r - tot_b,
                "% Réalisé": tot_pct_r,
            }
            st.dataframe(
                df_sum_show.style.format({
                    "Budget": "{:,.0f}",
                    "Réalisé": "{:,.0f}",
                    "Reste à faire": "{:,.0f}",
                    "Écart (hl)": "{:+,.0f}",
                    "% Réalisé": "{:.1f}%",
                }),
                use_container_width=True,
                hide_index=True,
            )

            with st.expander("📋 Détail par Mois et par Segment (Budget, Réalisé, Reste à faire)", expanded=False):
                st.dataframe(
                    df_ms[["Mois", "Segment", "Budget", "Réalisé", "Reste à faire", "Écart (hl)"]].style.format({
                        "Budget": "{:,.0f}",
                        "Réalisé": "{:,.0f}",
                        "Reste à faire": "{:,.0f}",
                        "Écart (hl)": "{:+,.0f}",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            fig_disp_mois = px.bar(
                df_disp_annee.groupby(["Mois", "Segment"], as_index=False)["Volume_Dispatch"].sum().sort_values("Mois"),
                x="Mois", y="Volume_Dispatch", color="Segment", barmode="stack",
                color_discrete_map=COULEURS_SEGMENTS, category_orders={"Segment": ORDRE_SEGMENTS},
            )
            st.plotly_chart(styler_graphe(fig_disp_mois, f"Évolution Mensuelle du Dispatch ({annee_dispatch})", "Volume (hl)"), use_container_width=True)

        df_pivot = df_disp_annee.groupby(["Agence", "Mois"])["Volume_Dispatch"].sum().reset_index()
        agences_index = [filtre_agence_disp] if filtre_agence_disp != "Toutes les agences" else AGENCES
        df_pivot_wide = (
            df_pivot.pivot(index="Agence", columns="Mois", values="Volume_Dispatch")
            .reindex(index=agences_index, columns=MOIS, fill_value=0.0)
            .fillna(0.0)
        )
        df_pivot_wide["Total Annuel"] = df_pivot_wide.sum(axis=1)

        st.markdown(f"#### 📊 Volume dispatché par Agence et par Mois pour {annee_dispatch}")
        st.dataframe(styler_pivot_dispatch(df_pivot_wide), use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Téléchargement Global (Toutes années 2027–2031 + Synthèse Mensuelle)")

        frames_glob = []
        for a_item in ANNEES:
            df_a = df_dispatch_base.copy()
            df_a = df_a.merge(df_detail[["Segment", "Marque", "SKU", a_item]], left_on=["Segment", "Marque", "Article"], right_on=["Segment", "Marque", "SKU"], how="left")
            df_a = df_a.rename(columns={a_item: "Volume_Annuel"}).drop(columns=["SKU"])
            df_a["Valeur"] = df_a["Volume_Annuel"] * df_a["Poids_Dispatch"]
            df_a["Année"] = a_item
            df_a["AG"] = df_a["Agence"].str.extract(r'^(\d+)').fillna(0).astype(int)
            df_a["Attribut"] = df_a["Mois"] + " Hecto"
            df_a["Col/Hl"] = "Hecto"
            frames_glob.append(df_a[["Année", "Segment", "Marque", "Article", "Agence", "AG", "Attribut", "Valeur", "Col/Hl", "Mois"]])

        df_export_global = pd.concat(frames_glob, ignore_index=True)

        df_2027_mois = (
            df_export_global[df_export_global["Année"] == "2027"]
            .groupby(["Mois"], as_index=False)["Valeur"]
            .sum()
            .set_index("Mois")
            .reindex(MOIS, fill_value=0.0)
        )
        df_2027_mois.loc["TOTAL R0 2027"] = df_2027_mois["Valeur"].sum()

        buffer_global = io.BytesIO()
        with pd.ExcelWriter(buffer_global, engine="openpyxl") as writer_glob:
            df_export_global.to_excel(writer_glob, sheet_name="Dispatch_Global_2027_2031", index=False)
            df_2027_mois.to_excel(writer_glob, sheet_name="TOTAL_R0_2027", index=True)
            for ws_name, ws in writer_glob.sheets.items():
                for col in ws.columns:
                    max_len = max((len(str(cell.value)) for cell in col if cell.value is not None), default=10)
                    ws.column_dimensions[col[0].column_letter].width = max(max_len + 2, 12)

        buffer_global.seek(0)
        st.download_button(
            label="📥 Télécharger le Fichier Global (Dispatch 2027–2031 + TOTAL R0 2027)",
            data=buffer_global,
            file_name="Dispatch_Global_2027_2031.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
