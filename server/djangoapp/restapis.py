import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if isinstance(json_result, list):
        for dealer_data in json_result:
            dealer_obj = CarDealer(
                address=dealer_data.get("address"),
                city=dealer_data.get("city"),
                full_name=dealer_data.get("full_name"),
                id=dealer_data.get("id")
            )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    
    if json_result and isinstance(json_result, dict):  # Check if json_result is a dictionary
        dealer_obj = CarDealer(
            address=json_result.get("address"),
            city=json_result.get("city"),
            full_name=json_result.get("full_name"),
            id=json_result.get("id")
        )
        return dealer_obj
    return None

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e0644675-9fce-4a74-aee4-2fc8f745c9ab"
    api_key = "ews5G2Jj09NPpW2jSZ6_pxcJqeJnvofrNhOzVJbJ07X1"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    
    
    if json_result and isinstance(json_result, list):
        reviews_data = json_result[0]  # Access the dictionary within the list
        review_obj = DealerReview(
            dealership=reviews_data.get("dealership"),
            name=reviews_data.get("name"),
            purchase=reviews_data.get("purchase"),
            review=reviews_data.get("review")
        )

        
        sentiment_result = analyze_review_sentiments(review_obj.review)
        review_obj.sentiment = sentiment_result
        results.append(review_obj)

    return results
    
           #sentiment = analyze_review_sentiments(review_obj.review)
           #print(sentiment)
           #review_obj.sentiment = sentiment
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


