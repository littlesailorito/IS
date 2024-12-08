
from metadata import extract
from data import list_data
from write_rap import report
from sys import argv




image= argv[1]


def main():
    
    while True:
        inp= input("1) Print metadata\n2) Print listing of the files located on every partition of the disc's image\n3) Write into the file a image's report\n")
        if inp=="1":
            extract(image)
        elif inp =="2":
            list_data(image)
        elif inp=="3":
            
            report(image)



    





main()