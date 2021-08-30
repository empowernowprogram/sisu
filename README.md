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
5. Setting up the local server using manage.py 
    ```
    python manage.py migrate
    python manage.py runserver
    ```

6. Open local server on computer at 
    ```
    http://127.0.0.1:8000/
    ```