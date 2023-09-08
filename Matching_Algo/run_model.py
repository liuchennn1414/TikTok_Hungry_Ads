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

ok_moderators = [matching.Moderator(ok_moderators_df.loc[i, "id"],
                             ok_moderators_df.loc[i, "score"],
                             json.loads(ok_moderators_df.loc[i, "countries"].replace("'", '"')),
                             ok_moderators_df.loc[i, "handling_time"])
                 for i in range(len(ok_moderators_df))]
bad_moderators = [matching.Moderator(bad_moderators_df.loc[i, "id"],
                             bad_moderators_df.loc[i, "score"],
                             json.loads(bad_moderators_df.loc[i, "countries"].replace("'", '"')),
                             bad_moderators_df.loc[i, "handling_time"])
                  for i in range(len(bad_moderators_df))]

high_contents_df = pd.read_csv("ads_good.csv")
middle_contents_df = pd.read_csv("ads_ok.csv")
low_contents_df = pd.read_csv("ads_bad.csv")


high_contents = [matching.Content(high_contents_df.loc[i, "id"], 
                                  high_contents_df.loc[i, "score"], 
                                  high_contents_df.loc[i, "country"], 
                                  high_contents_df.loc[i, "complexity"])
                 for i in range(len(high_contents_df))]
middle_contents = [matching.Content(middle_contents_df.loc[i, "id"], 
                                  middle_contents_df.loc[i, "score"], 
                                  middle_contents_df.loc[i, "country"], 
                                  middle_contents_df.loc[i, "complexity"])
                 for i in range(len(middle_contents_df))]
low_contents = [matching.Content(low_contents_df.loc[i, "id"], 
                                  low_contents_df.loc[i, "score"], 
                                  low_contents_df.loc[i, "country"], 
                                  low_contents_df.loc[i, "complexity"])
                 for i in range(len(low_contents_df))]




similarity_df = pd.read_csv("similarity_matrix.csv")
similarity_dictionary = {(similarity_df.loc[i, "code1"], similarity_df.loc[i, "code2"]): 
                         similarity_df.loc[i, "Decision"] for i in range(len(similarity_df))}




#Using good moderators and good contents as example:

w1 = #wwight 1
w2 = #weight 2
w3 = #weight 3

num_good = len(good_moderators)
    
while high_contents:
    batch_size = min(num_good, len(high_contents))
    content_batch, high_contents = high_contents[:batch_size], high_contents[batch_size:]
    matching(good_moderators, content_batch, w1, w2, w3)
