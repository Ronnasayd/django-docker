


<img src="django-docker.png" alt="django-docker" width="200"/>
# Django-Docker
Projeto para criar de forma semi-automática ambientes de desenvolvimento e produção em django com docker e docker-compose.

## Programas necessários

 - Python >= 3
 - Docker
 - Docker compose

## Modo de Usar
Os arguivos (***wait-for-it.sh***, ***config.py***, ***djangodocker.py*** e ***djangodocker.sh*** ) devem ficar no mesmo diretório do seu projeto django.

 Modifique as configurações do arquivo *config.py* conforme a sua vontade e em seguida execute o script djangodocker.sh. O arquivo djangodocker.py usará as configurações de config.py para montar a infraestrutura desejada no sistema. 

 A escolha do ambiente entre desenvolvimento ou produção é feita pela Variável ***DEBUG*** localizada no arquivo ***config.py***.

Em seu arquivo **settings.py** modifique ou adiciones as seguintes linhas de código pelos valores indicados abaixo:

    from decouple import config
    DEBUG = config('DEBUG', default=False, cast=bool)
    STATIC_ROOT = config('STATIC_ROOT')
    MEDIA_ROOT = config('MEDIA_ROOT')
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', ## coloque aqui a engine do banco que você vai utilizar ##
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD')
        }
    }

