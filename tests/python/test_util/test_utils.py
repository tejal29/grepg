from __future__ import print_function

from contextlib import contextmanager
import os
from textwrap import dedent
import unittest

from mock import patch
from twitter.common.contextutil import temporary_dir
import yaml

from util.utils import get_user_name, print_util

class UtilsTest(unittest.TestCase):

  @contextmanager
  def test_utils(self, content_str="", noFile=False):
    with temporary_dir() as dir:
      if not noFile:
        with open(os.path.join(dir, "grepg.yml"), 'w') as fp:
          fp.write(content_str)
      with patch('os.path.expanduser', return_value=dir) as mock_expand:
        yield (dir, mock_expand)

  def test_print_util_when_no_color(self):
    with patch('__builtin__.print') as mock_print:
      print_util("no color", 'blue', False)
      mock_print.assert_called_with("no color")

  def test_print_util_with_color(self):
    with patch('util.utils.cprint') as mock_cprint:
      print_util("color", 'blue', True)
      mock_cprint.assert_called_with("color", "blue")

  def test_get_user_name_from_opt(self):
    assert(get_user_name('foo') == "foo")

  def test_get_user_name_raise_err_when_no_user_name_no_config(self):
    with self.test_utils("", True) as (dir, mock_expand):
      with self.assertRaises(Exception) as e:
        get_user_name(None)
      self.assertEqual(e.exception.message, "Either username should be specified as --user on command line or in the {0}/grepg.yml".format(dir))

  def test_get_user_name_from_valid_config_when_no_username(self):
    with self.test_utils("'user': 'from_file'") as (_, mock_expand):
      self.assertEqual(get_user_name(None), "from_file")
      mock_expand.assert_called_once_with("~")

  def test_get_user_name_from_opt_when_valid_yaml(self):
    with self.test_utils("'user': 'from_file'") as (_, mock_expand):
      self.assertEqual(get_user_name("foo"), "foo")
      mock_expand.assert_not_called()

  def test_get_user_name_raise_err_when_invalid_yaml(self):
    with self.test_utils("'user': 'from_file"):
      with self.assertRaises(Exception) as e:
        get_user_name(None)

  def test_get_user_name_raise_err_when_no_user_attribute(self):
    with self.test_utils("'user1': 'from_file'"):
      with self.assertRaises(Exception) as e:
        get_user_name(None)