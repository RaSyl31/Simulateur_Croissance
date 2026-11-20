import json
import os
import csv
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


# ============================================================
#  CATALOGUE : Segment → Marque → Liste d'articles
#  (Seuls les articles portent une contenance en cl / L / CAN / VER / PET / FUT)
# ============================================================
CATALOGUE: Dict[str, Dict[str, List[str]]] = {
    "Alcomix": {
        "Booster": [
            "Booster Appel-Mix 50CL VER",
            "Booster Tornado 50CL VER VER",
        ],
        "BOTA Fresh": [
            "BOTA Fresh 50 cl VER",
        ],
        "Racines": [
            "Racines 33 cl VER",
        ],
    },
    "BG": {
        "Caprice": [
            "Caprice Ananas 100 cl VER",
            "Caprice Ananas 150 cl PET",
            "Caprice Ananas 30 cl VER",
            "Caprice Bonbon Anglais 100 cl VER",
            "Caprice Bonbon Anglais 150 cl PET",
            "Caprice Bonbon Anglais 20L FUT",
            "Caprice Bonbon Anglais 30 cl VER",
            "Caprice Bonbon Anglais 33 cl CAN",
            "Caprice Bonbon Anglais 35 cl PET",
            "Caprice Bonbon Anglais 50 cl PET",
            "Caprice Grenadine 100 cl VER",
            "Caprice Grenadine 150 cl PET",
            "Caprice Grenadine 30 cl VER",
            "Caprice Grenadine 33 cl CAN",
            "Caprice Grenadine 35 cl PET",
            "Caprice Grenadine 50 cl PET",
            "Caprice Orange 100 cl VER",
            "Caprice Orange 150 cl PET",
            "Caprice Orange 20L FUT",
            "Caprice Orange 30 cl VER",
            "Caprice Orange 33 cl CAN",
            "Caprice Orange 35 cl PET",
            "Caprice Orange 50 cl PET",
            "Caprice Pomme 100 cl VER",
            "Caprice Pomme 150 cl PET",
            "Caprice Pomme 30 cl VER",
            "Caprice Pomme 50 cl PET",
        ],
        "Tonic": [
            "Tonic 100 cl VER",
            "Tonic 30 cl VER",
        ],
        "World Cola": [
            "World Cola 100cl VER",
            "World Cola 100cl WOCO VER",
            "World Cola 150cl PET",
            "World Cola 30cl VER",
            "World Cola 30cl WOCO VER",
            "World Cola 33 cl CAN",
            "World Cola 35cl PET",
            "World Cola 50cl PET",
            "World Cola 20L FUT",
        ],
    },
    "BIERES": {
        "Beaufort": [
            "Beaufort 33 CL CAN",
            "Beaufort 33CL VER",
        ],
        "FRESH": [
            "FRESH 33 cl CAN",
            "FRESH 33 cl EXPORT CAN",
            "THB Fresh 33 cl VER",
            "THB Fresh 65 cl VER",
        ],
        "Gold": [
            "Gold 8 50 cl CAN",
            "Gold 8 50 cl VER",
            "Gold Blanche 33cl VER",
            "Gold Blanche 50 cl CAN",
            "Gold Blanche 50 cl VER",
            "Gold Amigo 33cl VER",
            "Gold Blonde 50 cl CAN",
            "Gold Blonde 50 cl VER",
            "Gold Blonde 65 cl VER",
            "Gold Blanche 20L FUT",
        ],
        "Queen": [
            "Queen s 65 cl VER",
        ],
        "THB": [
            "THB Pilsener 33 cl VER",
            "THB Pilsener 50 cl CAN",
            "THB Pilsener 65 cl VER",
            "THB Pilsener 20L FUT",
            "THB Pilsener 30L FUT",
            "THB Speciale NOEL 33 cl VER",
            "THB Pilsener 20L Export FUT",
            "THB Blanche 20L Export FUT",
            "THB Pilsener 30L Export FUT",
            "THB 8 20L Export FUT",
        ],
    },
    "EAUX": {
        "Cristal": [
            "Cristal 100 cl VER",
            "Cristal 150 cl PET",
            "Cristal 30 cl VER",
            "Cristal 50 cl VER",
        ],
        "Cristalline": [
            "Cristalline 100 cl PET",
            "Cristalline 200 cl PET",
        ],
        "Eau vive": [
            "Eau vive 150 cl PET",
            "Eau vive 50 cl PET",
            "Eau vive 50 cl VER",
        ],
    },
    "Energy": {
        "FOSA": [
            "FOSA 50 cl CAN",
        ],
        "XXL": [
            "XXL 30cl BOB VER",
            "XXL 30cl VER",
            "XXL 33 cl CAN",
            "XXL 35cl PET",
        ],
    },
}


