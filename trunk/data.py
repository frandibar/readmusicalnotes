from os.path import join

# paths
DATA_PATH   = "data"
FONTS_PATH  = join(DATA_PATH, "fonts")
IMAGES_PATH = join(DATA_PATH, "images")
SOUNDS_PATH = join(DATA_PATH, "sounds")

# images
WRONG_IMG         = join(IMAGES_PATH, "incorrect.gif")
CORRECT_IMG       = join(IMAGES_PATH, "correct.gif")
MAIN_MENU_IMG     = join(IMAGES_PATH, "strip.gif")
ICON_IMG          = join(IMAGES_PATH, "notes.gif")
MAIN_OVERLAY_IMG  = join(IMAGES_PATH, "main_overlay.png")
QUIZ_OVERLAY_IMG  = join(IMAGES_PATH, "notesquiz_overlay.png")
SETUP_OVERLAY_IMG = join(IMAGES_PATH, "setup_overlay.png")

TREBLE_CLEF_IMG     = join(IMAGES_PATH, "treble_clef.png")
BASS_CLEF_IMG       = join(IMAGES_PATH, "bass_clef.png")

WHOLE_IMG             = join(IMAGES_PATH, "whole.png")
HALF_STEM_UP_IMG      = join(IMAGES_PATH, "half_stem_up.png")
HALF_STEM_DOWN_IMG    = join(IMAGES_PATH, "half_stem_down.png")
QUARTER_STEM_UP_IMG   = join(IMAGES_PATH, "quarter_stem_up.png")
QUARTER_STEM_DOWN_IMG = join(IMAGES_PATH, "quarter_stem_down.png")
EIGHTH_STEM_UP_IMG    = join(IMAGES_PATH, "eighth_stem_up.png")
EIGHTH_STEM_DOWN_IMG  = join(IMAGES_PATH, "eighth_stem_down.png")
SIXTEEN_STEM_UP_IMG   = join(IMAGES_PATH, "sixteen_stem_up.png")
SIXTEEN_STEM_DOWN_IMG = join(IMAGES_PATH, "sixteen_stem_down.png")

WHOLE_REST_IMG   = join(IMAGES_PATH, "whole_rest.png")
HALF_REST_IMG    = join(IMAGES_PATH, "half_rest.png")
QUARTER_REST_IMG = join(IMAGES_PATH, "quarter_rest.png")
EIGHTH_REST_IMG  = join(IMAGES_PATH, "eighth_rest.png")
SIXTEEN_REST_IMG = join(IMAGES_PATH, "sixteen_rest.png")

FLAT_IMG    = join(IMAGES_PATH, "flat.png")
SHARP_IMG   = join(IMAGES_PATH, "sharp.png")
NATURAL_IMG = join(IMAGES_PATH, "natural.png")

# fonts
MAIN_MENU_FONT = join(FONTS_PATH, "ajile.ttf")
NOTES_FONT     = join(FONTS_PATH, "VeraMono.ttf")


bassClefImages = [
    "fa1.png", "fa2.png", "fb1.png", "fb2.png", "fc1.png", "fc2.png", "fc3.png",
    "fd1.png", "fd2.png", "fe1.png", "fe2.png", "ff1.png", "ff2.png", "fg1.png",
    "fg2.png"
]

trebleClefImages = [
    "ga3.png", "ga4.png", "gb3.png", "gb4.png", "gc4.png", "gc5.png", "gd3.png", 
    "gd4.png", "ge3.png", "ge4.png", "gf3.png", "gf4.png", "gg3.png", "gg4.png"
]

# these are the notes corresponding to the bassClefImages
bassNotes = [
    'A', 'A', 'B', 'B', 'C', 'C', 'C',
    'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G'
]

# these are the notes corresponding to the trebleClefImages
trebleNotes = [
    'A', 'A', 'B', 'B', 'C', 'C', 'D',
    'D', 'E', 'E', 'F', 'F', 'G', 'G'
]

