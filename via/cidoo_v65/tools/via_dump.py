#!/usr/bin/env python3
"""Read-only backup of a VIA keyboard (VIA protocol 9 / legacy QMK keycodes).

Usage: python3 via_dump.py /dev/hidrawN OUT_DIR ROWS COLS [VID PID NAME]

Only GET commands are sent: protocol version, layer count, keymap buffer,
macro count/size/buffer, rgblight values. Nothing is written to the keyboard.
"""
import json, os, select, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

dev, out = sys.argv[1], sys.argv[2]
ROWS, COLS = int(sys.argv[3]), int(sys.argv[4])
VID = int(sys.argv[5], 16) if len(sys.argv) > 5 else 0x320F
PID = int(sys.argv[6], 16) if len(sys.argv) > 6 else 0x5055
NAME = sys.argv[7] if len(sys.argv) > 7 else "CIDOO V65 V3"

fd = os.open(dev, os.O_RDWR)


def q(*b):
    os.write(fd, bytes([0]) + bytes(b) + bytes(32 - len(b)))
    r, _, _ = select.select([fd], [], [], 1.0)
    if not r:
        raise TimeoutError(f"no reply to {bytes(b).hex()}")
    resp = os.read(fd, 32)
    if resp[0] != b[0]:
        raise RuntimeError(f"bad reply to {bytes(b).hex()}: {resp.hex()}")
    return resp


proto = int.from_bytes(q(0x01)[1:3], "big")
layers = q(0x11)[1]
macro_count = q(0x0C)[1]
macro_size = int.from_bytes(q(0x0D)[1:3], "big")


def read_buf(cmd, total):
    data = bytearray()
    while len(data) < total:
        n = min(28, total - len(data))
        off = len(data)
        r = q(cmd, off >> 8, off & 0xFF, n)
        assert r[1:4] == bytes([off >> 8, off & 0xFF, n]), f"offset echo mismatch: {r.hex()}"
        data += r[4:4 + n]
    return bytes(data)


km_size = layers * ROWS * COLS * 2
keymap = read_buf(0x12, km_size)
# Firmware ignores per-key GET (0x04), so verify by reading everything twice
assert read_buf(0x12, km_size) == keymap, "keymap reads differ"
macros = read_buf(0x0E, macro_size)
assert read_buf(0x0E, macro_size) == macros, "macro reads differ"

rgb = {}
for key, vid in [("brightness", 0x80), ("effect", 0x81), ("effect_speed", 0x82), ("color", 0x83)]:
    try:
        rgb[key] = q(0x08, vid)[2:4].hex()
    except Exception as e:
        rgb[key] = f"error: {e}"

codes = [int.from_bytes(keymap[i:i + 2], "big") for i in range(0, km_size, 2)]
per_layer = ROWS * COLS
layer_codes = [codes[l * per_layer:(l + 1) * per_layer] for l in range(layers)]

from viakc import name  # noqa: E402


# ---- macros: NUL-separated; 0x01=tap 0x02=down 0x03=up followed by keycode ----
macro_list, cur, i = [], [], 0
while i < len(macros) and len(macro_list) < macro_count:
    b = macros[i]
    if b == 0:
        macro_list.append(cur); cur = []; i += 1
    elif b in (1, 2, 3) and i + 1 < len(macros):
        cur.append(("{" + name(macros[i + 1]) + "}") if b == 1 else f"<{b}:{name(macros[i + 1])}>"); i += 2
    else:
        cur.append(chr(b) if 32 <= b < 127 else f"\\x{b:02x}"); i += 1
macro_list = ["".join(m) for m in macro_list] + [""] * (macro_count - len(macro_list))

os.makedirs(out, exist_ok=True)
stamp = datetime.datetime.now().isoformat(timespec="seconds")
open(os.path.join(out, "keymap.bin"), "wb").write(keymap)
open(os.path.join(out, "macros.bin"), "wb").write(macros)
json.dump({
    "device": NAME, "vid": f"0x{VID:04x}", "pid": f"0x{PID:04x}", "hidraw": dev, "dumped_at": stamp,
    "via_protocol": proto, "layers": layers, "matrix": {"rows": ROWS, "cols": COLS},
    "macro_count": macro_count, "macro_buffer_size": macro_size, "rgblight_values_raw": rgb,
    "keymap_hex": [[[f"0x{c:04x}" for c in lc[r * COLS:(r + 1) * COLS]] for r in range(ROWS)] for lc in layer_codes],
    "macros_buffer_hex": macros.rstrip(b"\0").hex(),
}, open(os.path.join(out, "raw_dump.json"), "w"), indent=1)
json.dump({
    "name": NAME, "vendorProductId": (VID << 16) | PID, "macros": macro_list,
    "layers": [[name(c) for c in lc] for lc in layer_codes],
}, open(os.path.join(out, "via_layout.json"), "w"), indent=2)

unknown = sorted({name(c) for c in codes if name(c).startswith("0x")})
print(f"proto={proto} layers={layers} macros={macro_count}/{macro_size}B rgb={rgb}")
print("unmapped keycodes (kept as hex):", unknown)
for l, lc in enumerate(layer_codes):
    print(f"--- layer {l}")
    for r in range(ROWS):
        print("  " + " ".join(f"{name(c):>9}" for c in lc[r * COLS:(r + 1) * COLS]))
