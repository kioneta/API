import requests
import csv
from datetime import datetime


def take_1000_posts():
    token = "db886432db886432db8864328cd89c2bf4ddb88db886432bffff269c78fa8b0735cec14"
    domain = "spb_nastolki"
    version = "5.131"
    count = 100
    offset = 0
    all_posts = []

    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    "access_token": token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts


def save_to_excel(all_posts):
    post_number = 0
    with open('kds_1000_posts.csv', 'w', encoding="utf-8") as file:
        save = csv.writer(file)
        save.writerow(('date', 'author_url', 'likes', 'views', 'reposts_count', 'comments', 'body', 'post_type', 'post_url'))

        for post in all_posts:
            # try to find author.
            try:
                author = post['signer_id']
            except:
                pass

            save.writerow(
                (datetime.utcfromtimestamp(post['date']), "https://vk.com/id" + str(author), post['likes']['count'], post['views']['count'],
                 post['reposts']['count'], post['comments']['count'], str(post['text']).replace("\n", " "), post['post_type'],
                 "https://vk.com/spb_nastolki?w=wall-176558636_" + str(post['id'])))


all_posts = take_1000_posts()
save_to_excel(all_posts)
