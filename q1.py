import sys#for taking input
Node_Limit=3

class bptnode:

	def __init__(self):
		"""
		Initialize node
		Same node structure for leaf and non-leaf nodes for consistency
		"""

		self.keys=[]#stores values to compare
		self.ptrarr=[]#stores pointers to child
		self.is_leaf=True#true if leaf node
		self.next=None#for leaf nodes points to next leaf node



	def splitnode(self):
		"""
		splits node when overflows
		first half goes to original node
		second half goes to next node
		"""

		#store mid for splitting
		mid=len(self.keys)//2#int division
		
		#store median to return
		midval=self.keys[mid]

		#create new node
		tnode=bptnode()
		
		if(self.is_leaf):

            #new node changes
			tnode.keys=self.keys[mid:]
			tnode.ptrarr=self.ptrarr[mid:]
			tnode.is_leaf=self.is_leaf
			tnode.next=self.next

            #original node changes
			self.keys=self.keys[:mid]
			self.ptrarr=self.ptrarr[:mid]
			self.next=tnode

		else:

            #new node changes
			tnode.keys=self.keys[mid+1:]
			tnode.ptrarr=self.ptrarr[mid+1:]
			tnode.is_leaf=self.is_leaf

            #original node changes
			self.keys=self.keys[:mid]
			self.ptrarr=self.ptrarr[:mid+1]

		return [midval,tnode]



class bptree(bptnode):

	def __init__(self):
		"""
		Initialise the tree
		"""

		self.root=bptnode()
	


	def rq(self,l,r):
		"""
		Perform range query from [l,r]
		"""
        
		#get largest node less than l
		start=self.get_start_node(l,self.root)

		ans=0
		while(start):
			count,start=self.countnodes(l,r,start)
			ans+=count

		return ans



	def get_start_node(self,val,node):
		"""
		Give start node to perform range query
		"""

        #when node = leaf node return
		if(node.is_leaf):
			return node

		else:

			for i in range(len(node.keys)):
			
				#go in leftmost subtree
				if((i==0) and (val<=node.keys[i])):
					return self.get_start_node(val,node.ptrarr[0])
	
				#go in rightmost subtree
				if((i==(len(node.keys)-1)) and (val>node.keys[-1])):
					return self.get_start_node(val,node.ptrarr[i+1])
				
				#if val lies in between
				if(node.keys[i]<val<=node.keys[i+1]):
					return self.get_start_node(val,node.ptrarr[i+1])



	def countnodes(self,l,r,node):
		"""
		Counts no of values lying in given range in the given node
		"""
		
		retnode=None#return value of node
		ans=0#return value of count 

		if(len(node.keys)==0):
			return [ans,retnode]

		for i in range(len(node.keys)):
			if(l<=node.keys[i]<=r):
				ans+=1

		#check if we can move to next leaf node or not
		if(node.keys[len(node.keys)-1]<=r):
			retnode=node.next

		return [ans,retnode]



	def check_new_root(self,value):
		"""
		Check if after inserting, we require splitting of root or not 
		"""

		#flag non zero if new root
		flag,new_node=self.insert(value,self.root)
		if flag:
			self.root=self.initnewroot([self.root,new_node],[flag])



	def insert(self,value,node):
		"""
		Insert into node
		Returns value and node if node gets split
		Else returns none
		"""

		if(node.is_leaf):#case 1 for leaf node
			
			pos=self.findpos(node.keys,value)#find pos where to insert
			
			#insert pointer and value in appropriate position
			node.keys.insert(pos,value)
			node.ptrarr.insert(pos,value)

			#check if inserting causes splitting
			if(len(node.keys)>Node_Limit):
				return node.splitnode()
			else:
				return [None,None]

		else:#case 2 for non-leaf node
			
			#check which subtree to go
			for i in range(len(node.keys)):
				
				#case 1 if lies in leftmost subtree
				if((not i) and (value<node.keys[0])):
					midval,new=self.insert(value,node.ptrarr[0])
					break

				#case 2 if lies in rightmost subtree
				elif((i==(len(node.keys)-1)) and (value>=node.keys[i])):
					midval,new=self.insert(value,node.ptrarr[len(node.ptrarr)-1])
					break

				#case 3 if lies in between the node
				elif(value>=node.keys[i]) and (value<node.keys[i+1]):
					midval,new=self.insert(value,node.ptrarr[i+1])
					break

		# propagate splitting up the tree
		if midval:

			pos=self.findpos(node.keys,midval)#find pos to insert

			#insert pointer and value in appropriate position
			node.keys.insert(pos,midval)
			node.ptrarr.insert(pos+1,new)
			
			if len(node.keys)>Node_Limit:#if node split's further
				return node.splitnode()
			else:
				return [None,None]

		else:#if no splitting then return
			return [None,None]



	def findpos(self,arr,val):
		"""
		Returns pos where to insert in sorted order
		"""

		import bisect
		return bisect.bisect(arr,val)


	
	def initnewroot(self,arr1,arr2):
		"""
		Returns new root if root splits
		"""

		tnode=bptnode()
		tnode.ptrarr=arr1
		tnode.keys=arr2
		tnode.is_leaf=False
		return tnode



def processq(q):
    """
    Process queries
    """
    
    #set of queries
    q1,q2,q3,q4=["RANGE","INSERT","COUNT","FIND"]

    #convert numbers from string to int
    q[1]=int(q[1])

    if(q[0]==q1):
        print(bpt.rq(q[1],int(q[2])))

    elif(q[0]==q2):
        bpt.check_new_root(q[1])

    elif(q[0]==q3):
        print(bpt.rq(q[1],q[1]))
    
    elif(q[0]==q4):
        if(bpt.rq(q[1],q[1])>0):
            print("YES")
        else:
            print("NO")



if __name__=="__main__":
    """
    Runner function
    """

    #if arguments not entered correctly
    if(len(sys.argv)!=2):
        print("USAGE:- python3 q1.py input_file.txt")
        exit(0)

    #create bptree
    bpt=bptree()

    #initialise query list
    query=[]
    
    file=sys.argv[1]
    with open(file,'r') as f:
        for line in f:
            query.append(line.strip().split())

    #process each query
    for q in query:
        processq(q)