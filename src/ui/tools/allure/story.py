from enum import Enum


class Story(str, Enum):
    LOGIN = "Login"
    REGISTRATION = "Registration"

    GET_PRODUCTS_LIST = "Get products list"
    GET_PRODUCT_BY_ID = "Get product by id"

    ADD_PRODUCT_TO_CART = "Add product to cart"
    REMOVE_PRODUCT_FROM_CART = "Remove product from cart"
    GET_CART = "Get cart"
    CLEAR_CART = "Clear cart"

    GET_ORDERS = "Get orders"
    GET_ORDER_BY_ID = "Get order by id"
    CREATE_ORDER = "Create order"


