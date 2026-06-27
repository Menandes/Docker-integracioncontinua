import os
os.environ.setdefault('REDIS_HOST', 'localhost')

from app import app


def test_pagina_responde_ok():
    # La página principal debe responder con código HTTP 200
    cliente = app.test_client()
    respuesta = cliente.get('/')
    assert respuesta.status_code == 200


def test_pagina_cuenta_visitas():
    # El cuerpo de la respuesta debe contener el mensaje de visitas
    cliente = app.test_client()
    respuesta = cliente.get('/')
    texto = respuesta.get_data(as_text=True)
    assert 'visitado' in texto


def test_saludo_presente():
    cliente = app.test_client()
    respuesta = cliente.get('/')
    texto = respuesta.get_data(as_text=True)
    assert '¡Hola!' in texto, f"Se esperaba '¡Hola!' en la respuesta, pero se obtuvo: {texto!r}"