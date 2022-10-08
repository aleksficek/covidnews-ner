import csv
import re
# from pandas import *
from seqeval.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def label_count(some_labels):

    count = 0
    total_labels = 0
    total_labels_i = 0
    mean_labels_per_sentence = 0
    total_words = 0
    mean_label_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for each in some_labels:
        labels_per_sentence = 0
        for i in each:
            if len(i) > 1 and i[:2] == "B-":
                total_labels += 1
                labels_per_sentence += 1
            if len(i) > 1 and i[:2] == "I-":
                total_labels_i += 1
            total_words += 1

        each.reverse()
        i = 0
        current_len = 0

        while i < len(each):
            if len(each[i]) > 1:
                if each[i][:2] == "I-":
                    current_len += 1
                else:
                    mean_label_length[current_len] += 1
                    current_len = 0
            else:
                current_len = 0

            i += 1

        mean_labels_per_sentence = ((mean_labels_per_sentence * count) + labels_per_sentence) / (count + 1)
        count += 1

    output_label_length = 0
    for i, v in enumerate(mean_label_length):
        output_label_length += (i+1)*v
    output_label_length = output_label_length / total_labels

    total_labelled_words = total_labels + total_labels_i

    return total_labels, total_labelled_words, mean_labels_per_sentence, total_words, mean_label_length, output_label_length
            

def main():

    subfolder = "combined"
    train_text = open('final_dataset/'+subfolder+'/train_text.txt', 'r').readlines()
    label_true = open('final_dataset/'+subfolder+'/train_label_true.txt', 'r').readlines()
    label_dist = open('final_dataset/'+subfolder+'/train_label_dist.txt', 'r').readlines()
    # rest_label_dist = open('final_dataset/'+subfolder+'/rest_label_dist.txt', 'r').readlines()
    virus_dict = {}

    strong_labels = []
    weak_labels = []
    rest_weak_labels = []

    for i in range(len(label_true)):
        if not i % 100:
            print("Success to: ", i)

        if len(train_text[i].split()) != len(label_dist[i].split()) or (i < len(label_true) and len(label_true[i].split()) != len(train_text[i].split())):
            print("Error at: ", i)
            print(train_text[i])
            print(label_dist[i])
            print(label_true[i])
            print(len(train_text[i].split()))
            print(len(label_dist[i].split()))
            print(len(label_true[i].split()))
            break
            
        current_text = train_text[i].split()    
        current_strong_labels = label_true[i].split()
        current_buffer = []
        count = 0
        for x, y in enumerate(current_text):
            

            if len(current_buffer) > 0 and (current_strong_labels[x] == "B-virus" or current_strong_labels[x] == "O"):
                print(count)
                count += 1
                to_add = " ".join(current_buffer)
                if to_add not in virus_dict:
                    virus_dict[to_add] = 1
                    current_buffer = []
                else:
                    virus_dict[to_add] += 1
                    current_buffer = []

            if current_strong_labels[x][2:] == "virus":
                if current_strong_labels[x] == "B-virus":
                    current_buffer = []
                current_buffer.append(y)
 

        if len(current_buffer) > 0:
            to_add = " ".join(current_buffer)
            if to_add not in virus_dict:
                virus_dict[to_add] = 1
            else:
                virus_dict[to_add] += 1



        strong_labels.append(label_true[i].split())
        weak_labels.append(label_dist[i].split())

    
    # for i in range(len(rest_label_dist)):
    #     rest_weak_labels.append(rest_label_dist[i].split())

    # weak_labels = weak_labels + rest_weak_labels
    s, a, d, f, g, h = label_count(weak_labels)
    print("Weak total labels: ", s)
    print("Weak total labelled words: ", a, " out of ", f, " avg: ", a / f)
    print("Weak mean labels per sentence: ", d)
    print(g)
    print("Mean weak length: ", h)
    
    s, a, d, f, g, h = label_count(strong_labels)
    print("Strong total labels: ", s)
    print("Strong total labelled words: ", a, " out of ", f, " avg: ", a / f)
    print("Strong mean labels per sentence: ", d)
    print(g)
    print("Mean strong length: ", h)


    print(classification_report(strong_labels, weak_labels, 3))

    total_virus = 0
    for key, value in virus_dict.items():
        total_virus += value
    print(virus_dict)

if __name__ == '__main__':
    main()