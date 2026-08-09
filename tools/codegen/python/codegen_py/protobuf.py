"""Official protobuf parsing and descriptor helpers."""

from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

from google.protobuf import text_format
from google.protobuf.descriptor import EnumDescriptor, FieldDescriptor
from google.protobuf.message import Message


PYTHON_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PYTHON_DIR / "generated"
T = TypeVar("T", bound=Message)
P = TypeVar("P", bound=Message)


class FromProto(ABC, Generic[P]):
    """A domain value that can lower one generated protobuf message."""

    __slots__ = ()

    @classmethod
    @abstractmethod
    def from_proto(cls, proto: P):
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class EnumValue:
    name: str
    number: int


def check_schema_manifest(proto_dir: Path) -> None:
    manifest_path = GENERATED_DIR / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("Missing generated protobuf manifest; run: make -C tools/codegen protos")
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))["schemas"]
    actual = {
        path.relative_to(proto_dir).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(proto_dir.rglob("*.proto"))
    }
    if actual != expected:
        raise RuntimeError("Protobuf schemas changed; run: make -C tools/codegen protos")


def parse_textproto(path: Path, message_type: type[T]) -> T:
    message = message_type()
    try:
        text_format.Parse(path.read_text(encoding="utf-8"), message)
    except text_format.ParseError as error:
        raise ValueError(f"{path}: {error}") from error
    return message


def enum_name(message: Message, field_name: str) -> str:
    field = message.DESCRIPTOR.fields_by_name[field_name]
    return enum_value_name(field, getattr(message, field_name))


def enum_value_name(field: FieldDescriptor, value: int) -> str:
    if field.enum_type is None:
        raise TypeError(f"{field.full_name} is not an enum field")
    return field.enum_type.values_by_number[value].name


def repeated_enum_names(message: Message, field_name: str) -> list[str]:
    field = message.DESCRIPTOR.fields_by_name[field_name]
    return [enum_value_name(field, value) for value in getattr(message, field_name)]


def enum_values(descriptor: EnumDescriptor, *, exclude: set[str] = frozenset()) -> list[EnumValue]:
    return [EnumValue(value.name, value.number) for value in descriptor.values if value.name not in exclude]
