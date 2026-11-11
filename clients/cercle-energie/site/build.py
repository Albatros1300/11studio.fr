#!/usr/bin/env python3
"""Génère le site statique multi-pages Cercle Énergie.
Usage : python3 build.py  (écrit les .html à côté de ce fichier)"""
import pathlib

ROOT = pathlib.Path(__file__).parent
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NAV = [("services.html", "Services"), ("secteurs.html", "Secteurs"), ("comprendre-les-cee.html", "Les CEE"), ("a-propos.html", "À propos"), ("faq.html", "FAQ")]
NOTE = '<p class="note rv">* Sous réserve de validation du dossier.</p>'

# ------------------------------------------------------------------ données
STEPS = [
    ("Étude d’éligibilité", "Nous identifions les aides CEE mobilisables selon les travaux que vous envisagez.",
     ["Analyse du projet", "Aides mobilisables", "Retour clair avant engagement"],
     "La description des travaux envisagés.", "Une vision claire des aides CEE mobilisables."),
    ("Valorisation financière", "Nous recherchons les meilleures conditions de valorisation auprès de nos partenaires.",
     ["Mise en relation", "Meilleures conditions", "Proposition lisible"],
     "Les éléments de votre projet.", "Les meilleures conditions recherchées auprès de nos partenaires."),
    ("Gestion administrative", "Nous prenons en charge la constitution, la vérification et le suivi de vos dossiers.",
     ["Constitution", "Vérification des pièces", "Suivi"],
     "Les pièces et informations nécessaires au dossier.", "Un dossier constitué, vérifié et suivi par nos soins."),
    ("Accompagnement réglementaire", "Nous vérifions les exigences documentaires et les conditions du dispositif.",
     ["Exigences documentaires", "Conditions du dispositif", "Dossiers sécurisés"],
     "Les documents liés à vos travaux.", "Un dossier vérifié au regard des exigences du dispositif."),
    ("Suivi du financement", "Nous coordonnons avec les délégataires jusqu’au traitement du dossier et au versement des primes*.",
     ["Coordination délégataires", "Suivi du traitement", "Information à chaque avancée"],
     "Les compléments éventuellement demandés.", "Un suivi jusqu’au versement des primes*."),
]
s2_html = "".join(
    f'<div class="s2" data-n="0{i+1}"><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>'
    for i, (t, d, li, _a, _b) in enumerate(STEPS))
detail_html = "".join(
    f'<article class="rv" id="etape-{i+1}"><div class="num">0{i+1}</div><div><h3>{t}</h3><p style="margin-top:10px">{d}</p></div>'
    f'<ul><li><b>Vous nous transmettez :</b> {a}</li><li><b>Vous obtenez :</b> {b}</li></ul></article>'
    for i, (t, d, li, a, b) in enumerate(STEPS))

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
WHO_TABLE = f'<div class="table-scroll rv"><table class="who"><thead><tr><th scope="col">Étape</th><th scope="col">Vous</th><th scope="col">Cercle Énergie</th><th scope="col">Délégataire CEE</th></tr></thead><tbody>{who_html}</tbody></table></div>'

FAQ = [("Que sont les Certificats d’Économies d’Énergie (CEE) ?", "C’est un dispositif national qui conduit les fournisseurs d’énergie à financer des travaux d’économies d’énergie. Pour vos clients, cela se traduit par des primes sur les travaux éligibles."),
       ("Quel est le rôle de Cercle Énergie ?", "Cercle Énergie est mandataire : nous faisons le lien entre les entreprises d’installation et les acteurs du financement des CEE, en simplifiant l’ensemble des démarches administratives."),
       ("Qu’est-ce qu’un délégataire CEE ?", "C’est un acteur du financement des Certificats d’Économies d’Énergie. Nous travaillons en collaboration avec des délégataires pour valoriser vos dossiers."),
       ("Avec qui travaillez-vous ?", "Nous travaillons en collaboration avec des délégataires CEE, auprès desquels nous recherchons les meilleures conditions de valorisation."),
       ("À qui s’adresse l’accompagnement ?", "Aux artisans, installateurs, entreprises du bâtiment et professionnels de la rénovation énergétique, dans les secteurs résidentiel, tertiaire, industriel et agricole."),
       ("Que dois-je vous transmettre ?", "La description des travaux envisagés, puis les pièces et informations nécessaires au dossier. Nous vous indiquons ce qu’il faut à chaque étape."),
       ("Le versement des primes est-il garanti ?", "Non : le traitement du dossier et le versement des primes interviennent sous réserve de validation. Notre travail consiste à constituer et vérifier des dossiers conformes aux exigences du dispositif."),
       ("Comment devenir partenaire ?", "Remplissez le formulaire de la page « Devenir partenaire » : nous revenons vers vous pour échanger sur votre activité et vos chantiers.")]
