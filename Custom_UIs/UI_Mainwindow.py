# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_Mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    QSize,
)
from PySide6.QtGui import (
    QAction,
    QFont,
)
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from pyqtgraph import ImageView, PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow) -> None:
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1085, 551)
        self.actionOpen_Directory = QAction(MainWindow)
        self.actionOpen_Directory.setObjectName("actionOpen_Directory")
        self.action_cur_jpeg_export = QAction(MainWindow)
        self.action_cur_jpeg_export.setObjectName("action_cur_jpeg_export")
        self.action_geometry_load = QAction(MainWindow)
        self.action_geometry_load.setObjectName("action_geometry_load")
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.actionRead_Dependencies = QAction(MainWindow)
        self.actionRead_Dependencies.setObjectName("actionRead_Dependencies")
        self.actionContact_information = QAction(MainWindow)
        self.actionContact_information.setObjectName("actionContact_information")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.actionContact = QAction(MainWindow)
        self.actionContact.setObjectName("actionContact")
        self.action_cur_jpeg_preview = QAction(MainWindow)
        self.action_cur_jpeg_preview.setObjectName("action_cur_jpeg_preview")
        self.action_dir_goto_parent = QAction(MainWindow)
        self.action_dir_goto_parent.setObjectName("action_dir_goto_parent")
        self.action_dir_goto_cur_child = QAction(MainWindow)
        self.action_dir_goto_cur_child.setObjectName("action_dir_goto_cur_child")
        self.action_dir_cur_child_fold = QAction(MainWindow)
        self.action_dir_cur_child_fold.setObjectName("action_dir_cur_child_fold")
        self.action_dir_cur_child_unfold = QAction(MainWindow)
        self.action_dir_cur_child_unfold.setObjectName("action_dir_cur_child_unfold")
        self.action_cur_file_open = QAction(MainWindow)
        self.action_cur_file_open.setObjectName("action_cur_file_open")
        self.actionsdf = QAction(MainWindow)
        self.actionsdf.setObjectName("actionsdf")
        self.actionSave_geometry_configuration_Ctrl_Shift_L = QAction(MainWindow)
        self.actionSave_geometry_configuration_Ctrl_Shift_L.setObjectName(
            "actionSave_geometry_configuration_Ctrl_Shift_L"
        )
        self.action_dir_ft_filter_toggle = QAction(MainWindow)
        self.action_dir_ft_filter_toggle.setObjectName("action_dir_ft_filter_toggle")
        self.action_tabs_show_tab1 = QAction(MainWindow)
        self.action_tabs_show_tab1.setObjectName("action_tabs_show_tab1")
        self.action_tabs_show_tab2 = QAction(MainWindow)
        self.action_tabs_show_tab2.setObjectName("action_tabs_show_tab2")
        self.action_tabs_show_tab3 = QAction(MainWindow)
        self.action_tabs_show_tab3.setObjectName("action_tabs_show_tab3")
        self.actionChange_Pre_Trained_Model = QAction(MainWindow)
        self.actionChange_Pre_Trained_Model.setObjectName(
            "actionChange_Pre_Trained_Model"
        )
        self.actionChange_Output_Directory = QAction(MainWindow)
        self.actionChange_Output_Directory.setObjectName(
            "actionChange_Output_Directory"
        )
        self.actionOpen_Output_Directory = QAction(MainWindow)
        self.actionOpen_Output_Directory.setObjectName("actionOpen_Output_Directory")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.sp_audio_rec_duration = QDoubleSpinBox(self.groupBox)
        self.sp_audio_rec_duration.setObjectName("sp_audio_rec_duration")
        self.sp_audio_rec_duration.setValue(10.000000000000000)

        self.formLayout_3.setWidget(
            0, QFormLayout.FieldRole, self.sp_audio_rec_duration
        )

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.sp_audio_rec_rate = QSpinBox(self.groupBox)
        self.sp_audio_rec_rate.setObjectName("sp_audio_rec_rate")
        self.sp_audio_rec_rate.setMaximum(999999)
        self.sp_audio_rec_rate.setValue(44100)
        self.sp_audio_rec_rate.setDisplayIntegerBase(10)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.sp_audio_rec_rate)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.pb_start_record = QPushButton(self.groupBox)
        self.pb_start_record.setObjectName("pb_start_record")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.pb_start_record)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.formLayout_3.setItem(3, QFormLayout.FieldRole, self.verticalSpacer)

        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pb_play_selected_audio = QPushButton(self.groupBox_4)
        self.pb_play_selected_audio.setObjectName("pb_play_selected_audio")

        self.verticalLayout.addWidget(self.pb_play_selected_audio)

        self.pyqt_graph_audio = PlotWidget(self.groupBox_4)
        self.pyqt_graph_audio.setObjectName("pyqt_graph_audio")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(
            self.pyqt_graph_audio.sizePolicy().hasHeightForWidth()
        )
        self.pyqt_graph_audio.setSizePolicy(sizePolicy)
        self.pyqt_graph_audio.setMinimumSize(QSize(400, 200))

        self.verticalLayout.addWidget(self.pyqt_graph_audio)

        self.pyqt_graph_audio_2 = ImageView(self.groupBox_4)
        self.pyqt_graph_audio_2.setObjectName("pyqt_graph_audio_2")
        sizePolicy.setHeightForWidth(
            self.pyqt_graph_audio_2.sizePolicy().hasHeightForWidth()
        )
        self.pyqt_graph_audio_2.setSizePolicy(sizePolicy)
        self.pyqt_graph_audio_2.setMinimumSize(QSize(400, 200))

        self.verticalLayout.addWidget(self.pyqt_graph_audio_2)

        self.gridLayout.addWidget(self.groupBox_4, 0, 1, 2, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName("formLayout")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.label_result = QLabel(self.groupBox_3)
        self.label_result.setObjectName("label_result")
        font = QFont()
        font.setPointSize(22)
        self.label_result.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_result)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.formLayout.setItem(2, QFormLayout.FieldRole, self.verticalSpacer_3)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName("label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_result_confidence = QLabel(self.groupBox_3)
        self.label_result_confidence.setObjectName("label_result_confidence")
        self.label_result_confidence.setFont(font)

        self.formLayout.setWidget(
            0, QFormLayout.FieldRole, self.label_result_confidence
        )

        self.gridLayout.addWidget(self.groupBox_3, 0, 2, 2, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.pb_load_audio_file = QPushButton(self.groupBox_2)
        self.pb_load_audio_file.setObjectName("pb_load_audio_file")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.pb_load_audio_file)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.l_loaded_file_dur = QLabel(self.groupBox_2)
        self.l_loaded_file_dur.setObjectName("l_loaded_file_dur")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.l_loaded_file_dur)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_9)

        self.l_loaded_file_rate = QLabel(self.groupBox_2)
        self.l_loaded_file_rate.setObjectName("l_loaded_file_rate")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.l_loaded_file_rate)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.formLayout_2.setItem(3, QFormLayout.FieldRole, self.verticalSpacer_2)

        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(1, 100)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1085, 19))
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuOptions.addAction(self.actionChange_Pre_Trained_Model)
        self.menuOptions.addAction(self.actionChange_Output_Directory)
        self.menuOptions.addAction(self.actionOpen_Output_Directory)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionOpen_Directory.setText(
            QCoreApplication.translate("MainWindow", "Open Directory", None)
        )
        self.action_cur_jpeg_export.setText(
            QCoreApplication.translate("MainWindow", "Export (Ctlr-E)", None)
        )
        self.action_geometry_load.setText(
            QCoreApplication.translate(
                "MainWindow", "Load geometry configuration (Ctrl + L)", None
            )
        )
        self.action_help.setText(
            QCoreApplication.translate("MainWindow", "Help (Ctrl+H)", None)
        )
        self.actionRead_Dependencies.setText(
            QCoreApplication.translate("MainWindow", "Read Dependencies", None)
        )
        self.actionContact_information.setText(
            QCoreApplication.translate("MainWindow", "Contact information", None)
        )
        self.action_about.setText(
            QCoreApplication.translate("MainWindow", "About (Ctrl+A)", None)
        )
        self.actionContact.setText(
            QCoreApplication.translate("MainWindow", "Contact", None)
        )
        self.action_cur_jpeg_preview.setText(
            QCoreApplication.translate("MainWindow", "Preview (Space)", None)
        )
        self.action_dir_goto_parent.setText(
            QCoreApplication.translate(
                "MainWindow", "Go to Parent Directory (Backspace)", None
            )
        )
        self.action_dir_goto_cur_child.setText(
            QCoreApplication.translate(
                "MainWindow", "Go inside Selected Directory (Enter)", None
            )
        )
        self.action_dir_cur_child_fold.setText(
            QCoreApplication.translate(
                "MainWindow", "Fold Selected Directory (Left Arrow)", None
            )
        )
        self.action_dir_cur_child_unfold.setText(
            QCoreApplication.translate(
                "MainWindow", "Unfold Selected Directory (Right Arrow)", None
            )
        )
        self.action_cur_file_open.setText(
            QCoreApplication.translate(
                "MainWindow", "Open with an external app (Ctrl+O)", None
            )
        )
        self.actionsdf.setText(QCoreApplication.translate("MainWindow", "sdf", None))
        self.actionSave_geometry_configuration_Ctrl_Shift_L.setText(
            QCoreApplication.translate(
                "MainWindow", "Save geometry configuration (Ctrl + Shift + L)", None
            )
        )
        self.action_dir_ft_filter_toggle.setText(
            QCoreApplication.translate(
                "MainWindow", "File type filter toggle (Ctrl+F)", None
            )
        )
        self.action_tabs_show_tab1.setText(
            QCoreApplication.translate(
                "MainWindow", "Raw Bayer Tab (Ctrl+1) or (Alt+1)", None
            )
        )
        self.action_tabs_show_tab2.setText(
            QCoreApplication.translate(
                "MainWindow", "Spectrum-Raw Tab (Ctrl+2) or (Alt+2)", None
            )
        )
        self.action_tabs_show_tab3.setText(
            QCoreApplication.translate(
                "MainWindow", "Spectrum-Reflectance Tab (Ctrl+3) or (Alt+3)", None
            )
        )
        self.actionChange_Pre_Trained_Model.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u0443\u0440\u0433\u0430\u0441\u0430\u043d \u043c\u043e\u0434\u0435\u043b\u044b\u043d \u0444\u0430\u0439\u043b \u043e\u0440\u0443\u0443\u043b\u0430\u0445\n"
                "",
                None,
            )
        )
        self.actionChange_Output_Directory.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0413\u0430\u0440\u0430\u043b\u0442\u044b\u043d \u0445\u0430\u0432\u0442\u0430\u0441 \u0441\u043e\u043b\u0438\u0445\n"
                "",
                None,
            )
        )
        self.actionOpen_Output_Directory.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0413\u0430\u0440\u0430\u043b\u0442\u044b\u043d \u0445\u0430\u0432\u0442\u0430\u0441 \u043d\u044d\u044d\u0445\n"
                "",
                None,
            )
        )
        self.groupBox.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u041e\u0440\u043e\u043b\u0442 2: \u0411\u0438\u0447\u043b\u044d\u0433 ",
                None,
            )
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0411\u0438\u0447\u043b\u044d\u0433\u0438\u0439\u043d \u0445\u0443\u0433\u0430\u0446\u0430\u0430 (\u0441\u0435\u043a)",
                None,
            )
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0411\u0438\u0447\u043b\u044d\u0433\u0438\u0439\u043d \u0442\u04af\u04af\u0432\u044d\u0440\u043b\u044d\u043b\u0442\u0438\u0439\u043d\n"
                "\u0445\u0443\u0440\u0434 (1/\u0441\u0435\u043a)",
                None,
            )
        )
        self.label_5.setText("")
        self.pb_start_record.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0411\u0438\u0447\u0438\u0445", None
            )
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0410\u0443\u0434\u0438\u043e \u0413\u0440\u0430\u0444\u0438\u043a",
                None,
            )
        )
        self.pb_play_selected_audio.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0410\u0443\u0434\u0438\u043e \u0442\u043e\u0433\u043b\u0443\u0443\u043b\u0430\u0445",
                None,
            )
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate(
                "MainWindow", "\u04ae\u0440 \u0434\u04af\u043d", None
            )
        )
        self.label_6.setText(
            QCoreApplication.translate("MainWindow", "\u041e\u043d\u043e\u0448", None)
        )
        self.label_result.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u04ae\u0440 \u0434\u04af\u043d\u0433\u0438\u0439\u043d \u043e\u043d\u043e\u043e",
                None,
            )
        )
        self.label_result_confidence.setText(
            QCoreApplication.translate("MainWindow", "...", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u041e\u0440\u043e\u043b\u0442 1: \u0424\u0430\u0439\u043b",
                None,
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0424\u0430\u0439\u043b \u043e\u0440\u0443\u0443\u043b\u0430\u0445",
                None,
            )
        )
        self.pb_load_audio_file.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0424\u0430\u0439\u043b \u043e\u0440\u0443\u0443\u043b\u0430\u0445",
                None,
            )
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0410\u0443\u0434\u0438\u043e \u0444\u0430\u0439\u043b\u044b\u043d \u0445\u0443\u0433\u0430\u0446\u0430\u0430 (\u0441\u0435\u043a)",
                None,
            )
        )
        self.l_loaded_file_dur.setText(
            QCoreApplication.translate("MainWindow", "...", None)
        )
        self.label_9.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0410\u0443\u0434\u0438\u043e \u0444\u0430\u0439\u043b\u044b\u043d \u0442\u04af\u04af\u0432\u044d\u0440\u043b\u044d\u043b\u0442\u0438\u0439\u043d\n"
                " \u0445\u0443\u0440\u0434 (1/\u0441\u0435\u043a)\n"
                "",
                None,
            )
        )
        self.l_loaded_file_rate.setText(
            QCoreApplication.translate("MainWindow", "...", None)
        )
        self.menuOptions.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u043e\u043d\u0433\u043e\u043b\u0442\u0443\u0443\u0434",
                None,
            )
        )

    # retranslateUi
