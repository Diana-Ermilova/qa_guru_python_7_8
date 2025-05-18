"""
Протестируйте классы из модуля homework/models.py
"""
from os import putenv

import pytest
from setuptools.command.bdist_egg import can_scan
from urllib3 import proxy_from_url

from homework.models import Product, Cart



@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts: #group by "products"

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1001) == False
        assert product.check_quantity(998) == True
        assert product.check_quantity(1000) == True

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(250)
        assert product.quantity == 750
        product.buy(750)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(2000)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, product):
        cart = Cart()
        cart.add_product(product, 1000)
        assert cart.products[product] == 1000
        cart.add_product(product, 100)
        assert cart.products[product] == 1100

        cart.add_product(product)
        assert cart.products[product] == 1101

    def test_cart_remove_product(self, product):
        cart = Cart()
        with pytest.raises(ValueError):
            cart.remove_product(product)

        cart.add_product(product, 200)
        cart.remove_product(product, 10)
        assert cart.products[product] == 190

        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, product):
        cart = Cart()
        cart.clear()
        assert cart.products == {}

        cart.add_product(product, 5)
        cart.clear()
        assert cart.products == {}

    def test_total_price(self, product):
        cart = Cart()
        assert  cart.get_total_price() == 0

        cart.add_product(product, 2)
        assert cart.get_total_price() == 200

        product2 = Product("noodle", 300, "This is a noodle", 5000)
        cart.add_product(product2, 2)
        assert cart.get_total_price() == 800

        cart.clear()
        assert cart.get_total_price() == 0

    def test_buy(self, product):
        cart = Cart()
        cart.add_product(product, 5)
        cart.buy()

        assert cart.products == {}

        cart.add_product(product, 9999999)
        with pytest.raises(ValueError):
            cart.buy()