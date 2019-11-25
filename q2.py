import sys#for taking input
import math#for taking log

class LH:

    def __init__(self):
        """
        Initialise the linear hash data structure
        """

        self.hash=[[],[]]#hash table
        self.n=2#number of buckets
        self.i=1#number of bits to check
        self.limit=2#records in each bucket
        self.splitptr=0#which bucket to split

    def findlh(self,val):
        """
        Return true if val present in LH
        """

        bucket=self.findbucket(val)

        for i in self.hash[bucket]:
            if(i==val):
                return True

        return False

    def insertlh(self,val):
        """
        Insert into LH
        """

        #find pos to insert
        bucket=self.findbucket(val)

        #insert into LH
        self.hash[bucket].append(val)

        #if overflow then split
        if(len(self.hash[bucket])>self.limit):

            self.update()
            self.splitbucket(self.splitptr)
            self.splitptr+=1

        #update split ptr
        if(self.i==math.log(self.n,2)):
            self.splitptr=0

    def splitbucket(self,ptr):
        """
        Rearranges value in the bucket
        """

        temp=self.hash[ptr]
        self.hash[ptr]=[]
        for i in range(len(temp)):
            val=temp[i]
            bucket=val%(2**self.i)
            self.hash[bucket].append(val)

    def update(self):
        """
        Updates values after new bucket is added
        """
        
        self.hash.append([])
        self.n+=1
        self.i=math.log(self.n,2)
        self.i=math.ceil(self.i)

    def findbucket(self,val):
        """
        Returns bucket to insert/search
        """

        bucket=val%(2**self.i)
        #check if can fit into LH
        if(bucket>=self.n):
            bucket=bucket-(2**(self.i-1))

        return bucket


if __name__=="__main__":
    """
    Runner function
    """

    #if arguments not entered correctly
    if(len(sys.argv)!=2):
        print("USAGE:- python3 q2.py input_file.txt")
        exit(0)

    #create LH list
    lh=LH()

    #initialise query list
    query=[]
    
    file=sys.argv[1]
    with open(file,'r') as f:
        for line in f:
            query.append(int(line.strip()))

    #process each query
    for q in query:
        if not lh.findlh(q):
            print(q)
            lh.insertlh(q)

    # print(lh.hash)