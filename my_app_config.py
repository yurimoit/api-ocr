# my_app_config.py

bind = '0.0.0.0:1433'  # Endereço e porta para o Gunicorn ouvir
workers = 4  # Número de processos de trabalho (ajuste conforme necessário)
timeout = 60  # Tempo limite para solicitações
