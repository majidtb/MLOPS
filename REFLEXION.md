# Réflexion — TP2

## 1. Quel est le meilleur des 3 modèles ? Peut-on le prouver ?

Oui, en grande partie. `git log --oneline` montre les 3 commits distincts
(Version initiale, Essai 2, Essai 3), chacun avec un message explicite qui
décrit ce qui a changé. Aucun essai n'est écrasé : on peut les comparer
avec `git diff` et retrouver l'accuracy de chacun en restaurant le commit.

Limite : dans notre cas, les 3 essais donnent une accuracy de 1.0 à cause de
la fuite de données (la règle de churn dépend directement de `consommation`
et `anciennete`). On peut donc prouver *quelle modification a été faite*,
mais pas désigner un vrai « meilleur » modèle. Les accuracies ne sont pas
stockées dans Git : ce sera le rôle de MLflow (TP3-4).

## 2. Peut-on redonner exactement le modèle de l'Essai 1 ?

Oui. La commande suivante restaure le notebook tel qu'il était à l'Essai 1 :

    git checkout <identifiant_du_commit> -- churn_model.ipynb

En ré-exécutant le notebook, avec `random_state=42` et les mêmes données
(`churn_data.csv` est versionné), on retrouve le même modèle. Seul le fichier
`model.pkl` n'est pas versionné (il est dans `.gitignore`), il faut donc le
régénérer.

## 3. Un camarade peut-il reproduire notre travail sur une autre machine ?

Oui, en grande partie. `git clone <adresse>` donne une copie identique du
code, des données et de tout l'historique des 3 essais.

Limites : le dossier `venv/` et le fichier `model.pkl` ne sont pas dans le
dépôt. Le camarade doit recréer son environnement virtuel, réinstaller les
bibliothèques (idéalement avec les mêmes versions) et réentraîner le modèle.
Le problème « ça marche chez moi » n'est donc que partiellement résolu.