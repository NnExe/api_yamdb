# API_YAMDB
- [Введение](#введение)
- [Установка](#install)
- [Загрузка данных](#upload)
- [Endpoints](#endpoints)
  - [auth](#endpoint-auth)
  - [categories](#endpoint-categories)
  - [genres](#endpoint-genres)
  - [titles](#endpoint-titles)
  - [reviews](#endpoint-reviews)
  - [comments](#endpoint-comments)
  - [users](#endpoint-users)
- [О разработчиках](#about-authors)

## Введение
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
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
