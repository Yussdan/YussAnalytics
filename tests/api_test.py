"""
Тесты для API, включающие проверку получения последних данных о курсе BTC/USD
и получения исторических данных о курсе BTC за последние 5 дней.
"""
from collections.abc import Iterable
import requests

def test_get_latest():
    """
    Тест для получения последних данных о курсе BTC/USD.

    Отправляет GET-запрос к API, проверяет корректность статуса ответа,
    а также содержимое данных (тип данных и наличие информации о BTC).
    """
    response = requests.get('http://localhost:5000/latest/BTC/USD', timeout=20)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert 'BTC' in data

def test_get_history():
    """
    Тест для получения исторических данных о курсе BTC за последние 5 дней.

    Отправляет GET-запрос к API, проверяет статус ответа и содержимое данных.
    Убедится, что в ответе нет ошибок.
    """
    response = requests.get('http://localhost:5000/history/BTC/day/USD/5', timeout=20)
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert 'error' not in data
    assert isinstance(data, Iterable)

    for item in data:
        assert isinstance(item, dict)
