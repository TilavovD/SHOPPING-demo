# SHOPPING-demo

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) installed on your computer. From your command line:


#### Clone this repository

``` bash
git clone https://github.com/TilavovD/SHOPPING-demo.git
```


#### Go into the repository

``` bash
cd SHOPPING-demo
```

#### Create virtual environment

``` bash
python -m venv env
```


#### Activate virtual environment 

``` bash
source env/bin/activate # for linux
env/scripts/activate # for windows
```


#### Install dependencies

``` bash
pip install -r requirements.txt
```

#### Run migrations to setup SQLite database:
``` bash
python manage.py migrate
```

#### Create superuser to get access to admin panel:
``` bash
python manage.py createsuperuser
```

#### Create `.env` file in root directory
And fill it yourself or just copy-paste from .env copy file

#### Login stripe using following codes:
``` bash
./stripe login --interactive
```

##### Press enter and copy-paste following api-key in terminal to asked place
``` bash
sk_test_51LzPsRCGhinPHEzyjDC42vWZlwMF2RgPHpJjhaTDLHCqlXCmmL3ZoFqelcLq2vhUD4TLJaZkp48sBYYt7QDQ6DNr004XGmzKDt
```
or you can use your own api-key also


#### Set stripe webhook:
``` bash
./stripe listen --forward-to localhost:8000/api/v1/orders/webhook/
```

#### Run server:
``` bash
python manage.py runserver
```

### Enjoy!!! 🥂
