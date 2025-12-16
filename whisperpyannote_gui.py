#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI PySide6 — Whisper + Pyannote (CLI driver)
Auteur : marcdelage
"""

import os
import sys
import shlex
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets


# =========================
#   I18N (FR / EN)
# =========================

I18N = {
    "fr": {
        "app_title": "WhisperPyannote",
        "app_sub": "Transcription + Diarisation",
        "status_ready": "Prêt",
        "status_running": "En cours…",
        "status_stopping": "Arrêt…",
        "status_done": "Terminé",
        "status_error": "Erreur",

        "card_file": "FICHIER",
        "card_options": "OPTIONS",
        "card_actions": "ACTIONS",
        "card_logs": "Logs",

        "drop_title": "Glissez-déposez un fichier audio/vidéo",
        "drop_hint": 'ou cliquez sur "Parcourir…"',

        "btn_browse": "Parcourir…",
        "btn_output": "Sortie…",
        "btn_start": "▶ Démarrer",
        "btn_stop": "⏹ Stop",
        "btn_reset": "↺ Réinitialiser",
        "btn_open_output": "Ouvrir la sortie",

        "lbl_mode": "Mode",
        "lbl_whisper_model": "Modèle Whisper",
        "lbl_language": "Langue",
        "lbl_hf_token": "Token HF",

        "tip_exports": "Astuce : SRT/VTT/JSON sont générés en plus du .txt",

        "dlg_reset_title": "Réinitialiser",
        "dlg_reset_body": "Réinitialiser tous les réglages et effacer les préférences sauvegardées ?",

        "dlg_pick_input_title": "Choisir un fichier audio/vidéo",
        "dlg_pick_input_filter": "Audio/Vidéo (*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.mp4 *.mkv *.mov *.avi *.webm);;Tous (*.*)",
        "dlg_pick_output_title": "Choisir le fichier de sortie",
        "dlg_pick_output_filter": "TXT (*.txt);;Tous (*.*)",

        "msg_error_title": "Erreur",
        "msg_info_title": "Info",
        "msg_output_missing": "Le fichier de sortie n'existe pas encore.",

        "err_script_missing": "Script introuvable : {sp}",
        "err_invalid_input": "Entrée invalide (fichier manquant).",
        "err_missing_output": "Sortie manquante.",

        "log_ready": "Prêt.\n",
        "log_reset_done": "↺ Réglages réinitialisés.\n",
        "log_stop_requested": "⏹ Arrêt demandé…",
        "log_kill": "⚠️ Process not responding -> kill()",
        "log_failed_start": "❌ Failed to start process.",
        "log_finished": "✅ Terminé (code={code}).",
        "log_launch": "▶ Lancement:",
        "log_script_not_found": "[GUI] Script introuvable -> empty help",
        "log_help_start_fail": "[GUI] Help: process did not start (python={py})",
        "log_help_timeout": "[GUI] Help: timeout -> kill()",
        "log_help_exit": "[GUI] Help: exitCode={code} exitStatus={status}",
        "log_help_empty": "[GUI] Help: captured empty output",
        "log_using_script": "[GUI] Using script path = {sp}",
        "log_empty_help": "[GUI] Empty help -> cannot detect, keeping export options as-is.\n",
        "log_detected_caps": "[GUI] Detected capabilities:",
        "log_caps_json": "  --json: {v}",
        "log_caps_srt": "  --srt: {v}",
        "log_caps_vtt": "  --vtt: {v}",
        "log_caps_subs": "  --subs_no_speaker: {v}",
        "log_qprocess_error": "❌ QProcess error: {err}",
    },
    "en": {
        "app_title": "WhisperPyannote",
        "app_sub": "Transcription + Diarization",
        "status_ready": "Ready",
        "status_running": "Running…",
        "status_stopping": "Stopping…",
        "status_done": "Done",
        "status_error": "Error",

        "card_file": "FILE",
        "card_options": "OPTIONS",
        "card_actions": "ACTIONS",
        "card_logs": "Logs",

        "drop_title": "Drag & drop an audio/video file",
        "drop_hint": 'or click "Browse…"',

        "btn_browse": "Browse…",
        "btn_output": "Output…",
        "btn_start": "▶ Start",
        "btn_stop": "⏹ Stop",
        "btn_reset": "↺ Reset",
        "btn_open_output": "Open output",

        "lbl_mode": "Mode",
        "lbl_whisper_model": "Whisper model",
        "lbl_language": "Language",
        "lbl_hf_token": "HF token",

        "tip_exports": "Tip: SRT/VTT/JSON are generated in addition to the .txt",

        "dlg_reset_title": "Reset",
        "dlg_reset_body": "Reset all settings and clear saved preferences?",

        "dlg_pick_input_title": "Choose an audio/video file",
        "dlg_pick_input_filter": "Audio/Video (*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.mp4 *.mkv *.mov *.avi *.webm);;All (*.*)",
        "dlg_pick_output_title": "Choose output file",
        "dlg_pick_output_filter": "TXT (*.txt);;All (*.*)",

        "msg_error_title": "Error",
        "msg_info_title": "Info",
        "msg_output_missing": "The output file does not exist yet.",

        "err_script_missing": "Script not found: {sp}",
        "err_invalid_input": "Invalid input (missing file).",
        "err_missing_output": "Missing output.",

        "log_ready": "Ready.\n",
        "log_reset_done": "↺ Settings reset.\n",
        "log_stop_requested": "⏹ Stop requested…",
        "log_kill": "⚠️ Process not responding -> kill()",
        "log_failed_start": "❌ Failed to start process.",
        "log_finished": "✅ Finished (code={code}).",
        "log_launch": "▶ Launch:",
        "log_script_not_found": "[GUI] Script not found -> empty help",
        "log_help_start_fail": "[GUI] Help: process did not start (python={py})",
        "log_help_timeout": "[GUI] Help: timeout -> kill()",
        "log_help_exit": "[GUI] Help: exitCode={code} exitStatus={status}",
        "log_help_empty": "[GUI] Help: captured empty output",
        "log_using_script": "[GUI] Using script path = {sp}",
        "log_empty_help": "[GUI] Empty help -> cannot detect, keeping export options as-is.\n",
        "log_detected_caps": "[GUI] Detected capabilities:",
        "log_caps_json": "  --json: {v}",
        "log_caps_srt": "  --srt: {v}",
        "log_caps_vtt": "  --vtt: {v}",
        "log_caps_subs": "  --subs_no_speaker: {v}",
        "log_qprocess_error": "❌ QProcess error: {err}",
    },
}


def _ts() -> str:
    return datetime.now().strftime("[%H:%M:%S]")


# =========================
#   General configuration
# =========================

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whisperpyannote.py")

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
        padding: 6px 10px;
        min-height: 34px;
        color: {IMT_BLACK};
    }}
    QLineEdit:focus, QComboBox:focus {{
        background: {IMT_WHITE};
        border: 1px solid {IMT_CYAN};
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 32px;
        border-left: 1px solid {IMT_NAVY};
        background: {IMT_LIGHT};
    }}

    /* (On garde ce style, mais le FIX principal est côté Python via setView + palette) */
    QListView#ComboPopup {{
        background: {IMT_WHITE};
        color: {IMT_BLACK};
        border: 1px solid {IMT_NAVY};
        outline: 0;
    }}
    QListView#ComboPopup::item {{
        padding: 6px 10px;
        background: {IMT_WHITE};
        color: {IMT_BLACK};
    }}
    QListView#ComboPopup::item:hover {{
        background: {IMT_LIGHT};
        color: {IMT_BLACK};
    }}
    QListView#ComboPopup::item:selected {{
        background: {IMT_CYAN};
        color: {IMT_NAVY};
    }}

    QCheckBox {{
        spacing: 8px;
        font-weight: 700;
        color: {IMT_BLACK};
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {IMT_NAVY};
        background: {IMT_WHITE};
    }}
    QCheckBox::indicator:checked {{
        background: {IMT_CYAN};
    }}
    QCheckBox::indicator:disabled {{
        border: 1px solid {IMT_LIGHT};
        background: {IMT_LIGHT};
    }}

    QPushButton {{
        border-radius: 14px;
        padding: 6px 12px;
        min-height: 34px;
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

    QPushButton#LangToggle {{
        background: transparent;
        border: 1px solid {IMT_WHITE};
        color: {IMT_WHITE};
        font-weight: 900;
        min-height: 28px;
        padding: 6px 10px;
    }}
    QPushButton#LangToggle:hover {{
        border: 1px solid {IMT_CYAN};
        background: rgba(255,255,255,0.08);
        color: {IMT_WHITE};
    }}
    QPushButton#LangToggle:pressed {{
        background: rgba(255,255,255,0.14);
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
        min-height: 10px;
    }}
    QProgressBar::chunk {{
        border-radius: 999px;
        background: {IMT_CYAN};
    }}

    /* =========================================================
       STRICT: remove ALL rounding (override specific selectors)
       ========================================================= */
    * {{ border-radius: 0px !important; }}
    *::chunk,
    *::handle,
    *::indicator,
    *::drop-down,
    *::item,
    *::tab,
    *::title {{ border-radius: 0px !important; }}

    #Header {{ border-radius: 0px !important; }}
    #StatusPill {{ border-radius: 0px !important; }}
    #Card {{ border-radius: 0px !important; }}
    #DropZone {{ border-radius: 0px !important; }}
    QPlainTextEdit#Console {{ border-radius: 0px !important; }}

    QLineEdit, QComboBox {{ border-radius: 0px !important; }}
    QComboBox::drop-down {{
        border-top-right-radius: 0px !important;
        border-bottom-right-radius: 0px !important;
        border-radius: 0px !important;
    }}

    QPushButton {{ border-radius: 0px !important; }}
    QProgressBar {{ border-radius: 0px !important; }}
    QProgressBar::chunk {{ border-radius: 0px !important; }}
    """
    app.setStyleSheet(qss)


