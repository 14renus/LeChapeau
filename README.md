# LeChapeau

## Run 

### Install Dependencies

```bash
python3 -m venv myvenv
pip install -r requirements.txt
```

### Update database schema
```
python manage.py makemigrations chapeau
python manage.py migrate chapeau
```


### Run Server

```bash
python manage.py runserver
```

## Dev

### Test

Run all tests
```
python manage.py test --keepdb
```

Test specific file
```
python manage.py test chapeau.tests.test_utils
```
