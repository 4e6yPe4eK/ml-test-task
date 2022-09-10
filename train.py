import argparse
import pickle
import glob
import os
import re
import sys
import random


class Model:
    def __init__(self):
        self.data = {}
        self.N = 3

    def fit(self, x, y):
        counter = {}
        for ind in range(len(x)):
            if x[ind] not in counter:
                counter[x[ind]] = [0, {}]
            counter[x[ind]][0] += 1
            if y[ind] not in counter[x[ind]][1]:
                counter[x[ind]][1][y[ind]] = 0
            counter[x[ind]][1][y[ind]] += 1
        for pref, (cnt, dct) in counter.items():
            lst = []
            for key, amount in dct.items():
                lst.append((key, amount / cnt))
            self.data[pref] = list(zip(*lst))

    def generate(self, prefix=None, length=7):
        if prefix is None:
            prefix = random.choice(list(self.data.keys()))
            ret = list(prefix)
        else:
            choices = []
            ret = list(map(str.lower, prefix))
            prefix = tuple(ret[max(len(ret) - self.N, 0):len(ret)])
            for key in self.data.keys():
                for x in range(len(prefix)):
                    if key[x] != prefix[x]:
                        break
                else:
                    choices.append(key)
            if not choices:
                raise KeyError
            prefix = random.choice(choices)
            if len(ret) < len(prefix):
                ret = list(prefix)
        while len(ret) < length:
            ret.append(random.choices(*self.data[prefix])[0])
            prefix = tuple(ret[len(ret) - self.N:len(ret)])
        return " ".join(ret[:length]).capitalize()


parser = argparse.ArgumentParser()

parser.add_argument("--input-dir", nargs='?')
parser.add_argument("--model", nargs='?', default='./model.pkl', const='./model.pkl')

args = parser.parse_args()

data_dir = args.input_dir
model_file = args.model

model = Model()

train_x = []
train_y = []
if not data_dir:
    words = re.findall('[А-Яа-я]+-?[А-Яа-я]*', sys.stdin.read().lower())
    for i in range(len(words) - model.N):
        train_x.append(tuple(words[i:i + model.N]))
        train_y.append(words[i + model.N])
else:
    if not os.path.isdir(data_dir):
        raise IsADirectoryError("--input-dir argument is not directory")
    for text_file in glob.glob(os.path.join(data_dir, '**/*'), recursive=True):
        if not os.path.isfile(text_file):
            continue
        file = open(text_file, encoding='utf-8')
        words = re.findall('[А-Яа-я]+-?[А-Яа-я]*', file.read().lower())
        for i in range(len(words) - model.N):
            train_x.append(tuple(words[i:i + model.N]))
            train_y.append(words[i + model.N])

model.fit(train_x, train_y)
pickle.dump(model, open(model_file, 'wb'))
