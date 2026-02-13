from playwright.sync_api import Page, expect, Locator

from src.ui.components.base import BaseComponent


class Footer(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

    def menu_section(self, section_name: str) -> Locator:
        return self.page.get_by_test_id(f"{section_name}-section")

    def menu_title(self, section_name: str) -> Locator:
        return self.page.get_by_test_id(f"{section_name}-title")

    def contact_menu_item(self) -> Locator:
        return self.page.get_by_test_id("contacts-list").locator("li").first

    def menu_link(self, section_name: str) -> Locator:
        return self.page.get_by_test_id(f"{section_name}-links").locator("li").first

    def check_visibility(self):
        expect(self.menu_section("contacts")).to_be_visible()
        expect(self.menu_title("contacts")).to_be_visible()
        expect(self.contact_menu_item()).to_be_visible()

        expect(self.menu_section("info")).to_be_visible()
        expect(self.menu_title("info")).to_be_visible()
        expect(self.menu_link("info")).to_be_visible()

        expect(self.menu_section("legal")).to_be_visible()
        expect(self.menu_title("legal")).to_be_visible()
        expect(self.menu_link("legal")).to_be_visible()

    def click_link(self, section_name: str):
        self.menu_link(section_name).click()
