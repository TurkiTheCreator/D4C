# D4C

```
 ______   ___ _____
|  _  \ /   /  __ \
| | | |/ /| | /  \/
| | | / /_| | |
| |/ /\___  | \__/\
|___/     |_/\____/
```

A small CLI tool for translating between **binary, hex, decimal, and ASCII** —
built for reversing/crackme work where you're constantly converting values
between formats and doing quick XOR math.

## Features

- Auto-detects whether input is binary, hex, decimal, or plain text
- Force a specific input/output format with `--from` / `--to`
- Built-in `xor` subcommand for byte-level XOR puzzles (crackmes, CTFs)

## Usage

```bash
d4c 0x66                    # auto-detect input, show all formats
d4c 01100110                # binary input
d4c 102                     # decimal input
d4c Hello                   # ascii input

d4c 0x66 --to dec           # only print decimal
d4c 33 --from dec --to hex  # force input/output formats

d4c xor 0x13 0x5b           # XOR two values, show result in all formats
d4c --no-banner 0x66        # suppress the banner (useful when piping output)
```

## Installation

```bash
git clone https://github.com/TurkiTheCreator/D4C.git
cd D4C
chmod +x d4c.py
mkdir -p ~/.local/bin
cp d4c.py ~/.local/bin/d4c
```

Make sure `~/.local/bin` is on your `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then run it from anywhere:

```bash
d4c 0x66
```

## License

MIT
