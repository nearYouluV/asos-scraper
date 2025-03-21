import re
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from threading import Thread
import config
from time import sleep
import tls_client
clothing_items = [
    "t-shirt", "shirt", "dress", "jeans", "sweater", "jacket", "hoodie", 
    "skirt", "shorts", "coat", "blouse", "jumpsuit", "leggings", 
    "cardigan", "sweatpants"
]
original_colors = [
    "black", "white", "gray", "navy", "beige", "brown", "red", "blue", 
    "green", "yellow", "pink", "purple", "orange", "teal", "burgundy"
]

synthetic_fabrics = [
    "polyester", "nylon", "acrylic", "spandex", "lycra", "elastane", 
    "polypropylene", "polyethylene", "polyurethane", 
    "polyvinyl chloride", "acetate", "modacrylic"
]
s =tls_client.Session(client_identifier='chrome_105')
def get_products_id():
    print('start')
    curs = 'WzEsMjEwNjE0MjEyXQ=='
    products_id = []
    while True:
        json_data = [
            {
                'id': '683eef180f89f33b0a26f9b0f3c68f709a2118e937d30da81ec1326cf9ba1503',
                'variables': {
                    'id': 'ern:collection:cat:categ:womens-clothing',
                    'orderBy': 'POPULARITY',
                    'filters': {
                        'discreteFilters': [],
                        'rangeFilters': [],
                        'toggleFilters': [],
                    },
                    'after': curs,
                    'first': 1000,
                    'isPaginationRequest': True,
                    'fetchExperience': True,
                    'subSli': 'client',
                    'width': 2079,
                    'height': 1000,
                    'isLoggedIn': False,
                    
                },
            },
        ]
        # response = requests.post('https://www.zalando.be/api/graphql/', cookies=config.cookies, headers=config.headers, json=json_data)
        response = requests.post('https://www.zalando.be/api/graphql/', json=json_data, headers=config.headers, cookies=config.cookies)

        print(response)
        # with open('test.json', 'w') as f:
        #     json.dump(response.json(),f,indent=2)
        page = response.json()[0]['data']['collection']['entities']['pageInfo']['currentPage']
        print(page)
        curs = response.json()[0]['data']['collection']['entities']['pageInfo']["endCursor"]
        
        products_id.extend([i['node']['id'] for i in response.json()[0]['data']['collection']['entities']['edges']])
        if not curs:
            break
    return list(dict.fromkeys(products_id))

product_links = []
def get_product_links(products_id):
    for product_id in products_id:
        json_data = [
            {
                'id': '72eafc4dae3c11ac78db11a159ba25504e48151e0de84c9a0ea8299568bbe6b7',
                'variables': {
                    'id': 'ern:collection:cat:categ:womens-clothing',
                    'filters': {
                        'discreteFilters': [],
                        'rangeFilters': [],
                        'toggleFilters': [],
                    },
                },
            },
            {
                'id': '3545103e91641bbcd4e17f314e3203df8d47a5a1435bb3f8cd67ad6aec691704',
                'variables': {
                    'id': f'{product_id.strip()}',
                    'version': 1,
                    'moduleInput': {
                        'module': 'PRODUCT_CARD_WITH_HOVER',
                    },
                    'enableFlexiPrice': True,
                    'displayContext': {
                        'module': 'PRODUCT_CARD_WITH_HOVER',
                    },
                },
            }
        ]
        try:
            response = requests.post('https://www.zalando.be/api/graphql/', cookies=config.cookies, headers=config.headers, json=json_data)
        except:
            sleep(10)
            response = requests.post('https://www.zalando.be/api/graphql/', cookies=config.cookies, headers=config.headers, json=json_data)

        print(response)
        try:
            clothes = response.json()[1]['data']['product']['family']['products']['edges']
        except:
            continue
        for clothing in clothes:
            colors =  clothing['node']['name'].split('-')[-1].lower().strip().split()
            for color in colors:
                # if clothing['node']['name'].split('-')[-1].lower().strip() in colors:
                if color.strip() in original_colors:
                    for clothing_type in clothing_items:
                        #FIXME:
                        
                        if len(clothing['node']['name'].split('-')[-2].lower()) !=  len(clothing['node']['name'].split('-')[-2].lower().replace(clothing_type, '')):
                            product_links.append(clothing['node']['uri'])
                            break

def is_valid_product(parsed_json):
    for key in parsed_json['cache'].keys():
        # print(type(key))
        if json.loads(key).get('id', '') == '9e11ecba75b49ff4e6bf818b175a0acaa3e76fbe441c5a78f05bd72c9cd8b6ef':
            materials_key = key
    clothing_data = parsed_json['cache'][materials_key]
    for attribute in clothing_data['data']['product']['attributeSuperClusters']:
        if attribute['id'] == "material_care":
            for material in attribute['clusters'][0]['attributes']:
                try:
                    if material['value'].split()[-1] in synthetic_fabrics:
                        return False
                except:
                    continue
    return True


