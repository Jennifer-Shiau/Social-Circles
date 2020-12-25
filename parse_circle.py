import os

circle_dict = {}    # (int)user: (list)members in the circle

circles = sorted(os.listdir('data/circles'))
for file in circles:
    id = int(file.split('.')[0])
    circle_dict[id] = []
    f = open(os.path.join('data/circles', file), 'r')
    data = f.readlines()
    for line in data:
        line = line.split()
        f_id = int(line[0][6:-1])
        circle_dict[id].append(f_id)
        circle_dict[f_id] = [int(i) for i in line[1:]]
    f.close()

keys = sorted(circle_dict.keys())
dir = 'list'
if not os.path.exists(dir):
    os.makedirs(dir)
f = open(os.path.join(dir, 'circle_list.txt'), 'w+')
for k in keys:
    f.write(str(k) + ' ' + ' '.join(str(i) for i in circle_dict[k]) + '\n')
f.close()

print('\nOutput \'%s\'\n' % os.path.join(dir, 'circle_list.txt'))
