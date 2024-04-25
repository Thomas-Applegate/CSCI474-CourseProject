#!/usr/bin/env python
# coding: utf-8

# In[12]:


import nistrng as nst
from nistrng.sp800_22r1a import *
from nistrng import Test, Result
import random
import numpy as np
import pandas as pd
from Crypto.Hash import SHA256


# In[2]:


SP800_22R1A_BATTERY: dict = {
                                "monobit": MonobitTest(),
                                "frequency_within_block": FrequencyWithinBlockTest(),
                                "runs": RunsTest(),
                                "longest_run_ones_in_a_block": LongestRunOnesInABlockTest(),
                                "binary_matrix_rank": BinaryMatrixRankTest(),
                                "dft": DiscreteFourierTransformTest(),
                                "non_overlapping_template_matching": NonOverlappingTemplateMatchingTest(),
                                "overlapping_template_matching": OverlappingTemplateMatchingTest(),
                                "maurers_universal": MaurersUniversalTest(),
                                "linear_complexity": LinearComplexityTest(),
                                "serial": SerialTest(),
                                "approximate_entropy": ApproximateEntropyTest(),
                                "cumulative sums": CumulativeSumsTest(),
                                "random_excursion": RandomExcursionTest(),
                                "random_excursion_variant": RandomExcursionVariantTest()
                            }


# In[3]:


#given a list of strings that represent random hex values, return an array of array's of the bits for each hex value
def true_rand_bin(hex):
    bin = []
    inputs = []
    for h in hex:
        b = "{0:08b}".format(int(h, 16))
        bin.append(b)
        temp = []
        for i in b:
            temp.append(int(i))
        inputs.append(np.array(temp))
    return inputs


# In[4]:


#generate a list of three pseudo-random binary numbers in the correct format for the tests
def pseduo_rand_bin():
    random.seed(10)
    inputs = []
    for i in range(3):
        temp = []
        for j in range(256):
            bin = random.randint(0, 1)
            temp.append(bin)
        inputs.append(np.array(temp))
    return inputs


# In[19]:


#generate a list of three deskewed random numbers and returns a list of inputs in the correct form
def deskewed_rand_bin(hex):
    inputs = []
    for h in hex:
        hash_func = SHA256.new()
        byte = bytes.fromhex(h)
        hash_func.update(byte)
        bin_num = "{0:0256b}".format(int(hash_func.hexdigest(), 16))
        temp = []
        for i in bin_num:
            temp.append(int(i))
        inputs.append(np.array(temp))
    return inputs


# In[6]:


#inputs is a list of numpy array binary numbers and it will run all eligible
# tests. It returns a list of lists. The internal lists contains tuples of
# the format (test name, pass/fail, score, time_elapsed)
def run_tests(inputs):
    scores = []
    for num in inputs:
        eligible_battery: dict = nst.check_eligibility_all_battery(num, SP800_22R1A_BATTERY)
        results = nst.run_all_battery(num, eligible_battery, False)
        ind_res = []
        for result, elasped_time in results:
            if result.passed:
                new_row = (result.name, "Passed", result.score, elasped_time)
                ind_res.append(new_row)
            else: 
                new_row = (result.name, "Passed", result.score, elasped_time)
                ind_res.append(new_row)
        scores.append(ind_res)
    return scores


# In[7]:


#I generated these from random.org
hex_true_rand = ["e3bf00dc0aad2d180da829e5c620c6046fd726e36a1b2336e1067598ba307549", "f82897fe6abf801a7354271dc31e0b88e4f5da26bd4d64ac5076de173946a95c", "d3587c8bebd2b4e89626b4eca0d4b044256e4691610a6eb93aec7115249c58b5"]
true_rand = true_rand_bin(hex_true_rand)
tr_results = run_tests(true_rand)


# In[10]:


pseudo_rand = pseduo_rand_bin()
pr_results = run_tests(pseudo_rand)


# In[20]:


#I generated these numbers from codebeautify.org
hex_deskew_rand = ["8a72b640e033294f70d491e6f2786620e69b4720f7777815002874627aca1e65", "d15751fef5f775306106fd29cd44fd5a549d40dcfea7f5af834c8d70ed094b88", "85f64b25b03612d544b2bb7bfa175afbab6c18c8beed35e6e22f841bbe31dbee"]
deskew_rand = deskewed_rand_bin(hex_deskew_rand)
dr_results = run_tests(deskew_rand)

