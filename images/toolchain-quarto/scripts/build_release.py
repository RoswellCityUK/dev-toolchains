#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import zipfile
from datetime import datetime

# Allow imports
sys.path.append("/opt/tools/scripts")
try:
    import kdp_specs
    from pypdf import PdfReader
except ImportError:
    print("❌ Critical dependencies (pypdf or kdp_specs) missing.")
    sys.exit(1)

def run_command(cmd):
    print(f"🚀 Executing: {cmd}")
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError:
        print("❌ Build failed.")
        sys.exit(1)

def main():
    print("📦 Quarto KDP Release Builder\n=============================")

    if not os.path.exists("_quarto.yml"):
        print("❌ Error: Run from project root.")
        sys.exit(1)

    # 1. Clean old builds
    if os.path.exists("_output"):
        shutil.rmtree("_output")

    # 2. Run Linter First
    run_command("check-project")

    # 3. Render
    print("\n🔨 Rendering PDF and ePub...")
    run_command("quarto render")

    # 4. Post-Render Validation (Physical Page Count Check)
    print("\n🔎 Validating PDF Artifacts...")
    pdf_files = [f for f in os.listdir("_output") if f.endswith(".pdf")]

    if pdf_files:
        pdf_path = os.path.join("_output", pdf_files[0])
        reader = PdfReader(pdf_path)
        pages = len(reader.pages)
        print(f"   PDF Page Count: {pages}")

        # Check margins against page count
        required = kdp_specs.get_required_gutter(pages)
        print(f"   Required Gutter: {required} inches")

        # Note: We don't fail the build here, but we warn heavily
        # because the user might have set it correctly in latex already.
        print(f"   ⚠️  Ensure your _quarto.yml has 'inner={required}in' for {pages} pages.")

    # 5. Zip
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"release_{timestamp}.zip"

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("_output"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "_output"))

    print(f"\n✅ Build Complete: {zip_name}")

if __name__ == "__main__":
    main()