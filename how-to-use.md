# 撮影方法 (自分用メモ)
ディスプレイの解像度を3840x2160に設定。ゲームの画面も拡大する。

```
# godot_settings.godot
window/size/viewport_width=3808
window/size/viewport_height=1606
```

```
# 元の設定
window/size/viewport_width=1904
window/size/viewport_height=803
```

ゲームの設定
| 項目               | 設定値 |
| ------------------ | ------ |
| ドライバ           | Vulkan |
| 低品質レンダリング | 有効   |
| 画質               | 最低   |
| コントラスト       | 1.10   |
| 明るさ             | 1.00   |
| 列車の輪郭線無効   | 有効   |

サンドボックスでゲームを開き、リプレイを作っておく。撮影したいワゴンをエンジンに接続する。

1. リプレイを再生
2. Cキーを2度押し (視点変更)
3. Q/Eで中心をエンジンに固定
4. 撮影したいワゴンがエンジンに付いているタイミングでスペースキーを使って停止

```
py -m pipenv run py ./script/screenshot.py [ファイル名] [レベル] [透過の閾値] [マスクのディレクトリ] [モード wagon/engine]
```

## デバッグ用撮影の削除
```
py -m pipenv run py ./script/delete_debug.py
```

## リリース用ファイルの作成
```
py -m pipenv run py ./script/release.py [u2-wagon-{version}]
```