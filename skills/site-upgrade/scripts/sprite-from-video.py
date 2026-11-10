#!/usr/bin/env python3
"""Turn a person walking in a video into a sticker sprite sheet.

usage: sprite-from-video.py <video> <start-seconds> <seconds> <out.webp> --model <u2net_human_seg.onnx>
         [--every 3] [--idle-at SECONDS] [--skip 4,5] [--cell 216x356] [--edge 7] [--fps 30]

Cuts the person out of each sampled frame with a local segmentation model, finds the two frames
where the stride repeats, and writes the loop plus one standing cell as a single strip, with a
white die-cut edge and a soft contact shadow. It also writes <out>-preview.jpg: read it, then
re-run with --skip for any frame that picked up a road sign or a passer-by.

Needs Python with numpy, Pillow and onnxruntime, and ffmpeg (on the PATH or from imageio_ffmpeg).
The model is u2net_human_seg.onnx from the rembg releases on GitHub (176 MB): ask the owner before
downloading it, and keep it in its own folder outside the project.
"""
import argparse
import glob
import os
import shutil
import subprocess
import tempfile
from collections import deque

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw, ImageFilter

MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])


def ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def predict(session, name, image):
    x = np.array(image.convert("RGB").resize((320, 320), Image.LANCZOS), dtype=np.float32)
    x = x / max(x.max(), 1e-6)
    x = ((x - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
    p = session.run(None, {name: x})[0][0, 0]
    return (p - p.min()) / max(p.max() - p.min(), 1e-6)


def main_blob(mask):
    """The connected blob that is both large and near the middle of the picture."""
    h, w = mask.shape
    seen = np.zeros_like(mask, bool)
    best, score = None, -1
    for sy, sx in zip(*np.nonzero(mask)):
        if seen[sy, sx]:
            continue
        queue = deque([(sy, sx)])
        seen[sy, sx] = True
        points = []
        while queue:
            y, x = queue.popleft()
            points.append((y, x))
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((ny, nx))
        centre = np.mean([p[1] for p in points]) / w
        value = len(points) * (1.2 - abs(centre - 0.5))
        if value > score:
            score, best = value, points
    keep = np.zeros_like(mask, bool)
    if best:
        ys, xs = zip(*best)
        keep[list(ys), list(xs)] = True
    return keep


def cut_out(session, name, path):
    """Two passes: find the person in the whole frame, then segment a tight crop for a clean edge."""
    image = Image.open(path).convert("RGB")
    width, height = image.size
    ys, xs = np.nonzero(main_blob(predict(session, name, image) > 0.5))
    x0, x1 = xs.min() / 320 * width, xs.max() / 320 * width
    y0, y1 = ys.min() / 320 * height, ys.max() / 320 * height
    side = max(x1 - x0, y1 - y0) * 1.14
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2))
    crop = image.crop(box)
    p = predict(session, name, crop)
    keep = main_blob(p > 0.5)
    alpha = Image.fromarray((np.clip((p * keep - 0.25) / 0.5, 0, 1) * 255).astype(np.uint8)).resize(crop.size, Image.BICUBIC)
    rgba = crop.convert("RGBA")
    rgba.putalpha(alpha)
    bounds = alpha.point(lambda v: 255 if v > 60 else 0).getbbox()
    return rgba.crop(bounds), height - (box[1] + bounds[3])


def centred_mask(image, height):
    a = np.array(image.split()[3]) > 80
    canvas = np.zeros((height, 300), bool)
    offset = 150 - int(np.mean(np.nonzero(a)[1]))
    x0 = max(0, offset)
    w = min(300 - x0, a.shape[1] - max(0, -offset))
    canvas[: a.shape[0], x0 : x0 + w] = a[:, max(0, -offset) : max(0, -offset) + w]
    return canvas


