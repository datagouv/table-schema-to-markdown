## Métadonnées d'un répertoire Git

- Auteur : Antoine Augusti <antoine.augusti@example.com>
- Schéma créé le : 31/12/2018
- Site web : https://github.com/AntoineAugusti/data-codes-sources-fr
- Valeurs manquantes : `"Nan"`
- Clé primaire : `repertoire_url`

### Modèle de données


##### Liste des propriétés

| Propriété | Type | Obligatoire |
| -- | -- | -- |
| [nom](#propriete-nom) | chaîne de caractères  | Oui |
| [organisation_nom](#propriete-organisation-nom) | chaîne de caractères  | Oui |
| [plateforme](#propriete-plateforme) | chaîne de caractères  | Oui |
| [repertoire_url](#propriete-repertoire-url) | chaîne de caractères (format `uri`) | Oui |
| [description](#propriete-description) | chaîne de caractères  | Non |
| [est_fork](#propriete-est-fork) | booléen  | Oui |
| [date_creation](#propriete-date-creation) | date et heure  | Oui |
| [derniere_mise_a_jour](#propriete-derniere-mise-a-jour) | date et heure  | Oui |
| [page_accueil](#propriete-page-accueil) | chaîne de caractères  | Non |
| [nombre_stars](#propriete-nombre-stars) | nombre entier  | Oui |
| [nombre_forks](#propriete-nombre-forks) | nombre entier  | Oui |
| [licence](#propriete-licence) | chaîne de caractères  | Non |
| [nombre_issues_ouvertes](#propriete-nombre-issues-ouvertes) | nombre entier  | Oui |
| [langage](#propriete-langage) | chaîne de caractères  | Non |
| [topics](#propriete-topics) | chaîne de caractères  | Non |
| [prop.dot](#propriete-prop-dot) | chaîne de caractères  | Non |

#### Propriété `nom`

> *Description : Le nom du répertoire*<br/>*Exemple : nom-repertoire*
- Valeur obligatoire
- Type : chaîne de caractères

#### Propriété `organisation_nom`

> *Description : Le nom de l'organisation*<br/>*Exemple : etalab*
- Valeur obligatoire
- Type : chaîne de caractères

#### Propriété `plateforme`

> *Description : La plateforme de dépôt de code*<br/>*Exemple : GitHub*
- Valeur obligatoire
- Type : chaîne de caractères
- Valeurs autorisées : 
    - GitHub

#### Propriété `repertoire_url`

> *Description : L'URL vers le répertoire*<br/>*Exemple : https://github.com/etalab/nom-repertoire*
- Valeur obligatoire
- Type : chaîne de caractères (format `uri`)

#### Propriété `description`

> *Description : La description du répertoire*<br/>*Exemple : Ce répertoire est utile*
- Valeur optionnelle
- Type : chaîne de caractères

#### Propriété `est_fork`

> *Description : Indique si le répertoire est un fork*<br/>*Exemple : false*
- Valeur obligatoire
- Type : booléen

#### Propriété `date_creation`

> *Description : La date de création du répertoire*<br/>*Exemple : 2018-12-01T20:00:55Z*
- Valeur obligatoire
- Type : date et heure

#### Propriété `derniere_mise_a_jour`

> *Description : La date de dernière mise à jour du répertoire*<br/>*Exemple : 2018-12-01T20:00:55Z*
- Valeur obligatoire
- Type : date et heure

#### Propriété `page_accueil`

> *Description : URL vers la page d'accueil du projet*<br/>*Exemple : https://etalab.gouv.fr*
- Valeur optionnelle
- Type : chaîne de caractères

#### Propriété `nombre_stars`

> *Description : Le nombre de fois où le répertoire a été ajouté aux favoris*<br/>*Exemple : 42*
- Valeur obligatoire
- Type : nombre entier

#### Propriété `nombre_forks`

> *Description : Le nombre de fois où le répertoire a été forké*<br/>*Exemple : 13*
- Valeur obligatoire
- Type : nombre entier

#### Propriété `licence`

> *Description : La licence du répertoire, telle que détectée par la plateforme*<br/>*Exemple : MIT*
- Valeur optionnelle
- Type : chaîne de caractères

#### Propriété `nombre_issues_ouvertes`

> *Description : Le nombre d'issues actuellement ouvertes*<br/>*Exemple : 0*
- Valeur obligatoire
- Type : nombre entier

#### Propriété `langage`

> *Description : Le langage principal du répertoire, tel que détecté par la plateforme*<br/>*Exemple : Python*
- Valeur optionnelle
- Type : chaîne de caractères

#### Propriété `topics`

> *Description : Les tags du répertoire*<br/>*Exemple : utile,france,opendata*
- Valeur optionnelle
- Type : chaîne de caractères

#### Propriété `prop.dot`

> *Description : Un champ avec un point dans son nom (vérifier que son lien fonctionne sur le site)*<br/>*Exemple : :shrug:*
- Valeur optionnelle
- Type : chaîne de caractères
