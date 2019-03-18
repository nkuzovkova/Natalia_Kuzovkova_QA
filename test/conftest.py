import pytest
from auto_framework.src.general import Log

# Turning off logging in Selenium
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


@pytest.fixture(autouse=True)
def fx_sys_attach_logs(request):
    Log.info("=" * 80)
    Log.info("Test Case Function Name: " + request.function.__name__)
    Log.info("=" * 80)

    def fin():
        Log.log_stream.seek(0)

    request.addfinalizer(fin)