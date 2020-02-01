Парсер книг с litnet.com (он же lit-era.com) 
===================

Литнет не дает скачивать доступные вам книги и заставляет их читать со своего убого сайта? Решение тут.

# Для 1го использования:
1. Скачать и установить Python 3. При установке нажать галочку "Add to path" (добавить python в переменные среды, что сделает его запускаемым)
2. Скачать и распаковать проект. 

Далее на Windows в cmd: (или на Linux аналогично)
```
cd Downloads
cd litera-master
dir
pip install -r requirements.txt
starter.py -s volchya-tropa-b34046 -o volchya-tropa.txt
```
Здесь volchya-tropa-b34046 берется из URL (возьмите другую книгу, которую можно скачать без входа на сайт):
https://litnet.com/ru/reader/volchya-tropa-b34046

# Для повторного использования
```
cd Downloads
cd litera-master
starter.py -s volchya-tropa-b34046 -o volchya-tropa.txt
```

Для скачивания с авторизацией смотри проект-оригинал.
