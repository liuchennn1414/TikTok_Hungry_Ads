#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:35:33 2023

@author: zhangaijia
"""

class Moderator:
    def __init__(self, score, countries, productivity):
        self.score = score
        self.countries = countries
        self.productivity = productivity
        self.task_length= 0 


class Content:
    def __init__(self, score, country, complexity):
        self.score = score
        self.country = country
        self.complexity = complexity
        
        
good_moderators = #list of moderators with score in high range 
ok_moderators = #list of moderators with score in middle range
bad_moderators = #list of moderators with score in low range

high_contents = #list of contents with score in high range
middle_contents = #list of contents with score in middles range
low_contents = # list of contents with score in low range

def country_compatibility(c1, c2):
    '''
    Parameters
    ----------
    c1 : Short form of county 1.
    c2 : Short form of country 2.

    Returns score between 0 and 1
    '''

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
    
    # for example: complexity/productivity


def loss(moderator, content, w1, w2, w3):
    l1 = abs(moderator.score - content.score)
    l2 = max[country_compatibility(content.country, c2) for c2 in moderator.countries]
    l3 = country.score * moderator.task_length
    return w1*l1 + w2*l2 + w3*l3
    


def batch_graph(moderator_batch, content_batch):
    graph = [[loss(mj, ci, w1, w2, w3) for ci in content_batch] for mj in moderator_batch]
    
    return graph
    
    