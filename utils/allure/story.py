from enum import Enum


class Story(str, Enum):
    # Authentication
    USER_REGISTRATION = "User Registration"
    USER_LOGIN = "User Login"
    ADMIN_LOGIN = "Admin Login"
    USER_LOGOUT = "User Logout"

    # ADMIN USERS
    ADMIN_CREATE_USER = "Admin Create User"
    ADMIN_GET_USER_BY_ID = "Admin Get User by ID"
    ADMIN_UPDATE_USER_FULL = "Admin Full Update User"
    ADMIN_UPDATE_USER_PARTIAL = "Admin Partial Update User"
    ADMIN_DELETE_USER = "Admin Delete User"

    # USER PROFILE
    USER_GET_PROFILE = "User Get Own Profile"
    USER_UPDATE_PROFILE_FULL = "User Full Update Profile"
    USER_UPDATE_PROFILE_PARTIAL = "User Partial Update Profile"
    USER_DELETE_PROFILE = "User Delete Profile"

    # ADMIN PRODUCTS
    ADMIN_CREATE_PRODUCT = "Admin Create Product"
    ADMIN_UPDATE_PRODUCT_FULL = "Admin Full Update Product"
    ADMIN_UPDATE_PRODUCT_PARTIAL = "Admin Partial Update Product"
    ADMIN_DELETE_PRODUCT = "Admin Delete Product"

    # USER PRODUCTS
    USER_GET_PRODUCTS_LIST = "User Get Products List"
    USER_GET_PRODUCT_BY_ID = "User Get Product by ID"

    # USER CART
    USER_ADD_ITEM_TO_CART = "User Add Item to Cart"
    USER_GET_CART = "User Get Cart"
    USER_REMOVE_PRODUCT_FROM_CART = "User Remove Product from Cart"
    USER_CLEAR_CART = "User Clear Cart"

    # USER CHECKOUT
    USER_CHECKOUT = "User Checkout"

    # USER ORDERS
    USER_CREATE_ORDER = "User Create Order"
    USER_GET_ORDER_BY_ID = "User Get Order by ID"
    USER_GET_ORDERS_LIST = "User Get Orders List"

    # ADMIN ORDERS
    ADMIN_GET_ORDERS_LIST = "Admin Get Orders List"
    ADMIN_GET_ORDER_BY_ID = "Admin Get Order by ID"

    # NAVIGATION
    HEADER_NAVIGATION = "Header Links Navigation"

    # PAGES VISIBILITY
    PAGE_VISIBILITY = "Page Visibility"
