### api_yamdb
### Как запустить проект :

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/NikLukyan/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в папку api_yamdb и выполнить миграции:

```
cd api_yamdb
```

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


Когда вы запустите проект, по нижеуказанному адресу будет 
доступна полная документация для API Yatube в формате Redoc: 
```
/redoc/
```

Некоторые примеры запросов к API:
