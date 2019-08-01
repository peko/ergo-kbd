#!/usr/bin/env coffee

fs = require "fs" 
{symbols,key_names} = require "./layout_map"

parse_file = (file)->
  fs.readFileSync(file)
    .toString("utf8")
      .split /-----/g
      .map (s)->
        s.split(/\n/g)
         .filter((r)->r.length)
         .map((t)->t.split /\s+/g)

group1 = parse_file "group1.txt"

layout = {}
for level in group1
  for row, row_i in level
    for key, key_i in row
      key_name = key_names[row_i][key_i]
      symbol = symbols[key]
      symbol?= "NoSymbol"
      layout[key_name]?=[]
      layout[key_name].push symbol

keys = ("  key <#{k}> {[ #{v.join(', ')} ]};" for k, v of layout).join("\n")
xkb_symbols = """
  include "level5"
  key.type[Group1] = "EIGHT_LEVEL";
  #{keys}
"""

xkb_keymap = """
xkb_keymap {

  xkb_keycodes{ include "evdev+aliases(qwerty)"};
  xkb_types   { include "complete"             };
  xkb_compat  { include "complete"             };
  xkb_symbols {
    include "pc"
    include "us(workman)"

    // key.type[Group1] = "ONE_LEVEL";
    // key <KP5> { [ISO_Level5_Shift], actions[Group1]= [ SetMods(modifiers=LevelFive)] };
    // key <KP6> { [ISO_Level5_Shift], actions[Group1]= [ SetMods(modifiers=Shift+LevelFive)] };
    // key <KP7> { [ISO_Level5_Shift], actions[Group1]= [ SetMods(modifiers=LevelThree+LevelFive)] };
    // key <KP8> { [ISO_Level5_Shift], actions[Group1]= [ SetMods(modifiers=Shift+LevelThree+LevelFive)] };
  };
  XKB_geometry{include "pc(pc105)"};
};
"""

console.log xkb_keymap
