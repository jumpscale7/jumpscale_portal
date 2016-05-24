from JumpScale.portal.portal import exceptions
import re

INT = r"""(?:[+-]?(?:[0-9]+))"""
BASE10NUM = r"""(?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))"""
NUMBER = r"""(?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))"""
BASE16NUM = r"""(?<![0-9A-Fa-f])(?:[+-]?(?:0x)?(?:[0-9A-Fa-f]+))"""
BASE16FLOAT = r"""\b(?<![0-9A-Fa-f.])(?:[+-]?(?:0x)?(?:(?:[0-9A-Fa-f]+(?:\.[0-9A-Fa-f]*)?)|(?:\.[0-9A-Fa-f]+)))\b"""

POSINT = r"""\b(?:[1-9][0-9]*)\b"""
NONNEGINT = r"""\b(?:[0-9]+)\b"""
WORD = r"""\b\w+\b"""
NOTSPACE = r"""\S+"""
SPACE = r"""\s*"""
DATA = r""".*?"""
GREEDYDATA = r""".*"""
QUOTEDSTRING = r"""(?>(?<!\\)(?>"(?>\\.|[^\\"]+)+"|""|(?>'(?>\\.|[^\\']+)+')|''|(?>`(?>\\.|[^\\`]+)+`)|``))"""
UUID = r"""[A-Fa-f0-9]{8}-(?:[A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}"""

def NAME(val):
    return all(i not in val for i in r"""<>"'""") and len(val) >= 2

def IP(val):
    return sum([x.isdigit() and 0 <= int(x) <= 255 for x in val.split('.')]) == 4

def PASSWORD(val):
    return len(val) > 6

def USERNAME(val):
    m = re.match("[a-zA-Z0-9._-]+(?:@[a-zA-Z0-9._-]+)?", val)
    if 2 < len(val.split('@')[0]) < 40 and m and m.end() == len(val):
        return True
    else:
        raise exceptions.BadRequest('Usernames can only contain alphanumeric characeters, dots, dashes, underscores and should be between 2 and 40 characters')

def GROUPNAME(val):
    m = re.match("[a-zA-Z0-9._-]+", val)
    if 2 < len(val) < 40 m and m.end() == len(val):
        return True
    else:
        raise exceptions.BadRequest('Groupnames can only contain alphanumeric characeters, dots, dashes, underscores and should be between 2 and 40 characters')