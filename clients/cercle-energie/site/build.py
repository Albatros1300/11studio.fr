#!/usr/bin/env python3
"""Génère le site statique multi-pages Cercle Énergie.
Usage : python3 build.py  (écrit les .html à côté de ce fichier)"""
import pathlib

ROOT = pathlib.Path(__file__).parent
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NAV = [("accompagnement.html", "Le réseau"), ("services.html", "Dossiers CEE"), ("comprendre-les-cee.html", "Comment ça marche"), ("secteurs.html", "Secteurs"), ("a-propos.html", "À propos")]
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

MARQ = "".join(f"<span>{t}</span>" for t in ["Dossiers CEE", "Démarches administratives", "Formation", "Qualification RGE", "Tarifs fournisseurs", "Un réseau d’artisans", "Pompes à chaleur", "Chauffage", "Isolation", "Rénovation énergétique"])
CMP = [("Dossiers CEE", "À monter, vérifier et suivre vous-même, le soir", "Montés, vérifiés et suivis pour vous"),
       ("Administratif", "Seul face aux démarches et aux pièces à réunir", "Épaulé à chaque démarche"),
       ("Qualification RGE", "À obtenir et à conserver sans aide", "Accompagné pour l’obtenir et la conserver"),
       ("Fournisseurs", "Vos tarifs, négociés seul", "Des tarifs préférentiels auprès de fournisseurs partenaires")]
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

B3 = [("portrait-dossier.jpg", "Du temps", "Les dossiers et les démarches ne se font plus le soir. Vous transmettez, nous prenons le relais."),
      ("portrait-conseillere.jpg", "De la sécurité", "Des dossiers vérifiés, une qualification RGE suivie, un interlocuteur qui connaît les règles."),
      ("portrait-artisan.jpg", "Du poids", "Seul, on subit. En réseau, on accède à des tarifs fournisseurs et à des financeurs que l’on n’a pas seul.")]
b3_html = "".join(
    f'<article class="b3 rv" style="--d:{i*.1:.1f}s"><div class="ph"><img src="assets/img/{img}" alt="" loading="lazy"><span>0{i+1}</span></div><div class="tx"><h3>{t}</h3><p>{d}</p></div></article>'
    for i, (img, t, d) in enumerate(B3))

VOLETS = [
    ("services.html", "Dossiers CEE et primes", "remise-dossier.jpg", "Éligibilité, montage, vérification et suivi jusqu’au versement des primes*."),
    ("demarches-administratives.html", "Démarches administratives", "paperasse.jpg", "Les CEE, mais pas seulement : nous vous épaulons sur l’administratif de vos chantiers."),
    ("formation.html", "Formation aux CEE", "formation.jpg", "Comprendre les primes, les pièces à fournir et les erreurs qui font refuser un dossier."),
    ("qualification-rge.html", "Qualification RGE", "qualification-rge.jpg", "Un accompagnement pour obtenir et conserver votre qualification RGE."),
    ("tarifs-fournisseurs.html", "Tarifs fournisseurs", "fournisseur.jpg", "Des conditions préférentielles auprès de fournisseurs de matériel partenaires."),
    ("reseau.html", "Un réseau", "reseau.jpg", "Un interlocuteur, des artisans comme vous, et le lien avec les délégataires CEE."),
]
voletcards = "".join(
    f'<a class="lc rv" style="--d:{(i%3)*.08:.2f}s" href="{h}"><img src="assets/img/{img}" alt="" loading="lazy"><div><span class="vn">0{i+1}</span><h3>{t}</h3><p>{k}</p><span class="go">Découvrir {ARROW}</span></div></a>'
    for i, (h, t, img, k) in enumerate(VOLETS))
voletcards_autres = "".join(
    f'<a class="lc rv" style="--d:{(i%3)*.08:.2f}s" href="{h}"><img src="assets/img/{img}" alt="" loading="lazy"><div><span class="vn">0{i+2}</span><h3>{t}</h3><p>{k}</p><span class="go">Découvrir {ARROW}</span></div></a>'
    for i, (h, t, img, k) in enumerate(VOLETS[1:]))
VOLETS_SECTION = f"""<section id="accompagnement">
  <div class="wrap">
    <span class="eyebrow rv">L’accompagnement</span>
    <h2 class="rv">Six appuis.<br>Un seul réseau.</h2>
    <p class="lead rv">Ce que vous n’arrivez pas à faire seul, nous vous aidons à le faire.</p>
    <div class="linkcards six">{voletcards}</div>
    <p class="note rv">* Sous réserve de validation du dossier.</p>
  </div>
</section>"""