# ============================================================
#  MODELE
# ============================================================
@dataclass
class LigneBudget:
    segment: str
    marque: str
    article: str
    mois: str              # "YYYY-MM"
    volume: float          # quantité (unités/caisses)
    prix_unitaire: float   # prix unitaire

    @property
    def ca(self) -> float:
        return round(self.volume * self.prix_unitaire, 2)


# ============================================================
#  GESTIONNAIRE
# ============================================================
class BudgetAlcomix:
    def __init__(self, fichier: str = "budget_alcomix.json"):
        self.fichier = fichier
        self.lignes: List[LigneBudget] = []
        self.charger()

    # ----- PERSISTANCE -----
    def charger(self):
        if os.path.exists(self.fichier):
            try:
                with open(self.fichier, "r", encoding="utf-8") as f:
                    self.lignes = [LigneBudget(**d) for d in json.load(f)]
                print(f"✅ {len(self.lignes)} ligne(s) chargée(s)")
            except Exception as e:
                print(f"⚠️ Erreur de chargement : {e}")

    def sauvegarder(self):
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump([asdict(l) for l in self.lignes], f, indent=2, ensure_ascii=False)

    # ----- CATALOGUE -----
    @staticmethod
    def segments() -> List[str]:
        return list(CATALOGUE.keys())

    @staticmethod
    def marques(segment: str) -> List[str]:
        return list(CATALOGUE.get(segment, {}).keys())

    @staticmethod
    def articles(segment: str, marque: str) -> List[str]:
        return CATALOGUE.get(segment, {}).get(marque, [])

    @staticmethod
    def localiser(article: str) -> Optional[tuple]:
        for seg, marques in CATALOGUE.items():
            for marque, arts in marques.items():
                if article in arts:
                    return seg, marque
        return None

    # ----- CRUD -----
    def ajouter(self, article: str, mois: str, volume: float, prix_unitaire: float) -> bool:
        if not self._valider_mois(mois):
            print("❌ Mois invalide (attendu YYYY-MM)")
            return False
        loc = self.localiser(article)
        if not loc:
            print(f"❌ Article inconnu : {article}")
            return False
        seg, marque = loc
        ligne = LigneBudget(seg, marque, article, mois, volume, prix_unitaire)
        self.lignes.append(ligne)
        self.sauvegarder()
        print(f"✅ Ajouté : {article} | {mois} | CA = {ligne.ca:,.2f} €")
        return True

    def supprimer(self, index: int):
        if 0 <= index < len(self.lignes):
            l = self.lignes.pop(index)
            self.sauvegarder()
            print(f"🗑️ Supprimé : {l.article} ({l.mois})")

    # ----- AFFICHAGE -----
    def afficher(self, filtre_segment: Optional[str] = None,
                 filtre_marque: Optional[str] = None,
                 filtre_mois: Optional[str] = None):
        lignes = self.lignes
        if filtre_segment:
            lignes = [l for l in lignes if l.segment == filtre_segment]
        if filtre_marque:
            lignes = [l for l in lignes if l.marque == filtre_marque]
        if filtre_mois:
            lignes = [l for l in lignes if l.mois == filtre_mois]

        if not lignes:
            print("📭 Aucune ligne")
            return

        print("\n" + "=" * 112)
        print(f"{'#':<3} {'Segment':<9} {'Marque':<10} {'Article':<38} "
              f"{'Mois':<9} {'Volume':>10} {'PU':>9} {'CA':>14}")
        print("=" * 112)
        for i, l in enumerate(lignes):
            print(f"{i:<3} {l.segment:<9} {l.marque:<10} {l.article[:37]:<38} "
                  f"{l.mois:<9} {l.volume:>10,.0f} {l.prix_unitaire:>9,.2f} {l.ca:>14,.2f}")
        print("=" * 112)
        print(f"{'TOTAL':<72} {sum(l.volume for l in lignes):>10,.0f} "
              f"{'':<9} {sum(l.ca for l in lignes):>14,.2f}")
        print("=" * 112 + "\n")

    # ----- AGREGATIONS -----
    def total_volume(self) -> float:
        return sum(l.volume for l in self.lignes)

    def total_ca(self) -> float:
        return round(sum(l.ca for l in self.lignes), 2)

    def ca_par(self, attr: str) -> Dict[str, Dict[str, float]]:
        res = {}
        for l in self.lignes:
            k = getattr(l, attr)
            res.setdefault(k, {"volume": 0.0, "ca": 0.0})
            res[k]["volume"] += l.volume
            res[k]["ca"] += l.ca
        return dict(sorted(res.items()))

    def ca_par_segment(self): return self.ca_par("segment")
    def ca_par_marque(self):  return self.ca_par("marque")
    def ca_par_article(self): return self.ca_par("article")
    def ca_par_mois(self):    return self.ca_par("mois")

    # ----- EXPORT CSV -----
    def exporter_csv(self, chemin: str = "budget_alcomix.csv"):
        with open(chemin, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Segment", "Marque", "Article", "Mois",
                        "Volume", "Prix Unitaire", "CA"])
            for l in self.lignes:
                w.writerow([l.segment, l.marque, l.article, l.mois,
                            l.volume, l.prix_unitaire, l.ca])
        print(f"📄 Exporté : {chemin}")

    # ----- UTILS -----
    @staticmethod
    def _valider_mois(mois: str) -> bool:
        try:
            datetime.strptime(mois, "%Y-%m")
            return True
        except ValueError:
            return False