faq_all = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
faq_short = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[:4])

CHAIN = """<div class="chain">
      <div class="node rv"><div class="ic"><svg viewBox="0 0 24 24"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/></svg></div><h3>Installateurs &amp; artisans</h3><p>Vous réalisez les travaux chez vos clients.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node core rv" style="--d:.12s"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie"><span class="pill">Votre mandataire CEE</span><p>Nous montons, sécurisons et suivons vos dossiers.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node g rv" style="--d:.24s"><div class="ic"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="13" height="17" rx="2"/><path d="M7.5 8h6M7.5 11.5h6M7.5 15h3"/><circle cx="17.5" cy="17" r="4" fill="#5FA60E"/><path d="M19 15.8a2 2 0 1 0 0 2.4M15.6 16.5h2.4M15.6 17.6h2.4"/></svg></div><h3>Délégataires CEE</h3><p>Les acteurs du financement des Certificats d’Économies d’Énergie.</p></div>
    </div>"""
FLOW4 = """<div class="flow4 rv">
      <div class="f4"><h3>Les fournisseurs d’énergie financent</h3><p>Le dispositif les conduit à soutenir des travaux d’économies d’énergie, sous forme de primes.</p></div>
      <div class="f4"><h3>Les délégataires portent le financement</h3><p>Ce sont les acteurs avec lesquels les dossiers CEE sont valorisés.</p></div>
      <div class="f4 me"><h3>Cercle Énergie fait le lien</h3><p>Mandataire, nous étudions l’éligibilité, montons et suivons vos dossiers.</p></div>
      <div class="f4"><h3>Vous réalisez les travaux</h3><p>Vous restez sur vos chantiers ; votre client bénéficie de la prime*.</p></div>
    </div>"""

SECT = [
    ("secteur-residentiel.html", "Résidentiel", "pac-installation.jpg", "Vos chantiers dans l’habitat, nos dossiers CEE.",
     "Pompes à chaleur, chauffage, isolation, rénovation énergétique : c’est le terrain quotidien des installateurs et des artisans. Nous étudions l’éligibilité de vos chantiers et prenons en charge le dossier CEE.",
     ["Installateurs de pompes à chaleur et de systèmes de chauffage", "Entreprises d’isolation et de rénovation énergétique", "Professionnels de la ventilation"],
     ["pompe-a-chaleur.jpg", "isolation-combles.jpg", "renovation.jpg"]),
    ("secteur-tertiaire.html", "Tertiaire", "tertiaire.jpg", "Vos chantiers dans les bâtiments tertiaires, nos dossiers CEE.",
     "Bureaux, commerces, établissements : des projets plus techniques et des dossiers plus lourds. Nous les structurons avec vous et les suivons jusqu’au financement.",
     ["Entreprises intervenant dans le secteur tertiaire", "Professionnels de la ventilation et des équipements thermiques", "Installateurs de systèmes de chauffage"],
     ["tertiaire.jpg", "chauffage.jpg", "equipe.jpg"]),
    ("secteur-industrie.html", "Industrie", "industrie.jpg", "Vos chantiers sur les sites industriels, nos dossiers CEE.",
     "Nous accompagnons les entreprises intervenant sur des sites industriels dans le montage et le suivi de leurs dossiers CEE.",
     ["Entreprises intervenant dans le secteur industriel", "Professionnels des équipements thermiques", "Professionnels de la ventilation"],
     ["industrie.jpg", "remise-dossier.jpg", "equipe.jpg"]),
    ("secteur-agricole.html", "Agricole", "agricole.jpg", "Vos chantiers dans les exploitations agricoles, nos dossiers CEE.",
     "Serres, bâtiments d’exploitation : nous intervenons aussi auprès des professionnels qui travaillent pour le secteur agricole.",
     ["Entreprises intervenant dans le secteur agricole", "Professionnels des équipements thermiques", "Installateurs de systèmes de chauffage"],
     ["agricole.jpg", "chauffage.jpg", "remise-dossier.jpg"]),
]
linkcards = "".join(
    f'<a class="lc rv" style="--d:{i*.08:.2f}s" href="{h}"><img src="assets/img/{img}" alt="" loading="lazy"><div><h3>{t}</h3><p>{k}</p><span class="go">Découvrir {ARROW}</span></div></a>'
    for i, (h, t, img, k, _p, _l, _g) in enumerate(SECT))

