import sys
from pathlib import Path

from project_setup_helper.config import ProjectConfig, normalize_project_name, package_name_from_project_name


def test_project_name_normalization():
    assert normalize_project_name("Weather CLI!") == "weather-cli"


def test_package_name_from_project_name():
    assert package_name_from_project_name("weather-cli") == "weather_cli"


def test_project_config_helpers():
    config = ProjectConfig(
        project_type="pyproject",
        project_name="weather-cli",
        package_name="weather_cli",
        project_root=Path("weather-cli"),
        include_dev_tools=True,
        minimum_python_version="3.11",
        python_interpreter=Path(sys.executable),
    )
    assert config.uses_pyproject
    assert not config.uses_requirements
