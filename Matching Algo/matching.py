#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:35:33 2023

@author: zhangaijia
"""

class Moderator:
    def __init__(self, score, vector, productivity):
        self.score = score
        self.vector = vector
        self.productivity = productivity
        self.time_left = 0 # if 0 then not matched, if > 0 then currently working
        self.working_contents = []


class Content:
    def __init__(self, score, vector, complexity):
        self.score = score
        self.vector = vector
        self.complexity = complexity
        self.matched = False
        
        
moderators = #initiate list of moderators
contents = #initiate priority queue of contents
contents_to_match = #list of size M of current first M contents to moderate


def weight(Moderator, Content):
    
    '''
    calculate weight of edges between each available moderator and content, based on score, compatibility, time efficiency
    '''
    
def select_moderators(moderators, k, epsilon):
    '''
    select k moderators with least time_left, and time_left below treshold, and no working contents
    '''
    
def matching(moderator_list, content_list):
    '''
    genetic algorithm to maximise weight/minimize loss for current batch of matching
    '''
    
'''
Algorithm steps:
Assume discrete time step t = 1, 2, ... ...
    
    1) Initiate moderator list, content queue, and content list of first M content, record weight/loss
    2) Initiate matching between moderator list and content list
    3) At each time step, select k moderators with empty working_content list and next M contents to match (k < M)
    4) Perform matching with genetic algorithm
    5) pop the matched contents from the list
    6) Record the time taken for last moderator to evaluate last content