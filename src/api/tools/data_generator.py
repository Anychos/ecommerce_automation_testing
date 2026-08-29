import random

from faker import Faker


class DataGenerator:
    def __init__(self, faker: Faker):
        self.faker = faker

    def email(self) -> str:
        return self.faker.email()

    def first_name(self) -> str:
        return self.faker.first_name()

    def phone(self) -> str:
        prefix = self.faker.random_element(("8", "7", "+7"))
        number = self.faker.numerify("9#########")
        return f"{prefix}{number}"

    def password(self) -> str:
        return self.faker.password()

    def product_name(self) -> str:
        return f"Автотест Пицца {self.faker.uuid4()[:8]}"

    def description(self) -> str:
        return self.faker.text()

    def price(self) -> int:
        return self.faker.random_int(min=250, max=2000)

    def availability(self) -> bool:
        return self.faker.boolean()

    def image_url(self) -> str:
        image_url_format = [".jpg", ".png", ".jpeg", ".webp"]
        return self.faker.image_url() + random.choice(image_url_format)

    def quantity(self) -> int:
        return self.faker.random_int(min=1, max=99)

    def category(self) -> str:
        return f"Автотест Категория {self.faker.uuid4()[:8]}"


fake_ru = DataGenerator(Faker("ru_RU"))