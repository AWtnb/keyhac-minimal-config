import pyauto
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
