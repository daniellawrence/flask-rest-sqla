#!/usr/bin/env python
import requests

BASE = 'http://localhost:5000/api/'
headers = {'Accept': 'application/vnd.api+json'}

hives = requests.get(BASE + 'hive', headers=headers).json()

for hive in hives.get('data'):
    hive_id = hive.get('id')
    for hive_key, hive_value in hive.get('attributes').items():
        print 'HIVE', hive_key, hive_value

        bees = requests.get(BASE + 'hive/{0}/bees'.format(hive_id), headers=headers).json()
        for bee in bees.get('data'):
            for bee_key, bee_value in bee.get('attributes').items():
                print '', 'BEE', bee_key, bee_value
