# ---------- Base libraries -------------------------------------------------------------------------------------------
import os
from os.path import isdir
from typing import List
import tempfile
import logging

import platform
import subprocess
from datetime import datetime
#from pathlib import Path

from CoreCodes.Wav_prediction import InfluenzaClassifier

# ---------- Numerical, Visual packages--------------------------------------------------------------------------------
from PIL import Image
import numpy as np
import pyqtgraph as pg

# ---------- GUI libraries --------------------------------------------------------------------------------------------
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt  # pQModelIndex, QDir,
# from PySide6.QtGui import QKeySequence, QShortcut, QColor
from Custom_UIs.UI_Mainwindow import Ui_MainWindow      # ---------- UI from qt-designer ------------------------------

# =====================================================================================================================
# pyqtgraph config
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

logging.basicConfig(
    filename=os.path.join(tempfile.gettempdir(), datetime.now().strftime("Influenza_gui_%Y%m%d_%H%M%S.log")),
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
)

def open_file_externally(system_str, filepath: str) -> None:
    """Opens given file externally, without hanging current running python script."""
    try:
        if system_str == "Windows":   # Windows
            os.startfile(filepath)    # type: ignore
        elif system_str == "Darwin":  # BSDs and macos
            subprocess.Popen(("open ", filepath), stdin=None, stdout=None, stderr=None, close_fds=True)  # shell=True,
        elif system_str == "Linux":   # linux variants
            subprocess.Popen(
                ("xdg-open", os.path.abspath(filepath)),  # shell=True,
                stdin=None,
                stdout=None,
                stderr=None,
                close_fds=True,
            )
        else:
            logging.warning(f"Strange os-platform string id: {system_str}")
            logging.warning(" - Cannot open file")
        return None
    except Exception as e:
        logging.warning(f"error when openning {filepath}:\n{e}")
        return None

class TheMainWindow(QMainWindow):
    inf_classifier: InfluenzaClassifier
    pred_label: str
    pred_confidence: List[float]
    output_directory: str  = tempfile.gettempdir()
    os_name: str           = platform.system() # get the name of OS, Windows, Darwin, Linux

    def __init__(self, parent: QWidget | None = None) -> None:
        super(TheMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pb_load_audio_file.clicked.connect(self.callback_pb_load_audio_file)
        self.ui.pb_start_record.clicked.connect(self.callback_pb_start_record)
        self.ui.actionChange_Pre_Trained_Model.triggered.connect(self.callback_change_pretrained_data)
        self.ui.actionChange_Output_Directory.triggered.connect(self.callback_change_output_directory)
        self.ui.actionOpen_Output_Directory.triggered.connect(
            lambda: open_file_externally(self.os_name, self.output_directory))
        # self.ui.pb_process.clicked.connect(self.call_process)

        self.inf_classifier = InfluenzaClassifier("./CoreCodes/best_checkpoint_2_class_masked_5_17.model")
        logging.info("TheMainWindow: Done")


    def callback_pb_load_audio_file(self) -> None:
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setNameFilters(["Other File (*)", "Audio (*.wav)"])
        dlg.selectNameFilter("Audio (*.wav)")

        if dlg.exec_():
            selected_file_path = dlg.selectedFiles()[0]
            self.load_audio_file(selected_file_path)
            logging.info(f"callback_pb_load_audio_file: {selected_file_path=}")
        else:
            logging.info("callback_pb_load_audio_file: Canceled Dialog")

    def load_audio_file(self, file_path_to_wav: str) -> None:
        # load {file_path_to_wav} generate image.
        # save generated image into {self.inf_classifier.output_path_spectrogram_img}
        self.inf_classifier.generate_spectrogram_from_wav_file(file_path_to_wav, "/tmp/")
        logging.info("load_audio_file: generate_spectrogram_from_wav_file")

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
        logging.info("update_graph_on_ui: plotted wav graph")

        im = Image.open(self.inf_classifier.output_path_spectrogram_img)
        if im.mode == "RGBA":
            im = im.convert("RGB")

        # update graph2 (image)
        self.ui.pyqt_graph_audio_2.clear()
        self.ui.pyqt_graph_audio_2.setImage(img=np.array(im), levels=(0, 255), axes={"x": 1, "y": 0, "c": 2})
        logging.info("update_graph_on_ui: showed spectrograph image")

        self.predict_and_then_update_result_ui()

    def callback_pb_start_record(self) -> None:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Record...")
        dlg.setText("Start after pressing OK")
        dlg.exec()

        logging.info("callback_pb_start_record: Starting Record")

        file_path_wav_output = self.inf_classifier.record_audio(
            output_directory=self.output_directory,
            output_filename=datetime.now().strftime("%Y%m%d_%H%M%S.wav"),
            duration=10,
            sample_rate=44100,
            channels=1,
        )
        logging.info("callback_pb_start_record: Finishing Record")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Record...")
        dlg.setText("Finshed")
        dlg.exec()

        self.load_audio_file(file_path_wav_output)
        #self.predict_and_then_update_result_ui() already executed inside of  self.load_audio_file

        self.ui.pb_start_record.setText("Start New Record")

    def predict_and_then_update_result_ui(self) -> None:
        self.pred_label, self.pred_confidence = self.inf_classifier.predict_image(
            self.inf_classifier.output_path_spectrogram_img,
        )
        logging.info("predict_and_then_update_result_ui: predicted")
        self.ui.label_result.setText(self.pred_label)
        self.ui.label_result_confidence.setText(
            f"[{self.pred_confidence[0]:.2f}~{self.pred_confidence[1]:.2f}]"
        )
        logging.info("predict_and_then_update_result_ui: Labels showed")


        dlg = QMessageBox(self)
        dlg.setWindowTitle("Result")
        dlg.setText(
            f"Prediction Finished Result: {self.pred_label}"
        )
        dlg.exec()

    def callback_change_pretrained_data(self) -> None:
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setNameFilters(["Other File (*)", "Model (*.model)"])
        dlg.selectNameFilter("Model (*.model)")
        logging.info("callback_change_pretrained_data: File dialog start")
        retval = dlg.exec_()

        if not retval: # if pressed cancel
            logging.info("callback_change_pretrained_data: File dialog CANCEL")
            return

        # file has selected
        selected_file_path_for_model = dlg.selectedFiles()[0]
        try:
            self.inf_classifier.load_pre_trained_model(selected_file_path_for_model, True)
            logging.info(f"callback_change_pretrained_data: OK {selected_file_path_for_model}")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Success")
            dlg.setText(f"Loaded new file at {selected_file_path_for_model}")
            dlg.exec()

        except Exception:
            logging.info(f"callback_change_pretrained_data: FAIL {selected_file_path_for_model}")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Problem")
            dlg.setText(f"Problem while loading {selected_file_path_for_model}")
            dlg.exec()

    def callback_change_output_directory(self) -> None:
        """Changes output file directory"""
        file: str = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(file, type(file))

        if file == "":
            logging.info("callback_change_output_directory: CANCEL-ed")
            return

        self.output_directory = file
