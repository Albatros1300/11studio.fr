#!/usr/bin/env python3
"""Génère les pages statiques du site de démonstration Cercle Énergie.
Usage : python3 build.py  (écrit les .html à côté de ce fichier)"""
import pathlib

ROOT = pathlib.Path(__file__).parent
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NAV = [("index.html", "Accueil"), ("services.html", "Services"), ("secteurs.html", "Secteurs")]


def page(fname, title, desc, body):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/video-poster.jpg">
<meta name="theme-color" content="#0B3566">
<link rel="icon" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="progress" id="progress"></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Cercle Énergie — accueil"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie" width="300" height="209"></a>
    <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Navigation principale">{links}<a class="btn btn-primary" href="devenir-partenaire.html">Devenir partenaire {ARROW}</a></nav>
  </div>
</header>
<main id="contenu">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <span class="logo"><img src="assets/img/logo_full_t.png" alt="Cercle Énergie — Le partenaire unique de vos projets" width="300" height="192"></span>
        <p style="margin-top:20px;max-width:38ch">Mandataire CEE : nous accompagnons les professionnels dans la gestion et le financement de leurs Certificats d’Économies d’Énergie.</p>
      </div>
      <div><h4>Le site</h4><ul><li><a href="index.html">Accueil</a></li><li><a href="services.html">Services</a></li><li><a href="secteurs.html">Secteurs</a></li><li><a href="devenir-partenaire.html">Devenir partenaire</a></li></ul></div>
      <div><h4>Contact</h4><ul><li>[Téléphone à compléter]</li><li>[E-mail à compléter]</li><li>[Adresse à compléter]</li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Cercle Énergie. Tous droits réservés.</span><span>[Mentions légales] · [Politique de confidentialité] — Les primes CEE sont versées sous réserve de validation du dossier.</span></div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


CTA = f"""<section class="cta">
  <div class="wrap">
    <h2 class="rv">Devenez<br>partenaire.</h2>
    <p class="rv">Concentrez-vous sur vos chantiers et vos clients. Nous nous occupons de vos aides CEE.</p>
    <a class="btn btn-dark btn-xl rv" href="devenir-partenaire.html">Parlons de vos chantiers {ARROW}</a>
  </div>
</section>"""

