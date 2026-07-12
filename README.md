# Project: Yamd
YaMD is a platform for collecting user reviews of various works of art. The main focus is on categories of works, such as books, movies, and music, but there are options for expanding the list of categories. Users can leave text reviews and give ratings ranging from 1 to 10, forming an overall rating for the work. Reviews and comments on them are available for other users to view.

### Main features:

- Writing, editing, deleting publications: Authorized users can publish their reviews of works, as well as edit and delete their own publications.
- Viewing other people's publications: All users can view other users' reviews.;
- Ability to write and edit comments: Comments can be added to reviews, which facilitates discussion of the works.
- Reading publications in the category of interest: The ability to filter reviews by category, such as "Books," "Movies," "Music," is provided.

### YaMDb API resources:
- Resource auth: authentication.
- Resource users: users.
- Resource titles: works that reviews are written for (a specific movie, book, or song).
- Resource categories: categories (types) of works ("Movies," "Books," "Music"). A work can only be assigned to one category.
- Resource genres: genres of works. A work can be assigned to several genres.
- Resource reviews: reviews of works. A review is linked to a specific work.
- Resource comments: comments on reviews. A comment is linked to a specific review.
  
### User roles and access rights:
- Anonymous — can view descriptions of works, read reviews and comments.
- Authenticated user (user) — can read everything, like Anonymous, can publish reviews and rate works (movies/books/songs), can comment on reviews; can edit and delete their own reviews and comments, edit their own ratings of works. This role is assigned by default to every new user.
- Moderator (moderator) — the same rights as an Authenticated user, plus the right to delete and edit any reviews and comments.
- Administrator (admin) — full rights to manage all project content. Can create and delete works, categories, and genres. Can assign roles to users.
- A Django superuser must always have administrator rights, i.e. the rights of a user with the admin role. Even if the superuser's user role is changed, this will not deprive them of administrator rights. A superuser is always an administrator, but an administrator is not necessarily a superuser.
## Technologies used

The project uses the following technologies and libraries:

- Django - a web framework for creating web applications.
- djangorestframework - a library for creating RESTful APIs with Django.
- PyJWT - a library for working with JSON Web Tokens (JWT).
- pytest - a testing framework.
- requests - a library for simplifying HTTP requests.
- pytest-django: an extension for pytest that simplifies writing tests for Django-based applications.
- pytest-pythonpath: An add-on for pytest that allows dynamic management of the PYTHONPATH environment variable during test execution.

## Installation (Windows):

1. Cloning the repository

```
git clone git@github.com:kostoyanskaya/api_yamd.git
```

1. Navigate to the api_yamd directory

```
cd api_yamd
```

3. Creating a virtual environment

```
python -m venv venv
```

4. Activating the virtual environment

```
source venv/Scripts/activate
```

5. Update pip

```
python -m pip install --upgrade pip
```

6. Installing dependencies

```
pip install -r requirements.txt
```

7. Navigate to the api_yamdb directory

```
cd /api_yamd/api_yamdb
```

8. Applying migrations

```
python manage.py migrate
```


9.  Create a superuser

```
python manage.py createsuperuser
```

10. To run the project, enter the command

```
python manage.py runserver
```

## Example request and response

### POST request
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

Example response:

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


## Documentation:
[Documentation](http://127.0.0.1:8000/redoc/)
***
