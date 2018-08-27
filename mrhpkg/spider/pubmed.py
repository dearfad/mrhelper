#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: pubmed.py
Usage: PMC Spider For Citation Network
Reference: https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
"""

import requests
from bs4 import BeautifulSoup
from requests import adapters


def getdata(pmid, api_key=None, time_out=1, retries=1, proxies=None):
    if not pmid:
        return {'cr': -1, 'cs': -1}
    result = {'cr': [], 'cs': []}
    linknames = {'cr': 'pubmed_pubmed_refs', 'cs': 'pubmed_pubmed_citedin'}
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?'
    retry = adapters.HTTPAdapter(max_retries=retries)
    for key in linknames:
        payload = {'dbfrom': 'pubmed', 'linkname': linknames[key], 'id': pmid, 'api_key': api_key}
        pubmed = requests.Session()
        pubmed.mount('http://', retry)
        pubmed.mount('https://', retry)
        try:
            page = pubmed.get(url, params=payload, timeout=time_out, proxies=proxies)
            page.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            result[key] = -1
            continue
        if page.status_code == requests.codes.ok:
            soup = BeautifulSoup(page.content, 'lxml')
            data = []
            for item in soup.find_all('id'):
                if item.get_text() != pmid:
                    data.append(item.get_text())
            result[key] = data
        else:
            result[key] = -1
    return result


def main():
    pmid = '13129273'
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }
    result = getdata(pmid, proxies=proxies)

    print(result)


if __name__ == '__main__':
    main()
