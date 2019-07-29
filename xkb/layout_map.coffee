keys = (p,c)-> [1..c].map (i)->"#{p}#{('0'+i)[-2..]}"
symbols = (text)->
  o = {}
  for c in text
    o[c] = c
  o

module.exports =
  symbols: {
    symbols("ABCDEFGHIJKLMNOPQRSTUVWXYZ")...
    symbols("abcdefghijklmnopqrstuvwxyz")...
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
  }

  key_names: [
    ["TAB" , keys("AD",12)..., "BKSL"]
    ["CAPS", keys("AC",11)..., "RTRN"]
    ["LFSH", keys("AB",10)..., "RTSH"]]
