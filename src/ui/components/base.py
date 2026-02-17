from playwright.sync_api import Page


class BaseComponent:
    """
    Класс базового компонента
    """

    def __init__(self, page: Page):
        self.page = page

