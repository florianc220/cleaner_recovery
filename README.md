# cleaner_recovery
Un programme Windows capable de récupérer des fichiers supprimés ou des données perdues sur une usb.

Attention, il est possible que certains fichiers soient corrompus et inutilisables malgré la récupérations.
## Installation
1. git clone https://github.com/florianc220/cleaner_recovery.git
2. Télécharger l'exécutable cleaner_recovery.exe du dossier dist

## Utilisation
Lancer l'exécutable cleaner_recovery.exe en tant qu'administrateur.
Une fois la récupération de fichiers terminée, les fichiers seront placés 
dans un dossier "recovered_files" à la racine du programme.

Suivre les instructions:
- Arrivée sur le menu: 
    - 0: Commencer l'analyse d'un disque
      - Choisir le disque à analyser
      - Choisir la partition du disque à analyser
      - Affichage des fichiers trouvés
      - Sélection des fichiers à récupérer
      - Récupération des fichiers
      - Fin de l'analyse
    - 1: Options
      - Analyse des fichiers ordinaire. True(1) ou False(0)
    - 2: Quitter
      - Fin du programme

## Librairies utilisées:
- pytsk3 : Pour la lecture des partitions
- tqdm : Pour la barre de progression en invite de commande
