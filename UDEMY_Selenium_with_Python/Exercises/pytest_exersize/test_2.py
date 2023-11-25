import pytest


class TestSecondClass:

    @pytest.fixture
    def setup(self):
        print("Launching browser...") # will be executed before execution of the test
        print("Open application...")
        yield
        print("Closing browser...") # will be executed after execution of the tasts

    def test_login(self, setup):
        print("This is login test.")

    def test_logout(self, setup):
        print("This is logout test.")

    def test_search(self, setup):
        print("This is search test.")
