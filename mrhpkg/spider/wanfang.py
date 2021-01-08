#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: wanfang.py
# Usage: Wanfang Spider For Citation Network

import requests
from requests import adapters


def getmetrics(wfid, time_out=1, retries=1, proxies=None):
    if not wfid:
        return 0
    retry = adapters.HTTPAdapter(max_retries=retries)
    url = 'http://d.wanfangdata.com.cn/Detail/Periodical/'
    payload = {'Id': wfid}
    wanfang = requests.Session()
    wanfang.mount('http://', retry)
    try:
        page = wanfang.post(url, params=payload, timeout=time_out, proxies=proxies)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        result = page.json()
    else:
        result = 0
    return result


def getdata(wfid, time_out=1, retries=1, proxies=None):
    if not wfid:
        return {'cr': -1, 'cs': -1}
    result = {'cr': [[], 0], 'cs': [[], 0]}
    types = {'cr': 'Reference', 'cs': 'Quotation'}
    retry = requests.adapters.HTTPAdapter(max_retries=retries)
    url = 'http://d.wanfangdata.com.cn/Detail/Reference'
    pagecount = 1
    for key in types:
        pagenumber = 1
        while pagenumber:
            wanfang = requests.Session()
            wanfang.mount('http://', retry)
            payload = {'Id': wfid, 'ReferenceType': types[key], 'PageNum': pagenumber}
            try:
                page = wanfang.post(url, params=payload, timeout=time_out, proxies=proxies)
                page.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(error)
                result[key] = -1
                continue
            if page.status_code == requests.codes.ok:
                if pagenumber == 1:
                    result[key][1] = page.json()['total']
                    pagecount = result[key][1] // 10 + 1 if result[key][1] % 10 > 0 else result[key][1] // 10
                result[key][0] += [item['neo4j'] for item in page.json()['detail']]
                pagenumber += 1
                if pagenumber > pagecount:
                    pagenumber = 0
            else:
                result[key] = -1
    return result


def getpage(wfid, time_out=1, retries=1, proxies=None):
    if not wfid:
        return 0
    retry = requests.adapters.HTTPAdapter(max_retries=retries)
    url = 'http://d.wanfangdata.com.cn/periodical/' + wfid
    payload = {}
    wanfang = requests.Session()
    wanfang.mount('http://', retry)
    wanfang.mount('https://', retry)
    try:
        page = wanfang.post(url, params=payload, timeout=time_out, proxies=proxies)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        result = page.text
    else:
        result = 0
    return result


def main():
    wfid = 'gwyx-hlxfc200501027'
    # page = getpage(wfid)
    data = getdata(wfid)
    # metrics = getmetrics(wfid)
    # print('文献阅读：', metrics['detail'][0]['periodical']['MetadataViewCount'])
    # print('下载：', metrics['detail'][0]['periodical']['DownloadCount'])
    # print('第三方链接：', metrics['detail'][0]['periodical']['ThirdpartyLinkClickCount'])
    # print('被引：', metrics['detail'][0]['periodical']['CitedCount'])
    print(data['cr'][0][0].keys())


if __name__ == '__main__':
    main()
