import psutil
import pytsk3
import os
from tqdm import tqdm

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


def read_deleted_files(directory):
    """
    Lit les fichiers supprimés dans le dossier racine et les sous dossier
    """
    for node in directory:
        if node.info.meta:
            #Si c'est un fichier supprimé
            if node.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG and node.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                try:
                    if node.info.meta.name.name:
                        file_name = node.info.name.name.decode('utf-8')
                    else:
                        file_name = f'Fichier sans nom'
                    print(f'Fichier supprimé: {file_name}')
                except Exception as e:
                    print(f'Erreur lors de la lecture du nom du fichier: {e}')
            #Si c'est un dossier, on parcours récursivement
            if node.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                try:
                    new_dir = node.as_directory()
                    read_deleted_files(new_dir)
                except Exception as e:
                    print(f'Erreur lors de la lecture du dossier: {e}')

def read_partition(disk, partition):
    """
        Ouvre l'image du disque à l'offset de la partition choisie et lit les fichiers supprimés.
    """
    try:
        print(f'Lecture de la partition {partition[0]}...')
        img_info = pytsk3.Img_Info(disk)
        partition_offset = partition[0] * 512  # Multiplie par 512 car l'offset est en secteurs
        fs_info = pytsk3.FS_Info(img_info, offset=partition_offset)
        #Lecture des fichiers supprimés
        try:
            root_directory = fs_info.open_dir(path="/")
            read_deleted_files(root_directory)
        except Exception as e:
            print(f'Erreur lors de l\'analyse des fichiers supprimés: {e}')
    except Exception as e:
        print(f"Erreur lors de la lecture de la partition: {e}")


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
            read_partition(chosed_disk, chosed_part)
