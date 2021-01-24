#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Medical Review Helper
~~~~~~~~~~~~~~~~~~~~~

An application that can help to create medical review draft fast and rationally.

:mrhelper.py: Main Program
:copyright: (c) 2018-2021 by Dearfad
:Email: dearfad@sina.com
:license: GPL-v3
"""

import cgitb
import datetime
import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QCursor, QIcon, QColor
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QMenu, QTreeWidgetItemIterator, QComboBox, QAbstractItemView

import mrhpkg.mrhabout as mrhabout
import mrhpkg.mrhimp as mrhimp
import mrhpkg.mrhhelp as mrhhelp
from mrhpkg.mrhcore import MrhIo, MrhExport, MrhWeb, MrhConfig, MrhTable
from mrhpkg.mrhgui import MrhMainWindow


# noinspection PyArgumentList
class MainWindow(MrhMainWindow):
    """Main GUI of Mrhelper"""

    def __init__(self):
        super().__init__()
        self.iothread = ''
        self.qthread = ''
        # Set StyleSheet
        self._set_stylesheet()
        self._set_appearance()
        self._set_fixed_content()
        # Sigslot
        self._tab_change_sigslot()
        self._tab_read_sigslot()
        self._tab_classify_sigslot()
        self._tab_export_sigslot()
        self._tab_config_sigslot()
        # Last Project
        self._detect_lastproject()

    # region StyleSheet
    def _set_stylesheet(self):
        with open(CONFIG.ini['Resource']['qss'], encoding='utf-8') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def _set_appearance(self):
        # Window
        self.setGeometry(200, 300, 960, 540)
        self.setWindowTitle('医学综述助手')
        self.setWindowIcon(QIcon('mrhres/icon.ico'))
        # TabWidget
        self.maintabwidget.setTabEnabled(1, False)
        self.maintabwidget.setTabEnabled(2, False)
        # Tab READ
        datatable = self.maintabwidget.tab_read.datatable
        column_width = CONFIG.ini['Appearance']['read_table_column'].split(',')
        horizontal_headers = CONFIG.ini['Appearance']['read_table_column_header'].split(
            ',')
        datatable.setColumnCount(len(horizontal_headers))
        datatable.setHorizontalHeaderLabels(horizontal_headers)
        for index, width in enumerate(column_width):
            datatable.setColumnWidth(index, int(width))
        rowsize = CONFIG.ini['Appearance']['read_table_row']
        datatable.verticalHeader().setDefaultSectionSize(int(rowsize))

        self.maintabwidget.tab_read.functiongroup.showMinimized()
        self.maintabwidget.tab_read.info_textedit.hide()
        self.maintabwidget.tab_read.viewoptiongroup.hide()
        self.maintabwidget.tab_read.memooptiongroup.hide()

        self.maintabwidget.tab_classify.info_textedit.hide()
        self.maintabwidget.tab_classify.memooptiongroup.hide()

        self.maintabwidget.tab_read.functiongroup.add_button.setDisabled(True)
        self.maintabwidget.tab_read.functiongroup.save_button.setDisabled(True)

    def _set_fixed_content(self):
        self.show_config()
        self.show_help()
        self.show_about()

    # endregion

    # region SigSlot
    def _tab_change_sigslot(self):
        self.maintabwidget.currentChanged.connect(self._maintab_change)

    def _maintab_change(self):
        current_index = self.maintabwidget.currentIndex()
        show_tab = {
            0: self._do_nothing,
            1: self.treelist_show,
            2: self.export_show,
            3: self._do_nothing,
            4: self._do_nothing,
            5: self._do_nothing
        }
        show_tab[current_index]()

    def _tab_read_sigslot(self):
        read = self.maintabwidget.tab_read
        # View Option Group
        viewgroup = read.viewoptiongroup
        viewgroup.abstract_checkbox.clicked.connect(self._filter_table)
        viewgroup.use_checkbox.clicked.connect(self._filter_table)
        viewgroup.type_checkbox.clicked.connect(self._filter_table)
        viewgroup.fiveyears_checkbox.clicked.connect(self._filter_table)
        viewgroup.relate_checkbox.clicked.connect(self._filter_table)
        viewgroup.search_lineedit.returnPressed.connect(self._filter_table)
        # Function Group
        functiongroup = read.functiongroup
        functiongroup.info_button.clicked.connect(self._info_clicked)
        functiongroup.view_button.clicked.connect(self._view_clicked)
        functiongroup.memo_button.clicked.connect(self._memo_clicked)
        functiongroup.openbrowser_button.clicked.connect(
            self._openbrowser_clicked)
        functiongroup.fulltext_button.clicked.connect(
            self._fulltext_button_clicked)
        functiongroup.citeref_button.clicked.connect(
            self._citeref_button_clicked)
        functiongroup.save_button.clicked.connect(self.save_project)
        functiongroup.open_button.clicked.connect(self.open_project)
        functiongroup.add_button.clicked.connect(self.add_project)
        functiongroup.new_button.clicked.connect(self.new_project)
        # Memo Option Group
        memogroup = read.memooptiongroup
        memogroup.iv_lineedit.textEdited.connect(self._memo_edited)
        memogroup.dv_lineedit.textEdited.connect(self._memo_edited)
        memogroup.relation_checkbox.clicked.connect(self._memo_edited)
        memogroup.group_lineedit.textEdited.connect(self._memo_edited)
        memogroup.subgroup_lineedit.textEdited.connect(self._memo_edited)
        memogroup.reftext_textedit.textChanged.connect(self._reftext_change)
        # Datatable Group
        datatable = read.datatable
        datatable.itemChanged.connect(self._datatable_itemchanged)
        datatable.itemClicked.connect(self._datatable_item_clicked)
        datatable.itemDoubleClicked.connect(self._datatable_item_doubleclicked)
        datatable.currentItemChanged.connect(self._datatable_item_clicked)
        datatable.customContextMenuRequested.connect(self._datatable_popmenu)

    def _tab_classify_sigslot(self):
        classify = self.maintabwidget.tab_classify
        classify.functiongroup.info_button.clicked.connect(self._info_clicked)
        classify.functiongroup.memo_button.clicked.connect(self._memo_clicked)
        classify.functiongroup.openbrowser_button.clicked.connect(
            self._openbrowser_clicked)
        classify.functiongroup.fulltext_button.clicked.connect(
            self._fulltext_button_clicked)
        classify.treelist.currentItemChanged.connect(
            self._treelist_item_clicked)
        classify.treelist.itemClicked.connect(self._treelist_item_clicked)
        classify.functiongroup.genseq_button.clicked.connect(
            self.treelist_genseqbutton_click)
        classify.functiongroup.save_button.clicked.connect(self.save_project)
        classify.treelist.customContextMenuRequested.connect(
            self.treelist_popmenu)

        memogroup = classify.memooptiongroup
        memogroup.iv_lineedit.textEdited.connect(self._memo_edited)
        memogroup.dv_lineedit.textEdited.connect(self._memo_edited)
        memogroup.relation_checkbox.clicked.connect(self._memo_edited)
        memogroup.group_lineedit.textEdited.connect(self._memo_edited)
        memogroup.subgroup_lineedit.textEdited.connect(self._memo_edited)
        memogroup.reftext_textedit.textChanged.connect(self._reftext_change)

    def _tab_export_sigslot(self):
        self.maintabwidget.tab_export.export_button.clicked.connect(
            self._export_button_click)
        self.maintabwidget.tab_export.save_button.clicked.connect(
            self.save_project)
        self.maintabwidget.tab_export.opendata_button.clicked.connect(
            self._open_data_folder_click)

    def _tab_config_sigslot(self):
        self.maintabwidget.tab_config.save_button.clicked.connect(
            self._config_savebutton_click)

    # endregion

    # region General Function
    def _do_nothing(self):
        pass

    def _show_status(self, message):
        self.statusBar().showMessage(message)

    def _get_view_options(self):
        viewoptions = {}
        viewgroup = self.maintabwidget.tab_read.viewoptiongroup
        viewoptions['abstract'] = viewgroup.abstract_checkbox.checkState()
        viewoptions['fiveyears'] = viewgroup.fiveyears_checkbox.checkState()
        viewoptions['type'] = viewgroup.type_checkbox.checkState()
        viewoptions['use'] = viewgroup.use_checkbox.checkState()
        viewoptions['relate'] = viewgroup.relate_checkbox.checkState()
        viewoptions['search'] = viewgroup.search_lineedit.text()
        return viewoptions

    def _get_current_rid(self):
        current_tab = self.maintabwidget.currentIndex()
        if current_tab == 0:
            datatable = self.maintabwidget.tab_read.datatable
            current_row = datatable.currentRow()
            if current_row == -1:
                return -1
            else:
                rid = int(datatable.item(current_row, 0).text())
        elif current_tab == 1:
            treelist = self.maintabwidget.tab_classify.treelist
            current_row = treelist.currentItem()
            if current_row == -1 or not current_row:
                return -1
            else:
                rid = int(current_row.text(2)) if current_row.text(2) else -1
        else:
            rid = -1
        return rid

    def _get_selected_items(self):
        mrhitem_dict = {}
        datatable = self.maintabwidget.tab_read.datatable
        selected_ranges = datatable.selectedRanges()
        for selected_range in selected_ranges:
            for row in range(selected_range.rowCount()):
                row_nubmer = selected_range.topRow() + row
                if not datatable.isRowHidden(row_nubmer):
                    rid_item = datatable.item(row_nubmer, 0)
                    rid = int(rid_item.text())
                    mrhitem_dict[rid] = rid_item
        return mrhitem_dict

    # endregion

    # region PROJECT
    def _detect_lastproject(self):
        filepath = CONFIG.ini['Directory']['project']
        if os.path.exists(filepath):
            self.open_project(filepath=filepath)

    def new_project(self):
        """Create Project File and Set Initial State."""
        global MRHPROJECT

        filepath = QFileDialog.getSaveFileName(
            caption='New MrHelper Project',
            directory='./mrhelper.mrh',
            filter='MrHelper Files (*.mrh)',
        )[0]

        if filepath:
            CONFIG.ini['Directory']['project'] = filepath
            MrhConfig.save(CONFIG)
            MRHPROJECT = mrhimp.MrhProject()
            self.maintabwidget.tab_read.datatable.clearContents()
            self.maintabwidget.tab_read.datatable.setRowCount(0)
            self.maintabwidget.tab_read.functiongroup.save_button.setEnabled(
                True)
            self.maintabwidget.tab_read.functiongroup.add_button.setEnabled(
                True)
            self.maintabwidget.setTabEnabled(1, True)
            self.maintabwidget.setTabEnabled(2, True)
            self.save_project()
        else:
            self._show_status('No Project Created...')

    def open_project(self, filepath=None):
        """Open .mrh File and Set State."""
        global MRHPROJECT

        if not filepath:
            filepath, filtertype = QFileDialog.getOpenFileName(
                None,
                'Open MrHelper Project',
                './',
                'MrHelper Files (*.mrh)'
            )

        if filepath:
            CONFIG.ini['Directory']['project'] = filepath
            MrhConfig.save(CONFIG)
            MRHPROJECT = mrhimp.MrhProject()
            self.maintabwidget.tab_read.datatable.clearContents()
            self.maintabwidget.tab_read.datatable.setRowCount(0)
            self.maintabwidget.tab_read.functiongroup.add_button.setEnabled(
                True)
            self.maintabwidget.tab_read.functiongroup.save_button.setEnabled(
                True)
            self.maintabwidget.setTabEnabled(1, True)
            self.maintabwidget.setTabEnabled(2, True)

            openpath = CONFIG.ini['Directory']['project']
            self.iothread = MrhIo(MRHPROJECT, openpath, mode='open')
            self.iothread.sigmsg.connect(self._show_status)
            self.iothread.sigmrh.connect(self._receive_project)
            self.iothread.start()
        else:
            self._show_status('No Project Opened...')

    def add_project(self):
        """Add references file to project."""
        filepaths = QFileDialog.getOpenFileNames()[0]

        if filepaths:
            self.iothread = MrhIo(MRHPROJECT, filepaths, mode='add')
            self.iothread.sigmsg.connect(self._show_status)
            self.iothread.sigmrh.connect(self._receive_project)
            self.iothread.start()
        else:
            self._show_status('No File Selected...')

    def save_project(self):
        """Save .mrh File."""
        savepath = CONFIG.ini['Directory']['project']
        self.iothread = MrhIo(MRHPROJECT, savepath, mode='save')
        self.iothread.sigmsg.connect(self._show_status)
        self.iothread.start()

    def _receive_project(self, mrhproject):
        global MRHPROJECT
        MRHPROJECT = mrhproject
        self._create_table()

    # endregion

    # region Tab READ
    def _create_table(self):
        datatable = self.maintabwidget.tab_read.datatable
        datatable.itemChanged.disconnect(self._datatable_itemchanged)
        datatable.clearContents()
        datatable.setRowCount(0)
        datatable.setSortingEnabled(False)
        datatable.setRowCount(len(MRHPROJECT.mrhdata))
        fields = [datatable.horizontalHeaderItem(
            index).text() for index in range(datatable.columnCount())]
        datatable.setEnabled(False)
        for row, mrhitem in enumerate(MRHPROJECT.mrhdata):
            itemcolor = MrhTable.markitem(CONFIG, mrhitem)
            for column, field in enumerate(fields):
                value = getattr(mrhitem, field, '')
                if isinstance(value, str):
                    if field == 'cs' or field == 'cr':
                        if value:
                            qitem = QTableWidgetItem()
                            qitem.setData(0, int(value))
                        else:
                            qitem = QTableWidgetItem()
                    else:
                        qitem = QTableWidgetItem(
                            value) if value else QTableWidgetItem()
                elif isinstance(value, list):
                    if field == 'lcs' or field == 'lcr':
                        qitem = QTableWidgetItem()
                        qitem.setData(0, len(value))
                    else:
                        qitem = QTableWidgetItem(
                            value[0]) if value else QTableWidgetItem()
                elif isinstance(value, int):
                    qitem = QTableWidgetItem()
                    qitem.setData(0, value)
                else:
                    qitem = QTableWidgetItem('-1')

                if itemcolor.setdefault(field, ''):
                    qitem.setBackground(QColor(itemcolor[field]))

                qitem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                if field == 'title':
                    qitem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                if field == 'rid':
                    qitem = QTableWidgetItem()
                    qitem.setData(0, value)
                    use = getattr(mrhitem, 'use', '')
                    qitem.setCheckState(use)
                    if use == 2:
                        qitem.setBackground(QColor('lightgreen'))
                    datatable.setItem(row, column, qitem)
                else:
                    datatable.setItem(row, column, qitem)

                if row % 100 == 0:
                    self._show_status(str(row))
        datatable.setEnabled(True)
        datatable.setSortingEnabled(True)
        datatable.sortByColumn(0, Qt.AscendingOrder)
        datatable.itemChanged.connect(self._datatable_itemchanged)
        self._filter_table()

    def _filter_table(self):
        viewoptions = self._get_view_options()
        currentrid = int(self._get_current_rid())
        currentitem = MRHPROJECT.mrhdata[currentrid] if currentrid != -1 else ''
        datatable = self.maintabwidget.tab_read.datatable
        self.maintabwidget.tab_read.viewoptiongroup.setDisabled(True)
        self.maintabwidget.tab_read.datatable.setUpdatesEnabled(False)
        rows = datatable.rowCount()
        visiblerow = 0

        for row in range(rows):
            datatable.setRowHidden(row, False)
            rid = int(datatable.item(row, 0).text())
            mrhitem = MRHPROJECT.mrhdata[rid]
            result = MrhTable.check_viewoptions(
                viewoptions, currentrid, currentitem, mrhitem)
            if result:
                datatable.setRowHidden(row, False)
                visiblerow += 1
            else:
                datatable.setRowHidden(row, True)
        datatable.verticalHeader().setDefaultSectionSize(
            int(CONFIG.ini['Appearance']['read_table_row']))
        self._show_status(f'Total: {visiblerow}')
        self._show_table(currentrid)

    def _show_table(self, rid):
        self.maintabwidget.tab_read.viewoptiongroup.setEnabled(True)
        self.maintabwidget.tab_read.datatable.setUpdatesEnabled(True)
        datatable = self.maintabwidget.tab_read.datatable
        datatable.setEnabled(True)
        if rid != -1:
            datatable.selectRow(rid)
            current_item = datatable.item(rid, 0)
            datatable.scrollToItem(
                current_item, QAbstractItemView.PositionAtCenter)

    def _info_clicked(self):
        current_tab = self.maintabwidget.currentIndex()
        if current_tab == 0:
            info = self.maintabwidget.tab_read.info_textedit
        elif current_tab == 1:
            info = self.maintabwidget.tab_classify.info_textedit
        else:
            return
        info.setVisible(not info.isVisible())

    def _view_clicked(self):
        view = self.maintabwidget.tab_read.viewoptiongroup
        view.setVisible(not view.isVisible())
        view.minimumSize()

    def _memo_clicked(self):
        current_tab = self.maintabwidget.currentIndex()
        if current_tab == 0:
            memo = self.maintabwidget.tab_read.memooptiongroup
        elif current_tab == 1:
            memo = self.maintabwidget.tab_classify.memooptiongroup
        else:
            return
        memo.setVisible(not memo.isVisible())

    def _openbrowser_clicked(self):
        rid = self._get_current_rid()
        if rid != -1:
            item = MRHPROJECT.mrhdata[rid]
            pmid = item.pmid
            pmcid = item.pmcid
            link = item.link
            title = item.title
            database = item.database

            pubmed_url = 'https://www.ncbi.nlm.nih.gov/pubmed/'
            pmc_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
            webpage = ''
            # Change it as Preferred
            # doi_url = 'https://doi.org/'
            # scholar_google_url = 'https://scholar.google.com.hk/scholar?&q='
            xueshu_baidu_url = 'http://xueshu.baidu.com/s?wd='
            # wanfang_url = 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=all&searchWord='

            # TODO wos link

            if database == 'PUBMED' or database == 'WOS':
                if pmcid:
                    webpage = pmc_url + pmcid
                elif pmid:
                    webpage = pubmed_url + pmid
            else:
                if database == 'CNKI' or database == 'WANFANG':
                    if link:
                        webpage = link
            if not webpage:
                webpage = xueshu_baidu_url + title

            QDesktopServices().openUrl(QUrl(webpage))

    def _fulltext_button_clicked(self):
        rid = self._get_current_rid()
        if rid != -1:
            mrhitem = MRHPROJECT.mrhdata[rid]
            pdffile = str(rid) + '.pdf'
            pdf = os.path.join(
                CONFIG.ini['Directory']['project'], 'pdf', pdffile)
            if os.path.exists(pdf):
                QDesktopServices().openUrl(QUrl.fromLocalFile(pdf))
            else:
                self._fulltext_open(mrhitem)

    @staticmethod
    def _fulltext_open(mrhitem):
        if mrhitem.database == 'WOS' or mrhitem.database == 'PUBMED':
            if mrhitem.doi:
                address = CONFIG.ini['Scihub']['url'] + mrhitem.doi
            else:
                return
        elif mrhitem.database == 'CNKI':
            id_cnki = mrhitem.link.split('&DbName=')[0].split('FileName=')[1]
            prefix_cnki = 'http://kns.cnki.net/KXReader/Detail?dbcode=CJFD&filename='
            address = ''.join([prefix_cnki, id_cnki])
        elif mrhitem.database == 'WANFANG':
            prefix_wf = 'http://www.wanfangdata.com.cn/search/onlineread.do?language=chi&resourceType=perio&source=WF&resourceId='
            id_wanfang = mrhitem.link.split('&id=')[1]
            title_wanfang = '&resourceTitle='
            title = mrhitem.title
            address = ''.join([prefix_wf, id_wanfang, title_wanfang, title])
        else:
            return
        QDesktopServices().openUrl(QUrl(address))

    def _citeref_button_clicked(self, data=None):
        data = MRHPROJECT.mrhdata if not data else data
        self.qthread = MrhWeb(data, MRHPROJECT, CONFIG)
        self.qthread.sigmsg.connect(self._show_status)
        self.qthread.sigmrh.connect(self._receive_project)
        self.qthread.start()

    def _memo_edited(self):
        current_tab = self.maintabwidget.currentIndex()
        rid = self._get_current_rid()
        if rid != -1:
            item = MRHPROJECT.mrhdata[rid]
            if current_tab == 0:
                memogroup = self.maintabwidget.tab_read.memooptiongroup
            elif current_tab == 1:
                memogroup = self.maintabwidget.tab_classify.memooptiongroup
            else:
                return
            item.iv = memogroup.iv_lineedit.text()
            item.relation = int(memogroup.relation_checkbox.checkState())
            item.dv = memogroup.dv_lineedit.text()
            group = memogroup.group_lineedit.text()

            if group:
                item.group[0] = group
                memogroup.subgroup_lineedit.setDisabled(False)
            else:
                item.group[0] = ''
                memogroup.subgroup_lineedit.setDisabled(True)
                item.group[1] = ''
            subgroup = memogroup.subgroup_lineedit.text()
            item.group[1] = subgroup if subgroup else ''

    def _reftext_change(self):
        # Split from _memo_change for textChanged Signal
        current_tab = self.maintabwidget.currentIndex()
        rid = self._get_current_rid()
        if rid != -1:
            item = MRHPROJECT.mrhdata[rid]
            if current_tab == 0:
                memogroup = self.maintabwidget.tab_read.memooptiongroup
            elif current_tab == 1:
                memogroup = self.maintabwidget.tab_classify.memooptiongroup
            else:
                return
            item.reftext = memogroup.reftext_textedit.toPlainText()

    def _datatable_itemchanged(self, tableitem):
        datatable = self.maintabwidget.tab_read.datatable
        tableitem_header = datatable.horizontalHeaderItem(
            tableitem.column()).text()
        if tableitem_header == 'rid':
            rid = int(tableitem.text())
            use = tableitem.checkState()
            MRHPROJECT.mrhdata[rid].use = use
            self._datatable_setusecolor(tableitem, use)

    def _datatable_setusecolor(self, tableitem, use):
        datatable = self.maintabwidget.tab_read.datatable
        datatable.itemChanged.disconnect(self._datatable_itemchanged)
        if use == 2:
            tableitem.setBackground(QColor('lightgreen'))
        else:
            tableitem.setBackground(QColor('transparent'))
        datatable.itemChanged.connect(self._datatable_itemchanged)

    def _datatable_item_clicked(self):
        self._info_show()
        self._memo_show()

    def _datatable_item_doubleclicked(self):
        view = self.maintabwidget.tab_read.viewoptiongroup
        view.abstract_checkbox.setCheckState(Qt.PartiallyChecked)
        view.use_checkbox.setCheckState(Qt.PartiallyChecked)
        view.type_checkbox.setCheckState(Qt.PartiallyChecked)
        view.fiveyears_checkbox.setCheckState(Qt.PartiallyChecked)
        view.search_lineedit.setText('')
        view.relate_checkbox.setCheckState(Qt.Checked)
        self._filter_table()

    def _datatable_popmenu(self):
        popmenu = QMenu()
        action_use = popmenu.addAction('use')
        action_abandon = popmenu.addAction('nouse')
        action_keep = popmenu.addAction('keep')
        action_retrieve = popmenu.addAction('get')
        action_source = popmenu.addAction('Source')
        action = popmenu.exec_(QCursor.pos())

        usedict = {
            action_use: 2,
            action_abandon: 0,
            action_keep: 1,
        }
        if action:
            if action == action_retrieve:
                self._datatable_popmenu_retrieve()
            elif action == action_source:
                self._info_show_source()
            else:
                self._datatable_popmenu_setuse(usedict[action])

    def _datatable_popmenu_retrieve(self):
        mrhitem_dict = self._get_selected_items()
        mrhitems = [MRHPROJECT.mrhdata[rid] for rid in mrhitem_dict.keys()]
        self._citeref_button_clicked(data=mrhitems)

    def _datatable_popmenu_setuse(self, use):
        datatable = self.maintabwidget.tab_read.datatable
        mrhitem_dict = self._get_selected_items()
        for rid, tableitem in mrhitem_dict.items():
            MRHPROJECT.mrhdata[rid].use = use
            datatable.itemChanged.disconnect(self._datatable_itemchanged)
            tableitem.setCheckState(use)
            datatable.itemChanged.connect(self._datatable_itemchanged)
            self._datatable_setusecolor(tableitem, use)

    def _info_show(self):
        current_tab = self.maintabwidget.currentIndex()
        rid = self._get_current_rid()
        if rid != -1:
            mrhitem = MRHPROJECT.mrhdata[rid]
            srcitem = MRHPROJECT.rawdata[rid]
            text = CONFIG.info.format(**locals())
            if current_tab == 0:
                info = self.maintabwidget.tab_read
            elif current_tab == 1:
                info = self.maintabwidget.tab_classify
            else:
                return
            info.info_textedit.setText(text)

    def _info_show_source(self):
        current_tab = self.maintabwidget.currentIndex()
        rid = self._get_current_rid()
        if rid != -1:
            srcitem = MRHPROJECT.rawdata[rid]
            if current_tab == 0:
                info = self.maintabwidget.tab_read
            elif current_tab == 1:
                info = self.maintabwidget.tab_classify
            else:
                return
            info.info_textedit.append('<hr>')
            info.info_textedit.append('<b>Source Record List<b><br>')
            for item in srcitem.__dict__:
                # Pycharm Warning Python>=3.6
                info.info_textedit.append(
                    f"{item}: {srcitem.__dict__[item]}<br>")

    def _memo_show(self):
        current_tab = self.maintabwidget.currentIndex()
        rid = self._get_current_rid()
        if rid != -1:
            item = MRHPROJECT.mrhdata[rid]
            if current_tab == 0:
                memogroup = self.maintabwidget.tab_read.memooptiongroup
            elif current_tab == 1:
                memogroup = self.maintabwidget.tab_classify.memooptiongroup
            else:
                return
            keywords = 'Keywords: ' + ', '.join(item.keywords)
            memogroup.keywords_label.setText(
                keywords[:120])  # If Long, Layout Change
            memogroup.iv_lineedit.setText(item.iv)
            memogroup.dv_lineedit.setText(item.dv)
            relationdict = {0: Qt.Unchecked,
                            1: Qt.PartiallyChecked, 2: Qt.Checked}
            memogroup.relation_checkbox.setCheckState(
                relationdict[item.relation])
            memogroup.reftext_textedit.setPlainText(item.reftext)
            if item.group[0]:
                memogroup.group_lineedit.setText(item.group[0])
                memogroup.subgroup_lineedit.setDisabled(False)
            else:
                memogroup.group_lineedit.setText('')
                memogroup.subgroup_lineedit.setDisabled(True)

            if item.group[1]:
                memogroup.subgroup_lineedit.setText(item.group[1])
            else:
                memogroup.subgroup_lineedit.setText('')
            group = set()
            subgroup = set()
            iv = set()
            dv = set()
            for item in MRHPROJECT.mrhdata:
                if item.use == 2:
                    group.add(item.group[0])
                    subgroup.add(item.group[1])
                    iv.add(item.iv)
                    dv.add(item.dv)
            memogroup.group_list_model.setStringList(list(group))
            memogroup.subgroup_list_model.setStringList(list(subgroup))
            memogroup.iv_list_model.setStringList(list(iv))
            memogroup.dv_list_model.setStringList(list(dv))

    # endregion

    # region Tab CLASSIFY
    def treelist_show(self):
        """Show Sequence of Selected References."""

        treelist = self.maintabwidget.tab_classify.treelist
        treelist.setSortingEnabled(False)
        treelist.clear()
        treedata = [item for item in MRHPROJECT.mrhdata if item.use == 2]

        group, subgroup, seq = set(), set(), set(MRHPROJECT.refseq)

        temprid = []
        for item in treedata:
            if item.group[0]:
                group.add(item.group[0])
            else:
                item.group[0] = '- -'
            if item.group[1]:
                subgroup.add(item.group[1])
            else:
                item.group[1] = '- -'
            if item.rid not in seq:
                MRHPROJECT.refseq.append(item.rid)
            temprid.append(item.rid)

        removerid = list(set(seq).difference(set(temprid)))

        for i in removerid:
            MRHPROJECT.refseq.remove(i)

        treedata = [MRHPROJECT.mrhdata[rid] for rid in MRHPROJECT.refseq]
        self.treelist_createtree(treedata, group, subgroup)
        treelist.expandAll()
        self.statusBar().showMessage(str('Total: ' + str(len(treedata))))

    def treelist_createtree(self, treedata, group, subgroup):
        """Create Treelist."""
        treelist = self.maintabwidget.tab_classify.treelist
        for item in treedata:
            subgroup_item = self.treelist_creatgrpitem(item.group)
            treeitem = QTreeWidgetItem(subgroup_item)
            treeitem.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled
            )
            treeitem.setData(1, 0, MRHPROJECT.refseq.index(item.rid))
            treeitem.setData(2, 0, item.rid)

            groupbox = QComboBox()
            groupbox.addItems([item for item in group])
            groupbox.setCurrentText(item.group[0])
            treelist.setItemWidget(treeitem, 3, groupbox)
            groupbox.currentIndexChanged.connect(
                self.treelist_comboboxchange)  # Pycharm warning bug

            subgroupbox = QComboBox()
            subgroupbox.addItems([item for item in subgroup])
            subgroupbox.setCurrentText(item.group[1])
            treelist.setItemWidget(treeitem, 4, subgroupbox)
            subgroupbox.currentIndexChanged.connect(
                self.treelist_comboboxchange)  # Pycharm warning bug

            treeitem.setText(5, item.title)

    def treelist_creatgrpitem(self, item_group):
        """Create group item."""
        treelist = self.maintabwidget.tab_classify.treelist
        # Creat TopLevel Group
        tree_group = treelist.findItems(item_group[0], Qt.MatchFixedString, 0)
        if tree_group:
            group = tree_group[0]
        else:
            group = QTreeWidgetItem(treelist)
            group.setText(0, item_group[0])
        # Creat SubGroup
        subgroup = None
        childcount = group.childCount()
        for i in range(childcount):
            if item_group[1] == group.child(i).text(0):
                subgroup = group.child(i)
                break
        if not subgroup:
            subgroup = QTreeWidgetItem(group)
            subgroup.setText(0, item_group[1])
        return subgroup

    def treelist_comboboxchange(self):
        """Rearrange Sequence of References."""
        treelist = self.maintabwidget.tab_classify.treelist
        sender = self.sender()
        pos = sender.pos()
        item = treelist.itemAt(0, pos.y())
        rid = int(item.text(2))
        combo_grp = treelist.itemWidget(item, 3)
        group = combo_grp.currentText()
        combo_subgrp = treelist.itemWidget(item, 4)
        subgrp = combo_subgrp.currentText()
        MRHPROJECT.mrhdata[rid].group = [group, subgrp]
        # self.treelist_show()
        # self.treelist_genseqbutton_click()

    def _treelist_item_clicked(self):
        self._info_show()
        self._memo_show()

    def treelist_genseqbutton_click(self):
        """Generate Sequence."""
        item = QTreeWidgetItemIterator(
            self.maintabwidget.tab_classify.treelist)
        MRHPROJECT.refseq = []
        while item.value():
            if item.value().text(2):
                rid = int(item.value().text(2))
                MRHPROJECT.refseq.append(rid)
            item = item.__iadd__(1)
        self.treelist_show()

    def treelist_popmenu(self):
        """Set Use Reference"""
        popmenu = QMenu()
        nouse_action = popmenu.addAction('nouse')
        keep_action = popmenu.addAction('keep')
        action = popmenu.exec_(QCursor.pos())
        if action == nouse_action:
            use = 0
        elif action == keep_action:
            use = 1
        else:
            return
        selected_items = self.maintabwidget.tab_classify.treelist.selectedItems()
        for item in selected_items:
            rid = int(item.text(2))
            MRHPROJECT.mrhdata[rid].use = use
            MRHPROJECT.refseq.remove(rid)
        self.treelist_show()
        # self.treelist_genseqbutton_click()

    # endregion

    # region Tab EXPORT
    def _export_button_click(self):
        reftree = self._export_get_tree()
        exportpath = os.path.dirname(CONFIG.ini['Directory']['project'])
        MrhExport(MRHPROJECT, exportpath, reftree, CONFIG.ini)
        current_time = str(datetime.datetime.now().time()).split('.')[0]
        self.statusBar().showMessage(current_time + ' Exported')

    def _export_get_tree(self):
        reftree = []  # groupname, tag, rid (tag 0 item 1 group 2 subgroup)
        item = QTreeWidgetItemIterator(
            self.maintabwidget.tab_classify.treelist)
        while item.value():
            groupname = item.value().text(0)
            if groupname:
                if item.value().parent():
                    reftree.append([groupname, 2, -1])
                else:
                    reftree.append([groupname, 1, -1])
            else:
                rid = item.value().text(2)
                reftree.append([groupname, 0, rid])
            item = item.__iadd__(1)
        return reftree

    def export_show(self):
        """Show export Tab."""
        pass

    @staticmethod
    def _open_data_folder_click():
        datapath = CONFIG.ini['Directory']['project']
        folder = os.path.dirname(datapath)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    # endregion

    # region Tab HELP
    def show_help(self):
        """Show Tab Help."""
        help_textedit = self.maintabwidget.tab_help.help_textedit
        helptext = mrhhelp.HELP
        help_textedit.setText(helptext)

    # endregion

    # region Tab ABOUT
    def show_about(self):
        """Show Tab About."""
        about = self.maintabwidget.tab_about.about_textedit
        abouttext = mrhabout.ABOUT
        about.setText(abouttext)
    # endregion

    # region Tab CONFIG
    def show_config(self):
        """Show Tab Config."""
        scihuburl = self.maintabwidget.tab_config.scihuburl_lineedit
        url = CONFIG.ini['Scihub']['url']
        scihuburl.setText(url)

    def _config_savebutton_click(self):
        scihuburl = self.maintabwidget.tab_config.scihuburl_lineedit.text()
        CONFIG.ini['Scihub']['url'] = scihuburl
        MrhConfig.save(CONFIG)
        current_time = str(datetime.datetime.now().time()).split('.')[0]
        self.statusBar().showMessage(current_time + ' Config Saved.')
    # endregion


def main():
    """Main Function."""
    cgitb.enable(format='text')  # Debug

    app = QApplication(sys.argv)
    app.setStyle(CONFIG.ini['Appearance']['style'])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    CONFIG = MrhConfig()  # Config With './mrhelper.ini'
    MRHPROJECT = mrhimp.MrhProject()
    main()