WHO = [("Réalisation des travaux", 1, 0, 0), ("Étude d’éligibilité", 0, 1, 0), ("Recherche de valorisation", 0, 1, 0),
       ("Constitution et vérification du dossier", 0, 1, 0), ("Suivi et coordination", 0, 1, 0), ("Financement des CEE", 0, 0, 1)]
dot = lambda v: '<span class="dot"></span>' if v else '<span class="dot o"></span>'
who_html = "".join(f"<tr><th scope='row'>{t}</th><td>{dot(a)}</td><td>{dot(b)}</td><td>{dot(c)}</td></tr>" for t, a, b, c in WHO)
WHO_TABLE = f'<div class="table-scroll rv"><table class="who"><thead><tr><th scope="col">Étape</th><th scope="col">Vous</th><th scope="col">Cercle Énergie</th><th scope="col">Délégataire CEE</th></tr></thead><tbody>{who_html}</tbody></table></div>'

FAQ = [("Qu’est-ce que Cercle Énergie ?", "Un réseau d’accompagnement pour les artisans RGE. Mandataire CEE, nous montons et suivons vos dossiers de primes, et nous vous épaulons aussi sur les démarches administratives, la formation, la qualification RGE et l’accès à des tarifs fournisseurs."),
       ("Que sont les Certificats d’Économies d’Énergie (CEE) ?", "C’est un dispositif national qui oblige les fournisseurs d’énergie à financer des travaux d’économies d’énergie. Pour vos clients, cela se traduit par des primes sur les travaux éligibles."),
       ("Qui sont les obligés et les délégataires ?", "Les obligés sont les fournisseurs d’énergie soumis à cette obligation. Les délégataires sont des structures à qui les obligés délèguent leur obligation : ce sont eux qui financent les primes CEE. Cercle Énergie travaille en collaboration avec des délégataires."),
       ("Quel est le rôle d’un mandataire ?", "Le mandataire fait le lien entre l’artisan et le délégataire : il étudie l’éligibilité, monte et vérifie le dossier, puis suit son traitement. C’est notre rôle."),
       ("À qui s’adresse le réseau ?", "Aux artisans et aux petites entreprises du bâtiment : installateurs de pompes à chaleur, chauffagistes, entreprises d’isolation et de rénovation énergétique, qualifiés RGE ou en voie de l’être."),
       ("Faut-il déjà être qualifié RGE ?", "Non. Nous accompagnons aussi les artisans qui préparent leur qualification. La qualification elle-même est délivrée par un organisme de qualification, pas par Cercle Énergie."),
       ("En quoi consiste la formation ?", "Elle porte sur le fonctionnement des primes CEE : les travaux concernés, les pièces d’un dossier conforme et les erreurs qui le font refuser."),
       ("Comment fonctionnent les tarifs fournisseurs ?", "Nous vous mettons en relation avec des fournisseurs de matériel partenaires, auprès desquels les membres du réseau bénéficient de conditions préférentielles. Vous commandez directement auprès du fournisseur."),
       ("Que dois-je vous transmettre pour un dossier CEE ?", "La description des travaux envisagés, puis les pièces et informations nécessaires au dossier. Nous vous indiquons ce qu’il faut à chaque étape."),
       ("Le versement des primes est-il garanti ?", "Non : le traitement du dossier et le versement des primes interviennent sous réserve de validation. Notre travail consiste à constituer et vérifier des dossiers conformes aux exigences du dispositif."),
       ("Comment rejoindre le réseau ?", "Remplissez le formulaire de la page « Rejoindre le réseau » : nous revenons vers vous pour échanger sur votre activité et vos besoins.")]
faq_all = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
faq_short = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[:4])

CHAIN = """<div class="chain">
      <div class="node rv"><div class="ic"><svg viewBox="0 0 24 24"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/></svg></div><h3>Artisans RGE</h3><p>Vous réalisez les travaux chez vos clients.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node core rv" style="--d:.12s"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie"><span class="pill">Votre réseau · mandataire CEE</span><p>Nous montons vos dossiers et vous accompagnons sur le reste.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node g rv" style="--d:.24s"><div class="ic"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="13" height="17" rx="2"/><path d="M7.5 8h6M7.5 11.5h6M7.5 15h3"/><circle cx="17.5" cy="17" r="4" fill="#5FA60E"/><path d="M19 15.8a2 2 0 1 0 0 2.4M15.6 16.5h2.4M15.6 17.6h2.4"/></svg></div><h3>Délégataires CEE</h3><p>Ils financent les primes, pour le compte des fournisseurs d’énergie obligés.</p></div>
    </div>"""
