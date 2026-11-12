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
TXT.update({
 "D": "Vos chantiers sont soignés. Vos dossiers vous épuisent ?\n\nCercle Énergie est un réseau d'accompagnement pour les artisans : ce que vous n'arrivez pas à faire seul, on vous aide à le faire.\n\n✅ Dossiers CEE montés et suivis, démarches administratives\n✅ Formation, qualification RGE, tarifs préférentiels auprès de fournisseurs partenaires\n\n👉 Décrivez votre activité en 1 minute, un conseiller vous rappelle." + SUF,
 "E": "Vous posez des pompes à chaleur. On s'occupe du reste.\n\nVos dossiers de primes CEE montés et suivis, et des tarifs préférentiels auprès de fournisseurs partenaires : rejoignez le réseau Cercle Énergie.\n\n✅ Un seul interlocuteur pour vos dossiers CEE\n✅ Des conditions fournisseurs réservées aux membres du réseau\n\n👉 Décrivez votre activité en 1 minute, un conseiller vous rappelle." + SUF,
 "F": "Qualifié RGE, ou en train de le devenir ?\n\nCercle Énergie vous accompagne : qualification RGE, formation au fonctionnement des primes CEE, montage et suivi de vos dossiers.\n\n✅ Un accompagnement pour obtenir et conserver votre qualification\n✅ Les primes CEE expliquées simplement\n\n👉 Décrivez votre activité en 1 minute, un conseiller vous rappelle." + SUF,
})
VIS = [("R01", "RESEAU", "Petits artisans", "Petit artisan, pas artisan isolé.", "Le groupe d'artisans et la conseillère : l'image du réseau.", "D"),
       ("R02", "RESEAU", "Petits artisans", "Ce que vous n'arrivez pas à faire seul, on vous aide à le faire.", "La phrase directrice du réseau.", "D"),
       ("R03", "RESEAU", "Installateurs PAC", "Vous posez des pompes à chaleur. On s'occupe du reste.", "Cible : artisans pompe à chaleur.", "E"),
       ("R04", "RESEAU", "Tarifs fournisseurs", "Seul, vous négociez. En réseau, vous pesez.", "Cible : artisans pompe à chaleur. L'argument des tarifs fournisseurs.", "E"),
       ("R05", "RESEAU", "Artisans RGE", "Qualifié RGE ? Ne restez pas seul avec vos dossiers.", "Cible : artisans déjà qualifiés RGE.", "F"),
       ("R06", "RESEAU", "Formation aux CEE", "Les primes CEE, enfin expliquées simplement.", "L'argument de la formation.", "F"),
       ("R07", "RESEAU", "Qualification RGE", "La qualification RGE, sans y laisser vos week-ends.", "Cible : artisans qui préparent ou renouvellent leur qualification.", "F"),
       ("L01", "LOCAL", "Artisans locaux", "Vos chantiers sont soignés. Vos dossiers aussi, désormais.", "L'artisan local qui travaille bien : l'angle demandé par le dirigeant.", "D"),
       ("L02", "LOCAL", "Artisans locaux", "Excellent sur le chantier. Perdu dans les dossiers ?", "Même angle, version question.", "D"),
       ("L03", "LOCAL", "Artisans de proximité", "L'artisan du coin mérite un vrai réseau.", "Même angle, version affirmation.", "D"),
       ("H01", "AXE", "21 h · Après le chantier", "Encore vos dossiers CEE à 21 h ?", "L'artisan sur ses dossiers, le soir. L'accroche de l'axe.", "A"),
       ("H02", "AXE", "Installateurs · Artisans", "Vous posez. On gère le dossier CEE.", "L'artisan photographie son chantier pour nous le transmettre.", "B"),
       ("H03", "AXE", "Dossiers CEE", "Le dossier CEE, ce n'est pas votre métier.", "Les mains de l'artisan dans la paperasse.", "B"),
       ("H04", "AXE", "Fin de chantier", "Rentrez chez vous. On s'occupe du dossier.", "Fin de journée, l'artisan ferme son utilitaire.", "A"),
       ("H05", "AXE", "Mandataire CEE", "Un seul interlocuteur pour vos dossiers CEE.", "La conseillère qui vérifie le dossier.", "C"),
       ("H06", "MARQUE", "Aides CEE", "Moins de paperasse. Plus de chantiers.", "Variante directe du bénéfice.", "A"),
       ("H07", "MARQUE", "Mandataire CEE", "Vous réalisez les travaux. Nous gérons vos aides CEE.", "Le message clé de la marque.", "C")]
