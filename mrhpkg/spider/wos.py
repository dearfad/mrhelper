#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: wos.py
Usage: WOS Spider For Reference Webpage
Reference: https://apps.webofknowledge.com
"""

import requests
from bs4 import BeautifulSoup
from requests import adapters


def _getsid(page):

    if not page:
        return -1

    sid = ''

    soup = BeautifulSoup(page, 'lxml')

    for item in soup.find_all('input'):
        if item.get('type') == 'hidden' and item.get('name') == 'SID':
            sid = item.get('value')
            return sid

    return sid


def getdata(title, time_out=1, retries=1, proxies=None):

    webpage = ''

    link = 'https://apps.webofknowledge.com'

    retry = adapters.HTTPAdapter(max_retries=retries)
    wos = requests.Session()
    wos.mount('http://', retry)
    wos.mount('https://', retry)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

    try:
        page = wos.get(link, timeout=time_out,
                       proxies=proxies, headers=headers)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        webpage = page.text
    else:
        return 0

    sid = _getsid(webpage)

    cookies = page.cookies

    formdata = {
        'fieldCount': 1,
        'action': 'search',
        'product': 'WOS',
        'search_mode': 'GeneralSearch',
        'SID': sid,
        'max_field_count': 25,
        'max_field_notice': '注意: 无法添加另一字段。',
        'input_invalid_notice': '检索错误: 请输入检索词。',
        'exp_notice': '检索错误: 专利检索词可以在多个家族中找到 (',
        'input_invalid_notice_limits':  '<br/>注意: 滚动框中显示的字段必须至少与一个其他检索字段相组配。',
        'sa_params': 'WOS||'+sid+"|https://apps.webofknowledge.com:443|'",
        'formUpdated': 'true',
        'value(input1)': title,
        'value(select1)': 'TI',
        'value(hidInput1)': '',
        'limitStatus': 'expanded',
        'ss_lemmatization': 'On',
        'ss_spellchecking': 'Suggest',
        'SinceLastVisit_UTC': '',
        'SinceLastVisit_DATE': '',
        'period': 'Range Selection',
        'range': 'ALL',
        'startYear': '1900',
        'endYear': '2021',
        'editions': 'SCI',
        'editions': 'SSCI',
        'editions': 'AHCI',
        'editions': 'ISTP',
        'editions': 'ESCI',
        'editions': 'CCR',
        'editions': 'IC',
        'update_back2search_link_param': 'yes',
        'ssStatus': 'display:none',
        'ss_showsuggestions': 'ON',
        'ss_numDefaultGeneralSearchFields': 1,
        'ss_query_language': '',
        'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
    }

    # retry = adapters.HTTPAdapter(max_retries=retries)
    # wos = requests.Session()
    # wos.mount('http://', retry)
    # wos.mount('https://', retry)



    headers = {
        'origin': 'https://apps.webofknowledge.com',
        'referer': 'https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&SID='+ sid + '&search_mode=GeneralSearch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

    url = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'

    try:
        page = wos.post(url, timeout=time_out, proxies=proxies, headers=headers, data=formdata, cookies=cookies)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        result = page.text
    else:
        result = 0

    if result:
        soup = BeautifulSoup(result, 'lxml')

        for item in soup.find_all('a'):
            link = item.get('href')
            if link:
                if 'full_record.do' in link:
                    webpage = 'https://apps.webofknowledge.com' + link
                    # print(webpage)
                    return webpage
    return webpage


def main():
    title = 'Role of Rubia tinctorum in the synthesis of zinc oxide nanoparticles and apoptosis induction in breast cancer cell line'
    data = getdata(title)
    print(data)


if __name__ == '__main__':
    main()
