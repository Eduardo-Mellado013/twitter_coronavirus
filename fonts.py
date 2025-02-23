import matplotlib.font_manager as fm

def get_available_fonts():
    font_families = set([f.name for f in fm.fontManager.ttflist])
    return font_families

available_fonts = get_available_fonts()
for font in sorted(available_fonts):
    print(font)
