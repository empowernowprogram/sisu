# SISU VR

_**Sisu VR provides an experience immersive Virtual Reality training based on real-life scenarios.**_

Sisu VR&emsp;|&emsp;[www.sisuvr.com](https://www.sisuvr.com/)

## Build Branches
[![](https://img.shields.io/static/v1?label=build%20type&message=production&color=brightgreen)](https://github.com/empowernowprogram/sisu/tree/heroku-production) [![](https://img.shields.io/static/v1?label=build%20type&message=Staging&color=blue)](https://github.com/empowernowprogram/sisu/tree/heroku-staging) [![](https://img.shields.io/static/v1?label=build%20type&message=Development&color=yellow)](https://github.com/empowernowprogram/sisu/tree/heroku-dev)

### Production
Live production branch of the code that the website runs on. Code pushed to production should be thoroughly evaluated and tested for issues.

Heroku App: [sisu-test-release](https://dashboard.heroku.com/apps/sisu-test-release)

Database: Heroku Postgres

### Staging
Designated for testing and validating pre-production code. Incomplete features should be removed, code and features should be polished and ready for production.

Heroku App: [sisu-staging](https://dashboard.heroku.com/apps/sisu-staging)

Database: Localhost / Heroku Postgres (can be run locally or on heroku)

### Development
Core development branch where new features are merged together, tested, and evaluated. 

Heroku App: [sisu-dev](https://dashboard.heroku.com/apps/sisu-dev)

Database: Localhost / Heroku Postgres (can be run locally or on heroku)

## Build and Release Flow Diagram
![image](https://user-images.githubusercontent.com/16641866/131380627-6646b1a1-30fb-4967-bafb-07b72ba2f87c.png)


## Setup Process
1. Download / pull the development branch

2. Create and/or activate your sisu virtual environment using conda or another virtual environment tool.
    ```
    conda create --name sisu
    conda activate sisu
    ```
    
3. In your termianl or cmd, navigate to the root project folder

4. Install project requirements
    ```
    pip install -r requirements.txt
    ```
    
5. Everytime when you start with an empty database, you need to migrate.
    ```
    python manage.py migrate
    ```

6. If you need to access admin panel (where you can see your registered models), you need to create a superuser account first; if not, you can skip this step.
    ```
    python manage.py createsuperuser
    ```
    Use the credentials you just created to login to the admin panel later.

7. To provide initial data for models, load data from individual fixture:
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

8. Run the app in local server.
    ```
    python manage.py runserver
    ```

9. Open local server on computer at 
    ```
    http://127.0.0.1:8000/
    ```
