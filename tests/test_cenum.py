import pytest
import cstruct
from cstruct import CEnum
from enum import Enum


class Dummy(CEnum):
    __enum__ = """
        #define SOME_DEFINE 7

        A,
        B,
        C = 2,
        D = 5 + SOME_DEFINE,
        E = 2
      """


class HtmlFont(CEnum):
    __size__ = 2
    __def__ = """
        #define NONE         0

        enum htmlfont {
            HTMLFONT_NONE = NONE,
            HTMLFONT_BOLD,
            HTMLFONT_ITALIC,
        };
    """


class StructWithEnum(cstruct.MemCStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __def__ = """
        struct StructWithEnum {
            enum HtmlFont font;
            unsigned int font_size;
        }
    """


def test_dummy():
    assert Dummy.A == 0
    assert Dummy.B == 1
    assert Dummy.C == 2
    assert Dummy.D == 12
    assert Dummy.E == 2


def test_missing_attribute():
    with pytest.raises(AttributeError):
        assert Dummy.F


def test_set_attribute():
    with pytest.raises(AttributeError):
        Dummy.A = 100


def test_html_font():
    assert HtmlFont.HTMLFONT_NONE == 0
    assert HtmlFont.HTMLFONT_BOLD == 1
    assert HtmlFont.HTMLFONT_ITALIC == 2


def test_parse_enum():
    reply_stat = cstruct.parse("enum reply_stat { MSG_ACCEPTED=0, MSG_DENIED=1 }")
    assert isinstance(reply_stat.MSG_ACCEPTED, Enum)
    assert isinstance(reply_stat.MSG_DENIED, Enum)
    assert reply_stat.MSG_ACCEPTED == 0
    assert reply_stat.MSG_DENIED == 1


def test_struct_with_enum():
    s = StructWithEnum()
    s.font = HtmlFont.HTMLFONT_BOLD
    s.font_size = 11
    assert s.font == HtmlFont.HTMLFONT_BOLD
    assert s.font_size == 11

    s.font = HtmlFont.HTMLFONT_NONE
    s.font_size = 20
    assert s.font == HtmlFont.HTMLFONT_NONE
    assert s.font_size == 20
    packed = s.pack()

    s1 = StructWithEnum()
    s1.unpack(packed)
    assert s1.font == HtmlFont.HTMLFONT_NONE
    assert s1.font_size == 20
