# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from preprocessing import get_dataset_list, get_X, get_Y

dataset = get_dataset_list("datasets/dataset_koppel.csv")
namen = dataset[0]
del dataset[0]

x = get_X(0, 1, dataset)
y = get_Y(1, dataset)

plt.plot(x, y)
plt.hlines(2500, 0, 23, colors='red', linestyles='solid')
plt.xticks(range(0, 25, 2))
plt.yticks(range(0, 4001, 500))
plt.show()