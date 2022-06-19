#!/usr/bin/env python3
import time
import random
import requests
import schedule
from faker import Faker
from faker.providers import internet


def fake_round():
    fake = Faker()
    fake.add_provider(internet)

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
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
    )

    urls = [
        (
            "https://newmasster.cl/ingh/pro/unlock.php",
            "https://newmasster.cl/ingh/pro/ci.php",
            dict(login=profile["username"], password=profile["password"]),
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

    print("Impersonating", profile)

    for i, (get_url, post_url, data) in enumerate(urls):

        # response = session.get(get_url)
        # assert (
        #     response.status_code == 200
        # ), f"GET {get_url} failed with {response.status_code}"
        # time.sleep(random.random())

        response = session.post(post_url, data=data, allow_redirects=False)
        assert response.status_code == 302, f"POST to {post_url} failed with {response.status_code}"
        time.sleep(random.random())

    print("...")


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
            print("ERROR:", error)

        print("succeeded", passed, "failed", failed)

    schedule.every(5).seconds.do(do_and_count)

    print("started...")
    do_and_count()

    while failed < 3:
        schedule.run_pending()
        time.sleep(0.61803398875)
