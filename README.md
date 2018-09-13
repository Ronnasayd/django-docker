

# Django-Docker
projeto para criar de forma semi-automática ambientes de desenvolvimento e produção em django com docker e docker-compose.

## Programas necessários

 - Python >= 3
 - Docker
 - Docker compose

## Modo de Usar
Os arguivos (***wait-for-it.sh***, ***config.py***, ***djangodocker.py*** e ***djangodocker.sh*** ) devem ficar no mesmo diretório do seu projeto django.

 Modifique as configurações do arquivo *config.py* conforme a sua vontade e em seguida execute o script djangodocker.sh. O arquivo djangodocker.py usará as configurações de config.py para montar a infraestrutura desejada no sistema. 

 A escolha do ambiente entre desenvolvimento ou produção é feita pela Variável ***DEBUG*** localizada no arquivo ***config.py*** do seu projeto.

Em seu arquivo **settings.py** modifique ou adiciones as seguintes linhas de código pelos valores indicados abaixo:

- DEBUG = os.environ['DEBUG']
- STATIC_ROOT = os.environ['STATIC_ROOT']
- MEDIA_ROOT = os.environ['MEDIA_ROOT']
