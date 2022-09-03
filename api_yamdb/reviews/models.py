from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from categories.models import Title


class Review(models.Model):
    """Модель для отзывов на произведение."""
    text = models.CharField(max_length=800)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='1 это минимальная оценка, 1 за старание автору:)'
        ), MaxValueValidator(
            10, message='Он/она так хорош/а??? но 10 максимум:('
        )],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для соментариев к отзывам."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments")
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]
