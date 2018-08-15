# 医学综述助手

![GitHub (pre-)release](https://img.shields.io/github/release/dearfad/mrhelper/all.svg?style=plastic)

* **MrHelper**：**M**edical **R**eriew **H**elper
* 是一个用于**整理标注参考文献**、**快速创建医学综述初稿**的WORD文档及ENDNOTE参考文献生成器。

## 特色

* 使用**Web Of Science**, **Pubmed**, **CNKI**, **万方**数据库文献导出文件
* 便捷查看文献网页、全文、是否核心/SCI文献
* **CS/LCS/CR/LCR** 相关文献显示
* 导出生成含有ENDNOTE临时引文的WORD综述初稿

## 使用方法

* 快速入门 - [链接](https://https://dearfad.github.io/mrhelper/quickstart)
* 帮助文档 - [链接](https://dearfad.github.io/mrhelper)
* 解压后执行 **mrhelper.exe**
* 从源码执行，请安装以下模块：
* python 3.6
* python-docx
    ```python
    pip install python-docx
    ```
* PyQt5 5.10.1
    ```python
    pip install PyQt5==5.10.1
    ```
* Beautiful Soup
    ```python
    pip install beautifulsoup4
    ```
* defusedxml
    ```python
    pip install defusedxml
    ```
* requests
    ```python
    pip install requests
    ```
* requests[socks]
    ```python
    pip install requests[socks]
    ```
* pyinstaller
    ```python
    pip install pyinstaller
    ```

## 依赖库

* [Python](https://www.python.org) - 编程语言
* [python-docx](https://python-docx.readthedocs.io) - 生成综述WORD文稿
* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) - (GPL) 程序界面
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 解析抓取的文献页面
* [defusedxml](https://pypi.org/project/defusedxml/) - 安全解析CNKI E-Study .eln格式
* [requests/requests[socks]](http://www.python-requests.org) - Pubmed, CNKI, 万方文献页面抓取
* [Pyinstaller](http://www.pyinstaller.org/) - 打包可执行程序文件（.exe）

## 贡献

* 请参阅 [CONTRIBUTING.md](https://github.com/dearfad/MrHelper/blob/master/docs/CONTRIBUTING.md)

## 版本

* 使用 [SemVer](http://semver.org/)

## 作者

* [**dearfad**](https://github.com/dearfad)

## 版权

* 本项目遵循 GPLv3 License - 参阅 [LICENSE](https://github.com/dearfad/MrHelper/blob/master/LICENSE)

## 行为规范

* 请参阅[行为规范](https://github.com/dearfad/MrHelper/blob/master/docs/CODE_OF_CONDUCT.md)

## 致谢

* 所有本软件的使用者
