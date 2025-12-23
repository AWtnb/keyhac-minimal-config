import re
import time
import urllib.parse

import ckit
from keyhac import *


def configure(keymap):
    # フォント設定
    keymap.setFont("MS Gothic", 16)

    # テーマ
    keymap.setTheme("black")

    # エディタ
    keymap.editor = "notepad.exe"

    # 無変換をUser0に
    keymap.replaceKey("(29)", 235)
    keymap.defineModifier(235, "User0")

    # 無変換をUser1に
    keymap.replaceKey("(28)", 236)
    keymap.defineModifier(236, "User1")

    # クリップボード履歴の有効化（最大200MB）
    keymap.clipboard_history.enableHook(True)
    keymap.clipboard_history.maxnum = 200
    keymap.clipboard_history.quota = 10 * 1024 * 1024

    # Ctrl-Enter での貼り付け時の引用符
    keymap.quote_mark = "> "

    # どのアプリでも有効なキーマップを定義
    keymap_global = keymap.defineWindowKeymap()

    # キーボードマクロ
    keymap_global["U0-0"] = keymap.command_RecordToggle
    keymap_global["S-U0-0"] = keymap.command_RecordClear
    keymap_global["U1-0"] = keymap.command_RecordPlay

    # 無変換の単押しでescape
    keymap_global["O-(235)"] = "Esc"

    def bind_main_keys() -> None:
        mod_keys = ("", "S-", "C-", "A-", "C-S-", "C-A-", "S-A-", "C-A-S-")
        for mod_key in mod_keys:
            for key, value in {
                # 無変換+H/J/K/Lでカーソル移動
                "H": "Left",
                "J": "Down",
                "K": "Up",
                "L": "Right",
                # 無変換+B/DでBack / Delete
                "B": "Back",
                "D": "Delete",
                # 無変換+A/EでHome / End
                "A": "Home",
                "E": "End",
                # 無変換+SpaceでEnter
                "Space": "Enter",
            }.items():
                keymap_global[mod_key + "U0-" + key] = mod_key + value

    bind_main_keys()

    # 左Ctrl-左Shift-Xでクリップボード履歴
    keymap_global["LC-LS-X"] = keymap.command_ClipboardList

    # ミリ秒指定で待つ関数
    def delay(msec=50):
        if 0 < msec:
            time.sleep(msec / 1000)

    # URL指定でウェブ検索する関数を生成する関数
    def invoke_searcher(url):
        # 約物をスペースに変換するサブ関数
        def _replace(s):
            reg_noise = re.compile(
                r"[『』（）「」【】《》〈〉・，、。．：；―～─\(\)\"\'\[\]\{\}#&,\.:;/-]|\s+"
            )
            return reg_noise.sub(" ", s)

        # 実際に検索を実行するサブ関数（__watch_clipboad と __search のサブサブ関数をスレッド機能で実行する）
        def _searcher(u=url):
            cb = ckit.getClipboardText() or ""
            keymap.InputKeyCommand("C-C")()
            delay()

            def __watch_clipboard(job_item):
                job_item.origin = cb
                job_item.copied = ""
                trial = 600
                for _ in range(trial):
                    s = ckit.getClipboardText() or ""
                    if not s.strip():
                        continue
                    if s != job_item.origin:
                        job_item.copied = s
                        break

            def __search(job_item):
                s = job_item.copied
                if len(s) < 1:
                    s = job_item.origin
                s = _replace(s)
                s = urllib.parse.quote(s)
                keymap.ShellExecuteCommand(None, u.format(s), "", "")()

            job = ckit.JobItem(__watch_clipboard, __search)
            ckit.JobQueue.defaultQueue().enqueue(job)

        return _searcher

    keymap_global["U0-S"] = keymap.defineMultiStrokeKeymap()
    keymap_global["U0-S"]["G"] = invoke_searcher(
        "http://www.google.com/search?nfpr=1&q={}"
    )
    keymap_global["U0-S"]["I"] = invoke_searcher(
        "https://www.google.com/search?udm=2&nfpr=1&q={}"
    )
    keymap_global["U0-S"]["A"] = invoke_searcher(
        "https://www.amazon.co.jp/s?i=stripbooks&k={}"
    )
