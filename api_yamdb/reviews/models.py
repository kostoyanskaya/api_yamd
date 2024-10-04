from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_year


class Genre(models.Model):
    """
    Модель жанров произведений.

    Одно произведение может быть привязано к нескольким жанрам.

    Атрибуты:
    - name: Название жанра (максимальная длина - 200 символов).
    - slug: Уникальный слаг для жанра, используемый в URL.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категории (типы) произведений («Фильмы», «Книги», «Музыка»).

    Одно произведение может быть привязано только к одной категории.

    Атрибуты:
    - name: Название типа произведения (максимальная длина - 256 символов).
    - slug: Уникальный слаг для типа, используемый в URL.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель комментария к отзыву.

    Атрибуты:
    - review: Отзыв, к которому относится комментарий
    (ссылка на модель Review).
    - author: Автор комментария (ссылка на модель User).
    - text: Текст комментария.
    - pub_date: Дата и время публикации комментария.
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
