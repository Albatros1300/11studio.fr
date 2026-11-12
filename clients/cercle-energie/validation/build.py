#!/usr/bin/env python3
"""Génère index.html (page de validation des créas Cercle Énergie) à partir de selection.tpl.html."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SUF = "\n\nVersement des primes sous réserve de validation du dossier."
TXT = {
 "A": "Encore vos dossiers CEE à 21 h ?\n\nLe chantier est fini, pas votre journée. Transmettez-nous votre chantier : Cercle Énergie vérifie l'éligibilité, monte le dossier et suit la prime.\n\n✅ Un seul interlocuteur, de l'éligibilité au suivi des primes\n✅ Dossiers vérifiés avant transmission\n\n👉 Décrivez votre activité en 1 minute, un conseiller vous rappelle." + SUF,
 "B": "Vous posez. On gère le dossier CEE.\n\nÉligibilité, pièces, vérifications, suivi de la prime : c'est notre métier, pas le vôtre. Mandataire CEE, nous travaillons avec des délégataires pour financer vos chantiers.\n\n✅ Pompes à chaleur, chauffage, isolation, rénovation énergétique\n✅ Résidentiel, tertiaire, industrie, agricole\n\n👉 Décrivez votre activité en 1 minute, un conseiller vous rappelle." + SUF,
 "C": "Vous réalisez les travaux, Cercle Énergie vous accompagne dans la gestion et le financement de vos aides CEE.\n\nDe l'étude d'éligibilité à la constitution de vos dossiers, en passant par leur valorisation et le suivi des primes, nos équipes vous accompagnent à chaque étape.\n\n✅ Un seul interlocuteur pour tous vos dossiers CEE\n✅ Les meilleures conditions recherchées auprès de nos partenaires\n\n👉 Devenez partenaire : décrivez votre activité en 1 minute." + SUF,
}
VIS = [("H01", "AXE", "21 h · Après le chantier", "Encore vos dossiers CEE à 21 h ?", "L'artisan sur ses dossiers, le soir. L'accroche de l'axe.", "A"),
       ("H02", "AXE", "Installateurs · Artisans", "Vous posez. On gère le dossier CEE.", "L'artisan photographie son chantier pour nous le transmettre.", "B"),
       ("H03", "AXE", "Dossiers CEE", "Le dossier CEE, ce n'est pas votre métier.", "Les mains de l'artisan dans la paperasse.", "B"),
       ("H04", "AXE", "Fin de chantier", "Rentrez chez vous. On s'occupe du dossier.", "Fin de journée, l'artisan ferme son utilitaire.", "A"),
       ("H05", "AXE", "Mandataire CEE", "Un seul interlocuteur pour vos dossiers CEE.", "La conseillère qui vérifie le dossier.", "C"),
       ("H06", "MARQUE", "Aides CEE", "Moins de paperasse. Plus de chantiers.", "Variante directe du bénéfice.", "A"),
       ("H07", "MARQUE", "Mandataire CEE", "Vous réalisez les travaux. Nous gérons vos aides CEE.", "Le message clé de la marque.", "C")]
VID = [("N1", "N1-21h-le-chantier-est-fini", "AXE", "Film · voix off", "21 h. Le chantier est fini… mais pas votre journée.", "Film court avec voix off et sous-titres : l'artisan sur ses dossiers, il transmet le chantier, la conseillère prend le relais, il rentre chez lui. 23 s.", "A"),
       ("N2", "N2-qui-fait-quoi", "AXE", "Liste animée", "Dossier CEE : qui fait quoi ?", "Éligibilité, dossier, vérifications, suivi de la prime : « Nous ». Les travaux : « Vous ». Musique seule. 13 s.", "B"),
       ("E1", "E1-le-lien", "EXTRAIT", "Extrait du film", "Le lien entre vos chantiers et le financement CEE.", "Le schéma Installateurs ↔ Cercle Énergie ↔ Délégataires, avec la voix off. 11 s.", "C"),
       ("E2", "E2-nos-terrains", "EXTRAIT", "Extrait du film", "PAC, chauffage, isolation, tertiaire, industrie, agricole.", "Les secteurs d'intervention, avec la voix off. 11 s.", "B"),
       ("E3", "E3-cinq-services", "EXTRAIT", "Extrait du film", "De l'éligibilité au suivi des primes.", "Les cinq services, avec la voix off. 10 s.", "C"),
       ("E4", "E4-message", "EXTRAIT", "Extrait du film", "Vous réalisez les travaux. Nous gérons vos aides CEE.", "Le message clé, avec la voix off. 9 s.", "C"),
       ("V1", "V1-vos-dossiers-cee", "MARQUE", "Vidéo de marque", "Vos dossiers CEE, on s'en occupe.", "Cinq plans de chantier et de bureau, textes à l'écran, musique seule. 17 s.", "B"),
       ("V2", "V2-moins-de-paperasse", "MARQUE", "Vidéo de marque", "Les CEE font gagner des chantiers. La paperasse vous les fait payer.", "Du problème à la solution, musique seule. 17 s.", "A"),
       ("V3", "V3-tous-vos-terrains", "MARQUE", "Vidéo de marque", "Résidentiel, tertiaire, industrie, agricole.", "Les quatre terrains, musique seule. 17 s.", "B")]
items = []
for code, file, prod, tag, title, sub, tx in VID:
    items.append(dict(id=code, kind="video", file=file, product=prod, tag=tag, title=title, sub=sub, texte=TXT[tx]))
for code, prod, tag, title, sub, tx in VIS:
    items.append(dict(id=code, kind="visuel", product=prod, tag=tag, title=title, sub=sub, texte=TXT[tx]))
for it in items:
    it.update(temoignage=False, reel=False, badge=False, serie2=it["product"] == "AXE", titre_meta="Vos dossiers CEE, on s'en occupe",
              lien=f"https://cercle-energie.vercel.app/devenir-partenaire?utm_source=facebook&utm_medium=cpc&utm_campaign=cercle-energie-partenaires&utm_content={it['id']}")
items.sort(key=lambda i: (not i["serie2"], i["kind"] != "video", i["id"]))
tpl = open(os.path.join(ROOT, "selection.tpl.html"), encoding="utf-8").read()
nv, nd = sum(1 for i in items if i["kind"] == "visuel"), sum(1 for i in items if i["kind"] == "video")
out = tpl.replace("/*DATA*/", json.dumps(items, ensure_ascii=False)).replace("__NTOTAL__", str(len(items))).replace("__NVIS__", str(nv)).replace("__NVID__", str(nd))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html :", len(items), "créations,", nv, "visuels,", nd, "vidéos")
