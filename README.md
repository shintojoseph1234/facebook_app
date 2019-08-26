# Facebook API

Facebook API is an HTTP-based API capable of updating buisness page info

## Installation

Install virtual enviroonment  [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) for Dependency Management

```bash
pip install virtualenv
```
Create and Activate a virtual environment

```bash
virtualenv facebook_API_env
source facebook_API_env/bin/activate
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install --upgrade -r requirements.txt
```

Migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```

Run the server
```bash
python manage.py runserver 8000
```
Open  [localhost:8000](http://localhost:8000/)  in a browser to see the UI

Open  [localhost:8000/api](http://localhost:8000/api/)  in a browser to see the available API

Open  [localhost:8000/api/schema](http://localhost:8000/api/schema/)  in a browser to see the schema of all API
