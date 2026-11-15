"""Legacy QMK keycode <-> VIA name tables (VIA protocol <= 10)."""

# ---- keycode -> VIA name (legacy QMK numbering used by VIA protocol <= 10) ----
BASIC = {0x00: "KC_NO", 0x01: "KC_TRNS"}
for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    BASIC[0x04 + i] = f"KC_{ch}"
for i, ch in enumerate("1234567890"):
    BASIC[0x1E + i] = f"KC_{ch}"
for code, n in {0x28: "ENT", 0x29: "ESC", 0x2A: "BSPC", 0x2B: "TAB", 0x2C: "SPC", 0x2D: "MINS",
                0x2E: "EQL", 0x2F: "LBRC", 0x30: "RBRC", 0x31: "BSLS", 0x32: "NUHS", 0x33: "SCLN",
                0x34: "QUOT", 0x35: "GRV", 0x36: "COMM", 0x37: "DOT", 0x38: "SLSH", 0x39: "CAPS",
                0x46: "PSCR", 0x47: "SLCK", 0x48: "PAUS", 0x49: "INS", 0x4A: "HOME", 0x4B: "PGUP",
                0x4C: "DEL", 0x4D: "END", 0x4E: "PGDN", 0x4F: "RGHT", 0x50: "LEFT", 0x51: "DOWN",
                0x52: "UP", 0x53: "NLCK", 0x54: "PSLS", 0x55: "PAST", 0x56: "PMNS", 0x57: "PPLS",
                0x58: "PENT", 0x63: "PDOT", 0x64: "NUBS", 0x65: "APP", 0x67: "PEQL",
                0xA5: "PWR", 0xA6: "SLEP", 0xA7: "WAKE", 0xA8: "MUTE", 0xA9: "VOLU", 0xAA: "VOLD",
                0xAB: "MNXT", 0xAC: "MPRV", 0xAD: "MSTP", 0xAE: "MPLY", 0xAF: "MSEL", 0xB0: "EJCT",
                0xB1: "MAIL", 0xB2: "CALC", 0xB3: "MYCM", 0xB4: "WSCH", 0xB5: "WHOM", 0xB6: "WBAK",
                0xB7: "WFWD", 0xB8: "WSTP", 0xB9: "WREF", 0xBA: "WFAV", 0xBD: "BRIU", 0xBE: "BRID",
                0xE0: "LCTL", 0xE1: "LSFT", 0xE2: "LALT", 0xE3: "LGUI", 0xE4: "RCTL", 0xE5: "RSFT",
                0xE6: "RALT", 0xE7: "RGUI"}.items():
    BASIC[code] = f"KC_{n}"
for i in range(12):
    BASIC[0x3A + i] = f"KC_F{i + 1}"
for i in range(12):
    BASIC[0x68 + i] = f"KC_F{i + 13}"
for i, n in enumerate(["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P0"]):
    BASIC[0x59 + i] = f"KC_{n}"
MODWRAP = {0x01: "C", 0x02: "S", 0x04: "A", 0x08: "G", 0x11: "RCTL", 0x12: "RSFT",
           0x14: "RALT", 0x18: "RGUI", 0x03: "C_S", 0x06: "LSA", 0x05: "LCA", 0x0F: "HYPR", 0x07: "MEH"}
RGB = {0x5CC2: "RGB_TOG", 0x5CC3: "RGB_MOD", 0x5CC4: "RGB_RMOD", 0x5CC5: "RGB_HUI", 0x5CC6: "RGB_HUD",
       0x5CC7: "RGB_SAI", 0x5CC8: "RGB_SAD", 0x5CC9: "RGB_VAI", 0x5CCA: "RGB_VAD", 0x5CCB: "RGB_SPI",
       0x5CCC: "RGB_SPD", 0x5C00: "RESET", 0x5C16: "KC_GESC"}


def name(k):
    if k in BASIC:
        return BASIC[k]
    if k in RGB:
        return RGB[k]
    if 0x0100 <= k < 0x2000 and (k & 0xFF) in BASIC and (k >> 8) in MODWRAP:
        return f"{MODWRAP[k >> 8]}({BASIC[k & 0xFF]})"
    if 0x4000 <= k < 0x5000 and (k & 0xFF) in BASIC:
        return f"LT({(k >> 8) & 0xF},{BASIC[k & 0xFF]})"
    if 0x5010 <= k <= 0x501F:
        return f"TO({k & 0xF})"
    for base, fn in [(0x5100, "MO"), (0x5200, "DF"), (0x5300, "TG"), (0x5400, "OSL"), (0x5800, "TT")]:
        if base <= k <= base + 0x1F:
            return f"{fn}({k & 0x1F})"
    if 0x5F80 <= k <= 0x5F8F:
        return f"CUSTOM({k - 0x5F80})"
    if 0x5700 <= k <= 0x570F:
        return f"MACRO({k - 0x5700})"
    return f"0x{k:04x}"


CODE = {}
for _k in range(0x10000):
    CODE.setdefault(name(_k), _k)


def code(n):
    """VIA name or 0xNNNN hex string -> 16-bit keycode."""
    return int(n, 16) if n.startswith("0x") else CODE[n]