def cell(image, cell_w, cell_h, body, edge):
    a = np.array(image.split()[3])
    cx = int(np.mean(np.nonzero(a > 80)[1]))
    layer = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    layer.alpha_composite(image, (max(0, min(cell_w - image.width, cell_w // 2 - cx)), cell_h - body - 14))
    grown = (
        layer.split()[3]
        .filter(ImageFilter.MaxFilter(edge * 2 + 1))
        .filter(ImageFilter.GaussianBlur(1.6))
        .point(lambda v: 255 if v > 110 else 0)
        .filter(ImageFilter.GaussianBlur(0.7))
    )
    shadow = Image.new("L", (cell_w, cell_h), 0)
    ImageDraw.Draw(shadow).ellipse((cell_w // 2 - 62, cell_h - 24, cell_w // 2 + 62, cell_h - 5), fill=90)
    dark = Image.new("RGBA", (cell_w, cell_h), (12, 40, 46, 255))
    dark.putalpha(shadow.filter(ImageFilter.GaussianBlur(6)))
    white = Image.new("RGBA", (cell_w, cell_h), (255, 255, 255, 255))
    white.putalpha(grown)
    out = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    out.alpha_composite(dark)
    out.alpha_composite(white)
    out.alpha_composite(layer)
    return out


def main():
    ap = argparse.ArgumentParser(description="Turn a person walking in a video into a sticker sprite sheet.")
    ap.add_argument("video")
    ap.add_argument("start", type=float)
    ap.add_argument("seconds", type=float)
    ap.add_argument("out")
    ap.add_argument("--model", required=True)
    ap.add_argument("--every", type=int, default=3, help="keep every Nth video frame")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--idle-at", type=float, default=None, help="time of the standing frame")
    ap.add_argument("--skip", default="", help="sample numbers to drop, as printed, comma separated")
    ap.add_argument("--cell", default="216x356")
    ap.add_argument("--edge", type=int, default=7)
    args = ap.parse_args()

    cell_w, cell_h = (int(v) for v in args.cell.split("x"))
    body = cell_h - 40
    skip = {int(v) for v in args.skip.split(",") if v}

    options = ort.SessionOptions()
    session = ort.InferenceSession(args.model, options, providers=["CPUExecutionProvider"])
    name = session.get_inputs()[0].name

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(args.start), "-t", str(args.seconds),
             "-i", args.video, "-vf", f"fps={args.fps}", "-q:v", "2", os.path.join(tmp, "f%04d.jpg")],
            check=True,
        )
        frames = sorted(glob.glob(os.path.join(tmp, "f*.jpg")))[:: args.every]
        cuts = {}
        for number, path in enumerate(frames):
            if number in skip:
                continue
            image, margin = cut_out(session, name, path)
            note = "  feet touch the frame edge" if margin < 2 else ""
            print(f"sample {number}: cut {image.size}, {margin}px above the bottom{note}", flush=True)
            cuts[number] = image.resize((max(1, round(image.width * body / image.height)), body), Image.LANCZOS)

        idle = None
        if args.idle_at is not None:
            still = os.path.join(tmp, "idle.jpg")
            subprocess.run(
                [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(args.idle_at), "-i", args.video, "-frames:v", "1", "-q:v", "2", still],
                check=True,
            )
            image, _ = cut_out(session, name, still)
            idle = image.resize((max(1, round(image.width * body / image.height)), body), Image.LANCZOS)

    numbers = sorted(cuts)
    masks = {n: centred_mask(cuts[n], body) for n in numbers}
    iou = lambda a, b: (a & b).sum() / max((a | b).sum(), 1)
    shortest = max(4, round(0.55 * args.fps / args.every))
    best = None
    for i, a in enumerate(numbers):
        for j in range(i + shortest, len(numbers)):
            score = iou(masks[a], masks[numbers[j]])
            if best is None or score > best[0]:
                best = (score, i, j)
    if best is None:
        raise SystemExit("not enough frames to find a loop: use a longer stretch")
    score, i, j = best
    loop = numbers[i:j]
    print(f"loop: samples {loop} (match {score:.2f}), {len(loop) * args.every / args.fps:.2f}s per stride")

    cells = [cuts[n] for n in loop] + ([idle] if idle is not None else [cuts[loop[0]]])
    sheet = Image.new("RGBA", (cell_w * len(cells), cell_h), (0, 0, 0, 0))
    for k, image in enumerate(cells):
        sheet.alpha_composite(cell(image, cell_w, cell_h, body, args.edge), (k * cell_w, 0))
    sheet.save(args.out, "WEBP", quality=84, method=6, alpha_quality=90)

    preview = Image.new("RGBA", sheet.size, (240, 225, 215, 255))
    preview.alpha_composite(sheet)
    preview.convert("RGB").save(os.path.splitext(args.out)[0] + "-preview.jpg", quality=84)
    print(f"{args.out}: {len(loop)} walking cells + 1 standing, {cell_w}x{cell_h} each, {os.path.getsize(args.out) // 1024} KB")
    print(f"CSS: animation {len(loop) * args.every / args.fps:.2f}s steps({len(loop)}) infinite; the standing cell is number {len(loop)}")


if __name__ == "__main__":
    main()