FORM = f"""<form class="lead-form rv" id="lead-form" novalidate>
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
    </form>"""
JOIN = f"""<section class="join" id="partenaire">
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
    {FORM}
  </div>
</section>"""
CTA = f"""<section class="cta">
  <div class="wrap">
    <h2 class="rv">Devenez<br>partenaire.</h2>
    <p class="rv">Concentrez-vous sur vos chantiers et vos clients. Nous nous occupons de vos aides CEE.</p>
    <a class="btn btn-dark btn-xl rv" href="devenir-partenaire.html">Parlons de vos chantiers {ARROW}</a>
  </div>
</section>"""


def hero(img, eyebrow, h1, lead, crumbs=None, pos="50% 50%"):
    c = ""
    if crumbs:
        c = '<nav class="crumbs" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a>' + "".join(
            f'<span>/</span><a href="{h}">{t}</a>' if h else f"<span>/</span>{t}" for h, t in crumbs) + "</nav>"
    return f"""<section class="page-hero ph">
  <img class="bg" src="assets/img/{img}" alt="" style="object-position:{pos}">
  <div class="shade"></div>
  <div class="wrap">{c}<span class="eyebrow rv">{eyebrow}</span><h1 class="rv">{h1}</h1><p class="lead rv">{lead}</p></div>
</section>"""


# ------------------------------------------------------------------ pages
P = {}

P["index.html"] = ("Cercle Énergie — Mandataire CEE, partenaire des installateurs",
 "Cercle Énergie accompagne artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs aides CEE.", f"""
<section class="hero2" id="accueil">
  <video class="bgv" autoplay muted loop playsinline poster="assets/img/pac-installation.jpg"><source src="assets/video/hero.mp4" type="video/mp4"></video>
  <div class="shade"></div><div class="halo"></div><div class="halo b"></div>
  <div class="wrap">
    <span class="eyebrow">Mandataire CEE · Partenaire des professionnels</span>
    <h1 class="mega"><span class="ln" style="--i:0"><span>Vous réalisez</span></span><span class="ln" style="--i:1"><span>les travaux.</span></span><span class="ln lime" style="--i:2"><span>Nous gérons</span></span><span class="ln lime" style="--i:3"><span>vos aides CEE.</span></span></h1>
    <div class="hero2-foot">
      <div><p class="lead">Cercle Énergie accompagne les artisans, installateurs et entreprises du bâtiment dans la gestion et le financement de leurs Certificats d’Économies d’Énergie.</p>
      <div class="proof"><span>Un interlocuteur unique</span><span>Dossiers vérifiés</span><span>Suivi jusqu’au financement</span></div></div>
      <div class="hero-cta" style="margin:0"><a class="btn btn-primary btn-xl" href="devenir-partenaire.html">Devenir partenaire {ARROW}</a><a class="btn btn-ghost btn-xl" href="#video">Voir la vidéo</a></div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="track">{MARQ}{MARQ}</div></div>
<section class="statement" id="constat">
  <div class="wrap split">
    <div><span class="eyebrow rv">Le constat</span>
      <p class="fill" data-fill data-green="6">Les CEE font gagner des chantiers. La paperasse vous les fait payer. Nous reprenons la main sur vos dossiers.</p></div>
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
<section class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">Notre rôle</span>
    <h2 class="rv">Le lien entre vos chantiers<br>et le financement.</h2>
    <p class="lead rv">En tant que mandataire, Cercle Énergie travaille en collaboration avec des délégataires CEE pour accompagner les professionnels dans leurs projets.</p>
    {CHAIN}
    <p class="rv" style="margin:48px auto 0"><a class="btn btn-ghost" href="comprendre-les-cee.html">Comprendre les CEE {ARROW}</a></p>
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
      <p style="margin-top:24px"><a class="btn btn-line" href="services.html">Tous nos services en détail {ARROW}</a></p>
    </div>
  </div>
</section>
<section class="tint" id="secteurs">
  <div class="wrap">
    <span class="eyebrow rv">Nos terrains</span>
    <h2 class="rv">Partout où il y a de l’énergie<br>à économiser.</h2>
    <div class="panels rv" id="panels">{panels_html}</div>
    <p class="rv" style="margin-top:36px"><a class="btn btn-line" href="secteurs.html">Voir tous les secteurs {ARROW}</a></p>
  </div>
</section>
<section id="benefices">
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
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span>
    <h2 class="rv">L’essentiel à savoir</h2>
    <div class="faq" style="text-align:left">{faq_short}</div>
    <p class="rv" style="margin:36px auto 0"><a class="btn btn-line" href="faq.html">Toutes les questions {ARROW}</a></p>
  </div>
</section>
{JOIN}""")

