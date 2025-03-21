import requests
import math
from threading import Thread
import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import asyncio
from time import sleep
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.asos.com/nike-training/nike-training-totality-dri-fit-knit-7inch-shorts-in-light-khaki/prd/207051455',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

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
    "polyvinyl chloride", "acetate", "modacrylic", "polyamide"
]
cookies = {
    'asos_drmlp': '154ded000a5cbd4e9d1d1353b3506712',
    'asos-anon12': '019500e22ffc7ec6bbe162aa1fb855b0',
    'asos-ts121': '019500e2-2ffc-773a-a7b7-c6518b3facb3',
    'featuresId': '7abb4da0-2317-4a81-8c0c-75eb4a36a0a5',
    'AMCVS_C0137F6A52DEAFCC0A490D4C%40AdobeOrg': '1',
    's_cc': 'true',
    'OptanonAlertBoxClosed': '2025-02-13T19:56:29.749Z',
    'eupubconsent-v2': 'CQMwwLAQMwwLAAcABBENBcF8AP_gAEPAAAYgKiQEAAEgAYADuAHwATYA_QCigImATYApcBeYDLgGjgPrAjZBUMFRAPrgDAB8AH6AiYBeYDLgH1gAAAAA.f_wACHgAAAAA',
    'OTAdditionalConsentString': '1~230.318.540.737.1040.1166.1227.1548.1638.1651.1677.1703.1721.1765.1782.1786.1832.1917.1944.1987.2008.2039.2107.2140.2150.2177.2219.2292.2305.2312.2331.2370.2377.2387.2461.2493.2501.2535.2567.2569.2604.2612.2614.2643.2645.2650.2651.2784.2875.2898.2908.2920.3012.3017.3018.3048.3055.3112.3173.3185.3223.3227.3235.3293.3306.3309.3315.3328.3331.3731.8931.9731.13731.16931.27831.31631.32531.33631.34231.34631.36831',
    'plp_columsCount': 'fourColumns',
    'stc-welcome-message': 'cappedPageCount=2&resolvedDeliveryCountry=PL&userTookActionOnWelcomeMessage=true',
    'asosAffiliate': 'affiliateId=17295',
    'PIM-SESSION-ID': 'CMhiYUKiStN4ISvR',
    'floor': '1000',
    '_abck': '48DFF4A2007139E96424B6B74A528BE0~0~YAAQBwxAFwqt56OVAQAA0PJWpA21a1OdMMuEpZdIUO/cBU0zFewZLGdFIQncPm6DR8E4hZeAoV+DGkuGeQQsNw/8m+hbZhte0HNxSE0HJn47fnjNFixbZYVQmiJ8fa5kAYYdgb7yWwqh/ASbICA1XYA5PQ948Ek+i6Wi2iLguQTT9javxIW+3Q4/uusi79XIAKOAPORlqeFBCWs7MbbAfuzNzo0ErZR4LBwQoWyN8wwVCf6KJunYGh0s5upq/nZ+mr09/BgDRR/zBZ8DHoQc0psy5ilbLWDrbwlXd0wymyG54puifLDLwQ7ZQYj42iyvsZGThX4RSwgwEfAbN14PTwem7TX0jaIHANSDAI4Zb9imtUuMdPpPXttk3eQ0xT2obsFBJdkCtbNDdaw4GBWpRn1K+OfAn0Np3mkq2wvCEQAkxWShs4satOKQVk/WZlQzwWF/sDReBf7ZXCrVwT/MIeYlwmg9sTBG8e2f1kN3SmCguzGHfkWYoo4=~-1~-1~-1',
    'keyStoreDataversion': '4i7nlxk-44',
    'AMCV_C0137F6A52DEAFCC0A490D4C%40AdobeOrg': '-1303530583%7CMCMID%7C54027747559069552536811629355504292071%7CMCAID%7CNONE%7CMCOPTOUT-1742226119s%7CNONE%7CvVersion%7C3.3.0',
    'ak_bmsc': 'A71E1230E876B97E8D5AB730633FC0AF~000000000000000000000000000000~YAAQBwxAF4qt56OVAQAARvRWpBs+fgOCmLP6AYOJ1bj1TQseyD0sQARZTTJo4GZxfsoc67+Mr39MEJ0b99RY7w80OiZ6aR3+0OnLeZAKtEE0VrM23Hudghk4RP9lq0Ld5zWOQKuj/qj/74thvaNEVKqflsSQy4bG4lMHUiRnWJfayGC/+uGFWtPgpZq20g4PyyxJkQRNWffQniwhv/7mYwRioUdGNbfhNRf5vN405698elc9cIS3Vhpsf257N4Yshnq7slci0Mlx2tFyi0xrSC7RYvWt/JpQ4IKZDnDWDx2fmqqC8SJ2wPUx+2AsocLI7fBQ96P8lHTR4zXl9d/ITkAcSZbBJry9LpSsGCxkov76NoN9YOAOZZ5mQwbgzb/ul27iohQnsUlC',
    'asos-b-sdv629': '4i7nlxk-44',
    '_s_fpv': 'true',
    'browseSizeSchema': 'EU',
    'siteChromeVersion': 'au=13&com=13&de=13&dk=13&es=13&fr=13&it=13&nl=13&pl=13&roe=13&row=13&ru=13&se=13&us=13',
    'browseCountry': 'SE',
    'browseCurrency': 'SEK',
    'storeCode': 'SE',
    'currency': '8',
    'browseLanguage': 'sv-SE',
    'bm_sz': 'DB7DEEDABA88521EA5A44513B3A457DE~YAAQBwxAF8Lg9qOVAQAAtK2KpBvxKNdZwnfCEdc+FOQ/gbX6iuDJgvcAeqQVsHfLz0d1fQDE9S243g5enwK04ZFGajr8z1miJP+RcDDdNINF5LcYbItjIXqUn3VmbYitzAlgZfYKmgvyAB605RcGgPn+7H/CiTC5qhkQlClhhtjy+IMMoDzLHxqWe9ktK98JYwlRMNxqBnol7AJTFsDylzhpWhjKEfB+9etTpCWgsoWawZJHZgAzHO0EggvqlVDsTEtd9ynFhzjfDjIlxa0/1CNcn0gDlmsnJJNWkmC1qVkbwoYHzjEirlQrtkS6MH/BoJkNZLRjJqOFQGhvQoxcR/B5g5A0s9CoCHt6PnuWZ2hAFEXBohX13lYSg7ICUMiDZL2sxq9JS6DAWr0BC8PwACqXazJiid4/g/QGpemdbj2Qg5fqfkzuaP8ZYbMwBt4Vtg/gvB+aq31ARU9Elw3f8bZEdBeADRPPuS47~3228981~3552068',
    's_pers': '%20s_vnum%3D1743454800924%2526vn%253D3%7C1743454800924%3B%20gpv_eVar230%3Dno%2520value%7C1742223659181%3B%20gpv_eVar234%3Dno%2520value%7C1742223659181%3B%20gpv_eVar193%3Dno%2520value%7C1742223659183%3B%20gpv_e198%3Dno%2520value%7C1742223659183%3B%20gpv_p6%3D%2520%7C1742224090702%3B%20eVar225%3D13%7C1742224110152%3B%20visitCount%3D3%7C1742224110152%3B%20gpv_e231%3D4c20be26-3467-4d5c-8740-c8ca5f2bd801%7C1742224112310%3B%20s_invisit%3Dtrue%7C1742224112321%3B%20s_nr%3D1742222312327-Repeat%7C1773758312327%3B%20gpv_e47%3Dno%2520value%7C1742224112327%3B%20gpv_p10%3Ddesktop%2520se%257Ccategory%2520page%257C27108%2520page%25202%2520refined%7C1742224112333%3B',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Mar+17+2025+16%3A38%3A33+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=2a09491c-237c-4209-94b4-ef42c7c508e6&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0001%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=PL%3B14&AwaitingReconsent=false',
    's_sq': 'asoscomprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddesktop%252520se%25257Ccategory%252520page%25257C27108%252520page%2525202%252520refined%2526link%253DSweden%2526region%253Dchrome-header%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'asos-c-name': '@asosteam/asos-web-site-chrome-publisher',
    'asos-c-plat': 'web',
    'asos-c-ver': '13.0.0-b7870ac6-107',
    'asos-cid': '6e6b0d50-03ac-488a-be01-af78f0929c3e',
    'priority': 'u=1, i',
    'referer': 'https://www.asos.com/se/kvinna/nyheter/cat/?cid=27108&page=2',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'geocountry=PL; asos_drmlp=154ded000a5cbd4e9d1d1353b3506712; asos-anon12=019500e22ffc7ec6bbe162aa1fb855b0; asos-ts121=019500e2-2ffc-773a-a7b7-c6518b3facb3; featuresId=7abb4da0-2317-4a81-8c0c-75eb4a36a0a5; AMCVS_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=1; s_cc=true; OptanonAlertBoxClosed=2025-02-13T19:56:29.749Z; eupubconsent-v2=CQMwwLAQMwwLAAcABBENBcF8AP_gAEPAAAYgKiQEAAEgAYADuAHwATYA_QCigImATYApcBeYDLgGjgPrAjZBUMFRAPrgDAB8AH6AiYBeYDLgH1gAAAAA.f_wACHgAAAAA; OTAdditionalConsentString=1~230.318.540.737.1040.1166.1227.1548.1638.1651.1677.1703.1721.1765.1782.1786.1832.1917.1944.1987.2008.2039.2107.2140.2150.2177.2219.2292.2305.2312.2331.2370.2377.2387.2461.2493.2501.2535.2567.2569.2604.2612.2614.2643.2645.2650.2651.2784.2875.2898.2908.2920.3012.3017.3018.3048.3055.3112.3173.3185.3223.3227.3235.3293.3306.3309.3315.3328.3331.3731.8931.9731.13731.16931.27831.31631.32531.33631.34231.34631.36831; plp_columsCount=fourColumns; stc-welcome-message=cappedPageCount=2&resolvedDeliveryCountry=PL&userTookActionOnWelcomeMessage=true; asosAffiliate=affiliateId=17295; PIM-SESSION-ID=CMhiYUKiStN4ISvR; floor=1000; _abck=48DFF4A2007139E96424B6B74A528BE0~0~YAAQBwxAFwqt56OVAQAA0PJWpA21a1OdMMuEpZdIUO/cBU0zFewZLGdFIQncPm6DR8E4hZeAoV+DGkuGeQQsNw/8m+hbZhte0HNxSE0HJn47fnjNFixbZYVQmiJ8fa5kAYYdgb7yWwqh/ASbICA1XYA5PQ948Ek+i6Wi2iLguQTT9javxIW+3Q4/uusi79XIAKOAPORlqeFBCWs7MbbAfuzNzo0ErZR4LBwQoWyN8wwVCf6KJunYGh0s5upq/nZ+mr09/BgDRR/zBZ8DHoQc0psy5ilbLWDrbwlXd0wymyG54puifLDLwQ7ZQYj42iyvsZGThX4RSwgwEfAbN14PTwem7TX0jaIHANSDAI4Zb9imtUuMdPpPXttk3eQ0xT2obsFBJdkCtbNDdaw4GBWpRn1K+OfAn0Np3mkq2wvCEQAkxWShs4satOKQVk/WZlQzwWF/sDReBf7ZXCrVwT/MIeYlwmg9sTBG8e2f1kN3SmCguzGHfkWYoo4=~-1~-1~-1; keyStoreDataversion=4i7nlxk-44; AMCV_C0137F6A52DEAFCC0A490D4C%40AdobeOrg=-1303530583%7CMCMID%7C54027747559069552536811629355504292071%7CMCAID%7CNONE%7CMCOPTOUT-1742226119s%7CNONE%7CvVersion%7C3.3.0; ak_bmsc=A71E1230E876B97E8D5AB730633FC0AF~000000000000000000000000000000~YAAQBwxAF4qt56OVAQAARvRWpBs+fgOCmLP6AYOJ1bj1TQseyD0sQARZTTJo4GZxfsoc67+Mr39MEJ0b99RY7w80OiZ6aR3+0OnLeZAKtEE0VrM23Hudghk4RP9lq0Ld5zWOQKuj/qj/74thvaNEVKqflsSQy4bG4lMHUiRnWJfayGC/+uGFWtPgpZq20g4PyyxJkQRNWffQniwhv/7mYwRioUdGNbfhNRf5vN405698elc9cIS3Vhpsf257N4Yshnq7slci0Mlx2tFyi0xrSC7RYvWt/JpQ4IKZDnDWDx2fmqqC8SJ2wPUx+2AsocLI7fBQ96P8lHTR4zXl9d/ITkAcSZbBJry9LpSsGCxkov76NoN9YOAOZZ5mQwbgzb/ul27iohQnsUlC; asos-b-sdv629=4i7nlxk-44; _s_fpv=true; browseSizeSchema=EU; siteChromeVersion=au=13&com=13&de=13&dk=13&es=13&fr=13&it=13&nl=13&pl=13&roe=13&row=13&ru=13&se=13&us=13; browseCountry=SE; browseCurrency=SEK; storeCode=SE; asos=currencyid=8&currencylabel=SEK&topcatid=1000; currency=8; browseLanguage=sv-SE; bm_sz=DB7DEEDABA88521EA5A44513B3A457DE~YAAQBwxAF8Lg9qOVAQAAtK2KpBvxKNdZwnfCEdc+FOQ/gbX6iuDJgvcAeqQVsHfLz0d1fQDE9S243g5enwK04ZFGajr8z1miJP+RcDDdNINF5LcYbItjIXqUn3VmbYitzAlgZfYKmgvyAB605RcGgPn+7H/CiTC5qhkQlClhhtjy+IMMoDzLHxqWe9ktK98JYwlRMNxqBnol7AJTFsDylzhpWhjKEfB+9etTpCWgsoWawZJHZgAzHO0EggvqlVDsTEtd9ynFhzjfDjIlxa0/1CNcn0gDlmsnJJNWkmC1qVkbwoYHzjEirlQrtkS6MH/BoJkNZLRjJqOFQGhvQoxcR/B5g5A0s9CoCHt6PnuWZ2hAFEXBohX13lYSg7ICUMiDZL2sxq9JS6DAWr0BC8PwACqXazJiid4/g/QGpemdbj2Qg5fqfkzuaP8ZYbMwBt4Vtg/gvB+aq31ARU9Elw3f8bZEdBeADRPPuS47~3228981~3552068; s_pers=%20s_vnum%3D1743454800924%2526vn%253D3%7C1743454800924%3B%20gpv_eVar230%3Dno%2520value%7C1742223659181%3B%20gpv_eVar234%3Dno%2520value%7C1742223659181%3B%20gpv_eVar193%3Dno%2520value%7C1742223659183%3B%20gpv_e198%3Dno%2520value%7C1742223659183%3B%20gpv_p6%3D%2520%7C1742224090702%3B%20eVar225%3D13%7C1742224110152%3B%20visitCount%3D3%7C1742224110152%3B%20gpv_e231%3D4c20be26-3467-4d5c-8740-c8ca5f2bd801%7C1742224112310%3B%20s_invisit%3Dtrue%7C1742224112321%3B%20s_nr%3D1742222312327-Repeat%7C1773758312327%3B%20gpv_e47%3Dno%2520value%7C1742224112327%3B%20gpv_p10%3Ddesktop%2520se%257Ccategory%2520page%257C27108%2520page%25202%2520refined%7C1742224112333%3B; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+17+2025+16%3A38%3A33+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=2a09491c-237c-4209-94b4-ef42c7c508e6&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0001%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=PL%3B14&AwaitingReconsent=false; s_sq=asoscomprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddesktop%252520se%25257Ccategory%252520page%25257C27108%252520page%2525202%252520refined%2526link%253DSweden%2526region%253Dchrome-header%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}
item_params = {
    'browseCountry': 'AT',
    'browseCurrency': 'EUR',

}
countries = 'Austria, Belgium, Bulgaria, Croatia, Republic of Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden'.split(',')
countries.extend(['United States', 'United Kingdom'])
COUNTRY_CODES = {
    'Austria': 'AT', 'Belgium': 'BE', 'Bulgaria': 'BG', 'Croatia': 'HR',
    'Republic of Cyprus': 'CY', 'Czech Republic': 'CZ', 'Denmark': 'DK', 'Estonia': 'EE',
    'Finland': 'FI', 'France': 'FR', 'Germany': 'DE', 'Greece': 'GR', 'Hungary': 'HU',
    'Ireland': 'IE', 'Italy': 'IT', 'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU',
    'Malta': 'MT', 'Netherlands': 'NL', 'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO',
    'Slovakia': 'SK', 'Slovenia': 'SI', 'Spain': 'ES', 'Sweden': 'SE', 'United States': 'US',
    'United Kingdom': 'GB'
}
CODE_TO_COUNTRY = {code: country for country, code in COUNTRY_CODES.items()}

COUNTRY_CODES_LIST = list(COUNTRY_CODES.values())
stores_params = []
async def get_stores():
    params = {
        'keyStoreDataversion': '4i7nlxk-44',
        'lang': 'en-US',
        'platform': 'desktop',
    }

    response = requests.get(
        'https://www.asos.com/api/web/countrymetadata/v1/countrySelector/US',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    for country in response.json()['data']['countries']:
        if country['countryCode'] in COUNTRY_CODES_LIST:
            r = requests.get(
                f'https://www.asos.com/api/web/countrymetadata/v1/countrySelector/{country["countryCode"]}',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            p_data = r.json()['data']
            cookies['browseLanguage'] = p_data['lang'].split('-')[-1].lower()
            cookies['storeCode'] = p_data['storeCode']
            cookies['browseCountry'] = p_data['countryCode']
            cookies['browseCurrency'] =  p_data['currencies'][0]['currency']
            cookies['currency'] = str(p_data['currencies'][0]['currencyId'])
            item_params['browseCountry'] = p_data['countryCode']
            item_params['browseCurrency'] = p_data['currencies'][0]['currency']
            yield {
                'offset' : 0,
                'lang' : p_data['lang'],
                'currency' : p_data['currencies'][0]['currency'],
                'country' : p_data['countryCode'],
                'store' : p_data['storeCode'],
                'keyStoreDataversion': '4i7nlxk-44',
                'limit': '100',
            }

cats = [24920, 25278]

def split_materials(html_string):
    return re.split(r'<br\s*/?>\s*<br\s*/?>', html_string)
def get_page_count(cat_id, params):

    response = requests.get(
        f'https://www.asos.com/api/product/search/v2/categories/{cat_id}',
        params=params,
    )
    return math.ceil(response.json()["itemCount"] / 100)

base_url = 'https://www.asos.com/'
links = []
bad_links = []
def transofm_link(url):
    match = re.search(r'productId-(\d+)', url)
    if match:
        product_id = match.group(1)
        part_link = url.split('/')[:-1]
        part_link.append(product_id)
    try:
        return '/'.join(part_link).replace('grp', 'prd')
    except:
        return None
def get_links(cat_id, start_page, end_page, params):
    for page in range(start_page, end_page + 1):
        params['offset'] = f'{page * 100}'
        try:
            response = requests.get(
                f'https://www.asos.com/api/product/search/v2/categories/{cat_id}',
                params=params,
                headers=headers, 
                cookies=cookies
            )
        except:
            sleep(0.5)
            response = requests.get(
                f'https://www.asos.com/api/product/search/v2/categories/{cat_id}',
                params=params,
                headers=headers, 
                cookies=cookies
            )
        if response.status_code != 200:
            while response.status_code != 200:
                sleep(0.2)
                response = requests.get(
                    f'https://www.asos.com/api/product/search/v2/categories/{cat_id}',
                    params=params,
                    headers=headers, 
                    cookies=cookies
                )
        for i in response.json().get('products', []):
            for clothing in clothing_items:

                if clothing in i['name']:
                    part_url = transofm_link(i["url"]) if 'grp' in i['url'] else i['url']
                    if part_url:                            
                        links.append(f'https://www.asos.com/{cookies["storeCode"].lower()}/{part_url}')

data = []
def get_data(links):
    for url in links:
        r = requests.get(url, headers=headers, cookies=cookies, params=item_params)
        # print(r)
        if r.status_code == 404 or r.status_code == 410:
            continue
        if r.status_code != 200:
            while r.status_code != 200:
                sleep(0.1)
                try:
                    r = requests.get(url, headers=headers, cookies=cookies, params=item_params)
                except:
                    sleep(1)
                    try:
                        r = requests.get(url, headers=headers, cookies=cookies, params=item_params)
                    except:
                        continue
        print(r)
        soup = BeautifulSoup(r.text, 'lxml')
        country_code = soup.find('html').get('data-country-code').upper()
        country = CODE_TO_COUNTRY[country_code]
        scripts = soup.find_all('script', type="text/javascript")
        if len(scripts) > 1:
            j_data = scripts[1].text
            pattern = r"window\.asos\.pdp\.config\.stockPriceResponse\s*=\s*'([^']+)';"
            match = re.search(pattern, j_data)
            if match:
                try:
                    price_data = json.loads(match.group(1))[0]["productPrice"]
                except:
                    continue
                price = price_data['current']['value']
                currency = price_data['currency']
            else:
                price = None
                currency = None
            pattern = r"window\.asos\.pdp\.config\.product\s*=\s*({.*?});"
            match = re.search(pattern, j_data)
            if match:
                product_json_str = match.group(1)
                product_data = json.loads(product_json_str)
                name = product_data['name']
                gender = soup.find('html').get('data-gender')
                brand = product_data['brandName']
                images = '\n'.join([i['url'] for i in product_data['images']])
                try:
                    color = product_data['images'][0]['colour']
                except:
                    color = product_data['images'][1]['colour']
                try:
                    product_type = product_data['productType']['name']
                except:
                    print(url)
            if color.lower() not in original_colors:
                continue
            pattern = r"window\.asos\.pdp\.config\.productDescription\s*=\s*({.*?});"
            match = re.search(pattern, j_data)
            if match:
                materials = json.loads(match.group(1))['aboutMe']
            else:

                continue
            if not materials:
                data.append([url, price, currency, name, gender,brand,images,product_type,'Unable to find materials', color])
                continue
            materials_to_check = materials.lower()

            is_plastic = False
            for material in synthetic_fabrics:
                if material in materials_to_check:
                    is_plastic = True
                    break
            if not is_plastic:
                materials = split_materials(materials)
                try:
                    clothe_desc, materials = materials[0], materials[1]
                except:
                    clothe_desc, materials = materials[0], ''
                data.append([url, price, currency, name, gender,brand,images,product_type,clothe_desc,materials, color, country_code, country])


def save(data):
    cols = 'url, price, currency, name, gender,brand,images,product_type,clothe_desc,materials,color,country code, country'.split(',')
    df = pd.DataFrame(data=data, columns=cols)
    df.to_csv('asos.csv', encoding='utf-8', index=False)
    df.to_excel('asos.xlsx', index=False)


async def main():
    global links

    async for param in get_stores():
        for cat in cats:
            page_count = get_page_count(cat, param)
            print(f'{page_count} - pages')
            num_threads = 12
            threads = []
            batch_size = page_count // num_threads

            for i in range(num_threads):
                start = i * batch_size
                end = start + batch_size if i < num_threads - 1 else page_count
                t = Thread(target=get_links, args=(cat, start, end, param))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

    links = list(dict.fromkeys(links))
    num_threads = 12
    threads = []
    batch_size = len(links) // num_threads
    for i in range(num_threads):
        start = i * batch_size 
        end = start + batch_size if i < num_threads - 1 else len(links)
        t = Thread(target=get_data, args=(links[start:end], ))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    links.clear()

    save(data)
    input('Scrapping done press ENTER to continue')


if __name__ == '__main__':
    asyncio.run(main())