#!/usr/bin/env python3
import requests
from faker import Faker
from faker.providers import internet


def main():
    fake = Faker()
    fake.add_provider(internet)

    for i in range(10):
        print(fake.ipv4_public())

    session = requests.Session()

    public_ip = fake.ipv4_public()

    session.headers.update(
        dict(
            origin="https://newmasster.cl",
            referer=f"https://newmasster.cl/ingh/default.php?id={public_ip}",
        )
    )


if __name__ == "__main__":
    main()
