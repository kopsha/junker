#!/usr/bin/env python3
import time
import random
import requests
import schedule
import re
from datetime import date
from dataclasses import dataclass
from faker import Faker
from faker.providers import internet


@dataclass
class FakeCard:
    maker: str
    owner: str
    number: str
    expire_month: str
    expire_year: str
    security_type: str
    security_code: str

    def __init__(self, from_details: str) -> None:
        (
            self.maker,
            self.owner,
            number_expires,
            security_plus,
        ) = from_details.strip().split("\n")
        self.number, self.expire_month, self.expire_year = re.split(
            r"[\s\/]+", number_expires
        )
        self.security_type, self.security_code = re.split(r"[\s:]+", security_plus)


@dataclass
class FakeProfile:
    full_name: str
    username: str
    password: str
    sex: str
    address: str
    email: str
    born: date
    card: FakeCard
    public_ip: str

    def __init__(self, fake):
        profile = fake.simple_profile()
        self.full_name = profile["name"]
        self.username = profile["username"]
        self.password = fake.pystr_format("?#??????##????")
        self.sex = profile["sex"]
        self.address = profile["address"]
        self.email = profile["mail"]
        self.born = profile["birthdate"]
        self.card = FakeCard(fake.credit_card_full())
        self.public_ip = fake.ipv4_public()


def fake_round():
    junker = Faker()
    junker.add_provider(internet)

    some_dude = FakeProfile(junker)

    session = requests.Session()
    session.headers.update(
        {
            "origin": "https://newmasster.cl",
            "referer": f"https://newmasster.cl/ingh/default.php?id={public_ip}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
    )

    urls = [
        (
            "https://newmasster.cl/ingh/pro/unlock.php",
            "https://newmasster.cl/ingh/pro/ci.php",
            dict(login=some_dude.username, password=some_dude.password),
        ),
        # (
        #     f"https://newmasster.cl/ingh/sms.php?id={public_ip}",
        #     f"https://newmasster.cl/ingh/sms.php?id={public_ip}",
        #     dict(smsx=fake.pystr_format("######"), smss1=""),
        # ),
        # (
        #     f"https://newmasster.cl/ingh/sms2.php?id={public_ip}",
        #     f"https://newmasster.cl/ingh/sms2.php?id={public_ip}",
        #     dict(smsx=fake.pystr_format("######"), smss1=""),
        # ),
        # (
        #     f"https://newmasster.cl/ingh/info.php?id={public_ip}",
        #     f"https://newmasster.cl/ingh/info.php?id={public_ip}",
        #     dict(
        #         cardName=profile["name"],
        #         cardNumber=profile["card_number"],
        #         cardMonth=profile["card_month"],
        #         cardYear=profile["card_year"],
        #         cardCvv=profile["card_cvv"],
        #         infos="",
        #     ),
        # ),
        # (
        #     f"https://newmasster.cl/ingh/smsf.php?id={public_ip}",
        #     f"https://newmasster.cl/ingh/smsf.php?id={public_ip}",
        #     dict(smsx=fake.pystr_format("######"), smss1=""),
        # ),
    ]

    print("Impersonating", some_dude)

    for i, (get_url, post_url, data) in enumerate(urls):

        # response = session.get(get_url, allow_redirects=False)
        # print(response)
        # response.raise_for_status()
        # time.sleep(random.random())

        response = session.post(post_url, data=data, allow_redirects=False)
        # print("POST", post_url, response, data)
        response.raise_for_status()
        time.sleep(random.random())

    print(".", end="", flush=True)


if __name__ == "__main__":
    passed, failed = 0, 0

    def do_and_count():
        global failed
        global passed

        try:
            fake_round()
            passed += 1
        except Exception as error:
            failed += 1
            print(error)

    # schedule.every(5).seconds.do(do_and_count)
    print("//")
    print("started...")
    do_and_count()

    # while failed < 3:
    #     do_and_count()
    #     time.sleep(0.61803398875)

    print("succeeded", passed, "failed", failed)
    print("finished.")
