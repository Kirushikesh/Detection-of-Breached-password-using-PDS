import math
from fnvhash import fnv1a_32
from bitarray import bitarray

class BloomFilter():
    def __init__(self, n, fp_rate=None,m=None,n_hashfn=None):
        
        assert n!=None,"No of elements to enter in the filter should be known"
        self.n=n

        if(fp_rate):
            self.fp = fp_rate
        else:
            assert m and n_hashfn,'no of buckets and no of hash functions are required to find the fp_rate'
            self.fp=self.get_fp_prob(n,m,n_hashfn)
        
        if(m):
            self.m=m
        else:
            self.m = self.get_bucket_size(self.n, self.fp)

        if(n_hashfn):
            self.k=n_hashfn
        else:
            self.k = self.get_hash_count(self.n,self.m)

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
 
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
            self.bit_array[index] = True
 
    def check(self, item):
        for i in range(self.k):
            index = self.hash(item,i)
            if self.bit_array[index] == False:
                return False

        return True

    def required_memory(self):
        return self.m