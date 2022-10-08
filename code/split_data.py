import pickle
from labelled_data_analysis import StrongWeakData
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

swd = StrongWeakData()

r_train_text = open('final_dataset/combined/train_text.txt', 'r').readlines()
r_train_label_true = open('final_dataset/combined/train_label_true.txt', 'r').readlines()
r_train_label_dist = open('final_dataset/combined/train_label_dist.txt', 'r').readlines()
r_rest_text = open('final_dataset/combined/rest_text.txt', 'r').readlines()
r_rest_label_dist = open('final_dataset/combined/rest_label_dist.txt', 'r').readlines()

for i in r_train_text:
    swd.strong_text.append(i[:-1].split())
    swd.weak_text.append(i[:-1].split())
for i in r_train_label_true:
    swd.strong_labels.append(i[:-1].split())
for i in r_train_label_dist:
    swd.weak_labels.append(i[:-1].split())
for i in r_rest_text:
    swd.rest_of_weak_text.append(i[:-1].split())
for i in r_rest_label_dist:
    swd.rest_of_weak_labels.append(i[:-1].split())

# swd.strong_text, swd.weak_text = r_train_text, r_train_text
# swd.strong_labels, swd.weak_labels = r_train_label_true, r_train_label_dist
# swd.rest_of_weak_text, swd.rest_of_weak_labels = r_rest_text, r_rest_label_dist

swd2 = pickle.load(open('data5000/unlocked/strong_weak_data.pkl', 'rb'))
split = [0.7, 0.1, 0.2]
entities_set = {
    'B-person': 0,
    'B-location': 0,
    'B-organization': 0,
    'B-time': 0,
    'B-disease': 0,
    'B-virus': 0,
    'B-product': 0,
    'B-animal': 0,
    'B-symptom': 0,
    'B-bacterium': 0
}

def compute_optimal_dist(strong=True):
    entities_inst = entities_set.copy()
    if strong is True:
        all_labels = swd.strong_labels
    else:
        all_labels = swd.weak_labels
    for labels in all_labels:
        for each in labels:
            if each[0:2] == "B-":
                entities_inst[each] += 1

    train, dev, test = entities_set.copy(), entities_set.copy(), entities_set.copy()
    for k, v in entities_inst.items():
        train[k] = int(split[0] * entities_inst[k])
        dev[k] = int(split[1] * entities_inst[k])
        test[k] = int(split[2] * entities_inst[k])

    return entities_inst, train, dev, test

total_optim, train_optim, dev_optim, test_optim = compute_optimal_dist()
pp.pprint(train_optim)
pp.pprint(dev_optim)
pp.pprint(test_optim)
pp.pprint(compute_optimal_dist(strong=False))

def evaluate_splits(train, dev, test):
    distributions = [{}, {}, {}]
    optimal_dist = [train_optim, dev_optim, test_optim]
    total_entities = sum(total_optim.values())
    score = 0

    # count number of entities in each
    for i, partition in enumerate([train, dev, test]):

        entities_inst = entities_set.copy()
        for labels, text in partition:
            for each in labels:
                if each[0:2] == "B-":
                    entities_inst[each] += 1

        
        distributions[i] = entities_inst
    
        for k, v in distributions[i].items():
            score += abs((optimal_dist[i][k] - v) / optimal_dist[i][k])

    # pp.pprint(distributions)
    # print("Score: ", score)
    return distributions, score

# 70, 10, 20 split
split1 = int(split[0] * len(swd.strong_text))
split2 = int((split[0]+split[1]) * len(swd.strong_text))
together = np.array([[swd.strong_labels[k], swd.strong_text[k]] for k in range(len(swd.strong_text))])
together_weak = np.array([[swd.weak_labels[k], swd.weak_text[k]] for k in range(len(swd.weak_text))])
rest_together_weak = np.array([[swd.rest_of_weak_labels[k], swd.rest_of_weak_text[k]] for k in range(len(swd.rest_of_weak_text))])
best_score = 10
best_distributions = {}
best_distributions_weak = {}
saved_splits = []
worst_score = 0
worst_distributions = {}
saved_splits2 = []

for i in range(10000):

    strong_with_weak = np.concatenate((together.copy(),together_weak.copy()),axis=1)

    np.random.seed(i)
    np.random.shuffle(strong_with_weak)

    instance = strong_with_weak[:, :2]
    instance_weak = strong_with_weak[:, 2:]

    p1, p2, p3 = instance[:split1], instance[split1:split2], instance[split2:]
    p1w, p2w, p3w = instance_weak[:split1], instance_weak[split1:split2], instance_weak[split2:]
    
    distributions, score = evaluate_splits(p1, p2, p3)
    if score < best_score:
        best_score = score
        best_distributions = distributions
        saved_splits = [p1, p2, p3]
        saved_splits_weak = [p1w, p2w, p3w]
        best_distributions_weak, _ = evaluate_splits(p1w, p2w, p3w)

    if score > worst_score:
        worst_score = score
        worst_distributions = distributions
        saved_splits2 = [p1, p2, p3]


print("Best Score was: ", best_score)
pp.pprint(best_distributions)

print("Corresponding distribution for weak data was: ")
pp.pprint(best_distributions_weak)

print("Worst Score was: ", worst_score)
pp.pprint(worst_distributions)

# Output train, valid and test strong data
f_train_text = open('final_dataset/splits/strong/train_text.txt', 'w')
f_train_labels = open('final_dataset/splits/strong/train_label_dist.txt', 'w')
f_valid_text = open('final_dataset/splits/strong/valid_text.txt', 'w')
f_valid_labels = open('final_dataset/splits/strong/valid_label_dist.txt', 'w')
f_test_text = open('final_dataset/splits/strong/test_text.txt', 'w')
f_test_labels = open('final_dataset/splits/strong/test_label_dist.txt', 'w')
f_types = open('final_dataset/splits/strong/types.txt', 'w')

# Populate text and label files
for i in saved_splits[0]:
    f_train_text.write(" ".join(i[1]) + '\n')
    f_train_labels.write(" ".join(i[0]) + '\n')

for i in saved_splits[1]:
    f_valid_text.write(" ".join(i[1]) + '\n')
    f_valid_labels.write(" ".join(i[0]) + '\n')

for i in saved_splits[2]:
    f_test_text.write(" ".join(i[1]) + '\n')
    f_test_labels.write(" ".join(i[0]) + '\n')

# Populate list of entities file
for key in entities_set:
    f_types.write(key[2:] + '\n')

# Output train, valid and test weak data
w_train_text = open('final_dataset/splits/weak/train_text.txt', 'w')
w_train_labels = open('final_dataset/splits/weak/train_label_dist.txt', 'w')
w_train_text_rest = open('final_dataset/splits/weak/rest_train_text.txt', 'w')
w_train_labels_rest = open('final_dataset/splits/weak/rest_train_label_dist.txt', 'w')

for i in saved_splits_weak[0]:
    w_train_text.write(" ".join(i[1]) + '\n')
    w_train_labels.write(" ".join(i[0]) + '\n')

for i in rest_together_weak:
    w_train_text_rest.write(" ".join(i[1]) + '\n')
    w_train_labels_rest.write(" ".join(i[0]) + '\n')
