# coding=utf-8

# Copyright (C) 2013-2015 David R. MacIver (david@drmaciver.com)

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# END HEADER

from __future__ import division, print_function, absolute_import, \
    unicode_literals


import sys
from collections import namedtuple

import pytest

from hypothesis.settings import Settings
from hypothesis.internal.debug import timeout
from hypothesis.strategytests import templates_for
from tests.common.basic import Bitfields
from hypothesis.strategies import integers, floats, just, one_of, \
    sampled_from, streaming, basic, lists, booleans, dictionaries, tuples, \
    frozensets, complexes, sets, text, binary, decimals, fractions, none, \
    randoms
from hypothesis.internal.compat import hrange
from hypothesis.searchstrategy.narytree import n_ary_tree
from hypothesis.utils.show import show


settings = Settings(max_examples=100, timeout=4)

__all__ = ['small_verifier', 'timeout', 'standard_types', 'OrderedPair']


OrderedPair = namedtuple('OrderedPair', ('left', 'right'))


ordered_pair = integers().flatmap(
    lambda right: integers(min_value=0).map(
        lambda length: OrderedPair(right - length, right)))


def constant_list(strat):
    return strat.flatmap(
        lambda v: lists(just(v)),
    )


EvalledIntStream = streaming(integers()).map(lambda x: list(x[:10]) and x)

ABC = namedtuple('ABC', ('a', 'b', 'c'))


def abc(x, y, z):
    return tuples(x, y, z, tuple_class=ABC)

with Settings(average_list_length=10.0):
    standard_types = [
        basic(Bitfields),
        EvalledIntStream,
        lists(max_size=0), tuples(), sets(max_size=0), frozensets(max_size=0),
        dictionaries(),
        n_ary_tree(booleans(), booleans(), booleans()),
        n_ary_tree(integers(), integers(), integers()),
        abc(booleans(), booleans(), booleans()),
        abc(booleans(), booleans(), integers()),
        templates_for(one_of(*map(just, hrange(10)))),
        dictionaries({'a': integers(), 'b': booleans()}),
        one_of(integers(), tuples(booleans())),
        sampled_from(range(10)),
        one_of(just('a'), just('b'), just('c')),
        sampled_from(('a', 'b', 'c')),
        integers(),
        integers(min_value=3),
        integers(min_value=(-2 ** 32), max_value=(2 ** 64)),
        floats(), floats(min_value=-2.0, max_value=3.0),
        floats(min_value=3.14, max_value=3.14),
        text(), binary(),
        booleans(),
        tuples(booleans(), booleans()),
        frozensets(integers()),
        complexes(),
        fractions(),
        decimals(),
        lists(lists(booleans())),
        ordered_pair, constant_list(integers()),
        streaming(integers()).map(lambda x: list(x[:2]) and x),
        integers().filter(lambda x: abs(x) > 100),
        floats(min_value=-sys.float_info.max, max_value=sys.float_info.max),
        none(), randoms(),
        tuples().flatmap(lambda x: EvalledIntStream),
        templates_for(integers(min_value=0, max_value=0).flatmap(
            lambda x: integers(min_value=0, max_value=0))),
    ]


def parametrize(args, values):
    return pytest.mark.parametrize(args, values, ids=list(map(show, values)))
