#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:35:33 2023

@author: zhangaijia
"""

import numpy as np
import statistics
from scipy.optimize import linear_sum_assignment



class Moderator:
    def __init__(self, id, score, countries, handling_time):
        self.score = score
        self.countries = countries
        self.handling_time = handling_time
        self.id = id
        
        self.tasks_id = []
        self.task_length= 0 
        self.score_diff = []
        self.task_countries= []
        
        
    def add_task(self, content):
        self.tasks_id.append(content.id)
        self.task_length += self.handling_time * content.complexity
        self.score_diff.append(abs(self.score - content.score))
        self.task_countries.append(content.country)


class Content:
    def __init__(self, id, score, country, complexity):
        self.score = score
        self.country = country
        self.complexity = complexity
        self.id = id
        

def country_compatibility(c1, c2, sim_d):
    '''
    Parameters
    ----------
    c1 : Short form of county 1.
    c2 : Short form of country 2.

    Returns score between 0 and 1
    '''
    if c1 == '' or c2 == '':
        return 0
    elif c1 == 'OTHER' or c2 == 'OTHER':
        return 0.1
    elif (c1, c2) in sim_d:
        return sim_d[(c1, c2)]
    else:
        return sim_d[(c2, c1)]

def time_for_task(moderator, content):
    '''

    Parameters
    ----------
    moderator : Moderator of interest
    content : Content of interest
    
    A function involving content.complexity and moderator.productivity

    Returns
    Estimated time in (units?)

    '''
    
    return moderator.handling_time * content.complexity



def create_graph(moderator_batch, content_batch, w1, w2, w3, sim_d):
    
    # --- Sub-functions within create_graph ---

    def compute_mean_std():
        l1_values = []
        l3_values = []
        l2_values = []

        for mj in moderator_batch:
            for ci in content_batch:
                l1_values.append(abs(mj.score - ci.score))
                l2_values.append(max([country_compatibility(ci.country, c2, sim_d) for c2 in mj.countries]))
                l3_values.append(time_for_task(mj, ci) + mj.task_length)

        return statistics.mean(l1_values), statistics.stdev(l1_values), statistics.mean(l2_values), statistics.stdev(l2_values), statistics.mean(l3_values), statistics.stdev(l3_values)

    def normalized_loss(moderator, content, l1_mean, l1_std, l2_mean, l2_std, l3_mean, l3_std):
        l1 = abs(moderator.score - content.score)
        l2 = max([country_compatibility(content.country, c2, sim_d) for c2 in moderator.countries])
        l3 = time_for_task(moderator, content) + moderator.task_length

        # Normalize l1 and l3 to N(0,1)
        l1_normalized = (l1 - l1_mean) / l1_std
        l2_normalized = (l2 - l2_mean) / l2_std
        l3_normalized = (l3 - l3_mean) / l3_std

        return w1*l1_normalized + w2*l2_normalized + w3*l3_normalized

    # --- Main functionality of create_graph ---
    
    l1_mean, l1_std, l2_mean, l2_std, l3_mean, l3_std = compute_mean_std()
    graph = [[normalized_loss(mj, ci, l1_mean, l1_std, l2_mean, l2_std, l3_mean, l3_std) for mj in moderator_batch] for ci in content_batch]
    return graph



def add_dummy_content(content_batch, num_required):
    """Add dummy content nodes to content_batch."""
    dummy_content = Content(score=0, country='', complexity=0, id='dummy')
    for _ in range(num_required):
        content_batch.append(dummy_content)
    return content_batch



def matching(moderator_batch, content_batch, w1, w2, w3, sim_d):
    
    num_moderators = len(moderator_batch)
    num_contents = len(content_batch)
    
    # Add dummy content nodes if needed
    if num_contents < num_moderators:
        content_batch = add_dummy_content(content_batch, num_moderators - num_contents)
    
    graph = create_graph(moderator_batch, content_batch, w1, w2, w3, sim_d)
    
    c_indices, m_indices = linear_sum_assignment(graph)
    
    for c, m in zip(c_indices, m_indices):
        # Avoid adding dummy content to a moderator's tasks
        if content_batch[c].id != 'dummy':
            moderator_batch[m].add_task(content_batch[c])




    


    
