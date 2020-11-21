# Output list/friend_list.txt

import os

friend_dict = {}    # key, value = (int)user: (list)friends

egonets = sorted(os.listdir('data/egonets'))
for file in egonets:
    id = int(file.split('.')[0])
    friend_dict[id] = []
    f = open(os.path.join('data/egonets', file), 'r')
    data = f.readlines()
    for line in data:
        line = line.split()
        f_id = int(line[0][:-1])
        friend_dict[id].append(f_id)
        friend_dict[f_id] = [int(i) for i in line[1:]]
    f.close()

keys = sorted(friend_dict.keys())
dir = 'list'
if not os.path.exists(dir):
    os.makedirs(dir)
f = open(os.path.join(dir, 'friend_list.txt'), 'w+')
for k in keys:
    f.write(str(k) + ' ' + ' '.join(str(i) for i in friend_dict[k]) + '\n')
f.close()
