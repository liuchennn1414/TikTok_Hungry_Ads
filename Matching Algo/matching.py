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
    def __init__(self, score, countries, productivity, id, handling_time):
        self.score = score
        self.countries = countries
        self.tasks = []
        self.task_length= 0 
        self.handling_time = handling_time
        self.id = id
        
        
    def add_task(self, content):
        self.tasks.append(content)
        self.task_length += self.handling_time * content.complexity


class Content:
    def __init__(self, score, country, complexity, id):
        self.score = score
        self.country = country
        self.complexity = complexity
        self.id = id
        
        
good_moderators = #list of moderators with score in high range 
ok_moderators = #list of moderators with score in middle range
bad_moderators = #list of moderators with score in low range



high_contents = #list of contents with score in high range
middle_contents = #list of contents with score in middles range
low_contents = # list of contents with score in low range

similarity_dictionary = #dictionary assigning each country pair (c1, c2) to a similarity score

def country_compatibility(c1, c2):
    '''
    Parameters
    ----------
    c1 : Short form of county 1.
    c2 : Short form of country 2.

    Returns score between 0 and 1
    '''
    if c1 == '' or c2 == '':
        return 1
    else:
        return similarity_dictionary['({c1}, {c2})'.format(c1, c2)]

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



def create_graph(moderator_batch, content_batch, w1, w2, w3):
    
    # --- Sub-functions within create_graph ---

    def compute_mean_std_l1_l3():
        l1_values = []
        l3_values = []

        for mj in moderator_batch:
            for ci in content_batch:
                l1_values.append(abs(mj.score - ci.score))
                l3_values.append(time_for_task(mj, ci) + mj.task_length)

        return statistics.mean(l1_values), statistics.stdev(l1_values), statistics.mean(l3_values), statistics.stdev(l3_values)

    def normalized_loss(moderator, content, l1_mean, l1_std, l3_mean, l3_std):
        l1 = abs(moderator.score - content.score)
        l2 = max([country_compatibility(content.country, c2) for c2 in moderator.countries])
        l3 = time_for_task(moderator, content) + moderator.task_length

        # Normalize l1 and l3 to N(0,1)
        l1_normalized = (l1 - l1_mean) / l1_std
        l3_normalized = (l3 - l3_mean) / l3_std

        return w1*l1_normalized + w2*l2 + w3*l3_normalized

    # --- Main functionality of create_graph ---
    
    l1_mean, l1_std, l3_mean, l3_std = compute_mean_std_l1_l3()
    graph = [[normalized_loss(mj, ci, l1_mean, l1_std, l3_mean, l3_std) for mj in moderator_batch] for mj in content_batch]
    return graph



def add_dummy_content(content_batch, num_required):
    """Add dummy content nodes to content_batch."""
    dummy_content = Content(score=0, country='', complexity=0, id='dummy')
    for _ in range(num_required):
        content_batch.append(dummy_content)
    return content_batch



def matching(moderator_batch, content_batch, w1, w2, w3):
    
    num_moderators = len(moderator_batch)
    num_contents = len(content_batch)
    
    # Add dummy content nodes if needed
    if num_contents < num_moderators:
        content_batch = add_dummy_content(content_batch, num_moderators - num_contents)
    
    graph = create_graph(moderator_batch, content_batch, w1, w2, w3)
    
    c_indices, m_indices = linear_sum_assignment(graph)
    
    for c, m in zip(c_indices, m_indices):
        # Avoid adding dummy content to a moderator's tasks
        if content_batch[c].id != 'dummy':
            moderator_batch[m].add_task(content_batch[c])


    

#Using good moderators and good contents as example:

w1 = #wwight 1
w2 = #weight 2
w3 = #weight 3

num_good = len(good_moderators)
    
while high_contents:
    batch_size = min(num_good, len(high_contents))
    content_batch, high_contents = high_contents[:batch_size], high_contents[batch_size:]
    matching(good_moderators, content_batch, w1, w2, w3)

    
