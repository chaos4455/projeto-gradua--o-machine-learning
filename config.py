SERVICES = [
    {
        'name': 'Gerador de Dados',
        'module': 'gerador_stream',
        'port': 12777,
        'retry_delay': 5,
        'max_retries': 3
    },
    {
        'name': 'Normalizador',
        'module': 'normalizador_stream',
        'port': 12778,
        'retry_delay': 5,
        'max_retries': 3
    },
    {
        'name': 'Treinador',
        'module': 'treinador_stream',
        'port': 12779,
        'retry_delay': 5,
        'max_retries': 3
    },
    {
        'name': 'Consumidor',
        'module': 'consumidor_stream',
        'port': 12780,
        'retry_delay': 5,
        'max_retries': 3
    }
]