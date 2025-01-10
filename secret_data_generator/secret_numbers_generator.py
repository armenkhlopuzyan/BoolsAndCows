import random
from typing import List

class SecretNumbers:
    def __init__(self, digits: int = 4):
        if digits < 1 or digits > 9:
            raise Exception("The argument must be in the range [1, 9]!")
        self.__digits = digits

    @property
    def digits(self):
        return self.__digits

    @digits.setter
    def digits(self, value):
        if value < 1 or value > 9:
            raise ValueError("The the value must be in the range [1, 9]!")
        self.__digits = value

    def generate_numbers(self) -> List[str]:
        """
        Generates non-repeating single-digit numbers where the first digit is not 0, with a total count of <__digits>.
        :return: a list of unique characters from the set ('0', '1', ..., '9'), where the first element is not equal to '0'. .
        """
        secret_nums = random.sample(range(0,10), self.__digits)
        if secret_nums[0] == 0:
            if self.__digits == 1:
                secret_nums[0] = random.randint(1, 9)
            else:
                secret_nums[0], secret_nums[1] = secret_nums[1], secret_nums[0]
        return list(map(str, secret_nums))


if __name__ == '__main__':
    sn1= SecretNumbers(1)
    print(sn1.generate_numbers())
    sn5 = SecretNumbers()
    print(sn5.generate_numbers())
    sn7 = SecretNumbers(7)
    print(sn7.generate_numbers())
    #sn = SecretNumbers(-4)
    #print(sn.generate_numbers())
