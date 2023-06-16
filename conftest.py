import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="default", help="environment config file"
        # environment: like int, test or production
    )
