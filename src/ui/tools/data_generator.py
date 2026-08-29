from faker import Faker


class DataGenerator:
    def __init__(self, faker: Faker):
        self.faker = faker

    def email(self) -> str:
        return self.faker.email()

    def first_name(self) -> str:
        return self.faker.first_name()

    def last_name(self) -> str:
        return self.faker.last_name()

    def middle_name(self) -> str:
        return self.faker.middle_name()

    def full_name(self) -> str:
        return self.faker.name()

    def phone(self) -> str:
        prefix = self.faker.random_element(("8", "7", "+7"))
        number = self.faker.numerify("9#########")
        return f"{prefix}{number}"
        
    def password(self) -> str:
        return self.faker.password()

    def address(self) -> str:
        return self.faker.address()


fake_ru = DataGenerator(Faker("ru_RU"))
