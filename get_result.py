import os
import random
from numpy import mean, std, cov

num_features = 3

# Original
root = 'results'
output_files = sorted(os.listdir(root))
print('==> Total: %d' % len(output_files))
result = set()
for file in output_files:
    f = open(os.path.join(root, file), 'r')
    data = f.readlines()
    tmp = []
    for i, line in enumerate(data):
        line = line.split('\t')[1][:-1]
        tmp.append(line)
        if i == num_features - 1:
            break
    result.add(tuple(sorted(tmp)))

print('==> Original: %d' % len(result))


# Compute correlation
print()
f = open('data/featureList.txt', 'r')
data = f.readlines()
features = [line[:-1] for line in data] # list of all features' name
f.close()

feature_dict = {}   # (str)features: (list)values
for feat in features:
    feature_dict[feat] = []

f = open('data/features.txt', 'r')
data = f.readlines()
for line in data:
    line = line.split()
    id = int(line[0])
    line = line[1:]
    for feat in line:
        feat = feat.split(';')
        key = ';'.join(feat[:-1])
        value = int(feat[-1])
        feature_dict[key].append(value)
    print('\rFinish processing ID %d' % id, end='')
print()
f.close()

print('\nComputing correlation ...  ', end='')
corr = {}
for i in range(len(features)-1):
    for j in range(i+1, len(features)):
        f1 = feature_dict[features[i]]
        f2 = feature_dict[features[j]]
        if len(f1) > len(f2):
            f1 = f1[:(len(f2))]
            # f1 = random.sample(f1, k=len(f2))
        else:
            f2 = f2[:(len(f1))]
            # f2 = random.sample(f2, k=len(f1))
        c = (cov(f1, f2) / (std(f1)*std(f2)))[0][1]
        corr[(features[i], features[j])] = c
        corr[(features[j], features[i])] = c
print('\bdone')

f = open(os.path.join('list', 'correlation.txt'), 'w+')
corr = dict(sorted(corr.items(), key=lambda item: item[1], reverse=True))
for k, v in corr.items():
    f.write('(' + k[0] + ', ' + k[1] + ')' + ' ' + '%.4f'%v + '\n')
f.close()

print('\nOutput \'%s\'\n' % os.path.join('list', 'correlation.txt'))


# Improved
thre = 0.2
result = set()
for file in output_files:
    f = open(os.path.join(root, file), 'r')
    data = f.readlines()
    tmp = []
    for i, line in enumerate(data):
        if float(line.split('\t')[0]) < 1.0:
            continue
        feat = line.split('\t')[1][:-1]
        if len(tmp) == 0:
            tmp.append(feat)
        elif len(tmp) == 1 and corr[(feat, tmp[0])] < thre:
            tmp.append(feat)
        elif len(tmp) == 2 and corr[(feat, tmp[0])] < thre and corr[(feat, tmp[1])] < thre:
            tmp.append(feat)
        if i == num_features - 1:
            break
    result.add(tuple(sorted(tmp)))

print('==> Improved: %d' % len(result))

f = open(os.path.join('list', 'circle_type.txt'), 'w+')
for tup in result:
    tup = list(tup)
    f.write(' '.join(tup) + '\n')
f.close()

print('\nOutput \'%s\'\n' % os.path.join('list', 'circle_type.txt'))
