import csv
import re
import requests
import shutil
import os
import time
from bs4 import BeautifulSoup as bs


def get_html(url, useragent=None, proxy=None):
    # session = requests.Session()
    # request = session.get(url=url, headers=useragent, proxies=proxy)
    request = requests.get(url=url, headers=useragent, proxies=proxy)
    if request.status_code == 200:
        return request.text
    else:
        print("Error " + str(request.status_code))
        return request.status_code


def get_pagination_index(html):
    soup = bs(html, 'lxml')
    try:
        pagination = soup.find_all('a', attrs={'class': 'paging__it'})
        count = int(pagination[-1].text.strip())
        print(count)
        return count
    except:
        return 1


def get_link_models(html):
    soup = bs(html, 'lxml')
    prod_list = []

    prods = soup.find_all('div', class_='prod')
    for prod in prods:
        title = prod.find('a', attrs={'class': 'prod__link'}).text.strip()
        title = stripeText(title)
        href = prod.find('a', attrs={'class': 'prod__link'})['href']
        try:
            img = prod.find('img', attrs={'class': 'prod__img'})['src']
        except:
            pass
        desc = prod.find('p', attrs={'class': 'prod__descr'}).text.strip()

        prod_list.append({
            'title': title,
            'href': 'https://komp.1k.by/' + href,
            'img': img,
            'desc': desc
        })

    return prod_list


def parser_model(html, brand_name, model_name):
    soup = bs(html, 'lxml')
    model_options = []

    model_options.append({
        'title': 'Model',
        'value': stripeText(model_name),
    })

    try:
        model = soup.find('b', class_='c-red').text
        status = 'Снят с производства'
    except:
        status = 'Актуальный'

    model_options.append({
        'title': 'Status',
        'value': status
    })

    # Разбираем характеристики устройства
    try:
        spec_units = soup.find_all('div', class_='spec-unit')
        for spec_unit in spec_units:
            spec_unit_title_text = spec_unit.find('span', class_='spec-unit__ttl').text.strip()
            model_options.append({
                'title': 'Caption',
                'value': spec_unit_title_text
            })
            spec_unit_titles = spec_unit.find_all('div', class_='spec-list')
            for spec_unit_title in spec_unit_titles:
                if 'spec-list--sub' in spec_unit_title['class']:
                    model_options.append({
                        'title': 'SubCaption',
                        'value': spec_unit_title.find('caption').text
                    })
                    for row in spec_unit_title.select('tbody tr'):
                        row_text = [x.text for x in row.find_all('span', class_='spec-list__txt')]
                        spect_list_text = ', '.join(row_text)

                        row_val = [x.text for x in row.find_all('td')]
                        spect_list_val = ', '.join(row_val)

                        if spect_list_text:
                            model_options.append({
                                'title': spect_list_text,
                                'value': spect_list_val
                            })
                    model_options.append({
                        'title': 'EndSubCaption',
                        'value': spec_unit_title.find('caption').text
                    })
                else:
                    for row in spec_unit_title.select('tbody tr'):
                        row_text = [x.text for x in row.find_all('span', class_='spec-list__txt')]
                        spect_list_text = ', '.join(row_text)

                        row_val = [x.text for x in row.find_all('td')]
                        spect_list_val = ', '.join(row_val)

                        model_options.append({
                            'title': spect_list_text,
                            'value': spect_list_val
                        })

            if spec_unit_title_text == 'Фото':
                try:
                    # Сохраняем картинку из заголовка
                    big_img = soup.find('img', attrs={'class': 'spec-about__img'})['src']
                    img_file_name = save_img(big_img, brand_name + '_image', model_name)
                    model_options.append({
                        'title': 'main_image',
                        'value': img_file_name
                    })
                except:
                    pass

                # Сохраняем дополнительные картинки из опций модели
                img_link_list = soup.find_all('span', class_='spec-images__it')
                for img_link in img_link_list:
                    img = img_link.find('img')['src']
                    img_file_name = save_img(img, brand_name + '_image', model_name)
                    model_options.append({
                        'title': 'image',
                        'value': img_file_name
                    })
    except:
        pass

    return model_options


def stripeText(text, par=False):
    name = re.sub('[а-яА-ЯёЁ]', '', text)
    name = re.sub('\([^)]+\)', '', name)
    name = re.sub('/', ' ', name).replace('"', '')
    if par:
        name = name.replace('+', '')
    return name.strip()


def spaseSub(text):
    result = re.sub('\s', '', text)
    return result


def save_model_options(data, brand_name, file_name):
    if not os.path.exists(brand_name):
        os.mkdir(brand_name)
    # file_name = spaseSub(model_name) + '__' + timestamp + '.jpg'
    # with open(os.path.join(os.path.dirname(__file__), brand_name, file_name),
    #           'wb') as f:

    with open(os.path.join(brand_name, f'{stripeText(file_name, True)}.csv'), 'a') as file:
        add_data = csv.writer(file, delimiter=';', lineterminator='\n')
        for d in data:
            add_data.writerow((d['title'], d['value']))


def saveFile(prods, file_name):
    for prod in prods:
        with open(f'{file_name}.csv', 'a') as file:
            print(prod['title'])
            add_data = csv.writer(file, delimiter=';', lineterminator='\n')
            add_data.writerow((prod['title'], prod['href'], prod['img'], prod['desc']))


def read_csv(file_name):
    row_list = []
    with open(f'{file_name}.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            row_list.append(row)

    return row_list


def save_img(url, brand_name, model_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        timestamp = str(round(time.time() * 1000))

        if not os.path.exists(brand_name):
            os.mkdir(brand_name)
        file_name = spaseSub(model_name) + '_' + timestamp + '.jpg'
        with open(os.path.join(os.path.dirname(__file__), brand_name, file_name),
                  'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    file_name = brand_name + '/' + file_name
    return file_name