P["services.html"] = ("Nos services CEE — Cercle Énergie",
 "Étude d’éligibilité, valorisation financière, gestion administrative, accompagnement réglementaire et suivi du financement de vos dossiers CEE.",
 hero("remise-dossier.jpg", "Nos services", "De l’étude du projet jusqu’au financement.", "Un accompagnement complet pour simplifier, sécuriser et valoriser vos projets d’économies d’énergie.", [(None, "Services")]) + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">Cinq étapes</span><h2 class="rv">Ce que nous faisons pour vous</h2>
    <div class="detail">{detail_html}</div>
    {NOTE}
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Répartition des rôles</span><h2 class="rv">Vous, sur le chantier.<br>Nous, sur le dossier.</h2>
    {WHO_TABLE}
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Ce que vous y gagnez</span><h2 class="rv">Simplifier. Sécuriser. Valoriser.</h2>
    <div class="trio3">{b3_html}</div>
  </div>
</section>
{CTA}""")

P["comprendre-les-cee.html"] = ("Comprendre les CEE — Cercle Énergie",
 "Les Certificats d’Économies d’Énergie expliqués simplement : qui finance, qui porte les dossiers, et le rôle de Cercle Énergie, mandataire CEE.",
 hero("renovation.jpg", "Comprendre", "Les CEE en 30 secondes.", "Un dispositif simple sur le papier. Nous le rendons simple sur le terrain.", [(None, "Les CEE")]) + f"""
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Le principe</span>
    <h2 class="rv">Qui fait quoi dans un dossier CEE ?</h2>
    {FLOW4}
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
<section>
  <div class="wrap split">
    <div class="media rv"><img src="assets/img/paperasse.jpg" alt="" loading="lazy"></div>
    <div>
      <span class="eyebrow rv">Pour vous, concrètement</span>
      <h2 class="rv">Une opportunité commerciale, sans la charge administrative.</h2>
      <p class="lead rv">Les CEE sont un vrai levier pour vos chantiers. Mais l’éligibilité, les pièces à réunir, les exigences du dispositif et le suivi prennent du temps.</p>
      <ul class="ticks rv"><li>Vous vous concentrez sur vos chantiers et vos clients.</li><li>Nous vous accompagnons dans la gestion administrative et financière de vos aides CEE.</li><li>Nos équipes restent à vos côtés à chaque étape.</li></ul>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">L’essentiel à savoir</h2>
    <div class="faq" style="text-align:left">{faq_short}</div>
  </div>
</section>
{CTA}""")

P["secteurs.html"] = ("Secteurs d’intervention — Cercle Énergie",
 "Résidentiel, tertiaire, industriel, agricole : Cercle Énergie accompagne les professionnels de l’efficacité énergétique.",
 hero("tertiaire.jpg", "Nos terrains", "Partout où il y a de l’énergie à économiser.", "Résidentiel, tertiaire, industriel ou agricole : nous accompagnons les professionnels de l’efficacité énergétique, quel que soit leur terrain.", [(None, "Secteurs")]) + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">Quatre secteurs</span><h2 class="rv">Choisissez votre terrain</h2>
    <div class="linkcards">{linkcards}</div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Vos métiers</span><h2 class="rv">Les travaux que nous accompagnons</h2>
    <div class="panels rv" id="panels">{panels_html}</div>
  </div>
</section>
{CTA}""")

