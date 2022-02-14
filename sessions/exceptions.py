#!/usr/bin/env python3

# *-- Exception (BUILT-IN)
#     |
#     *-- BethException
#     |   |
#     |   *-- DatabaseException
#     |   *-- ModuleException
#     |   |   |
#     |   |   *-- VerificationException
#     |   |   *-- UnreachableException
#     |   |
#     |   *-- WebhookException
#     |
#     *-- RuntimeError (BUILT-IN)
#     |   |
#     |   *-- BethError
#     |       |
#     |       *-- DatabaseError
#     |
#     *-- SessionException
#     *-- SituationException
#     |
#     *-- TypeError (BUILT-IN)
#     |   |
#     |   *-- BethTypeError
#     |
#     *-- Warning (BUILT-IN)
#         |
#         *-- RuntimeWarning (BUILT-IN)
#         |   |
#         |   *-- BethWarning
#         |       |
#         |       *-- DatabaseWarning
#         |       *-- ModuleWarning
#         |           |
#         |           *-- VerificationWarning
#         |           *-- UnreachableWarning
#         |
#         *-- SessionWarning
#         *-- SituationWarning

class BethException(Exception):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class ModuleException(BethException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class VerificationException(ModuleException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class EmailVerificationException(VerificationException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)