FLOW4 = """<div class="flow4 rv">
      <div class="f4"><h3>Les obligés</h3><p>Les fournisseurs d’énergie. L’État les oblige à financer des économies d’énergie.</p></div>
      <div class="f4"><h3>Les délégataires</h3><p>Les obligés leur délèguent cette obligation. Ce sont eux qui financent les primes CEE.</p></div>
      <div class="f4 me"><h3>Cercle Énergie, mandataire</h3><p>Nous faisons le lien entre vous et les délégataires, et nous prenons en charge l’administratif.</p></div>
      <div class="f4"><h3>Vous, artisan RGE</h3><p>Vous réalisez les travaux ; votre client bénéficie de la prime*.</p></div>
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
      <h3 class="full">Parlons de votre activité</h3>
      <label>Société<input id="f-societe" name="societe" autocomplete="organization" required></label>
      <label>Nom et prénom<input id="f-nom" name="nom" autocomplete="name" required></label>
      <label>Téléphone<input id="f-tel" name="telephone" type="tel" autocomplete="tel" required></label>
      <label>E-mail<input id="f-email" name="email" type="email" autocomplete="email" required></label>
      <label>Votre activité<select id="f-activite" name="activite" required><option value="">Sélectionnez…</option><option>Pompes à chaleur</option><option>Chauffage</option><option>Isolation</option><option>Ventilation / équipements thermiques</option><option>Rénovation énergétique</option><option>Autre</option></select></label>
      <label>Qualification RGE<select id="f-rge" name="rge"><option>Oui, je suis qualifié RGE</option><option>En cours</option><option>Pas encore</option></select></label>
      <label class="full">Ce sur quoi vous avez besoin d’aide (facultatif)<textarea id="f-message" name="message" rows="3"></textarea></label>
      <label class="check full"><input id="f-ok" type="checkbox" name="consentement" required><span>J’accepte d’être recontacté par Cercle Énergie au sujet de ma demande.</span></label>
      <button class="btn btn-primary full" type="submit">Envoyer ma demande {ARROW}</button>
      <p class="form-ok" role="status" id="form-ok">Merci ! Votre demande a bien été prise en compte.<br><small>(Version de démonstration : le formulaire n’est pas encore relié à une messagerie.)</small></p>
    </form>"""
JOIN = f"""<section class="join" id="partenaire">
  <div class="wrap form-grid">
    <div>
      <h2 class="rv">Rejoignez<br>le réseau.</h2>
      <p class="lead rv">Concentrez-vous sur vos chantiers et vos clients. Le réseau vous accompagne sur le reste.</p>
      <ol class="mini-steps rv">
        <li><b>Vous nous présentez votre activité</b>Métier, taille de l’entreprise, qualification RGE.</li>
        <li><b>Nous faisons le point sur vos besoins</b>Dossiers CEE, démarches, formation, qualification, fournisseurs.</li>
        <li><b>Nous vous accompagnons</b>Un interlocuteur, à chaque étape, sur chaque sujet.</li>
      </ol>
      <p class="note rv">* Sous réserve de validation du dossier.</p>
    </div>
    {FORM}
  </div>
</section>"""
CTA = f"""<section class="cta">
  <div class="wrap">
    <h2 class="rv">Rejoignez<br>le réseau.</h2>
    <p class="rv">Concentrez-vous sur vos chantiers et vos clients. Le réseau vous accompagne sur le reste.</p>
    <a class="btn btn-dark btn-xl rv" href="devenir-partenaire.html">Rejoindre le réseau {ARROW}</a>
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

P["index.html"] = ("Cercle Énergie — Le réseau d’accompagnement des artisans RGE",
 "Cercle Énergie accompagne les artisans RGE : dossiers CEE, démarches administratives, formation, qualification RGE et tarifs fournisseurs.", f"""
