import math
from fnvhash import fnv1a_32
from bitarray import bitarray
from bitarray.util import ba2int,int2ba

class CBloomFilter():
    def __init__(self, n, fp_rate=None,Counter_size=None,bucket_size=None,no_hashfn=None):
        
        assert n!=None and Counter_size!=None,"No of elements and countersize should be known"
        self.n=n
        self.N=Counter_size

        if(fp_rate):
            self.fp = fp_rate
        else:
            assert bucket_size and no_hashfn,'no of buckets and no of hash functions are required to find the fp_rate'
            self.fp=self.get_fp_prob(n,bucket_size,no_hashfn)
        
        if(bucket_size):
            self.m=bucket_size
        else:
            self.m = self.get_bucket_size(self.n, self.fp)

        if(no_hashfn):
            self.k=no_hashfn
        else:
            self.k = self.get_hash_count(self.n,self.m)

        self.bit_array = []
        for i in range(self.m):
            count=bitarray(self.N)
            count.setall(0)
            self.bit_array.append(count)
    
    def get_overflow_prob(self):
        max_val=2**(self.N)
        return self.m*(((math.e*math.log(2))/max_val)**max_val)

    def get_bucket_size(self, n, fp):
        m = -(n * math.log(fp))/(math.log(2)**2)
        return int(m)
 
    def get_hash_count(self, n, m):
        k = (m/n) * math.log(2)
        return int(k)
    
    def get_fp_prob(self,n,m,k):
        return (1-math.exp(-k*n/m))**k

    def hash(self,item,seed):
        return fnv1a_32(item.encode(),seed) % self.m

    def add(self, item):

        for i in range(self.k):
            index = self.hash(item,i)

            cur_val=ba2int(self.bit_array[index])
            new_array=int2ba(cur_val+1,length=self.N)
            
            self.bit_array[index]=new_array
 
    def check(self, item):
        for i in range(self.k):
            index = self.hash(item,i)
            cur_val=ba2int(self.bit_array[index])

            if(not cur_val>0):
                return False
        return True
 
    def remove(self,item):
        if(self.check(item)):
            for i in range(self.k):
                index = self.hash(item,i)
                
                cur_val=ba2int(self.bit_array[index])
                new_array=int2ba(cur_val-1,length=self.N)
                self.bit_array[index]=new_array

            print('Element Removed')
        else:
            print('Element is probably not exist')

    def required_memory(self):
        return self.N*self.m