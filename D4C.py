#!/usr/bin/env python3
"""
D4C — Dirty Data, Converted Cheap
A CLI tool for translating between binary, hex, decimal, and ASCII,
plus quick XOR math for crackme-style challenges.

Usage examples:
    d4c 0x66                    # auto-detect input type, show all formats
    d4c 01100110                # binary input
    d4c 102                     # decimal input
    d4c Hello                   # ascii input
    d4c 0x66 --to dec           # show only decimal
    d4c 33 --from dec --to hex  # force input/output formats
    d4c xor 0x13 0x5b           # XOR two values, show result in all formats
"""

import argparse
import sys

BANNER = r"""
 ______   ___ _____
|  _  \ /   /  __ \
| | | |/ /| | /  \/
| | | / /_| | |
| |/ /\___  | \__/\
|___/     |_/\____/
"""


def clean(s: str) -> str:
    return s.replace("0x", "").replace("0X", "").replace("0b", "").replace(" ", "").strip()


def looks_binary(s: str) -> bool:
    c = clean(s)
    return c != "" and all(ch in "01" for ch in c)


def looks_hex(s: str) -> bool:
    c = clean(s)
    return c != "" and all(ch in "0123456789abcdefABCDEF" for ch in c) and not looks_binary(s)


def looks_decimal(s: str) -> bool:
    return s.strip().lstrip("-").isdigit()


def bytes_from_binary(s: str) -> bytes:
    c = clean(s)
    c = c.zfill((len(c) + 7) // 8 * 8)
    return bytes(int(c[i:i + 8], 2) for i in range(0, len(c), 8))


def bytes_from_hex(s: str) -> bytes:
    c = clean(s)
    if len(c) % 2 != 0:
        c = "0" + c
    return bytes.fromhex(c)


def bytes_from_decimal(s: str) -> bytes:
    n = int(s)
    length = max(1, (n.bit_length() + 7) // 8)
    return n.to_bytes(length, "big")


def bytes_from_ascii(s: str) -> bytes:
    return s.encode()


def detect_and_convert(raw: str, forced: str) -> bytes:
    if forced == "bin":
        return bytes_from_binary(raw)
    if forced == "hex":
        return bytes_from_hex(raw)
    if forced == "dec":
        return bytes_from_decimal(raw)
    if forced == "ascii":
        return bytes_from_ascii(raw)

    if looks_binary(raw):
        return bytes_from_binary(raw)
    if raw.strip().lower().startswith("0x"):
        return bytes_from_hex(raw)
    if looks_decimal(raw):
        return bytes_from_decimal(raw)
    if looks_hex(raw):
        return bytes_from_hex(raw)
    return bytes_from_ascii(raw)


def show(data: bytes, only: str):
    binary_str = " ".join(format(b, "08b") for b in data)
    hex_str = " ".join(format(b, "02x") for b in data)
    dec_str = str(int.from_bytes(data, "big"))
    try:
        ascii_str = data.decode("ascii")
    except UnicodeDecodeError:
        ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in data)

    outputs = {
        "bin": ("Binary", binary_str),
        "hex": ("Hex", hex_str),
        "dec": ("Decimal", dec_str),
        "ascii": ("ASCII", ascii_str),
    }

    if only == "all":
        for label, value in outputs.values():
            print(f"{label:<8}{value}")
    else:
        print(outputs[only][1])


def cmd_convert(args):
    raw = " ".join(args.value)
    data = detect_and_convert(raw, args.from_fmt)
    show(data, args.to_fmt)


def cmd_xor(args):
    a = int(args.a, 0) if args.a.lower().startswith("0x") else int(args.a, 16) if looks_hex(args.a) else int(args.a)
    b = int(args.b, 0) if args.b.lower().startswith("0x") else int(args.b, 16) if looks_hex(args.b) else int(args.b)
    result = a ^ b
    length = max(1, (result.bit_length() + 7) // 8)
    data = result.to_bytes(length, "big")
    print(f"{a:#x} ^ {b:#x} = {result:#x}")
    show(data, "all")


def main():
    # Manual dispatch: "xor" as a subcommand needs its own parser, since
    # mixing subparsers with a free-form positional list confuses argparse.
    if len(sys.argv) > 1 and sys.argv[1] == "xor":
        parser = argparse.ArgumentParser(prog="d4c xor", description="XOR two values and show the result")
        parser.add_argument("a", help="first value (hex like 0x13, or decimal)")
        parser.add_argument("b", help="second value (hex like 0x5b, or decimal)")
        parser.add_argument("--no-banner", action="store_true", help="suppress the D4C banner")
        args = parser.parse_args(sys.argv[2:])
        if not args.no_banner:
            print(BANNER)
        cmd_xor(args)
        return

    parser = argparse.ArgumentParser(
        prog="d4c",
        description="D4C — translate between binary, hex, decimal, and ASCII; XOR values for crackme work.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Subcommand: d4c xor <a> <b>   — XOR two values and show the result",
    )
    parser.add_argument("value", nargs="*", help="value to convert")
    parser.add_argument(
        "--from", dest="from_fmt", choices=["auto", "bin", "hex", "dec", "ascii"],
        default="auto", help="force interpretation of the input (default: auto-detect)"
    )
    parser.add_argument(
        "--to", dest="to_fmt", choices=["all", "bin", "hex", "dec", "ascii"],
        default="all", help="only print one output format (default: all)"
    )
    parser.add_argument("--no-banner", action="store_true", help="suppress the D4C banner")

    args = parser.parse_args()

    if not args.no_banner:
        print(BANNER)

    if not args.value:
        parser.print_help()
        sys.exit(1)
    cmd_convert(args)


if __name__ == "__main__":
    main()