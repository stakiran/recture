# recture
矩形選択した範囲をキャプチャするだけのシンプルなツール implemented by python.

名前は rect + capture = recture より。

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

## 注意点など
- たぶん Windows でのみ動作する
- recture 自体の DOS 窓が邪魔なので、pythonw で実行した方がいい
- バッチファイルでラップした場合、その分の DOS 窓も出ちゃう
    - なので事実上 AutoHotkey を使うしかないのではなかろうか？
