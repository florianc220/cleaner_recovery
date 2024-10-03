import os
import sys
import time
import ctypes
import pytsk3
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


def read_partition(disk, partition, strict=True):
    """
        Ouvre l'image du disque à l'offset de la partition choisie
        et lit les fichiers supprimés avant de les retourner dans une liste
    """
    deleted_files = []
    try:
        print(f'Lecture de la partition {partition[0]}...')
        img_info = pytsk3.Img_Info(disk)
        partition_offset = partition[0] * 512  # Multiplie par 512 car l'offset est en secteurs
        fs_info = pytsk3.FS_Info(img_info, offset=partition_offset)
        #Lecture des fichiers supprimés
        try:
            root_directory = fs_info.open_dir(path="/")
            total_files = sum(1 for _ in root_directory)

            root_directory = fs_info.open_dir(path="/")
            with tqdm(total=total_files, desc="Recherche des fichiers supprimés", unit=" file") as pbar:
                for inode in root_directory:
                    #Si est un fichier ou un dossier
                    if inode.info.meta:
                        #On ne veut que les fichiers ordinaire (pas de répertoire ou autre type spécial) et qu'il est marqué comme "non alloué"
                        if strict:
                            if inode.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG and inode.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                                deleted_files.append(inode)
                        #On prend tout types de fichiers "non alloué"
                        else:
                            if inode.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                                deleted_files.append(inode)
                    pbar.update(1)
            return deleted_files
        except Exception as e:
            print(f'Erreur lors de l\'analyse des fichiers supprimés: {e}')
            return None
    except Exception as e:
        print(f"Erreur lors de la lecture de la partition: {e}")
        return None


def choose_files_to_restore(deleted_files):
    files_to_restore = []

    time.sleep(0.25)
    print('Choisissez l\'indice du/des fichier(s) à restaurer')
    for index, file in enumerate(deleted_files):
        print(f'{index}: {file.info.name.name.decode('utf-8')}')

    while True:
        choice = (int)(input("Saisir l'index pour ajouter le fichier souhaité | Tout Sélectionner: -1 | Continuer: -2 | Annuler: -3: "))
        if choice == -1:
            return deleted_files
        # On soumet la liste de fichiers à restaurer
        elif choice == -2:
            return files_to_restore
        # On annule
        elif choice == -3:
            return None
        #On ajoute à la liste indice correct et si n'est pas déjà présent
        elif 0 <= choice < len(deleted_files):
            if deleted_files[choice] not in files_to_restore:
                files_to_restore.append(deleted_files[choice])
                print(f'Fichier {deleted_files[choice].info.name.name.decode("utf-8")} ajouté à la liste')


def restore_file(files_to_restore, chosed_disk, chosed_part):
    """
    Restaure les fichiers sélectionnés dans un répertoire spécifique
    """
    #Création du répertoire "restored_files" s'il n'existe pas
    restored_dir = os.path.join(os.getcwd(), 'restored_files')
    if not os.path.exists(restored_dir):
        os.makedirs(restored_dir)

    print('Fichiers à restaurer',end=': ')
    for file in files_to_restore:
        print(f'{file.info.name.name.decode("utf-8")}', end=', ')
    print()
    time.sleep(0.25)

    success_cpt = 0
    total_size = len(files_to_restore)
    with tqdm(total=total_size, desc="Restauration des fichiers") as pbar:
        for file in files_to_restore:
            try:
                inode_nb = file.info.meta.addr
                file_name = file.info.name.name.decode('utf-8')
                output_file_path = os.path.join(restored_dir, file_name)
                #print(f'inode_nb: {inode_nb}, output: {output_file_path}')

                image_disk = pytsk3.Img_Info(chosed_disk)
                fs_info = pytsk3.FS_Info(image_disk, offset=chosed_part[0] * 512)
                restore_file = fs_info.open_meta(inode_nb)

                with open(output_file_path, 'wb') as output_file:
                    file_size = restore_file.info.meta.size
                    offset = 0
                    while offset < file_size:
                        available_to_read = min(1024*1024, file_size-offset)
                        data = restore_file.read_random(offset, available_to_read)
                        if not data:
                            break
                        output_file.write(data)
                        offset += len(data)
                        #success_cpt += 1

            except Exception as e:
                print(f'Erreur lors de la restauration du fichier {file.info.name.name.decode('utf-8')}: {e}')
            success_cpt += 1
            pbar.update(1)

        print(f'{success_cpt} fichier(s) restauré(s) avec succès dans le répertoire: {os.getcwd()}\\restored_files')


def os_is_windows()->bool:
    """
    Vérifie si le système d'exploitation est Windows
    :return: True si Windows, False sinon
    """
    return False if sys.platform != "win32" else True

def executed_as_admin()->bool:
    """
    Vérifie si le programme est exécuté en tant qu'administrateur
    :return: True si l'utilisateur est administrateur, False sinon
    """
    return True if ctypes.windll.shell32.IsUserAnAdmin() else False



if __name__ == "__main__":

    if os_is_windows() and not executed_as_admin():
        print("Ce programme nécessite des privilèges administrateur pour fonctionner correctement.")
        print("Veuillez exécuter le programme en tant qu'administrateur.")
        time.sleep(2)
        sys.exit(1)


    print("Bienvenue sur Cleaner Recovery !")
    strict = True
    while True:
        choice = (int)(input('Menu:\n0: Analyse des fichiers supprimés.\n1: Options.\n2: Quitter '))
        if choice == 0 :
            disks = search_disks()
            if disks is not None:
                chosed_disk = choose_disk(disks)
                print(f"Disque choisi: {chosed_disk}")
                partitions = search_partitions(chosed_disk)
                if partitions is not None:
                    chosed_part = choose_partition(partitions)
                    print(f'Partition choisie: {chosed_part}.')
                    deleted_files = read_partition(chosed_disk, chosed_part, strict)
                    files_to_restore = choose_files_to_restore(deleted_files)
                    if files_to_restore is not None:
                        restore_file(files_to_restore, chosed_disk, chosed_part)
        elif choice == 1:
            print(f'Options:')
            strict_value = (int)(input(f'Lecture des fichiers "ordinaire" lors de l\'analyse des fichiers supprimés ? Actuel: {strict}({(int)(strict)}) '))
            if strict_value == 0:
                strict = False
            elif strict_value == 1:
                strict = True
            else:
                continue
            print(f'Option set to {strict}')
        elif choice == 2:
            break





