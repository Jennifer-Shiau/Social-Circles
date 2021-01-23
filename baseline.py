import os
import copy
import numpy as np
from utils import evaluate, sigmoid
from timeList import Node

np.random.seed(123564)

n_iters = 1000
lambda_reg = 0.001
feature_size = 58

# Variable to keep track of time 
time = 1

# Function to perform DFS starting 
# from node u 
def dfs(u, TimeDAG, timeList):
     
    global time
     
    # Storing the pre number whenever 
    # the node comes into recursion stack 
    TimeDAG[u].set_pre(time)
 
    # Increment time 
    time += 1
    TimeDAG[u].visited()
     
    for v in TimeDAG[u].child:
        if (TimeDAG[v].vis == 0):
            dfs(v, TimeDAG, timeList)
             
    # Storing the post number whenever 
    # the node goes out of recursion stack 
    TimeDAG[u].set_post(time)
    timeList.append(u)
    time += 1

def topological_sort(TimeDAG):
    #find initial node
    node_zero_degree = []
    timeList = []
    for k in TimeDAG.keys():
        if len(TimeDAG[k].parents) == 0:
            node_zero_degree.append(k)
    for i in node_zero_degree:
        dfs(i, TimeDAG, timeList)
    return timeList

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

        #work initialize
        work_buff = []
        work_start_date = []
        work_end_date = []

        for feat in line:
            feat = feat.split(';')
            key = ';'.join(feat[:-1])
            value = int(feat[-1])
            #work
            if 'work' in key:
                work_key = key
                if 'project' in key:
                    work_key = key.replace(';projects',"")

                
                if work_key in work_buff:
                    #empty buffer
                    work_buff.clear()
                    work_buff.append(work_key)
                    #new work experience
                    #check dates of last work are comleted or not                    
                    if len(work_start_date) < len(work_end_date):
                        for i in range(len(work_end_date) - len(work_start_date)):
                            work_start_date.append(float("inf"))
                            
                    elif len(work_start_date) > len(work_end_date):
                        for i in range(len(work_start_date) - len(work_end_date)):
                            work_end_date.append(-1)
                    else:
                        if len(work_start_date) != 0:
                            if work_end_date[-1] < 0:
                                continue
                            elif work_start_date[-1] > 100000:
                                continue
                            if work_start_date[-1] in TimeDAG.keys():
                                TimeDAG[work_start_date[-1]].add_child(work_end_date[-1])
                            else:
                                TimeDAG[work_start_date[-1]] = Node(work_start_date[-1])
                                TimeDAG[work_start_date[-1]].add_child(work_end_date[-1])
                                
                            if work_end_date[-1] in TimeDAG.keys():
                                TimeDAG[work_end_date[-1]].add_parent(work_start_date[-1])
                            else:
                                TimeDAG[work_end_date[-1]] = Node(work_end_date[-1])
                                TimeDAG[work_end_date[-1]].add_parent(work_start_date[-1])
                else:
                    work_buff.append(work_key)
                if 'start' in key:
                    work_start_date.append(value)
                if 'end' in key:
                    work_end_date.append(value)

                    
            temp[key].append(value)
        if len(work_start_date) < len(work_end_date):
            for i in range(len(work_end_date) - len(work_start_date)):
                work_start_date.append(float("inf"))
               
        elif len(work_start_date) > len(work_end_date):
            for i in range(len(work_start_date) - len(work_end_date)):
                work_end_date.append(-1)
        else:
            if len(work_start_date) != 0:
                if work_start_date[-1] in TimeDAG.keys():
                    TimeDAG[work_start_date[-1]].add_child(work_end_date[-1])
                else:
                    TimeDAG[work_start_date[-1]] = Node(work_start_date[-1])
                    TimeDAG[work_start_date[-1]].add_child(work_end_date[-1])
                    
                if work_end_date[-1] in TimeDAG.keys():
                    TimeDAG[work_end_date[-1]].add_parent(work_start_date[-1])
                else:
                    TimeDAG[work_end_date[-1]] = Node(work_end_date[-1])
                    TimeDAG[work_end_date[-1]].add_parent(work_start_date[-1])
        temp['aligned_work_start_date'] = work_start_date
        temp['aligned_work_end_date'] = work_end_date
        feature_dict[id] = temp
        print('\rFinish processing ID %d' % id, end='')
    print('\n')
    f.close()

   

