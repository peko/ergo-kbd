fs = require "fs" 
{symbols,key_names} = require "./layout_map"

levels = fs.readFileSync("layout.txt").toString("utf8")
levels = levels
  .split /-----/g
  .map (s)->
    s.split(/\n/g)
     .filter((r)->r.length)
     .map((t)->t.split /\s+/g)

layout = {}
for level in levels
  for row, row_i in level
    for key, key_i in row
      key_name = key_names[row_i][key_i]
      symbol = symbols[key]
      symbol?= "NoSymbol"
      layout[key_name]?=[]
      layout[key_name].push symbol

keys = ("  key <#{k}> {[ #{v.join(', ')} ]};" for k, v of layout).join("\n")
symbols = """
  partial alphanumeric_keys modifier_keys
  xkb_symbols "lv5" {
  #{keys}
  };"""
console.log symbols