STEPS = [
    ("Étude d’éligibilité", "Identification des aides CEE mobilisables selon les travaux envisagés."),
    ("Valorisation financière", "Recherche des meilleures conditions de valorisation auprès de nos partenaires."),
    ("Gestion administrative", "Constitution, vérification et suivi de vos dossiers."),
    ("Accompagnement réglementaire", "Vérification des exigences documentaires et des conditions du dispositif."),
    ("Suivi du financement", "Coordination avec les délégataires jusqu’au versement des primes*."),
]
steps_html = "".join(f'<div class="step rv" style="--d:{i*.08:.2f}s"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))

SECTORS = [
    ("pompe-a-chaleur.jpg", "Pompes à chaleur", "Installateurs de pompes à chaleur et de systèmes thermodynamiques."),
    ("chauffage.jpg", "Chauffage", "Systèmes de chauffage, équipements thermiques et ventilation."),
    ("isolation-combles.jpg", "Isolation", "Entreprises spécialisées dans l’isolation des bâtiments."),
    ("tertiaire.jpg", "Tertiaire", "Bureaux, commerces, établissements recevant du public."),
    ("industrie.jpg", "Industrie", "Sites de production, utilités et procédés."),
    ("agricole.jpg", "Agricole", "Exploitations, serres et bâtiments d’élevage."),
]
cards_html = "".join(
    f'<a class="card rv" style="--d:{(i%3)*.08:.2f}s" href="secteurs.html"><img src="assets/img/{img}" alt="" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></a>'
    for i, (img, t, d) in enumerate(SECTORS))

CHAIN = """<div class="chain">
      <div class="node rv"><div class="ic"><svg viewBox="0 0 24 24"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/></svg></div><h3>Installateurs &amp; artisans</h3><p>Vous réalisez les travaux chez vos clients.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node core rv" style="--d:.12s"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie"><span class="pill">Votre mandataire CEE</span><p>Nous montons, sécurisons et suivons vos dossiers.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node g rv" style="--d:.24s"><div class="ic"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="13" height="17" rx="2"/><path d="M7.5 8h6M7.5 11.5h6M7.5 15h3"/><circle cx="17.5" cy="17" r="4" fill="#5FA60E"/><path d="M19 15.8a2 2 0 1 0 0 2.4M15.6 16.5h2.4M15.6 17.6h2.4"/></svg></div><h3>Délégataires CEE</h3><p>Les acteurs du financement des Certificats d’Économies d’Énergie.</p></div>
    </div>"""

# ------------------------------------------------------------------ index
MARQ = "".join(f"<span>{t}</span>" for t in ["Pompes à chaleur", "Chauffage", "Isolation", "Ventilation", "Rénovation énergétique", "Tertiaire", "Industrie", "Agricole"])
CMP = [("Aides", "À identifier vous-même, chantier par chantier", "Identifiées selon vos travaux"),
       ("Dossiers", "À constituer, vérifier et suivre en interne", "Constitués, vérifiés et suivis pour vous"),
       ("Exigences", "À maîtriser et contrôler seul", "Exigences documentaires contrôlées"),
       ("Financement", "Des acteurs à trouver et à coordonner", "Un partenaire unique, en lien avec les délégataires")]
cmp_html = "".join(f'<div class="cmp" style="--i:{i}"><small>{k}</small><p class="a">{a}</p><p class="b">{b}</p><i></i></div>' for i, (k, a, b) in enumerate(CMP))
s2_html = "".join(f'<div class="s2" data-n="0{i+1}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))
PANELS = [("pompe-a-chaleur.jpg", "Pompes à chaleur", "Installateurs de pompes à chaleur et de systèmes thermodynamiques."),
          ("chauffage.jpg", "Chauffage", "Systèmes de chauffage, ventilation et équipements thermiques."),
          ("isolation-combles.jpg", "Isolation", "Entreprises spécialisées dans l’isolation des bâtiments."),
          ("renovation.jpg", "Rénovation énergétique", "Entreprises de rénovation énergétique et entreprises générales du bâtiment."),
          ("tertiaire.jpg", "Tertiaire", "Bureaux, commerces, établissements recevant du public."),
          ("industrie.jpg", "Industrie", "Sites de production, utilités et équipements thermiques."),
          ("agricole.jpg", "Agricole", "Exploitations, serres et bâtiments d’élevage.")]
panels_html = "".join(
    f'<article class="panel{" on" if i == 0 else ""}" tabindex="0"><img src="assets/img/{img}" alt="" loading="lazy"><span class="no">0{i+1}</span><span class="lab">{t}</span><div class="in"><h3>{t}</h3><p>{d}</p></div></article>'
    for i, (img, t, d) in enumerate(PANELS))

index = f"""<section class="hero2">
  <video class="bgv" autoplay muted loop playsinline poster="assets/img/pac-installation.jpg"><source src="assets/video/hero.mp4" type="video/mp4"></video>
  <div class="shade"></div><div class="halo"></div><div class="halo b"></div>
  <div class="wrap">
    <span class="eyebrow">Mandataire CEE · Partenaire des professionnels</span>
    <h1 class="mega"><span class="ln" style="--i:0"><span>Vous réalisez</span></span><span class="ln" style="--i:1"><span>les travaux.</span></span><span class="ln lime" style="--i:2"><span>Nous gérons</span></span><span class="ln lime" style="--i:3"><span>vos aides CEE.</span></span></h1>
    <div class="hero2-foot">
      <p class="lead">Cercle Énergie accompagne les artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs Certificats d’Économies d’Énergie.</p>
      <div class="hero-cta" style="margin:0"><a class="btn btn-primary btn-xl" href="devenir-partenaire.html">Devenir partenaire {ARROW}</a><a class="btn btn-ghost btn-xl" href="#video">Voir la vidéo</a></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{MARQ}{MARQ}</div></div>

<section class="statement" id="constat">
  <div class="wrap">
    <span class="eyebrow rv">Le constat</span>
    <p class="fill" data-fill data-green="6">Les CEE font gagner des chantiers. La paperasse vous les fait payer. Nous reprenons la main sur vos dossiers.</p>
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
      <p style="margin-top:24px"><a class="btn btn-line" href="services.html">Découvrir nos services {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Nos terrains</span>
    <h2 class="rv">Partout où il y a de l’énergie<br>à économiser.</h2>
    <div class="panels rv" id="panels">{panels_html}</div>
  </div>
</section>

<section id="video" class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span>
    <h2 class="rv">Cercle Énergie en 72 secondes</h2>
    <div class="video-frame rv"><video controls preload="none" poster="assets/img/video-poster.jpg"><source src="assets/video/presentation.mp4" type="video/mp4">Votre navigateur ne peut pas lire cette vidéo.</video></div>
  </div>
</section>
{CTA}"""

# ------------------------------------------------------------------ services
DETAIL = [
    ("Étude d’éligibilité", "Nous identifions les aides CEE mobilisables selon les travaux que vous envisagez.",
     ["Analyse du projet et des travaux prévus", "Identification des aides mobilisables", "Un retour clair avant de vous engager"]),
    ("Valorisation financière", "Nous recherchons les meilleures conditions de valorisation auprès de nos partenaires.",
     ["Mise en relation avec les délégataires", "Recherche des meilleures conditions", "Une proposition lisible pour vous et votre client"]),
    ("Gestion administrative", "Nous prenons en charge la constitution, la vérification et le suivi de vos dossiers.",
     ["Constitution du dossier", "Vérification des pièces", "Suivi jusqu’au dépôt"]),
    ("Accompagnement réglementaire", "Nous vérifions les exigences documentaires et les conditions du dispositif.",
     ["Contrôle des exigences documentaires", "Vérification des conditions du dispositif", "Des dossiers sécurisés avant transmission"]),
    ("Suivi du financement", "Nous coordonnons avec les délégataires jusqu’au traitement du dossier et au versement des primes, sous réserve de validation.",
     ["Coordination avec les délégataires", "Suivi du traitement du dossier", "Information à chaque avancée"]),
]
detail_html = "".join(
    f'<article class="rv"><div class="num">0{i+1}</div><div><h3>{t}</h3><p style="margin-top:10px">{d}</p></div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></article>'
    for i, (t, d, li) in enumerate(DETAIL))
WHO = [("Réalisation des travaux", 1, 0, 0), ("Étude d’éligibilité", 0, 1, 0), ("Recherche de valorisation", 0, 1, 0),
       ("Constitution et vérification du dossier", 0, 1, 0), ("Suivi et coordination", 0, 1, 0), ("Financement des CEE", 0, 0, 1)]
d = lambda v: '<span class="dot"></span>' if v else '<span class="dot o"></span>'
who_html = "".join(f"<tr><th scope='row'>{t}</th><td>{d(a)}</td><td>{d(b)}</td><td>{d(c)}</td></tr>" for t, a, b, c in WHO)

services = f"""<section class="page-hero">
  <div class="wrap"><span class="eyebrow rv">Nos services</span><h1 class="rv">De l’étude du projet jusqu’au financement</h1><p class="lead rv">Un accompagnement complet pour simplifier, sécuriser et valoriser vos projets d’économies d’énergie.</p></div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Cinq étapes</span><h2 class="rv">Ce que nous faisons pour vous</h2>
    <div class="detail">{detail_html}</div>
    <p class="note rv">Le versement des primes CEE intervient sous réserve de validation du dossier.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Répartition des rôles</span><h2 class="rv">Qui fait quoi ?</h2>
    <p class="lead rv">Vous réalisez les travaux, Cercle Énergie vous accompagne dans la gestion et le financement de vos aides CEE.</p>
    <div class="table-scroll rv"><table class="who"><thead><tr><th scope="col">Étape</th><th scope="col">Vous</th><th scope="col">Cercle Énergie</th><th scope="col">Délégataire CEE</th></tr></thead><tbody>{who_html}</tbody></table></div>
  </div>
</section>
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">L’essentiel à savoir</h2>
    <div class="faq" style="text-align:left">
      <details class="rv"><summary>Que sont les Certificats d’Économies d’Énergie (CEE) ?</summary><p>C’est un dispositif national qui conduit les fournisseurs d’énergie à financer des travaux d’économies d’énergie. Pour vos clients, cela se traduit par des primes sur les travaux éligibles.</p></details>
      <details class="rv"><summary>Quel est le rôle de Cercle Énergie ?</summary><p>Cercle Énergie est mandataire : nous faisons le lien entre les entreprises d’installation et les acteurs du financement des CEE, en simplifiant l’ensemble des démarches administratives.</p></details>
      <details class="rv"><summary>Avec qui travaillez-vous ?</summary><p>Nous travaillons en collaboration avec des délégataires CEE, auprès desquels nous recherchons les meilleures conditions de valorisation.</p></details>
      <details class="rv"><summary>À qui s’adresse l’accompagnement ?</summary><p>Aux artisans, installateurs, entreprises du bâtiment et professionnels de la rénovation énergétique, dans les secteurs résidentiel, tertiaire, industriel et agricole.</p></details>
      <details class="rv"><summary>Le versement des primes est-il garanti ?</summary><p>Non : le traitement du dossier et le versement des primes interviennent sous réserve de validation. Notre travail consiste à constituer et vérifier des dossiers conformes aux exigences du dispositif.</p></details>
    </div>
  </div>
</section>
{CTA}"""

# ------------------------------------------------------------------ secteurs
BLOCKS = [
    ("pac-installation.jpg", "Résidentiel", "Pompes à chaleur et chauffage", "Vous installez des pompes à chaleur ou des systèmes de chauffage : nous étudions l’éligibilité de vos chantiers et prenons en charge le dossier CEE.",
     ["Installateurs de pompes à chaleur", "Chauffagistes", "Professionnels de la ventilation et des équipements thermiques"]),
    ("isolation-exterieure.jpg", "Résidentiel", "Isolation et rénovation énergétique", "Isolation, menuiseries, rénovation d’ampleur : nous vous aidons à valoriser les économies d’énergie générées par vos travaux.",
     ["Entreprises d’isolation", "Entreprises de rénovation énergétique", "Entreprises générales du bâtiment"]),
    ("tertiaire.jpg", "Tertiaire", "Bâtiments tertiaires", "Bureaux, commerces, établissements : des projets plus techniques, des dossiers plus lourds — nous les structurons avec vous.",
     ["Bureaux et commerces", "Établissements recevant du public", "Équipements thermiques et ventilation"]),
    ("industrie.jpg", "Industrie", "Sites industriels", "Nous accompagnons les entreprises intervenant sur des sites industriels dans le montage et le suivi de leurs dossiers CEE.",
     ["Sites de production", "Utilités et équipements thermiques", "Projets d’efficacité énergétique"]),
    ("agricole.jpg", "Agricole", "Exploitations agricoles", "Serres, bâtiments d’élevage, exploitations : nous intervenons aussi auprès des professionnels du secteur agricole.",
     ["Serres", "Bâtiments d’exploitation", "Équipements thermiques"]),
]
blocks_html = "".join(
    f"""<section{' class="tint"' if i % 2 else ''}><div class="wrap split{' rev' if i % 2 else ''}">
    <div class="media rv"><img src="assets/img/{img}" alt="{h}" loading="lazy"></div>
    <div><span class="eyebrow rv">{k}</span><h2 class="rv">{h}</h2><p class="lead rv">{p}</p><ul class="ticks rv">{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
  </div></section>""" for i, (img, k, h, p, li) in enumerate(BLOCKS))

secteurs = f"""<section class="page-hero">
  <div class="wrap"><span class="eyebrow rv">Secteurs d’intervention</span><h1 class="rv">Résidentiel, tertiaire, industriel, agricole</h1><p class="lead rv">Nous accompagnons les professionnels de l’efficacité énergétique dans de nombreux domaines d’activité.</p></div>
</section>
{blocks_html}
{CTA}"""

# ------------------------------------------------------------------ partenaire
partenaire = f"""<section class="page-hero">
  <div class="wrap"><span class="eyebrow rv">Devenir partenaire</span><h1 class="rv">Développez votre activité, simplifiez votre gestion</h1><p class="lead rv">Rejoignez les professionnels accompagnés par Cercle Énergie pour la gestion et le financement de leurs aides CEE.</p></div>
</section>
<section>
  <div class="wrap form-grid">
    <div>
      <span class="eyebrow rv">Comment ça marche</span>
      <h2 class="rv">Un échange, et nous prenons le relais</h2>
      <ol class="mini-steps rv">
        <li><b>Vous nous présentez votre activité</b>Remplissez le formulaire : métier, secteur, type de chantiers.</li>
        <li><b>Nous étudions vos projets</b>Nous identifions les aides CEE mobilisables sur vos travaux.</li>
        <li><b>Nous gérons vos dossiers</b>Constitution, vérification, coordination avec les délégataires et suivi des primes*.</li>
      </ol>
      <ul class="ticks rv" style="margin-top:36px">
        <li>Un interlocuteur unique</li>
        <li>Des dossiers vérifiés avant transmission</li>
        <li>Un suivi jusqu’au financement</li>
      </ul>
      <p class="note rv">* Sous réserve de validation du dossier.</p>
    </div>
    <form class="lead-form rv" id="lead-form" novalidate>
      <h3 class="full">Parlons de vos chantiers</h3>
      <label>Société<input name="societe" autocomplete="organization" required></label>
      <label>Nom et prénom<input name="nom" autocomplete="name" required></label>
      <label>Téléphone<input name="telephone" type="tel" autocomplete="tel" required></label>
      <label>E-mail<input name="email" type="email" autocomplete="email" required></label>
      <label>Votre activité<select name="activite" required><option value="">Sélectionnez…</option><option>Pompes à chaleur</option><option>Chauffage</option><option>Isolation</option><option>Ventilation / équipements thermiques</option><option>Rénovation énergétique</option><option>Autre</option></select></label>
      <label>Secteur principal<select name="secteur"><option>Résidentiel</option><option>Tertiaire</option><option>Industriel</option><option>Agricole</option></select></label>
      <label class="full">Votre projet (facultatif)<textarea name="message" rows="4"></textarea></label>
      <label class="check full"><input type="checkbox" name="consentement" required><span>J’accepte d’être recontacté par Cercle Énergie au sujet de ma demande.</span></label>
      <button class="btn btn-primary full" type="submit">Envoyer ma demande {ARROW}</button>
      <p class="form-ok" role="status" id="form-ok">Merci ! Votre demande a bien été prise en compte. <br><small>(Version de démonstration : le formulaire n’est pas encore relié à une messagerie.)</small></p>
    </form>
  </div>
</section>"""

PAGES = {
    "index.html": ("Cercle Énergie — Mandataire CEE, partenaire des installateurs", "Cercle Énergie accompagne artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs aides CEE.", index),
    "services.html": ("Nos services CEE — Cercle Énergie", "Étude d’éligibilité, valorisation financière, gestion administrative, accompagnement réglementaire et suivi du financement de vos dossiers CEE.", services),
    "secteurs.html": ("Secteurs d’intervention — Cercle Énergie", "Résidentiel, tertiaire, industriel, agricole : Cercle Énergie accompagne les professionnels de l’efficacité énergétique.", secteurs),
    "devenir-partenaire.html": ("Devenir partenaire — Cercle Énergie", "Installateurs et entreprises du bâtiment : devenez partenaire de Cercle Énergie pour la gestion et le financement de vos aides CEE.", partenaire),
}
for f, (t, de, b) in PAGES.items():
    (ROOT / f).write_text(page(f, t, de, b), encoding="utf-8")
    print("écrit", f)
