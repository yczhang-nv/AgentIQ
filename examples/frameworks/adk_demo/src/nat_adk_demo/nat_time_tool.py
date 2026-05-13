# SPDX-FileCopyrightText: Copyright (c) 2025-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

import datetime
from collections.abc import AsyncIterator
from zoneinfo import ZoneInfo

from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig

CITY_TIMEZONES = {
    "london": ("London", "Europe/London"),
    "new york": ("New York", "America/New_York"),
    "tokyo": ("Tokyo", "Asia/Tokyo"),
}

CITY_ALIASES = {
    "london, england": "london",
    "london, uk": "london",
    "london, united kingdom": "london",
    "new york city": "new york",
    "new york, ny": "new york",
    "new york, usa": "new york",
    "new york, united states": "new york",
    "nyc": "new york",
    "tokyo, japan": "tokyo",
}


def _normalize_city(city: str) -> str:
    """Normalize city names and common qualified variants."""
    normalized_city = " ".join(city.strip().casefold().split())
    return CITY_ALIASES.get(normalized_city, normalized_city)


class TimeMCPToolConfig(FunctionBaseConfig, name="get_city_time_tool"):
    """Configuration for the get_city_time tool."""


@register_function(config_type=TimeMCPToolConfig, framework_wrappers=[LLMFrameworkEnum.ADK])
async def get_city_time(_config: TimeMCPToolConfig, _builder: Builder) -> AsyncIterator[FunctionInfo]:
    """
    Register a get_city_time(city: str) -> str tool for ADK.

    Args:
        _config (TimeMCPToolConfig): The configuration for the get_city_time tool.
        _builder (Builder): The NAT builder instance.
    """

    async def _get_city_time(city: str) -> str:
        """
        Get the time in a specified city.

        Args:
            city (str): The name of the city.

        Returns:
            str: The current time in the specified city or an error message if the city is not recognized.
        """

        city_timezone = CITY_TIMEZONES.get(_normalize_city(city))
        if city_timezone is None:
            return f"Sorry, I don't have timezone information for {city}."

        canonical_city, timezone_name = city_timezone
        now = datetime.datetime.now(ZoneInfo(timezone_name))
        local_time = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        return f"The current time in {canonical_city} is {local_time}"

    yield FunctionInfo.from_fn(_get_city_time, description=_get_city_time.__doc__)
