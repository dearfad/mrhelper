#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: cnki.py
# Usage: CNKI Spider For Citation Network
# 中国博士学位论文全文数据库 CDFD 中国优秀硕士学位论文全文数据库 CMFD
# 中国学术期刊网络出版总库 CJFQ 外文题录数据库 CRLDENG
# 国际期刊数据库 SSJD 中国重要会议论文全文数据库 CPFD
###############################################################
# Something wrong in cnki crldeng
# pagecount_eng = pagecount_eng if pagecount_eng < 10 else 10
###############################################################
import ast

import requests
from bs4 import BeautifulSoup
from requests import adapters


def getpage(link, time_out=1, retries=1, proxies=None):
    if link:
        link = link.lower()
    else:
        return 0
    retry = adapters.HTTPAdapter(max_retries=retries)
    cnki = requests.Session()
    cnki.mount('http://', retry)
    cnki.mount('https://', retry)
    try:
        page = cnki.get(link, timeout=time_out, proxies=proxies)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        result = page.text
    else:
        result = 0
    return result


def getdata(link, time_out=1, retries=1, proxies=None):
    if link:
        link = link.lower()
    else:
        return {'cr': -1, 'cs': -1}
    result = {'cr': [], 'cs': []}
    reftypes = {'cr': 1, 'cs': 3}
    databases = ['CJFQ', 'SSJD', 'CRLDENG', 'CMFD', 'CPFD', 'CDFD']
    retry = requests.adapters.HTTPAdapter(max_retries=retries)
    url = 'http://kns.cnki.net/kcms/detail/frame/list.aspx'
    templink = link.split('&dbname=')
    dbname = templink[1]
    dbcode = dbname[0:4]
    filename = templink[0].split('filename=')[1]
    for reftype in reftypes:
        cnki = requests.Session()
        cnki.mount('http://', retry)
        cnki.mount('https://', retry)
        payload = {'dbcode': dbcode, 'filename': filename, 'dbname': dbname, 'RefType': reftypes[reftype], 'vl': ''}
        try:
            page = cnki.get(url, params=payload, timeout=time_out, proxies=proxies)
            page.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            result[reftype] = -1
            continue
        if page.status_code == requests.codes.ok:
            result[reftype].append(page.text)
            soup = BeautifulSoup(result[reftype][0], 'lxml')
            for item in soup.find_all('span'):
                for database in databases:
                    total = {}
                    count = {}
                    dbid = 'pc_' + database
                    if item.get('name') == 'pcount' and item.get('id') == dbid:
                        total[database] = int(item.get_text())
                        if total[database] % 10 > 0:
                            count[database] = total[database] // 10 + 1
                        else:
                            count[database] = total[database] // 10
                    if count.setdefault(database):
                        for page in range(2, count[database] + 1):
                            payload['CurDBCode'] = database
                            payload['page'] = page
                            try:
                                refpage = cnki.get(url, params=payload, timeout=time_out, proxies=proxies)
                                refpage.raise_for_status()
                            except requests.exceptions.RequestException as error:
                                print(error)
                                result[reftype] = -1
                                return result
                            if refpage.status_code == requests.codes.ok:
                                result[reftype].append(refpage.text)
                            else:
                                result[reftype] = -1

        else:
            result[reftype] = -1

    return result


def getcount(link, time_out=1, retries=1, proxies=None):
    if link:
        link = link.lower()
    else:
        return 0
    retry = requests.adapters.HTTPAdapter(max_retries=retries)
    cnki = requests.Session()
    cnki.mount('http://', retry)
    cnki.mount('https://', retry)
    url = 'http://kns.cnki.net/kcms/detail/block/refcount.aspx'
    templink = link.split('&dbname=')
    dbcode = templink[1][0:4]
    filename = templink[0].split('filename=')[1]
    querydict = {'dbcode': dbcode, 'filename': filename, 'vl': ''}
    try:
        page = cnki.get(url, params=querydict, timeout=time_out, proxies=proxies)
        page.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        return 0
    if page.status_code == requests.codes.ok:
        result = ast.literal_eval(page.text)
    else:
        result = 0
    return result


def main():
    link = 'http://kns.cnki.net/KCMS/detail/detail.aspx?filename=LCMZ201205031&dbname=CJFD2012'
    page = getpage(link)
    data = getdata(link)
    count = getcount(link)
    print(page, data, count)


if __name__ == '__main__':
    main()
