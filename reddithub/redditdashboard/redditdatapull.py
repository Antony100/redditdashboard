import requests

class DataPull():

    def __init__(self, client_id, client_secret,
                 user_agent, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password
        self.token = self.login()
        self.headers = {
            "Authorization": f"bearer {self.token['access_token']}",
            "User-Agent": self.user_agent
        }

    def login(self):
        headers = {"User-Agent": self.user_agent}
        client_auth = requests.auth.HTTPBasicAuth(
            self.client_id, self.client_secret
        )

        post_data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=client_auth,
            data=post_data,
            headers=headers
        )
        return response.json()

    def get_articles(self, subreddit, n_pages=1):
        stories = []
        after = None
        for page_number in range(n_pages):

            url = "https://oauth.reddit.com/r/{}?limit=5".format(subreddit)

            if after:
                url += "&after={}".format(after)
            response = requests.get(url, headers=self.headers)
            result = response.json()
            after = result['data']['after']
            stories.extend(
                [
                    (story['data']['title'], story['data']['url'],
                        story['data']['score'])
                    for story in result['data']['children']
                    if story['data']['stickied'] is False
                ]
            )

        return self.article_results_dict(stories)

    def get_image(self, subreddit, n_pages=1):
        image_data = []
        after = None
        for page_number in range(n_pages):

            url = "https://oauth.reddit.com/r/{}?limit=1".format(subreddit)

            if after:
                url += "&after={}".format(after)
            response = requests.get(url, headers=self.headers)
            result = response.json()
            after = result['data']['after']
        image_data.extend(
            [(image['data']['title'], image['data']['url'])
                for image in result['data']['children']
                if image['data']['stickied'] is False]
        )

        return self.image_results_dict(image_data)

    def get_quote(self, subreddit, n_pages=1):
        quote_data = []
        after = None
        for page_number in range(n_pages):

            url = "https://oauth.reddit.com/r/{}?limit=1".format(subreddit)

            if after:
                url += "&after={}".format(after)
            response = requests.get(url, headers=self.headers)
            result = response.json()
            after = result['data']['after']
        quote_data.extend(
            [(quote['data']['title'])
                for quote in result['data']['children']
                if quote['data']['stickied'] is False]
        )

        return quote_data

    def article_results_dict(self, data):
        return [dict(zip(['title', 'link', 'upvotes'], item))
                for item in data]

    def image_results_dict(self, data):
        return [dict(zip(['title', 'link'], item)) for item in data]

    def quote_results_dict(self, data):
        return [dict(zip(['title'], item)) for item in data]

