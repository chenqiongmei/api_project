import pytest

from common.operyaml import ReadYamlData


@pytest.fixture(scope='session', autouse=True)
def clear_data():
    ReadYamlData().clear_extract_yaml()
