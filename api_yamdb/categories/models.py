from django.core.validators import MaxValueValidator
from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True, verbose_name='Ссылка на категорию')

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True, verbose_name='Ссылка на жанр')

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField(
        validators=[MaxValueValidator(
            datetime.datetime.now().year,
            message='Работы из будущего не принимаются'
        )],
        help_text='Дата выхода'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        related_name='genre', verbose_name='Жанр',
        help_text='Жанр(ы), к которому(ым) относится произведение'
    )
    category = models.ForeignKey(
        Category, related_name='category', verbose_name='Категория',
        on_delete=models.SET_NULL, null=True,
        help_text='Категория, к которой относится произведение'
    )
    rating = models.IntegerField(
        null=True, verbose_name='Рейтинг',
        help_text='Средний рейтинг произведения'
    )

    def __str__(self):
        return self.text[:20]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'
