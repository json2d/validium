import logging

logger = logging.getLogger('validium')
LOGGER_TAG = '💎'

class Validator:

  def __init__(self, predicate, msg=None):

    assert callable(predicate), "the argument 'predicate' must be callable"
    assert msg is None or isinstance(msg, str), "the argument 'msg' must be None or an instance of str"

    self.__dict__ = dict(
      predicate=predicate,
      msg=msg,
    )

  def validate(self, target, tag=None):
    assert self.confirm(target, tag), self.msg

  def confirm(self, target, tag=None):
    result = self.predicate(target)
    logger.info(f"[{ LOGGER_TAG + ':' + repr(tag) if tag is not None else LOGGER_TAG}] - {'✅ pass' if result else '❌ fail'}: {self.msg}")
    
    return result