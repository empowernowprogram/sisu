## Getting Started

Download Anaconda and run Django in conda virtual environment:

#### Step 1. 
Create a new environment named **sisu** (or name it as you like) with specific version of python inside your fetched working directory.
```
conda create -n sisu python=3.6
```

#### Step 2. 
Activate the environment **sisu** 
```
conda activate sisu
```

`(sisu)` denotes that the environment is activated.

#### Step 3.
Install packages specified in the `requirements.txt` file.
```
pip install -r requirements.txt
```

#### Step 4.
Everytime when you start with an empty database, you need to migrate.
```
python manage.py migrate
```

#### Step 5.
If you need to access admin panel (where you can see your registered models), you need to create a superuser account first; if not, you can skip this step.
```
python manage.py createsuperuser
```
Use the credentials you just created to login to the admin panel later.

#### Step 6.
To provide initial data for models, load data from individual fixture:
```
python manage.py loaddata post-program-survey-choices.json
python manage.py loaddata behavior.json
python manage.py loaddata mock-player-role.json
python manage.py loaddata mock-ethical-feedback.json
```

Or load multiple fixtures at once:
```
python manage.py loaddata */fixtures/*.json
```

#### Step 7.
Run the app in local server.
```
python manage.py runserver
```
Now, you can access the app at `http://127.0.0.1:8000/` or the port you specified.