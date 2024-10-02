# Fonction pour lister les disques physiques
def list_disk():
    print("Liste des disques physiques disponibles :")
    disks = []
    for disk in range(10):  # On teste les disques \\.\PhysicalDrive0 à \\.\PhysicalDrive9
        disk_path = f"\\\\.\\PhysicalDrive{disk}"
        if os.path.exists(disk_path):  # Vérifie si le disque existe
            disks.append(disk_path)
            print(f"{len(disks)}. {disk_path}")
    return disks

# Fonction pour permettre à l'utilisateur de choisir un disque
def chose_disk(disks):
    choice = input(f"Choisissez un disque (1-{len(disks)}): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(disks):
            return disks[index]
        else:
            print("Choix non valide.")
            return chose_disk(disks)
    except ValueError:
        print("Entrez un nombre valide.")
        return chose_disk(disks)

# Fonction pour récupérer les partitions d'un disque
def list_partitions(disk):
    try:
        img = pytsk3.Img_Info(disk)
        partition_table = pytsk3.Volume_Info(img)
        partitions = []
        print("Partitions trouvées sur le disque :")
        for part in partition_table:
            print(f"Partition {len(partitions) + 1} : Début = {part.start}, Taille = {part.len}, Type = {part.desc.decode()}")
            partitions.append((part.start, part.len))
        return partitions
    except Exception as e:
        print(f"Erreur lors de la lecture de la table de partitions : {e}")
        return []

# Fonction pour permettre à l'utilisateur de choisir une partition
def choose_partition(partitions):
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
        return choose_partition(partitions