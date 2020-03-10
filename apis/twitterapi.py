import requests
import json
from requests_oauthlib import OAuth1

auth_params = {
    'app_key': '15jOrY8IM2TPebrx5pQRK5GDy',
    'app_secret': '9DaDO8NeqfpaHBl7ALFe5kToNcXRgRd44BRkzPbeuvTie0HfFH',
    'oauth_token': '1174842082269323264-9ypP0ijl5busbynHVOcs7SE7pN7XHK',
    'oauth_token_secret': 'lzSoPUh8G3mZLTDiH0tbL4KMe32btHY6fEEaGF3rz55p9'
}

# Creating an OAuth Client connection
auth = OAuth1(
    auth_params['app_key'],
    auth_params['app_secret'],
    auth_params['oauth_token'],
    auth_params['oauth_token_secret']
)


def get_tweets(count):
    url_rest = "https://api.twitter.com/1.1/search/tweets.json"

    # getting rid of retweets and filtering
    q = '%23Music -filter:retweets -filter:replies'
    params = {'q': q, 'count': count, 'result_type': 'popular'}
    response = requests.get(url_rest, params=params, auth=auth)

    results = json.loads(response.text)
    return results


def get_retweets(id_str):
    url_rest = 'https://api.twitter.com/1.1/statuses/retweets/' + id_str + '.json'
    params = {'count': 100}
    response = requests.get(url_rest, params=params, auth=auth)

    results = json.loads(response.text)

    return results

def get_user_location(user_id_str):
    url_rest = 'https://api.twitter.com/1.1/users/lookup.json?user_id=' + user_id_str
    params = {}
    response = requests.get(url_rest, params = params, auth=auth)
    results = json.loads(response.text)
    return results
