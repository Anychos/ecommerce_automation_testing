from playwright.sync_api import Page


class BaseComponent:
    """
    Базовый компонент
    """
    def __init__(self, page: Page):
        self.page = page

