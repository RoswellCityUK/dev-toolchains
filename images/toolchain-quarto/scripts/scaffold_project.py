#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# Import our logic library (assumed in same folder or path)
sys.path.append("/opt/tools/scripts")
import kdp_specs

def main():
    print("\n📚 Amazon KDP Professional Scaffolder\n=======================================")

    project_name = input("Project folder name: ").strip()

    # --- INTERACTIVE CONFIGURATION ---
    print("\nSelect Binding Type:")
    print("  1. Paperback")
    print("  2. Hardcover")
    b_choice = input("Choice [1]: ").strip() or "1"
    binding = "hardcover" if b_choice == "2" else "paperback"

    print(f"\nSelect Trim Size for {binding}:")
    specs = kdp_specs.HARDCOVER_SPECS if binding == "hardcover" else kdp_specs.PAPERBACK_SPECS
    sizes = list(specs.keys())
    for i, s in enumerate(sizes):
        print(f"  {i+1}. {s}")
    s_choice = int(input("Choice [2]: ").strip() or "2") - 1
    trim_size = sizes[s_choice]

    print("\nSelect Ink & Paper:")
    print("  1. Black Ink / White Paper (bw_white)")
    print("  2. Black Ink / Cream Paper (bw_cream)")
    print("  3. Standard Color / White Paper (color_std)")
    print("  4. Premium Color / White Paper (color_prem)")
    ip_map = {"1":"bw_white", "2":"bw_cream", "3":"color_std", "4":"color_prem"}
    ip_choice = input("Choice [1]: ").strip() or "1"
    ink_paper = ip_map.get(ip_choice, "bw_white")

    # Estimate pages to set initial margins
    print("\n⚠️  Margins depend on page count.")
    est_pages = int(input("Estimated page count (you can change later): ").strip() or "200")

    # Validation check before we start
    valid, msg = kdp_specs.validate_compatibility(binding, trim_size, ink_paper, est_pages)
    if not valid:
        print(f"\n❌ Configuration Error: {msg}")
        sys.exit(1)

    # --- GEOMETRY CALCULATION ---
    gutter = kdp_specs.get_required_gutter(est_pages)
    width, height = trim_size.split('x')

    # --- GENERATE PROJECT ---
    print(f"\n🚀 Scaffolding {project_name}...")
    subprocess.run(f"quarto create project book {project_name}", shell=True, check=True)

    # --- WRITE CONFIG ---
    os.chdir(project_name)
    os.makedirs("assets/bib", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)

    # Create KDP specific _quarto.yml
    config = f"""project:
  type: book
  output-dir: _output

book:
  title: "{project_name}"
  author: "Author Name"
  date: "today"
  chapters:
    - index.qmd
    - intro.qmd
    - summary.qmd
    - references.qmd

bibliography: assets/bib/references.bib

# --- KDP CONFIGURATION METADATA ---
# Used by the validation scripts. Do not remove.
kdp_settings:
  binding: {binding}
  trim_size: "{trim_size}"
  ink_paper: "{ink_paper}"

format:
  epub:
    cover-image: assets/images/cover.jpg
    toc: true
    number-sections: false

  pdf:
    documentclass: scrbook
    keep-tex: true
    classoption: ["twoside", "openright"]
    include-in-header:
      text: |
        \\usepackage[paperwidth={width}in, paperheight={height}in, top=0.75in, bottom=0.75in, inner={gutter}in, outer=0.5in]{{geometry}}
    lof: false
    lot: false
    toc: true
"""
    with open("_quarto.yml", "w") as f:
        f.write(config)

    print("\n✅ Project Ready!")
    print(f"   Binding: {binding}, Size: {trim_size}, Paper: {ink_paper}")
    print(f"   Initial Gutter set to {gutter}in (based on {est_pages} pages).")