<section class="hero2" id="accueil">
  <video class="bgv" autoplay muted loop playsinline poster="assets/img/pac-installation.jpg"><source src="assets/video/hero.mp4" type="video/mp4"></video>
  <div class="shade"></div><div class="halo"></div><div class="halo b"></div>
  <div class="wrap">
    <span class="eyebrow">Le réseau des artisans RGE · Mandataire CEE</span>
    <h1 class="mega"><span class="ln" style="--i:0"><span>Artisan RGE ?</span></span><span class="ln" style="--i:1"><span>Vous n’êtes</span></span><span class="ln lime" style="--i:2"><span>plus seul.</span></span></h1>
    <div class="hero2-foot">
      <div><p class="lead">Cercle Énergie est un réseau d’accompagnement pour les artisans : dossiers CEE, démarches administratives, formation, qualification RGE et tarifs préférentiels auprès de fournisseurs partenaires.</p>
      <div class="proof"><span>Dossiers CEE pris en charge</span><span>Formation et qualification RGE</span><span>Tarifs fournisseurs partenaires</span></div></div>
      <div class="hero-cta" style="margin:0"><a class="btn btn-primary btn-xl" href="devenir-partenaire.html">Rejoindre le réseau {ARROW}</a><a class="btn btn-ghost btn-xl" href="#video">Voir la vidéo</a></div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="track">{MARQ}{MARQ}</div></div>
<section class="statement" id="constat">
  <div class="wrap split">
    <div><span class="eyebrow rv">Le constat</span>
      <p class="fill" data-fill data-green="9">Seul, un petit artisan passe ses soirées sur l’administratif. En réseau, il retrouve du temps pour ses chantiers et ses clients.</p></div>
    <div class="media rv"><img src="assets/img/paperasse.jpg" alt="Artisan débordé par les démarches administratives" loading="lazy"><span class="badge">Ce que vous n’arrivez pas à faire seul, on vous aide à le faire.</span></div>
  </div>
</section>
{VOLETS_SECTION}
<section class="tint" id="comparer">
  <div class="wrap center">
    <span class="eyebrow rv">Avant / après</span>
    <h2 class="rv">Seul, ou en réseau ?</h2>
    <div class="switch rv" id="switch" role="group" aria-label="Comparer"><span class="knob"></span><button type="button" data-v="sans" aria-pressed="true">Seul</button><button type="button" data-v="avec" aria-pressed="false">Avec Cercle Énergie</button></div>
    <div class="compare rv" id="compare">{cmp_html}</div>
  </div>
</section>
<section class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">Notre rôle</span>
    <h2 class="rv">Le lien entre vos chantiers<br>et le financement.</h2>
    <p class="lead rv">Mandataire CEE, Cercle Énergie travaille en collaboration avec des délégataires pour financer vos chantiers, et vous accompagne sur tout ce qui les entoure.</p>
    {CHAIN}
    <p class="rv" style="margin:48px auto 0"><a class="btn btn-ghost" href="comprendre-les-cee.html">Comment ça marche {ARROW}</a></p>
  </div>
</section>
<section id="services">
  <div class="wrap svc2">
    <div class="stick">
      <span class="eyebrow rv">Vos dossiers CEE</span>
      <h2 class="rv">Cinq étapes.<br>Un seul interlocuteur.</h2>
      <div class="bigno" id="bigno" aria-hidden="true">01</div>
    </div>
    <div class="rail" id="rail"><span class="fillbar" id="fillbar"></span>{s2_html}
      <p class="note">* Sous réserve de validation du dossier.</p>
      <p style="margin-top:24px"><a class="btn btn-line" href="services.html">Les dossiers CEE en détail {ARROW}</a></p>
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
    <h2 class="rv">Du temps. De la sécurité. Du poids.</h2>
    <div class="trio3">{b3_html}</div>
  </div>
</section>
<section id="video" class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span>
    <h2 class="rv">Cercle Énergie en vidéo</h2>
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

P["services.html"] = ("Dossiers CEE et primes — Cercle Énergie",
 "Étude d’éligibilité, valorisation financière, gestion administrative, accompagnement réglementaire et suivi du financement de vos dossiers CEE.",
 hero("remise-dossier.jpg", "Volet 1 · Dossiers CEE et primes", "De l’étude du projet jusqu’au financement.", "Le cœur de notre accompagnement : nous montons, vérifions et suivons vos dossiers CEE, en lien avec les délégataires.", [("accompagnement.html", "Le réseau"), (None, "Dossiers CEE")]) + f"""
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
    <span class="eyebrow rv">Et au-delà des dossiers</span><h2 class="rv">Les cinq autres appuis du réseau</h2>
    <div class="linkcards six">{voletcards_autres}</div>
  </div>
</section>
{CTA}""")

