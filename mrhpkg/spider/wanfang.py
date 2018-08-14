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
    url = 'http://www.wanfangdata.com.cn/search/wfmetrics.do?id='
    payload = {'id': wfid, 'type': 'perio'}
    wanfang = requests.Session()
    wanfang.mount('http://', retry)
    try:
        page = wanfang.get(url, params=payload, timeout=time_out, proxies=proxies)
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
    types = {'cr': 'reference', 'cs': 'citaition'}
    retry = requests.adapters.HTTPAdapter(max_retries=retries)
    url = 'http://www.wanfangdata.com.cn/graphical/turnpage.do?'
    pagecount = 1
    for key in types:
        pagenumber = 1
        while pagenumber:
            wanfang = requests.Session()
            wanfang.mount('http://', retry)
            payload = {'type': types[key], 'id': wfid, 'number': pagenumber}
            try:
                page = wanfang.get(url, params=payload, timeout=time_out, proxies=proxies)
                page.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(error)
                result[key] = -1
                continue
            if page.status_code == requests.codes.ok:
                if pagenumber == 1:
                    result[key][1] = page.json()[1]
                    pagecount = result[key][1] // 10 + 1 if result[key][1] % 10 > 0 else result[key][1] // 10
                result[key][0] += page.json()[0]
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
    url = 'http://www.wanfangdata.com.cn/details/detail.do?'
    payload = {'_type': 'perio', 'id': wfid}
    wanfang = requests.Session()
    wanfang.mount('http://', retry)
    wanfang.mount('https://', retry)
    try:
        page = wanfang.get(url, params=payload, timeout=time_out, proxies=proxies)
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
    wfid = 'xljsyyy201604007'
    page = getpage(wfid)
    data = getdata(wfid)
    metrics = getmetrics(wfid)
    print(page, data, metrics)


if __name__ == '__main__':
    main()
