#!/usr/bin/env python3
"""Génère index.html (page de validation des créas Cercle Énergie) à partir de selection.tpl.html."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SUF = "\n\nVersement des primes selon les conditions contractuelles et la validation des dossiers."
FIN = "\n\n👉 Décrivez votre activité en 1 minute, nous vous rappelons pour un premier échange."
TXT = {
 "G": "Vous installez. Nous vous accompagnons à chaque étape.\n\nCercle Énergie, mandataire CEE (Certificats d'Économies d'Énergie), est le partenaire des installateurs de pompes à chaleur, de chauffe-eau thermodynamiques et d'isolation : du premier contact au versement de la prime.\n\n✅ Des dossiers suivis, des règles expliquées\n✅ Un interlocuteur identifié, à chaque étape" + FIN + SUF,
 "T": "Moins de temps dans l'administratif, plus de temps sur vos chantiers.\n\nVos chantiers sont soignés. Les dossiers de primes, eux, vous prennent vos soirées. Cercle Énergie, mandataire CEE, les prépare, les contrôle et les suit avec vous.\n\n✅ Un partenaire qui parle le langage du terrain\n✅ Une visibilité sur l'avancement de vos dossiers" + FIN + SUF,
 "E": "Les bons équipements, les bons outils, le bon accompagnement.\n\nEn plus du suivi de vos dossiers CEE, Cercle Énergie vous accompagne dès la visite technique et vous donne un accès simplifié à des équipements de qualité, selon les accords et gammes disponibles.\n\n✅ Un seul cercle de services, du premier contact à la prime\n✅ Des dossiers suivis, des règles expliquées" + FIN + SUF,
}
VIS = [("C01", "BRIEF", "Installateurs · Chauffagistes", "Vous installez. Nous vous accompagnons à chaque étape.", "Accroche « Simplification » du brief.", "G"),
       ("C02", "BRIEF", "Mandataire CEE", "Des dossiers suivis, des règles expliquées, un partenaire à vos côtés.", "Accroche « Confiance » du brief.", "G"),
       ("C03", "BRIEF", "Le partenaire unique de vos projets", "Du premier contact au paiement de la prime, un seul cercle de services.", "Accroche « Offre globale » du brief, avec la mention des conditions.", "G"),
       ("C04", "BRIEF", "Sur le terrain", "Moins de temps dans l'administratif, plus de temps sur vos chantiers.", "Accroche « Terrain » du brief.", "T"),
       ("C05", "BRIEF", "Équipements · Outils", "Les bons équipements, les bons outils, le bon accompagnement.", "Accroche « Équipement » du brief. Aucune marque citée ni montrée.", "E"),
       ("C06", "BRIEF", "Pompes à chaleur", "Vous posez des pompes à chaleur. On vous accompagne sur le reste.", "Déclinaison pour le cœur de cible.", "G"),
       ("C07", "BRIEF", "Isolation", "Vous isolez. Nous vous accompagnons à chaque étape.", "Déclinaison pour les spécialistes de l'isolation.", "G"),
       ("L01", "LOCAL", "Artisans locaux", "Vos chantiers sont soignés. Vos dossiers le seront aussi.", "L'artisan local qui travaille bien : l'angle demandé par le dirigeant.", "T"),
       ("L02", "LOCAL", "Artisans locaux", "Excellent sur le chantier. Perdu dans les dossiers ?", "Même angle, version question.", "T"),
       ("L03", "LOCAL", "Artisans de proximité", "L'artisan du coin mérite un vrai partenaire.", "Même angle, version affirmation.", "T"),
       ("H01", "AXE", "21 h · Après le chantier", "Encore vos dossiers CEE à 21 h ?", "L'artisan sur ses dossiers, le soir.", "T"),
       ("H06", "AXE", "Aides CEE", "Moins de paperasse. Plus de chantiers.", "Variante courte de l'accroche « Terrain ».", "T")]
VID = [("C1", "C1-a-chaque-etape", "BRIEF", "Le parcours", "Vous installez. Huit étapes, un seul cercle de services.", "Le parcours de A à Z, deux étapes par plan. Musique seule. 20 s.", "G"),
       ("C2", "C2-installateurs-pac", "BRIEF", "Pompes à chaleur", "Vous posez des pompes à chaleur. Et les dossiers de primes ?", "Cœur de cible : chauffagistes. Musique seule. 17 s.", "E"),
       ("C3", "C3-artisan-local", "LOCAL", "Artisans locaux", "Vos chantiers sont soignés. Les dossiers vous épuisent.", "L'artisan local, bien accompagné. Musique seule. 14 s.", "T"),
       ("C4", "C4-moins-d-administratif", "BRIEF", "Sur le terrain", "Moins de temps dans l'administratif, plus de temps sur vos chantiers.", "Accroche « Terrain » du brief. Musique seule. 14 s.", "T"),
       ("N1", "N1-21h-le-chantier-est-fini", "AXE", "Film · voix off", "21 h. Le chantier est fini… mais pas votre journée.", "Film court avec voix off et sous-titres, réalisé avant le brief : à réécouter au regard du nouveau discours. 23 s.", "T")]
items = []
for code, file, prod, tag, title, sub, tx in VID:
    items.append(dict(id=code, kind="video", file=file, product=prod, tag=tag, title=title, sub=sub, texte=TXT[tx]))
for code, prod, tag, title, sub, tx in VIS:
    items.append(dict(id=code, kind="visuel", product=prod, tag=tag, title=title, sub=sub, texte=TXT[tx]))
for it in items:
    it.update(temoignage=False, reel=False, badge=False, serie2=it["product"] == "BRIEF", titre_meta="Cercle Énergie, le partenaire unique de vos projets",
              lien=f"https://cercle-energie.vercel.app/devenir-partenaire?utm_source=facebook&utm_medium=cpc&utm_campaign=cercle-energie-installateurs&utm_content={it['id']}")
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
