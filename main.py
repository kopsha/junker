#!/usr/bin/env python3
import time
import random
import requests
import schedule
from faker import Faker
from faker.providers import internet
from fake_useragent import UserAgent


def fake_round():
    fake = Faker()
    fake.add_provider(internet)
    fake_ua = UserAgent()

    session = requests.Session()
    public_ip = fake.ipv4_public()
    profile = fake.simple_profile()
    profile["password"] = fake.pystr_format("?#??????##????")
    profile["card_number"] = fake.credit_card_number()
    expire = fake.credit_card_expire().split("/")
    profile["card_month"] = expire[0]
    profile["card_year"] = expire[1]
    profile["card_cvv"] = fake.credit_card_security_code()

    session.headers.update(
        {
            "origin": "https://newmasster.cl",
            "referer": f"https://newmasster.cl/ingh/default.php?id={public_ip}",
            "user-agent": fake_ua.chrome,
        }
    )

    urls = [
        (
            f"https://newmasster.cl/ingh/default.php?id={public_ip}",
            "https://newmasster.cl/ingh/pro/ci.php",
            dict(login=profile["username"], password=profile["password"])
        ),
        (
            f"https://newmasster.cl/ingh/sms.php?id={public_ip}",
            f"https://newmasster.cl/ingh/sms.php?id={public_ip}",
            dict(smsx=fake.pystr_format("######"), smss1=""),
        ),
        (
            f"https://newmasster.cl/ingh/sms2.php?id={public_ip}",
            f"https://newmasster.cl/ingh/sms2.php?id={public_ip}",
            dict(smsx=fake.pystr_format("######"), smss1=""),
        ),
        (
            f"https://newmasster.cl/ingh/info.php?id={public_ip}",
            f"https://newmasster.cl/ingh/info.php?id={public_ip}",
            dict(
                cardName=profile["name"],
                cardNumber=profile["card_number"],
                cardMonth=profile["card_month"],
                cardYear=profile["card_year"],
                cardCvv=profile["card_cvv"],
                infos="",
            ),
        ),
        (
            f"https://newmasster.cl/ingh/smsf.php?id={public_ip}",
            f"https://newmasster.cl/ingh/smsf.php?id={public_ip}",
            dict(smsx=fake.pystr_format("######"), smss1=""),
        ),
    ]


    for i, (get_url, post_url, data) in enumerate(urls):
    
        print(i, get_url)
        response = session.get(get_url)
        assert response.status_code == 200
        time.sleep(random.random())

        print(i, post_url)
        print("\t", data)
        response = session.post(post_url, data=data, allow_redirects=False)
        print(response)
        assert response.status_code == 302
        print(" => ", response.headers["location"])
        time.sleep(random.random())

    print("...")


if __name__ == "__main__":
    passed, failed = 0, 0

    def do_and_count():
        try:
            fake_round()
            passed += 1
        except Exception as error:
            failed += 1

    schedule.every(15).seconds.do(do_and_count)

    while failed < 3:
        schedule.run_pending()
        time.sleep(0.61803398875)
