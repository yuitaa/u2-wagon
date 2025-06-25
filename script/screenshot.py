import pyautogui
import time
import sys
import pygetwindow as gw
import os
import mask

filename = sys.argv[1] if len(sys.argv) > 1 else "debug"
level = sys.argv[2] if len(sys.argv) > 2 else "1"
threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 20

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
paths = {
    "sideview_original": f"images/original/sideview/{level}/{filename}_s{level}.png",
    "sideview": f"images/transparent/sideview/{level}/{filename}_s{level}.png",
    "topview_original": f"images/original/topview/{level}/{filename}_t{level}.png",
    "topview": f"images/transparent/topview/{level}/{filename}_t{level}.png",
}

for path in paths.values():
    os.makedirs(os.path.dirname(path), exist_ok=True)

# スクショ1枚目（sideview）
screenshot1 = pyautogui.screenshot(region=(1455, 837, 368, 326))
screenshot1.save(paths["sideview_original"])
mask.mask(screenshot1, "src/mask_sideview.png", threshold).save(paths["sideview"])

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')

time.sleep(0.05)

# スクショ2枚目（topview）
screenshot2 = pyautogui.screenshot(region=(1421, 840, 382, 382))
screenshot2.save(paths["topview_original"])
mask.mask(screenshot2, "src/mask_topview.png", threshold).save(paths["topview"])

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')
