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
"""Weather update tool file."""

from collections.abc import AsyncIterator

from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig


WEATHER_BY_CITY = {
    "london": ("London",
               "The weather in London is partly cloudy with a temperature of 18 degrees Celsius "
               "(64 degrees Fahrenheit)."),
    "new york": ("New York",
                 "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."),
    "tokyo": ("Tokyo",
              "The weather in Tokyo is clear with a temperature of 22 degrees Celsius (72 degrees Fahrenheit)."),
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


class WeatherToolConfig(FunctionBaseConfig, name="weather_update"):
    pass


@register_function(config_type=WeatherToolConfig, framework_wrappers=[LLMFrameworkEnum.ADK])
async def weather_update(_config: WeatherToolConfig, _builder: Builder) -> AsyncIterator[FunctionInfo]:

    async def _weather_update(city: str) -> str:
        """
        Get the current weather for a specified city.

        Args:
            city (str): The name of the city.

        Returns:
            str: The current weather for the specified city.
        """
        city_weather = WEATHER_BY_CITY.get(_normalize_city(city))
        if city_weather is not None:
            _, weather = city_weather
            return weather

        return f"Weather information for '{city}' is not available."

    yield FunctionInfo.from_fn(_weather_update, description=_weather_update.__doc__)
