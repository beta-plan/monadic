#  Copyright (C) 2023 Plan-beta
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from functools import wraps
from typing import Callable, TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")


class LambdaFunction(Generic[T, U]):
    def __new__(cls, func: Callable[[T], U], *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(func)
        instance = wraps(func)(instance)
        return instance

    def __init__(self, func: Callable[..., U], *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, value: T) -> U:
        return self.func(value, *self.args, **self.kwargs)


def curry_func(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        lambda_func = LambdaFunction(func, *args, **kwargs)
        return lambda_func

    return wrapper
