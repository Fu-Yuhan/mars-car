import base64
import json

import requests


API_KEY = "a2aIVOHjRudd2CVQB4UZFKzj"
SECRET_KEY = "1y3BmLoqYcaSetoritDsNjKTrNHBA1jy"


def find_obj(image:str):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/multi_object_detect?access_token=" + get_access_token()

    payload = {
        "image":image
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.content)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    with open("514.jpg","rb") as f:
        image_content = f.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        results = find_obj(image_base64)
        print(results)
        biggest = {'location': {'height': 0, 'left': 0, 'top': 0, 'width': 0}, 'name': None, 'score': 0}
    for result in results['result']:
        if result['location']['height']*result['location']['width'] >= biggest['location']['height']*biggest['location']['width']:
            biggest = result

    middle = biggest['location']['left'] + biggest['location']['width']
    if middle <= 499/2:
        print("left")
    else:
        print("right")