P["comprendre-les-cee.html"] = ("Comment ça marche — Cercle Énergie",
 "Les Certificats d’Économies d’Énergie expliqués simplement : qui finance, qui porte les dossiers, et le rôle de Cercle Énergie, mandataire CEE.",
 hero("renovation.jpg", "Comment ça marche", "Les primes CEE, expliquées simplement.", "Obligés, délégataires, mandataire : qui fait quoi, et où vous vous situez.", [(None, "Comment ça marche")]) + f"""
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Le principe</span>
    <h2 class="rv">Qui fait quoi dans un dossier CEE ?</h2>
    {FLOW4}
    <p class="note rv" style="margin-inline:auto">* Sous réserve de validation du dossier.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Le vocabulaire</span><h2 class="rv">Trois mots à connaître</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">Obligé</span><h3>Celui qui doit financer</h3><p>Un fournisseur d’énergie auquel l’État impose de faire réaliser des économies d’énergie.</p></div>
      <div class="box rv"><span class="n">Délégataire</span><h3>Celui qui finance pour lui</h3><p>Une structure à qui un obligé délègue son obligation. Le délégataire finance les primes CEE.</p></div>
      <div class="box rv"><span class="n">Mandataire</span><h3>Celui qui vous accompagne</h3><p>Cercle Énergie : le lien entre vous et le délégataire, et la prise en charge de l’administratif.</p></div>
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">Notre rôle</span>
    <h2 class="rv">Le lien entre vos chantiers<br>et le financement.</h2>
    <p class="lead rv">Mandataire CEE, Cercle Énergie travaille en collaboration avec des délégataires pour financer vos chantiers, et vous accompagne sur tout ce qui les entoure.</p>
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
      <ul class="ticks rv"><li>Vous vous concentrez sur vos chantiers et vos clients.</li><li>Nous prenons en charge la gestion administrative et financière de vos aides CEE.</li><li>Nous vous formons pour que le dispositif n’ait plus de secret pour vous.</li></ul>
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
 "Cercle Énergie, réseau d’accompagnement des artisans RGE et mandataire CEE : dossiers, démarches, formation, qualification, fournisseurs.",
 hero("reseau.jpg", "À propos", "Le partenaire unique de vos projets.", "Cercle Énergie est une structure d’accompagnement pour les artisans RGE, spécialisée dans les Certificats d’Économies d’Énergie.", [(None, "À propos")], "50% 30%") + f"""
<section>
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Qui sommes-nous</span>
      <h2 class="rv">Un réseau au service des petits artisans.</h2>
      <p class="lead rv">En qualité de mandataire, nous travaillons en collaboration avec des délégataires CEE afin d’accompagner les professionnels dans le financement de leurs projets de rénovation et d’efficacité énergétique.</p>
      <p class="rv" style="margin-top:18px">Notre rôle ne s’arrête pas au dossier : démarches administratives, formation, qualification RGE, tarifs fournisseurs. Nous aidons les artisans sur ce qu’ils n’arrivent pas à faire seuls.</p>
    </div>
    <div class="media rv"><img src="assets/img/remise-dossier.jpg" alt="Une conseillère remet un dossier à un artisan" loading="lazy"><span class="badge">Ce que vous n’arrivez pas à faire seul, on vous aide à le faire.</span></div>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <span class="eyebrow rv">Notre mission</span>
    <p class="bigquote rv">Permettre aux artisans de <em>se concentrer sur leur métier</em>, en leur apportant ce qu’un petit artisan n’a pas quand il est seul.</p>
    <div class="cols3">
      <div class="box rv"><span class="n">01</span><h3>Du temps</h3><p>Les dossiers et les démarches ne se font plus le soir.</p></div>
      <div class="box rv"><span class="n">02</span><h3>De la sécurité</h3><p>Des dossiers vérifiés, une qualification RGE suivie.</p></div>
      <div class="box rv"><span class="n">03</span><h3>Du poids</h3><p>Des tarifs fournisseurs et des financeurs que l’on n’a pas seul.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">L’accompagnement</span><h2 class="rv">Six appuis, un seul réseau</h2>
    <div class="linkcards six">{voletcards}</div>
  </div>
</section>
<section class="tint" id="video">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span><h2 class="rv">Cercle Énergie en vidéo</h2>
    <div class="video-frame rv"><video controls preload="none" poster="assets/img/video-poster.jpg"><source src="assets/video/presentation.mp4" type="video/mp4"></video></div>
  </div>
</section>
{CTA}""")

VP = [
 ("demarches-administratives.html", 2, "Démarches administratives", "paperasse.jpg", "L’administratif ne devrait pas décider de vos soirées.",
  "Les CEE, mais pas seulement. Quand une démarche vous bloque, vous avez quelqu’un à appeler.",
  "Vous bloquez ? On débloque.", "Un petit artisan n’a ni secrétariat ni service administratif. Devis, pièces justificatives, demandes de compléments : nous vous épaulons sur l’administratif qui entoure vos chantiers.",
  ["Les pièces à réunir, expliquées avant le chantier, pas après", "Des devis et des factures conformes à ce que les aides exigent", "Les demandes de compléments traitées avec vous"],
  "portrait-dossier.jpg",
  [("Avant le chantier", "Nous vous disons quoi préparer", "Les documents et les mentions attendus, pour ne pas découvrir un manque une fois les travaux finis."),
   ("Pendant", "Vous transmettez, nous contrôlons", "Vous nous envoyez vos pièces au fil de l’eau. Nous vérifions qu’il ne manque rien."),
   ("Après", "Nous suivons jusqu’au bout", "Relances, compléments, suivi du traitement : vous n’y passez plus vos soirées.")]),
 ("formation.html", 3, "Formation aux CEE", "formation.jpg", "Comprendre les primes, une bonne fois pour toutes.",
  "Nous vous formons au fonctionnement des CEE, pour que vous sachiez en parler à vos clients et monter des chantiers éligibles.",
  "Des règles claires, expliquées par ceux qui montent les dossiers.", "Les CEE ont leur vocabulaire, leurs pièces et leurs pièges. Nous vous les expliquons simplement, avec les cas que nous rencontrons tous les jours.",
  ["Comment fonctionnent les primes et qui les finance", "Les pièces d’un dossier conforme", "Les erreurs qui font refuser un dossier, et comment les éviter"],
  "portrait-conseillere.jpg",
  [("Le dispositif", "Obligés, délégataires, mandataire", "Qui fait quoi, et ce que cela change pour vous et pour votre client."),
   ("Le dossier", "Les pièces et les mentions", "Ce qu’il faut sur un devis, une facture et les documents à faire signer."),
   ("Le terrain", "Savoir en parler à vos clients", "Présenter la prime simplement, sans promettre ce qui dépend de la validation du dossier.")]),
 ("qualification-rge.html", 4, "Qualification RGE", "qualification-rge.jpg", "La qualification RGE, sans y laisser vos week-ends.",
  "Nous vous accompagnons pour obtenir votre qualification RGE, et pour la conserver.",
  "Un dossier de plus ? Pas tout seul.", "La qualification RGE ouvre l’accès aux chantiers aidés. La demande, les justificatifs et les contrôles demandent du temps et de la méthode : nous vous accompagnons à chaque étape.",
  ["Préparer votre demande et réunir les justificatifs", "Vous préparer aux contrôles de réalisation", "Suivre les échéances pour conserver votre qualification"],
  "portrait-artisan.jpg",
  [("Obtenir", "Monter votre demande", "Nous vous aidons à constituer le dossier demandé par l’organisme de qualification."),
   ("Conserver", "Rester à jour", "Nous vous aidons à anticiper les échéances et les contrôles qui jalonnent la qualification."),
   ("À savoir", "Qui délivre la qualification ?", "Un organisme de qualification, et lui seul. Cercle Énergie vous accompagne dans la démarche ; il ne délivre pas la qualification.")]),
 ("tarifs-fournisseurs.html", 5, "Tarifs fournisseurs", "fournisseur.jpg", "Seul, vous négociez. En réseau, vous pesez.",
  "Les membres du réseau accèdent à des conditions préférentielles auprès de fournisseurs de matériel partenaires.",
  "Le prix du matériel ne devrait pas dépendre de votre taille.", "Un petit artisan achète peu, donc cher. En rejoignant le réseau, vous êtes mis en relation avec des fournisseurs partenaires, à des conditions négociées pour l’ensemble des membres.",
  ["Une mise en relation avec des fournisseurs de matériel partenaires", "Des conditions préférentielles réservées aux membres du réseau", "Vous commandez directement auprès du fournisseur"],
  "pompe-a-chaleur.jpg",
  [("Le principe", "Le poids du réseau", "Les conditions sont négociées pour l’ensemble des membres, pas artisan par artisan."),
   ("En pratique", "Une mise en relation", "Nous vous présentons les fournisseurs partenaires qui correspondent à votre métier."),
   ("Vous restez libre", "Vos achats, vos choix", "Vous gardez la main sur votre matériel et sur vos commandes.")]),
 ("reseau.html", 6, "Un réseau", "reseau.jpg", "Petit artisan, pas artisan isolé.",
  "Un interlocuteur, des artisans comme vous, et le lien avec les délégataires CEE.",
  "Ce qu’un artisan n’a pas quand il est seul.", "Rejoindre Cercle Énergie, c’est ne plus avancer seul : quelqu’un à appeler, des règles expliquées, et un accès à des financeurs et à des fournisseurs que l’on n’a pas seul.",
  ["Un interlocuteur unique, pour tous vos sujets", "Le lien avec les délégataires qui financent les primes", "Des artisans qui partagent les mêmes chantiers et les mêmes contraintes"],
  "artisan-clients.jpg",
  [("Un interlocuteur", "Quelqu’un à appeler", "Une question sur un dossier, une pièce, une démarche : vous savez à qui la poser."),
   ("Des financeurs", "Le lien avec les délégataires", "Mandataire CEE, nous travaillons en collaboration avec des délégataires pour financer vos chantiers."),
   ("Des fournisseurs", "Des conditions de réseau", "Des tarifs préférentiels auprès de fournisseurs de matériel partenaires.")]),
]
VOLET_PAGES = {"services.html"} | {v[0] for v in VP}

P["accompagnement.html"] = ("L’accompagnement — Le réseau Cercle Énergie",
 "Dossiers CEE, démarches administratives, formation, qualification RGE, tarifs fournisseurs : les six appuis du réseau Cercle Énergie pour les artisans.",
 hero("reseau.jpg", "Le réseau", "Six appuis pour ne plus avancer seul.", "Ce que vous n’arrivez pas à faire seul, nous vous aidons à le faire.", [(None, "Le réseau")]) + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">L’accompagnement</span><h2 class="rv">Choisissez votre sujet</h2>
    <div class="linkcards six">{voletcards}</div>
    {NOTE}
  </div>
</section>
<section class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">Avant / après</span>
    <h2 class="rv">Seul, ou en réseau ?</h2>
    <div class="switch rv" id="switch" role="group" aria-label="Comparer"><span class="knob"></span><button type="button" data-v="sans" aria-pressed="true">Seul</button><button type="button" data-v="avec" aria-pressed="false">Avec Cercle Énergie</button></div>
    <div class="compare rv" id="compare">{cmp_html}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Pour qui</span><h2 class="rv">Le réseau est fait pour vous si…</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">01</span><h3>Vous posez des pompes à chaleur</h3><p>Vos chantiers sont éligibles aux primes, et les dossiers vous prennent trop de temps.</p></div>
      <div class="box rv"><span class="n">02</span><h3>Vous êtes un petit artisan</h3><p>Seul ou à quelques-uns, sans personne pour l’administratif ni pour négocier vos achats.</p></div>
      <div class="box rv"><span class="n">03</span><h3>Vous êtes qualifié RGE</h3><p>Ou vous préparez votre qualification, et vous voulez en tirer parti sur vos chantiers.</p></div>
    </div>
  </div>
</section>
{CTA}""")

