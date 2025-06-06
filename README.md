<h1 align="center">Django ToDo App</h1>
<h3 align="center">A class base view restframework with GenericView classes</h3>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" alt="django" width="40" height="40"/> </a>
<a href="https://www.django-rest-framework.org/" target="_blank"> <img src="https://www.django-rest-framework.org/img/logo.png" alt="sqlite" width="90" height="40"/> </a>
<a href="https://www.w3.org/html/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
</a>
<a href="https://www.w3schools.com/css/" target="_blank"> <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
</a>
<a href="https://www.sqlite.org/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> </a>

</p>

### Demo
It's a preview of the project
![Screenshot 2025-04-30 002633](https://github.com/user-attachments/assets/5911faff-d2eb-4e34-8803-1128046b8760)

### General features
- Class Based View
- Django RestFramewok
- Generic View
- User Authentication

### Todolist features
- Add task
- Edit task
- Delete task

### Setup
To get the repository you need to run this command in git terminal
```bash
https://github.com/mohammadmatin2000/CBV-DRF-ToDoApp.git
```

### Getting ready

Install all project dependencies with this command
```bash
pip install -r rquirements.txt
```

Once you have installed django and other packages, go to the cloned repo directory and ru fallowing command
```bash
python manage.py makemigrations
```

This command will create all migrations file to database

Now, to apply this migrations run following command
```bash
python manage.py migrate
```

### Option
For editing or manage the database, you shulde be superuser and have superuser permission. So lets create superuser
```bash
python manage.py createsuperuser
```
- Email
- Password
- Password confirmation

### Run server
And finally lets start server and see and using the app
```bash
python manage.py runserver
```

Whene server is up and running, go to a browser and type http://127.0.0.1:8000

### Database shema

![Screenshot 2025-04-30 002305](https://github.com/user-attachments/assets/6c978c2d-b553-48fd-ab49-a54beb935daf)

<hr>

<h3 align='center'>Thanks for visiting my app, if you have any opinions or seeing bugs; let me know 🙂</h3>
