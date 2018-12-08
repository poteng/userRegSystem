import random
import unittest
from password_system import check_password_level, generate_password


class test_check_password_level(unittest.TestCase):
    """a unit test to test password_level() function with passwords with multiple scenarios
        all 4 complexities will be tested, with length longer than 8 or not"""

    """ That's not a good approach to use randomly generated data to do unit test, but since we have
    generate_password() function, we can use it as a support method to test. all 4 complexities will be tested 50
    times each, with length longer than 8 or not (400 tests in total) """

    def test_check_password_level_with_level_1(self):
        password = 'aaa'
        self.assertEqual(check_password_level(password), 1, "Test failed: " + password)
        print("Success: check_password_level() with complexity 1")

    def test_check_password_level_with_level_1_long(self):
        password = 'aaafewer'
        self.assertEqual(check_password_level(password), 2, "Test failed: " + password)
        print("Success: check_password_level() with complexity 1 (long)")

    def test_check_password_level_with_level_2(self):
        password = 'a01'
        self.assertEqual(check_password_level(password), 2, "Test failed: " + password)
        print("Success: check_password_level() with complexity 2")

    def test_check_password_level_with_level_2_long(self):
        password = '4848werr3789487fse532'
        self.assertEqual(check_password_level(password), 3, "Test failed: " + password)
        print("Success: check_password_level() with complexity 2 (long)")

    def test_check_password_level_with_level_3(self):
        password = 'a0B'
        self.assertEqual(check_password_level(password), 3, "Test failed: " + password)
        print("Success: check_password_level() with complexity 3")

    def test_check_password_level_with_level_3_long(self):
        password = 'err37a0B89487fse532'
        self.assertEqual(check_password_level(password), 3, "Test failed: " + password)
        print("Success: check_password_level() with complexity 3 (long)")

    def test_check_password_level_with_level_4(self):
        password = 'a0,B'
        self.assertEqual(check_password_level(password), 4, "Test failed: " + password)
        print("Success: check_password_level() with complexity 4")

    def test_check_password_level_with_level_4_long(self):
        password = 'a0,BkX-;'
        self.assertEqual(check_password_level(password), 4, "Test failed: " + password)
        print("Success: check_password_level() with complexity 4 (long)")

    def test_check_password_level_with_random_password(self):
        counter = 0
        for complex in range(1, 5):
            for i in range(50):
                counter += 1
                length = random.randrange(complex, 8)  # minimum length for a password is its complexty
                password = generate_password(length, complex)
                self.assertEqual(check_password_level(password), complex, "Test failed: " + password)
        print("Success: (random test) check_password_level() with complexity 1 ~ 4")
        print(counter, "random tests in total.")

        counter = 0
        for complex in range(1, 5):
            for i in range(50):
                counter += 1
                length = random.randrange(8, 30)  # minimum length is 8
                complex_long = complex + 1 if 1 <= complex <= 2 else complex
                password = generate_password(length, complex)
                self.assertEqual(check_password_level(password), complex_long, "Test failed: " + password)
        print("Success: (random test) check_password_level() with complexity 1 ~ 4 (long)")
        print(counter, "random tests in total.")


if __name__ == '__main__':
    unittest.main()
