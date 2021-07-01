import json

value = u''


with open ("input.txt", "r") as myfile:
    value = myfile.readlines()[0]
    obj = json.loads(value)
    data = obj['data']
    body = data['body']

    body_obj = json.loads(body)

    for o in body_obj:
        print o