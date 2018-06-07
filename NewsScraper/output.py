import json


def save_json(list_news, file):
    with open(file + '.json', 'w') as fp:
        json.dump(list_news, fp)
