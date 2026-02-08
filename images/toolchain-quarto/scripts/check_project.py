#!/usr/bin/env python3
import os
import yaml
import sys

# Allow importing our local KDP logic
sys.path.append("/opt/tools/scripts")
try:
    import kdp_specs
except ImportError:
    # Fallback if running outside container without specs
    kdp_specs = None

def check_fail(msg):
    print(f"❌ [FAIL] {msg}")
    return False

def check_pass(msg):
    print(f"✅ [PASS] {msg}")
    return True

def main():
    print("🔍 Quarto Project Linter (KDP Enhanced)\n=======================================")

    if not os.path.exists("_quarto.yml"):
        print("❌ Error: No _quarto.yml found. Are you in the project root?")
        sys.exit(1)

    all_passed = True

    # 1. Load Configuration
    try:
        with open("_quarto.yml", "r") as f:
            config = yaml.safe_load(f)
        check_pass("Configuration file is valid YAML.")
    except Exception as e:
        check_fail(f"Invalid _quarto.yml: {e}")
        sys.exit(1)

    # 2. Check Standard Structure
    required_dirs = ["chapters", "assets/images", "assets/bib"]
    for d in required_dirs:
        if os.path.isdir(d):
            check_pass(f"Directory exists: {d}/")
        else:
            check_fail(f"Missing directory: {d}/ (Professional standard required)")
            all_passed = False

    # 3. Check Bibliography
    bib_file = config.get("bibliography")
    if bib_file and os.path.exists(bib_file):
        check_pass(f"Bibliography found: {bib_file}")
    elif bib_file:
        check_fail(f"Bibliography missing: {bib_file}")
        all_passed = False
    else:
        print("⚠️  [WARN] No bibliography defined.")

    # 4. Check Chapters
    book_conf = config.get("book", {})
    chapters = book_conf.get("chapters", [])
    if not chapters:
        print("⚠️  [WARN] No chapters listed in configuration.")

    for chapter in chapters:
        if isinstance(chapter, str):
            if not os.path.exists(chapter):
                check_fail(f"Missing chapter file: {chapter}")
                all_passed = False

    # 5. Check Amazon KDP Configuration
    formats = config.get("format", {})
    kdp_settings = config.get("kdp_settings")

    if kdp_settings and kdp_specs:
        print("\n📚 Validating KDP Print Settings...")
        binding = kdp_settings.get("binding")
        trim = kdp_settings.get("trim_size")
        paper = kdp_settings.get("ink_paper")

        # Validate that the Configured Trim Size matches the Geometry in PDF format
        if "pdf" in formats:
            pdf_conf = formats["pdf"]
            header = pdf_conf.get("include-in-header", {}).get("text", "")

            # Extract width/height from trim string (e.g. "6x9")
            if trim and "x" in trim:
                w, h = trim.split("x")
                if f"paperwidth={w}in" in header and f"paperheight={h}in" in header:
                    check_pass(f"PDF Geometry matches KDP Trim: {trim}")
                else:
                    check_fail(f"Mismatch: KDP setting is {trim}, but PDF geometry (latex) looks different.")
                    all_passed = False

    # 6. Check E-Book Cover
    if "epub" in formats:
        cover = formats["epub"].get("cover-image")
        if not cover:
            check_fail("ePub output defined but no 'cover-image' found.")
            all_passed = False
        elif not os.path.exists(cover):
            check_fail(f"ePub cover image missing at: {cover}")
            all_passed = False
        else:
            check_pass(f"ePub cover verified: {cover}")

    # 7. Check PDF Cover (Should NOT exist)
    if "pdf" in formats:
        if "cover-image" in formats["pdf"]:
             print("⚠️  [WARN] 'cover-image' detected in PDF config. KDP Print requires a separate cover file.")

    # 8. Content Checks
    print("\n📝 Scanning content for TODOs...")
    for root, dirs, files in os.walk("."):
        if "_output" in root: continue # Skip build artifacts
        for file in files:
            if file.endswith(".qmd") or file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "TODO" in content or "FIXME" in content:
                            print(f"   ⚠️  TODO found in {path}")
                except:
                    pass

    print("\n=======================")
    if all_passed:
        print("🎉 Project is clean and standard-compliant!")
        sys.exit(0)
    else:
        print("🛑 Issues found. Please fix before publishing.")
        sys.exit(1)

if __name__ == "__main__":
    main()