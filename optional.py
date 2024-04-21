import csv
import random

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    # 'cookie': 'referer=https%3A%2F%2Ffreelancehunt.com%2F; landing=%2Fua%2Fcategory%2Fvelosipedy%2F; _gcl_au=1.1.1175543886.1713534622; _fbp=fb.2.1713534622429.1237638202; _clck=1aihf3b%7C2%7Cfl2%7C0%7C1570; _gid=GA1.3.1966647188.1713534623; biatv-cookie=; viewed_list=27469; cf_clearance=yPeQVcMee0SDfRgQLfTlwSD4WM0fVmLQlC2ZTKt2KVY-1713536938-1.0.1.1-afC12iI6JeXhD8hxdvq8tFeVt_.Kq6M9iJ.pnLIusuMsp_wKyLa3nr1V9T094SKb4NuIok0JF47uVSIuOELFYw; _ga_LH6D3BMKT4=GS1.1.1713534622.1.1.1713536953.45.0.0; _ga=GA1.3.1960823556.1713534623; _clsk=1ijeogm%7C1713536954953%7C7%7C1%7Cj.clarity.ms%2Fcollect; _ga_6YNHLZVP03=GS1.1.1713534622.1.1.1713536999.60.0.886119238',
    "referer": "https://freelancehunt.com/",
    "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}


class UserAgentAndProxy:
    @classmethod
    def get_random_ua(cls):
        with open("user_agent.txt") as file:
            ua = file.readlines()
            return random.choice(ua).strip()

    @classmethod
    def get_random_proxy(cls):
        with open("proxy.txt") as file:
            proxy = random.choice(file.readlines()).strip()
            return proxy.split(":")


class FileWork:
    @classmethod
    def create_file(cls):
        with open("royal_toys.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    "Категория",
                    "Название",
                    "Картинки",
                    "Артикул",
                    "Описание",
                    "Характеристика",
                )
            )

    @classmethod
    def add_to_file(
        cls,
        product_category,
        product_name,
        product_images,
        product_code,
        product_description,
        product_options,
    ):
        with open("royal_toys.csv", "a", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    product_category,
                    product_name,
                    product_images,
                    product_code,
                    product_description,
                    product_options,
                )
            )
