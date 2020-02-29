import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from numbers import Number

# from helpers import *

# from functools import reduce

import unittest
import ramda as R
import pandas as pd

import validium as V

# extensions for some missing ramda functions
R.isinstance = lambda x: lambda y: isinstance(y,x)

class TestEverything(unittest.TestCase):

  # use `_test` prefix isntead of `test` (w/o leading underscore) so test runner doesn't use it
  def _test_should_fail(self, fail_validators, foo):
    for validator in fail_validators:
      with self.assertRaises(AssertionError):
        validator.validate(foo)

  def _test_should_pass(self, pass_validators, foo):
    try:
      for validator in pass_validators:
        validator.validate(foo)
    except:
      self.fail('validation should have passed but exception was raised')

  def test_base(self):

    foo = 3.14
    
    pass_validators = [
      V.Validator(
        lambda x: isinstance(x, Number), 
        'must be a number'
      ),

      V.Validator(
        lambda x: isinstance(x, float), 
        'must be a float'
      ),

      V.Validator(
        lambda x: x > 0 and x < 100, 
        'must be greater than 0 and less than 100'
      ),

      V.Validator(
        lambda x: x == 3.14, 
        'must equal 3.14'
      ),
    ]

    self._test_should_pass(pass_validators, foo)

    fail_validators = [

      V.Validator(
        R.isinstance(str),
        'must be a string'
      ),

      V.Validator(R.equals(42), 'must equal 42'),

      V.Validator(
        lambda x: x < 0, 
        'must be less than 0',
      )
    ]

    self._test_should_fail(fail_validators, foo)

  def test_list(self):

    class Mystery:
      pass

    bars = [1, 2, .14, None, 'hello', 'world']
    
    pass_validators = [
      V.Validator(
        lambda xs: isinstance(xs, list), 
        'must be a list'
      ),

      V.Validator(
        lambda xs: len(xs) == 6, 
        'must be of length 6'
      ),

      V.Validator(
        lambda xs: all([not isinstance(x, Mystery) for x in xs]),  
        'all must not be Mystery'
      ),

      V.Validator(
        lambda xs: all([x > 0 for x in filter(lambda x: isinstance(x, Number), xs)]), 
        'all numbers must be greater than 0'
      ),

      V.Validator(
        lambda xs: ' '.join(filter(lambda x: isinstance(x, str), xs)) == 'hello world', 
        'all strings joined with a space must equal "hello world"'
      ),

      V.Validator(
        R.any(R.equals('hello')), 
        'any must equal "hello"'
      ),

      V.Validator(
        R.all(R.isinstance((Number, type(None), str))), 
        'all must be number, None or str'
      ),

      V.Validator(
        R.pipe(R.filter(R.isinstance(Number)), R.sum, R.equals(3.14)),
        'all numbers summed must equal 3.14'
      ),
      
      V.Validator(
        R.pipe(R.filter(R.isinstance(str)), R.length, R.equals(2)),
        'the count of str must be 2'
      ),
    ]

    self._test_should_pass(pass_validators, bars)

    fail_validators = [
      V.Validator(
        R.all(R.pipe(R.isinstance(type(None)), R.negate)),
        'all must not be None'
      ),
      
      V.Validator(
        R.any(R.isinstance(dict)),
        'any must be dict'
      ),

      V.Validator(
        R.pipe(R.filter(R.isinstance(Number)), R.sum, R.equals(42)),
        'all numbers summed must equal 42'
      ),

      V.Validator(
        R.pipe(R.filter(R.isinstance(str)), R.length, R.equals(4)),
        'the count of str must be 4'
      ),

    ]

    self._test_should_fail(fail_validators, bars)

unittest.main()