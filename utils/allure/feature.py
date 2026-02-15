from enum import Enum


class Feature(str, Enum):
    # Authentication
    AUTHENTICATION = "Authentication"

    # Users
    ADMIN_USERS = "Admin - Users Management"
    USER_PROFILE = "User - Profile Management"

    # Products
    ADMIN_PRODUCTS = "Admin - Products Management"
    USER_PRODUCTS = "User - Products Browsing"

    # Cart
    USER_CART = "User - Shopping Cart"

    # Orders
    ADMIN_ORDERS = "Admin - Orders Management"
    USER_ORDERS = "User - Orders"

    # Checkout
    USER_CHECKOUT = "User - Checkout"

    # Navigation
    NAVIGATION = "Navigation"

    # Pages
    HOME_PAGE = "Home Page"
    REGISTRATION_PAGE = "Registration Page"
    LOGIN_PAGE = "Login Page"
    PRODUCT_DETAIL_PAGE = "Product Detail Page"
    CART_PAGE = "Cart Page"
    CHECKOUT_PAGE = "Checkout Page"
    ORDERS_PAGE = "Orders Page"
    ORDER_DETAIL_PAGE = "Order Detail Page"
    USER_PROFILE_PAGE = "User Profile Page"
