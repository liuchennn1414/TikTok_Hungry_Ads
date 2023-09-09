#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 13:22:20 2023

@author: zhangaijia
"""

import numpy as np
import statistics
from scipy.optimize import linear_sum_assignment
import pandas as pd
import matching
import json
import random

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


    
merged_moderators = good_moderators + ok_moderators + bad_moderators
random.shuffle(merged_moderators)

merged_contents = high_contents + middle_contents + low_contents
random.shuffle(merged_contents)

num_mod = len(merged_moderators)-1

####################### RANDOM ASSIGNMETN #####################################

for content in merged_contents:
    random_mod = random.randint(0, num_mod)
    merged_moderators[random_mod].add_task(content)
    

random_assignment_results = {m.id:m.tasks_id for m in merged_moderators} #SAVE THIS DICTIONARY

count_comp = [[max([matching.country_compatibility(mc, c, similarity_dictionary) for mc in m.countries]) for c in m.task_countries] for m in merged_moderators]
avg_country_score = [np.mean(l) for l in count_comp] 

avg_score_diff = [np.mean(m.score_diff) for m in merged_moderators] 

task_lengths = [m.task_length for m in merged_moderators] 

max([m.task_length for m in merged_moderators])

moderator_ids = [m.id for m in merged_moderators]

random_results_df = pd.DataFrame(list(zip(moderator_ids, avg_score_diff, avg_country_score, task_lengths)),
               columns =['ID', 'Average_Score_Difference', 'Average_Country_Score', 'Total_Task_Lengths']) #SAVE THIS DATAFRAME


random_results_df.to_csv("performance_random.csv")
    