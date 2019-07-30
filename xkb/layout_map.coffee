keys = (p,c)-> [1..c].map (i)->"#{p}#{('0'+i)[-2..]}"
c = (n)->"Cyrillic_#{n}"
symbols = (text)->
  o = {}
  o[c] = c for c in text
  o

cyr = {}
Cyr = {}
cyr_names = "io shorti tse u ka ie en ghe sha shcha ze ha hardsign ef yeru ve a pe er o el de zhe e ya che es em i te softsign be yu".split " "
cyr_symbols = "ёйцукенжшщзхъфывапролджеячсмитьбю"
for s, i in  cyr_symbols
  cyr[s] = "Cyrillic_#{cyr_names[i]}"
  Cyr[s.toUpperCase()] = "Cyrillic_#{cyr_names[i].toUpperCase()}"
  
module.exports =
  symbols: {
  
    symbols("0123456789")...
    symbols("ABCDEFGHIJKLMNOPQRSTUVWXYZ")...
    symbols("abcdefghijklmnopqrstuvwxyz")...
    cyr...
    Cyr...

    "sp": "space"
    "tb": "Tab"
    "rt": "Return"
     
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

  key_names: [
    ["TAB" , keys("AD",12)..., "BKSL"]
    ["CAPS", keys("AC",11)..., "RTRN"]
    ["LFSH", keys("AB",10)..., "RTSH"]]
