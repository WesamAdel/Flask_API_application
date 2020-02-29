# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:33:54 2020

@author: waels
"""

def get_review_tones(review, tone_analyzer):
    tone_analysis = tone_analyzer.tone({'text': review},
                    content_type='application/json').get_result()
    return tone_analysis['document_tone']['tones']

def get_hotel_tones(hotel, df, tone_analyzer):
    hotel_reviews = df.loc[df['name'] == hotel]['reviews.text']
    tone_cnt_dict = {}
    tone_score_dict = {}

    for review in hotel_reviews:
        review_tones = get_review_tones(review, tone_analyzer)
        for tone in review_tones:
            tone_id = tone['tone_id']
            tone_score = tone['score']
            
            if tone_id in tone_cnt_dict:
                tone_cnt_dict[tone_id] += 1
                tone_score_dict[tone_id] += tone_score
            else:
                tone_cnt_dict[tone_id] = 1
                tone_score_dict[tone_id] = tone_score
        
    
    for tone_id in tone_cnt_dict.keys():
        tone_score_dict[tone_id] /= tone_cnt_dict[tone_id]
        
        
    return tone_score_dict
    



    