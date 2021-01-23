# [CNKI](http://www.cnki.net) 中国知网

---

* **解析文件**：./mrhpkg/filters/cnki.py
* **默认格式**：知网研学（原E-Study）

## **文献导出格式对照表**

**最后更新**：2021.01.23

|Fields|CNKI E-Study|RefWorks|Endnote|NoteExpress|NoteFirst|
|-|-|-|-|-|-|
|**Essential Fields**|
|Author|Y (CN)|Y (CN)|Y (CN)|Y (CN)|Y (CN)|
|Title|Y (CN)|Y (CN)|Y (CN)|Y (CN)|Y (CN)|
|Journal|Y (CN)|Y (CN)|Y (CN)|Y (CN)|Y (CN)|
|Type|Y|Y|Y|Y|Y|
|Year|Y|Y|Y|Y|Y|
|Volumn|Y|Y|Y|Y|Y|
|Issue|Y|Y|Y|Y|Y|
|Page|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|Y (BP/EP)|
|**Analysis Fields**|
|Month|Y|N|N|N|N|
|Link|Y|N|N|N|N|
|DOI|N|N|N|N|N|
|Abstract|Y|Y|Y|Y|Y|
|Keywords|Y|Y|Y|Y|Y|
|Address|Y|Y|Y|Y|Y|
|ISSN|N|Y|Y|Y|Y|
|Database[^1]|Y|Y|N|Y|N|
|Language|N|Y|N|N|Y|
|**Other Fields**|
|Country|N|N|N|N|N|
|Fund|N|N|N|N|N|
|Notes|N|N|N|Y|N|
|CallNum|N|Y|Y|N|N|

[^1]: **标注**：DataType 1=学术期刊，2=学位论文，等等；SrcDatabase-来源库 定义2级标题，期刊，硕士，博士，报纸...

## **E-STUDY**

??? example "范例"

    ```text
    DataType: 1
    Title-题名: 医学综述撰写中的注意事项
    Author-作者: 施洋;
    Source-刊名: 中国科技信息
    Year-年: 2013
    PubTime-出版时间: 2013-04-01
    Keyword-关键词: 医学综述;写作;规范化
    Summary-摘要: 为指导医学人员查阅专业文献并撰写医学综述,了解目前的医学研究进展状况并培养独立思考、分析、归纳和总结的能力。对于初次接触医学综述写作的作者难免会犯一些错误,诸如综述题目过大、收集的文献量少、综述题目与参考文献出现偏差等。指导正确的医学综述写作方法,有助于医学人员把握领域内的发展前沿,明确自己的科研思路,为今后的科研临床工作打下良好的基础。
    Period-期: 07
    PageCount-页数: 1
    Page-页码: 161
    SrcDatabase-来源库: 期刊
    Organ-机构: 新疆医科大学学报编辑部;
    Link-链接: https://kns.cnki.net/kcms/detail/detail.aspx?FileName=XXJK201307097&DbName=CJFQ2013
    ```

!!! note "格式"

    * 文件起始：`DataType: 1`
    * 文件终止：无
    * 文献起始：`DataType: 1`
    * 文献终止：无
    * 字段标识：XXX-YYY: ZZZ
    * 校验方式：
        1. 第1行： `DataType: 1\n`

!!! note "方法"

    ```python
    import cnki

    srcdata = cnki.getdata(filepath)
    ```

!!! note "校验及更正"

    * Author-作者 Keyword-关键词 Organ-机构 -> list
    * 其余字段 -> 未校验
    * 如果'Year-年'无内容，则使用'PubTime-出版时间'内'-'前字符替换

## **Refworks**

!!! 暂无计划支持

## **EndNote**

!!! 暂无计划支持

## **NoteExpress**

!!! 暂无计划支持

## **NoteFirst**

!!! 暂无计划支持

