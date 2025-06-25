import pyautogui
import time
import sys
import pygetwindow as gw
import os

filename = sys.argv[1] if len(sys.argv) > 1 else "debug"
level = sys.argv[2] if len(sys.argv) > 2 else "1"

# Unrailed2のウインドウをアクティブに
window = None
for w in gw.getWindowsWithTitle('Unrailed2'):
    if w.title.startswith('Unrailed2'):
        window = w
        break

if window:
    window.activate()
    time.sleep(0.5)
else:
    raise Exception("Unrailed2 が見つかりません")

# 保存先ディレクトリを作成（なければ）
sideview_path = f"images/sideview/{level}/sideview_{filename}_{level}.png"
topview_path = f"images/topview/{level}/topview_{filename}_{level}.png"
os.makedirs(os.path.dirname(sideview_path), exist_ok=True)
os.makedirs(os.path.dirname(topview_path), exist_ok=True)

# スクショ1枚目（sideview）
screenshot1 = pyautogui.screenshot(region=(1455, 837, 368, 326))
screenshot1.save(sideview_path)

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')

time.sleep(0.05)

# スクショ2枚目（topview）
screenshot2 = pyautogui.screenshot(region=(1421, 840, 382, 382))
screenshot2.save(topview_path)

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')
