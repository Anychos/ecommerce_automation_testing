from enum import Enum


class Route(str, Enum):
    Home = "/"
    Login = "/login"
    Registration = "/register"
    ProductDetail = "/product/"
    Cart = "/cart"
    Checkout = "/checkout"
    OrdersList = "/orders"
    OrderDetail = "/orders/"
