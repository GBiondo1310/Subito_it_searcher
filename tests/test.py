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
    from tests import functionality_test
except Exception:
    import functionality_test

suite = Suite(functionality_test)
