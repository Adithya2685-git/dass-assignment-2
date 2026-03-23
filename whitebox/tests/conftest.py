"""Test configuration for the white-box MoneyPoly tests."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "code" / "moneypoly" / "moneypoly"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
