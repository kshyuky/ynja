import requests
import json
import pickle

def search(date_start, date_end, page, limit):
    hotel_list = []
    url = "https://www.yanolja.com/api/v1/contents/search"
    payload={}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'cgntId=ap-northeast-2%3Ac8efb93e-a30b-4f22-8b2e-09590fab1254; yanolja_sid=s%3AdwsIgv3od9VjJfx5_e2jELoFtsPJSrcw.NcKx%2FbhuqVtsjEXPylWp%2Bg%2FZUVSpfRVugGmg%2BqoHX6E; _gcl_au=1.1.28593903.1645502893; ACEUACS=1645502893475181365; ACEFCID=UID-621461ADED57E94B183591E2; ACEUCI=1; _fbp=fb.1.1645502893611.261173520; _ga=GA1.2.107073480.1645502894; _gid=GA1.2.1288083050.1645502894; _gat=1; location={%22latitude%22:%2237.50681%22%2C%22longitude%22:%22127.06624%22%2C%22address%22:%22%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC%20%ED%85%8C%ED%97%A4%EB%9E%80%EB%A1%9C108%EA%B8%B8%2042%22%2C%22addressShort%22:%22%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B0%95%EB%82%A8%EA%B5%AC%20%ED%85%8C%ED%97%A4%EB%9E%80%EB%A1%9C108%EA%B8%B8%22%2C%22addressOnlyRoad%22:%22%ED%85%8C%ED%97%A4%EB%9E%80%EB%A1%9C108%EA%B8%B8%22}; SavedFiltersKey=/hotel/r-900590/hkey-hotel; wcs_bt=ae93a192ec48a4:1645502952; _AceT=fb.1.1645502893611.261173520; yanolja_sid=s%3AtRMz4bvWEdfP9ZYyWRZL2731gA9dJvFg.%2Bu%2FGmAkrSszbEcqwWGBwYjyIGejGxsnWGcFA%2FnQLZes',
        'Host': 'www.yanolja.com',
        'Referer': 'https://www.yanolja.com/hotel/r-900590/hkey-hotel?advert=AREA&rentType=1&stayType=1&placeListType=hotel&pathDivision=r-900590&pathDivisionCuts=hkey-hotel',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    parmas = "advert=AREA&capacityAdult=2&capacityChild=0&checkinDate="+date_start+"&checkoutDate="+date_end+\
             "&hotel=1&lat=37.50681&lng=127.06624&page="+str(page)+"&region=900590&rentType=1&limit="+str(limit)+"&searchType=hotel&sort=106&stayType=1&themes=&coupon=&excludeSoldout=&includeRent=&includeStay="
    url_parmas = "{}?{}".format(url, parmas)
    response = requests.request("GET", url_parmas, headers=headers, data=payload)
    # print(response.json())
    return response.json()

def get_list(date_start="2022-02-26", date_end="2022-03-01"):
    hotel_list = []
    page = 1
    limit = 20
    res_dict = search(date_start="2022-02-26", date_end="2022-03-01", page=page, limit=limit)
    hotel_list += res_dict["motels"]["lists"]
    # counts = res_dict["motels"]["counts"]
    total_cnt = res_dict["motels"]["totalCounts"]
    repeat = int(total_cnt-1/limit) if total_cnt>0 else 0
    for page in range(repeat+1):
        res_dict = search(date_start="2022-02-26", date_end="2022-03-01", page=page, limit=limit)
        hotel_list += res_dict["motels"]["lists"]
    # print(hotel_list)
    return hotel_list


def parser(hotel_list):
    # print(hotel_list)
    # counts = res_dict["motels"]["counts"]
    # total_cnt = res_dict["motels"]["totalCounts"]
    # lists = res_dict["motels"]["lists"]
    # print(counts, total_cnt)
    # for idx, item in enumerate(res_dict["motels"]["lists"]):
    for idx, item in enumerate(hotel_list):
        name = item["title"]
        dayuse_info, dayuse_price, night_info, night_price = None, None, None, None
        for priceinfo in item["displayPrices"]:
            if priceinfo["label"] == "대실":
                dayuse_info = priceinfo["extraInfo"]
                dayuse_price = priceinfo["rawDiscountPrice"]
            elif priceinfo["label"] == "숙박":
                night_info = priceinfo["extraInfo"]
                night_price = priceinfo["rawDiscountPrice"]
            elif priceinfo["label"] == "연박":
                night_info = priceinfo["extraInfo"]
                night_price = priceinfo["rawDiscountPrice"]
            else:
                raise Exception("Unexpected label:{}".format(priceinfo["label"]))
        print(idx, name, dayuse_info, dayuse_price, night_info, night_price)

    return

if __name__ == "__main__":
    if 0:
        pkl_data = search(page=2, limit=100)
        with open("./search.pkl", "wb") as f:
            pickle.dump(pkl_data, f)

    if 0:
        pkl_data = get_list()
        with open("./get_list.pkl", "wb") as f:
            pickle.dump(pkl_data, f)

    if 1:
        with open("./get_list.pkl", "rb") as f:
            pkl_data = pickle.load(f)
        parser(pkl_data)
