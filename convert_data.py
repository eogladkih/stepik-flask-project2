import json
from data import goals, teachers


def convert_data(data, out):
    with open(out, 'w') as g:
        json.dump(data, g, ensure_ascii=False, sort_keys=True, indent=4)


convert_data(goals, 'goals.json')
convert_data(teachers, 'teachers.json')


