#!/usr/bin/env python3
"""Génère la landing page statique Cercle Énergie (index.html).
Usage : python3 build.py"""
import pathlib

ROOT = pathlib.Path(__file__).parent
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NAV = [("#services", "Services"), ("#secteurs", "Secteurs"), ("#benefices", "Bénéfices"), ("#faq", "FAQ")]

STEPS = [
    ("Étude d’éligibilité", "Nous identifions les aides CEE mobilisables selon les travaux que vous envisagez.", ["Analyse du projet", "Aides mobilisables", "Retour clair avant engagement"]),
    ("Valorisation financière", "Nous recherchons les meilleures conditions de valorisation auprès de nos partenaires.", ["Mise en relation", "Meilleures conditions", "Proposition lisible"]),
    ("Gestion administrative", "Nous prenons en charge la constitution, la vérification et le suivi de vos dossiers.", ["Constitution", "Vérification des pièces", "Suivi"]),
    ("Accompagnement réglementaire", "Nous vérifions les exigences documentaires et les conditions du dispositif.", ["Exigences documentaires", "Conditions du dispositif", "Dossiers sécurisés"]),
    ("Suivi du financement", "Nous coordonnons avec les délégataires jusqu’au traitement du dossier et au versement des primes*.", ["Coordination délégataires", "Suivi du traitement", "Information à chaque avancée"]),
]
s2_html = "".join(
    f'<div class="s2" data-n="0{i+1}"><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>'
    for i, (t, d, li) in enumerate(STEPS))

MARQ = "".join(f"<span>{t}</span>" for t in ["Pompes à chaleur", "Chauffage", "Isolation", "Ventilation", "Rénovation énergétique", "Tertiaire", "Industrie", "Agricole"])
CMP = [("Aides", "À identifier vous-même, chantier par chantier", "Identifiées selon vos travaux"),
       ("Dossiers", "À constituer, vérifier et suivre en interne", "Constitués, vérifiés et suivis pour vous"),
       ("Exigences", "À maîtriser et contrôler seul", "Exigences documentaires contrôlées"),
       ("Financement", "Des acteurs à trouver et à coordonner", "Un partenaire unique, en lien avec les délégataires")]
cmp_html = "".join(f'<div class="cmp" style="--i:{i}"><small>{k}</small><p class="a">{a}</p><p class="b">{b}</p><i></i></div>' for i, (k, a, b) in enumerate(CMP))

PANELS = [("pompe-a-chaleur.jpg", "Pompes à chaleur", "Installateurs de pompes à chaleur et de systèmes thermodynamiques."),
          ("chauffage.jpg", "Chauffage", "Systèmes de chauffage, ventilation et équipements thermiques."),
          ("isolation-combles.jpg", "Isolation", "Entreprises spécialisées dans l’isolation des bâtiments."),
          ("renovation.jpg", "Rénovation énergétique", "Entreprises de rénovation énergétique et entreprises générales du bâtiment."),
          ("tertiaire.jpg", "Tertiaire", "Bureaux, commerces, établissements recevant du public."),
          ("industrie.jpg", "Industrie", "Sites de production, utilités et équipements thermiques."),
          ("agricole.jpg", "Agricole", "Exploitations, serres et bâtiments d’élevage.")]
panels_html = "".join(
    f'<article class="panel{" on" if i == 0 else ""}" tabindex="0"><img src="assets/img/{img}" alt="{t}" loading="lazy"><span class="no">0{i+1}</span><span class="lab">{t}</span><div class="in"><h3>{t}</h3><p>{d}</p></div></article>'
    for i, (img, t, d) in enumerate(PANELS))

B3 = [("portrait-dossier.jpg", "Simplifier", "Un interlocuteur unique pour toutes vos démarches CEE. Vous transmettez, nous montons le dossier."),
      ("portrait-conseillere.jpg", "Sécuriser", "Des dossiers vérifiés au regard des exigences documentaires et des conditions du dispositif."),
      ("portrait-artisan.jpg", "Valoriser", "Les meilleures conditions de valorisation recherchées auprès de nos partenaires.")]
b3_html = "".join(
    f'<article class="b3 rv" style="--d:{i*.1:.1f}s"><div class="ph"><img src="assets/img/{img}" alt="" loading="lazy"><span>0{i+1}</span></div><div class="tx"><h3>{t}</h3><p>{d}</p></div></article>'
    for i, (img, t, d) in enumerate(B3))

