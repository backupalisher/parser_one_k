import get_my_proxy
import parser_utils as parser
from random import uniform
from time import sleep
import os

url_list = {
    'hp': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=filter&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=1122&searchProducers=&fullproducers%5B%5D=1122&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'epson': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=1120&searchProducers=&fullproducers%5B%5D=1122&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'canon': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=411&searchProducers=&fullproducers%5B%5D=1120&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'ricoh': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=filter&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=414&searchProducers=&fullproducers%5B%5D=414&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'kyocera': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=62&searchProducers=&fullproducers%5B%5D=414&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'konica': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=1126&searchProducers=&fullproducers%5B%5D=1131&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'pantum': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=7855&searchProducers=&fullproducers%5B%5D=1126&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'kip': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=8608&searchProducers=&fullproducers%5B%5D=8608&fullproducers%5B%5D=7855&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'mb': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=3033&searchProducers=&fullproducers%5B%5D=3033&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'mimaki': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=6&searchProducers=&fullproducers%5B%5D=6&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'minolta': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=412&searchProducers=&fullproducers%5B%5D=412&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'panasonic': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=383&searchProducers=&fullproducers%5B%5D=383&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'brother': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=filter&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=410&searchProducers=&fullproducers%5B%5D=410&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'lexmark': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=5&searchProducers=&fullproducers%5B%5D=410&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'xerox': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=415&searchProducers=&fullproducers%5B%5D=5&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'samsung': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=387&searchProducers=&fullproducers%5B%5D=415&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'oki': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=producers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=413&searchProducers=&fullproducers%5B%5D=413&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'riso': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=6291&searchProducers=&fullproducers%5B%5D=6291&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'sharp': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=71&searchProducers=&fullproducers%5B%5D=71&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748=',
    'toshiba': 'https://komp.1k.by/periphery-printers/s.php?alias=periphery&alias2=printers&order=top&focuselementid=&selectedelementname=fullproducers%5B%5D&viewmode=standart&keywords=&pricemin=&pricemax=&filter=all&producers%5B%5D=75&searchProducers=&fullproducers%5B%5D=75&from_el_4616=&to_el_4616=&from_el_4624=&to_el_4624=&from_el_4748=&to_el_4748='}


# Получаем ссылки моделей из указанных брендов
def get_models_links():
    brand_name = 'canon'
    url = str(url_list[brand_name])

    proxy = {'http': 'http://' + get_my_proxy.get_proxies_list()}
    useragent = {'User-Agent': get_my_proxy.get_useregent_list()}
    count = parser.get_pagination_index(parser.get_html(url, useragent, proxy))
    parser.saveFile(parser.get_link_models(parser.get_html(url, useragent, proxy)), brand_name)
    if count > 1:
        for i in range(count):
            t = uniform(4, 12)
            sleep(t)
            index = i + 2
            print(index)
            proxy = {'http': 'http://' + get_my_proxy.get_proxies_list()}
            useragent = {'User-Agent': get_my_proxy.get_useregent_list()}
            next_url = url + f'&page={index}'
            if index <= count:
                parser.saveFile(parser.get_link_models(parser.get_html(next_url, useragent, proxy)), brand_name)


def model_parser(brand_name):
    try:
        print(brand_name)
        models_list = parser.read_csv(os.path.join(os.path.dirname(__file__), 'brands', brand_name))
        for model in models_list:
            # 0 - title, 1 - url, 2 - desc
            t = uniform(3, 16)
            sleep(t)
            print(model[0].strip())
            proxy = {'http': 'http://' + get_my_proxy.get_proxies_list()}
            useragent = {'User-Agent': get_my_proxy.get_useregent_list()}
            parser.save_model_options(
                parser.parser_model(parser.get_html(model[1], useragent, proxy), brand_name, model[0]),
                brand_name, model[0]
            )
            parsed_model = []
            parsed_model.append({
                model[0]
            })
            parser.parsed_save(parsed_model, brand_name + '_parsed')

    except:
        print('File not found!')


def main():
    model_parser('hp')


if __name__ == '__main__':
    main()
