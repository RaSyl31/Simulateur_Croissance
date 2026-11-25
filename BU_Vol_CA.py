@st.cache_data
def charger_dispatch_depuis_fichier():
    fichiers_candidats = [
        "Vol par AG_5.xlsx",
        "Vol par AG_4.xlsx",
        "Vol par AG_3.xlsx",
        "Vol par AG_2.xlsx",
        "Vol par AG.xlsx",
    ]
    chemin_fichier = next((f for f in fichiers_candidats if os.path.exists(f)), None)

    if chemin_fichier is None:
        agences_fallback = [
            "01-Tanjombato", "11-Andranomahery", "09-Tamatave", "07-Majunga", "12-Antsirabe",
            "18-Ambanja", "04-Tulear", "08-Manakara", "03-Usine-Diego", "19-Sambava",
            "21-Nosy-Be", "05-Fianarantsoa", "24-Fort-Dauphin", "06-Ihosy", "23-Morondava",
        ]
        np.random.seed(42)
        rows = []
        for _, r in df_base.iterrows():
            if r["Base_2027"] == 0:
                continue
            p_ag = np.random.dirichlet(np.ones(len(agences_fallback)))
            p_m = np.random.dirichlet(np.ones(len(MOIS)))
            for i_a, ag in enumerate(agences_fallback):
                for i_m, m in enumerate(MOIS):
                    rows.append({
                        "Segment": r["Segment"], "Marque": r["Marque"], "Article": r["SKU"],
                        "Agence": ag, "Mois": m, "Poids_Dispatch": p_ag[i_a] * p_m[i_m],
                    })
        return agences_fallback, pd.DataFrame(rows)

    xls = pd.ExcelFile(chemin_fichier)
    feuille_cible = "Feuil2" if "Feuil2" in xls.sheet_names else xls.sheet_names[0]
    df_xl = pd.read_excel(chemin_fichier, sheet_name=feuille_cible)

    cols_requis = ["Année", "Segment", "Marque", "Article", "Agence", "Volume", "Mois", "Poids"]
    df_hl = df_xl[cols_requis].copy()
    df_hl["Agence_Norm"] = df_hl["Agence"].astype(str).str.strip()
    df_hl = df_hl[df_hl["Agence"].notna() & (df_hl["Agence_Norm"] != "0") & (df_hl["Agence_Norm"] != "")]

    df_hl["Volume_Num"] = pd.to_numeric(df_hl["Volume"], errors="coerce").fillna(0.0)
    df_hl["Poids_Num"] = pd.to_numeric(df_hl["Poids"], errors="coerce").fillna(0.0)
    tot_poids = df_hl["Poids_Num"].sum()
    df_hl["Poids_Norm"] = (df_hl["Poids_Num"] / tot_poids) if tot_poids > 0 else 0.0

    agences_liste = (
        df_hl.groupby("Agence_Norm", as_index=False)["Poids_Norm"]
        .sum()
        .sort_values("Poids_Norm", ascending=False)["Agence_Norm"]
        .tolist()
    )

    df_hl["Segment_Norm"] = df_hl["Segment"].astype(str).str.strip().map(SEG_MAP_XL).fillna(df_hl["Segment"].astype(str).str.strip())
    df_hl["Marque_Norm"] = df_hl["Marque"].astype(str).str.strip()
    df_hl["Article_Norm"] = df_hl["Article"].astype(str).str.strip()
    df_hl["Mois_Norm"] = pd.to_numeric(df_hl["Mois"], errors="coerce").fillna(1).astype(int).apply(lambda x: f"{x:02d}")

    grp_art = (
        df_hl.groupby(["Segment_Norm", "Marque_Norm", "Article_Norm", "Agence_Norm", "Mois_Norm"], as_index=False)["Poids_Norm"]
        .sum()
    )
    tot_art = grp_art.groupby(["Segment_Norm", "Marque_Norm", "Article_Norm"])["Poids_Norm"].transform("sum")
    grp_art["Poids_Art"] = np.where(tot_art > 0, grp_art["Poids_Norm"] / tot_art, 0.0)

    grp_glob = grp_art.groupby(["Agence_Norm", "Mois_Norm"], as_index=False)["Poids_Norm"].sum()
    tot_glob = grp_glob["Poids_Norm"].sum()
    grp_glob["Poids_Glob"] = np.where(tot_glob > 0, grp_glob["Poids_Norm"] / tot_glob, 1.0 / (len(agences_liste) * len(MOIS)))

    poids_art_map = {
        (r["Segment_Norm"], r["Marque_Norm"], r["Article_Norm"], r["Agence_Norm"], r["Mois_Norm"]): r["Poids_Art"]
        for _, r in grp_art.iterrows()
        if r["Poids_Art"] > 0
    }
    poids_sku_only_map = {}
    for (_, _, art, ag, m), p in poids_art_map.items():
        poids_sku_only_map[(art, ag, m)] = poids_sku_only_map.get((art, ag, m), 0.0) + p
    sku_sums = {}
    for (art, _, _), p in poids_sku_only_map.items():
        sku_sums[art] = sku_sums.get(art, 0.0) + p
    for k in list(poids_sku_only_map.keys()):
        s = sku_sums.get(k[0], 0.0)
        poids_sku_only_map[k] = poids_sku_only_map[k] / s if s > 0 else 0.0

    poids_glob_map = {(r["Agence_Norm"], r["Mois_Norm"]): r["Poids_Glob"] for _, r in grp_glob.iterrows()}

    rows_final = []
    for _, r in df_base.iterrows():
        seg = r["Segment"]
        marq = r["Marque"]
        sku = r["SKU"]
        has_exact = any(k[0] == seg and k[1] == marq and k[2] == sku for k in poids_art_map.keys())
        has_sku = any(k[0] == sku for k in poids_sku_only_map.keys())

        for ag in agences_liste:
            for m in MOIS:
                if has_exact:
                    w = poids_art_map.get((seg, marq, sku, ag, m), 0.0)
                elif has_sku:
                    w = poids_sku_only_map.get((sku, ag, m), 0.0)
                else:
                    w = poids_glob_map.get((ag, m), 0.0)
                rows_final.append({
                    "Segment": seg,
                    "Marque": marq,
                    "Article": sku,
                    "Agence": ag,
                    "Mois": m,
                    "Poids_Dispatch": w,
                })

    return agences_liste, pd.DataFrame(rows_final)
