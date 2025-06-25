from PIL import Image
import numpy as np


def mask(input, mask_path, threshold=0):
    """
    マスク画像と入力を比べて近似するピクセルを削除
    """
    input_img = input.convert("RGBA")
    mask_img = Image.open(mask_path).convert("RGBA")

    input_array = np.array(input_img)
    mask_array = np.array(mask_img)

    diff = np.abs(input_array[:, :, :3] - mask_array[:, :, :3])
    distance = np.sum(diff, axis=-1)

    # 閾値以内のピクセルを透明にする
    matching_pixels = distance <= threshold
    input_array[matching_pixels, 3] = 0

    result_img = Image.fromarray(input_array, 'RGBA')
    return result_img