for i, (h, t, img, k, p, li, gal) in enumerate(SECT):
    nxt = SECT[(i + 1) % len(SECT)]
    P[h] = (f"{t} — Secteurs — Cercle Énergie", f"{k} Cercle Énergie accompagne les professionnels du secteur {t.lower()} dans leurs dossiers CEE.",
     hero(img, f"Secteur {i+1}/4", t + ".", k, [("secteurs.html", "Secteurs"), (None, t)], "60% 50%") + f"""
<section>
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Votre terrain</span>
      <h2 class="rv">Vous intervenez, nous montons le dossier.</h2>
      <p class="lead rv">{p}</p>
      <ul class="ticks rv">{"".join(f"<li>{x}</li>" for x in li)}</ul>
    </div>
    <div class="media rv"><img src="assets/img/{gal[1]}" alt="" loading="lazy"></div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Notre accompagnement</span><h2 class="rv">Les mêmes cinq étapes, quel que soit le chantier</h2>
    <div class="cols3">{"".join(f'<div class="box rv"><span class="n">0{j+1}</span><h3>{s[0]}</h3><p>{s[1]}</p></div>' for j, s in enumerate(STEPS))}</div>
    {NOTE}
    <div class="nextprev rv"><a class="btn btn-line" href="services.html">Nos services en détail {ARROW}</a><a class="btn btn-line" href="{nxt[0]}">Secteur suivant : {nxt[1]} {ARROW}</a></div>
  </div>
</section>
{CTA}""")

P["a-propos.html"] = ("À propos — Cercle Énergie",
 "Cercle Énergie, société spécialisée dans l’accompagnement et la valorisation des Certificats d’Économies d’Énergie, partenaire des professionnels.",
 hero("equipe.jpg", "À propos", "Le partenaire unique de vos projets.", "Cercle Énergie est une société spécialisée dans l’accompagnement et la valorisation des Certificats d’Économies d’Énergie.", [(None, "À propos")], "50% 30%") + f"""
<section>
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Qui sommes-nous</span>
      <h2 class="rv">Un mandataire CEE au service des professionnels.</h2>
      <p class="lead rv">En qualité de mandataire, nous travaillons en collaboration avec des délégataires CEE afin d’accompagner les professionnels dans le financement de leurs projets de rénovation et d’efficacité énergétique.</p>
      <p class="rv" style="margin-top:18px">Notre rôle est de faire le lien entre les entreprises d’installation et les acteurs du financement des CEE, tout en simplifiant l’ensemble des démarches administratives.</p>
    </div>
    <div class="media rv"><img src="assets/img/remise-dossier.jpg" alt="Une conseillère remet un dossier à un artisan" loading="lazy"><span class="badge">Vous réalisez les travaux, nous vous accompagnons.</span></div>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <span class="eyebrow rv">Notre mission</span>
    <p class="bigquote rv">Permettre aux professionnels de <em>se concentrer sur leur métier</em>, pendant que nous les accompagnons dans la gestion et le financement de leurs dossiers CEE.</p>
    <div class="cols3">
      <div class="box rv"><span class="n">01</span><h3>Simplifier</h3><p>Un interlocuteur unique pour toutes vos démarches CEE.</p></div>
      <div class="box rv"><span class="n">02</span><h3>Sécuriser</h3><p>Des dossiers vérifiés au regard des exigences du dispositif.</p></div>
      <div class="box rv"><span class="n">03</span><h3>Valoriser</h3><p>Les meilleures conditions recherchées auprès de nos partenaires.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Ceux que nous accompagnons</span><h2 class="rv">Des professionnels de tous les terrains</h2>
    <div class="linkcards">{linkcards}</div>
  </div>
</section>
<section class="tint" id="video">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span><h2 class="rv">Cercle Énergie en 72 secondes</h2>
    <div class="video-frame rv"><video controls preload="none" poster="assets/img/video-poster.jpg"><source src="assets/video/presentation.mp4" type="video/mp4"></video></div>
  </div>
</section>
{CTA}""")

P["faq.html"] = ("Questions fréquentes — Cercle Énergie",
 "Les réponses aux questions les plus fréquentes sur les CEE, le rôle de Cercle Énergie et le partenariat.",
 hero("portrait-conseillere.jpg", "Questions fréquentes", "Vos questions, nos réponses.", "L’essentiel à savoir sur les CEE, notre rôle de mandataire et le partenariat.", [(None, "FAQ")], "50% 25%") + f"""
<section>
  <div class="wrap center">
    <div class="faq" style="text-align:left;margin-top:0">{faq_all}</div>
    <p class="rv" style="margin:44px auto 0">Une autre question ? <a class="hl" href="contact.html" style="font-weight:700">Contactez-nous</a>.</p>
  </div>
</section>
{CTA}""")

