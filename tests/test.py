# ===== EXAMPLE ===== #

# try:
#     from tests import test_example1, test_example2
# except Exception:
#     import test_example1
#     import test_example2

# suite = Suite(test_example1, test_example2)

# ===== EXAMPLE ===== #

from test_suite.suite import Suite

try:
    from tests import test_functionality, test_advertisement_class, test_searcher_class
except Exception:
    import tests.test_functionality as test_functionality
    import tests.test_advertisement_class as test_advertisement_class
    import tests.test_searcher_class as test_searcher_class

suite = Suite(test_functionality, test_advertisement_class, test_searcher_class)


if __name__ == "__main__":
    suite.ask_tests()
    suite.run()
