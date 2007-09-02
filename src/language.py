# -*- coding: latin-1 -*-

ENGLISH, SPANISH = range(2)

languages = ["english", "espanol"]

dict = {}

# define constants for use in dictionary
T_NOTES_QUIZ, T_OPTIONS, T_QUIT, T_TREBLE_CLEF, T_BASS_CLEF, T_SOUNDS, T_TIMER, T_SOFT_TRANSITIONS, T_LANGUAGE, T_BACK, T_NO, T_YES, T_ENGLISH, T_SPANISH, T_OFF, T_SECONDS, T_5SEC, T_10SEC, T_15SEC, T_20SEC, T_PRESS_KEY, T_TIMEISUP, T_EXPLAIN_SOFT_TRANSITIONS, T_DO, T_RE, T_MI, T_FA, T_SOL, T_LA, T_SI, T_FULLSCREEN = range(31) 

# dictionary of language translations
dict[T_NOTES_QUIZ] = ["Notes Quiz", "Aprender Notas"]
dict[T_OPTIONS]    = ["Options", "Opciones"]
dict[T_QUIT]       = ["Quit", "Salir"]

dict[T_TREBLE_CLEF]      = ["Treble clef", "Clave de Sol"]
dict[T_BASS_CLEF]        = ["Bass clef", "Clave de Fa"]
dict[T_SOUNDS]           = ["Sounds", "Sonido"]
dict[T_TIMER]            = ["Timer", "Tiempo"]
dict[T_SOFT_TRANSITIONS] = ["Soft transitions", "Transiciones suaves"]
dict[T_LANGUAGE]         = ["Language", "Idioma"]
dict[T_FULLSCREEN]       = ["Fullscreen", "Pantalla Completa"]
dict[T_BACK]             = ["Back", "Volver"]
   
dict[T_NO]  = ["no", "no"]
dict[T_YES] = ["yes", "si"]

dict[T_ENGLISH]  = ["english", "english"]
dict[T_SPANISH]  = ["español", "español"]

dict[T_OFF] = ["off", "apagado"]

dict[T_SECONDS] = ["sec", "seg"]
dict[T_5SEC]  = ["5 sec", "5 seg"]
dict[T_10SEC] = ["10 sec", "10 seg"]
dict[T_15SEC] = ["15 sec", "15 seg"]
dict[T_20SEC] = ["20 sec", "20 seg"]

dict[T_PRESS_KEY] = ["Press any key to continue", "Presione una tecla para continuar"]
dict[T_TIMEISUP]  = ["Time is up!", "¡Se acabo el tiempo!"]

dict[T_EXPLAIN_SOFT_TRANSITIONS] = ["Show animations and screen effects", "Mostrar animaciones y efectos de pantalla"]

dict[T_DO] = ["C do", "C do"]
dict[T_RE] = ["D re", "D re"]
dict[T_MI] = ["E mi", "E mi"]
dict[T_FA] = ["F fa", "F fa"]
dict[T_SOL] = ["G sol", "G sol"]
dict[T_LA] = ["A la", "A la"]
dict[T_SI] = ["B si", "B si"]
