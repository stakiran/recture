# recture
矩形選択した範囲をキャプチャするだけのシンプルなツール implemented by python.

名前は rect + capture = recture より。

## 要件
- Python 3.10+
- requirements.txt に書いてるライブラリ

## 使い方
デスクトップに出したい場合

```
python recture.py --dir C:\Users\ユーザー名\Desktop
```

## 素早く起動したい場合
AutoHotkey を使う:

```ahk
; recture
!^z::Run,pythonw "D:\work\github\recture\recture.py" --dir "C:\Users\ユーザー名\Desktop"
```

バッチファイルでラップする:

- launch_recture.bat.sample 参照

## その他雑多
- たぶん Windows でのみ動作する
- DOS 窓問題:
    - recture 自体の DOS 窓が邪魔なので、pythonw で実行した方がいい
    - バッチファイルでラップした場合、その分の DOS 窓も出ちゃう
        - なので **事実上 AutoHotkey を使うしかないのではなかろうか**
- ChatGPT 5.2 Thinking でつくった
    - <https://chatgpt.com/share/695986c4-8be8-8007-839b-33ff8582e4d1>
