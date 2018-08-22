# [万方数据知识服务平台](http://www.wanfangdata.com.cn)

---

* **解析文件**：./mrhpkg/filters/wanfang.py
* **默认格式**：NoteExpress

## **文献导出格式对照表**

**最后更新**：2018.05.29

|Fields|NoteExpress|RefWorks|NoteFirst|EndNote|Bibtex|
|-|-|-|-|-|-|
|**Essential Fields**|
|Author|Y (CN/ENG)|X[^1]|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|
|Title|Y (CN/ENG)|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|Y (CN)|
|Journal|Y (CN/ENG)|Y (CN/ENG)|Y (CN)|Y (CN/ENG)|Y (CN)|
|Type|Y|Y|Y|Y|Y|
|Year|Y|Y|Y|Y|Y|
|Volumn|N|N|N|N|N|
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
    {Title}: 医护人员职业性损伤的危险因素及防护对策
    {Author}: 戴青梅
    {Author}: 王立英
    {Author}: 刘素美
    {Author}: 李法云
    {Author Address}: 261041
    {Author Address}: 261041
    {Author Address}: 261041
    {Author Address}: 潍坊市卫生局医政科
    {Journal}: 中华护理杂志
    {Translated Journal}: CHINESE JOURNAL OF NURSING
    {ISBN/ISSN}: 0254-1769
    {Year}: 2002
    {Issue}: 7
    {Pages}: 532-534
    {Keywords}: 医护人员
    {Keywords}: 职业性
    {Keywords}: 性损伤
    {Keywords}: 危险因素
    {Keywords}: 医务工作者
    {Keywords}: 诊疗技术
    {Keywords}: 医学科学
    {Keywords}: 危害因素
    {Keywords}: 身心健康
    {Keywords}: 临床应用
    {Keywords}: 化学药物
    {Keywords}: 个人防护
    {Keywords}: 高新技术
    {Keywords}: 操作过程
    {Keywords}: 护理
    {Keywords}: 国内
    {Abstract}: 随着医学科学的发展和各种诊疗技术的推广，尤其是近几年新的化学药物和高新技术的临床应用，医务工作者常暴露于多种职业性危害因素之中，在诊疗、护理、操作过程中若不注意个人防护容易造成职业性损伤（occupational injuries,OI）,严重威胁着医护人员的身心健康，成为目前亟待解决的问题，现将国内外OI最新进展情况综述如下。
    {URL}: http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=zhhlzz200207021
    {Database Provider}: 北京万方数据股份有限公司
    {Language}: chi
    ```

!!! note "格式"

    * 文件起始：{Reference Type}: XXXX
    * 文件终止：空行
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

## **RefWorks**

!!! 暂无计划支持

## **NoteFirst**

!!! 暂无计划支持

## **EndNote**

!!! 暂无计划支持

## **Bibtex**

!!! 暂无计划支持
