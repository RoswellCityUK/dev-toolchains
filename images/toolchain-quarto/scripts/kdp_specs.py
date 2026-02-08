"""
Amazon KDP Specifications Matrix
"""

# Gutter margins based on page count
# (Max Page Count, Gutter Size in Inches)
MARGIN_RULES = [
    (150, 0.375),
    (300, 0.500),
    (500, 0.625),
    (700, 0.750),
    (828, 0.875)
]

# Valid Trim Sizes and their Page Count Limits
# Format: "WidthxHeight": {"ink_paper_type": (min_pages, max_pages)}
PAPERBACK_SPECS = {
    "5x8": {"bw_white": (24, 828), "bw_cream": (24, 776), "color_std": (72, 600), "color_prem": (24, 828)},
    "5.25x8": {"bw_white": (24, 828), "bw_cream": (24, 776), "color_std": (72, 600), "color_prem": (24, 828)},
    "5.5x8.5": {"bw_white": (24, 828), "bw_cream": (24, 776), "color_std": (72, 600), "color_prem": (24, 828)},
    "6x9": {"bw_white": (24, 828), "bw_cream": (24, 776), "color_std": (72, 600), "color_prem": (24, 828)},
    "7x10": {"bw_white": (24, 828), "bw_cream": (24, 776), "color_std": (72, 600), "color_prem": (24, 828)},
    "8.5x11": {"bw_white": (24, 590), "bw_cream": (24, 550), "color_std": (72, 600), "color_prem": (24, 590)}
}

HARDCOVER_SPECS = {
    "5.5x8.5": {"bw_white": (75, 550), "bw_cream": (75, 550), "color_std": (0, 0), "color_prem": (75, 550)},
    "6x9": {"bw_white": (75, 550), "bw_cream": (75, 550), "color_std": (0, 0), "color_prem": (75, 550)},
    "7x10": {"bw_white": (75, 550), "bw_cream": (75, 550), "color_std": (0, 0), "color_prem": (75, 550)},
    "8.25x11": {"bw_white": (75, 550), "bw_cream": (75, 550), "color_std": (0, 0), "color_prem": (75, 550)}
}

def get_required_gutter(page_count):
    for max_pages, gutter in MARGIN_RULES:
        if page_count <= max_pages:
            return gutter
    return 0.875 # Fallback for huge books

def validate_compatibility(binding, size, ink_paper, page_count):
    """Returns (True, Msg) or (False, ErrorMsg)"""
    specs = HARDCOVER_SPECS if binding == "hardcover" else PAPERBACK_SPECS

    if size not in specs:
        return False, f"Trim size {size} not supported for {binding}."

    if ink_paper not in specs[size]:
        return False, f"Ink/Paper type '{ink_paper}' unknown."

    min_p, max_p = specs[size][ink_paper]

    if min_p == 0 and max_p == 0:
        return False, f"Combination not allowed: {binding} + {ink_paper}."

    if not (min_p <= page_count <= max_p):
        return False, f"Page count ({page_count}) is out of bounds for {size} {ink_paper}. Allowed: {min_p}-{max_p}."

    return True, "Valid."