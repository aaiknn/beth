#!/usr/bin/env python3

# *-- Exception (BUILT-IN)
#     |
#     *-- BethException
#     |   |
#     |   *-- DatabaseException
#     |   *-- ModuleException
#     |   |   |
#     |   |   *-- QueryException
#     |   |   *-- SubmissionException
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
#     |   |
#     |   *-- AuthorisationException
#     |   *-- NavigationException
#     |
#     *-- TypeError (BUILT-IN)
#     |   |
#     |   *-- BethTypeError
#     |
#     *-- Warning (BUILT-IN)
#         |
#         *-- RuntimeWarning (BUILT-IN)
#         *-- BethWarning
#         |   |
#         |   *-- DatabaseWarning
#         |   *-- ModuleWarning
#         |       |
#         |       *-- QueryWarning
#         |       |   |
#         |       |   *-- UnsuccessfulQueryWarning
#         |       |
#         |       *-- NoTargetWarning
#         |       *-- VerificationWarning
#         |       *-- UnreachableWarning
#         |
#         *-- SessionWarning
#         *-- SituationWarning

class BethException(Exception):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class SessionException(Exception):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class ModuleException(BethException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class SituationException(BethException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class AuthorisationException(SituationException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class NavigationException(SituationException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class UnreachableException(ModuleException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class QueryException(ModuleException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class SubmissionException(ModuleException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class VerificationException(ModuleException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class EmailVerificationException(VerificationException):
  def __init__(self, exceptionMessage=''):
    super().__init__(exceptionMessage)

class BethWarning(Warning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)

class SessionWarning(Warning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)

class ModuleWarning(BethWarning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)

class QueryWarning(ModuleWarning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)

class NoTargetWarning(ModuleWarning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)

class UnsuccessfulQueryWarning(QueryWarning):
  def __init__(self, warningMessage=''):
    super().__init__(warningMessage)
