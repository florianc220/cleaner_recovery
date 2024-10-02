import psutil

import os
import win32file
import win32con
import struct

import pytsk3
import numpy as np
import pandas as pd

import constant

def search_disks():
    """
    Cherche les disques visible sur la machine et les affiche dans l'invite de commande.
    Retourne une liste des disques trouvées ou None.
    """
    print("Disques présents sur le système...")
    disques = psutil.disk_partitions()
    # Si aucune disque n'est trouvée, on affiche un message et on retourne None
    if len(disques) == 0:
        print("Aucune disque trouvée")
        return None
    else :
        for index, disque in enumerate(disques):
            if disque.mountpoint == disque.device:
                print(f'{index}: device={disque.device},\tfstype={disque.fstype},\topts={disque.opts}')
            else:
                print(f'{index}: device={disque.device},\tmountpoint={disque.mountpoint},\tfstype={disque.fstype},\topts={disque.opts}')
    return disques


def choose_disk(disques):
    """
    Demande à l'utilisateur de choisir un disque.
    Retourne le disque choisi.
    """
    while True:
        print("Choisissez un disque : ")
        choice = int(input())
        if choice < 0 or choice >= len(disques):
            print("Choisissez un disque : ")
            choice = int(input())
        else:
            break
    return disques[choice]

def search_partitions(disque):
    """
    Cherche les partitions d'un disque donné.
    Retourne une liste des partitions trouvées ou None.
    """

def choose_partition(partitions):
    """
    Demande à l'utilisateur de choisir une partition.
    Retourne la partition choisie.
    """


def read_partition_hidden_files(choosen_partition: psutil._common.sdiskpart):
    """
    Lis les fichiers dans la partition choisie par l'utilisateur.
    Retourne les infos du système de fichier ou None.
    """
    try:
        print(f'Lecture de la partition {choosen_partition.device} sur le lecteur {choosen_partition.mountpoint}...')
        image_disk_path = create_image_disk(choosen_partition)
        #Ouverture image disque
        disk_image = pytsk3.Img_Info(image_disk_path)
        #Analyse de système de fichier
        fs_info = pytsk3.FS_Info(disk_image)
        return fs_info
    except Exception as e:
        print(f"Erreur lors de la lecture de la partition : {e}")
        return None


if __name__ == "__main__":
    print("Bienvenue sur Cleaner Recovery !")
    disques = search_disks()

    if disques is not None:
        partition_chosen = choose_partition(partitions)
        print(f"Partition choisie: {partition_chosen.device}")
        image_disk_path = create_image_disk(partition_chosen)
        print(f"Image disque créée: {image_disk_path}")
        #fs_info = read_partition_hidden_files(partition_chosen)
        #print(fs_info)

