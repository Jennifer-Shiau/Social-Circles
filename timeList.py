




class Node:

    def __init__(self, index):
        self.idx = index
        self.child = []
        self.parents = []
        self.vis = 0
        self.pre = 0
        self.post = 0
        #the larger the earlier
        self.timeLine = -1

    
    def check_child(self, child_idx):
        if child_idx in self.child:
            return True
        else:
            return False

    def check_parent(self, parent_idx):
        if parent_idx in self.parents:
            return True
        else:
            return False  

    
    def add_child(self, child_idx):
        if self.check_child(child_idx) == False:
            self.child.append(child_idx)

    def add_parent(self, parent_idx):
        if self.check_parent(parent_idx) == False:
            self.parents.append(parent_idx)

    def visited(self):
        self.vis = 1
    
    def set_pre(self, order):
        self.pre = order
    
    def set_post(self, order):
        self.post = order

    def set_timeLine(self, order):
        self.timeLine = order
        