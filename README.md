A django app to collect and display movie's short comments from douban.com.

## Quick start
1. `pip3 install django-scrapy-douban`

2. Add "douban" to your INSTALLED_APPS setting like this::
    ```py
    INSTALLED_APPS = (
        ...
        'douban',
    )
    ```

3. Set database configuration in your INSTALLED_APPS setting like this::
   ```py     
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',             # database name 
        'USER': '',             # username 
        'PASSWORD': '',         # password 
        'HOST': '127.0.0.1',
        'PORT': '3306',         # default listen port 
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # the default charset used by django to connect db is 'utf-8'
            # change to 'utf8mb4' is recommended, otherwise some data like emoji faces cannot save 
            # database also need to changed, reference http://www.cnblogs.com/seayxu/p/5603876.html    
            'charset': 'utf8mb4',
        },
    ```
    
 4. Include the polls URLconf in your project urls.py like this::
    ```py
    from django.urls import include 
    from django.conf.urls import url
    url(r'^douban/', include('douban.urls'))
    ```
    
5. Run `python3 manage.py makemigrations douban` and `python3 manage.py migrate` to create the douban models.

6. Visit http://127.0.0.1:8000/douban/ to participate it.

7. Use [virtualenv](https://virtualenv.pypa.io/en/stable/) to deploy project is recommended.

## Show
![film](film_comments.png
)

![custom](custom.png
)

![update](update.png
)
