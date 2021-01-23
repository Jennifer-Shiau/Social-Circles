# Variable to keep track of time 
time = 1
 
# Function to perform DFS starting 
# from node u 
def dfs(u, aList, pre, post, vis):
     
    global time
     
    # Storing the pre number whenever 
    # the node comes into recursion stack 
    pre[u] = time
 
    # Increment time 
    time += 1
     
    vis[u] = 1
     
    for v in aList[u]:
        if (vis[v] == 0):
            dfs(v, aList, pre, post, vis)
             
    # Storing the post number whenever 
    # the node goes out of recursion stack 
    post[u] = time
    time += 1
 
# Driver code 
if __name__=='__main__':
     
    # Number of nodes in graph 
    n = 6
 
    # Adjacency list 
    aList = [[] for i in range(n + 1)]
     
    pre = [0 for i in range(n + 1)]
    post = [0 for i in range(n + 1)]
 
    # Visited array 
    vis = [0 for i in range(n + 1)]
     
    # Edges 
    aList[1].append(2)
    aList[2].append(1) 
    aList[2].append(4) 
    aList[4].append(2) 
    aList[1].append(3) 
    aList[3].append(1) 
    aList[3].append(4) 
    aList[4].append(3) 
    aList[3].append(5) 
    aList[5].append(3) 
    aList[5].append(6)
    aList[6].append(5) 
 
    # DFS starting at Node 1 
    dfs(1, aList, pre, post, vis)
 
    # Number of nodes in graph 
    for i in range(1, n + 1):
        print("Node " + str(i) +
              " Pre number " + str(pre[i]) +
              " Post number " + str(post[i]))
 
# This code is contributed by rutvik_56