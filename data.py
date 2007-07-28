from os.path import join

CONFIG_FILE = "~/.readMusic.config"

# paths
DATA_PATH   = "data"
FONTS_PATH  = join(DATA_PATH, "fonts")
IMAGES_PATH = join(DATA_PATH, "images")
SOUNDS_PATH = join(DATA_PATH, "sounds")

# images
WRONG_IMG         = join(IMAGES_PATH, "wrong.png")
CORRECT_IMG       = join(IMAGES_PATH, "correct.png")
ICON_IMG          = join(IMAGES_PATH, "notes.gif")

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

SOUND_ON_IMG  = join(IMAGES_PATH, "sound_on.png")
SOUND_OFF_IMG = join(IMAGES_PATH, "sound_off.png")

BACKGROUND_IMG  = join(IMAGES_PATH, "background.png")
TIMER_IMG       = EIGHTH_STEM_UP_IMG
#TIMER_FULL_IMG  = join(IMAGES_PATH, "timer_full.png")
#TIMER_EMPTY_IMG = join(IMAGES_PATH, "timer_empty.png")

# fonts
MAIN_MENU_FONT = join(FONTS_PATH, "ajile.ttf")
NOTES_FONT     = join(FONTS_PATH, "goodfish.ttf")
SCORE_FONT     = join(FONTS_PATH, "SCRIPTIN.ttf")
LEGEND_FONT    = MAIN_MENU_FONT

CURSOR_DATA = (                  # sized 24x24
"          XXXX          ", 
"          X..X          ", 
"          X...X         ", 
"          X....X        ", 
"          X..XX.X       ", 
"          X..X X.X      ", 
"          X..X  X.X     ", 
"          X..X  X.X     ", 
"          X..X  X.X     ", 
"          X..X  X.X     ", 
"          X..X  X.X     ", 
"          X..X X.X      ", 
"          X..X XXX      ", 
"          X..X          ", 
"        XXX..X          ", 
"     XXX.....X          ", 
"   XX........X          ", 
"  XX.........X          ", 
" XX..........X          ", 
" XX..........X          ", 
" XX........XX           ", 
"  XX.....XX             ", 
"    XXXXX               ",
"                        ")

