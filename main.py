import psutil
import pytsk3
import os

def search_disks():
    """
    Cherche les disques visible sur la machine et les affiche dans l'invite de commande.
    Retourne une liste des disques trouvées ou None.
    """
    print("Disques présents sur le système...")
    disks = []
    for disk in range(10):  # On teste les disques \\.\PhysicalDrive0 à \\.\PhysicalDrive9
        disk_path = f"\\\\.\\PhysicalDrive{disk}"
        if os.path.exists(disk_path):  # Vérifie si le disque existe
            disks.append(disk_path)
            print(f"{len(disks)}. {disk_path}")
    return disks


def search_partitions(disque):
    """
    Cherche les partitions d'un disque donné.
    Retourne une liste des partitions trouvées ou None.
    """
    try:
        image_disk = pytsk3.Img_Info(disque)
        partition_table = pytsk3.Volume_Info(image_disk)
        partitions = []
        print(f'Partitions présentes sur le disque...')
        for index, partition in enumerate(partition_table):
            print(f'{index+1}: Début={partition.start}, Taille = {partition.len}, Type = {partition.desc.decode()}')
            partitions.append((partition.start, partition.len))
        return partitions
    except Exception as e:
        print(f'Erreur lors de la lecture des partitions : {e}')


def choose_disk(disks):
    """
    Demande à l'utilisateur de choisir un disque.
    Retourne le disque choisi.
    """
    choice = input(f"Choisissez un disque (1-{len(disks)}): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(disks):
            return disks[index]
        else:
            print("Choix non valide.")
            return choose_disk(disks)
    except ValueError:
        print("Entrez un nombre valide.")
        return choose_disk(disks)

def choose_partition(partitions):
    """
    Demande à l'utilisateur de choisir une partition.
    Retourne la partition choisie.
    """
    choice = input(f"Choisissez une partition (1-{len(partitions)}): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(partitions):
            return partitions[index]
        else:
            print("Choix non valide.")
            return choose_partition(partitions)
    except ValueError:
        print("Entrez un nombre valide.")
        return choose_partition(partitions)


def read_partition_hidden_files(choosen_partition: psutil._common.sdiskpart):
    """
    Lis les fichiers dans la partition choisie par l'utilisateur.
    Retourne les infos du système de fichier ou None.
    """
    """try:
        print(f'Lecture de la partition {choosen_partition.device} sur le lecteur {choosen_partition.mountpoint}...')
        image_disk_path = create_image_disk(choosen_partition)
        #Ouverture image disque
        disk_image = pytsk3.Img_Info(image_disk_path)
        #Analyse de système de fichier
        fs_info = pytsk3.FS_Info(disk_image)
        return fs_info
    except Exception as e:
        print(f"Erreur lors de la lecture de la partition : {e}")
        return None"""


if __name__ == "__main__":
    print("Bienvenue sur Cleaner Recovery !")
    disks = search_disks()

    if disks is not None:
        chosed_disk = choose_disk(disks)
        print(f"Disque choisi: {chosed_disk}")
        partitions = search_partitions(chosed_disk)

        if partitions is not None:
            chosed_part = choose_partition(partitions)
            print(f'Partition choisie: {chosed_part}')

