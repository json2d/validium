# validium
a Python utility library for performing validations flexibly

## Installation

```bash
pip install validium
```

## Quick Start

Here's an example of how to create and use some very simple validators for some numbers:

```py
import validium as V

PI = 3.14
ONE = 1

is_number = V.Validator(lambda x: isinstance(x, Number), 'must be a number')

is_number.validate(PI) # pass
is_number.validate(ONE) # pass

is_positive = V.Validator(lambda x: x > 0, 'must be positive')

is_positive.validate(PI) # pass
is_positive.validate(ONE) # pass

is_not_one = V.Validator(lambda x: not x == 1, 'must not equal 1')

is_not_one.validate(PI) # pass
is_not_one.validate(ONE) # AssertionError: must not equal 1

```

### Building Up

Here's an example of how to parameterize and reuse a common validator pattern:

```py
is_not = lambda y: V.Validator(lambda x: not x == y, 'must not equal {}'.format(x)) # u

is_not(-1).validate(ONE) # pass
is_not(0).validate(ONE) # pass
is_not(1).validate(ONE) # AssertionError: must not equal 1

```

This approach will help keep your code nice and DRY in the event you need handful of validators that behave mostly the same but slightly different.

### Confirmation only

As you can see `Validator.validate` raises for fails. If you just want the results of the validation use `Validator.confirm` which returns `True` if it passed or `False` if it failed:

```py
eq = lambda y: V.Validator(lambda x: x == y, 'must equal {}'.format(x)) # u
eq_42 = eq(42)

all_possible_answers = [
  1, 1, 1, 1, 1 ... 42 ... 1, 1, 1, 1, 1
]

for x in all_possible_answers
print('pass:' if eq_42.confirm(x) else 'fail:', eq_42.msg)

if eq_42.confirm(42):
  print('i think i found the answer')
else:
  print('need more time to find the answer')
```
