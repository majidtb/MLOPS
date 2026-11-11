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

## 4. Pourquoi MLflow est-il utile au TP3 ?

MLflow apporte la traçabilité des expériences et la reproductibilité des modèles.
Dans notre projet, chaque essai est enregistré dans un run avec ses paramètres,
les métriques (accuracy, precision, recall, f1) et le modèle entraîné. Cela
permet de comparer les essais de manière objective, sans dépendre uniquement de
la mémoire du développeur ou des fichiers locaux.

Sans MLflow, il serait difficile de retrouver rapidement quel modèle a été
entraîné avec quelles hyperparamètres, sur quels jeux de données, et avec
quelle performance. Le tracking transforme la recherche expérimentale en un
historique exploitable.

## 5. Comment le meilleur modèle est-il sélectionné ?

Le choix du meilleur modèle se fait à partir des métriques enregistrées dans
MLflow. Dans le script de training, chaque run logue le score F1, ainsi que
l'accuracy et les autres mesures. Ensuite, on peut trier les runs selon
`metrics.f1 DESC` pour repérer le meilleur modèle.

Cette étape est importante car elle permet de formaliser la décision : le
modèle n'est plus choisi au hasard, mais selon une métrique de performance
clairement définie. Dans notre cas, le choix du meilleur modèle reste
sensiblement stable si les données sont bien préparées, même si la base de
churn a une fuite de données qui peut artificiellement améliorer les scores.

## 6. Qu'est-ce que le registre de modèles et l'alias champion ?

Le registre de modèles permet de versionner les modèles comme des artefacts
pérénisés. Le script `register_model.py` enregistre le meilleur run sous le
nom `churn-model`, puis lui attribue un alias `champion`.

Cela est très utile en production : on peut déployer un modèle connu, le
définir comme référence, et le remplacer plus tard par une autre version en
gardant la trace de l'historique. L'alias `champion` sert de point d'entrée
stable pour l'application et évite de dépendre d'un identifiant de version qui
peut changer.

## 7. Pourquoi charger un modèle via son alias est-il intéressant ?

Le chargement d'un modèle via `models:/churn-model@champion` rend le pipeline
plus robuste. L'API ne dépend plus d'un run local ou d'un fichier `model.pkl` 
qui peut être écrasé. Elle charge explicitement la version actuellement
désignée comme champion dans le registre MLflow.

Ceci correspond à une bonne pratique MLOps : la production pointe vers une
version explicitement validée, et les changements de modèle passent par un
contrôle clair. Cela améliore la traçabilité, la reproductibilité et la
qualité de la livraison.

## 8. Bilan du TP3

Le TP3 montre l'importance du monitoring et de la gestion de modèles dans un
projet de machine learning. MLflow ne sert pas seulement à enregistrer des
résultats : il offre une infrastructure complète pour suivre les expériences,
stocker les artefacts, comparer les performances et déployer des modèles de
façon reproductible.

Dans le contexte du projet churn, cette approche permet de passer d'un modèle
local, difficile à suivre, à un pipeline de production plus structuré et plus
fiable. C'est la base du MLOps moderne : automatiser, tracer et contrôler
chaque étape du cycle de vie du modèle.

## 9. Pourquoi le TP4 est-il un vrai exercice de déploiement ?

Le TP4 passe de la phase d'expérimentation à la phase de mise en production.
Le modèle n'est plus seulement entraîné puis évalué localement : il est
chargé depuis MLflow, servi via une API REST, et exposé pour des prédictions
réelles. C'est le cœur du MLOps : transformer un modèle de notebook en un
service exploitable par d'autres applications.

L'API FastAPI permet de rendre le modèle accessible par HTTP, avec une
validation automatique des entrées grâce à Pydantic. Cela garantit que les
données envoyées au modèle respectent le bon format, ce qui réduit les erreurs
et facilite l'intégration côté client.

## 10. Quel est le rôle du point d'entrée /predict ?

Le point d'entrée `/predict` reçoit un client au format JSON et le transforme
en DataFrame exploitable par le modèle. Les colonnes sont ensuite encodées de
la même manière que pendant l'entraînement, puis on réordonne les variables
pour correspondre exactement au modèle attendu.

Cette étape est cruciale : un mauvais ordre des colonnes ou une mauvaise
conversion des catégories peut empêcher le modèle de prédire correctement.
C'est précisément là que la reproductibilité du pipeline de données prend toute
sa valeur.

## 11. Pourquoi le modèle ne doit-il pas être chargé à partir d'un fichier local ?

Le chargement depuis `model.pkl` ou depuis un notebook local est fragile car le
modèle peut être écrasé, perdu, ou ne pas correspondre au bon essai. En
revanche, MLflow permet d'accéder à la version exacte du modèle enregistrée et
validée dans le registre.

Le choix de `models:/churn-model@champion` est une bonne pratique de
production, car il sépare le service de l'implémentation technique du modèle.
Le code de l'API ne dépend pas d'un fichier physique ; il dépend d'une version
de référence clairement identifiée.

## 12. Comment le service devient-il robuste et maintenable ?

Plusieurs éléments rendent l'API plus fiable :

- validation des entrées par Pydantic ;
- point d'état `/health` pour vérifier le bon fonctionnement du service ;
- déclaration explicite du modèle champion dans le registre MLflow ;
- séparation claire entre entraînement, enregistrement et prédiction.

Cela permet de surveiller le service, de comprendre les erreurs rapidement et
de remplacer facilement le modèle sans modifier l'API si la logique de
consommation reste identique.

## 13. Bilan du TP4

Le TP4 montre la transition d'un projet de science des données vers un projet
MLOps complet. L'entraînement, la comparaison, la mise en registre et le
déploiement du modèle sont maintenant reliés dans un même flux cohérent.

Le point important est que le modèle n'est plus un simple artefact local : il
est versionné, référencé, déployé et consommé comme un service. C'est cette
architecture qui permet de passer d'un prototype à une solution opérationnelle,
robuste, traçable et facile à faire évoluer.