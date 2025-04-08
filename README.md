# Cleaner Recovery
Un programme Windows capable de récupérer des fichiers supprimés ou des données perdues sur une usb.

Attention, il est possible que certains fichiers soient corrompus et inutilisables malgré la récupération.

## Installation
1. git clone https://github.com/florianc220/cleaner_recovery.git
2. Télécharger l'exécutable cleaner_recovery.exe du dossier dist

## Utilisation
Lancer l'exécutable cleaner_recovery.exe en tant qu'administrateur.
Une fois la récupération de fichiers terminée, les fichiers seront placés 
dans un dossier "recovered_files" à la racine du programme.

Suivre les instructions:
- Arrivée sur le menu: 
    - Commencer l'analyse d'un disque
      - Choisir le disque à analyser
      - Choisir la partition du disque à analyser
      - Affichage des fichiers trouvés
      - Sélection des fichiers à récupérer
      - Récupération des fichiers
      - Fin de l'analyse
    - Options
      - Analyse des fichiers ordinaire. True(1) ou False(0)
    - Quitter
      - Fin du programme

## Librairies utilisées:
- pytsk3 : Pour la lecture des partitions
- tqdm : Pour la barre de progression en invite de commande

## Lien VirusTotal:
https://www.virustotal.com/gui/file/74c076bce85348ab39072dff078e9b096fe4e3e1b1197f0e84e8e4ec56e21ded/detection
