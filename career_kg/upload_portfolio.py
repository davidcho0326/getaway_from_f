"""
PDF 페이지 추출 → Cloudinary 업로드 → portfolio_pages.json 생성

Usage:
    pip install cloudinary pdf2image
    brew install poppler  (macOS)
    python upload_portfolio.py <path_to_pdf>
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pdf2image import convert_from_path

load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_portfolio(pdf_path: str, output_json: str = None):
    if output_json is None:
        output_json = str(Path(__file__).parent / "portfolio_pages.json")

    print(f"Converting {pdf_path} to images...")
    pages = convert_from_path(pdf_path, dpi=200)
    print(f"Found {len(pages)} pages")

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, page_img in enumerate(pages, start=1):
            tmp_path = os.path.join(tmpdir, f"page_{i:02d}.png")
            page_img.save(tmp_path, "PNG")

            resp = cloudinary.uploader.upload(
                tmp_path,
                public_id=f"career_kg/portfolio/page_{i:02d}",
                overwrite=True,
                resource_type="image",
                transformation=[{"fetch_format": "auto", "quality": "auto"}],
            )
            results.append({
                "page": i,
                "url": resp["secure_url"],
            })
            print(f"  Uploaded page {i}/{len(pages)}")

    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} entries to {output_json}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_portfolio.py <path_to_pdf>")
        sys.exit(1)
    upload_portfolio(sys.argv[1])
