# ---------- Base libraries -------------------------------------------------------------------------------------------
# import os
# from os import PathLike
# import sys
import tempfile
import logging

# import subprocess
import platform
from datetime import datetime
from pathlib import Path


from CoreCodes.Wav_prediction import InfluenzaClassifier

# import shutil
import pyqtgraph as pg
# import time
from PIL import Image

# ---------- Numerical Visual packages---------------------------------------------------------------------------------
import numpy as np

# ---------- GUI libraries --------------------------------------------------------------------------------------------
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
# from PySide6.QtGui import QKeySequence, QShortcut, QColor
from PySide6.QtCore import Qt  # pQModelIndex, QDir,

# ---------- Custom libs ----------------------------------------------------------------------------------------------
from Custom_UIs.UI_Mainwindow import Ui_MainWindow
# from Custom_Libs.Lib_DataDirTree import DataDirTree

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


system_str = platform.system()
logging.basicConfig(
    filename=Path(tempfile.gettempdir()) / datetime.now().strftime("%Y%m%d_%H%M%S.log"),
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
)


class TheMainWindow(QMainWindow):
    inf_classifier: InfluenzaClassifier

    def __init__(self, parent: QWidget | None = None) -> None:
        super(TheMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_load_audio_file.clicked.connect(self.callback_pb_load_audio_file)
        self.ui.pb_start_record.clicked.connect(self.callback_pb_start_record)

        self.inf_classifier = InfluenzaClassifier("./CoreCodes/best_checkpoint_2_class_masked_5_17.model")

    def callback_pb_load_audio_file(self) -> None:
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setNameFilters(["Other File (*)", "Audio (*.wav)"])
        dlg.selectNameFilter("Audio (*.wav)")

        if dlg.exec_():
            selected_file_path = dlg.selectedFiles()[0]
            self.load_audio_file(selected_file_path)

    def load_audio_file(self, file_path_to_wav: str) -> None:
        # load {file_path_to_wav} generate image.
        # save generated image into {self.inf_classifier.output_path_spectrogram_img}
        self.inf_classifier.generate_spectrogram_from_wav_file(file_path_to_wav, "/tmp/")

        self.ui.l_loaded_file_rate.setNum(self.inf_classifier.sample_rate)
        self.ui.l_loaded_file_dur.setNum(self.inf_classifier.audio.shape[0] / self.inf_classifier.sample_rate)
        self.update_graph_on_ui()

    def update_graph_on_ui(self) -> None:
        """updates graph from self.audio_wav_data"""

        # update graph1 (wave graph)
        self.ui.pyqt_graph_audio.clear()
        self.ui.pyqt_graph_audio.plot(
            self.inf_classifier.time,
            self.inf_classifier.audio,
            pen=pg.mkPen("k", width=1, style=Qt.PenStyle.SolidLine),
        )

        im = Image.open(self.inf_classifier.output_path_spectrogram_img)
        if im.mode == "RGBA":
            im = im.convert("RGB")


        # update graph2 (image)
        self.ui.pyqt_graph_audio_2.clear()
        self.ui.pyqt_graph_audio_2.setImage(
            img = np.array(im),
            levels=(0, 255),
            axes={"x":1, "y":0, "c":2}
        )


    def callback_pb_start_record(self) -> None:
        self.ui.pb_start_record.setText("Recording")

        file_path_wav_output = self.inf_classifier.record_audio(
            output_directory="/tmp",
            output_filename=datetime.now().strftime("%Y%m%d_%H%M%S.wav"),
            duration=10,
            sample_rate=44100,
            channels=1,
        )

        self.ui.l_rec_state.setText(f"Record saved at {file_path_wav_output}")

        self.load_audio_file(file_path_wav_output)
        self.ui.pb_start_record.setText("Start New Record")
