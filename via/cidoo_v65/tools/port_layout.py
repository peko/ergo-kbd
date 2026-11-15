#!/usr/bin/env python3
"""Port the CIDOO QK61 VIA layout (6x16) to CIDOO V65 V3 (8x15) by physical position.

Usage: python3 port_layout.py QK61_LAYOUT.json V65_BACKUP_keymap.bin OUT.layout.json
Starts from the V65 backup, so matrix slots that are not physical keys keep factory values.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viakc import name  # noqa: E402

src, backup, out = sys.argv[1:4]
QR, QC, VR, VC = 6, 16, 8, 15

# --- physical V65 rows (matrix "r,c"); knob = press 0,14, rotate 7,0 (ccw) / 7,1 (cw) ---
V65_ROWS = [
    ["1,%d" % c for c in range(14)] + ["0,14"],
    ["2,%d" % c for c in range(14)] + ["1,14"],
    ["3,%d" % c for c in range(12)] + ["3,13", "2,14"],
    ["4,0"] + ["4,%d" % c for c in range(2, 12)] + ["4,12", "4,13", "3,14"],
    ["5,0", "5,1", "5,2", "5,6", "5,9", "5,10", "5,12", "5,13", "5,14"],
]
KNOB = ["7,0", "7,1"]

# --- QK61 -> V65 physical position map ---
POS = {"0,0": "1,0", "4,0": "4,0", "4,13": "4,12",
       "5,0": "5,0", "5,1": "5,1", "5,2": "5,2", "5,5": "5,6",
       "5,9": "5,9",    # Tab/RAlt/Left -> V65 RAlt slot
       "5,12": "5,10"}  # MO(2)/MO(3)  -> V65 Fn slot (replaces vendor Fn 0x5f10)
POS.update({"1,%d" % c: "1,%d" % c for c in range(1, 14)})
POS.update({"2,%d" % c: "2,%d" % c for c in range(14)})
POS.update({"3,%d" % c: "3,%d" % c for c in list(range(12)) + [13]})
POS.update({"4,%d" % c: "4,%d" % c for c in range(2, 12)})
DROPPED = ["5,10", "5,11"]  # QK61 App / RCtl: no room left of the V65 arrows

# --- QK61 vendor keycodes (by QK61 OEM JSON labels) -> V65 equivalents ---
CUSTOM = {
    "CUSTOM(0)": "CUSTOM(0)",   # MD_24G   -> 2.4G MODE
    "CUSTOM(1)": "CUSTOM(2)",   # MD_BLE1  -> BT 1
    "CUSTOM(2)": "CUSTOM(3)",   # MD_BLE2  -> BT 2
    "CUSTOM(3)": "CUSTOM(4)",   # MD_BLE3  -> BT 3
    "CUSTOM(4)": "CUSTOM(1)",   # MD_USB   -> USB MODE
    "CUSTOM(5)": "CUSTOM(13)",  # QK_BAT   -> BATT
    "CUSTOM(6)": "CUSTOM(9)",   # QK_WLO   -> LOCK WIN KEY
    "CUSTOM(8)": "RGB_TOG",     # RGB_RTOG -> RGB_TOG
    "CUSTOM(9)": "RESET",       # U_EE_CLR -> 0x5C00, what stock V65 has on Fn+Bksp
    "CUSTOM(12)": "CUSTOM(5)",  # LG_RMOD  -> LED LOGO MODE
    "CUSTOM(14)": "CUSTOM(6)",  # LG_HUD   -> LED LOGO COLOUR
}
# Extra V65 keys on layers 1-3 (layer 0 keeps factory Del/PgUp/PgDn/arrows)
EXTRA = ["1,14", "2,14", "3,14", "4,13", "5,12", "5,13", "5,14"]
EXTRA_OVERRIDE = {(2, "1,14"): "CUSTOM(1)"}  # USB MODE on Fn layer: v2.1 has no way back to USB


def idx(p, cols):
    r, c = map(int, p.split(","))
    return r * cols + c


q = json.load(open(src))
raw = open(backup, "rb").read()
stock = [[name(int.from_bytes(raw[(l * VR * VC + i) * 2:(l * VR * VC + i) * 2 + 2], "big"))
          for i in range(VR * VC)] for l in range(4)]
layers = [list(L) for L in stock]
notes = []
for l in range(4):
    for qp, vp in POS.items():
        k = q["layers"][l][idx(qp, QC)]
        k2 = CUSTOM.get(k, k)
        if k.startswith("CUSTOM(") and k not in CUSTOM:
            raise SystemExit(f"unmapped {k} at L{l} {qp}")
        layers[l][idx(vp, VC)] = k2
    if l:
        for vp in EXTRA:
            layers[l][idx(vp, VC)] = EXTRA_OVERRIDE.get((l, vp), "KC_TRNS")
    for qp in DROPPED:
        k = q["layers"][l][idx(qp, QC)]
        if k not in ("KC_NO", "KC_TRNS"):
            notes.append(f"L{l}: QK61 {qp}={k} dropped")

json.dump({"name": "CIDOO V65 V3", "vendorProductId": (0x320F << 16) | 0x5055,
           "macros": q["macros"], "layers": layers}, open(out, "w"), indent=2)

# --- report ---
inv = {v: k for k, v in POS.items()}
for l in range(4):
    print(f"\n### Layer {l}")
    for row in V65_ROWS:
        cells = []
        for vp in row:
            k = layers[l][idx(vp, VC)]
            qp = inv.get(vp)
            qk = q["layers"][l][idx(qp, QC)] if qp else None
            mark = "" if qp and qk == k else ("*" if qp else "+")
            cells.append(f"{k.replace('KC_', '')}{mark}")
        print("  " + " | ".join(cells))
    print("  knob: " + " / ".join(layers[l][idx(p, VC)] for p in ["7,0", "0,14", "7,1"]))
print("\n" + "\n".join(notes))
