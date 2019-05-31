"""
@author Farzaneh.Tlb
5/30/19 4:29 PM
Implementation of data analytics (Fill this line)
"""

import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import wilcoxon

def read_task(file_name):
    # with open(file_name) as csvfile:
    csvfile = open(file_name)
    dataset = csv.reader(csvfile, delimiter=',')
    np_dataset = np.empty([180, 7])
    i = 0
    for row in dataset:
        row[0] = str.replace(row[0], '[', '')
        row[4] = str.replace(row[4], ']', '')
        morph_level = str.split(row[1], "/")[0]
        morph_level = str.replace(morph_level, "'", "")
        img_num = str.split(row[1], "/")[1]
        img_num = str.replace(img_num, "'", "")

        np_dataset[i, 0] = row[0]
        np_dataset[i, 1] = morph_level
        np_dataset[i, 3] = row[3]
        row[2] = str.replace(row[2], " ", "")
        row[2] = str.replace(row[2], "'", "")

        np_dataset[i, 2] = 1 if row[2] == 'male' else 2
        row[4] = str.replace(row[4], " ", "")

        np_dataset[i, 4] = int(row[4])
        # print(row[4])

        np_dataset[i, 5] = img_num
        np_dataset[i, 6] = 1 if int(morph_level) < 0 else 2
        np_dataset[i, 6] = 3 if morph_level == 0 else np_dataset[i, 6]

        i = i + 1

    return np_dataset


def get_trial_by_degree(dataset, degree):
    response = dataset[np.where(dataset[:, 4] == degree)]
    return response


def get_trial_by_answer_morph(dataset, answer, morph_level):
    response = dataset[np.where(dataset[:, 1] == morph_level)]
    response = response[np.where(response[:, 2] == answer)]
    return response


def get_trial_by_morph(dataset, morph_level):
    response = dataset[np.where(dataset[:, 1] == morph_level)]
    return response


def get_trial_by_answer_degree(dataset, answer, degree):
    response = dataset[np.where(dataset[:, 4] == degree)]
    response = response[np.where(response[:, 2] == answer)]
    return response


def get_trial_by_real_degree(dataset, real, degree):
    response = dataset[np.where(dataset[:, 4] == degree)]
    response = response[np.where(response[:, 6] == real)]
    return response


def get_trial_by_answer_degree_morph(dataset, answer, morph, degree):
    response = dataset[np.where(dataset[:, 1] == morph)]
    response = response[np.where(response[:, 4] == degree)]
    response = response[np.where(response[:, 2] == answer)]
    return response


def get_trial_by_degree_morph(dataset, morph, degree):
    response = dataset[np.where(dataset[:, 1] == morph)]
    response = response[np.where(response[:, 4] == degree)]
    return response


def get_performance(dataset, ):
    return len(np.where(dataset[:, 2] == dataset[:, 6])[0]) / 160


def pf(x, alpha, beta):
    return 1. / (1 + np.exp(-(x - alpha) / beta))


dataset = read_task("13.csv")
print(dataset[0])

x_data = [-40, -30, -20, -10, 0, 10, 20, 30, 40]
degrees = [90, 180]
for i in range(3, 15, 1):
    dataset = read_task(str(i) + ".csv")
    for deg in degrees:
        if (deg == 90):
            col = 'red'
        else:
            col = 'blue'
        y_data = []
        for num in x_data:
            y_data.append((get_trial_by_answer_degree_morph(dataset, 2, num, deg).shape[0]) /
                          get_trial_by_degree_morph(dataset, num, deg).shape[0])
        print(deg, "female", get_trial_by_real_degree(dataset, 2, deg).shape[0])
        print(deg, "male", get_trial_by_real_degree(dataset, 1, deg).shape[0])

        par, mcov = curve_fit(pf, x_data, y_data)
        plt.subplot(2, 6, i - 2)
        plt.title("user" + str(i))
        plt.plot(x_data, y_data, 'o', color=col)
        # plt.plot(x_data, y_data, 'o', color='red' if deg == 90 else 'blue')
        plt.plot(x_data, pf(x_data, par[0], par[1]), color='red' if deg == 90 else 'blue')
        if deg == 90:
            y_data_90 = y_data
        else:
            d = np.array(y_data_90) - np.array(y_data)
            w, p = wilcoxon(d)
            print(w, p, i)
plt.show()

# for i in range(3,14,1):
#     dataset = read_task(str(i) + ".csv")
#     print(get_trial_by_degree(dataset,90).shape[0])
#     print(get_trial_by_degree(dataset,180).shape[0])
#     print("\n")
