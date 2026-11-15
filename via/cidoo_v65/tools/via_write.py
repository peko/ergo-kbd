#!/usr/bin/env python3
"""Write a keymap to a VIA keyboard and verify by reading it back.

Usage:
  python3 via_write.py /dev/hidrawN LAYOUT.json   # VIA layout file (names / 0xNNNN)
  python3 via_write.py /dev/hidrawN keymap.bin    # raw backup from via_dump.py
Only the dynamic keymap is written (per-key VIA cmd 0x05); macros and lighting are untouched.
"""
import json, os, select, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from viakc import code  # noqa: E402

dev, src = sys.argv[1], sys.argv[2]
fd = os.open(dev, os.O_RDWR)


def q(*b):
    os.write(fd, bytes([0]) + bytes(b) + bytes(32 - len(b)))
    r, _, _ = select.select([fd], [], [], 1.0)
    if not r:
        raise TimeoutError(f"no reply to {bytes(b[:4]).hex()}")
    resp = os.read(fd, 32)
    if resp[0] != b[0]:
        raise RuntimeError(f"bad reply to {bytes(b[:4]).hex()}: {resp.hex()}")
    return resp


if src.endswith(".bin"):
    data = open(src, "rb").read()
else:
    layers = json.load(open(src))["layers"]
    data = b"".join(code(k).to_bytes(2, "big") for L in layers for k in L)

layers_n = q(0x11)[1]
assert len(data) % layers_n == 0 and len(data) == layers_n * 8 * 15 * 2, \
    f"size {len(data)} != {layers_n} layers * 8x15 * 2"

def read_all():
    buf = bytearray()
    while len(buf) < len(data):
        off, n = len(buf), min(28, len(data) - len(buf))
        r = q(0x12, off >> 8, off & 0xFF, n)
        assert r[1:4] == bytes([off >> 8, off & 0xFF, n]), f"read echo mismatch: {r.hex()}"
        buf += r[4:4 + n]
    return bytes(buf)


# Firmware ignores bulk SET (0x13), so write per key (0x05), only keys that differ
cur = read_all()
changed = 0
for i in range(0, len(data), 2):
    if cur[i:i + 2] == data[i:i + 2]:
        continue
    k = i // 2
    l, rc = divmod(k, 8 * 15)
    r_, c_ = divmod(rc, 15)
    resp = q(0x05, l, r_, c_, data[i], data[i + 1])
    assert resp[1:6] == bytes([l, r_, c_, data[i], data[i + 1]]), f"set echo mismatch: {resp.hex()}"
    changed += 1
print(f"keys changed: {changed}")

back = read_all()
if bytes(back) != data:
    bad = [i // 2 for i in range(0, len(data), 2) if back[i:i + 2] != data[i:i + 2]]
    raise SystemExit(f"VERIFY FAILED at key indexes {bad[:20]} ({len(bad)} total)")
print(f"OK: wrote and verified {len(data)} bytes ({layers_n} layers)")
