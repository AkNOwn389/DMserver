import codecs

with codecs.open('data.json', 'r', encoding='utf-8', errors="ignore") as f:
    data = f.read()
    data = data.encode('utf-8')
    data = data.decode()

with open('datanew.json', 'w', encoding='utf-8') as f:
    f.write(data)