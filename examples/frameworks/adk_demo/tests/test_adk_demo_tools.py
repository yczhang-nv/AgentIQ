# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import cast

import pytest

from nat.builder.builder import Builder
from nat_adk_demo.nat_time_tool import TimeMCPToolConfig
from nat_adk_demo.nat_time_tool import get_city_time
from nat_adk_demo.weather_update_tool import WeatherToolConfig
from nat_adk_demo.weather_update_tool import weather_update

BUILDER = cast(Builder, None)


@pytest.mark.parametrize(
    ("city", "expected_city"),
    [
        ("London", "London"),
        ("Tokyo, Japan", "Tokyo"),
        ("New York", "New York"),
    ],
)
async def test_weather_update_supports_demo_cities(city: str, expected_city: str):
    async with weather_update(WeatherToolConfig(), BUILDER) as tool_info:
        assert tool_info.single_fn is not None

        result = await tool_info.single_fn(city)

    assert expected_city in result
    assert "not available" not in result


@pytest.mark.parametrize(
    ("city", "expected_city", "expected_timezone"),
    [
        ("London", "London", ("GMT", "BST")),
        ("Tokyo, Japan", "Tokyo", ("JST",)),
        ("New York", "New York", ("EST", "EDT")),
    ],
)
async def test_get_city_time_supports_demo_cities(city: str,
                                                 expected_city: str,
                                                 expected_timezone: tuple[str, ...]):
    async with get_city_time(TimeMCPToolConfig(), BUILDER) as tool_info:
        assert tool_info.single_fn is not None

        result = await tool_info.single_fn(city)

    assert f"The current time in {expected_city}" in result
    assert any(timezone in result for timezone in expected_timezone)
    assert "don't have timezone information" not in result