VID = [("R1", "R1-petit-artisan-pas-isole", "RESEAU", "Petits artisans", "Seul face à l'administratif ? Un réseau qui vous épaule.", "Du constat aux appuis du réseau : dossiers CEE, qualification RGE, tarifs fournisseurs. Musique seule. 20 s.", "D"),
       ("R2", "R2-six-appuis", "RESEAU", "Artisans RGE", "Artisan RGE ? Plus jamais seul. Six appuis, un seul réseau.", "Les six appuis un par un. Musique seule. 23 s.", "F"),
       ("R3", "R3-installateurs-pac", "RESEAU", "Installateurs PAC", "Vous posez des pompes à chaleur. Et les dossiers de primes ?", "Cible : artisans pompe à chaleur. Musique seule. 17 s.", "E"),
       ("R4", "R4-artisan-local", "LOCAL", "Artisans locaux", "Vos chantiers sont soignés. Les dossiers vous épuisent.", "L'artisan local qui travaille bien, bien entouré. Musique seule. 17 s.", "D"),
       ("N1", "N1-21h-le-chantier-est-fini", "AXE", "Film · voix off", "21 h. Le chantier est fini… mais pas votre journée.", "Film court avec voix off et sous-titres : l'artisan sur ses dossiers, il transmet le chantier, la conseillère prend le relais, il rentre chez lui. 23 s.", "A"),
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
    it.update(temoignage=False, reel=False, badge=False, serie2=it["product"] in ("RESEAU", "LOCAL"), titre_meta="Rejoignez le réseau Cercle Énergie" if it["product"] in ("RESEAU", "LOCAL") else "Vos dossiers CEE, on s'en occupe",
              lien=f"https://cercle-energie.vercel.app/devenir-partenaire?utm_source=facebook&utm_medium=cpc&utm_campaign=cercle-energie-partenaires&utm_content={it['id']}")
items.sort(key=lambda i: (not i["serie2"], i["kind"] != "video", i["id"]))
import re, subprocess, glob
from PIL import Image
FM = {"carre": "1x1", "portrait": "4x5", "story": "9x16"}
for d in ("img", "thumb", "vid"): os.makedirs(os.path.join(ROOT, d), exist_ok=True)
for f in sorted(glob.glob(os.path.join(ROOT, "../pub/visuels/*.jpg"))):
    m = re.match(r"([A-Z]\d\d)-.*-(carre|portrait|story)\.jpg", os.path.basename(f))
    if not m: continue
    n = f"{m.group(1)}-{FM[m.group(2)]}.jpg"; im = Image.open(f).convert("RGB")
    im.save(os.path.join(ROOT, "img", n), quality=90); im.thumbnail((720, 1280)); im.save(os.path.join(ROOT, "thumb", n), quality=82)
for it in items:
    if it["kind"] != "video": continue
    src = os.path.join(ROOT, "../pub/videos", it["file"] + "-story.mp4"); dst = os.path.join(ROOT, "vid", it["file"] + ".mp4")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-c:v", "libx264", "-crf", "24", "-vf", "scale=720:1280", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dst], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2.5", "-i", src, "-frames:v", "1", "-vf", "scale=540:960", "-q:v", "4", os.path.join(ROOT, "thumb", it["file"] + ".jpg")], check=True)
tpl = open(os.path.join(ROOT, "selection.tpl.html"), encoding="utf-8").read()
nv, nd = sum(1 for i in items if i["kind"] == "visuel"), sum(1 for i in items if i["kind"] == "video")
out = tpl.replace("/*DATA*/", json.dumps(items, ensure_ascii=False)).replace("__NTOTAL__", str(len(items))).replace("__NVIS__", str(nv)).replace("__NVID__", str(nd))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html :", len(items), "créations,", nv, "visuels,", nd, "vidéos")
