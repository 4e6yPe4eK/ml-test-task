import argparse
import pickle
import os
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
parser.add_argument('--model', nargs='?')
parser.add_argument('--length', nargs='?', type=int, default=7, const=7)
parser.add_argument('--prefix', nargs='+')

args = parser.parse_args()

if args.model is None:
    raise ValueError('Аргумент --model не найден')

if not os.path.isfile(args.model):
    raise FileNotFoundError("Файл не найден")

model: Model = pickle.load(open(args.model, 'rb'))
try:
    ret = model.generate(args.prefix, args.length)
    print(ret)
except KeyError as e:
    print("К сожалению, для данной фразы не удалось придумать окончания, попробуйте что-нибудь другое.")