def similarity(x1, x2):
    phi = []
    for feat in features:
        if feat != 'aligned_work_start_date' and feat!='aligned_work_end_date' and feat!='overlap':
            sup = feature_dict[x1][feat]
            que = feature_dict[x2][feat]
            v = evaluate(sup, que)
            phi.append(v)
    #distinguish work time overlap or not
    x1_start = feature_dict[x1]['aligned_work_start_date']
    x2_start = feature_dict[x2]['aligned_work_start_date']
    x1_end = feature_dict[x1]['aligned_work_end_date']
    x2_end = feature_dict[x2]['aligned_work_end_date']
    overlap = 0

    for i in range(len(x1_start)):
        for j in range(len(x2_start)):
            if x1_end[i]==-1 or x2_end[j]==-1 or x1_start[i]==float("inf") or x2_start[j]==float("inf"):
                continue            
            tmp_start_idx = [x1_start[i], x2_start[j]]
            tmp_end_idx = [x1_end[i], x2_end[j]]
            tmp_start_value = np.array([TimeDAG[tmp_start_idx[0]].timeLine, TimeDAG[tmp_start_idx[1]].timeLine])
            tmp_end_value = np.array([TimeDAG[tmp_end_idx[0]].timeLine, TimeDAG[tmp_end_idx[1]].timeLine])
            if np.max(tmp_end_value) < tmp_start_value[np.argmin(tmp_end_value)]:
                overlap = 1
    phi.append(overlap)


    return np.array(phi)

def run(circle_dict, featureBaseline):
    keys = sorted(circle_dict.keys())

    for k in keys:  # for each circle
        idx_num = len(circle_dict[k])
        for i in range(idx_num):
            for j in range(idx_num):
                if i!=j:
                    tmp = similarity(circle_dict[k][i], circle_dict[k][j])

                    featureBaseline += tmp
        #ouput to txt
        arg = np.flipud(np.argsort(featureBaseline))
        print(arg)
        dir = 'baseline'
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open(os.path.join(dir, 'circle{}_baseline.txt'.format(k)), 'w+')
        for a in arg:
            f.write(features[a] + ' ' + str(featureBaseline[a]) + '\n')
        f.close()

        print('\nOutput \'%s\'\n' % os.path.join(dir, 'circle{}_baseline.txt'.format(k)))



if __name__ == '__main__':
    f = open('data/featureList.txt', 'r')
    data = f.readlines()
    features = [line[:-1] for line in data] # list of all features' name
    f.close()
    features.append('overlap')

    feature_dict = {}   # (int)user: (dict)features
                        #                  (str)feature: (list)values
    TimeDAG = {}
    process_feature()

    TimeList = topological_sort(TimeDAG)
    g = open('timelist.txt', 'w')
    for t in TimeList:
        g.write(str(t)+" ")
    g.close()
    #analysis TimeList
    for i, t in enumerate(TimeList):
        TimeDAG[t].set_timeLine(i)
    TimeDAG[-1] = Node(-1)
    TimeDAG[-1].set_timeLine(-1)
    TimeDAG[float("inf")] = Node(float("inf"))
    TimeDAG[float("inf")].set_timeLine(float("inf"))

    result_dir = 'results'
    os.makedirs(result_dir, exist_ok=True)
    
    circles = sorted(os.listdir('data/circles'))
    circle_dict = {}
    for file in circles:
        id = int(file.split('.')[0])
        f = open(os.path.join('data/circles', file), 'r')
        data = f.readlines()
        for line in data:
            line = line.split()
            f_id = int(line[0][6:-1])
            circle_dict[f_id] = [int(i) for i in line[1:]]
            circle_dict[f_id].append(id)
        f.close()
        featureBaseline = np.zeros(shape=(feature_size,),dtype=int)
        run(circle_dict, featureBaseline)