#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI PySide6 — Whisper + Pyannote (CLI driver)
Auteur : marcdelage
"""

import os
import sys
import shlex
from PySide6 import QtCore, QtGui, QtWidgets


# =========================
#   General configuration
# =========================

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whisperpyannote.py")

# Languages: (display label, code sent to CLI)
WHISPER_LANG_CHOICES = [
    ("Auto (detect)", "auto"),
    ("French", "fr"),
    ("English", "en"),
    ("German", "de"),
    ("Spanish", "es"),
    ("Italian", "it"),
    ("Portuguese", "pt"),
    ("Dutch", "nl"),
    ("Swedish", "sv"),
    ("Norwegian", "no"),
    ("Danish", "da"),
    ("Finnish", "fi"),
    ("Polish", "pl"),
    ("Czech", "cs"),
    ("Slovak", "sk"),
    ("Slovenian", "sl"),
    ("Hungarian", "hu"),
    ("Romanian", "ro"),
    ("Bulgarian", "bg"),
    ("Greek", "el"),
    ("Turkish", "tr"),
    ("Russian", "ru"),
    ("Ukrainian", "uk"),
    ("Arabic", "ar"),
    ("Hebrew", "he"),
    ("Persian", "fa"),
    ("Hindi", "hi"),
    ("Bengali", "bn"),
    ("Tamil", "ta"),
    ("Telugu", "te"),
    ("Urdu", "ur"),
    ("Chinese", "zh"),
    ("Japanese", "ja"),
    ("Korean", "ko"),
    ("Thai", "th"),
    ("Vietnamese", "vi"),
    ("Indonesian", "id"),
    ("Malay", "ms"),
]


# =========================
#   IMT palette (strict)
# =========================

IMT_CYAN   = "#00B8DE"
IMT_NAVY   = "#14223C"
IMT_WHITE  = "#FFFFFF"
IMT_LIGHT  = "#EDF3F4"
IMT_BLACK  = "#000000"
IMT_GRAY90 = "#3C3C3C"

# Aliases kept so nothing else breaks
IMT_BG     = IMT_LIGHT
IMT_TEXT   = IMT_BLACK
IMT_MUTED  = IMT_GRAY90
IMT_BORDER = IMT_NAVY
IMT_DARK   = IMT_NAVY
IMT_DARK2  = IMT_NAVY


def apply_imt_theme(app: QtWidgets.QApplication):
    qss = f"""
    * {{
        font-family: Helvetica, Arial, sans-serif;
        font-size: 13px;
        color: {IMT_BLACK};
    }}

    #Root {{
        background: {IMT_LIGHT};
    }}

    #Header, #Header * {{
        background: transparent;
    }}
    #Header {{
        background: {IMT_NAVY};
        border-radius: 18px;
    }}
    #HeaderText {{
        background: transparent;
        padding: 10px 14px;
    }}
    #HeaderTitle {{
        background: transparent;
        color: {IMT_WHITE};
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 0.2px;
    }}
    #HeaderSub {{
        background: transparent;
        color: {IMT_WHITE};
        font-size: 13px;
        font-weight: 700;
    }}
    #StatusPill {{
        background: transparent;
        border: 1px solid {IMT_WHITE};
        border-radius: 999px;
        padding: 7px 12px;
        color: {IMT_WHITE};
        font-weight: 900;
    }}

    #Card {{
        background: {IMT_WHITE};
        border: 1px solid {IMT_NAVY};
        border-radius: 18px;
    }}
    #CardTitle {{
        background: transparent;
        color: {IMT_NAVY};
        font-size: 13px;
        font-weight: 900;
    }}
    QLabel#Muted {{
        background: transparent;
        color: {IMT_GRAY90};
    }}

    QLineEdit, QComboBox {{
        background: {IMT_LIGHT};
        border: 1px solid {IMT_NAVY};
        border-radius: 14px;
        padding: 10px 12px;
    }}
    QLineEdit:focus, QComboBox:focus {{
        background: {IMT_WHITE};
        border: 1px solid {IMT_CYAN};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 36px;
        border-left: 1px solid {IMT_NAVY};
        border-top-right-radius: 14px;
        border-bottom-right-radius: 14px;
        background: {IMT_LIGHT};
    }}

    QPushButton {{
        border-radius: 14px;
        padding: 10px 14px;
        font-weight: 900;
        border: 1px solid {IMT_NAVY};
        background: {IMT_WHITE};
        color: {IMT_NAVY};
    }}
    QPushButton:hover {{ border: 1px solid {IMT_CYAN}; }}
    QPushButton:pressed {{ background: {IMT_LIGHT}; }}
    QPushButton:disabled {{
        color: {IMT_GRAY90};
        background: {IMT_LIGHT};
        border: 1px solid {IMT_LIGHT};
    }}
    QPushButton#Primary {{
        background: {IMT_CYAN};
        border: 1px solid {IMT_CYAN};
        color: {IMT_NAVY};
    }}
    QPushButton#Danger {{
        background: {IMT_NAVY};
        border: 1px solid {IMT_NAVY};
        color: {IMT_WHITE};
    }}
    QPushButton#Ghost {{
        background: transparent;
        border: 1px solid {IMT_NAVY};
        color: {IMT_NAVY};
    }}
    QPushButton#Ghost:hover {{
        border: 1px solid {IMT_CYAN};
        background: {IMT_LIGHT};
    }}

    #DropZone {{
        background: {IMT_WHITE};
        border: 2px dashed {IMT_NAVY};
        border-radius: 18px;
    }}
    #DropZone[active="true"] {{
        border: 2px dashed {IMT_CYAN};
        background: {IMT_LIGHT};
    }}
    #DropTitle {{
        background: transparent;
        font-size: 13px;
        font-weight: 900;
        color: {IMT_NAVY};
    }}
    #DropHint {{
        background: transparent;
        color: {IMT_GRAY90};
        font-weight: 700;
    }}

    QPlainTextEdit#Console {{
        background: {IMT_NAVY};
        border: 1px solid {IMT_NAVY};
        border-radius: 18px;
        color: {IMT_WHITE};
        padding: 16px;
        font-family: Menlo, Monaco, Consolas, "Liberation Mono", monospace;
        font-size: 12px;
    }}

    QProgressBar {{
        border: 1px solid {IMT_NAVY};
        border-radius: 999px;
        background: {IMT_LIGHT};
        height: 10px;
    }}
    QProgressBar::chunk {{
        border-radius: 999px;
        background: {IMT_CYAN};
    }}
    """
    app.setStyleSheet(qss)


# =========================
#   Drop zone widget
# =========================

class DropZone(QtWidgets.QFrame):
    fileDropped = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("DropZone")
        self.setProperty("active", "false")

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(6)

        icon = QtWidgets.QLabel("⬇︎")
        icon.setAlignment(QtCore.Qt.AlignCenter)
        icon.setStyleSheet(f"font-size: 22px; color: {IMT_CYAN}; font-weight: 900;")

        title = QtWidgets.QLabel("Drag & drop an audio/video file")
        title.setObjectName("DropTitle")
        title.setAlignment(QtCore.Qt.AlignCenter)

        hint = QtWidgets.QLabel('or click "Browse…"')
        hint.setObjectName("DropHint")
        hint.setAlignment(QtCore.Qt.AlignCenter)

        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(hint)

    def _set_active(self, active: bool):
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            self._set_active(True)
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dragLeaveEvent(self, e):
        self._set_active(False)
        super().dragLeaveEvent(e)

    def dropEvent(self, e):
        self._set_active(False)
        urls = e.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path:
                self.fileDropped.emit(path)


# =========================
#   UI card widget
# =========================

class Card(QtWidgets.QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("Card")
        self.v = QtWidgets.QVBoxLayout(self)
        self.v.setContentsMargins(16, 16, 16, 16)
        self.v.setSpacing(10)

        t = QtWidgets.QLabel(title)
        t.setObjectName("CardTitle")
        self.v.addWidget(t)


# =========================
#   Main window
# =========================

class Main(QtWidgets.QWidget):
    ORG = "marcdelage"
    APP = "whisperpyannote_gui"

    def __init__(self):
        super().__init__()
        self.setObjectName("Root")
        self.setWindowTitle("WhisperPyannote")
        self.resize(1120, 780)

        self.settings = QtCore.QSettings(self.ORG, self.APP)

        self.proc = QtCore.QProcess(self)
        self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        # ----- Header -----
        header = QtWidgets.QFrame()
        header.setObjectName("Header")
        hl = QtWidgets.QHBoxLayout(header)
        hl.setContentsMargins(18, 16, 18, 16)
        hl.setSpacing(12)

        header_text = QtWidgets.QFrame()
        header_text.setObjectName("HeaderText")
        tv = QtWidgets.QVBoxLayout(header_text)
        tv.setContentsMargins(10, 8, 10, 8)
        tv.setSpacing(2)

        title = QtWidgets.QLabel("WhisperPyannote")
        title.setObjectName("HeaderTitle")
        sub = QtWidgets.QLabel("Transcription + Diarization")
        sub.setObjectName("HeaderSub")
        tv.addWidget(title)
        tv.addWidget(sub)

        self.status_pill = QtWidgets.QLabel("Ready")
        self.status_pill.setObjectName("StatusPill")

        hl.addWidget(header_text)
        hl.addStretch(1)
        hl.addWidget(self.status_pill)

        # ----- Widgets -----
        self.input_path = QtWidgets.QLineEdit()
        self.input_path.setReadOnly(True)
        self.input_path.setPlaceholderText("No file selected")

        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output path… (e.g. /path/output.txt)")

        self.mode = QtWidgets.QComboBox()
        self.mode.addItem("Transcription + Diarization", "full")
        self.mode.addItem("Transcription", "transcription_only")
        self.mode.addItem("Diarization", "diarization_only")

        self.whisper_model = QtWidgets.QComboBox()
        self.whisper_model.addItem("Tiny", "tiny")
        self.whisper_model.addItem("Base", "base")
        self.whisper_model.addItem("Small", "small")
        self.whisper_model.addItem("Medium", "medium")
        self.whisper_model.addItem("Large", "large")
        self.whisper_model.addItem("Turbo", "turbo")

        self.lang = QtWidgets.QComboBox()
        for label, code in WHISPER_LANG_CHOICES:
            self.lang.addItem(label, code)

        self.hf_token = QtWidgets.QLineEdit()
        self.hf_token.setEchoMode(QtWidgets.QLineEdit.Password)
        self.hf_token.setPlaceholderText("Hugging Face token (for Pyannote)")

        self.keep_temp = QtWidgets.QCheckBox("Keep temporary files")
        self.auto_scroll = QtWidgets.QCheckBox("Auto-scroll logs")
        self.auto_scroll.setChecked(True)

        self.export_json = QtWidgets.QCheckBox("JSON")
        self.export_srt = QtWidgets.QCheckBox("SRT")
        self.export_vtt = QtWidgets.QCheckBox("VTT")
        self.subs_no_speaker = QtWidgets.QCheckBox("Subtitles without speaker labels")

        self.browse_btn = QtWidgets.QPushButton("Browse…")
        self.browse_btn.setObjectName("Ghost")
        self.save_btn = QtWidgets.QPushButton("Output…")
        self.save_btn.setObjectName("Ghost")

        self.start_btn = QtWidgets.QPushButton("▶ Start")
        self.start_btn.setObjectName("Primary")
        self.stop_btn = QtWidgets.QPushButton("⏹ Stop")
        self.stop_btn.setObjectName("Danger")
        self.stop_btn.setEnabled(False)

        self.reset_btn = QtWidgets.QPushButton("↺ Reset")
        self.reset_btn.setObjectName("Ghost")

        self.open_output_btn = QtWidgets.QPushButton("Open output")
        self.open_output_btn.setObjectName("Ghost")
        self.open_output_btn.setEnabled(False)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)

        self.console = QtWidgets.QPlainTextEdit()
        self.console.setObjectName("Console")
        self.console.setReadOnly(True)

        # ----- Layout -----
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)
        root.addWidget(header)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(14)

        c_file = Card("FILE")
        drop = DropZone()

        # Only change here: prevent overlap by allowing the DropZone to shrink/grow inside its layout
        drop.setMinimumHeight(140)
        drop.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        c_file.v.addWidget(drop)

        row_pick = QtWidgets.QHBoxLayout()
        row_pick.addWidget(self.input_path, 1)
        row_pick.addWidget(self.browse_btn)
        c_file.v.addLayout(row_pick)

        row_out = QtWidgets.QHBoxLayout()
        row_out.addWidget(self.output_path, 1)
        row_out.addWidget(self.save_btn)
        c_file.v.addLayout(row_out)

        hint = QtWidgets.QLabel("Tip: SRT/VTT/JSON are generated in addition to the .txt")
        hint.setObjectName("Muted")
        c_file.v.addWidget(hint)

        c_opts = Card("OPTIONS")
        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        grid.addWidget(QtWidgets.QLabel("Mode"), 0, 0)
        grid.addWidget(self.mode, 0, 1)

        grid.addWidget(QtWidgets.QLabel("Whisper model"), 1, 0)
        grid.addWidget(self.whisper_model, 1, 1)

        grid.addWidget(QtWidgets.QLabel("Language"), 2, 0)
        grid.addWidget(self.lang, 2, 1)

        grid.addWidget(QtWidgets.QLabel("HF token"), 3, 0)
        grid.addWidget(self.hf_token, 3, 1)

        grid.addWidget(self.keep_temp, 4, 0, 1, 2)
        grid.addWidget(self.auto_scroll, 5, 0, 1, 2)

        exp_box = QtWidgets.QVBoxLayout()
        exp_box.setSpacing(6)
        exp_box.addWidget(self.export_json)
        exp_box.addWidget(self.export_srt)
        exp_box.addWidget(self.export_vtt)
        exp_box.addWidget(self.subs_no_speaker)
        grid.addLayout(exp_box, 6, 0, 1, 2)

        c_opts.v.addLayout(grid)

        top_row.addWidget(c_file, 1, QtCore.Qt.AlignTop)
        top_row.addWidget(c_opts, 1, QtCore.Qt.AlignTop)
        root.addLayout(top_row, 0)

        c_actions = Card("ACTIONS")
        btns = QtWidgets.QHBoxLayout()
        btns.setSpacing(10)
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)
        btns.addWidget(self.reset_btn)
        btns.addWidget(self.open_output_btn)
        btns.addStretch(1)
        c_actions.v.addLayout(btns)
        c_actions.v.addWidget(self.progress)
        root.addWidget(c_actions, 0)

        c_logs = Card("Logs")
        c_logs.v.addWidget(self.console, 1)
        root.addWidget(c_logs, 1)

        # ----- Signals -----
        self.browse_btn.clicked.connect(self.pick_input)
        self.save_btn.clicked.connect(self.pick_output)
        drop.fileDropped.connect(self.set_input)

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.reset_btn.clicked.connect(self.reset_settings)
        self.open_output_btn.clicked.connect(self.open_output)

        self.proc.readyRead.connect(self._read)
        self.proc.finished.connect(self._finished)
        self.proc.errorOccurred.connect(self._proc_error)

        self.output_path.textChanged.connect(self._refresh_open_button)

        # ----- Restore prefs + detect capabilities -----
        self._restore_settings()
        self._detect_and_apply_script_capabilities()

        self._log("Ready.\n")

    # =============================
    #   Script capabilities detection
    # =============================

    def _script_path(self) -> str:
        return SCRIPT_PATH

    def _get_script_help(self) -> str:
        """
        Fetches help via "python script -h".
        Increased timeout because some scripts import heavy libs before argparse.
        """
        sp = self._script_path()
        if not os.path.exists(sp):
            self._log("[GUI] Script not found -> empty help")
            return ""

        p = QtCore.QProcess()
        p.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        p.start(sys.executable, [sp, "-h"])
        if not p.waitForStarted(3000):
            self._log(f"[GUI] Help: process did not start (python={sys.executable})")
            return ""

        if not p.waitForFinished(30000):
            self._log("[GUI] Help: timeout -> kill()")
            try:
                p.kill()
            except Exception:
                pass

        out = bytes(p.readAll()).decode("utf-8", "replace").strip()
        self._log(f"[GUI] Help: exitCode={p.exitCode()} exitStatus={p.exitStatus()}")
        if not out:
            self._log("[GUI] Help: captured empty output")

        return out

    def _detect_and_apply_script_capabilities(self):
        sp = self._script_path()
        self._log(f"[GUI] Using script path = {sp}")

        help_txt = self._get_script_help()
        if not help_txt:
            self._log("[GUI] Empty help -> cannot detect, keeping export options as-is.\n")
            return

        def supports(flag: str) -> bool:
            return (flag in help_txt) or (f"{flag}]" in help_txt) or (f"{flag} " in help_txt)

        self._set_export_enabled(self.export_json, supports("--json"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.export_srt, supports("--srt"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.export_vtt, supports("--vtt"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.subs_no_speaker, supports("--subs_no_speaker"), f"Option not supported by {os.path.basename(sp)}")

        self._log("\n[GUI] Detected capabilities:")
        self._log(f"  --json: {supports('--json')}")
        self._log(f"  --srt: {supports('--srt')}")
        self._log(f"  --vtt: {supports('--vtt')}")
        self._log(f"  --subs_no_speaker: {supports('--subs_no_speaker')}\n")

    def _set_export_enabled(self, cb: QtWidgets.QCheckBox, enabled: bool, disabled_tip: str):
        cb.setEnabled(enabled)
        if not enabled:
            cb.setChecked(False)
            cb.setToolTip(disabled_tip)
        else:
            cb.setToolTip("")

    # =========================
    #   Preferences (Settings)
    # =========================

    def _set_combo_by_data(self, combo: QtWidgets.QComboBox, data_value: str, fallback_data: str):
        for i in range(combo.count()):
            if combo.itemData(i) == data_value:
                combo.setCurrentIndex(i)
                return
        for i in range(combo.count()):
            if combo.itemData(i) == fallback_data:
                combo.setCurrentIndex(i)
                return

    def _restore_settings(self):
        geo = self.settings.value("window/geometry")
        if geo:
            try:
                self.restoreGeometry(geo)
            except Exception:
                pass

        self._set_combo_by_data(self.mode, self.settings.value("prefs/mode", "full"), "full")
        self._set_combo_by_data(self.whisper_model, self.settings.value("prefs/whisper_model", "turbo"), "turbo")
        self._set_combo_by_data(self.lang, self.settings.value("prefs/lang", "auto"), "auto")

        self.keep_temp.setChecked(self.settings.value("prefs/keep_temp", False, type=bool))
        self.auto_scroll.setChecked(self.settings.value("prefs/auto_scroll", True, type=bool))

        self.export_json.setChecked(self.settings.value("prefs/export_json", False, type=bool))
        self.export_srt.setChecked(self.settings.value("prefs/export_srt", False, type=bool))
        self.export_vtt.setChecked(self.settings.value("prefs/export_vtt", False, type=bool))
        self.subs_no_speaker.setChecked(self.settings.value("prefs/subs_no_speaker", False, type=bool))

        last_out = self.settings.value("prefs/last_output_path", "")
        if last_out:
            self.output_path.setText(last_out)

        tok = self.settings.value("prefs/hf_token", "")
        if tok:
            self.hf_token.setText(tok)

        self._refresh_open_button()

    def _save_settings(self):
        self.settings.setValue("window/geometry", self.saveGeometry())

        self.settings.setValue("prefs/mode", self.mode.currentData())
        self.settings.setValue("prefs/whisper_model", self.whisper_model.currentData())
        self.settings.setValue("prefs/lang", self.lang.currentData())

        self.settings.setValue("prefs/keep_temp", self.keep_temp.isChecked())
        self.settings.setValue("prefs/auto_scroll", self.auto_scroll.isChecked())

        self.settings.setValue("prefs/export_json", self.export_json.isChecked())
        self.settings.setValue("prefs/export_srt", self.export_srt.isChecked())
        self.settings.setValue("prefs/export_vtt", self.export_vtt.isChecked())
        self.settings.setValue("prefs/subs_no_speaker", self.subs_no_speaker.isChecked())

        self.settings.setValue("prefs/last_output_path", self.output_path.text().strip())
        self.settings.setValue("prefs/hf_token", self.hf_token.text().strip())
        self.settings.sync()

    def closeEvent(self, event):
        try:
            self._save_settings()
        except Exception:
            pass
        super().closeEvent(event)

    # =========================
    #   Reset
    # =========================

    def reset_settings(self):
        resp = QtWidgets.QMessageBox.question(
            self,
            "Réinitialiser",
            "Réinitialiser tous les réglages et effacer les préférences sauvegardées ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if resp != QtWidgets.QMessageBox.Yes:
            return

        if self.proc.state() != QtCore.QProcess.NotRunning:
            self.stop()

        try:
            self.settings.clear()
            self.settings.sync()
        except Exception:
            pass

        self.input_path.setText("")
        self.output_path.setText("")

        self._set_combo_by_data(self.mode, "full", "full")
        self._set_combo_by_data(self.whisper_model, "turbo", "turbo")
        self._set_combo_by_data(self.lang, "auto", "auto")

        self.hf_token.setText("")
        self.keep_temp.setChecked(False)
        self.auto_scroll.setChecked(True)

        self.export_json.setChecked(False)
        self.export_srt.setChecked(False)
        self.export_vtt.setChecked(False)
        self.subs_no_speaker.setChecked(False)

        self._detect_and_apply_script_capabilities()

        self.console.clear()
        self.progress.setVisible(False)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.reset_btn.setEnabled(True)
        self.open_output_btn.setEnabled(False)
        self._set_status("Ready")
        self._log("↺ Settings reset.\n")

    # =========================
    #   UX: status / logs
    # =========================

    def _refresh_open_button(self):
        outp = self.output_path.text().strip()
        self.open_output_btn.setEnabled(bool(outp) and os.path.exists(outp))

    def _set_status(self, s: str):
        self.status_pill.setText(s)

    def _log(self, s: str):
        self.console.appendPlainText(s.rstrip("\n"))
        if self.auto_scroll.isChecked():
            cursor = self.console.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.console.setTextCursor(cursor)

    def _format_cmd_for_log(self, args):
        return " ".join(shlex.quote(a) for a in args)

    # =========================
    #   File pickers
    # =========================

    def pick_input(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier audio/vidéo",
            "",
            "Audio/Vidéo (*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.mp4 *.mkv *.mov *.avi *.webm);;Tous (*.*)",
        )
        if path:
            self.set_input(path)

    def set_input(self, path: str):
        self.input_path.setText(path)
        if not self.output_path.text().strip():
            base, _ = os.path.splitext(path)
            self.output_path.setText(base + ".txt")
        self._refresh_open_button()

    def pick_output(self):
        suggested = self.output_path.text().strip() or "output.txt"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Choisir le fichier de sortie",
            suggested,
            "TXT (*.txt);;Tous (*.*)",
        )
        if path:
            self.output_path.setText(path)
            self._refresh_open_button()

    def open_output(self):
        outp = self.output_path.text().strip()
        if not outp or not os.path.exists(outp):
            QtWidgets.QMessageBox.information(self, "Info", "Le fichier de sortie n'existe pas encore.")
            self._refresh_open_button()
            return
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(outp))

    # =========================
    #   Process: build args
    # =========================

    def build_args(self):
        inp = self.input_path.text().strip()
        outp = self.output_path.text().strip()
        sp = self._script_path()

        if not os.path.exists(sp):
            raise RuntimeError(f"Script introuvable: {sp}")
        if not inp or not os.path.exists(inp):
            raise RuntimeError("Entrée invalide (fichier manquant).")
        if not outp:
            raise RuntimeError("Sortie manquante.")

        out_dir = os.path.dirname(outp)
        if out_dir and not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                raise RuntimeError(f"Impossible de créer le dossier de sortie: {out_dir}\n{e}")

        args = [sys.executable, sp, inp, outp]

        args += ["--whisper_model", str(self.whisper_model.currentData())]

        lang_code = str(self.lang.currentData() or "auto")
        if lang_code != "auto":
            args += ["--language", lang_code]

        if self.keep_temp.isChecked():
            args += ["--keep_temp"]

        mode_val = self.mode.currentData()
        if mode_val == "transcription_only":
            args += ["--transcription_only"]
        elif mode_val == "diarization_only":
            args += ["--diarization_only"]

        tok = self.hf_token.text().strip()
        if tok:
            args += ["--hf_token", tok]

        if self.export_json.isEnabled() and self.export_json.isChecked():
            args += ["--json"]
        if self.export_srt.isEnabled() and self.export_srt.isChecked():
            args += ["--srt"]
        if self.export_vtt.isEnabled() and self.export_vtt.isChecked():
            args += ["--vtt"]
        if self.subs_no_speaker.isEnabled() and self.subs_no_speaker.isChecked():
            args += ["--subs_no_speaker"]

        return args

    # =========================
    #   Process: start/stop
    # =========================

    def start(self):
        if self.proc.state() != QtCore.QProcess.NotRunning:
            return

        try:
            args = self.build_args()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))
            return

        try:
            self._save_settings()
        except Exception:
            pass

        self.open_output_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.reset_btn.setEnabled(False)
        self.progress.setVisible(True)
        self._set_status("Running…")

        self._log("\n" + "=" * 72)
        self._log("▶ Launch:")
        self._log(self._format_cmd_for_log(args))

        self.proc.start(args[0], args[1:])
        if not self.proc.waitForStarted(3000):
            self._log("❌ Failed to start process.")
            self._restore_ui_after_run(error=True)

    def stop(self):
        if self.proc.state() == QtCore.QProcess.NotRunning:
            return
        self._log("⏹ Stop requested…")
        self._set_status("Stopping…")
        self.proc.terminate()
        QtCore.QTimer.singleShot(2500, self._kill_if_needed)

    def _kill_if_needed(self):
        if self.proc.state() != QtCore.QProcess.NotRunning:
            self._log("⚠️ Process not responding -> kill()")
            self.proc.kill()

    def _restore_ui_after_run(self, error: bool):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.reset_btn.setEnabled(True)
        self.progress.setVisible(False)
        self._set_status("Error" if error else "Done")
        self._refresh_open_button()

    # =========================
    #   Process: logs
    # =========================

    def _read(self):
        data = bytes(self.proc.readAll()).decode("utf-8", errors="replace")
        if data:
            for line in data.splitlines():
                self._log(line)

    def _proc_error(self, err: QtCore.QProcess.ProcessError):
        self._log(f"❌ QProcess error: {err}")

    def _finished(self, code, status):
        self._log(f"\n✅ Finished (code={code}).")
        self._restore_ui_after_run(error=(code != 0))


# =========================
#   Entry point
# =========================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_imt_theme(app)

    w = Main()
    w.show()

    sys.exit(app.exec())
