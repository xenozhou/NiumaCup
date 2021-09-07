import os
import json
import participants as part
import random

DATABASE_PATH = os.path.join(os.path.abspath("."), r"database.conf")
parts = {}
defParts = ["许小蒿", "阿鱼", "黄老板", "铁树", "她的宝", "她的宝的宝", "叫我特哥", "陈放屁", "四四", "深海老师"]
for i in range(len(defParts)):
    id = 10000 + random.randint(1, 1000)
    while parts.__contains__(id):
        id = 10000 + random.randint(1, 1000)
    parts[id] = part.Participant(id, defParts[i]).toDic()
with open(DATABASE_PATH, 'w') as f:
    json.dump(parts, f, indent=4, ensure_ascii=False)



