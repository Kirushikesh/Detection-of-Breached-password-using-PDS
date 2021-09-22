import math
from fnvhash import fnv1a_32

class Bucket:
    def __init__(self):
        self.is_occupied=False
        self.is_continuation=False
        self.is_shifted=False

        self.fr=0
        self.empty=True

    def insert(self,fr):
        self.fr=fr
        self.empty=False

class QuotientFilter:
    def __init__(self,n,fp_rate=None,q=None,r=None):

        assert n!=None,"No of elements to enter in the filter should be known"
        self.n=n

        if(fp_rate):
            self.fp = fp_rate
        else:
            assert q and r,'quotient size and remainder size is required for calculating false positive rate'
            self.fp=self.get_fp_prob(n,q,r)

        if(q):
            self.q=q
        else:
            self.q=self.get_quotient_size(self.n)
        
        if(r):
            self.r=r
        else:
            self.r=self.get_remainder_size(self.n,self.q,self.fp)

        self.buckets=[Bucket() for _ in range(2**self.q)]

    def get_remainder_size(self,n,q,fp):
        return math.ceil(math.log2(-n/((2**q)*math.log(1-fp))))

    def get_quotient_size(self,n):
        return math.ceil(math.log2(n))
    
    def get_fp_prob(self,n,q,r):
        return n/(2**(q+r))

    def shift_right(self,k):
        prev=self.buckets[k]
        i=k+1

        while(True):
            if(self.buckets[i].empty):
                self.buckets[i].fr=prev.fr
                self.buckets[i].is_continuation=True
                self.buckets[i].is_shifted=True
                return 
            else:
                prev.fr,self.buckets[i].fr=self.buckets[i].fr,prev.fr
                prev.is_continuation,self.buckets[i].is_continuation=self.buckets[i].is_continuation,prev.is_continuation
                prev.is_shifted,self.buckets[i].is_shifted=self.buckets[i].is_shifted,prev.is_shifted

            i+=1

            if(i>=(2**self.q)):
                i=0
                
    def find_run_index(self,fq):
        j=fq
        while(self.buckets[j].is_shifted==True):
            j-=1
        
        rstart=j
        while(j!=fq):
            while(True):
                rstart+=1
                if(self.buckets[rstart].is_continuation==False):
                    break
            while(True):
                j+=1
                if(self.buckets[j].is_occupied==True):
                    break
        rend=rstart

        while(True):
            rend=(rend+1)%(2**self.q)
            if(self.buckets[rend].is_continuation==False):
                break

        return [rstart,rend]

    def hash(self,item):
        return fnv1a_32(item.encode()) % (2**(self.q+self.r))

    def get_qr(self,f):
        return (math.floor(f/(2**self.r)),math.floor(f%(2**self.r)))
        
    def add(self,item):

        f=self.hash(item)
        fq,fr=self.get_qr(f)

        if(self.buckets[fq].is_occupied==False and self.buckets[fq].empty):
            self.buckets[fq].insert(fr)
            self.buckets[fq].is_occupied=True
            return True

        self.buckets[fq].is_occupied=True
        rstart,rend=self.find_run_index(fq)

        if(rend>rstart):
            for i in range(rstart,rend):
                if(self.buckets[i].fr==fr):
                    return True

                elif(self.buckets[i].fr>fr):
                    self.shift_right(i)
                    self.buckets[i].insert(fr)
                    return True
        else:
            for i in range(rend,2**self.q):
                if(self.buckets[i].fr==fr):
                    return True

                elif(self.buckets[i].fr>fr):
                    self.shift_right(i)
                    self.buckets[i].insert(fr)
                    return True
            
            for i in range(0,rstart):
                if(self.buckets[i].fr==fr):
                    return True

                elif(self.buckets[i].fr>fr):
                    self.shift_right(i)
                    self.buckets[i].insert(fr)
                    return True
        
        self.shift_right(i)
        self.buckets[rend].insert(fr)
        return True

    def shift_left(self,k):
        i=k+1
        while(not self.buckets[i].empty):
            print(i,k)
            self.buckets[i-1].fr=self.buckets[i].fr
            self.buckets[i-1].is_continuation=self.buckets[i].is_continuation
            self.buckets[i-1].is_shifted=self.buckets[i].is_shifted
            self.buckets[i].empty=True

            self.buckets[i].is_shifted=False
            self.buckets[i].is_continuation=False
            i=i+1
            if(i>=2**(self.q)):
                i=0

    def remove(self,item):
        f=self.hash(item)
        fq,fr=self.get_qr(f)

        if(self.buckets[fq].is_occupied==False):
            return True
        
        rstart,rend=self.find_run_index(fq)
        if(rstart<rend):
            for i in range(rstart,rend):
                if(self.buckets[i].empty==False and self.buckets[i].fr==fr):
                    self.buckets[i].empty=True
                    if(rstart==rend-1):
                        self.buckets[i].is_occupied=False
                    elif(i<rend):
                        self.shift_left(i+1)
                    return True
        else:
            for i in range(rend,2**self.q):
                if(self.buckets[i].empty==False and self.buckets[i].fr==fr):
                    self.buckets[i].empty=True
                    if(rstart==rend-1):
                        self.buckets[i].is_occupied=False
                    elif(i<rend):
                        self.shift_left(i+1)
                    return True

            for i in range(0,rstart):
                if(self.buckets[i].empty==False and self.buckets[i].fr==fr):
                    self.buckets[i].empty=True
                    if(rstart==rend-1):
                        self.buckets[i].is_occupied=False
                    elif(i<rend):
                        self.shift_left(i+1)
                    return True

        return False

    def check(self,item):
        f=self.hash(item)
        fq,fr=self.get_qr(f)

        if(self.buckets[fq].is_occupied==False):
            return False
        else:
            rstart,rend=self.find_run_index(fq)
            
            for i in range(rstart,rend):
                if(self.buckets[i].empty==False and self.buckets[i].fr==fr):
                    return True

            return False

    def required_memory(self):
        return (self.q+self.r)*(2**self.q)

    def print_buckets(self):
        for i in range(2**self.q):
            print(i)
            print(self.buckets[i].is_occupied,self.buckets[i].is_continuation,self.buckets[i].is_shifted)
            print(self.buckets[i].empty,self.buckets[i].fr)
            print()