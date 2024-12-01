import subprocess
import hashlib


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

def extract_partition_info(fdisk_output):
    lines = fdisk_output.splitlines()
    partitions = []
    
    for line in lines:
        if len(line.split()) >= 6 and line[0] != 'Device':
            parts = line.split()
            partitions.append({
                "device": parts[0],
                "boot": parts[1],
                "start": parts[2],
                "end": parts[3],
                "size": parts[4],
                "id": parts[5],
                "type": parts[6]
            })
    
    return partitions


def extract(image_path):
    print(run_fdisk(image_path))
    print(run_mmls(image_path))