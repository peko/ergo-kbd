keys = (p,c)-> [1..c].map (i)->"#{p}#{('0'+i)[-2..]}"
c = (n)->"Cyrillic_#{n}"
symbols = (text)->
  o = {}
  o[c] = c for c in text
  o

cyr = {}
Cyr = {}
cyr_names = "io shorti tse u ka ie en ghe sha shcha ze ha hardsign ef yeru ve a pe er o el de zhe e ya che es em i te softsign be yu".split " "
cyr_symbols = "ёйцукенгшщзхъфывапролджэячсмитьбю"
for s, i in  cyr_symbols
  cyr[s] = "Cyrillic_#{cyr_names[i]}"
  Cyr[s.toUpperCase()] = "Cyrillic_#{cyr_names[i].toUpperCase()}"

module.exports =
  key_names: [
    keys("AD",13)   # 1  2  3  4  5    6  7  8  9  0  1  2  3
    keys("AC",11)   #  1  2  3  4  5    6  7  8  9  0  1
    keys("AB",10)]  #   1  2  3  4  5    6  7  8  9  0

  symbols: {
  
    symbols("0123456789")...
    symbols("ABCDEFGHIJKLMNOPQRSTUVWXYZ")...
    symbols("abcdefghijklmnopqrstuvwxyz")...
    cyr...
    Cyr...

    "cp": "Caps_Lock"
    "tb": "Tab"
    "sr": "Shift_R"
    "sl": "Shift_L"
    "es": "Escape"
    
    "sp": "space"
    "tb": "Tab"
    "rt": "Return"
    "bs": "backslash"
    
    "al": "Meta"
    "st": "Shift"
    "ct": "Control"
     
    "`": "grave"
    "~": "asciitilde"
    "!": "exclam"
    "@": "at"
    "#": "numbersign"
    "$": "dollar"
    "%": "percent"
    "^": "asciicircum"
    "&": "ampersand"
    "*": "asterisk"
    "-": "minus"
    "_": "underscore"
    "=": "equal"
    "+": "plus"
    "(": "parenleft"
    ")": "parenright"
    "[": "bracketleft"
    "]": "bracketright"
    "{": "braceleft"
    "}": "braceright"
    ";": "semicolon"
    ":": "colon"
    "'": "apostrophe"
    '"': "quotedbl"
    "<": "less"
    ">": "greater"
    ",": "comma"
    ".": "period"
    "/": "slash"
    "?": "question"
    "\\": "backslash"
    "|": "bar"
    
    "↑": "Up"
    "←": "Left"
    "↓": "Down"
    "→": "Right"
    "⇤": "Home" 
    "⇥": "End"
    "↰": "Escape"
    "↲": "Return"
    "↟": "Prior"
    "↡": "Next"
    "↚": "Delete"
    "↛": "BackSpace"
  }
