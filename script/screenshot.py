import pyautogui
import time
import sys
import pygetwindow as gw
import os
import mask

regions = {
    "wagon": [
        (1455, 837, 368, 326),
        (1421, 840, 382, 382),
    ],
    "engine": [
        (1719, 850, 410, 289),
        (1682, 848, 434, 359),
    ]
}

filename = sys.argv[1] if len(sys.argv) > 1 else "debug"
level = sys.argv[2] if len(sys.argv) > 2 else "1"
threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 20
mask_dir = sys.argv[4] if len(sys.argv) > 4 else "mask_1"
region_mode = sys.argv[5] if len(sys.argv) > 5 else "wagon"

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
screenshot1 = pyautogui.screenshot(region=regions[region_mode][0])
screenshot1.save(paths["sideview_original"])
if region_mode == "wagon":
    mask.mask(screenshot1, f"src/{mask_dir}/sideview.png",
              threshold).save(paths["sideview"])

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')

time.sleep(0.05)

# スクショ2枚目（topview）
screenshot2 = pyautogui.screenshot(region=regions[region_mode][1])
screenshot2.save(paths["topview_original"])
if region_mode == "wagon":
    mask.mask(screenshot2, f"src/{mask_dir}/topview.png",
              threshold).save(paths["topview"])

# Cキーを3回押す
for _ in range(3):
    pyautogui.press('c')
