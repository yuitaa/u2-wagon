import os
import sys
import shutil
from PIL import Image
import glob
import zipfile

filename = sys.argv[1] if len(sys.argv) > 1 else "debug"

src_dir = 'images'
dist_dir = 'dist/tmp'
os.makedirs(dist_dir, exist_ok=True)


def get_bbox(image):
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    return bbox


def get_encompassing_bbox(bboxes):
    min_left = min(b[0] for b in bboxes)
    min_upper = min(b[1] for b in bboxes)
    max_right = max(b[2] for b in bboxes)
    max_lower = max(b[3] for b in bboxes)

    return (min_left, min_upper, max_right, max_lower)


# imagesディレクトリ内のすべてのファイルとフォルダをコピー
for item in os.listdir(src_dir):
    src_path = os.path.join(src_dir, item)
    dst_path = os.path.join(dist_dir, item)

    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    else:
        shutil.copy2(src_path, dst_path)

bboxes = {
    "engine_top": [],
    "engine_side": [],
    "wagon_top": [],
    "wagon_side": [],
}

# それぞれ画像内容の範囲を取得
for filepath in glob.glob(os.path.join(f"{dist_dir}/transparent", "**", "*.png"), recursive=True):
    try:
        path = filepath.split(os.sep)
        with Image.open(filepath) as image:
            bbox = get_bbox(image)

            if "engine" in path:
                if "topview" in path:
                    bboxes["engine_top"].append(bbox)
                elif "sideview" in path:
                    bboxes["engine_side"].append(bbox)

            elif "topview" in path:
                bboxes["wagon_top"].append(bbox)
            elif "sideview" in path:
                bboxes["wagon_side"].append(bbox)

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# 全画像が収まるような切り抜き範囲を取得
encompassing_bboxes = {}
for key, bbox_list in bboxes.items():
    if bbox_list:
        encompassing_bboxes[key] = get_encompassing_bbox(bbox_list)
    else:
        encompassing_bboxes[key] = None

# 画像処理
for filepath in glob.glob(os.path.join(f"{dist_dir}/transparent", "**", "*.png"), recursive=True):
    try:
        path = filepath.split(os.sep)
        with Image.open(filepath) as image:
            bbox = get_bbox(image)

            if "engine" in path:
                if "topview" in path:
                    image.crop(encompassing_bboxes["engine_top"]).save(
                        filepath)
                elif "sideview" in path:
                    image.crop(encompassing_bboxes["engine_side"]).save(
                        filepath)

            elif "topview" in path:
                image.crop(encompassing_bboxes["wagon_top"]).save(filepath)
            elif "sideview" in path:
                image.crop(encompassing_bboxes["wagon_side"]).save(filepath)

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

source_dir = 'dist/tmp/transparent'
zip_path = f'dist/{filename}.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(source_dir):
        for file in filenames:
            file_path = os.path.join(foldername, file)
            arcname = os.path.relpath(file_path, start=source_dir)
            zipf.write(file_path, arcname)