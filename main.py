import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

from optional import headers, UserAgentAndProxy, FileWork


class RoyalToys:
    def format_text(self, text):
        formatted_text = re.sub(r"[;,]", " ", text)
        return formatted_text

    async def settings_for_parsing(self, max_attempts, time, showLogs=True, **kwargs):
        attempts = 0
        while attempts <= max_attempts:
            try:
                await self.parse_page(kwargs["url"], kwargs["headers"], kwargs["proxy"])

                if showLogs:
                    print(f"[LOGS] Successful! {attempts}/{max_attempts} attempts")

                return
            except Exception as ex:
                attempts += 1

                if showLogs:
                    print(f"[LOGS] Error! {attempts}/{max_attempts} attempts.")
                    print(f"[ErrorINFO] {ex}")

                proxy_params = UserAgentAndProxy.get_random_proxy()
                proxy = f"http://{proxy_params[2]}:{proxy_params[3]}@{proxy_params[0]}:{proxy_params[1]}"

                kwargs["proxy"] = proxy

                await asyncio.sleep(time)

    async def parse_page(self, url, headers, proxy):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                res_text = await response.text()
                soup = BeautifulSoup(res_text, "lxml")

                product_category = self.format_text(
                    soup.find("ul", class_="breadcrumbs")
                    .find_all("li")[-1]
                    .find("a")
                    .text.strip()
                )
                product_name = self.format_text(
                    soup.find("div", class_="content-head__title")
                    .find("h1")
                    .text.strip()
                )
                try:
                    product_images = [
                        "https://royaltoys.com.ua" + item.get("src")
                        for item in soup.find(
                            "div", class_="gallery-previews-l"
                        ).find_all("img")
                    ]
                except:
                    product_images = "https://royaltoys.com.ua" + soup.find(
                        "a",
                        class_="product-gallery-main__el js-product-gallery-main-el js-product-image-popup",
                    ).get("href")
                code = soup.find("div", class_="product-code") 
                if len(code.find_all("span")) == 2:
                    product_code = (
                        soup.find("div", class_="product-code")
                        .find_all("span")[-1]
                        .text.strip()
                    )
                else:
                    product_code = (
                        soup.find("div", class_="product-code")
                        .text
                        .strip()
                        .split(":")[-1][1:]
                    )
                product_description = self.format_text(
                    soup.find("div", class_="product-card__description")
                    .find("div")
                    .text.strip()
                )
                product_options = [
                    f"{item.find_all('td')[0].text.strip()}: {item.find_all('td')[-1].text.strip()}"
                    for item in soup.find(
                        "table", class_="products-list__features product_features"
                    ).find_all("tr")
                ]

                FileWork.add_to_file(
                    product_category,
                    product_name,
                    " | ".join(product_images)
                    if type(product_images) == list
                    else product_images,
                    product_code,
                    product_description,
                    " | ".join(product_options),
                )

    async def create_tasks(self, url):
        proxy_params = UserAgentAndProxy.get_random_proxy()
        proxy = f"http://{proxy_params[2]}:{proxy_params[3]}@{proxy_params[0]}:{proxy_params[1]}"

        tasks = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                res_text = await response.text()
                soup = BeautifulSoup(res_text, "lxml")

                pagination = int(
                    soup.find("ul", class_="pagination").find_all("li")[-2].text
                )

                count_of_proxy = 1
                for page in range(1, pagination + 1):
                    headers["user-agent"] = UserAgentAndProxy.get_random_ua()

                    if count_of_proxy % 5 == 0:
                        proxy_params = UserAgentAndProxy.get_random_proxy()
                        proxy = f"http://{proxy_params[2]}:{proxy_params[3]}@{proxy_params[0]}:{proxy_params[1]}"

                    async with session.get(
                        f"{url}?page={page}", headers=headers, proxy=proxy
                    ) as response:
                        res_text = await response.text()
                        soup = BeautifulSoup(res_text, "lxml")

                        for item in soup.find_all("div", class_="product-tile__outer"):
                            link = "https://royaltoys.com.ua" + item.find("a").get(
                                "href"
                            )
                            task = asyncio.create_task(
                                self.settings_for_parsing(
                                    3, 1, url=link, headers=headers, proxy=proxy
                                )
                            )
                            tasks.append(task)

                    count_of_proxy += 1

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    FileWork.create_file()
    royal_toys = RoyalToys()
    asyncio.run(
        royal_toys.create_tasks("https://royaltoys.com.ua/ua/category/velosipedy/")
    )
