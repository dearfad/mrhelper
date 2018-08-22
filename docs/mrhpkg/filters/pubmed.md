# [PUBMED](https://www.ncbi.nlm.nih.gov/pubmed/)

---

* **解析文件**：./mrhpkg/filters/pubmed.py
* **默认格式**：MEDLINE

## **MEDLINE**

??? example "范例"

    ```text
    PMID- 29447299
    OWN - NLM
    STAT- In-Data-Review
    LR  - 20180215
    IS  - 1932-6203 (Electronic)
    IS  - 1932-6203 (Linking)
    VI  - 13
    IP  - 2
    DP  - 2018
    TI  - Effects of breast stimulation for spontaneous onset of labor on salivary oxytocin
        levels in low-risk pregnant women: A feasibility study.
    PG  - e0192757
    LID - 10.1371/journal.pone.0192757 [doi]
    AB  - OBJECTIVES: This preliminary study aimed to 1) determine changes in the salivary
        oxytocin (OT) level during breast stimulation for promoting the spontaneous onset
        of labor in low-risk term pregnancies, and 2) clarify the feasibility of the
        breast stimulation intervention protocol in terms of practicality and
        acceptability. METHODS: We used a single arm trial design. Sixteen low-risk
        pregnant women between 38 and 40 weeks of gestation with cephalic presentation
        participated. They performed breast stimulation for 3 days with an attendant
        midwife in a single maternity hospital. Each breast was stimulated for 15 minutes
        for a total of 1 hour per day. Saliva was collected 10 minutes before the
        intervention and 15, 30, 60, 75, and 90 minutes after the intervention, yielding
        18 samples per woman. RESULTS: Among a total of 282 saliva samples from the 16
        participants, OT level was measured in 142 samples (missing rate: 49.6%). The
        median OT level showed the highest values on day 3 of the breast stimulation,
        with a marked increase 30 min after the intervention. In the mixed models after
        multiple imputation for missing data, the OT level on the first day of
        intervention was significantly lower than that on the third day of intervention.
        Fatigue from breast stimulation decreased on subsequent days, and most of the
        women (75%) felt no discomfort with the protocol. Uterine hyperstimulation was
        not observed. CONCLUSION: Following a 3-day breast stimulation protocol for
        spontaneous onset of labor, the mean OT level showed the highest values on day 3.
        The breast stimulation intervention protocol showed good feasibility in terms of
        practicality and acceptability among the pregnant women. Additional large-scale
        studies are warranted to confirm the protocol's effectiveness.
    FAU - Takahata, Kaori
    AU  - Takahata K
    AUID- ORCID: http://orcid.org/0000-0002-8141-3354
    AD  - St. Luke's International University, Tokyo, Japan.
    FAU - Horiuchi, Shigeko
    AU  - Horiuchi S
    AD  - Graduate School of Nursing Science, St. Luke's International University, Tokyo,
        Japan.
    AD  - St. Luke's Maternity Care Home, Tokyo, Japan.
    FAU - Tadokoro, Yuriko
    AU  - Tadokoro Y
    AD  - St. Luke's International University, Tokyo, Japan.
    FAU - Shuo, Takuya
    AU  - Shuo T
    AD  - Hokuriku University, Ishikawa, Japan.
    FAU - Sawano, Erika
    AU  - Sawano E
    AD  - Department of Neurobiology and Behavior, Graduate School of Biomedical Sciences,
        Nagasaki University, Nagasaki, Japan.
    FAU - Shinohara, Kazuyuki
    AU  - Shinohara K
    AD  - Department of Neurobiology and Behavior, Graduate School of Biomedical Sciences,
        Nagasaki University, Nagasaki, Japan.
    LA  - eng
    PT  - Journal Article
    DEP - 20180215
    PL  - United States
    TA  - PLoS One
    JT  - PloS one
    JID - 101285081
    EDAT- 2018/02/16 06:00
    MHDA- 2018/02/16 06:00
    CRDT- 2018/02/16 06:00
    PHST- 2017/01/19 00:00 [received]
    PHST- 2018/01/19 00:00 [accepted]
    PHST- 2018/02/16 06:00 [entrez]
    PHST- 2018/02/16 06:00 [pubmed]
    PHST- 2018/02/16 06:00 [medline]
    AID - 10.1371/journal.pone.0192757 [doi]
    AID - PONE-D-16-47379 [pii]
    PST - epublish
    SO  - PLoS One. 2018 Feb 15;13(2):e0192757. doi: 10.1371/journal.pone.0192757.
        eCollection 2018.
    ```

!!! note "格式"

    * 文件起始：空行
    * 文件终止：空行
    * 文献起始：PMID- XXXXXXXX
    * 文献终止：空行
    * 字段标识：XXXX- YYYYYYYY
    * 校验方式：
        1. 第1行： `line = '/n'`
        2. 第2行前4个字母： `line[:4] = 'PMID'`

!!! note "方法"

    ```python
    import pubmed

    srcdata = pubmed.getdata(filepath)
    ```

## **XML**

!!! 暂无计划支持

## **PMID List**

!!! 暂无计划支持

## **CSV**

!!! 暂无计划支持
