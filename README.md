# cleaner_recovery

## Description
Un programme Windows capable de récupérer des fichiers supprimés ou des données perdues sur une usb.

## Librairies utilisées:
- os : Pour les opérations sur le système de fichiers et les PhysicalDrive installés
- pytsk3 : Pour la lecture des paritions
- tqdm : Barre de progression en invite de commande
- time : Pour les délais

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