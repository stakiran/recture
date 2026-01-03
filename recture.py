#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

# Pillow
from PIL import ImageGrab

def _try_set_dpi_awareness_for_windows():
    # Windowsの高DPI環境で座標ずれを減らす
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PER_MONITOR_AWARE
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def _ensure_dir(path: str) -> str:
    path = os.path.abspath(path)
    os.makedirs(path, exist_ok=True)
    return path

def _unique_filename(dirpath: str, base: str) -> str:
    # 同秒衝突対策で連番付与
    name = base
    i = 1
    while os.path.exists(os.path.join(dirpath, name)):
        stem, ext = os.path.splitext(base)
        name = f"{stem}_{i}{ext}"
        i += 1
    return os.path.join(dirpath, name)

def main():
    _try_set_dpi_awareness_for_windows()

    parser = argparse.ArgumentParser(description="Rectangular area capture tool (recture).")
    parser.add_argument("--dir", required=True, help="保存先ディレクトリパス")
    args = parser.parse_args()

    save_dir = _ensure_dir(args.dir)

    import tkinter as tk

    root = tk.Tk()
    root.withdraw()  # いったん隠す

    overlay = tk.Toplevel(root)
    overlay.title("recture")
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-topmost", True)

    # 透過＆枠線なし（環境によっては透過が効かないこともあります）
    overlay.overrideredirect(True)
    try:
        overlay.attributes("-alpha", 0.25)
    except Exception:
        pass

    canvas = tk.Canvas(overlay, cursor="cross", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    state = {
        "x0": None, "y0": None,
        "rect_id": None,
        "cancelled": False,
        "done": False,
    }

    def quit_all():
        try:
            overlay.destroy()
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass

    def on_esc(event=None):
        state["cancelled"] = True
        state["done"] = True
        quit_all()

    def on_button_press(event):
        state["x0"], state["y0"] = event.x, event.y
        if state["rect_id"] is not None:
            canvas.delete(state["rect_id"])
            state["rect_id"] = None
        state["rect_id"] = canvas.create_rectangle(
            state["x0"], state["y0"], event.x, event.y,
            outline="red", width=2
        )

    def on_move(event):
        if state["x0"] is None or state["y0"] is None or state["rect_id"] is None:
            return
        canvas.coords(state["rect_id"], state["x0"], state["y0"], event.x, event.y)

    def on_button_release(event):
        if state["x0"] is None or state["y0"] is None:
            on_esc()
            return

        x1, y1 = state["x0"], state["y0"]
        x2, y2 = event.x, event.y

        # 方向補正
        left, right = sorted([x1, x2])
        top, bottom = sorted([y1, y2])

        # ほぼクリックのみなら保存しないで終了
        if (right - left) < 2 or (bottom - top) < 2:
            on_esc()
            return

        # overlayのスクリーン座標に変換
        ox = overlay.winfo_rootx()
        oy = overlay.winfo_rooty()
        bbox = (ox + left, oy + top, ox + right, oy + bottom)

        # 直ちにキャプチャ＆保存
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outpath = _unique_filename(save_dir, f"{ts}.png")

        try:
            # ★ここを追加：オーバーレイを隠してからキャプチャ
            overlay.withdraw()
            overlay.update_idletasks()
            overlay.update()
            img = ImageGrab.grab(bbox=bbox)
            img.save(outpath, "PNG")
        except Exception as e:
            print(f"[recture] capture failed: {e}", file=sys.stderr)
            # 失敗しても終了はする
        finally:
            state["done"] = True
            quit_all()

    overlay.bind("<Escape>", on_esc)
    overlay.bind("<ButtonPress-1>", on_button_press)
    overlay.bind("<B1-Motion>", on_move)
    overlay.bind("<ButtonRelease-1>", on_button_release)

    # フォーカスを確実に取る
    overlay.focus_force()

    root.mainloop()

if __name__ == "__main__":
    main()
