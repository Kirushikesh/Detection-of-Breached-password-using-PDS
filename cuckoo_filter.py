import math
from fnvhash import fnv1a_32
import mmh3
import random

class Bucket():
    def __init__(self,bucket_size):
        self.size=bucket_size
        self.b=[]

    def is_full(self):
        return len(self.b) >= self.size

    def add(self,fingerprint):
        if(not self.is_full()):
            self.b.append(fingerprint)
            return True
        return False
    
    def contains(self,fingerprint):
        return fingerprint in self.b
    
    def remove(self,fingerprint):
        if(self.contains(fingerprint)):
            self.b.remove(fingerprint)
            return True
        return False
    
    def swap_fingerprint(self,new_fingerprint):
        index=random.choice(range(self.size))
        fingerprint,self.b[index]=self.b[index],new_fingerprint

        return fingerprint

class CuckooFilter():
    def __init__(self,n,bucket_size=4,fp_rate=None,max_kicks=500,p=None,m=None):

        assert n!=None,"No of elements should not be None"
        self.n=n
        self.nb=bucket_size
        self.maxiter=max_kicks

        if(fp_rate):
            self.fp=fp_rate
        else:
            assert p!=None,'fingerprint size should be given in advance'
            self.fp=self.get_fp_prob(self.n,p)
        
        if(p):
            self.p=p
        else:
            self.p=self.get_p_value(self.nb,self.fp)
        
        if(m):
            self.m=m
        else:
            self.m=self.get_nobucket(self.n,self.nb)
    
        self.buckets=[Bucket(self.nb) for _ in range(self.m)]

    def get_p_value(self,b,fp):
        return math.ceil(math.log(2*b/fp))
    
    def get_nobucket(self,n,b):
        return math.ceil(n/b)+1
    
    def get_fp_prob(self,b,p):
        return (2*b)/(2**p)

    def hash(self,item):
        return fnv1a_32(item.encode()) % (2**self.p)

    def get_indices(self,item,fingerprint):
        return [mmh3.hash(item)% self.m,((mmh3.hash(item)% self.m)^(mmh3.hash(str(fingerprint))%self.m)) % self.m]

    def add(self,item):
        fingerprint=self.hash(item)

        i,j=self.get_indices(item,fingerprint)

        if self.buckets[i].add(fingerprint):
            return True
        elif self.buckets[j].add(fingerprint):
            return True

        k = random.choice((i,j))
        for n in range(self.maxiter):
            fingerprint = self.buckets[k].swap_fingerprint(fingerprint)
            k = (k ^ mmh3.hash(str(fingerprint))) % self.m
            if self.buckets[k].add(fingerprint):
                return True

        return False

    def check(self,item):
        fingerprint=self.hash(item)
        i,j=self.get_indices(item,fingerprint)

        return self.buckets[i].contains(fingerprint) or self.buckets[j].contains(fingerprint)
    
    def remove(self,item):
        fingerprint=self.hash(item)
        i,j=self.get_indices(item,fingerprint)

        if(self.buckets[i].remove(fingerprint) or self.buckets[j].remove(fingerprint)):
            return True
        return False

    
