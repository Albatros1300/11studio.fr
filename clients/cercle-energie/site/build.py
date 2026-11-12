#!/usr/bin/env python3
"""Génère le site statique multi-pages Cercle Énergie (cadrage : brief de marque, novembre 2026).
Usage : python3 build.py  (écrit les .html à côté de ce fichier)"""
import pathlib

ROOT = pathlib.Path(__file__).parent
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NAV = [("accompagnement.html", "Le Cercle"), ("parcours.html", "Parcours de A à Z"), ("services.html", "Financement CEE"), ("comprendre-les-cee.html", "Comprendre les CEE"), ("a-propos.html", "À propos")]
NOTE = '<p class="note rv">* Selon les conditions contractuelles et la validation des dossiers.</p>'
CERCLE_PAGES = {"visite-technique.html", "suivi-dossiers.html", "equipements.html"}

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
    ("Suivi du financement", "Nous suivons le dossier jusqu’à son traitement et au versement des primes*.",
     ["Coordination", "Suivi du traitement", "Information à chaque avancée"],
     "Les compléments éventuellement demandés.", "Un suivi jusqu’au versement des primes*."),
]
s2_html = "".join(
    f'<div class="s2" data-n="0{i+1}"><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>'
    for i, (t, d, li, _a, _b) in enumerate(STEPS))
detail_html = "".join(
    f'<article class="rv" id="etape-{i+1}"><div class="num">0{i+1}</div><div><h3>{t}</h3><p style="margin-top:10px">{d}</p></div>'
    f'<ul><li><b>Vous nous transmettez :</b> {a}</li><li><b>Vous obtenez :</b> {b}</li></ul></article>'
    for i, (t, d, li, a, b) in enumerate(STEPS))


MARQ = "".join(f"<span>{t}</span>" for t in ["Pompes à chaleur air/eau", "Pompes à chaleur air/air", "Chauffe-eau thermodynamiques", "Isolation", "Visite technique", "Équipements", "Dossiers CEE", "Suivi jusqu’à la prime"])
CMP = [("Équipements", "Des offres de négoces et de fabricants difficiles à comparer", "Un accès simplifié à des équipements de qualité"),
       ("Aides", "Des règles complexes et mouvantes à interpréter seul", "Des règles expliquées, des aides identifiées"),
       ("Dossiers", "À monter, à relancer et à suivre vous-même", "Préparés, contrôlés et suivis, avec une visibilité sur leur avancement"),
       ("Parcours", "Une chaîne morcelée, de la visite à la prime", "Un seul interlocuteur, du premier contact à la prime*")]
cmp_html = "".join(f'<div class="cmp" style="--i:{i}"><small>{k}</small><p class="a">{a}</p><p class="b">{b}</p><i></i></div>' for i, (k, a, b) in enumerate(CMP))

PILIERS = [("Simplicité", "Un interlocuteur identifié, des étapes claires et des informations compréhensibles."),
           ("Confiance", "Des dossiers rigoureux, une communication transparente et une culture de conformité."),
           ("Performance", "Des outils et des services qui font gagner du temps et aident à convertir les projets."),
           ("Proximité", "Un langage de terrain, des échanges humains et une connaissance des contraintes des installateurs.")]
