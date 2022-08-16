### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AIBogdanov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Можно загрузить тестовые данные в проект:

```
python3 manage.py <base_name> <file_name>
```

Примеры csv-файлов находятся в директории statc/data/
Рекомендуемый порядок загрузки данных:
1. user
2. category
3. genre
4. title
5. review
6. comment
7. genretitle
