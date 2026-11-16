#!/usr/bin/env python3
"""Apply the QK61 Workman+ergo *logic* on top of the V65 V3 factory keymap.

Usage: python3 port_layout.py QK61_LAYOUT.json V65_FACTORY_keymap.bin OUT.layout.json

- Layer 0: factory V65; only alpha keys (A-Z, ;) become Workman; Caps -> MO(2).
- Layer 1: factory V65 Fn layer, untouched.
- Layer 2: QK61 ergo layer (its layer 1) inside the alpha block + space; a key is set only
  where it differs both from the QK61 base and from the new V65 base, everything else is KC_TRNS (V65 arrows, Del,
  PgUp/PgDn, knob keep working from layer 0).
- Layer 3: factory, untouched.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viakc import name  # noqa: E402

src, factory_bin, out = sys.argv[1:4]
QC, VR, VC = 16, 8, 15
ERGO_SRC, ERGO_DST = 1, 2  # QK61 ergo layer -> V65 layer

# QK61 -> V65 matrix positions of the shared 60% block (alpha rows + space)
POS = {"0,0": "1,0", "4,0": "4,0", "4,13": "4,12", "5,5": "5,6"}
POS.update({f"1,{c}": f"1,{c}" for c in range(1, 14)})
POS.update({f"2,{c}": f"2,{c}" for c in range(14)})
POS.update({f"3,{c}": f"3,{c}" for c in list(range(12)) + [13]})
POS.update({f"4,{c}": f"4,{c}" for c in range(2, 12)})
CAPS = "3,0"
ALPHA = {f"KC_{ch}" for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"} | {"KC_SCLN"}


def idx(p, cols):
    r, c = map(int, p.split(","))
    return r * cols + c


q = json.load(open(src))["layers"]
raw = open(factory_bin, "rb").read()
factory = [[name(int.from_bytes(raw[(l * VR * VC + i) * 2:][:2], "big")) for i in range(VR * VC)]
           for l in range(4)]
layers = [list(L) for L in factory]

# Layer 0: Workman letters + Caps -> MO(ergo)
for qp, vp in POS.items():
    qk, vk = q[0][idx(qp, QC)], factory[0][idx(vp, VC)]
    if qk in ALPHA and vk in ALPHA:
        layers[0][idx(vp, VC)] = qk
layers[0][idx(CAPS, VC)] = f"MO({ERGO_DST})"

# Layer 2: ergo layer = only keys that differ from the new base
# firmware rejects writes to non-existent matrix slots (factory 0xffff) -> keep them
layers[ERGO_DST] = [k if k == "0xffff" else "KC_TRNS" for k in factory[ERGO_DST]]
for qp, vp in POS.items():
    if vp == CAPS:
        continue
    qk = q[ERGO_SRC][idx(qp, QC)]
    if qk not in ("KC_TRNS", q[0][idx(qp, QC)], layers[0][idx(vp, VC)]):
        layers[ERGO_DST][idx(vp, VC)] = qk

json.dump({"name": "CIDOO V65 V3", "vendorProductId": (0x320F << 16) | 0x5055,
           "macros": [""] * 16, "layers": layers}, open(out, "w"), indent=2)

# Report: physical rows from the VIA definition (knob press = 0,14)
ROWS = [[f"1,{c}" for c in range(14)] + ["0,14"],
        [f"2,{c}" for c in range(14)] + ["1,14"],
        [f"3,{c}" for c in range(12)] + ["3,13", "2,14"],
        ["4,0"] + [f"4,{c}" for c in range(2, 13)] + ["4,13", "3,14"],
        ["5,0", "5,1", "5,2", "5,6", "5,9", "5,10", "5,12", "5,13", "5,14"]]
for l in (0, 2):
    print(f"\n### Layer {l}   (* = changed vs factory)")
    for row in ROWS:
        print("  " + " ".join(
            (layers[l][idx(p, VC)].replace("KC_", "").replace("TRNS", "·")
             + ("*" if layers[l][idx(p, VC)] != factory[l][idx(p, VC)] else "")).ljust(8)
            for p in row))
diff = sum(a != b for l in range(4) for a, b in zip(layers[l], factory[l]))
print(f"\nkeys changed vs factory: {diff}; layers 1 and 3 untouched:",
      layers[1] == factory[1] and layers[3] == factory[3])
