
# Django-Docker
projeto para criar de forma semi-automática ambientes de desenvolvimento e produção com django e docker.

## Programas necessários

 - Python >= 3
 - Docker
 - Docker compose

## Modo de Usar
Os arguivos ( ***config.py***, ***djangodocker.py*** e ***djangodocker.sh*** ) devem ficar no mesmo diretório do seu projeto django. Modifique as configurações do arquivo *config.py* conforme a sua vontade e em seguida execute o script djangodocker.sh como ***root***. O arquivo djangodocker.py usará as configurações de config.py assim como algumas configurações do arquivo de ***settings.py*** do seu projeto. A escolha do ambiente em desenvolvimento e produção é feita pela Variável ***DEBUG*** localizada no arquivo ***settings.py*** do seu projeto.
