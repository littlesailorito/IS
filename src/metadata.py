import subprocess
import hashlib
import pytsk3  # type: ignore
from sys import argv

# fdisk run
def run_fdisk(image_path):
   try:
        # Run the fdisk command with sudo
        result = subprocess.run(
            ["sudo", "fdisk", "-l", image_path],
            text=True,  # Ensures the output is a string, not bytes
            capture_output=True,  # Captures stdout and stderr
            check=True  # Raises an exception on non-zero exit code
        )
        print(result.stdout)

   except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
   

def run_mmls(image_path):
    mmls= subprocess.run(["mmls", image_path],capture_output=True, text=True)
    return mmls.stdout

def return_to_report(image_path):
    commands=[subprocess.run(["mmls", image_path],capture_output=True, text=True).stdout,subprocess.run(
            ["sudo", "fdisk", "-l", image_path],
            text=True,  
            capture_output=True,  
            check=True  
        ).stdout]
    return commands


#######################################################Main func#################################################
def extract(image_path):
    print(run_fdisk(image_path))
    print(run_mmls(image_path))




#################################################Getting info partitions##############################################
def extract_file_system_info(img):
    """Extract basic file system information."""
    partitions=[]
    try:
        with open(img, 'rb') as f:
            f.seek(0x1BE)  # Start of partition table
            
            for i in range(4):  # Four partition entries
                entry = f.read(16)
                if len(entry) < 16:
                    break
                
                partition = {
                    "boot_flag": entry[0],  # Boot indicator (0x80 = active)
                    "start_chs": entry[1:4],  # Starting CHS (raw bytes)
                    "partition_type": entry[4],  # Partition type ID
                    "end_chs": entry[5:8],  # Ending CHS (raw bytes)
                    "start_sector": int.from_bytes(entry[8:12], "little"),  # Starting sector (LBA)
                    "total_sectors": int.from_bytes(entry[12:16], "little"),  # Number of sectors
                }
                partitions.append(partition)
        return partitions
    except Exception as e:
        return f"Error extracting file system info: {e}"


def return_start_sector(img):
    """Getting start sector of partitions """
    start_sector=[]
    partitions = []
    partitions=extract_file_system_info(img)
    for i in partitions:
        if i["start_sector"] != 0:
            
            start_sector.append(i["start_sector"]) 

    return start_sector
            
        
    
######################################################################################################

