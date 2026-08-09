from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HelpMenuColors(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DARK: _ClassVar[HelpMenuColors]
    BLUE: _ClassVar[HelpMenuColors]
    RED: _ClassVar[HelpMenuColors]
    YELLOW: _ClassVar[HelpMenuColors]
    GREEN: _ClassVar[HelpMenuColors]
DARK: HelpMenuColors
BLUE: HelpMenuColors
RED: HelpMenuColors
YELLOW: HelpMenuColors
GREEN: HelpMenuColors

class HelpArticles(_message.Message):
    __slots__ = ("help_category",)
    class HelpCategory(_message.Message):
        __slots__ = ("title", "color", "help_article")
        class HelpArticle(_message.Message):
            __slots__ = ("title", "page")
            TITLE_FIELD_NUMBER: _ClassVar[int]
            PAGE_FIELD_NUMBER: _ClassVar[int]
            title: str
            page: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, title: _Optional[str] = ..., page: _Optional[_Iterable[str]] = ...) -> None: ...
        TITLE_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        HELP_ARTICLE_FIELD_NUMBER: _ClassVar[int]
        title: str
        color: HelpMenuColors
        help_article: _containers.RepeatedCompositeFieldContainer[HelpArticles.HelpCategory.HelpArticle]
        def __init__(self, title: _Optional[str] = ..., color: _Optional[_Union[HelpMenuColors, str]] = ..., help_article: _Optional[_Iterable[_Union[HelpArticles.HelpCategory.HelpArticle, _Mapping]]] = ...) -> None: ...
    HELP_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    help_category: _containers.RepeatedCompositeFieldContainer[HelpArticles.HelpCategory]
    def __init__(self, help_category: _Optional[_Iterable[_Union[HelpArticles.HelpCategory, _Mapping]]] = ...) -> None: ...