WHO = [("Réalisation des travaux", 1, 0, 0), ("Étude d’éligibilité", 0, 1, 0), ("Recherche de valorisation", 0, 1, 0),
       ("Constitution et vérification du dossier", 0, 1, 0), ("Suivi et coordination", 0, 1, 0), ("Financement des CEE", 0, 0, 1)]
dot = lambda v: '<span class="dot"></span>' if v else '<span class="dot o"></span>'
who_html = "".join(f"<tr><th scope='row'>{t}</th><td>{dot(a)}</td><td>{dot(b)}</td><td>{dot(c)}</td></tr>" for t, a, b, c in WHO)

FAQ = [("Que sont les Certificats d’Économies d’Énergie (CEE) ?", "C’est un dispositif national qui conduit les fournisseurs d’énergie à financer des travaux d’économies d’énergie. Pour vos clients, cela se traduit par des primes sur les travaux éligibles."),
       ("Quel est le rôle de Cercle Énergie ?", "Cercle Énergie est mandataire : nous faisons le lien entre les entreprises d’installation et les acteurs du financement des CEE, en simplifiant l’ensemble des démarches administratives."),
       ("Avec qui travaillez-vous ?", "Nous travaillons en collaboration avec des délégataires CEE, auprès desquels nous recherchons les meilleures conditions de valorisation."),
       ("À qui s’adresse l’accompagnement ?", "Aux artisans, installateurs, entreprises du bâtiment et professionnels de la rénovation énergétique, dans les secteurs résidentiel, tertiaire, industriel et agricole."),
       ("Le versement des primes est-il garanti ?", "Non : le traitement du dossier et le versement des primes interviennent sous réserve de validation. Notre travail consiste à constituer et vérifier des dossiers conformes aux exigences du dispositif.")]
faq_html = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

CHAIN = """<div class="chain">
      <div class="node rv"><div class="ic"><svg viewBox="0 0 24 24"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/></svg></div><h3>Installateurs &amp; artisans</h3><p>Vous réalisez les travaux chez vos clients.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node core rv" style="--d:.12s"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie"><span class="pill">Votre mandataire CEE</span><p>Nous montons, sécurisons et suivons vos dossiers.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node g rv" style="--d:.24s"><div class="ic"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="13" height="17" rx="2"/><path d="M7.5 8h6M7.5 11.5h6M7.5 15h3"/><circle cx="17.5" cy="17" r="4" fill="#5FA60E"/><path d="M19 15.8a2 2 0 1 0 0 2.4M15.6 16.5h2.4M15.6 17.6h2.4"/></svg></div><h3>Délégataires CEE</h3><p>Les acteurs du financement des Certificats d’Économies d’Énergie.</p></div>
    </div>"""

