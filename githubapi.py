import os
import requests

token = os.environ.get('GITHUB_TOKEN')


def graphql_query(query):
    req = requests.post('https://api.github.com/graphql',
                        json={'query': query},
                        headers={'Authorization': f'token {token}'})
    if req.status_code == 200:
        print(req.json())
        return req.json()
    raise Exception(f'Github API Query Failed with Status {req.status_code}')
