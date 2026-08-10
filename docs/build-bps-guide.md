# Building `EliteRedux.bps` From Source

This document explains how to compile a `.bps` patch file from the Elite Redux source code.

A `.bps` file is a **binary patch** — it contains only the *differences* between a clean vanilla Pokémon Emerald ROM and the modified Elite Redux ROM. Players apply it to a clean Emerald ROM using a patching tool like [FLIPS](https://github.com/Alcaro/Flips). The build process therefore requires **two** ROMs: the base (vanilla) and the hack (Elite Redux), which are then diffed into a single `.bps`.

## Docker build (recommended)

With Docker running, build only the full Elite Redux ROM with:

```sh
make docker-rom
# equivalent: ./docker/build-bps.sh --rom
```

The ROM is written to `pokeemerald_modern.gba`. Build both the ROM and its BPS
patch with:

```sh
make docker-bps
# equivalent: ./docker/build-bps.sh --bps
```

The wrapper builds a compact Debian Trixie image containing the ARM toolchain, host
compiler, Poryscript, Python protobuf runtime, protoc 29.2, and a verified
vanilla Emerald ROM. A CLI-only FLIPS binary is compiled from its pinned
official source without GTK. The wrapper bind-mounts the repository at `/workspace`, so the
results are written to the repository and owned by the current host user.
Running the script without a flag defaults to `--bps`.

Trixie is intentional: current upstream source uses C23 fixed-underlying enum
syntax, which is unsupported by Debian Bookworm's ARM GCC 12 package.

The same image can regenerate or validate codegen output:

```sh
make docker-codegen       # regenerate generated C headers
make docker-protos        # regenerate committed Python protobuf bindings
make docker-check-protos  # verify the committed bindings
make docker-test-codegen  # run the Python codegen tests
make docker-shell         # open a shell in the build environment
```

Set `DOCKER_IMAGE` to choose another local image tag, `DOCKER_PLATFORM` to
override the default `linux/amd64` platform, or `JOBS` to limit parallelism.
The amd64 default is required by the Poryscript 3.5.2 Linux release.

The Docker context excludes the source tree because it is mounted only when
the container runs. Multi-stage builds retain only the 16 MB verified vanilla
ROM rather than its source and build tree. Use `docker system df` to inspect
usage; removing `eliteredux-bps-build:local` is sufficient to remove the final
image when it is no longer needed.

---

## Prerequisites

The build needs three categories of tools: the **ARM cross-compiler** (to compile GBA code), **host build tools** (to compile helper programs that run on your machine), and **language runtimes** (for the Kotlin/Java codegen system).

### 1. ARM Cross-Compiler (`gcc-arm-none-eabi`)

The GBA uses an ARM7TDMI CPU. You need a cross-compiler that targets it:

- `arm-none-eabi-gcc` / `arm-none-eabi-binutils` — compiles and links C/assembly into ARM machine code
- ARM newlib and libstdc++ headers — provide the embedded C/C++ standard headers

| Distro | Command |
|---|---|
| Debian/Ubuntu | `sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-dev` |
| Arch Linux | `sudo pacman -S arm-none-eabi-gcc arm-none-eabi-binutils arm-none-eabi-newlib` |

### 2. Host Build Tools

Several helper programs in `tools/` are compiled natively (to run on your machine, not the GBA):

- **`gcc` / `g++` / `make`** — almost always pre-installed
- **`libpng` (dev headers)** — required by `gbagfx` and `rsfont`, which convert PNG images into GBA tile formats
- **Python 3.10+** — runs the protobuf-to-C code generator

| Distro | Command |
|---|---|
| Debian/Ubuntu | `sudo apt install build-essential libpng-dev python3 python3-pip` |
| Arch Linux | `sudo pacman -S base-devel libpng python python-pip` |

### 3. Python Protobuf Runtime

Elite Redux uses a Python protobuf codegen system in `tools/codegen/`. It reads `.textproto` data files for abilities, species, moves, trainers, items, and wiki articles, then generates the C headers compiled into the ROM.

Install its runtime dependency with:

```sh
python3 -m pip install -r tools/codegen/python/requirements.txt
```

The generated Python protobuf bindings are committed. `protoc` is only needed when changing `.proto` schemas, not when changing `.textproto` game data or building the ROM.

### 4. Poryscript (Script Compiler)

Poryscript compiles `.pory` script files (human-readable map/event scripts) into `.inc` assembly includes. It's distributed as a pre-built binary:

```bash
cd tools/
wget https://github.com/huderlem/poryscript/releases/download/3.5.2/poryscript-linux.zip
unzip poryscript-linux.zip -d poryscript/
rm poryscript-linux.zip
chmod +x poryscript/poryscript
```

### 5. Flips (Patch Creator)

`flips-linux` is included in the repo root. It creates the `.bps` patch by diffing the two ROMs.

---

## Build Steps

The build has four phases. Here's the overview:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Build host tools (gbagfx, codegen, poryscript, etc.)    │
│                         ↓                                   │
│  2. Build Elite Redux ROM (pokeemerald_modern.gba)          │
│                         ↓                                   │
│  3. Build vanilla Emerald ROM (pokeemerald.gba via agbcc)   │
│                         ↓                                   │
│  4. Create .bps patch (flips diffs the two ROMs)            │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Build Host Tools

```bash
make tools -j$(nproc)
```

This compiles everything under `tools/` (except `agbcc`, `poryscript`, and `pokeemerald`):

- **`gbagfx`** / **`rsfont`** — image/font converters (PNG → GBA tile format)
- **`mid2agb`** — MIDI → GBA sound converter
- **`aif2pcm`** — audio sample converter
- **`preproc`** — C preprocessor for assembly charmap handling
- **`scaninc`** — dependency scanner for include files
- **`ramscrgen`** — generates RAM linker scripts
- **`mapjson`** / **`jsonproc`** — map data processors
- **`gbafix`** — fixes GBA ROM headers (title, game code, checksum)
- **`codegen`** (Python) — protobuf → C header generator

> **Important:** Never clone `pokeemerald` into `tools/` before running `make tools` — the Makefile builds *all* subdirectories under `tools/`, and pokeemerald is not a host tool.

### Step 2: Build the Elite Redux ROM

```bash
make -j$(nproc)
```

This produces `pokeemerald_modern.gba` (32 MB). Despite the Makefile having a `MODERN` variable, the build system is configured so `make` and `make modern` are equivalent — both use the modern GCC toolchain (`arm-none-eabi-gcc`).

The build pipeline for each source file is:
1. **C preprocess** — expand `#include` and `#define` directives
2. **Preproc** — apply charmap substitutions (text encoding)
3. **Compile** — `arm-none-eabi-gcc` C/C++ → ARM assembly
4. **Assemble** — `arm-none-eabi-as` → object files
5. **Link** — `arm-none-eabi-ld` → ELF binary
6. **Objcopy** — ELF → raw GBA ROM
7. **Gbafix** — fix ROM header

### Step 3: Build the Vanilla Emerald ROM

The `.bps` patch needs a clean, unmodified Pokémon Emerald ROM as its base. This is built separately using **agbcc** — the original Game Freak-style compiler (different from the modern GCC toolchain).

```bash
# Clone pokeemerald (vanilla decompilation)
cd tools/
git clone https://github.com/pret/pokeemerald

# Build and install agbcc
git clone https://github.com/pret/agbcc
cd agbcc && ./build.sh && ./install.sh ../pokeemerald && cd ..

# Build vanilla Emerald ROM
cd pokeemerald && make -j$(nproc)
```

This produces `tools/pokeemerald/pokeemerald.gba` (16 MB).

> **Why agbcc?** The vanilla ROM must match the official Pokémon Emerald byte-for-byte. agbcc reproduces the exact behavior of the original compiler used by Game Freak. The modern toolchain (`arm-none-eabi-gcc`) optimizes differently and produces a non-matching ROM — which is fine for the hack, but not for the base.

### Step 4: Create the `.bps` Patch

```bash
./flips-linux --create tools/pokeemerald/pokeemerald.gba pokeemerald_modern.gba EliteRedux.bps
```

This diffs the 16 MB vanilla ROM against the 32 MB Elite Redux ROM and produces a `.bps` file containing only the changed bytes.

---

## Troubleshooting

### `cc1: all warnings being treated as errors` / `-Werror` failures

Newer versions of GCC introduce new warnings that the project doesn't suppress. To work around this, add `-Wno-error` to the CFLAGS in the Makefile (around line 124). This keeps warnings visible but prevents them from aborting the build.

### `json11.cpp: error: 'uint8_t' does not name a type`

Add `#include <cstdint>` to `tools/mapjson/json11.cpp` (and potentially `tools/pokeemerald/tools/mapjson/json11.cpp`). This is a GCC 15+ issue.

### `ModuleNotFoundError: No module named 'google.protobuf'`

Install the codegen runtime dependency:

```sh
python3 -m pip install -r tools/codegen/python/requirements.txt
```

### `make tools` fails trying to compile `tools/pokeemerald`

Remove `tools/pokeemerald/` before running `make tools`. Clone it only after the tools and ER ROM are built (see Step 3).

### `make clean` removed my tools

Use `make mostlyclean` instead. `make clean` also removes compiled host tools, forcing a full rebuild.

---

## CI Reference

The official build is defined in `.github/workflows/build.yml`. The steps above mirror that workflow exactly.
