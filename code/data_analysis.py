import csv
import re

# train_text.txt - one sequence per line; words seperated by whitespace
f_train = open('train_text.txt', 'r').readlines()

# train_label_dist.txt - one sequence per line; labels seperated by whitespace
f_labels = open('train_label_dist.txt', 'r').readlines()

# types.txt - one entity type per line, lists all entities
f_types = open('types.txt', 'r')

for i in range(0, len(f_train)):
    if len(f_labels[i].strip().split()) != len(f_train[i].strip().split()):
        breakpoint()
        for j in range(0, 70):
            print(f_labels[i].strip().split()[j], f_train[i].strip().split()[j])

# Current preprocessing fails on <p> imbedded in text, first seen in lael 3963