for i, (h, n, t, img, h1, lead, h2, intro, ticks, img2, boxes) in enumerate(VP):
    nh, nt = (VP[i + 1][0], VP[i + 1][2]) if i + 1 < len(VP) else ("services.html", "Dossiers CEE et primes")
    P[h] = (f"{t} — Cercle Énergie", lead,
     hero(img, f"Volet {n} · {t}", h1, lead, [("accompagnement.html", "Le réseau"), (None, t)], "50% 40%") + f"""
<section>
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Ce que nous faisons</span>
      <h2 class="rv">{h2}</h2>
      <p class="lead rv">{intro}</p>
      <ul class="ticks rv">{"".join(f"<li>{x}</li>" for x in ticks)}</ul>
    </div>
    <div class="media rv"><img src="assets/img/{img2}" alt="" loading="lazy"></div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Concrètement</span><h2 class="rv">Comment cela se passe</h2>
    <div class="cols3">{"".join(f'<div class="box rv"><span class="n">{a}</span><h3>{b}</h3><p>{c}</p></div>' for a, b, c in boxes)}</div>
    <div class="nextprev rv"><a class="btn btn-line" href="accompagnement.html">Tout l’accompagnement {ARROW}</a><a class="btn btn-line" href="{nh}">Volet suivant : {nt} {ARROW}</a></div>
  </div>
</section>
{CTA}""")

