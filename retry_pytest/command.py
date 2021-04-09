#     retry_pytest is a library for pytest test framework
#     Copyright (C) 2021  Alexander Evdokimov
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable


class ResultHandler(ABC):
    @abstractmethod
    def set_next(self, handler: ResultHandler) -> ResultHandler:
        pass

    @abstractmethod
    def handle(self, result, cmd):
        pass


class BaseHandler(ResultHandler):
    def __init__(self):
        self._next = None

    def set_next(self, handler: ResultHandler) -> ResultHandler:
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, result, item):
        if self._next:
            return self._next.handle(result, item)


class CallableHandler(BaseHandler):
    def handle(self, result, item):
        if callable(item):
            return item(result)
        return super().handle(result, item)


class ListHandler(BaseHandler):
    def handle(self, result, item):
        if isinstance(result, (list, tuple)):
            return result[int(item)]
        return super().handle(result, item)


class DictHandler(BaseHandler):
    def handle(self, result, item):
        if isinstance(result, dict):
            return result.get(item)
        return super().handle(result, item)


class ObjectHandler(BaseHandler):
    def handle(self, result, item):
        attr = getattr(result, item)
        if isinstance(attr, property):
            return attr
        if callable(attr):
            return attr()
        return attr


class Command:
    def __init__(self, func: Callable, *args, **kwargs):
        self._condition = lambda: False
        self._result_value = None
        self._result_history = []
        self._command = func
        self._args = args
        self._kwargs = kwargs
        self._actions = []
        handler = self._action_handler = CallableHandler()
        for h in [ListHandler(), DictHandler(), ObjectHandler()]:
            handler = handler.set_next(h)

    @property
    def history(self):
        return self._result_history

    @property
    def result(self):
        self._result_history.clear()
        self._result_history.append(self._result_value)
        if self._actions:
            for item in self._actions:
                self._result_history.append(
                    self._action_handler.handle(self._result_history[-1], item)
                )
        return self._result_history[-1]

    def less(self, other):
        self._condition = lambda: self.result < other

    def less_equal(self, other):
        self._condition = lambda: self.result <= other

    def equal(self, other):
        self._condition = lambda: self.result == other

    def not_equal(self, other):
        self._condition = lambda: self.result != other

    def greater(self, other):
        self._condition = lambda: self.result > other

    def greater_equal(self, other):
        self._condition = lambda: self.result >= other

    def len(self):
        self._actions.append(len)
        return self

    def is_(self, other):
        self._condition = lambda: self.result is other

    def is_not(self, other):
        self._condition = lambda: self.result is not other

    def in_(self, other):
        self._condition = lambda: self.result in other

    def not_in(self, other):
        self._condition = lambda: self.result not in other

    def get(self, attribute_name=None):
        self._actions.append(attribute_name)
        return self

    def __call__(self, *args, **kwargs):
        self._result_value = self._command(*self._args, **self._kwargs)
        return self._condition()
