# Backend for blog-like service

----
Packed into docker


If you cloned this repo use: 
>docker-compose -f docker-compose.yml up -d --build - to build this project
>docker-compose -f docker-compose.yml exec web python manage.py makemigrations - to make migrations
>docker-compose -f docker-compose.yml exec web python manage.py migrate - to apply migrations
>after this your app will be available on localhost:8000

----
### heroku.yml


File configures everything you need to deploy on Heroku

----
### requirements.txt


Contains all required modules

---
### .envs
.env files are hidden, but you should specify your system variables to work with this project:
>DEBUG
>SECRET_KEY
>DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
>SQL_ENGINE=django.db.backends.postgresql
>SQL_DATABASE
>SQL_USER
>SQL_PASSWORD
>SQL_HOST
>SQL_PORT
>DATABASE=postgres
>EMAIL_USER
>EMAIL_PASSWORD

----
### Authorization
App uses standart Django's token authentication model, you need to send Authorization header into some endpoints to receive content


App speaks JSON :) (accept:application/json)

----
### Emailing
Here we use gmail smpt to send messages about new posts to users, specify your credentials to do this





