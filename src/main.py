
from metadata import extract
from data import list_data
from sys import argv



image= argv[1]


def main():
    while True:
        inp= input("1) Print metadata\n2) Print listing of files located on every partition of the disc image\n")
        if inp=="1":
            extract(image)
        elif inp =="2":
            list_data(image)
        else:
            continue
    





main()