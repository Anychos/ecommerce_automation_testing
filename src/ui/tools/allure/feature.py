from enum import Enum


class Feature(str, Enum):
    AUTHENTICATION = "Authentication"
    HOME_PAGE = "Home Page"
    PRODUCT_DETAIL_PAGE = "Product Detail Page"
    CART_PAGE = "Cart Page"
    CHECKOUT_PAGE = "Checkout Page"
    ORDERS_PAGE = "Orders Page"
    USER_PROFILE_PAGE = "User Profile Page"
