#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 23:00:33 2023

@author: zhangaijia
"""

import numpy as np
import statistics
from scipy.optimize import linear_sum_assignment
import pandas as pd
import matching
import json

good_moderators_df = pd.read_csv("moderator_good.csv")
ok_moderators_df = pd.read_csv("moderator_ok.csv")
bad_moderators_df = pd.read_csv("moderator_bad.csv")



good_moderators = [matching.Moderator(good_moderators_df.loc[i, "id"],
                             good_moderators_df.loc[i, "score"],
                             json.loads(good_moderators_df.loc[i, "countries"].replace("'", '"')),
                             good_moderators_df.loc[i, "handling_time"])
                             for i in range(len(good_moderators_df))]

ok_moderators = 
bad_moderators = 

high_contents_df = pd.read_csv("ads_good.csv")
middle_contents_df = pd.read_csv("ads_ok.csv")
low_contents_df = pd.read_csv("ads_bad.csv")


high_contents = #list of contents with score in high range
middle_contents = #list of contents with score in middles range
low_contents = # list of contents with score in low range

similarity_dictionary = #dictionary assigning each country pair (c1, c2) to a similarity score





#Using good moderators and good contents as example:

w1 = #wwight 1
w2 = #weight 2
w3 = #weight 3

num_good = len(good_moderators)
    
while high_contents:
    batch_size = min(num_good, len(high_contents))
    content_batch, high_contents = high_contents[:batch_size], high_contents[batch_size:]
    matching(good_moderators, content_batch, w1, w2, w3)