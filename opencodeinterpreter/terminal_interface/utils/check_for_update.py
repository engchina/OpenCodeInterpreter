try:
    from importlib import resources as pkg_resources
except ImportError:
    # Fallback for Python versions that don't have importlib.resources
    import pkg_resources
import requests
from packaging import version


def check_for_update():
    # 从PyPI API获取最新版本
    response = requests.get(f"https://pypi.org/pypi/open-interpreter/json")
    latest_version = response.json()["info"]["version"]

    # 使用pkg_resources获取当前版本
    current_version = pkg_resources.get_distribution("open-interpreter").version

    return version.parse(latest_version) > version.parse(current_version)
