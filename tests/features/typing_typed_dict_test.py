import pytest

from pyupgrade._main import _fix_py36_plus


@pytest.mark.parametrize(
    's',
    (
        pytest.param(
            'from wat import TypedDict\n'
            'Q = TypedDict("Q")\n',
            id='from imported from elsewhere',
        ),
        pytest.param('D = typing.TypedDict("D")', id='no typed kwargs'),
        pytest.param('D = typing.TypedDict("D", {})', id='no typed args'),
        pytest.param('D = typing.TypedDict("D", {}, a=int)', id='both'),
        pytest.param('D = typing.TypedDict("D", 1)', id='not a dict'),
        pytest.param(
            'D = typing.TypedDict("D", {1: str})',
            id='key is not a string',
        ),
        pytest.param(
            'D = typing.TypedDict("D", {"a-b": str})',
            id='key is not an identifier',
        ),
        pytest.param(
            'D = typing.TypedDict("D", {"class": str})',
            id='key is a keyword',
        ),
        pytest.param(
            'D = typing.TypedDict("D", {**d, "a": str})',
            id='dictionary splat operator',
        ),
        pytest.param(
            'C = typing.TypedDict("C", *types)',
            id='starargs',
        ),
        pytest.param(
            'D = typing.TypedDict("D", **types)',
            id='starstarkwargs',
        ),
        pytest.param(
            'D = typing.TypedDict("D", x=int, total=False)',
            id='kw_typed_dict with total',
        ),
    ),
)
def test_typing_typed_dict_noop(s):
    assert _fix_py36_plus(s, min_version=(3, 6)) == s


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'from typing import TypedDict\n'
            'D = TypedDict("D", a=int)\n',

            'from typing import TypedDict\n'
            'class D(TypedDict):\n'
            '    a: int\n',

            id='keyword TypedDict from imported',
        ),
        pytest.param(
            'import typing\n'
            'D = typing.TypedDict("D", a=int)\n',

            'import typing\n'
            'class D(typing.TypedDict):\n'
            '    a: int\n',

            id='keyword TypedDict from attribute',
        ),
        pytest.param(
            'import typing\n'
            'D = typing.TypedDict("D", {"a": int})\n',

            'import typing\n'
            'class D(typing.TypedDict):\n'
            '    a: int\n',

            id='TypedDict from dict literal',
        ),
        pytest.param(
            'import typing\n'
            'D = typing.TypedDict("D", {"a": int}, total=False)\n',

            'import typing\n'
            'class D(typing.TypedDict, total=False):\n'
            '    a: int\n',

            id='TypedDict from dict literal with total',
        ),
        pytest.param(
            'from typing_extensions import TypedDict\n'
            'D = TypedDict("D", a=int)\n',

            'from typing_extensions import TypedDict\n'
            'class D(TypedDict):\n'
            '    a: int\n',

            id='keyword TypedDict from typing_extensions',
        ),
        pytest.param(
            'import typing_extensions\n'
            'D = typing_extensions.TypedDict("D", {"a": int})\n',

            'import typing_extensions\n'
            'class D(typing_extensions.TypedDict):\n'
            '    a: int\n',

            id='keyword TypedDict from typing_extensions',
        ),
        pytest.param(
            'import typing_extensions\n'
            'D = typing_extensions.TypedDict("D", {"a": int}, total=True)\n',

            'import typing_extensions\n'
            'class D(typing_extensions.TypedDict, total=True):\n'
            '    a: int\n',

            id='keyword TypedDict from typing_extensions, with total',
        ),
        pytest.param(
            'from typing import List\n'
            'from typing_extensions import TypedDict\n'
            'Foo = TypedDict("Foo", {"lsts": List[List[int]]})',

            'from typing import List\n'
            'from typing_extensions import TypedDict\n'
            'class Foo(TypedDict):\n'
            '    lsts: List[List[int]]',

            id='index unparse error',
        ),
        pytest.param(
            'import typing\n'
            'if True:\n'
            '    if False:\n'
            '        pass\n'
            '    D = typing.TypedDict("D", a=int)\n',

            'import typing\n'
            'if True:\n'
            '    if False:\n'
            '        pass\n'
            '    class D(typing.TypedDict):\n'
            '        a: int\n',

            id='right after a dedent',
        ),
    ),
)
def test_typing_typed_dict(s, expected):
    assert _fix_py36_plus(s, min_version=(3, 6)) == expected
