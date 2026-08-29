from enum import Enum


class Routes(str, Enum):
    REGISTRATION = "/auth/register"
    LOGIN = "/auth/login"
    USERS = "/users"
    PRODUCTS = "/products"
    CARTS = "/cart"
    ORDERS = "/orders"

    def __str__(self):
        return self.value
