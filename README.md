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
```
python manage.py test --keepdb
```
