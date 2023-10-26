import os
from unittest import TestLoader, TextTestRunner


def run_tests():
    loader = TestLoader()
    runner = TextTestRunner()

    suite = loader.discover(
        start_dir=os.getcwd(),
        pattern='test_*.py'
    )

    result = runner.run(suite)

    # set exit code for CI
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    run_tests()