piliers_html = '<div class="cols4">' + "".join(f'<div class="box rv" style="--d:{i*.08:.2f}s"><span class="n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PILIERS)) + "</div>"

PARCOURS = [
    ("Opportunité", "Vous aider à accéder à des projets qualifiés et à mieux organiser la prise de contact avec vos prospects."),
    ("Qualification du projet", "Comprendre le besoin du client, le logement, l’équipement envisagé et les conditions d’éligibilité."),
    ("Visite technique", "Structurer les relevés, fiabiliser les informations et faciliter votre travail, notamment avec le logiciel WOLTIC."),
    ("Choix des équipements", "Vous donner accès à une offre de matériels de qualité, notamment via des marques telles que Hitachi ou Thomson, selon les accords et gammes disponibles."),
    ("Devis et financement", "Vous aider à présenter un projet lisible, à identifier les aides mobilisables et à expliquer le reste à charge."),
    ("Chantier et justificatifs", "Accompagner la collecte des documents, les points de conformité et la traçabilité du dossier."),
    ("Montage et suivi CEE", "Préparer, contrôler et suivre vos dossiers, avec une visibilité sur leur état d’avancement."),
    ("Versement de la prime", "Accompagner le suivi jusqu’au paiement, selon les conditions contractuelles et la validation des dossiers."),
]
p8_html = "".join(f'<div class="s2" data-n="0{i+1}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PARCOURS))
p8_detail = "".join(f'<article class="rv p8" id="etape-{i+1}"><div class="num">0{i+1}</div><div><h3>{t}</h3><p style="margin-top:10px">{d}</p></div></article>' for i, (t, d) in enumerate(PARCOURS))

CERCLE = [
    ("services.html", "Le financement CEE", "remise-dossier.jpg", "Notre cœur de métier : des règles expliquées, des dossiers constitués, contrôlés et suivis jusqu’au paiement des primes*."),
    ("visite-technique.html", "La visite technique", "artisan-clients.jpg", "WOLTIC, le logiciel utilisé pour les visites techniques, aide à structurer la collecte des informations terrain."),
    ("suivi-dossiers.html", "Un suivi humain", "qualification-rge.jpg", "Une équipe d’experts dédiée, et une visibilité sur l’avancement de vos dossiers."),
    ("equipements.html", "Des équipements sélectionnés", "fournisseur.jpg", "Un accès simplifié à des équipements de qualité, selon les accords et gammes disponibles."),
    ("parcours.html", "Le parcours de A à Z", "pac-installation.jpg", "Huit étapes, du premier contact au versement de la prime*."),
    ("comprendre-les-cee.html", "Comprendre les CEE", "formation.jpg", "Le dispositif, les documents à anticiper, les points de vigilance : nous expliquons."),
]
cerclecards = "".join(
    f'<a class="lc rv" style="--d:{(i%3)*.08:.2f}s" href="{h}"><img src="assets/img/{img}" alt="" loading="lazy"><div><span class="vn">0{i+1}</span><h3>{t}</h3><p>{k}</p><span class="go">Découvrir {ARROW}</span></div></a>'
    for i, (h, t, img, k) in enumerate(CERCLE))
CERCLE_SECTION = f"""<section id="cercle">
  <div class="wrap">
    <span class="eyebrow rv">Un cercle de confiance</span>
    <h2 class="rv">Du premier contact au paiement de la prime*,<br>un seul cercle de services.</h2>
    <p class="lead rv">Nous ne sommes pas un simple mandataire qui collecte des dossiers. Nous voulons être votre point d’entrée unique vers les services, les outils, les financements et les partenaires dont vous avez besoin.</p>
    <div class="linkcards six">{cerclecards}</div>
    {NOTE}
  </div>
</section>"""

FAQ = [("Que sont les Certificats d’Économies d’Énergie (CEE) ?", "Un dispositif d’État qui oblige les fournisseurs d’énergie et les distributeurs de carburant, appelés « obligés », à financer des travaux de rénovation énergétique, sous peine de pénalités. Pour vos clients, cela se traduit par des primes sur les travaux éligibles."),
       ("Qu’est-ce qu’un mandataire CEE ?", "Une société de services spécialisée qui aide les obligés à réaliser leurs obligations. Elle est experte du montage des dossiers administratifs, des règles fixées par l’État et de l’accompagnement des entreprises de travaux. C’est le métier de Cercle Énergie, mandataire CEE de la 6e période."),
       ("En quoi Cercle Énergie est-il différent ?", "Nous ne voulons pas être un simple mandataire qui collecte des dossiers. Nous accompagnons l’installateur sur tout le parcours : qualification du projet, visite technique, choix des équipements, devis, justificatifs, montage et suivi du dossier, jusqu’au versement de la prime."),
       ("À qui s’adresse Cercle Énergie ?", "D’abord aux artisans chauffagistes et aux entreprises de génie climatique, notamment les professionnels RGE, qui posent chez les particuliers des pompes à chaleur air/eau, des pompes à chaleur air/air lorsque les dispositifs le permettent, et des chauffe-eau thermodynamiques. Les spécialistes de l’isolation sont aussi concernés."),
       ("Le versement des primes est-il garanti ?", "Non. Le paiement intervient selon les conditions contractuelles et la validation des dossiers. Notre travail consiste à expliquer les règles, à préparer des dossiers rigoureux et à les suivre jusqu’au bout."),
       ("Qu’est-ce que WOLTIC ?", "Le logiciel utilisé pour réaliser les visites techniques : il aide à structurer la collecte des informations sur le terrain."),
       ("Proposez-vous du matériel ?", "En complément de notre accompagnement, nous proposons un accès simplifié à des équipements de qualité, notamment via des marques telles que Hitachi ou Thomson, selon les accords et gammes disponibles. Nous ne sommes pas un négociant généraliste."),
       ("Comment suivre l’avancement de mes dossiers ?", "Nos équipes suivent chaque dossier, du montage au paiement, et vous tiennent informé de son état d’avancement. Vous avez un interlocuteur identifié."),
       ("Que dois-je vous transmettre pour un dossier CEE ?", "La description des travaux envisagés, puis les pièces et informations nécessaires au dossier. Nous vous indiquons ce qu’il faut à chaque étape, le plus tôt possible."),
       ("Comment travailler avec vous ?", "Par un premier échange : remplissez le formulaire « Parlons de vos projets », nous revenons vers vous pour comprendre votre activité et vos besoins.")]
faq_all = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
faq_short = "".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[:5])

FLOW4 = """<div class="flow4 rv">
      <div class="f4"><h3>L’État fixe la règle</h3><p>Le dispositif CEE oblige certains acteurs de l’énergie à financer des travaux de rénovation énergétique.</p></div>
      <div class="f4"><h3>Les obligés financent</h3><p>Fournisseurs d’énergie et distributeurs de carburant, sous peine de pénalités.</p></div>
      <div class="f4 me"><h3>Cercle Énergie, mandataire</h3><p>Nous aidons les obligés à réaliser leurs obligations : montage des dossiers, respect des règles, accompagnement des entreprises de travaux.</p></div>
      <div class="f4"><h3>Vous, installateur</h3><p>Vous réalisez les travaux ; votre client bénéficie de la prime*.</p></div>
    </div>"""

PANELS = [("pompe-a-chaleur.jpg", "Pompes à chaleur", "Pompes à chaleur air/eau, et air/air lorsque les dispositifs le permettent."),
          ("chauffage.jpg", "Chauffe-eau thermodynamiques", "Chauffe-eau thermodynamiques et équipements thermiques chez les particuliers."),
          ("isolation-combles.jpg", "Isolation", "Entreprises spécialisées dans l’isolation des logements."),
          ("renovation.jpg", "Rénovation énergétique", "Entreprises de rénovation énergétique et entreprises générales du bâtiment."),
          ("tertiaire.jpg", "Tertiaire", "Bureaux, commerces, établissements recevant du public."),
          ("industrie.jpg", "Industrie", "Sites de production, utilités et équipements thermiques."),
          ("agricole.jpg", "Agricole", "Exploitations, serres et bâtiments d’élevage.")]
panels_html = "".join(
    f'<article class="panel{" on" if i == 0 else ""}" tabindex="0"><img src="assets/img/{img}" alt="{t}" loading="lazy"><span class="no">0{i+1}</span><span class="lab">{t}</span><div class="in"><h3>{t}</h3><p>{d}</p></div></article>'
    for i, (img, t, d) in enumerate(PANELS))

WHO = [("Réalisation des travaux", 1, 0, 0), ("Étude d’éligibilité", 0, 1, 0), ("Recherche de valorisation", 0, 1, 0),
       ("Constitution et vérification du dossier", 0, 1, 0), ("Suivi et coordination", 0, 1, 0), ("Financement des CEE", 0, 0, 1)]
dot = lambda v: '<span class="dot"></span>' if v else '<span class="dot o"></span>'
who_html = "".join(f"<tr><th scope='row'>{t}</th><td>{dot(a)}</td><td>{dot(b)}</td><td>{dot(c)}</td></tr>" for t, a, b, c in WHO)
WHO_TABLE = f'<div class="table-scroll rv"><table class="who"><thead><tr><th scope="col">Étape</th><th scope="col">Vous</th><th scope="col">Cercle Énergie</th><th scope="col">Financeur (obligé)</th></tr></thead><tbody>{who_html}</tbody></table></div>'

CHAIN = """<div class="chain">
      <div class="node rv"><div class="ic"><svg viewBox="0 0 24 24"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/></svg></div><h3>Vous, installateur</h3><p>Vous conseillez, dimensionnez et installez chez vos clients.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node core rv" style="--d:.12s"><img src="assets/img/logo_mark_t.png" alt="Cercle Énergie"><span class="pill">Mandataire CEE · votre partenaire</span><p>Nous préparons, contrôlons et suivons vos dossiers, à vos côtés.</p></div>
      <div class="flow" aria-hidden="true"><i></i><i></i></div>
      <div class="node g rv" style="--d:.24s"><div class="ic"><svg viewBox="0 0 24 24"><rect x="4" y="3" width="13" height="17" rx="2"/><path d="M7.5 8h6M7.5 11.5h6M7.5 15h3"/><circle cx="17.5" cy="17" r="4" fill="#5FA60E"/><path d="M19 15.8a2 2 0 1 0 0 2.4M15.6 16.5h2.4M15.6 17.6h2.4"/></svg></div><h3>Les obligés</h3><p>Fournisseurs d’énergie et distributeurs de carburant : le dispositif les oblige à financer des travaux.</p></div>
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
      <h3 class="full">Parlons de vos projets</h3>
      <label>Société<input id="f-societe" name="societe" autocomplete="organization" required></label>
      <label>Nom et prénom<input id="f-nom" name="nom" autocomplete="name" required></label>
      <label>Téléphone<input id="f-tel" name="telephone" type="tel" autocomplete="tel" required></label>
      <label>E-mail<input id="f-email" name="email" type="email" autocomplete="email" required></label>
      <label>Votre activité principale<select id="f-activite" name="activite" required><option value="">Sélectionnez…</option><option>Pompes à chaleur air/eau</option><option>Pompes à chaleur air/air</option><option>Chauffe-eau thermodynamiques</option><option>Isolation</option><option>Autre</option></select></label>
      <label>Qualification RGE<select id="f-rge" name="rge"><option>Oui</option><option>En cours</option><option>Non</option></select></label>
      <label class="full">Votre besoin (facultatif)<textarea id="f-message" name="message" rows="3"></textarea></label>
      <label class="check full"><input id="f-ok" type="checkbox" name="consentement" required><span>J’accepte d’être recontacté par Cercle Énergie au sujet de ma demande.</span></label>
      <button class="btn btn-primary full" type="submit">Demander un échange {ARROW}</button>
      <p class="form-ok" role="status" id="form-ok">Merci ! Votre demande a bien été prise en compte.<br><small>(Version de démonstration : le formulaire n’est pas encore relié à une messagerie.)</small></p>
    </form>"""
JOIN = f"""<section class="join" id="partenaire">
  <div class="wrap form-grid">
    <div>
      <h2 class="rv">Parlons de<br>vos projets.</h2>
      <p class="lead rv">Un premier échange, sans engagement, pour comprendre votre activité et voir comment nous pouvons vous accompagner.</p>
      <ol class="mini-steps rv">
        <li><b>Vous nous présentez votre activité</b>Métier, type de chantiers, organisation.</li>
        <li><b>Nous faisons le point ensemble</b>Vos projets, vos dossiers, ce qui vous prend du temps.</li>
        <li><b>Nous vous accompagnons</b>Un interlocuteur identifié, à chaque étape.</li>
      </ol>
    </div>
    {FORM}
  </div>
</section>"""
CTA = f"""<section class="cta">
  <div class="wrap">
    <h2 class="rv">Parlons de<br>vos projets.</h2>
    <p class="rv">Moins de temps dans l’administratif, plus de temps sur vos chantiers.</p>
    <a class="btn btn-dark btn-xl rv" href="devenir-partenaire.html">Demander un échange {ARROW}</a>
  </div>
</section>"""
VIDEO = """<div class="video-frame rv"><video controls preload="none" poster="assets/img/video-poster.jpg"><source src="assets/video/presentation.mp4" type="video/mp4">Votre navigateur ne peut pas lire cette vidéo.</video></div>"""


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

P["index.html"] = ("Cercle Énergie — Le partenaire unique de vos projets | Mandataire CEE",
 "Cercle Énergie, mandataire CEE, accompagne les installateurs de pompes à chaleur, de chauffe-eau thermodynamiques et d’isolation, du premier contact au versement de la prime.", f"""
<section class="hero2" id="accueil">
  <video class="bgv" autoplay muted loop playsinline poster="assets/img/pac-installation.jpg"><source src="assets/video/hero.mp4" type="video/mp4"></video>
  <div class="shade"></div><div class="halo"></div><div class="halo b"></div>
  <div class="wrap">
    <span class="eyebrow">Le partenaire unique de vos projets · Mandataire CEE de la 6e période</span>
    <h1 class="mega"><span class="ln" style="--i:0"><span>Vous installez.</span></span><span class="ln lime" style="--i:1"><span>Nous vous</span></span><span class="ln lime" style="--i:2"><span>accompagnons</span></span><span class="ln lime" style="--i:3"><span>à chaque étape.</span></span></h1>
    <div class="hero2-foot">
      <div><p class="lead">Moins de complexité, plus de visibilité et un accompagnement concret : du premier contact commercial au versement de la prime*.</p>
      <div class="proof"><span>Un interlocuteur identifié</span><span>Des règles expliquées</span><span>Des dossiers suivis</span></div></div>
      <div class="hero-cta" style="margin:0"><a class="btn btn-primary btn-xl" href="devenir-partenaire.html">Parlons de vos projets {ARROW}</a><a class="btn btn-ghost btn-xl" href="#video">Voir la vidéo</a></div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="track">{MARQ}{MARQ}</div></div>
<section class="statement" id="constat">
  <div class="wrap split">
    <div><span class="eyebrow rv">Votre quotidien</span>
      <p class="fill" data-fill data-green="17">Conseiller, installer, satisfaire vos clients, c’est votre métier. Comparer des offres, décrypter les aides, relancer des dossiers, on le fait avec vous.</p></div>
    <div class="media rv"><img src="assets/img/paperasse.jpg" alt="Artisan devant ses dossiers, le soir" loading="lazy"><span class="badge">Moins de temps dans l’administratif, plus de temps sur vos chantiers.</span></div>
  </div>
</section>
{CERCLE_SECTION}
<section class="tint" id="comparer">
  <div class="wrap center">
    <span class="eyebrow rv">Avant / après</span>
    <h2 class="rv">Tout gérer seul, ou être accompagné ?</h2>
    <div class="switch rv" id="switch" role="group" aria-label="Comparer"><span class="knob"></span><button type="button" data-v="sans" aria-pressed="true">Seul</button><button type="button" data-v="avec" aria-pressed="false">Avec Cercle Énergie</button></div>
    <div class="compare rv" id="compare">{cmp_html}</div>
    <p class="note rv" style="margin-inline:auto">* Selon les conditions contractuelles et la validation des dossiers.</p>
  </div>
</section>
<section id="parcours">
  <div class="wrap svc2">
    <div class="stick">
      <span class="eyebrow rv">Le parcours de A à Z</span>
      <h2 class="rv">Huit étapes.<br>Un seul cercle.</h2>
      <div class="bigno" id="bigno" aria-hidden="true">01</div>
    </div>
    <div class="rail" id="rail"><span class="fillbar" id="fillbar"></span>{p8_html}
      <p style="margin-top:24px"><a class="btn btn-line" href="parcours.html">Le parcours en détail {ARROW}</a></p>
    </div>
  </div>
</section>
<section class="dark" id="piliers">
  <div class="wrap">
    <span class="eyebrow rv">Notre façon de travailler</span>
    <h2 class="rv">Expliquer plutôt que promettre.<br>Sécuriser plutôt que compliquer.</h2>
    {piliers_html}
  </div>
</section>
<section id="video" class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span>
    <h2 class="rv">Cercle Énergie en vidéo</h2>
    {VIDEO}
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

P["accompagnement.html"] = ("Le Cercle — Un seul cercle de services | Cercle Énergie",
 "Financement CEE, visite technique, suivi des dossiers, équipements : Cercle Énergie fédère autour de l’installateur les services dont il a besoin.",
 hero("reseau.jpg", "Le Cercle", "Un cercle de confiance autour de l’installateur.", "Le cercle, c’est la continuité de l’accompagnement, la proximité et la coopération : un point d’entrée unique vers les services, les outils, les financements et les partenaires.", [(None, "Le Cercle")]) + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">Nos services</span><h2 class="rv">Les bons équipements, les bons outils,<br>le bon accompagnement.</h2>
    <div class="linkcards six">{cerclecards}</div>
    {NOTE}
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <span class="eyebrow rv">Les quatre piliers</span><h2 class="rv">Ce que vous pouvez attendre de nous</h2>
    {piliers_html}
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">À qui nous parlons</span><h2 class="rv">Des professionnels de terrain</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">01</span><h3>Chauffagistes et génie climatique</h3><p>Pompes à chaleur air/eau, pompes à chaleur air/air lorsque les dispositifs le permettent, chauffe-eau thermodynamiques.</p></div>
      <div class="box rv"><span class="n">02</span><h3>Spécialistes de l’isolation</h3><p>Les entreprises qui interviennent sur l’enveloppe des logements.</p></div>
      <div class="box rv"><span class="n">03</span><h3>Artisans RGE, près de chez leurs clients</h3><p>Des professionnels qui font des chantiers de qualité chez les particuliers, et qui veulent y consacrer leur temps.</p></div>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Et demain</span>
    <h2 class="rv">Un cercle qui s’élargit</h2>
    <p class="lead rv" style="max-width:62ch">Le cercle a vocation à s’ouvrir à d’autres services utiles aux installateurs : appui commercial, outils digitaux, formation, accompagnement technique, nouveaux partenariats. Nous les annoncerons lorsqu’ils seront disponibles.</p>
  </div>
</section>
{CTA}""")

P["parcours.html"] = ("Le parcours de A à Z — Cercle Énergie",
 "Les huit étapes de l’accompagnement Cercle Énergie, de l’opportunité au versement de la prime.",
 hero("pac-installation.jpg", "Le parcours de A à Z", "Présents à chaque étape de vos projets.", "De l’opportunité au versement de la prime* : huit étapes, un seul interlocuteur.", [(None, "Parcours de A à Z")], "60% 50%") + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">Huit étapes</span><h2 class="rv">Ce que nous faisons, étape par étape</h2>
    <div class="detail">{p8_detail}</div>
    {NOTE}
    <p class="rv" style="margin-top:28px"><a class="btn btn-line" href="plaquette.pdf">Télécharger la présentation (PDF) {ARROW}</a></p>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Répartition des rôles</span><h2 class="rv">Avec vous, jamais à votre place.</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">Vous</span><h3>Le métier</h3><p>Vous conseillez, dimensionnez, installez et restez l’interlocuteur de votre client.</p></div>
      <div class="box rv"><span class="n">Cercle Énergie</span><h3>L’accompagnement</h3><p>Nous expliquons les règles, préparons et contrôlons les dossiers, et les suivons jusqu’au paiement*.</p></div>
      <div class="box rv"><span class="n">Ensemble</span><h3>Des projets solides</h3><p>Des informations fiables dès la visite technique, des justificatifs anticipés, un dossier tracé.</p></div>
    </div>
  </div>
</section>
{CTA}""")

P["services.html"] = ("Le financement CEE — Cercle Énergie",
 "Le cœur de métier de Cercle Énergie : compréhension des règles, constitution des dossiers, contrôles documentaires, suivi et paiement des primes CEE.",
 hero("remise-dossier.jpg", "Notre cœur de métier", "Le financement CEE, expliqué et suivi.", "Compréhension des règles, constitution des dossiers, contrôles documentaires, suivi des étapes et paiement des primes* : une équipe d’experts dédiée.", [("accompagnement.html", "Le Cercle"), (None, "Financement CEE")]) + f"""
<section>
  <div class="wrap">
    <span class="eyebrow rv">Un dossier CEE, cinq étapes</span><h2 class="rv">Ce que nous faisons pour vos dossiers</h2>
    <div class="detail">{detail_html}</div>
    {NOTE}
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Répartition des rôles</span><h2 class="rv">Vous, sur le chantier.<br>Nous, à vos côtés sur le dossier.</h2>
    {WHO_TABLE}
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <span class="eyebrow rv">Notre engagement</span>
    <p class="bigquote rv">Des dossiers suivis, des règles expliquées, <em>un partenaire à vos côtés.</em></p>
    <div class="cols3">
      <div class="box rv"><span class="n">Pédagogie</span><h3>Nous expliquons</h3><p>Les étapes, les conditions, les contrôles et les responsabilités de chacun.</p></div>
      <div class="box rv"><span class="n">Conformité</span><h3>Nous contrôlons</h3><p>Des dossiers rigoureux, vérifiés au regard des exigences du dispositif.</p></div>
      <div class="box rv"><span class="n">Transparence</span><h3>Nous ne promettons pas l’impossible</h3><p>Pas de prime « garantie » : le paiement dépend des conditions contractuelles et de la validation des dossiers.</p></div>
    </div>
  </div>
</section>
{CTA}""")

VP = [
 ("visite-technique.html", "La visite technique", "artisan-clients.jpg", "Une visite technique structurée, des projets plus solides.",
  "WOLTIC est le logiciel utilisé pour réaliser les visites techniques : il aide à structurer la collecte des informations sur le terrain.",
  "Tout commence par des informations fiables.", "Un relevé incomplet, et c’est le devis, le dimensionnement ou le dossier qui en pâtit. La visite technique est l’étape où se joue la qualité du projet.",
  ["Structurer les relevés", "Fiabiliser les informations recueillies chez le client", "Faciliter votre travail d’installateur"],
  "pac-installation.jpg",
  [("Sur le terrain", "Un relevé structuré", "Les informations utiles au projet sont collectées de façon ordonnée pendant la visite."),
   ("Pour le devis", "Un projet lisible", "Des informations fiables aident à présenter le projet, à identifier les aides mobilisables et à expliquer le reste à charge."),
   ("Pour le dossier", "Moins d’allers-retours", "Ce qui est bien relevé dès la visite n’a pas à être redemandé ensuite.")]),
 ("suivi-dossiers.html", "Un suivi humain", "qualification-rge.jpg", "Vos dossiers suivis par des personnes, pas par un guichet.",
  "Une équipe d’experts dédiée accompagne le montage, le suivi et le traitement de vos dossiers CEE, jusqu’au paiement des primes*.",
  "Vous savez où en sont vos dossiers.", "Nous ne sommes pas une plateforme de dépôt. Chaque dossier est préparé, contrôlé et suivi par nos équipes, qui vous tiennent informé de son avancement.",
  ["Un interlocuteur identifié", "Une visibilité sur l’état d’avancement de vos dossiers", "Des réponses, pas des renvois"],
  "portrait-conseillere.jpg",
  [("Pendant le chantier", "Les justificatifs, au fil de l’eau", "Nous accompagnons la collecte des documents, les points de conformité et la traçabilité du dossier."),
   ("Après le chantier", "Préparé, contrôlé, suivi", "Le dossier est monté et vérifié par nos équipes, puis suivi à chaque étape de son traitement."),
   ("Jusqu’au bout", "Jusqu’au paiement*", "Nous accompagnons le suivi jusqu’au versement de la prime, selon les conditions contractuelles et la validation des dossiers.")]),
 ("equipements.html", "Des équipements sélectionnés", "fournisseur.jpg", "Les bons équipements, les bons outils, le bon accompagnement.",
  "En complément de notre accompagnement, un accès simplifié à des équipements de qualité, selon les accords et gammes disponibles.",
  "Comparer les offres ne devrait pas vous prendre des heures.", "Prix, disponibilité, qualité, support, conditions commerciales : les offres des négoces et des fabricants sont difficiles à comparer. Nous vous donnons accès à une offre de matériels de qualité, notamment via des marques telles que Hitachi ou Thomson, selon les accords et gammes disponibles.",
  ["Une cohérence technique avec vos chantiers", "Un choix adapté au projet", "Un accompagnement commercial"],
  "pompe-a-chaleur.jpg",
  [("Notre rôle", "Un accès simplifié", "Nous ne sommes pas un négociant généraliste : nous facilitons l’accès à des équipements sélectionnés."),
   ("Votre liberté", "Vos choix techniques", "Vous restez maître du dimensionnement et du matériel que vous posez."),
   ("À savoir", "Selon les accords en vigueur", "Les marques, les gammes et les conditions dépendent des partenariats et de l’approvisionnement effectifs.")]),
]
for i, (h, t, img, h1, lead, h2, intro, ticks, img2, boxes) in enumerate(VP):
    nh, nt = (VP[i + 1][0], VP[i + 1][1]) if i + 1 < len(VP) else ("parcours.html", "Le parcours de A à Z")
    P[h] = (f"{t} — Cercle Énergie", lead,
     hero(img, "Le Cercle · " + t, h1, lead, [("accompagnement.html", "Le Cercle"), (None, t)], "50% 40%") + f"""
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
    {NOTE if "*" in lead + "".join(b[1] for b in boxes) else ""}
    <div class="nextprev rv"><a class="btn btn-line" href="accompagnement.html">Tout le Cercle {ARROW}</a><a class="btn btn-line" href="{nh}">Suite : {nt} {ARROW}</a></div>
  </div>
</section>
{CTA}""")

P["comprendre-les-cee.html"] = ("Comprendre les CEE — Cercle Énergie",
 "Les Certificats d’Économies d’Énergie expliqués simplement : le dispositif, les obligés, le rôle du mandataire, les documents à anticiper et les points de vigilance.",
 hero("renovation.jpg", "Comprendre", "Les CEE, expliqués simplement.", "Une marque qui explique plutôt qu’elle ne promet : voici comment fonctionne le dispositif, et où vous vous situez.", [(None, "Comprendre les CEE")]) + f"""
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Le principe</span>
    <h2 class="rv">Qui fait quoi ?</h2>
    {FLOW4}
    <p class="note rv" style="margin-inline:auto">* Selon les conditions contractuelles et la validation des dossiers.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <span class="eyebrow rv">Le vocabulaire</span><h2 class="rv">Trois notions à connaître</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">CEE</span><h3>Certificats d’Économies d’Énergie</h3><p>Le dispositif d’État qui finance une partie des travaux de rénovation énergétique.</p></div>
      <div class="box rv"><span class="n">Obligés</span><h3>Ceux qui financent</h3><p>Les fournisseurs d’énergie et les distributeurs de carburant, tenus de financer ces travaux sous peine de pénalités.</p></div>
      <div class="box rv"><span class="n">Mandataire</span><h3>Celui qui accompagne</h3><p>Une société de services spécialisée, experte du montage des dossiers, des règles fixées par l’État et de l’accompagnement des entreprises de travaux.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Sur le terrain</span><h2 class="rv">Ce qu’il vaut mieux anticiper</h2>
    <div class="cols3">
      <div class="box rv"><span class="n">Avant</span><h3>Les documents à anticiper</h3><p>Un dossier se prépare avant le chantier. Nous vous indiquons, pour chaque projet, les pièces à réunir et à quel moment.</p></div>
      <div class="box rv"><span class="n">Pendant</span><h3>Les points de vigilance</h3><p>Conformité des documents, cohérence des informations, traçabilité : nous vous aidons à les sécuriser au fil du chantier.</p></div>
      <div class="box rv"><span class="n">Après</span><h3>Le fonctionnement des primes</h3><p>Le paiement intervient après contrôle et validation du dossier, selon les conditions contractuelles. Nous vous expliquons chaque étape.</p></div>
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap center">
    <span class="eyebrow rv">Notre rôle</span>
    <h2 class="rv">Entre vos chantiers<br>et le financement.</h2>
    {CHAIN}
  </div>
</section>
<section>
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">L’essentiel à savoir</h2>
    <div class="faq" style="text-align:left">{faq_short}</div>
  </div>
</section>
{CTA}""")

P["secteurs.html"] = ("Secteurs d’intervention — Cercle Énergie",
 "Résidentiel, tertiaire, industriel, agricole : Cercle Énergie accompagne les professionnels de l’efficacité énergétique.",
 hero("pac-installation.jpg", "Nos terrains", "D’abord chez les particuliers. Et au-delà.", "Notre cœur d’activité : la pose de pompes à chaleur, de chauffe-eau thermodynamiques et l’isolation dans l’habitat. Nous accompagnons aussi les professionnels du tertiaire, de l’industrie et de l’agricole.", [(None, "Secteurs")]) + f"""
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
    <span class="eyebrow rv">Le dossier CEE</span><h2 class="rv">Les mêmes cinq étapes, quel que soit le chantier</h2>
    <div class="cols3">{"".join(f'<div class="box rv"><span class="n">0{j+1}</span><h3>{s[0]}</h3><p>{s[1]}</p></div>' for j, s in enumerate(STEPS))}</div>
    {NOTE}
    <div class="nextprev rv"><a class="btn btn-line" href="services.html">Nos services en détail {ARROW}</a><a class="btn btn-line" href="{nxt[0]}">Secteur suivant : {nxt[1]} {ARROW}</a></div>
  </div>
</section>
{CTA}""")

P["a-propos.html"] = ("À propos — Cercle Énergie",
 "Cercle Énergie, mandataire CEE de la 6e période : notre ambition, notre positionnement et notre façon de travailler avec les installateurs.",
 hero("reseau.jpg", "À propos", "Le partenaire unique de vos projets.", "Notre ambition : être le partenaire de référence des artisans qui installent des pompes à chaleur et des chauffe-eau thermodynamiques.", [(None, "À propos")], "50% 30%") + f"""
<section>
  <div class="wrap split">
    <div>
      <span class="eyebrow rv">Notre ambition</span>
      <h2 class="rv">Un interlocuteur fiable, accessible, présent à chaque étape.</h2>
      <p class="lead rv">Nous ne voulons pas être perçus comme un simple mandataire CEE qui collecte des dossiers.</p>
      <p class="rv" style="margin-top:18px">Nous voulons devenir le point d’entrée unique vers les services, les outils, les financements et les partenaires dont les professionnels ont besoin pour développer leur activité sereinement.</p>
    </div>
    <div class="media rv"><img src="assets/img/remise-dossier.jpg" alt="Une conseillère et un artisan autour d’un dossier" loading="lazy"><span class="badge">Vous installez. Nous vous accompagnons à chaque étape.</span></div>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <span class="eyebrow rv">Notre positionnement</span>
    <p class="bigquote rv">Une marque qui <em>explique</em> plutôt qu’elle ne promet, qui <em>répond</em> plutôt qu’elle ne renvoie, et qui <em>sécurise</em> plutôt qu’elle ne complexifie.</p>
    {piliers_html}
  </div>
</section>
<section>
  <div class="wrap">
    <span class="eyebrow rv">Un cercle de confiance</span><h2 class="rv">Un seul cercle de services</h2>
    <div class="linkcards six">{cerclecards}</div>
    {NOTE}
  </div>
</section>
<section class="tint" id="video">
  <div class="wrap center">
    <span class="eyebrow rv">En vidéo</span><h2 class="rv">Cercle Énergie en vidéo</h2>
    {VIDEO}
  </div>
</section>
{CTA}""")

P["faq.html"] = ("Questions fréquentes — Cercle Énergie",
 "Les réponses aux questions les plus fréquentes sur les CEE, le rôle de mandataire et l’accompagnement Cercle Énergie.",
 hero("portrait-conseillere.jpg", "Questions fréquentes", "Vos questions, nos réponses.", "Répondre plutôt que renvoyer : l’essentiel sur les CEE, notre rôle et notre accompagnement.", [(None, "FAQ")], "50% 25%") + f"""
<section>
  <div class="wrap center">
    <div class="faq" style="text-align:left;margin-top:0">{faq_all}</div>
    <p class="rv" style="margin:44px auto 0">Une autre question ? <a class="hl" href="contact.html" style="font-weight:700">Contactez-nous</a>.</p>
  </div>
</section>
{CTA}""")

P["devenir-partenaire.html"] = ("Parlons de vos projets — Cercle Énergie",
 "Installateurs de pompes à chaleur, de chauffe-eau thermodynamiques, spécialistes de l’isolation : échangeons sur votre activité et vos projets.",
 hero("reseau.jpg", "Parlons de vos projets", "Un échange pour commencer.", "Dites-nous comment vous travaillez. Nous vous dirons, simplement, ce que nous pouvons faire avec vous.", [(None, "Parlons de vos projets")]) + f"""
{JOIN}
<section>
  <div class="wrap">
    <span class="eyebrow rv">Ce que vous pouvez attendre de nous</span><h2 class="rv">Simplicité. Confiance. Performance. Proximité.</h2>
    {piliers_html}
  </div>
</section>
<section class="tint">
  <div class="wrap center">
    <span class="eyebrow rv">Questions fréquentes</span><h2 class="rv">Avant d’échanger</h2>
    <div class="faq" style="text-align:left">{"".join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[2:5] + FAQ[9:])}</div>
  </div>
</section>""")

P["contact.html"] = ("Contact — Cercle Énergie", "Contactez Cercle Énergie, mandataire CEE et partenaire des installateurs.",
 hero("remise-dossier.jpg", "Contact", "Parlons de vos projets.", "Une question sur les CEE ou sur notre accompagnement ? Écrivez-nous.", [(None, "Contact")]) + f"""
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
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if (h == fname or (h == "secteurs.html" and fname.startswith("secteur-")) or (h == "accompagnement.html" and fname in CERCLE_PAGES)) else ""}>{t}</a>' for h, t in NAV)
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
    <nav class="nav" aria-label="Navigation principale">{links}<a class="btn btn-primary" href="devenir-partenaire.html">Parlons de vos projets {ARROW}</a></nav>
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
        <p style="margin-top:20px;max-width:38ch">Mandataire CEE de la 6e période. Le partenaire des installateurs, du premier contact au versement de la prime, selon les conditions contractuelles et la validation des dossiers.</p>
      </div>
      <div><h4>Le Cercle</h4><ul><li><a href="accompagnement.html">Un cercle de services</a></li><li><a href="parcours.html">Le parcours de A à Z</a></li><li><a href="services.html">Le financement CEE</a></li><li><a href="visite-technique.html">La visite technique</a></li><li><a href="suivi-dossiers.html">Le suivi de vos dossiers</a></li><li><a href="equipements.html">Les équipements</a></li></ul></div>
      <div><h4>Le site</h4><ul><li><a href="comprendre-les-cee.html">Comprendre les CEE</a></li><li><a href="secteurs.html">Secteurs</a></li><li><a href="a-propos.html">À propos</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="plaquette.pdf">Présentation (PDF)</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="devenir-partenaire.html">Parlons de vos projets</a></li><li><a href="contact.html">Nous contacter</a></li><li>[Téléphone à compléter]</li><li>[E-mail à compléter]</li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Cercle Énergie. Tous droits réservés.</span><span><a href="mentions-legales.html">Mentions légales</a> — Primes CEE : selon les conditions contractuelles et la validation des dossiers.</span></div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

for f, (t, d, b) in P.items():
    (ROOT / f).write_text(page(f, t, d, b), encoding="utf-8")
print(len(P), "pages écrites :", ", ".join(P))