data = []
bad_links = []
def get_products_data(products_links):
    for url in products_links:
        # r = requests.get(
        #     'https://www.zalando.be/stradivarius-straight-leg-jeans-raw-denim-sth21n0ky-k11.html',
        #     cookies=config.cookies,
        #     headers=config.headers,
        # )
        r = s.get(
            'https://www.zalando.be/stradivarius-straight-leg-jeans-raw-denim-sth21n0ky-k11.html',
        )
        print(r)
        if r.status_code == 403:
            bad_links.append(url)
        if r.status_code == 429:
            while r.status_code == 429:
                sleep(60)
                r = s.get(
                    url,
                )
                print(r)
        soup = BeautifulSoup(r.text, 'lxml')

        js_string = soup.find('body').find_all('script')[2].text
        start_index = js_string.find("runtime['hydratePartial'](")

        if start_index != -1:
            json_string = js_string[start_index + len("runtime['hydratePartial']("):-3].replace(');', '')  # Remove the last `);`
            try:
                # **Step 2: Parse JSON**
                parsed_json = json.loads(json_string)
                

                
            
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
        else:
            print("Pattern not found.")
        # with open('test2.json', 'w') as f:
        #     json.dump(parsed_json, f, indent=2)
        if not is_valid_product(parsed_json):
            continue
        for key in parsed_json['cache'].keys():
            # print(type(key))
            if json.loads(key).get('id', '') == '9e11ecba75b49ff4e6bf818b175a0acaa3e76fbe441c5a78f05bd72c9cd8b6ef':
                materials_key = key
            elif json.loads(key).get('id', '') == 'cdbf06a32be4b782abcb5163dd5243a9f5c7a9301a8dad07d4d5aca8a65d642e':
                price_key = key
            elif json.loads(key).get('id', '') == "895297954c2c899245f48c91e0a7d664a49edaa438c7e238c56737f359dd4968":
                imgs_key = key
        clothing_data = parsed_json['cache'][materials_key]['data']['product']
        name = clothing_data['name']
        brand = clothing_data['brand']['name']
        pricing_data = parsed_json['cache'][price_key]['data']['product']
        price = pricing_data['simplesWithStock'][0]['allOffers'][0]['price']['trackingCurrentAmount']
        color = name.split('-')[-1]
        article_of_clothing = name.split('-')[0]
        imgs_data = parsed_json['cache'][imgs_key]['data']['product']
        imgs = '\n'.join([i['uri'] for i in imgs_data['galleryMedia']])
        data.append([url,name,brand,price,color,article_of_clothing,imgs])
        # print(data)


def save(data):
    cols = ['Link', 'Name', 'Brand', 'Price', 'Color', 'Article of clothing', 'Imgs']
    df = pd.DataFrame(data=data,columns=cols)
    df.to_csv('sample.csv', index=False, encoding='utf-8')
    df.to_excel('women-denmark.xlsx', index=False)

# products_id = get_products_id()

def main():
    # products_id = get_products_id()
    # num_threads = 8
    # batch_size = len(products_id) // num_threads
    threads = []
    # for i in range(num_threads):
    #     start = i * batch_size
    #     end = start + batch_size if i < num_threads -1 else len(products_id)
    #     t = Thread(target=get_product_links, args=(products_id[start:end], ))
    #     t.start()
    #     threads.append(t)
    
    # for t in threads:
    #     t.join()
    # with open('product-links.json', 'w') as f:
    #     json.dump(product_links, f,indent=2)
    threads.clear()
    with open('product-links.json', 'r') as f:
        product_links = json.load(f)
    num_threads = 4
    batch_size = len(product_links) // num_threads
    for i in range(num_threads):
        start = i * batch_size
        end = start + batch_size if i < num_threads -1 else len(product_links)
        t = Thread(target=get_products_data, args=(product_links[start:end], ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    with open('bad_links.json', 'w') as f:
        json.dump(bad_links,f,indent=2)
    save(data)
    # get_products_data(['https://en.zalando.de/jjxx-jxvienna-jeans-skinny-fit-dark-blue-denim-jj621n001-k11.html'])
if __name__ == '__main__':
    main()
    # get_product_links(products_id[:2])
    # get_products_data(['https://en.zalando.de/jjxx-jxvienna-jeans-skinny-fit-dark-blue-denim-jj621n001-k11.html'])
    # print(len(products_id))

