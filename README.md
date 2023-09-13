ЗАПУСК:

1. sudo vim etc/hosts и вставить:  
    192.168.220.2   djangoproject  
    192.168.220.6   adminer  
    192.168.220.10  redis  
    192.168.220.11  celery  

2. docker-compose up --build

.env file незаигнорен специально!!!