# =========================
#   Drop zone widget
# =========================

class DropZone(QtWidgets.QFrame):
    fileDropped = QtCore.Signal(str)

    def __init__(self, tr_callable):
        super().__init__()
        self._tr = tr_callable

        self.setAcceptDrops(True)
        self.setObjectName("DropZone")
        self.setProperty("active", "false")

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(6)

        icon = QtWidgets.QLabel("⬇︎")
        icon.setAlignment(QtCore.Qt.AlignCenter)
        icon.setStyleSheet(f"font-size: 22px; color: {IMT_CYAN}; font-weight: 900;")

        self.title_lbl = QtWidgets.QLabel("")
        self.title_lbl.setObjectName("DropTitle")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.hint_lbl = QtWidgets.QLabel("")
        self.hint_lbl.setObjectName("DropHint")
        self.hint_lbl.setAlignment(QtCore.Qt.AlignCenter)

        lay.addWidget(icon)
        lay.addWidget(self.title_lbl)
        lay.addWidget(self.hint_lbl)

        self.retranslate()

    def retranslate(self):
        self.title_lbl.setText(self._tr("drop_title"))
        self.hint_lbl.setText(self._tr("drop_hint"))

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

        self.t = QtWidgets.QLabel(title)
        self.t.setObjectName("CardTitle")
        self.v.addWidget(self.t)

    def setTitle(self, title: str):
        self.t.setText(title)


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
        self.ui_lang = self.settings.value("ui/lang", "fr")
        if self.ui_lang not in ("fr", "en"):
            self.ui_lang = "fr"

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

        self.title_lbl = QtWidgets.QLabel(self.tr("app_title"))
        self.title_lbl.setObjectName("HeaderTitle")
        self.sub_lbl = QtWidgets.QLabel(self.tr("app_sub"))
        self.sub_lbl.setObjectName("HeaderSub")
        tv.addWidget(self.title_lbl)
        tv.addWidget(self.sub_lbl)

        self.status_pill = QtWidgets.QLabel(self.tr("status_ready"))
        self.status_pill.setObjectName("StatusPill")

        self.lang_btn = QtWidgets.QPushButton(self.ui_lang.upper())
        self.lang_btn.setObjectName("LangToggle")
        self.lang_btn.setFixedWidth(62)
        self.lang_btn.clicked.connect(self.toggle_lang)

        hl.addWidget(header_text)
        hl.addStretch(1)
        hl.addWidget(self.lang_btn)
        hl.addWidget(self.status_pill)

        # ----- Widgets -----
        self.input_path = QtWidgets.QLineEdit()
        self.input_path.setReadOnly(True)
        self.input_path.setPlaceholderText("No file selected")
        self.input_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.output_path = QtWidgets.QLineEdit()
        self.output_path.setPlaceholderText("Output path… (e.g. /path/output.txt)")
        self.output_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

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

        # ✅ FIX robuste: forcer view + palette pour rendre le popup visible partout
        self._force_combo_popup_visible(self.mode)
        self._force_combo_popup_visible(self.whisper_model)
        self._force_combo_popup_visible(self.lang)

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

        self.browse_btn = QtWidgets.QPushButton(self.tr("btn_browse"))
        self.browse_btn.setObjectName("Ghost")
        self.save_btn = QtWidgets.QPushButton(self.tr("btn_output"))
        self.save_btn.setObjectName("Ghost")

        BTN_W = 128
        self.browse_btn.setFixedWidth(BTN_W)
        self.save_btn.setFixedWidth(BTN_W)

        self.start_btn = QtWidgets.QPushButton(self.tr("btn_start"))
        self.start_btn.setObjectName("Primary")
        self.stop_btn = QtWidgets.QPushButton(self.tr("btn_stop"))
        self.stop_btn.setObjectName("Danger")
        self.stop_btn.setEnabled(False)

        self.reset_btn = QtWidgets.QPushButton(self.tr("btn_reset"))
        self.reset_btn.setObjectName("Ghost")

        self.open_output_btn = QtWidgets.QPushButton(self.tr("btn_open_output"))
        self.open_output_btn.setObjectName("Ghost")
        self.open_output_btn.setEnabled(False)

        for b in (self.start_btn, self.stop_btn, self.reset_btn, self.open_output_btn):
            b.setMinimumHeight(34)

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

        self.c_file = Card(self.tr("card_file"))
        drop = DropZone(self.tr)

        drop.setMinimumHeight(140)
        drop.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.c_file.v.addWidget(drop)

        row_pick = QtWidgets.QHBoxLayout()
        row_pick.addWidget(self.input_path, 1)
        row_pick.addWidget(self.browse_btn)
        self.c_file.v.addLayout(row_pick)

        row_out = QtWidgets.QHBoxLayout()
        row_out.addWidget(self.output_path, 1)
        row_out.addWidget(self.save_btn)
        self.c_file.v.addLayout(row_out)

        self.hint = QtWidgets.QLabel(self.tr("tip_exports"))
        self.hint.setObjectName("Muted")
        self.c_file.v.addWidget(self.hint)

        self.c_opts = Card(self.tr("card_options"))
        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        self.lbl_mode = QtWidgets.QLabel(self.tr("lbl_mode"))
        grid.addWidget(self.lbl_mode, 0, 0)
        grid.addWidget(self.mode, 0, 1)

        self.lbl_whisper_model = QtWidgets.QLabel(self.tr("lbl_whisper_model"))
        grid.addWidget(self.lbl_whisper_model, 1, 0)
        grid.addWidget(self.whisper_model, 1, 1)

        self.lbl_language = QtWidgets.QLabel(self.tr("lbl_language"))
        grid.addWidget(self.lbl_language, 2, 0)
        grid.addWidget(self.lang, 2, 1)

        self.lbl_hf = QtWidgets.QLabel(self.tr("lbl_hf_token"))
        grid.addWidget(self.lbl_hf, 3, 0)
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

        self.c_opts.v.addLayout(grid)

        self.c_file.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.c_opts.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        top_row.addWidget(self.c_file, 1)
        top_row.addWidget(self.c_opts, 1)
        root.addLayout(top_row, 0)

        self.c_actions = Card(self.tr("card_actions"))
        btns = QtWidgets.QHBoxLayout()
        btns.setSpacing(10)
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)
        btns.addWidget(self.reset_btn)
        btns.addWidget(self.open_output_btn)
        btns.addStretch(1)
        self.c_actions.v.addLayout(btns)
        self.c_actions.v.addWidget(self.progress)
        root.addWidget(self.c_actions, 0)

        self.c_logs = Card(self.tr("card_logs"))
        self.c_logs.v.addWidget(self.console, 1)
        root.addWidget(self.c_logs, 1)

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

        self._log(self.tr("log_ready"))

    # =========================
    #   Combo popup hard-fix
    # =========================

    def _force_combo_popup_visible(self, combo: QtWidgets.QComboBox):
        # Force a dedicated QListView so the popup is not "weird" on some platforms/styles
        view = QtWidgets.QListView()
        view.setObjectName("ComboPopup")
        view.setUniformItemSizes(True)
        view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        view.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Force palette (this fixes "list exists but invisible")
        pal = view.palette()
        pal.setColor(QtGui.QPalette.Base, QtGui.QColor(IMT_WHITE))
        pal.setColor(QtGui.QPalette.Window, QtGui.QColor(IMT_WHITE))
        pal.setColor(QtGui.QPalette.Text, QtGui.QColor(IMT_BLACK))
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(IMT_BLACK))
        pal.setColor(QtGui.QPalette.Highlight, QtGui.QColor(IMT_CYAN))
        pal.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(IMT_NAVY))
        view.setPalette(pal)

        # Ensure it behaves like a popup window
        view.setWindowFlag(QtCore.Qt.Popup, True)

        combo.setView(view)

    # =========================
    #   I18N helpers
    # =========================

    def tr(self, key: str) -> str:
        return I18N.get(self.ui_lang, I18N["fr"]).get(key, key)

    def toggle_lang(self):
        self.ui_lang = "en" if self.ui_lang == "fr" else "fr"
        self.lang_btn.setText(self.ui_lang.upper())
        self.settings.setValue("ui/lang", self.ui_lang)
        self.settings.sync()
        self._apply_i18n()

    def _apply_i18n(self):
        self.setWindowTitle(self.tr("app_title"))
        self.title_lbl.setText(self.tr("app_title"))
        self.sub_lbl.setText(self.tr("app_sub"))

        self.c_file.setTitle(self.tr("card_file"))
        self.c_opts.setTitle(self.tr("card_options"))
        self.c_actions.setTitle(self.tr("card_actions"))
        self.c_logs.setTitle(self.tr("card_logs"))

        self.hint.setText(self.tr("tip_exports"))

        self.lbl_mode.setText(self.tr("lbl_mode"))
        self.lbl_whisper_model.setText(self.tr("lbl_whisper_model"))
        self.lbl_language.setText(self.tr("lbl_language"))
        self.lbl_hf.setText(self.tr("lbl_hf_token"))

        self.browse_btn.setText(self.tr("btn_browse"))
        self.save_btn.setText(self.tr("btn_output"))
        self.start_btn.setText(self.tr("btn_start"))
        self.stop_btn.setText(self.tr("btn_stop"))
        self.reset_btn.setText(self.tr("btn_reset"))
        self.open_output_btn.setText(self.tr("btn_open_output"))

        if self.proc.state() == QtCore.QProcess.NotRunning:
            cur = self.status_pill.text().strip()
            if cur in ("Ready", "Prêt"):
                self._set_status(self.tr("status_ready"))

    # =============================
    #   Script capabilities detection
    # =============================

    def _script_path(self) -> str:
        return SCRIPT_PATH

    def _get_script_help(self) -> str:
        sp = self._script_path()
        if not os.path.exists(sp):
            self._log(self.tr("log_script_not_found"))
            return ""

        p = QtCore.QProcess()
        p.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        p.start(sys.executable, [sp, "-h"])
        if not p.waitForStarted(3000):
            self._log(self.tr("log_help_start_fail").format(py=sys.executable))
            return ""

        if not p.waitForFinished(30000):
            self._log(self.tr("log_help_timeout"))
            try:
                p.kill()
            except Exception:
                pass

        out = bytes(p.readAll()).decode("utf-8", "replace").strip()
        self._log(self.tr("log_help_exit").format(code=p.exitCode(), status=p.exitStatus()))
        if not out:
            self._log(self.tr("log_help_empty"))

        return out

    def _detect_and_apply_script_capabilities(self):
        sp = self._script_path()
        self._log(self.tr("log_using_script").format(sp=sp))

        help_txt = self._get_script_help()
        if not help_txt:
            self._log(self.tr("log_empty_help"))
            return

        def supports(flag: str) -> bool:
            return (flag in help_txt) or (f"{flag}]" in help_txt) or (f"{flag} " in help_txt)

        self._set_export_enabled(self.export_json, supports("--json"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.export_srt, supports("--srt"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.export_vtt, supports("--vtt"), f"Option not supported by {os.path.basename(sp)}")
        self._set_export_enabled(self.subs_no_speaker, supports("--subs_no_speaker"), f"Option not supported by {os.path.basename(sp)}")

        self._log("\n" + self.tr("log_detected_caps"))
        self._log(self.tr("log_caps_json").format(v=supports("--json")))
        self._log(self.tr("log_caps_srt").format(v=supports("--srt")))
        self._log(self.tr("log_caps_vtt").format(v=supports("--vtt")))
        self._log(self.tr("log_caps_subs").format(v=supports("--subs_no_speaker")) + "\n")

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

        self.lang_btn.setText(self.ui_lang.upper())
        self._apply_i18n()
        self._set_status(self.tr("status_ready"))

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
        self.settings.setValue("ui/lang", self.ui_lang)
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
            self.tr("dlg_reset_title"),
            self.tr("dlg_reset_body"),
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

        self.settings.setValue("ui/lang", self.ui_lang)

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
        self._set_status(self.tr("status_ready"))
        self._log(self.tr("log_reset_done"))

    # =========================
    #   UX: status / logs
    # =========================

    def _refresh_open_button(self):
        outp = self.output_path.text().strip()
        self.open_output_btn.setEnabled(bool(outp) and os.path.exists(outp))

    def _set_status(self, s: str):
        self.status_pill.setText(s)

    def _log(self, s: str):
        s = s.rstrip("\n")
        if not s:
            return
        for line in s.splitlines():
            self.console.appendPlainText(f"{_ts()} {line}")
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
            self.tr("dlg_pick_input_title"),
            "",
            self.tr("dlg_pick_input_filter"),
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
            self.tr("dlg_pick_output_title"),
            suggested,
            self.tr("dlg_pick_output_filter"),
        )
        if path:
            self.output_path.setText(path)
            self._refresh_open_button()

    def open_output(self):
        outp = self.output_path.text().strip()
        if not outp or not os.path.exists(outp):
            QtWidgets.QMessageBox.information(self, self.tr("msg_info_title"), self.tr("msg_output_missing"))
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
            raise RuntimeError(self.tr("err_script_missing").format(sp=sp))
        if not inp or not os.path.exists(inp):
            raise RuntimeError(self.tr("err_invalid_input"))
        if not outp:
            raise RuntimeError(self.tr("err_missing_output"))

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
            QtWidgets.QMessageBox.critical(self, self.tr("msg_error_title"), str(e))
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
        self._set_status(self.tr("status_running"))

        self._log("\n" + "=" * 72)
        self._log(self.tr("log_launch"))
        self._log(self._format_cmd_for_log(args))

        self.proc.start(args[0], args[1:])
        if not self.proc.waitForStarted(3000):
            self._log(self.tr("log_failed_start"))
            self._restore_ui_after_run(error=True)

    def stop(self):
        if self.proc.state() == QtCore.QProcess.NotRunning:
            return
        self._log(self.tr("log_stop_requested"))
        self._set_status(self.tr("status_stopping"))
        self.proc.terminate()
        QtCore.QTimer.singleShot(2500, self._kill_if_needed)

    def _kill_if_needed(self):
        if self.proc.state() != QtCore.QProcess.NotRunning:
            self._log(self.tr("log_kill"))
            self.proc.kill()

    def _restore_ui_after_run(self, error: bool):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.reset_btn.setEnabled(True)
        self.progress.setVisible(False)
        self._set_status(self.tr("status_error") if error else self.tr("status_done"))
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
        self._log(self.tr("log_qprocess_error").format(err=err))

    def _finished(self, code, status):
        self._log("\n" + self.tr("log_finished").format(code=code))
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
