# Breached Password Detection using Probabilistic Datastructures
## Table of Contents

- [Overview of Problem](#overview)
- [Motivation](#motivation)
- [Different Algorithms](#different-algorithms)
- [Usage](#usage)
- [Analysis of various algorithms](#analysis-of-various-algorithms)
- [Deployment](#deployment)
- [Tools and Technologies](#tools-and-technologies)
- [References](#references)
- [Future Work](#future-work)
- [Contact](#contact)

## Overview

**A Massive Resource for Cybercriminals Makes it Easy to Access Billions of Credentials.** While scanning the deep and dark web for stolen, leaked or lost data, 4iQ discovered a single file with a database of 1.4 billion clear text credentials the largest aggregate database found in the dark web to date. Now even unsophisticated and newbie hackers can access the largest trove ever of sensitive credentials in an underground community forum.

In the increasingly difficult times of protecting our own digital life or helping others protect theirs, we must be ever vigilant about ensuring that we have strong passwords. When building systems to manage passwords, there are common and time-tested algorithms for checking the strength of a password so you can warn users about weak ones and how they can make them stronger. Some properties of a strong password are not so straightforward to build a check for, or it is difficult to implement a check to run with real-time performance. In this post we present an approach that has performed well for detecting one aspect of a strong password — whether it has been breached or not.

![image](https://user-images.githubusercontent.com/49152921/134380402-c7f8d0a4-7924-425b-b0a8-6127f430500f.png)

NIST's Digital Identity Guidelines advises organisations to block subscribers from using passwords that have previously appeared in a data breach. Because this is a serious threat for a number of reasons:

1. It's enormously effective due to the password reuse problem.
2. It's hard for organisations to defend against because a successful "attack" is someone logging on with legitimate credentials.
3. It's very easily automatable; you simply need software which will reproduce the logon process against a target website.
4. There are readily available tools and credential lists that enable anyone to try their hand at credential stuffing.

## Motivation

Being such a large amount of data cannot be linearly scanned to find whether the password is breached or not. For small sets, it could be solved by direct lookup and subsequent comparison of the given element to each element in the set. However, such a naive approach depends on the number of elements in the set and takes on average O(log n) comparisons (on pre-sorted data), where n is the total number of elements. It is obvious that for huge sets of elements, which are operated by Big Data applications, this approach is not efficient and requires too much time and O(n) memory to store the elements.

Possible workaround solutions like chunking such sets and running comparisons in parallel can help in the reduction of computation time. However, it is not always applicable because for big data processing to store such huge sets of elements is almost an unachievable task. On the other hand, in many cases, it isn’t necessary to know exactly which element from the set has been matched, only that a match has been made and, therefore, it is possible to store only signatures of the elements rather than the whole value.

The problem of fast lookup can be solved using hashing, which is also the simplest way to do that. With a hash function, every element of the dataset can be hashed into a hash table that maintains a (sorted) list of hash values. However, such an approach yields a small probability of errors (caused by possible hash collisions) and requires about O(log n) bits per each hashed element. This this application we are going to look 4 different types of Probabilistic Data Structures which can be useful for the membership problem with a small amount on error.

## Different Algorithms
- [Bloom Filter](##bloom-filter)
- [Counting Bloom Filter](##counting-bloom-filter)
- [Quotient Filter](##quotient-filter)
- [Cuckoo Filter](##cuckoo-filter)

### Bloom Filter

The simplest and most well-known data structure that solves the membership problem is the Bloom filter which was proposed by Burton Howard Bloom in 1970. It is a space-efficient probabilistic data structure for representing a dataset D = {x1, x2, . . . , xn} of n elements that supports only two operations:
• Adding an element into the set, and
• Testing whether an element is or is not a member of the set.

Practically, the Bloom filter is represented by a bit array and can be described by its length **m** and number of different hash functions **hi**(i=1 to k). Hash functions hi should be independent and uniformly distributed so that the probability of collisions is less. In this application we are going to use two types of non-cryptographic hash functions because non-cryptographic hash functions are faster than cryptographic hash functions and since cryptographic hash functions require a lot of criteria to satify for ex: preimage resistance for the security, non-cryptographic hash functions require only criterion of guaranting low probablity of collisions. We use two famous algorithms FNV and MurMurHash functions of 32bit version. 

The BloomFilter data structure is a bit array of length m where at the beginning all bits are equal to zero, meaning the filter is empty. To insert an element x into the filter, for every hash function hk we compute its value j = hk (x ) on the element x and set the corresponding bit j in the filter to one. Note, it is possible that some bits can be set multiple times due to hash collisions. Each hashfunctions use same FNV Hash function with different seed each time. 

When we need to test if the given element x is in the filter, we compute all k hash functions hi ={hi(x)}(i=1 to k) and check bits in the corresponding positions. If all bits are set to one, then the element x may exist in the filter. Otherwise, the element x is definitely not in the filter.

**Properties**
False Positives are possible and occur because of hash collisions because in the test operationthere is no prior knowledge of whether the particular bit has been set by the same hash function as the one we compare with. The false positive rate can be estimated by

![image](https://user-images.githubusercontent.com/49152921/134318992-7c5f99a2-0931-4be0-853d-81a3134bfbc6.png)

In practice, the length of the filter m, under given false positive probability P<sub>fp</sub> and the expected number of elements n, can be determined by

![image](https://user-images.githubusercontent.com/49152921/134319021-58001183-da3c-4f31-b39b-7d0f6a595db1.png)

The optimal value of number of hash functions k can be found using 

![image](https://user-images.githubusercontent.com/49152921/134319066-f344dd42-c9ac-4496-a798-b0a2561d8c81.png)

With the increase of number of hash functions k and the ratio of m/n the false positive probability decreases

![image](https://user-images.githubusercontent.com/49152921/134316817-23a48a41-a7a0-4acf-8ee6-d6fb0d988201.png)

With the constant number of entries in the bloom filter n when the false positive rates reduces to result a higher number of hash functions,

![image](https://user-images.githubusercontent.com/49152921/134317951-8354a6f6-1cc7-4a26-a8fd-a49c394ae381.png)

With the constant number of entries n=20 when the false probability rate reduces the bucket size m or the size of the filter increases.

![image](https://user-images.githubusercontent.com/49152921/134318364-8459c5c4-6cb3-4c69-ae07-cbbfd4ca0030.png)

### Counting Bloom Filter

Unfortunately the classical bloom filter does not support deletion which leads us to use counting bloom filter which uses the counters instead of bits. Building on
the classical Bloom filter algorithm, it introduces an array of m counters Cj(j=1 to m) corresponding to each bit in the filter’s array. 
The Counting Bloom filter allows approximating the number of times each element has been seen in the filter by incrementing the corresponding counter every time the element is added. The associated CountingBloomFilter data structure contains a bit array and the array of counters of length m, all initialized to zeros.

Checking for a element is similar to the classical bloom filter if the counter at all the hash indices are greater than zero then the element is probably present.

The deletion is quite similar to the insertion but in reverse. To delete an element x , we compute all k hash values hi = {hi(x)}(i=1 to k) and decrease the corresponding counters. If the counter changes its value from one to zero, the corresponding bit in the bit-array has to be unset. Each of the counter is a fixed size of nb bits where the maximum value of the counter is N=2<sup>nb</sup>. There is very little probability of the counter could overflow given by

![image](https://user-images.githubusercontent.com/49152921/134319222-bbcad865-7297-4704-a3e3-a79c5944d4d4.png)

Counting Bloom filter inherits all the properties and the recomendations of optimal choice of parameters from the bloom filter. With constant number of entries and the constant counter size on decrease in the false positive rate the size of the counting bloom filter increases since we are using counters instead of bits the size will be greater than the classical bloom filter.

![image](https://user-images.githubusercontent.com/49152921/134319728-fbde757d-6e30-4521-8eb8-d58a131cb886.png)

### Quotient Filter
![image](https://user-images.githubusercontent.com/49152921/134323079-14ac4695-d1e9-4122-83e0-e3979cd9bd2a.png)
![image](https://user-images.githubusercontent.com/49152921/134323175-0c1b7366-bc81-453f-ae91-014cced0f0ce.png)
![image](https://user-images.githubusercontent.com/49152921/134323231-b5c66768-dd9a-4749-a341-022e79482a40.png)
![image](https://user-images.githubusercontent.com/49152921/134323313-07b413c2-da83-4fbb-ac01-5f115ee34e8a.png)

![image](https://user-images.githubusercontent.com/49152921/134310615-00e3682e-c811-4d47-a42a-412cf2f696fe.png)
![image](https://user-images.githubusercontent.com/49152921/134321963-e0d221e5-288f-4daa-9c11-6aa949fce8ec.png)
![image](https://user-images.githubusercontent.com/49152921/134324874-8bdbd237-536e-48fc-b550-147e822a6af2.png)

# CuckooFilter
![image](https://user-images.githubusercontent.com/49152921/134324969-ec01a7b1-b47d-4aba-9dea-07e9c0160f06.png)
![image](https://user-images.githubusercontent.com/49152921/134325007-4b4fdd67-175a-4089-bda6-fe3a875c3ba1.png)
![image](https://user-images.githubusercontent.com/49152921/134325083-14977b34-3c12-4d8a-adda-228b523f01fe.png)
![image](https://user-images.githubusercontent.com/49152921/134325124-a648d877-8485-4834-9f18-51fbc4a3405c.png)
![image](https://user-images.githubusercontent.com/49152921/134325149-23177574-4601-40c1-9ce9-c3ca892fb1cb.png)


![image](https://user-images.githubusercontent.com/49152921/134343051-673c7b12-72a4-4d52-a934-7998c1b49490.png)
![image](https://user-images.githubusercontent.com/49152921/134343803-9daff8c7-d67e-4efc-a583-a7d32588e468.png)
![image](https://user-images.githubusercontent.com/49152921/134311376-3293c8c9-11c3-426f-95cb-e5b93613efd4.png)

# References
https://github.com/prriyanayak/Advanced-Algorithm-Project

https://dzone.com/articles/introduction-probabilistic-0#:~:text=Probabilistic%20data%20structures%20have%20many,commonly%20used%20probabilistic%20data%20structures.

https://www.kdnuggets.com/2019/08/count-big-data-probabilistic-data-structures-algorithms.html

https://github.com/gakhov/pdsa

https://www.threatstack.com/blog/optimizing-detection-of-breached-passwords

https://haveibeenpwned.com/Passwords#:~:text=Pwned%20Passwords%20are%20613%2C584%2C246%20real,to%20take%20over%20other%20accounts.

https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/

https://github.com/vedantk/quotient-filter

https://github.com/michael-the1/python-cuckoo

https://medium.com/4iqdelvedeep/1-4-billion-clear-text-credentials-discovered-in-a-single-database-3131d0a1ae14

# Heroku 

https://breached-password-detection.herokuapp.com/

![image](https://user-images.githubusercontent.com/49152921/134309723-d44ee54d-f5c7-408a-b203-ee49befbc755.png)
![image](https://user-images.githubusercontent.com/49152921/134310165-cf3667bf-34c3-45eb-b032-0b58a3573f09.png)
