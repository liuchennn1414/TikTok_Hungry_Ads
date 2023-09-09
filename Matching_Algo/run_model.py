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




################################## RUNNING THE MODEL ###############################################

w1 = 0.3
w2 = -0.3
w3 = 0.4


moderators = good_moderators[:] #CHANGE ACCORDINGLY
contents = high_contents[:] #CHANGE ACCORDINGLY
num_mod = len(moderators)

while contents:
    batch_size = min(num_mod, len(contents))
    content_batch, contents = contents[:batch_size], contents[batch_size:]
    matching.matching(moderators, content_batch, w1, w2, w3, similarity_dictionary)
    

#''' Getting results data

assignment_results = {m.id:m.tasks_id for m in moderators} #SAVE THIS DICTIONARY

count_comp = [[max([matching.country_compatibility(mc, c, similarity_dictionary) for mc in m.countries]) for c in m.task_countries] for m in moderators]
avg_country_score = [np.mean(l) for l in count_comp] 

avg_score_diff = [np.mean(m.score_diff) for m in moderators] 

task_lengths = [m.task_length for m in moderators] 

max([m.task_length for m in moderators])

moderator_ids = [m.id for m in moderators]

results_df = pd.DataFrame(list(zip(moderator_ids, avg_score_diff, avg_country_score, task_lengths)),
               columns =['ID', 'Average_Score_Difference', 'Average_Country_Score', 'Total_Task_Lengths']) #SAVE THIS DATAFRAME
#'''