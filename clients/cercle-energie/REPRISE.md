# Cercle Énergie — dossier de reprise

Ce fichier permet à une nouvelle session (ou à une personne) de reprendre le projet sans l'historique de la conversation. État au 12 novembre 2026.

## Le client
- Nom exact : **Cercle Énergie** (jamais « Cercle d'Énergie »). Signature : « Le partenaire unique de vos projets ». Mandataire CEE de la 6e période.
- Interlocuteur côté client qui valide les publicités : Jordan.
- E-mail du site : contact@cercleenergie.com. Domaines achetés : cercleenergie.fr (principal) et cercleenergie.com.
- **Le brief de marque du client fait autorité** : `materiel/Brief_vision_marketing_Cercle_Energie.pdf`. Les règles d'application décidées par l'agence, suivies du texte intégral du brief, sont dans `materiel/cadrage-agence-et-brief-client.md`. À lire avant toute production.

## Règles à ne pas enfreindre
- Aucune prime « garantie », aucun délai ou prix chiffré, aucun témoignage, chiffre ou coordonnée inventés. Mention : « selon les conditions contractuelles et la validation des dossiers ».
- Concept : le **cercle** (cercle de confiance, un seul cercle de services). Ne plus parler de « réseau » ni de « volets ».
- Cible : installateurs de pompes à chaleur, de chauffe-eau thermodynamiques, isolation ; artisans RGE. Angle du dirigeant : l'artisan **local** (jamais « du coin », jugé péjoratif) qui fait des chantiers de qualité mais galère sur ses dossiers.
- Demandes de Jordan sur les pubs : dire « dossiers de financement » (pas seulement « dossiers CEE »), mettre en avant « des applications dédiées » / des outils pour des dossiers de qualité.
- WOLTIC, Hitachi, Thomson : texte seul avec réserve sur le site et la présentation ; absents des publicités. Le CRM interne n'est jamais présenté comme un outil pour les artisans. L'orthographe « WOLTIC » vient du brief, qui donne pourtant l'adresse woltik.fr : à confirmer.
- Appel à l'action unique : « Parlons de vos projets ».
- Toujours vérifier à l'image avant de livrer (textes coupés, chevauchements) : le propriétaire de l'agence y tient.

## Ce qui existe
| Élément | Emplacement | En ligne |
|---|---|---|
| Site (18 pages statiques) | `site/` — généré par `site/build.py` | https://cercle-energie.vercel.app |
| Page de validation des pubs | `validation/` — générée par `validation/build.py` | https://cercle-energie-validation.vercel.app |
| Présentation commerciale (16 diapositives) | `plaquette/` — `build_plaquette.js`, `build_diffusion.js` | PDF aussi dans `site/plaquette.pdf` |
| Vidéo de présentation | `cercle-energie-presentation-v3.mp4` (actuelle, 70 s), sources `sources/v3/` ; v1 et v2 conservées | intégrée au site |
| Publicités | `pub/visuels/` (12 visuels × 3 formats), `pub/videos/` (C1 à C4, N1, formats story et fil) | sur la page de validation |
| Kit page Facebook | `pub/page-facebook/` (couverture, profil, textes) | — |
| Notes de campagne | `pub/campagne-leads.md` | — |
| Matière première | `materiel/` (plans vidéo, voix, musique, brief, scripts de déploiement) | — |

Envoyer au client le PDF ou le PowerPoint « diffusion » de la présentation, pas le PowerPoint éditable (il a provoqué des blancs sur iPhone).

## Refaire les fichiers
Prérequis : Python 3 (Pillow), Node avec Playwright, ffmpeg ; pour la présentation, pptxgenjs + sharp, LibreOffice.
```
python3 site/build.py                                   # site
cd pub && node render.js                                # visuels
python3 pub/build_cercle.py materiel/plans-paysage materiel/audio/musique.mp3            # vidéos C1 à C4
python3 pub/build_nouvelles.py materiel/plans-verticaux materiel/audio/n1-voix-v2.mp3 materiel/audio/musique.mp3   # film N1
python3 validation/build.py                             # page de validation (recopie visuels et vidéos)
```
`pub/work/` est un dossier temporaire ; `build_nouvelles.py` a besoin de `pub/work/r.js`, créé par `build_cercle.py` (le lancer d'abord).

## Mise en ligne (Vercel)
- Équipe `team_DkRXYwyRxWZUQsOAueGPLbBq` (rachidaddouche-8982s-projects). Projets : `cercle-energie` (site) et `cercle-energie-validation`.
- Les deux projets sont poussés par l'API ou la ligne de commande, **pas reliés à Git** : toute modification demande un nouveau déploiement. Depuis un ordinateur : `vercel deploy --prod` dans `site/` ou `validation/` après `vercel link`. Les scripts `materiel/deployer_*.py` font la même chose par l'API (ils attendent un jeton Vercel fourni par l'environnement ; ne jamais écrire de jeton dans le dépôt).
- La page de validation enregistre les avis dans l'espace de stockage `cercle-energie-validation-reviews` ; ils se lisent à l'adresse `/api/reviews` de la page.
- Avis de Jordan au 12/11 : validés C01, C02, C03, C05, C06, C07, C2, H01, H06, L01, L02. Retouches demandées sur C04, C1, C3, C4, L03, N1 : faites et remises en ligne, **en attente de sa nouvelle validation**.

## Reste à faire
1. **Domaine** : ajouter `cercleenergie.fr` (et `www`) au projet `cercle-energie` dans Vercel → Settings → Domains, créer les enregistrements DNS indiqués, éventuellement rediriger `cercleenergie.com` vers le `.fr` sans toucher à ses enregistrements MX (messagerie). Puis remplacer `https://cercle-energie.vercel.app` par `https://cercleenergie.fr` dans `validation/build.py`, `validation/selection.tpl.html`, `pub/page-facebook/textes.md`, `pub/campagne-leads.md`, et régénérer.
2. **Motion design** : une vidéo publicitaire en motion design (référence fournie par l'agence : aplats illustrés sur fond bleu nuit, grands titres, voix) était en fabrication à la fin de la session cloud. Sources attendues dans `pub/motion/`, livrables `pub/videos/M1-motion-design-fil.mp4` et `-story.mp4`. S'ils sont absents ou incomplets, la tâche est à reprendre ; s'ils sont là, les contrôler image par image puis les ajouter à `validation/build.py`.
3. **Publicités Meta** : rien n'est lancé. Attendre le feu vert de l'agence. Il faut : la page Facebook de Cercle Énergie, un compte publicitaire avec moyen de paiement, le budget, la zone, la destination des demandes, une politique de confidentialité si formulaire Meta.
4. **Site** : téléphone, adresse et mentions légales sont encore des emplacements entre crochets ; le formulaire n'envoie rien (à relier à contact@cercleenergie.com ou à un CRM).
5. **À faire écouter** (les sessions ne peuvent pas écouter l'audio) : la vidéo de présentation v3 et le film N1 — prononciation de « CEE », rythme, équilibre voix/musique.
6. Points ouverts du brief (section 10) : périmètre exact des prestations, accords Hitachi/Thomson et droits d'usage des marques, conditions d'accès aux leads, orthographe WOLTIC.
