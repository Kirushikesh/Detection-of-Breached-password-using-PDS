from bloom_filter import BloomFilter
from counting_bloom_filter import CBloomFilter
from quotient_filter import QuotientFilter
from cuckoo_filter import CuckooFilter
 
n = 1000000
p = 0.001
 
word_present=[]
with open('1-million-password-list-top-1000000.txt','r') as f:
    for word in f.readlines():
        word_present.append(word[:-1])

#Bloom Filter
bfilter=BloomFilter(n,p)

print("Size of bitarray:{}".format(bfilter.m))
print("False positive Probability:{}".format(bfilter.fp))
print("No of hash functions:{}".format(bfilter.k))
 
for item in word_present:
    bfilter.add(item)

#Counting Bloom Filter
cbfilter=CBloomFilter(n,p,4)

print("Size of bitarray:{}".format(cbfilter.m))
print("False positive Probability:{}".format(cbfilter.fp))
print("No of hash functions:{}".format(cbfilter.k))
 
for item in word_present:
    cbfilter.add(item)
 
#Counting Bloom Filter
qfilter=QuotientFilter(n,p)

print("Size of quotient:{}".format(qfilter.q))
print("False positive Probability:{}".format(qfilter.fp))
print("Size of remainder:{}".format(qfilter.r))
 
for item in word_present:
    qfilter.add(item)

#Cuckoo Filter
cufilter=CuckooFilter(n,4,p)

print("Size of fingerprint:{}".format(cufilter.p))
print("False positive Probability:{}".format(cufilter.fp))
print("No of hash Buckets:{}".format(cufilter.m))
 
for item in word_present:
    cufilter.add(item)

choice='y'
while(choice=='y'):
    word=input()
    if bfilter.check(word):
        print("'{}' is probably present from bloom filter!".format(word))
    else:
        print("'{}' is definitely not present from bloom filter!".format(word))
    
    if cbfilter.check(word):
        print("'{}' is probably present from bloom filter!".format(word))
    else:
        print("'{}' is definitely not present from bloom filter!".format(word))
    
    if qfilter.check(word):
        print("'{}' is probably present from bloom filter!".format(word))
    else:
        print("'{}' is definitely not present from bloom filter!".format(word))
    
    if cufilter.check(word):
        print("'{}' is probably present from bloom filter!".format(word))
    else:
        print("'{}' is definitely not present from bloom filter!".format(word))