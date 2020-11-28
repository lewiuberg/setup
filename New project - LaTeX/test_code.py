# Precondition 1: The "rantint" function from the random module is imported.
from random import randint

# Precondition 2: All input values are integers.
class RandomNumRange:
    def randy(self, amount: int, min_range: int, max_range: int) -> list:
        """
        A method providing a set-list of random integers in a specific range.

        Args:
            amount (int): The quantity of items in the return list.
            min_range (int): The first possible selectable number.
            max_range (int): The last possible selectable number.

        Returns:
            list: A list containing all the random integers. Note! These may
            not be unique to each other.
        """
        self.amount = amount
        self.min_range = min_range
        self.max_range = max_range

        return [randint(min_range, max_range) for i in range(amount)]


_inst = RandomNumRange()
random_list = _inst.randy(10, 1, 20)
print(random_list)

# Postcondition 1: The output type is a list.
assert isinstance(list(), type(random_list))

# Postcondition 2: The length of the amount input and the list is equal.
assert len(random_list) == _inst.amount
