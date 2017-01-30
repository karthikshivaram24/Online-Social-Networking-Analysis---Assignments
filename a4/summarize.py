import os

def read_method_details():
    """
    This method reads the details saved in files that occurs when you run Collector.py, Cluster.py and Classify.py
    and prints the details to screen and save it to "summary.txt" .

    :return: Nothing
    """

    with open("Collect_Folder"+ os.path.sep + "collector_details.txt",'r' ) as fp:
         collector_details = fp.read()
    fp.close()
    with open("Cluster_Folder" + os.path.sep + "cluster_details.txt",'r') as gp:
        cluster_details = gp.read()
    gp.close()
    with open("Classify_Folder" + os.path.sep + "classify_details.txt",'r') as dp:
        classify_details = dp.read()
    dp.close()

    with open("summary.txt",'w') as sp:
        sp.write("Collector.py Details : \n")
        sp.write(collector_details)
        sp.write("Cluster.py Details : \n")
        sp.write(cluster_details)
        sp.write("Classify.py Details : \n")
        sp.write(classify_details)

    sp.close()

    print("Details saved to --> summary.txt")

    return collector_details,cluster_details,classify_details


def main():

    print("\t\t************************ - Starting summary.py - ************************ ")

    collector_details,cluster_details,classify_details  = read_method_details()
    print("\n")
    print("\t\t---- Collect_Details ----\n")
    print(collector_details)
    print("\n")
    print("\t\t---- Cluster_Details ----\n")
    print(cluster_details)
    print("\n")
    print("\t\t---- Classifier_Details ----\n")
    print(classify_details)
    print("\n")
    print("\n\t\t************************ - Finished Printing Summary - ************************")


if __name__ == main():
    main()
