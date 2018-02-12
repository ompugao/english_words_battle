#!/user/bin/python
import os
import sys
from src import main
import unittest


def test_remove_mentions():
    text = '@word_battle hello'
    assert ' hello' == main.remove_mentions(text)
