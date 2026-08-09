from __future__ import annotations

import importlib
import re
import sys
import unittest
from pathlib import Path


PYTHON_DIR = Path(__file__).resolve().parents[1]
ROOT = PYTHON_DIR.parents[2]
sys.path[:0] = [str(PYTHON_DIR), str(PYTHON_DIR / "generated")]

from google.protobuf import descriptor_pool, message_factory, text_format

import MoveList_pb2
from codegen_py.protobuf import check_schema_manifest


class ProtobufTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path in sorted((PYTHON_DIR / "generated").glob("*_pb2.py")):
            importlib.import_module(path.stem)

    def test_all_repository_textprotos_parse(self):
        pool = descriptor_pool.Default()
        for path in sorted((ROOT / "proto").rglob("*.textproto")):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^# proto-message:\s*(\S+)", text, re.MULTILINE)
            self.assertIsNotNone(match, path)
            descriptor = pool.FindMessageTypeByName(match.group(1))
            text_format.Parse(text, message_factory.GetMessageClass(descriptor)())

    def test_schema_manifest_is_current(self):
        check_schema_manifest(ROOT / "proto")

    def test_move_flag_options_are_registered(self):
        fields = []
        for field in MoveList_pb2.Move.DESCRIPTOR.fields:
            options = field.GetOptions()
            if options.HasExtension(MoveList_pb2.is_flag) and options.Extensions[MoveList_pb2.is_flag]:
                fields.append(field.name)
        self.assertEqual(45, len(fields))
        self.assertEqual(["contact", "crit", "ignores_protect"], fields[:3])
        self.assertEqual(["sleep_talk_banned", "mimic_banned"], fields[-2:])

        high = MoveList_pb2.Crit.DESCRIPTOR.values_by_name["HIGH"]
        self.assertEqual(
            "FLAG_HIGH_CRIT",
            high.GetOptions().Extensions[MoveList_pb2.enum_flag_code_value],
        )

    def test_optional_and_oneof_presence(self):
        root = MoveList_pb2.MoveList()
        text_format.Parse('moves { split: PHYSICAL argument { int: 0 } }', root)
        move = root.moves[0]
        self.assertTrue(move.HasField("split"))
        self.assertEqual("int", move.argument.WhichOneof("argument"))
        self.assertEqual(0, move.argument.int)

    def test_invalid_textproto_is_rejected(self):
        invalid = [
            'moves { unknown_field: 1 }',
            'moves { split: NOT_A_SPLIT }',
            'moves { name: "first" name: "second" }',
            'moves { argument { int: 1 other: "two" } }',
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(text_format.ParseError):
                text_format.Parse(text, MoveList_pb2.MoveList())


if __name__ == "__main__":
    unittest.main()
