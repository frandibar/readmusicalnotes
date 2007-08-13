from os.path import join
from gethomedir import get_home_dir

# global constants
CONFIG_FILE = get_home_dir() + "/.readMusic.config"
DEBUG = False
ANIMATION_FR = 100
FOREVER = -1

# paths
RESOURCE_PATH   = "resources"
FONTS_PATH  = join(RESOURCE_PATH, "fonts")
IMAGES_PATH = join(RESOURCE_PATH, "images")
SOUNDS_PATH = join(RESOURCE_PATH, "sounds")

# images
WRONG_IMG    = join(IMAGES_PATH, "wrong.png")
CORRECT_IMG  = join(IMAGES_PATH, "correct.png")
ICON_IMG     = join(IMAGES_PATH, "notes.gif")

TREBLE_CLEF_IMG     = join(IMAGES_PATH, "2xtreble_clef.png")
BASS_CLEF_IMG       = join(IMAGES_PATH, "2xbass_clef.png")

TREBLE_CLEF_SEL_IMG   = join(IMAGES_PATH, "treble_clef_icon_sel.png")
TREBLE_CLEF_UNSEL_IMG = join(IMAGES_PATH, "treble_clef_icon_unsel.png")
BASS_CLEF_SEL_IMG     = join(IMAGES_PATH, "bass_clef_icon_sel.png")
BASS_CLEF_UNSEL_IMG   = join(IMAGES_PATH, "bass_clef_icon_unsel.png")
SOUND_SEL_IMG         = join(IMAGES_PATH, "sounds_icon_sel.png")
SOUND_UNSEL_IMG       = join(IMAGES_PATH, "sounds_icon_unsel.png")
TIMER_SEL_IMG         = join(IMAGES_PATH, "timer_icon_sel.png")
TIMER_UNSEL_IMG       = join(IMAGES_PATH, "timer_icon_unsel.png")
LANGUAGE_SEL_IMG      = join(IMAGES_PATH, "language_icon_sel.png")
LANGUAGE_UNSEL_IMG    = join(IMAGES_PATH, "language_icon_unsel.png")

WHOLE_IMG             = join(IMAGES_PATH, "whole.png")
HALF_STEM_UP_IMG      = join(IMAGES_PATH, "half_stem_up.png")
HALF_STEM_DOWN_IMG    = join(IMAGES_PATH, "half_stem_down.png")
QUARTER_STEM_UP_IMG   = join(IMAGES_PATH, "2xquarter_stem_up.png")
QUARTER_STEM_DOWN_IMG = join(IMAGES_PATH, "2xquarter_stem_down.png")
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

#SOUND_ON_IMG  = join(IMAGES_PATH, "sound_on.png")
#SOUND_OFF_IMG = join(IMAGES_PATH, "prohibited.png")

BACKGROUND_IMG  = join(IMAGES_PATH, "background.png")
DECORATION1_IMG = join(IMAGES_PATH, "curl1.png")
DECORATION2_IMG = join(IMAGES_PATH, "curl2.png")
DECORATION3_IMG = join(IMAGES_PATH, "curl3.png")
FLARE_IMG       = join(IMAGES_PATH, "flare.png")
MENU_MARKER_IMG = join(IMAGES_PATH, "marker.png")

# fonts
MAIN_MENU_FONT = join(FONTS_PATH, "ajile.ttf")
OPTIONS_FONT   = join(FONTS_PATH, "GenI102.ttf")
NOTES_FONT     = OPTIONS_FONT
SCORE_FONT     = join(FONTS_PATH, "SCRIPTIN.ttf")
LEGEND_FONT    = SCORE_FONT

# sounds
INTRO_SND    = join(SOUNDS_PATH, "bach_846_prelude1.ogg")
TICTAC_SND   = join(SOUNDS_PATH, "ticking.wav")
TIMEISUP_SND = join(SOUNDS_PATH, "tam.wav")
MENU_SND     = join(SOUNDS_PATH, "xyloc3.wav")
ENTER_SND    = join(SOUNDS_PATH, "enter.wav")
OPTION_SND   = MENU_SND

noteSounds = { "b3": join(SOUNDS_PATH, "b3.ogg"), 
               "a3": join(SOUNDS_PATH, "a3.ogg"),
               "g3": join(SOUNDS_PATH, "g3.ogg"),
               "f3": join(SOUNDS_PATH, "f3.ogg"),
               "e3": join(SOUNDS_PATH, "e3.ogg"),
               "d3": join(SOUNDS_PATH, "d3.ogg"),
               "c3": join(SOUNDS_PATH, "c3.ogg")
}

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

