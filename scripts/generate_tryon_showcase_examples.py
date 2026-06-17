#!/usr/bin/env python3
"""Generate try-on showcase pairs: person plate + garments + fit-on (2 examples)."""
from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

API_KEY = os.environ["PRUNA_API_KEY"]
BASE = "https://api.pruna.ai"
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "output" / "try-on-examples"

EXAMPLES = [
    {
        "id": "example-1",
        "ritual_seed": 847291,
        "label": "Pottery studio · wax-print skirt + rust jacket",
        "person": {
            "prompt": (
                "Photoreal full-body fashion photograph, woman mid-50s West African, silver locs, "
                "standing relaxed in artisan pottery studio with ceramic shelves and clay floor, "
                "warm tungsten practical light, neutral beige linen tunic and wide trousers base outfit, "
                "bare feet visible, natural skin pores, not CGI, 3:4 vertical, single subject one frame"
            ),
            "aspect_ratio": "3:4",
        },
        "garments": [
            {
                "name": "indigo_wax_print_skirt",
                "prompt": (
                    "Flat-lay packshot of indigo and gold West African wax-print wrap skirt on pure white "
                    "background, crisp fabric folds, ecommerce product photo, no model, single garment one frame"
                ),
                "aspect_ratio": "1:1",
            },
            {
                "name": "rust_cropped_jacket",
                "prompt": (
                    "Flat-lay packshot of hand-woven rust-orange cropped jacket with textured weave on white "
                    "background, no model, single garment one frame, studio even light"
                ),
                "aspect_ratio": "1:1",
            },
        ],
    },
    {
        "id": "example-2",
        "ritual_seed": 163548,
        "label": "Neon laundromat · holo puffer + corduroy pants",
        "person": {
            "prompt": (
                "Photoreal full-body street portrait, androgynous person early 20s East European, short bleached "
                "hair, standing in neon-lit laundromat with pink and teal fluorescent tubes, washing machines "
                "behind, grey tank top and black shorts base outfit, white sneakers visible, slight low angle, "
                "natural skin texture, not CGI, 9:16 vertical, single subject one frame"
            ),
            "aspect_ratio": "9:16",
        },
        "garments": [
            {
                "name": "holographic_puffer_vest",
                "prompt": (
                    "Flat-lay packshot of iridescent holographic puffer vest on white background, "
                    "shiny quilted panels, no model, single garment one frame"
                ),
                "aspect_ratio": "1:1",
            },
            {
                "name": "olive_corduroy_pants",
                "prompt": (
                    "Flat-lay packshot of olive green wide-leg corduroy trousers on white background, "
                    "visible wale texture, no model, single garment one frame"
                ),
                "aspect_ratio": "1:1",
            },
        ],
    },
]


def api_json(method, path, data=None, headers=None):
    url = BASE + path
    h = {"apikey": API_KEY}
    if headers:
        h.update(headers)
    body = json.dumps(data).encode() if data is not None else None
    if data is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


def predict_sync(model, inp):
    return api_json("POST", "/v1/predictions", data={"input": inp}, headers={"Model": model, "Try-Sync": "true"})


def download(url, dest):
    req = urllib.request.Request(url, headers={"apikey": API_KEY})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def upload_file(path):
    boundary = f"----Boundary{int(time.time())}"
    data = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="content"; filename="{path.name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{BASE}/v1/files",
        data=data,
        headers={"apikey": API_KEY, "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.loads(resp.read().decode())
    return out["urls"]["get"]


def try_on(person_url, garment_urls, seed):
    return predict_sync(
        "p-image-try-on",
        {
            "person_image": person_url,
            "garment_images": garment_urls,
            "seed": seed,
            "output_format": "jpg",
            "output_quality": 95,
            "preserve_input_size": True,
        },
    )


def run_example(ex):
    ex_dir = OUT / ex["id"]
    ex_dir.mkdir(parents=True, exist_ok=True)
    seed = ex["ritual_seed"]
    manifest = {"id": ex["id"], "label": ex["label"], "ritual_seed": seed, "assets": {}}
    print(f"\n=== {ex['id']}: ritual seed {seed} ===")

    p = ex["person"]
    print("  p-image person...")
    pr = predict_sync("p-image", {"prompt": p["prompt"], "aspect_ratio": p["aspect_ratio"], "seed": seed})
    if pr.get("status") != "succeeded":
        raise RuntimeError(f"person failed: {pr}")
    person_path = ex_dir / "01_person_plate.jpg"
    download(pr["generation_url"], person_path)
    person_file_url = upload_file(person_path)
    manifest["assets"]["person"] = {"local": str(person_path.relative_to(REPO)), "file_url": person_file_url, "prompt": p["prompt"]}
    print(f"    saved {person_path.name}")

    garment_urls = []
    for i, g in enumerate(ex["garments"], start=1):
        gseed = seed + i * 17
        print(f"  p-image garment {g['name']} (seed {gseed})...")
        gr = predict_sync("p-image", {"prompt": g["prompt"], "aspect_ratio": g["aspect_ratio"], "seed": gseed})
        if gr.get("status") != "succeeded":
            raise RuntimeError(f"garment {g['name']} failed: {gr}")
        gpath = ex_dir / f"02_garment_{g['name']}.jpg"
        download(gr["generation_url"], gpath)
        gurl = upload_file(gpath)
        garment_urls.append(gurl)
        manifest["assets"][f"garment_{g['name']}"] = {"local": str(gpath.relative_to(REPO)), "file_url": gurl, "prompt": g["prompt"]}
        print(f"    saved {gpath.name}")

    print("  p-image-try-on...")
    tr = try_on(person_file_url, garment_urls, seed)
    if tr.get("status") != "succeeded":
        raise RuntimeError(f"try-on failed: {tr}")
    fit_path = ex_dir / "03_tryon_result.jpg"
    download(tr["generation_url"], fit_path)
    manifest["assets"]["tryon"] = {"local": str(fit_path.relative_to(REPO)), "generation_url": tr["generation_url"]}
    print(f"    saved {fit_path.name}")

    (ex_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = [run_example(ex) for ex in EXAMPLES]
    (OUT / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nDone. Output: {OUT.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
