#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: pubmed.py
Usage: DataFile Parse Module For MEDLINE Format of PubMed

PMID- 33465792
OWN - NLM
STAT- Publisher
LR  - 20210119
IS  - 1806-9339 (Electronic)
IS  - 0100-7203 (Linking)
DP  - 2021 Jan 19
TI  - Switching of Hormone Therapies in Breast Cancer Women.
LID - 10.1055/s-0040-1719149 [doi]
AB  - OBJECTIVE:  The objective of the present study was to analyze the reasons that led 
      to hormone therapies (HTs) regimen changes in women with breast cancer. METHODS: 
       This was a retrospective cross-sectional study from a single-institution Brazilian 
      cancer center with patient records diagnosed with breast cancer between January 2012 
      and January 2017. RESULTS:  From 1,555 women who were in treatment with HT, 213 
      (13.7%) women had HT switched, either tamoxifen to anastrozole or vice-versa. Most 
      women included in the present study who switched HT were > 50 years old, 
      postmenopausal, Caucasian, and had at least one comorbidity. From the group with 
      therapy change, 'disease progression' was reason of change in 124 (58.2%) cases, and 
      in 65 (30.5%) patients, 'presence of side effects' was the reason. From those women 
      who suffered with side effects, 24 (36.9%) had comorbidities. CONCLUSION:  The 
      present study demonstrated a low rate of HT switch of tamoxifen to anastrozole. 
      Among the reasons for changing therapy, the most common was disease progression, 
      which includes cancer recurrence, metastasis or increased tumor. Side effects were 
      second; furthermore, age and comorbidities are risk factors for side effects.
CI  - Federação Brasileira de Ginecologia e Obstetrícia. This is an open access article 
      published by Thieme under the terms of the Creative Commons Attribution License, 
      permitting unrestricted use, distribution, and reproduction so long as the original 
      work is properly cited. (https://creativecommons.org/licenses/by/4.0/).
FAU - de Medeiros, Luana Moreira
AU  - de Medeiros LM
AUID- ORCID: 0000-0002-3770-1404
AD  - Faculty of Pharmaceutical Sciences, Universidade de Campinas (Unicamp), Campinas, 
      SP, Brazil.
FAU - Stahlschmidt, Rebeca
AU  - Stahlschmidt R
AUID- ORCID: 0000-0003-3429-584X
AD  - Graduate Program in Medical Sciences, Faculty of Medical Sciences, Universidade de 
      Campinas (Unicamp), Campinas, SP, Brazil.
FAU - Ferracini, Amanda Canato
AU  - Ferracini AC
AUID- ORCID: 0000-0002-9626-5227
AD  - Graduate Program in Medical Sciences, Faculty of Medical Sciences, Universidade de 
      Campinas (Unicamp), Campinas, SP, Brazil.
FAU - de Souza, Cinthia Madeira
AU  - de Souza CM
AUID- ORCID: 0000-0001-5606-9144
AD  - Graduate Program in Medical Sciences, Faculty of Medical Sciences, Universidade de 
      Campinas (Unicamp), Campinas, SP, Brazil.
FAU - Juliato, Cassia Raquel Teatin
AU  - Juliato CRT
AUID- ORCID: 0000-0003-3197-1195
AD  - Department of Obstetrics and Gynecology, Faculty of Medical Sciences, Universidade 
      de Campinas (Unicamp), Campinas, SP, Brazil.
FAU - Mazzola, Priscila Gava
AU  - Mazzola PG
AUID- ORCID: 0000-0002-3795-8189
AD  - Faculty of Pharmaceutical Sciences, Universidade de Campinas (Unicamp), Campinas, 
      SP, Brazil.
LA  - eng
PT  - Journal Article
TT  - Avaliação da mudança do esquema hormonioterápico em mulheres com câncer de mama.
DEP - 20210119
PL  - Brazil
TA  - Rev Bras Ginecol Obstet
JT  - Revista brasileira de ginecologia e obstetricia : revista da Federacao Brasileira 
      das Sociedades de Ginecologia e Obstetricia
JID - 9214757
SB  - IM
COIS- The authors have no conflict of interests to declare.
EDAT- 2021/01/20 06:00
MHDA- 2021/01/20 06:00
CRDT- 2021/01/19 20:15
PHST- 2021/01/19 20:15 [entrez]
PHST- 2021/01/20 06:00 [pubmed]
PHST- 2021/01/20 06:00 [medline]
AID - 10.1055/s-0040-1719149 [doi]
PST - aheadofprint
SO  - Rev Bras Ginecol Obstet. 2021 Jan 19. doi: 10.1055/s-0040-1719149.
"""


class PubmedItem:
    """PubMed MEDLINE Data Format.
    MEDLINE®/PubMed® Data Element (Field) Descriptions
    https://www.nlm.nih.gov/bsd/mms/medlineelements.html
    """

    def __init__(self):
        self.database = 'PUBMED'


def getdata(filepath):
    """Return Data From File By MEDLINE Format Parser.
    Normal: Return Data Type List
    Error:  Return -1
    """
    data = _parsefile(filepath) if checktype(filepath) else -1
    data = _fixdata(data) if data != -1 else data
    return data


def checktype(filepath):
    """Check PubMed MEDLINE Format."""
    with open(filepath, encoding='utf-8') as datafile:
        return datafile.readline()[:4] == 'PMID'


def _parsefile(filepath):
    """Parse Exported File From Pubmed in MEDLINE format."""
    data = []
    lastfield = ''
    pubmeditem = ''
    with open(filepath, encoding='utf-8') as datafile:
        for line in datafile:
            if line != '\n':
                if line[:4] == 'PMID':
                    pubmeditem = PubmedItem()
                    data.append(pubmeditem)
                    text = line[6:].strip()
                    setattr(pubmeditem, 'PMID', text)
                else:
                    field = line[:4].strip()
                    text = line[6:].strip()
                    if field:
                        content = getattr(pubmeditem, field, '')
                        if content:
                            if isinstance(content, str):
                                content = [content]
                            content.append(text)
                            setattr(pubmeditem, field, content)
                        else:
                            setattr(pubmeditem, field, text)
                        lastfield = field
                    else:
                        content = getattr(pubmeditem, lastfield)
                        if isinstance(content, str):
                            content = ' '.join([content, text])
                        else:
                            content[-1] = ' '.join([content[-1], text])
                        setattr(pubmeditem, lastfield, content)
    return data


def _fixdata(data):
    """Data Preparation."""
    # Change str to list format

    listfield = set(['AU', 'FAU', 'AUID', 'AD', 'OT'])

    for pubmeditem in data:

        # Change field to list
        for key in pubmeditem.__dict__.keys():
            if key in listfield:
                item = getattr(pubmeditem, key, '')
                if item:
                    if isinstance(item, str):
                        setattr(pubmeditem, key, [item])

                        # todo fixe lastname ?
                        # if item.database == 'pubmed':
                        #     firstname = author.split(' ')[0]
                        #     lastname = author.split(' ')[1]
                        #     fix_lastname = ''
                        #     for c in lastname:
                        #         fix_lastname += c + '. '
                        #     author = ', '.join([firstname, fix_lastname])

    return data


if __name__ == '__main__':
    filepath = './mrhpkg/filters/demo_pubmed_202101.nbib'
    data = getdata(filepath)
    for pubmeditem in data:
        print(getattr(pubmeditem, 'OT', ''))
