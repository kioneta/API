import vk_api
import time
from datetime import date
import requests
import json
import re
import random


def wall_get(domain, vk):  # looks at the posts of the selected group (by domain)

    old_date = '20230401'
    offset = 0
    autors = []
    places = []
    while True:
        wall = vk.method('wall.get', {
                                    'domain': domain,
                                    'count': 1,
                                    'offset': offset
                                }
                         )

        post_date = wall['items'][0]['date']

        if check_date(post_date, old_date):
            print('Дата совпадает')
            check_text(wall,autors, places)
        else:
            print('Перебоор, лишний пост')
            print("__________________")
            break
        offset = offset + 1
        print("__________________")

    print("Конец проверки постов")
    get_autors(autors, places)
    

# date - time when post was published
def check_date(post_date, check_date):
    t = time.ctime(post_date)
    ts = time.strptime(t)
    post_date = time.strftime("%Y%m%d", ts)
    print('Дата поста: ', post_date)
    result = (post_date >= check_date)  # true or false
    return result

#checking if there any word in post
def check_text(wall,autors, places):
    post_text = wall['items'][0]['text']
    if len(post_text) > 0:
        print('Текст есть. Начинается проверка тега')
        check_tag(post_text, wall,autors, places)
    else:
        print('Текста нет, пропускаем')

# If "YES", taking from post additional information "autor id, place for event"
def check_tag(post_text, wall, autors, places):
    post_text = post_text.lower()
    kd2s = '#кд2с'
    if re.search(kd2s, post_text):
        print('ТЕГ НАЙДЕН')
        id = str(wall['items'][0]['id'])
        link = 'https://vk.com/wall-176558636_' + id
        print(link)
        add_autor(wall, autors)
        check_place(post_text, places)
    else:
        print('Тега нет. Пропускаем')

# append autor to the list
def add_autor(wall,autors):
    try:
        autor = wall['items'][0]['signer_id']
        autors.append(autor)
    except:
        pass

# append place to the list
def check_place(post_text, places):
    lines = post_text.split('\n')
    a = 'где:'
    for line in lines:
        if re.search(a, line):
            places.append(line)

# print all information that we get from wall
def get_autors(autors, places):
    autorslen = 'Всего постов: ' + str(len(autors))
    print(autorslen)

    my_dict = {i: autors.count(i) for i in autors}
    for key in my_dict:
        a = '@id' + str(key) + " : " + str(my_dict[key])
        print(a)


    print('Места:')
    for place in places:
        print(place)


def main():
    #token = ''  #befor start, unteg this line and put your personal token, otherwise this script wont work.
    vk = vk_api.VkApi(token=token)

    print("Сервер запущен")

    domain = 'spb_nastolki'
    wall_get(domain, vk)  # Main cycle


if __name__ == '__main__':
    main()
