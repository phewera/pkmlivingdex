import logging
import os
from unittest import TestLoader, TextTestRunner


def run_tests():
    loader = TestLoader()
    runner = TextTestRunner(verbosity=2)
    suite = loader.discover(
        start_dir=os.getcwd(),
        pattern='test_*.py'
    )

    # disable logging while running tests
    logging.disable(logging.CRITICAL)
    result = runner.run(suite)
    logging.disable(logging.NOTSET)

    # set exit code for CI
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    run_tests()
