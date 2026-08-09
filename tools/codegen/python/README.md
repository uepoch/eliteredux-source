# Python code generator

This replaces the Kotlin/JVM generator with Python and the official Protobuf
runtime. Generated `*_pb2.py` bindings are committed, so normal builds do not
require protoc. The generator parses the repository's `.textproto` data and
emits the same generated C headers used by the ROM build.

Install the runtime dependency with:

```sh
python3 -m pip install -r tools/codegen/python/requirements.txt
```

The top-level build invokes it through `tools/codegen/makefile`. To generate one
file manually:

```sh
PYTHONPATH=tools/codegen/python:tools/codegen/python/generated \
  python3 -m codegen_py.main \
  abilities /tmp/abilities.h --proto-dir proto
```

Normal Make builds generate all outputs in one Python process so parsing and
domain lowering are shared:

```sh
PYTHONPATH=tools/codegen/python:tools/codegen/python/generated \
  python3 -m codegen_py.main --all . --proto-dir proto
```

Single-generator mode remains available for focused debugging. Any codegen or
protobuf input change causes the Makefile to regenerate the complete set.

## Parity check

`cmp.py` generates into temporary directories, runs astyle on both the Python
output and the checked-in Kotlin reference output, then compares every file:

```sh
python3 tools/codegen/python/cmp.py
python3 tools/codegen/python/cmp.py battlemoves evos --diff
python3 tools/codegen/python/cmp.py --raw
```

The normalized comparison requires `astyle`. Generation requires Python 3.10
or newer and the Python `protobuf` package.

## Protobuf bindings

Changing `.textproto` data does not require regenerating bindings. After
changing a `.proto` schema, regenerate and verify the committed `*_pb2.py` and
`*_pb2.pyi` files with:

```sh
make -C tools/codegen protos
make -C tools/codegen check-protos
```

Normal generation checks `generated/manifest.json` and reports stale schemas
without invoking protoc. Binding regeneration uses protoc 29.2.

Run parser and descriptor regression tests with:

```sh
make -C tools/codegen test
```

## Domain mapping

Domain values implement `FromProto[ProtoMessage]` and provide a concrete
`from_proto()` classmethod. This keeps field, enum, optional, and oneof lowering
next to the resulting dataclass while `GameData` handles file aggregation,
filtering, and indexes. Gameplay derivations remain explicit domain logic
rather than protobuf concerns.

## Writer design

`CWriter` owns multiline syntax and indentation through contexts such as
`array()`, `initializer()`, `function()`, `switch()`, and `block()`. Scalar
expression objects implement `CValue` (`CString`, `CGuiString`,
`CDollarString`, `CBraceList`, and related wrappers) and can be passed to
`field()` or `entry()`.

Domain dataclasses deliberately do not implement C rendering. This keeps data
loading independent from output layout while still preventing generators from
manually managing common C punctuation and indentation.