P["faq.html"] = ("Questions fréquentes — Cercle Énergie",
 "Les réponses aux questions les plus fréquentes sur les CEE, le rôle de Cercle Énergie et le partenariat.",
 hero("portrait-conseillere.jpg", "Questions fréquentes", "Vos questions, nos réponses.", "L’essentiel à savoir sur le réseau, les CEE et notre rôle de mandataire.", [(None, "FAQ")], "50% 25%") + f"""
<section>
  <div class="wrap center">
    <div class="faq" style="text-align:left;margin-top:0">{faq_all}</div>
    <p class="rv" style="margin:44px auto 0">Une autre question ? <a class="hl" href="contact.html" style="font-weight:700">Contactez-nous</a>.</p>
  </div>
</section>
{CTA}""")

P["devenir-partenaire.html"] = ("Rejoindre le réseau — Cercle Énergie",
 "Artisans RGE : rejoignez le réseau Cercle Énergie pour vos dossiers CEE, vos démarches, votre formation, votre qualification et vos achats.",
 hero("reseau.jpg", "Rejoindre le réseau", "Rejoignez un réseau qui vous épaule.", "Dossiers CEE, démarches administratives, formation, qualification RGE, tarifs fournisseurs : un seul interlocuteur.", [(None, "Rejoindre le réseau")]) + f"""
{JOIN}
<section>
  <div class="wrap">
    <span class="eyebrow rv">Pourquoi nous rejoindre</span><h2 class="rv">Du temps. De la sécurité. Du poids.</h2>
    <div class="trio3">{b3_html}</div>
  </div>
</section>
<section class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">Avant de vous lancer</h2>
    <div class="faq" style="text-align:left">{"".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[4:])}</div>
  </div>
</section>""")

