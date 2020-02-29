from elasticsearch import Elasticsearch 
import numpy as np
from review_analysis import *
from elasticsearch_dsl import Index

def create_es():
    es=Elasticsearch([{'host':'localhost','port':9200}])
    return es, 'hotel_index'

def create_doc(hotel_name, df, tone_analyzer):
    hotel_dict = {}
    hotel_df = df.loc[df['name'] == hotel_name]
    for column in hotel_df.columns:
        hotel_df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)

        val = np.unique(hotel_df[column].tolist())
        if len(val) == 1:
            dict_val = val.tolist()
        else:
            dict_val = hotel_df[column].tolist()
        hotel_dict[column] = dict_val
    hotel_dict['tones'] = get_hotel_tones(hotel_name, df, tone_analyzer)
    return hotel_dict
        

def index_hotels_es(df, es, index_name, tone_analyzer):
    for hotel_name in np.unique(df['name'].to_list()):
        print(hotel_name, ' 1')
        hotel_doc = create_doc(hotel_name, df, tone_analyzer)
        es.index(index=index_name, id=hotel_doc['name'][0], body=hotel_doc)
        print(hotel_name)

def get_hotel_es(hotel_name, es, index_name):
    return es.get(index=index_name, id=hotel_name)