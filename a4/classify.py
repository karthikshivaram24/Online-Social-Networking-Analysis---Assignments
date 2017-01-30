"""
FILE DESCRIPTION:
-----------------

This file contains all methods i use to classify my data as having a positive sentiment towards "Donald Trump" or
negative sentiment towards "Donald Trump", Here i have manually annotated tweets obtained from Collector.py  as 1 or 0
where 1 represents the positive class and 0 represents the negative one, then using this as my training set i have
trained my support vector machine(SVM) classifier using a linear kernel , then i collect my tweets at run time and
i classify them using my trained SVM.

Module Requirements for this File:
1) csv
2) sklearn
3) nltk
4) os

Here you might need to download the nltk stopwords corpus using the command
-- nltk download , then select the one mentioned as stopwords corpus and download it.

"""
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.metrics import classification_report
import os

def read_data(filename,flag):
    """
    This method reads the test/train data file and creates a list of test/train data and
    its labels. The file is .csv file in the form of (tweet_id,tweet_text,tweet_label),
    **
    IMPORTANT: These files have been manually annotated for class label
    **
    :param      filename: The name of the file to read
    :param      flag    : Stating true if train file or false for test file

    :return:    2 lists, one data list and one label list
    """
    data =[]
    label = []
    with open(filename,'r') as fp:
        csv_reader = csv.reader(fp)
        for row in csv_reader:
            # row_terms = row.split(",")
            if flag:
                data.append(row[1])
                label.append(row[2])
            else:
                data.append(row[1])
    fp.close()
    if flag:
        return data,label
    else:
        return data

def vectorize_train_data(data_list,train_test_flag,mindf=4,maxdf=0.8):
    """
    This method reads the list of tweets then converts it to a csr_matrix using sklearns built-in function
    we also remove the stopwords from every tweet using nltk's list of stopwords

    :param data_list: list of tweets
    :return: csr_matrix containing tf-idf values of the tweets
    """
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(min_df=mindf,max_df=maxdf,sublinear_tf=True,use_idf=True,stop_words=stopword_list)

    data_vector = vectorizer.fit_transform(data_list)

    return data_vector,vectorizer

def vectorize_test_data(test_data_list,vectorizer):
    """

    :param test_data_list:
    :param vectorizer:
    :return:
    """
    data_vector = vectorizer.transform(test_data_list)

    return data_vector

def classify(test_vector,train_vector,train_labels,strategy='linear'):
    """
    This method takes in the train and test vectors containing tf-idf scores , train_labels and performs classification
    using SVM(Support Vector Machine, and uses a linear kernel for the strategy) and returns a list of predicted labels
    for the test data.

    :param      test_vector : csr matrix containing tf-idf scores for the test_data
    :param      train_vector: csr matrix containing tf-idf scores for the train_data
    :param      train_labels: list of corresponding labels for the train_data_vector
    :param      strategy    : The type of Kernel to use for a Support Vector Machine

    :return:  A list of predicted labels for the test data
    """
    classifier_linear = svm.SVC(kernel=strategy)
    classifier_linear.fit(train_vector, train_labels)
    prediction_svm_linear = classifier_linear.predict(test_vector)
    return prediction_svm_linear

def classifier_report(test_labels,predicted_labels):
    """
    This method generates classification report using sklearns built-in function comparing true labels to
    predicted labels, and prints the classification Report.

    :param       test_labels      : A list of true labels for the data
    :param       predicted_labels : A list of predicted labels received from the classifier

    :return:     Classification report object
    """
    result = classification_report(test_labels,predicted_labels)
    print(result)
    return result



def save_classify_details(test_data,predicted_labels):
    """
    This method saves the classification details to classify_details.txt, which will be used in our summary.py
    file to read and display the summary of our classification

    :param          test_data        :  Our list of test tweets obtained from collector.py
    :param          predicted_labels :  Our predicted classes/labels for our test data by our classify method.

    :return:        Nothing
    """
    pos_instance = 0
    neg_instance = 0
    index_pos_instance = 0
    index_neg_instance = 0

    for i in range(len(predicted_labels)):
        if predicted_labels[i] == str(0):
            index_neg_instance = i
            neg_instance+=1
        elif predicted_labels[i] == str(1):
            index_pos_instance = i
            pos_instance+=1

    with open("Classify_Folder"+os.path.sep+"classify_details.txt",'w') as fp:
        fp.write("Positive Number of Instances : " + str(pos_instance) + "\n")
        print("Positive Number of Instances : " + str(pos_instance) + "\n")
        fp.write("Negative Number of Instances : " + str(neg_instance)+ "\n")
        print("Negative Number of Instances : " + str(neg_instance)+ "\n")
        fp.write("Positive Instance Example : " + str(test_data[index_pos_instance])+ "\n")
        print("Positive Instance Example : " + str(test_data[index_pos_instance])+ "\n")
        fp.write("Negative Instance Example : " + str(test_data[index_neg_instance])+ "\n")
        print("Negative Instance Example : " + str(test_data[index_neg_instance])+ "\n")

    fp.close()

def main():
    """
    This method just runs all the other methods defined in this file and classifies our data based on the sentiment
    towards "trump"

    :return:
    """

    print("\t\t************************ - Starting cluster.py - ************************ ")

    train_data,train_label = read_data("Manual_annotated_classification_train_data.csv",True)
    test_data = read_data("Collect_Folder"+os.path.sep+"data.csv",False)
    train_vector,vectorizer = vectorize_train_data(data_list=train_data,train_test_flag="train")
    test_vector = vectorize_test_data(test_data_list=test_data,vectorizer=vectorizer)
    predicted_labels = classify(test_vector=test_vector,train_vector=train_vector,train_labels=train_label,strategy="linear")
    save_classify_details(test_data=test_data,predicted_labels=predicted_labels)

    print("\n\t\t************************ - Finished Graph Clustering - ************************")

if __name__ == main():
    main()
