#Сервис "одноразовых" заметок

разработаноно на Python 3.9.3


##Cервер (xmlrpc + sqlite3)

для запуска :
```
python3 server_xml_rpc.py
```

##WEB-приложение (django=3.2.2)

установка:

```
pip install -r requirements.txt
```

запуск
```
python3 django_notes_xml/manage.py runserver
```

открываем в браузере http://127.0.0.1:8000/


