This is a htoel review dataset where each row represents a review for a hotel, hotel branch to be more specific. We use hotel name as id
for query simplicity instead of using hotel address/ location.

To run: run mani.py

Hotel Review Tone Analyzer:
	- api: tone. accepts hotel name as input and returns score for each tone.
	- the api calls get_hotel_tones to get tones of hotel reviews. which get tones of each review
	  seprately then aggregate tones from all reviews.
	  - We use only document tones instead of sentences tones for simplicity.

Hotel Indexer:
	- Indexer api: index_hotels, calls index_hotels_es to create a document for each hotel and add it to elasticsearch index.
	  We use hotel name as id. For the other entries, if it's not the same for all reviews we use it as a list with same length as 
          the number of reviews for this hotel, so each entry entry will be of length either 1 or number of reviews.
	  - doc retrieval api: get_hotel. retrieves hotel doc from elasticsearch given hotel name.

Note:
	IBM-Watson tone analyzer takes a while for each review, so hotel indexer will take some time if we add review tones 
	to the doc. To disable adding tone to doc comment this line in create_doc function:
	hotel_dict['tones'] = get_hotel_tones(hotel_name, df, tone_analyzer).