P["contact.html"] = ("Contact — Cercle Énergie", "Contactez Cercle Énergie, réseau d’accompagnement des artisans RGE et mandataire CEE.",
 hero("remise-dossier.jpg", "Contact", "Parlons de votre activité.", "Une question sur le réseau, les CEE ou notre accompagnement ? Écrivez-nous.", [(None, "Contact")]) + f"""
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
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if (h == fname or (h == "secteurs.html" and fname.startswith("secteur-")) or (h == "accompagnement.html" and fname in VOLET_PAGES)) else ""}>{t}</a>' for h, t in NAV)
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
    <nav class="nav" aria-label="Navigation principale">{links}<a class="btn btn-primary" href="devenir-partenaire.html">Rejoindre le réseau {ARROW}</a></nav>
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
        <p style="margin-top:20px;max-width:38ch">Réseau d’accompagnement des artisans RGE et mandataire CEE : dossiers, démarches, formation, qualification, fournisseurs.</p>
      </div>
      <div><h4>Le réseau</h4><ul><li><a href="accompagnement.html">L’accompagnement</a></li><li><a href="services.html">Dossiers CEE et primes</a></li><li><a href="demarches-administratives.html">Démarches administratives</a></li><li><a href="formation.html">Formation aux CEE</a></li><li><a href="qualification-rge.html">Qualification RGE</a></li><li><a href="tarifs-fournisseurs.html">Tarifs fournisseurs</a></li></ul></div>
      <div><h4>Le site</h4><ul><li><a href="comprendre-les-cee.html">Comment ça marche</a></li><li><a href="secteurs.html">Secteurs</a></li><li><a href="a-propos.html">À propos</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="plaquette.pdf">Plaquette (PDF)</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="devenir-partenaire.html">Rejoindre le réseau</a></li><li><a href="contact.html">Nous contacter</a></li><li>[Téléphone à compléter]</li><li>[E-mail à compléter]</li></ul></div>
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
