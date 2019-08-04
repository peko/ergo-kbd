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
         .map((t)->t.replace(/^\s+/,'').split /\s+/g)


read_layout = (file)->
  group = parse_file "#{__dirname}/#{file}"
  layout = {}
  for level in group
    for row, row_i in level
      for key, key_i in row
        key_name = key_names[row_i][key_i]
        symbol = symbols[key]
        symbol?= "NoSymbol"
        layout[key_name]?=[]
        layout[key_name].push symbol
  layout

generate_keys = (g1, g2)->
  ("  key <#{k}> {[ #{v.join(', ')} ], [#{g2[k].join(', ')}] };" for k, v of g1).join("\n")
  
g1 = read_layout "group1.txt"
g2 = read_layout "group2.txt"
keys = generate_keys g1, g2

xkb_symbols = """
xkb_symbols {
      include "pc"
      
      include "us(workman)"

      include "level5"
      key.type[Group1] = "EIGHT_LEVEL";

      #{keys}
      key.type[Group1] = "ONE_LEVEL";
      key <SPCE> {
        [ISO_Level5_Shift],[ISO_Level5_Shift],
        actions[Group1]= [ SetMods(modifiers=LevelFive)],
        actions[Group2]= [ SetMods(modifiers=LevelFive)]
      };
     
      include "group(shifts_toggle)"  // switch
      include "ergo(overlay1)"        // keys binding
      include "ergo(caps_overlay1)"   // keys binding
};
"""

xkb_keymap = """
xkb_keymap {

  xkb_keycodes{include "evdev+aliases(qwerty)"};
  xkb_types{include "complete+ergo"};
  
  xkb_compat{
      include "complete" 
      include "ergo(overlay1)"    
  };

  #{xkb_symbols}
 
};
"""

console.log xkb_keymap
