# LinkTree v6

LinkTree v6 est une application de gestion de liens personnalisés, conçue pour simplifier et accélérer l'accès à vos ressources préférées depuis un navigateur web. Cette application offre une interface utilisateur intuitive permettant de naviguer, modifier et organiser des collections de liens de manière efficace.

## Fonctionnalités

- **Navigation rapide** : Utilisez les touches `A` et `Z` pour parcourir les collections de liens.
- **Interface de modification** : Ajoutez, modifiez ou supprimez des liens directement via l'interface utilisateur.
- **Création de nouvelles collections** : Créez des collections pré-remplies avec des placeholders.
- **Sauvegarde persistante** : Les données sont stockées dans un fichier binaire pour une récupération rapide.

## Structure du Projet

- **`main.py`** : Point d'entrée principal de l'application. Gère l'affichage et la navigation entre les collections de liens.
- **`modifier.py`** : Interface de modification permettant de gérer les collections et leurs liens.
- **`infos.py`** : Fenêtre d'informations fournissant des détails sur l'application et un accès rapide au dépôt GitHub.
- **`all_labels_make.py`** : Script d'initialisation pour créer le fichier de données contenant les collections par défaut.

## Prérequis

- Python 3.x
- Bibliothèques nécessaires : `wxPython`, `Pillow`

