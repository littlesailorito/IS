from metadata import return_to_report
from data import return_data
from os import system


def report(img):

    with open("../Results/Report.txt","w") as file:
        data=return_data(img)
        
        for i in return_to_report(img):
            file.write(i)
            file.write("\n")
        for i in data:
            file.write(i)
            file.write("\n")
    print("Report has been successfully written in the Results")