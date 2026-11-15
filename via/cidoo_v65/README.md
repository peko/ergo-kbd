# CIDOO V65 V3

USB `320f:5055` (RDR CIDOO V65 V3), vendor QMK-like firmware, VIA protocol 9,
matrix 8×15, 4 layers, 16 macros (512 B buffer). Raw HID = interface 1
(usage page `0xFF60`).

## Contents

| Path | What |
|---|---|
| `original layout/` | Factory backup (2026-11-15): `keymap.bin` (exact 960 B dump), `macros.bin`, `raw_dump.json` (hex + rgblight values), `via_layout.json` (VIA Load format) |
| `workman layout/cidoo_v65.layout.v2.1.json` | Workman + ergo layout ported from `../cidoo_qk61/workman layout/cidoo_qk61.layout.v2.1.json` |
| `via definition/` | VIA definitions (USB / 2.4G) from [DenisGas/cidoo-v65-v3-via](https://github.com/DenisGas/cidoo-v65-v3-via) @ `7976aaa`, MIT |
| `tools/` | `via_dump.py` (read-only backup), `via_write.py` (write + verify), `port_layout.py` (QK61 → V65), `viakc.py` (legacy keycode names) |

| `manual/CIDOO_V65_V3_manual.pdf` | Official V3 manual (CN/EN), from cidootech.com |

Firmware binary is **not** backed up: VIA cannot read flash.

## Firmware availability (checked 2026-11-15)

- No official V65 firmware download: cidootech.com/blogs/firmware lists only V75 Pro; the manual says to contact support.
- [dongdevcom/V65](https://github.com/dongdevcom/V65) has a dump of the **original** V65 (Artery AT32F415, DFU `2e3c:df11`).
  V3 is a different platform (Evision `320f:5055`; the same ID is used by unrelated boards, e.g. Kreo Hive in
  OpenRGB issue #4831) — **do not flash V1/V2 or look-alike firmware on V3**.
- No known DFU/bootloader procedure for V3, so a flash backup is not possible.

## Manual notes (V3)

- **Hold Fn + Backspace 3 s = factory reset.** This is keycode `0x5C00` (`RESET`), kept on layer 2/3 Bksp
  like U_EE_CLR on QK61. After a reset: `tools/via_write.py … "workman layout/…v2.1.json"`.
- **Emergency wired mode:** hold Esc while switching power on. Power switch: towards USB port = OFF.
- Fn + Space → USB (factory layout; in v2.1 it is Fn + Del), Fn + V → 2.4G (long = pair),
  Fn + Z/X/C → BT 1–3 (long = pair, names "CIDOO V65 V3 -1/2/3").
- Fn + A / Fn + S = Win / Mac mode. Factory Fn `0x5f10` is "Fn1(3)": MO(1) in Win, MO(3) in Mac; Mac mode
  appears to use layer 2 as base — in v2.1 that would be the Fn layer. WIN/MAC keys are not mapped in v2.1.
- Hold Fn + B = battery level (number row 1…0 = 10…100 %). Fn blinks red = battery < 3.5 V, steady red = charging.
- Backlight off after 5 min idle; BT deep sleep after 30 min. VIA works in wired and 2.4G mode (matching JSON).

## Hardware: V65 V3 vs QK61 V2

| | V65 V3 | QK61 V2 |
|---|---|---|
| Layout | 65% ANSI, 64 keys + knob | 60%, 61 keys |
| Case | CNC aluminium, anodized | not stated in sources |
| Mount / plate | Gasket (Poron), PC plate | Gasket, PC plate |
| PCB | Hot-swap 3/5-pin, south-facing RGB | Hot-swap 3/5-pin, south-facing RGB |
| Dampening | Poron sandwich + bottom, socket pad, silicone | 5 layers: sandwich foam, PET film, IXPE, bottom foam, silicone |
| Switches | Quark Matte / Frosted Grey linear, 47–49 gf | CIDOO Pearl White linear, 40 gf |
| Keycaps | Dye-sub PBT | Double-shot PBT, Cherry profile |
| Battery | 3000 mAh | 3000 mAh |
| Connectivity | USB-C / BT 5.0 ×3 / 2.4G, mode via Fn keys | same, mode via hardware switch |
| Controller | Evision (VID `320f`) | VID `36b0` |

Sources: V3 manual (above), epomaker.com/products/cidoo-v65, mechkeys.com (V65 V3), keeb-finder.com,
cidootech.com/products/cidoo-qk61-v2, TechPowerUp V65 review (original V65).

## Commands

Find the raw HID node (number changes after replug):

```sh
for d in /sys/class/hidraw/hidraw*; do grep -qi 0000320F:00005055 $d/device/uevent \
  && xxd -p $d/device/report_descriptor | grep -q '^0660ff0961' && echo /dev/$(basename $d); done
```

```sh
python3 tools/via_dump.py  /dev/hidrawN OUT_DIR 8 15                               # backup
python3 tools/via_write.py /dev/hidrawN "workman layout/cidoo_v65.layout.v2.1.json" # apply layout
python3 tools/via_write.py /dev/hidrawN "original layout/keymap.bin"               # restore factory
```

Alternatively load the layout in usevia.app (Design → "Use V2 definitions" → Load the
JSON from `via definition/`, then Configure → Save/Load).

## Firmware quirks

- Supported: `0x01` protocol, `0x05` set keycode, `0x08` lighting get, `0x0C/0x0D/0x0E` macros, `0x11` layer count, `0x12` keymap buffer get.
- **Not supported:** `0x04` get keycode, `0x13` keymap buffer set, `0x14` encoder. Unknown
  commands return a stale `01 00 09 …` reply instead of `0xFF`. `via_write.py` therefore writes key by key.
- The knob is not an encoder: rotation = matrix keys `7,0` (ccw) / `7,1` (cw), press = `0,14`.
- Factory Fn is vendor keycode `0x5f10`; standard `MO(n)` works too.

## Port QK61 → V65 (v2.1)

Physical-position mapping; V65-only keys (Del, PgUp, PgDn, arrows) keep factory values on
layer 0 and are `KC_TRNS` on layers 1–3.

- Right of space: QK61 has Tab, App, RCtl, MO(2); V65 has 2 keys → **Tab, MO(2)** (App and RCtl dropped).
  MO(2) replaces the factory Fn (`0x5f10`).
- **USB MODE** added at Fn + Del (QK61 v2.1 had none; the factory Fn + Space is now RGB_TOG).
- Vendor keycodes remapped by meaning (indexes differ between models):

  | QK61 | V65 |
  |---|---|
  | CUSTOM(0) MD_24G | CUSTOM(0) 2.4G |
  | CUSTOM(1–3) MD_BLE1–3 | CUSTOM(2–4) BT 1–3 |
  | CUSTOM(4) MD_USB | CUSTOM(1) USB |
  | CUSTOM(5) QK_BAT | CUSTOM(13) BATT |
  | CUSTOM(6) QK_WLO | CUSTOM(9) LOCK WIN |
  | CUSTOM(8) RGB_RTOG | RGB_TOG |
  | CUSTOM(9) U_EE_CLR | `0x5C00` (factory V65 Fn + Bksp; exact effect unverified) |
  | CUSTOM(12) LG_RMOD / CUSTOM(14) LG_HUD | CUSTOM(5) LOGO MODE / CUSTOM(6) LOGO COLOUR |

Verified on hardware: write + readback, persistence after replug, layer 1 (Caps hold),
layer 2 (Fn + Del → USB). Fn + Caps toggles Caps Lock (layer 2 `KC_CAPS`).
