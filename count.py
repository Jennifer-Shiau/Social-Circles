import csv

f = open('data/featureList.txt', 'r')
data = f.readlines()
features = [line[:-1] for line in data] # list of all features' name
f.close()

# Count the number of occurrences of each feature in circle_type
feat_count = {}     # (str)feature: (int)num
for feat in features:
    feat_count[feat] = 0

f = open('list/circle_type.txt', 'r')
data = f.readlines()
for line in data:
    line = line.split()
    for i in line:
        feat_count[i] += 1
f.close()

file = open('list/ours.csv', 'w+')
out_file = csv.writer(file, delimiter=',', lineterminator='\n')
out_file.writerow(['Feature', 'Count'])
feat_count = dict(sorted(feat_count.items(), key=lambda item: item[1], reverse=True))
for k, v in feat_count.items():
    out_file.writerow([k, v])
file.close()
