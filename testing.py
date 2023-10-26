import os
from unittest import TestLoader, TextTestRunner


def run_tests():
    loader = TestLoader()
    runner = TextTestRunner()

    suite = loader.discover(
        start_dir=os.getcwd(),
        pattern='test_*.py'
    )

    runner.run(suite)


if __name__ == '__main__':
    run_tests()
