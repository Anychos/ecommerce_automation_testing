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

    def phone_number(self) -> str:
        number_prefix_list = ["+7", "8", "7"]
        number_prefix = self.faker.random_element(number_prefix_list)
        number_body = self.faker.random_int(min=0000000000, max=9999999999)
        return f"{number_prefix}{number_body}"

    def password(self) -> str:
        return self.faker.password()

    def address(self) -> str:
        return self.faker.address()


fake_ru = DataGenerator(Faker("ru_RU"))