BODY = f"""<section class="hero2" id="accueil">
  <img class="bgv" src="assets/img/pac-installation.jpg" alt="Installateur posant une pompe à chaleur">
  <div class="shade"></div><div class="halo"></div><div class="halo b"></div>
  <div class="wrap">
    <span class="eyebrow">Mandataire CEE · Partenaire des professionnels</span>
    <h1 class="mega"><span class="ln" style="--i:0"><span>Vous réalisez</span></span><span class="ln" style="--i:1"><span>les travaux.</span></span><span class="ln lime" style="--i:2"><span>Nous gérons</span></span><span class="ln lime" style="--i:3"><span>vos aides CEE.</span></span></h1>
    <div class="hero2-foot">
      <div><p class="lead">Cercle Énergie accompagne les artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs Certificats d’Économies d’Énergie.</p>
      <div class="proof"><span>Un interlocuteur unique</span><span>Dossiers vérifiés</span><span>Suivi jusqu’au financement</span></div></div>
      <div class="hero-cta" style="margin:0"><a class="btn btn-primary btn-xl" href="#partenaire">Devenir partenaire {ARROW}</a><a class="btn btn-ghost btn-xl" href="#video">Voir la vidéo</a></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{MARQ}{MARQ}</div></div>

<section class="statement" id="constat">
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Le constat</span>
      <p class="fill" data-fill data-green="6">Les CEE font gagner des chantiers. La paperasse vous les fait payer. Nous reprenons la main sur vos dossiers.</p>
    </div>
    <div class="media rv"><img src="assets/img/paperasse.jpg" alt="Artisan débordé par les démarches administratives" loading="lazy"><span class="badge">Les aides CEE ne devraient pas vous coûter vos soirées.</span></div>
  </div>
</section>

<section class="tint" id="comparer">
  <div class="wrap center">
    <span class="eyebrow rv">Avant / après</span>
    <h2 class="rv">Qui porte vos dossiers CEE ?</h2>
    <div class="switch rv" id="switch" role="group" aria-label="Comparer"><span class="knob"></span><button type="button" data-v="sans" aria-pressed="true">Sans accompagnement</button><button type="button" data-v="avec" aria-pressed="false">Avec Cercle Énergie</button></div>
    <div class="compare rv" id="compare">{cmp_html}</div>
  </div>
</section>

<section id="cee">
  <div class="wrap center">
    <span class="eyebrow rv">Les CEE en 30 secondes</span>
    <h2 class="rv">Un dispositif simple sur le papier.<br>Nous le rendons simple sur le terrain.</h2>
    <div class="flow4 rv">
      <div class="f4"><h3>Les fournisseurs d’énergie financent</h3><p>Le dispositif les conduit à soutenir des travaux d’économies d’énergie, sous forme de primes.</p></div>
      <div class="f4"><h3>Les délégataires portent le financement</h3><p>Ce sont les acteurs avec lesquels les dossiers CEE sont valorisés.</p></div>
      <div class="f4 me"><h3>Cercle Énergie fait le lien</h3><p>Mandataire, nous étudions l’éligibilité, montons et suivons vos dossiers.</p></div>
      <div class="f4"><h3>Vous réalisez les travaux</h3><p>Vous restez sur vos chantiers ; votre client bénéficie de la prime*.</p></div>
    </div>
    <p class="note rv" style="margin-inline:auto">* Sous réserve de validation du dossier.</p>
  </div>
</section>

<section class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">Notre rôle</span>
    <h2 class="rv">Le lien entre vos chantiers<br>et le financement.</h2>
    <p class="lead rv">En tant que mandataire, Cercle Énergie travaille en collaboration avec des délégataires CEE pour accompagner les professionnels dans leurs projets.</p>
    {CHAIN}
  </div>
</section>

<section id="services">
  <div class="wrap svc2">
    <div class="stick">
      <span class="eyebrow rv">Nos services</span>
      <h2 class="rv">Cinq étapes.<br>Un seul interlocuteur.</h2>
      <div class="bigno" id="bigno" aria-hidden="true">01</div>
    </div>
    <div class="rail" id="rail"><span class="fillbar" id="fillbar"></span>{s2_html}
      <p class="note">* Sous réserve de validation du dossier.</p>
    </div>
  </div>
</section>

<section class="tint" id="roles">
  <div class="wrap">
    <span class="eyebrow rv">Répartition des rôles</span>
    <h2 class="rv">Vous, sur le chantier.<br>Nous, sur le dossier.</h2>
    <div class="table-scroll rv"><table class="who"><thead><tr><th scope="col">Étape</th><th scope="col">Vous</th><th scope="col">Cercle Énergie</th><th scope="col">Délégataire CEE</th></tr></thead><tbody>{who_html}</tbody></table></div>
  </div>
</section>

<section id="secteurs">
  <div class="wrap">
    <span class="eyebrow rv">Nos terrains</span>
    <h2 class="rv">Partout où il y a de l’énergie<br>à économiser.</h2>
    <p class="lead rv">Résidentiel, tertiaire, industriel ou agricole : nous accompagnons les professionnels de l’efficacité énergétique, quel que soit leur terrain.</p>
    <div class="panels rv" id="panels">{panels_html}</div>
  </div>
</section>

<section class="tint" id="benefices">
  <div class="wrap">
    <span class="eyebrow rv">Ce que vous y gagnez</span>
    <h2 class="rv">Simplifier. Sécuriser. Valoriser.</h2>
    <div class="trio3">{b3_html}</div>
  </div>
</section>

<section id="video" class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span>
    <h2 class="rv">Cercle Énergie en 72 secondes</h2>
    <div class="video-frame rv"><video controls preload="none" poster="assets/img/video-poster.jpg"><source src="assets/video/presentation.mp4" type="video/mp4">Votre navigateur ne peut pas lire cette vidéo.</video></div>
  </div>
</section>

<section id="faq">
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span>
    <h2 class="rv">L’essentiel à savoir</h2>
    <div class="faq" style="text-align:left">{faq_html}</div>
  </div>
</section>

<section class="join" id="partenaire">
  <div class="wrap form-grid">
    <div>
      <h2 class="rv">Devenez<br>partenaire.</h2>
      <p class="lead rv">Concentrez-vous sur vos chantiers et vos clients. Nous nous occupons de vos aides CEE.</p>
      <ol class="mini-steps rv">
        <li><b>Vous nous présentez votre activité</b>Métier, secteur, type de chantiers.</li>
        <li><b>Nous étudions vos projets</b>Nous identifions les aides CEE mobilisables sur vos travaux.</li>
        <li><b>Nous gérons vos dossiers</b>Constitution, vérification, coordination et suivi des primes*.</li>
      </ol>
      <p class="note rv">* Sous réserve de validation du dossier.</p>
    </div>
    <form class="lead-form rv" id="lead-form" novalidate>
      <h3 class="full">Parlons de vos chantiers</h3>
      <label>Société<input id="f-societe" name="societe" autocomplete="organization" required></label>
      <label>Nom et prénom<input id="f-nom" name="nom" autocomplete="name" required></label>
      <label>Téléphone<input id="f-tel" name="telephone" type="tel" autocomplete="tel" required></label>
      <label>E-mail<input id="f-email" name="email" type="email" autocomplete="email" required></label>
      <label>Votre activité<select id="f-activite" name="activite" required><option value="">Sélectionnez…</option><option>Pompes à chaleur</option><option>Chauffage</option><option>Isolation</option><option>Ventilation / équipements thermiques</option><option>Rénovation énergétique</option><option>Autre</option></select></label>
      <label>Secteur principal<select id="f-secteur" name="secteur"><option>Résidentiel</option><option>Tertiaire</option><option>Industriel</option><option>Agricole</option></select></label>
      <label class="full">Votre projet (facultatif)<textarea id="f-message" name="message" rows="3"></textarea></label>
      <label class="check full"><input id="f-ok" type="checkbox" name="consentement" required><span>J’accepte d’être recontacté par Cercle Énergie au sujet de ma demande.</span></label>
      <button class="btn btn-primary full" type="submit">Envoyer ma demande {ARROW}</button>
      <p class="form-ok" role="status" id="form-ok">Merci ! Votre demande a bien été prise en compte.<br><small>(Version de démonstration : le formulaire n’est pas encore relié à une messagerie.)</small></p>
    </form>
  </div>
</section>"""

