import os
import copy
from utils import spinner, evaluate

f = open('data/featureList.txt', 'r')
data = f.readlines()
features = [line[:-1] for line in data] # list of all features' name
f.close()

# Initialize a helper dictionary
feat_init = {}      # (str)feature: (list)[]
for feat in features:
    feat_init[feat] = []

# Step 1
print('\nStart processing features ...\n')

feature_dict = {}   # (int)user: (dict)features
                    #                  (str)feature: (list)values

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

# Step 2
print('\nCounting number of values of each feature ...  ', end='')

temp_values = {}    # (str)feature: (set){}
for feat in features:
    temp_values[feat] = set()

i = 0
for user in feature_dict.keys():
    for feat in features:
        values = feature_dict[user][feat]
        for v in values:
            temp_values[feat].add(v)
            i += 1
            print('\b%s' % spinner[i%4], end='')

feat_count = {}     # (str)feature: (int)value
for feat in features:
    feat_count[feat] = len(temp_values[feat])

print('\bdone\n')

# Step 3
print('\nStart evaluating features of each user and his/her friends ...\n')

feat_value = {}     # (str)feature: (int)value
for feat in features:
    feat_value[feat] = 0

f = open('list/friend_list.txt')
data = f.readlines()
for line in data:
    line = [int(i) for i in line.split()]
    user = line[0]
    friends = line[1:]
    
    for friend in friends:
        for feat in features:
            sup = feature_dict[user][feat]
            que = feature_dict[friend][feat]
            v = evaluate(sup, que)
            feat_value[feat] += v
    print('\rFinish evaluating ID %d' % user, end='')
print('\n')
f.close()

for feat in features:
    feat_value[feat] *= feat_count[feat]

result = dict(sorted(feat_value.items(), key=lambda item: item[1], reverse=True))

# Output result
dir = 'list'
if not os.path.exists(dir):
    os.makedirs(dir)
f = open(os.path.join(dir, 'feature_value.txt'), 'w+')
for k in result.keys():
    f.write(k + ' ' + str(result[k]) + '\n')
f.close()

print('Output \'%s\'\n' % os.path.join(dir, 'feature_value.txt'))
print('\nDone\n')
