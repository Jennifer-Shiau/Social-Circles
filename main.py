import os
import copy
import numpy as np
from utils import evaluate, sigmoid

np.random.seed(123564)

n_iters = 1000
lambda_reg = 0.001
feature_size = 57


def process_feature():
    print('\nStart processing features ...\n')

    # Initialize a helper dictionary
    feat_init = {}      # (str)feature: (list)[]
    for feat in features:
        feat_init[feat] = []

    f = open('data/features.txt', 'r')
    data = f.readlines()
    for line in data:
        line = line.split()
        id = int(line[0])
        line = line[1:]
        temp = copy.deepcopy(feat_init)
        for feat in line:
            feat = feat.split(';')
            key = ';'.join(feat[:-1])
            value = int(feat[-1])
            temp[key].append(value)
        feature_dict[id] = temp
        print('\rFinish processing ID %d' % id, end='')
    print('\n')
    f.close()

def similarity(x1, x2):
    phi = []
    for feat in features:
        sup = feature_dict[x1][feat]
        que = feature_dict[x2][feat]
        v = evaluate(sup, que)
        phi.append(v)
    return np.array(phi)

def run(circle_dict):
    keys = sorted(circle_dict.keys())

    for k in keys:  # for each circle
        w = np.zeros((feature_size,))
        b = np.zeros((1,))
        
        lr = 1
        # w_prev = np.zeros(len(w))
        # b_prev = 0

        for _ in range(n_iters):
            # sample a distinct circle
            while True:
                _k = np.random.choice(keys, 1)[0]
                if _k != k:
                    break
            
            # sample 2 distinct samples in circle k
            x1 = np.random.choice(circle_dict[k], 1)[0]
            while True:
                x2 = np.random.choice(circle_dict[k], 1)[0]
                if x2 != x1:
                    break
            
            # sample 1 sample in circle _k
            _x = np.random.choice(circle_dict[_k], 1)[0]

            # similarity of (x1, x2)
            phi = similarity(x1, x2)

            # similarity of (x1, _x)
            _phi = similarity(x1, _x)

            # logistic regression
            y = sigmoid(np.dot(phi, w.T) + b)
            _y = sigmoid(np.dot(_phi, w.T) + b)

            loss = -1 * (np.dot(1, np.log(y)) + np.dot(1-1, np.log(1 - y))) \
                -1 * (np.dot(0, np.log(_y)) + np.dot(1-0, np.log(1 - _y)))
            print('\r==> Circle %d\t|  Loss: %.4f' % (k, loss), end='')

            # w_grad = np.dot(phi.T, y - 1) + np.dot(_phi.T, _y - 0) + lambda_reg * np.sign(w)
            w_grad = (y - 1) * phi + (_y - 0) * _phi + lambda_reg * np.sign(w)
            b_grad = np.sum(y - 1) + np.sum(_y - 0)

            # w_prev += w_grad**2
            # b_prev += b_grad**2
            # w_ada = np.sqrt(w_prev)
            # b_ada = np.sqrt(b_prev)
            # w -= lr * w_grad / w_ada
            # b -= lr * b_grad / b_ada

            w -= lr * w_grad
            b -= lr * b_grad
        print(' ... done')

        # for j in range(feature_size):
        #     print(features[j], ':', w[j])

        idx = np.argsort(w)[::-1]
        temp = np.array(features)[idx]
        w = np.sort(w)[::-1]
        f = open(os.path.join(result_dir, '%d.txt' % k), 'w')
        for i in range(feature_size):
            f.write('%.4f'%w[i] + '\t' + temp[i] + '\n')
        f.close()
    return


if __name__ == '__main__':
    f = open('data/featureList.txt', 'r')
    data = f.readlines()
    features = [line[:-1] for line in data] # list of all features' name
    f.close()

    feature_dict = {}   # (int)user: (dict)features
                        #                  (str)feature: (list)values
    process_feature()

    result_dir = 'results'
    os.makedirs(result_dir, exist_ok=True)
    
    circles = sorted(os.listdir('data/circles'))
    for file in circles:
        circle_dict = {}    # (int)circleID: (list)members in the circle
        # id = int(file.split('.')[0])
        # circle_dict[id] = []
        f = open(os.path.join('data/circles', file), 'r')
        data = f.readlines()
        for line in data:
            line = line.split()
            c_id = int(line[0][6:-1])
            # circle_dict[id].append(f_id)
            circle_dict[c_id] = [int(i) for i in line[1:]]
        f.close()
        run(circle_dict)
        