links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
HEADER = f"""<a class="skip" href="#contenu">Aller au contenu</a>
<div class="progress" id="progress"></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#accueil" aria-label="Cercle Énergie — accueil"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie" width="300" height="209"></a>
    <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Navigation principale">{links}<a class="btn btn-primary" href="#partenaire">Devenir partenaire {ARROW}</a></nav>
  </div>
</header>"""
FOOTER = """<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <span class="logo"><img src="assets/img/logo_full_t.png" alt="Cercle Énergie — Le partenaire unique de vos projets" width="300" height="192"></span>
        <p style="margin-top:20px;max-width:38ch">Mandataire CEE : nous accompagnons les professionnels dans la gestion et le financement de leurs Certificats d’Économies d’Énergie.</p>
      </div>
      <div><h4>Le site</h4><ul><li><a href="#services">Services</a></li><li><a href="#secteurs">Secteurs</a></li><li><a href="#faq">Questions fréquentes</a></li><li><a href="#partenaire">Devenir partenaire</a></li><li><a href="plaquette.pdf">Plaquette (PDF)</a></li></ul></div>
      <div><h4>Contact</h4><ul><li>[Téléphone à compléter]</li><li>[E-mail à compléter]</li><li>[Adresse à compléter]</li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Cercle Énergie. Tous droits réservés.</span><span>[Mentions légales] · [Politique de confidentialité] — Les primes CEE sont versées sous réserve de validation du dossier.</span></div>
  </div>
</footer>"""
INNER = f"{HEADER}\n<main id=\"contenu\">\n{BODY}\n</main>\n{FOOTER}\n<script src=\"assets/js/main.js\" defer></script>"
TITLE = "Cercle Énergie — Mandataire CEE, partenaire des installateurs"
DESC = "Cercle Énergie accompagne artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs aides CEE."
(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="assets/img/video-poster.jpg">
<meta name="theme-color" content="#0B3566">
<link rel="icon" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{INNER}
</body>
</html>
""", encoding="utf-8")
# version « page partagée » (sans squelette html, polices Google en secours)
(ROOT / "_partage.html").write_text(f"""<title>Cercle Énergie</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Montserrat:ital,wght@0,600;0,700;0,800;1,700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{INNER}
""", encoding="utf-8")
print("écrit index.html")