# ============================================================
#  MENU INTERACTIF
# ============================================================
def menu():
    bm = BudgetAlcomix()

    while True:
        print("\n" + "=" * 60)
        print("  🍹  BUDGET ALCOMIX  -  Volume & CA")
        print("=" * 60)
        print("  1. Ajouter une ligne")
        print("  2. Afficher tout")
        print("  3. Filtrer par segment")
        print("  4. Filtrer par mois")
        print("  5. Synthèse par segment")
        print("  6. Synthèse par marque")
        print("  7. Synthèse par mois")
        print("  8. Top 10 articles (CA)")
        print("  9. Supprimer une ligne")
        print(" 10. Exporter en CSV")
        print(" 11. Parcourir le catalogue")
        print("  0. Quitter")
        print("=" * 60)

        choix = input("👉 Choix : ").strip()

        if choix == "1":
            print("\n📚 Segments :", bm.segments())
            seg = input("Segment : ").strip()
            if seg not in bm.segments():
                print("❌ Segment inconnu"); continue

            print("📚 Marques :", bm.marques(seg))
            marque = input("Marque : ").strip()
            arts = bm.articles(seg, marque)
            if not arts:
                print("❌ Marque inconnue"); continue

            print("📚 Articles :")
            for i, a in enumerate(arts):
                print(f"   {i}. {a}")
            try:
                idx = int(input("N° article : "))
                article = arts[idx]
                mois = input("Mois (YYYY-MM) : ").strip()
                vol = float(input("Volume : "))
                pu = float(input("Prix unitaire (€) : "))
                bm.ajouter(article, mois, vol, pu)
            except (ValueError, IndexError):
                print("❌ Saisie invalide")

        elif choix == "2":
            bm.afficher()

        elif choix == "3":
            seg = input("Segment : ").strip()
            bm.afficher(filtre_segment=seg)

        elif choix == "4":
            mois = input("Mois (YYYY-MM) : ").strip()
            bm.afficher(filtre_mois=mois)

        elif choix in ("5", "6", "7"):
            titre = {"5": "SEGMENT", "6": "MARQUE", "7": "MOIS"}[choix]
            data = {"5": bm.ca_par_segment, "6": bm.ca_par_marque, "7": bm.ca_par_mois}[choix]()
            print(f"\n📊 Synthèse par {titre}")
            print("-" * 62)
            for k, v in data.items():
                print(f"  {k:<20} Volume: {v['volume']:>10,.0f} | CA: {v['ca']:>14,.2f} €")
            print("-" * 62)
            print(f"  {'TOTAL':<20} Volume: {bm.total_volume():>10,.0f} | CA: {bm.total_ca():>14,.2f} €")

        elif choix == "8":
            top = sorted(bm.ca_par_article().items(), key=lambda x: x[1]["ca"], reverse=True)[:10]
            print("\n🏆 Top 10 articles (CA)")
            for i, (art, v) in enumerate(top, 1):
                print(f"  {i:>2}. {art:<42} {v['ca']:>14,.2f} €")

        elif choix == "9":
            bm.afficher()
            try:
                idx = int(input("N° ligne à supprimer : "))
                bm.supprimer(idx)
            except ValueError:
                print("❌ Saisie invalide")

        elif choix == "10":
            bm.exporter_csv()

        elif choix == "11":
            for seg, marques in CATALOGUE.items():
                print(f"\n🔹 {seg}")
                for marque, arts in marques.items():
                    print(f"   └─ {marque} ({len(arts)} article(s))")
                    for a in arts:
                        print(f"       • {a}")

        elif choix == "0":
            print("👋 À bientôt !")
            break
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    menu()
