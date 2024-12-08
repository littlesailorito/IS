from pytsk3 import FS_Info, Img_Info, TSK_FS_META_TYPE_DIR # type: ignore
from sys import argv
from metadata import return_start_sector
from os import system



def list_filesystem(image_path, start_sector,data=[]):
    to_the_report=[]
    """
    List the file structure of a partition in an image.
    Args:
        image_path (str): Path to the disk image.
        start_sector (int): Starting sector of the partition.
    """
    # Open the image in read-only mode
    img = Img_Info(image_path)

    # Access the filesystem
    offset = start_sector * 512  # Convert sectors to bytes
    fs = FS_Info(img, offset)

    def traverse_directory(directory, parent_path="/"):
        """
        Recursively list directory contents.
        Args:
            directory: pytsk3 directory object.
            parent_path: Current path in the directory tree.
        """
        for entry in directory:
            if not hasattr(entry, "info") or not entry.info.name:
                continue

            # Get the name of the entry
            name = entry.info.name.name.decode("utf-8", "ignore")
            if name in [".", ".."]:
                continue  # Skip special entries

            # Create the full path
            full_path = f"{parent_path}/{name}"

            # Check if it's a directory or file
            if entry.info.meta and entry.info.meta.type == TSK_FS_META_TYPE_DIR:
                print(f"Directory: {full_path}")
                data.append(f"{full_path}\n")
                try:
                    sub_directory = entry.as_directory()
                    traverse_directory(sub_directory, full_path)  # Recurse into sub-directory
                except Exception as e:
                    print(f"Error accessing directory {full_path}: {e}")
            else:
                print(f"File: {full_path}")
                data.append(f"{full_path}\n")

    # Start traversal from the root directory
    root_dir = fs.open_dir("/")
    traverse_directory(root_dir)

def return_data(img):
    data_to_write=[]
    return_start= return_start_sector(img)
    data_to_write.append("Begin of the list that contains all files:\n")
    for index,i in enumerate(return_start):
        list_filesystem(img,i,data_to_write)
        system("clear")
        data_to_write.append(f"\nEnd of the {index+1} partition\n")

    return  data_to_write

def list_data(img):
    start_sector = return_start_sector(img)    
    for index,i in enumerate(start_sector):
        print("Begin of the list that contains all files:\n")
        print(list_filesystem(img, i))
        print(f"\nEnd of the {index+1} partition\n")
    
