import random
import linecache
from pathlib import Path
from typing import List


class SecretWord:
    def __init__(self, letters: int = 5):
        if letters < 5 or letters > 7:
            raise Exception("The argument must be in the range [5, 7]!")
        self.__letters = letters

    @property
    def letters(self) -> int:
        return self.__letters

    @letters.setter
    def letters(self, value):
        if value < 5 or value > 7:
            raise ValueError("The value must be in the range [5, 7]!")
        self.__letters = value

    def generate_word(self) -> List[str]:
        """
        Randomly selects a word of length <__letters> from the corresponding file.
        :return: list of characters of length <__letters>
        """
        # Get the directory of the current script
        current_dir = Path(__file__).parent
        file_name = f"words_{self.__letters}.txt"
        file_path = current_dir / file_name
        with open(file_path, 'r') as wf:
            wf_total_lines = sum(1 for _ in wf)
            random_line_index = random.randint(1, wf_total_lines)
            random_line = linecache.getline(str(file_path), random_line_index).strip()
        return list(random_line)


if __name__ == '__main__':
    sw5 = SecretWord()
    print(sw5.generate_word())
    sw6 = SecretWord(6)
    print(sw6.generate_word())
    sw7 = SecretWord(7)
    print(sw7.generate_word())
    # print(dir())
    # print(dir(sw5))
    # sw = SecretWord(12)
    # print(sw.generate_word())