P["devenir-partenaire.html"] = ("Devenir partenaire — Cercle Énergie",
 "Installateurs et entreprises du bâtiment : devenez partenaire de Cercle Énergie pour la gestion et le financement de vos aides CEE.",
 hero("artisan-clients.jpg", "Devenir partenaire", "Développez votre activité, simplifiez votre gestion.", "Rejoignez les professionnels accompagnés par Cercle Énergie pour la gestion et le financement de leurs aides CEE.", [(None, "Devenir partenaire")]) + f"""
{JOIN}
<section>
  <div class="wrap">
    <span class="eyebrow rv">Pourquoi nous rejoindre</span><h2 class="rv">Simplifier. Sécuriser. Valoriser.</h2>
    <div class="trio3">{b3_html}</div>
  </div>
</section>
<section class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">Avant de vous lancer</h2>
    <div class="faq" style="text-align:left">{"".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[4:])}</div>
  </div>
</section>""")

P["contact.html"] = ("Contact — Cercle Énergie", "Contactez Cercle Énergie, mandataire CEE et partenaire des professionnels de la rénovation énergétique.",
 hero("remise-dossier.jpg", "Contact", "Parlons de vos chantiers.", "Une question sur les CEE ou sur notre accompagnement ? Écrivez-nous.", [(None, "Contact")]) + f"""
<section>
  <div class="wrap">
    <div class="contact-grid">
      <div class="box rv"><span class="n">Téléphone</span><h3>[Téléphone à compléter]</h3><p>Du lundi au vendredi.</p></div>
      <div class="box rv"><span class="n">E-mail</span><h3>[E-mail à compléter]</h3><p>Nous revenons vers vous rapidement.</p></div>
      <div class="box rv"><span class="n">Adresse</span><h3>[Adresse à compléter]</h3><p>Sur rendez-vous.</p></div>
    </div>
  </div>
</section>
{JOIN}""")

P["mentions-legales.html"] = ("Mentions légales — Cercle Énergie", "Mentions légales du site Cercle Énergie.",
 """<section class="page-hero"><div class="wrap"><span class="eyebrow rv">Informations légales</span><h1 class="rv">Mentions légales</h1></div></section>
<section><div class="wrap legaltext">
  <p><strong>Page à compléter avant mise en ligne publique.</strong></p>
  <h2>Éditeur du site</h2><p>[Raison sociale] — [Forme juridique] — [Capital social]<br>[Adresse du siège]<br>[SIREN / RCS] — [N° TVA]<br>Directeur de la publication : [Nom]</p>
  <h2>Hébergement</h2><p>[Nom et adresse de l’hébergeur]</p>
  <h2>Données personnelles</h2><p>Les informations saisies dans le formulaire de contact sont utilisées uniquement pour répondre à votre demande. [Politique de confidentialité à compléter : responsable de traitement, durée de conservation, droits d’accès et de suppression, contact.]</p>
  <h2>Primes CEE</h2><p>Le traitement des dossiers et le versement des primes CEE interviennent sous réserve de validation du dossier.</p>
</div></section>""")

# ------------------------------------------------------------------ gabarit
def page(fname, title, desc, body):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if (h == fname or (h == "secteurs.html" and fname.startswith("secteur-"))) else ""}>{t}</a>' for h, t in NAV)
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
      <div><h4>Le site</h4><ul><li><a href="services.html">Services</a></li><li><a href="secteurs.html">Secteurs</a></li><li><a href="comprendre-les-cee.html">Comprendre les CEE</a></li><li><a href="a-propos.html">À propos</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="plaquette.pdf">Plaquette (PDF)</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="devenir-partenaire.html">Devenir partenaire</a></li><li><a href="contact.html">Nous contacter</a></li><li>[Téléphone à compléter]</li><li>[E-mail à compléter]</li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Cercle Énergie. Tous droits réservés.</span><span><a href="mentions-legales.html">Mentions légales</a> — Les primes CEE sont versées sous réserve de validation du dossier.</span></div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

for f, (t, d, b) in P.items():
    (ROOT / f).write_text(page(f, t, d, b), encoding="utf-8")
print(len(P), "pages écrites :", ", ".join(P))
