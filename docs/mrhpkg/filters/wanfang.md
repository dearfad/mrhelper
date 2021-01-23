# [万方数据知识服务平台](http://www.wanfangdata.com.cn)

---

* **解析文件**：./mrhpkg/filters/wanfang.py
* **默认格式**：NoteExpress

## **文献导出格式对照表**

**最后更新**：2021.01.23

|Fields|NoteExpress|RefWorks|NoteFirst|EndNote|Bibtex|
|-|-|-|-|-|-|
|**Essential Fields**|
|Author|Y (CN/ENG)|X[^1]|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|
|Title|Y (CN/ENG)|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|Y (CN)|
|Journal|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|Y (CN/ENG)|Y (CN)|
|Type|Y|Y|Y|Y|Y|
|Year|Y|Y|Y|Y|Y|
|Volumn|Y|Y|Y|Y|Y|
|Issue|Y|Y|Y|Y|Y|
|Page|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|
|**Analysis Fields**|
|Month|N|N|N|N|Y|
|Link|Y|Y|Y|Y|N|
|DOI|Y|Y|Y|Y|N|
|Abstract|Y|Y|Y|Y|N|
|Keywords|Y|Y|Y|Y|N|
|Address|Y|N[^2]|N|Y[^3]|N|
|ISSN|Y|Y|Y|Y|N|
|Database|Y|Y|N|Y|N|
|Language|Y|Y|Y|Y|N|
|**Other Fields**|
|Country|N|Y|N|N|N|
|Fund|N|Y|N|N|N|
|Notes|N|Y[^4]|N|N|N|

[^1]: **错误**：作者中文及英文姓名列于A1字段内，无英文姓名时标注为之前文献作者英文名。
[^2]: **错误**：设计有地址字段AD，但一些文献没有导出地址。
[^3]: **标记**：地址非常完整，单位/省市/邮编
[^4]: **标记**：作者个数，第一作者

## **NoteExpress**

??? example "范例"

    ```text
    {Reference Type}: Journal Article
    {Title}: 乳腺癌术后患者婚姻质量与负性情绪、社会支持的相关性
    {Translated Title}: Relationship between marital quality, negative emotion and social support in patients with breast cancer after operation
    {Author}: 许雅琼
    {Author}: 张银萍
    {Translated Author}: XU Ya-qiong
    {Translated Author}: ZHANG Yin-ping
    {Author Address}: 西安交通大学医学部公共卫生学院,陕西 西安,710061;西安交通大学第二附属医院肿瘤病院,陕西 西安,710004
    {Author Address}: 西安交通大学医学部
    {Journal}: 临床医学研究与实践
    {Translated Journal}: Clinical Research and Practice
    {ISBN/ISSN}: 2096-1413
    {Year}: 2020
    {Volume}: 5
    {Issue}: 1
    {Pages}: 49-51
    {Keywords}: 乳腺癌
    {Keywords}: 婚姻质量
    {Keywords}: 焦虑
    {Keywords}: 抑郁
    {Keywords}: 社会支持
    {Abstract}: 目的 调查乳腺癌术后患者婚姻质量,并探讨负性情绪、社会支持与乳腺癌术后患者婚姻质量的相关性.方法 选取西安交通大学第二附属医院肿瘤外科的乳腺癌术后患者110例,采用一般情况调查问卷、中国人婚姻质量问卷(CMQI)、焦虑自评量表(SAS)、抑郁自评量表(SDS)和社会支持评定量表(SSRS)进行调查.结果 患者的婚姻质量总分低于常模,SAS和SDS评分均高于常模(P<0.05).患者的婚姻质量评分与SAS评分、SDS评分呈负相关,与社会支持评分呈正相关(P<0.05).结论 乳腺癌术后患者婚姻质量会降低且容易产生负性情绪,医护人员应该加强对其心理健康的关注,提高对患者的社会支持.
    {URL}: http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=lcyxyjysj202001019
    {DOI}: 10.19347/j.cnki.2096-1413.202001019
    {Database Provider}: 北京万方数据股份有限公司
    {Language}: chi
    ```

!!! note "格式"

    * 文件起始：{Reference Type}: XXXX
    * 文件终止：无
    * 文献起始：{Reference Type}: XXXX
    * 文献终止：空行
    * 字段标识：{XXXX}: YYYYYYYY
    * 校验方式：
        1. 第1行： `line[:16] == '{Reference Type}'`

!!! note "方法"

    ```python
    import wanfang

    srcdata = wanfang.getdata(filepath)
    ```

!!! note "校验及更正"

    * Abstract有分行BUG，已合并
    * 'Author', 'Translated Author', 'Author Address', 'Keywords' -> if str -> list
    * if Abstact list -> str

## **RefWorks**

!!! 暂无计划支持

## **NoteFirst**

!!! 暂无计划支持

## **EndNote**

!!! 暂无计划支持

## **Bibtex**

!!! 暂无计划支持
