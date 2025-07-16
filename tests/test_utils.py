import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import compute_aqi, SO2_BREAKPOINTS, CO_BREAKPOINTS


def test_compute_aqi_so2():
    # 10 ppb should fall in first SO2 breakpoint (0-35 -> 0-50 AQI)
    expected = round((50 - 0) / (35 - 0) * (10 - 0) + 0)
    assert compute_aqi(10, SO2_BREAKPOINTS) == expected


def test_compute_aqi_co():
    # 5 ppm should fall in second CO breakpoint (4.5-9.4 -> 51-100 AQI)
    expected = round((100 - 51) / (9.4 - 4.5) * (5 - 4.5) + 51)
    assert compute_aqi(5, CO_BREAKPOINTS) == expected
