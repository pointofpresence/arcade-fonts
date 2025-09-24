# pylint: disable=missing-module-docstring
# pylint: disable=wrong-import-order
# pylint: disable=import-error
# pylint: disable=line-too-long

from random import randint
from time import sleep

import requests

import json
from fonts import FONTS


def json_to_ttf_via_web(json_path, ttf_path):
    """ Reads JSON font, extracts glyphs and letterspace, sends to pentacom and saves as TTF. """

    with open(json_path, 'r', encoding='utf-8') as f_handle:
        full_data = json.load(f_handle)

    # We filter only numerical keys (character codes)
    glyph_data = {
        k: v for k, v in full_data.items()
        if k.isdigit()
    }

    data = {
        'data': json.dumps(glyph_data),
        'letterspace': str(full_data.get("letterspace", 64)),
        'monospace': '0',
        'monospacewidth': '14',
        'name': full_data.get('name', ''),
        'copy': full_data.get('copy', ''),
        'mobile': '0',
        'inspect': '0',
        'ascender': '',
        'descender': '',
        'linegap': '',
        'wordspacing': '',
        'optionalparams': '',
        'token': '_token_'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.pentacom.jp',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.pentacom.jp/pentacom/bitfontmaker2/',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    }

    response = requests.post(
            'https://www.pentacom.jp/pentacom/bitfontmaker2/makes.php',
            headers=headers,
            data=data
    )

    if response.status_code == 200:
        with open(ttf_path, 'wb') as f_handle:
            f_handle.write(response.content)

        print(f"TTF saved to {ttf_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    for idx, font in enumerate(FONTS):
        if not font.get('build', False):
            print(f"Skipping {font['name']}")
            continue

        if idx != 0:
            sleep(randint(5, 15))

        input_json_path = f"json/{font['output']}"
        output_ttf_path = f"ttf/{font['output'].split('.')[0]}.ttf"

        json_to_ttf_via_web(input_json_path, output_ttf_path)
