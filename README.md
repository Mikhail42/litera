Парсер книг с litnet.com (он же lit-era.com) 
===================

Литнет не дает скачивать доступные вам книги и заставляет их читать со своего убого сайта? Решение тут.

Для 1го использования:
1. Скачать и установить Python 3. При установке нажать галочку "Add to path" (добавить python в переменные среды, что сделает его запускаемым)
2. Выполнить
```
pip install -r requirements.txt
```
3. Скачать проект. 
Далее на Windows в cmd:
``
cd Downloads
cd litera-master
dir
starter.py -s volchya-tropa-b34046 -o volchya-tropa.txt
```
или на Linux:
``
./starter.py -s volchya-tropa-b34046 -o ~/volchya-tropa.txt
```

Здесь volchya-tropa-b34046 берется из URL (вольмите другую книгу, котую можно скачать без входа на сайт):
https://litnet.com/ru/reader/volchya-tropa-b34046
