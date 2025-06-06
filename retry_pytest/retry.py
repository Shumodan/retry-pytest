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


from math import ceil
from time import sleep
from typing import Callable, List

import allure
from allure_commons import plugin_manager
from allure_commons.utils import uuid4

from retry_pytest.command import Command
from retry_pytest.custom_errors import NegativeAction, RetryTimeout


class Retry:

    def __init__(
        self, *expected_exceptions,
        timeout=10,
        poll_frequency=1,
        title='Retry',
        error_msg='',
        show_expected=False,
        assertion_error_on_timeout=True,
        **kwargs
    ):
        self._exceptions = expected_exceptions if expected_exceptions else (NegativeAction,)
        self._timeout = timeout
        error_msg = error_msg if error_msg else f'timeout {timeout}s exceeded'
        self._timeout_msg = f'{title}: {error_msg}'
        self._poll_frequency = poll_frequency
        self._command_queue = []
        self._title = title
        self._step_params = kwargs
        self._current_step = None
        self._show_expected = show_expected
        self._timeout_command = None
        self._timeout_exception = AssertionError if assertion_error_on_timeout else RetryTimeout
        self._above_exception = None

    @property
    def commands(self) -> List[Command]:
        return self._command_queue

    @property
    def last_command(self) -> Command:
        return self._command_queue[-1]

    def __enter__(self):
        self._current_step = uuid4()
        plugin_manager.hook.start_step(uuid=self._current_step, title=self._title, params=self._step_params)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            for i in range(ceil(self._timeout / self._poll_frequency)):
                try:
                    if i > 0:
                        sleep(self._poll_frequency)
                    if all([f() for f in self._command_queue]):
                        break
                except self._exceptions as e:
                    self._above_exception = e
                    if self._show_expected:
                        allure.attach(
                            f'{e.__class__.__name__}: {str(e)}', 'Expected exception', allure.attachment_type.TEXT
                        )
            else:
                exc_type = self._timeout_exception
                exc_val = exc_type(self._timeout_msg)
                exc_tb = None
                if callable(self._timeout_command):
                    self._timeout_command()
        except Exception as e:
            exc_type = e.__class__
            exc_val = e
            exc_tb = None
        plugin_manager.hook.stop_step(
            uuid=self._current_step,
            title=self._title,
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb
        )
        if exc_val:
            if not self._above_exception:
                raise exc_val
            try:
                raise self._above_exception
            except Exception as e:
                raise exc_val from e

    def check(self, func: Callable, *args, **kwargs) -> Command:
        self._command_queue.append(Command(func, *args, **kwargs))
        return self._command_queue[-1]

    def on_timeout(self, func: Callable, *args, **kwargs) -> None:
        self._timeout_command = lambda: func(*args, **kwargs)
