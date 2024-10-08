#  Проект: Yamd
YaMD — платформа для сбора пользовательских отзывов на различные произведения искусства. Основное внимание уделяется категориям произведений, таким как книги, фильмы и музыка, однако предусмотрены возможности для расширения списка категорий. Пользователи могут оставлять текстовые отзывы и выставлять оценки в диапазоне от 1 до 10, формируя общий рейтинг произведения. Отзывы и комментарии к ним доступны для просмотра другими пользователями.

### Основные возможности:

- Написание публикаций, редактирование, удаление: авторизованные пользователи могут публиковать свои отзывы на произведения, а также редактировать и удалять собственные публикации.
- Просмотр чужих публикаций: Все пользователи могут просматривать отзывы других пользователей.;
- Возможность написать и редактировать комментарии: К отзывам можно добавлять комментарии, что способствует обсуждению произведений.
- Чтение публикаций в интересующей категории: Предоставляется возможность фильтрации отзывов по категориям, таким как «Книги», «Фильмы», «Музыка».

### Ресурсы API YaMDb:
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
  
### Пользовательские роли и права доступа:
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперпользователь Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперпользователя — это не лишит его прав администратора. Суперпользователь — всегда администратор, но администратор — не обязательно суперпользователь.
## Используемые технологии

В проекте используются следующие технологии и библиотеки:

- Django - веб-фреймворк для создания веб-приложений.
- djangorestframework - библиотека для создания  RESTful API на Django.
- PyJWT - библиотека для работы с JSON Web Tokens (JWT).
- pytest - фреймворк для тестирования.
- requests - библиотека для упрощения HTTP-запросов.
- pytest-django: расширение для pytest, которое упрощает написание тестов для приложений на основе Django.
- pytest-pythonpath: Дополнение для pytest, позволяющее динамически управлять переменными окружения PYTHONPATH во время выполнения тестов.

## Установка (Windows):

1. Клонирование репозитория

```
git clone git@github.com:kostoyanskaya/api_yamd.git
```

1. Переход в директорию api_yamd

```
cd api_yamd
```

3. Создание виртуального окружения

```
python -m venv venv
```

4. Активация виртуального окружения

```
source venv/Scripts/activate
```

5. Обновите pip

```
python -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt
```

7. Переход в директорию api_yamdb

```
cd /api_yamd/api_yamdb
```

8. Применение миграций

```
python manage.py migrate
```


9.  Создать суперпользователя

```
python manage.py createsuperuser
```

10. Запуск проекта, введите команду

```
python manage.py runserver
```

## Пример запроса и ответа

### POST запрос
`/api/v1/titles/`

body:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Пример ответа:

```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```


## Документация:
[Documentation](http://127.0.0.1:8000/redoc/)
***

## Авторы
#### [_Анастасия_](https://github.com/kostoyanskaya/),
#### [_Станислав_](https://github.com/Parceva1),
#### [_Елена_](https://github.com/ElenaChelyshkina)
