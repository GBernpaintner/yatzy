def all_combos(dice):
    """Return the result of choosing each possible combination."""
    return {
        'ones': ones(dice),
        'twos': twos(dice),
        'threes': threes(dice),
        'fours': fours(dice),
        'fives': fives(dice),
        'sixes': sixes(dice),
        'pair': pair(dice),
        'two_pairs': two_pairs(dice),
        'three_of_a_kind': three_of_a_kind(dice),
        'four_of_a_kind': four_of_a_kind(dice),
        'small_straight': small_straight(dice),
        'large_straight': large_straight(dice),
        'full_house': full_house(dice),
        'chance': chance(dice),
        'yahtzee': yahtzee(dice),
    }


def ones(dice):
    """Return the value of ones in the dice."""
    return dice.count(1) * 1


def twos(dice):
    """Return the value of twos in the dice."""
    return dice.count(2) * 2


def threes(dice):
    """Return the value of threes in the dice."""
    return dice.count(3) * 3


def fours(dice):    
    """Return the value of fours in the dice."""
    return dice.count(4) * 4


def fives(dice):
    """Return the value of fives in the dice."""
    return dice.count(5) * 5


def sixes(dice):
    """Return the value of sixes in the dice."""
    return dice.count(6) * 6


def pair(dice):
    """Return the value of the best pair if the dice contains one, 0 otherwise."""
    for i in range(6, 0, -1):
        if dice.count(i) >= 2:
            return i * 2
    return 0


def two_pairs(dice):
    """Return the value of the best two pairs if the dice contains two, 0 otherwise."""
    pairs = []
    for i in range(6, 0, -1):
        if dice.count(i) >= 2:
            pairs.append(i)
    if len(pairs) == 2:
        return sum(pairs[:2]) * 2
    return 0


def three_of_a_kind(dice):
    """Return the value of the three of a kind if the dice contains one, 0 otherwise."""
    for i in range(6, 0, -1):
        if dice.count(i) >= 3:
            return i * 3
    return 0


def four_of_a_kind(dice):
    """Return the value of the four of a kind if the dice contains one, 0 otherwise."""
    for i in range(6, 0, -1):
        if dice.count(i) >= 4:
            return i * 4
    return 0


def small_straight(dice):
    """Return the value of the small straight if the dice contains one, 0 otherwise."""
    if dice.count(1) and dice.count(2) and dice.count(3) and dice.count(4) and dice.count(5):
        return 15
    return 0


def large_straight(dice):
    """Return the value of the large straight if the dice contains one, 0 otherwise."""
    if dice.count(2) and dice.count(3) and dice.count(4) and dice.count(5) and dice.count(6):
        return 20
    return 0


def full_house(dice):
    """Return the value of the full house if the dice contains one, 0 otherwise."""
    if two_pairs(dice) and three_of_a_kind(dice):
        return sum(dice)
    return 0


def chance(dice):
    """Return the value of the chance."""
    return sum(dice)


def yahtzee(dice):
    """Return the value of the yahtzee if the dice contains one, 0 otherwise."""
    if dice.count(dice[0]) == len(dice):
        return 50
    return 0


def test():
    """Test the functions in this module."""
    assert all_combos([1, 1, 1, 1, 1]) == {
        'ones': 5,
        'twos': 0,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 2,
        'two_pairs': 0,
        'three_of_a_kind': 3,
        'four_of_a_kind': 4,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 5,
        'yahtzee': 50,
    }
    assert all_combos([2, 2, 2, 2, 2]) == {
        'ones': 0,
        'twos': 10,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 4,
        'two_pairs': 0,
        'three_of_a_kind': 6,
        'four_of_a_kind': 8,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 10,
        'yahtzee': 50,
    }
    assert all_combos([3, 3, 3, 3, 3]) == {
        'ones': 0,
        'twos': 0,
        'threes': 15,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 6,
        'two_pairs': 0,
        'three_of_a_kind': 9,
        'four_of_a_kind': 12,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 15,
        'yahtzee': 50,
    }
    assert all_combos([4, 4, 4, 4, 4]) == {
        'ones': 0,
        'twos': 0,
        'threes': 0,
        'fours': 20,
        'fives': 0,
        'sixes': 0,
        'pair': 8,
        'two_pairs': 0,
        'three_of_a_kind': 12,
        'four_of_a_kind': 16,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 20,
        'yahtzee': 50,
    }
    assert all_combos([5, 5, 5, 5, 5]) == {
        'ones': 0,
        'twos': 0,
        'threes': 0,
        'fours': 0,
        'fives': 25,
        'sixes': 0,
        'pair': 10,
        'two_pairs': 0,
        'three_of_a_kind': 15,
        'four_of_a_kind': 20,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 25,
        'yahtzee': 50,
    }
    assert all_combos([6, 6, 6, 6, 6]) == {
        'ones': 0,
        'twos': 0,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 30,
        'pair': 12,
        'two_pairs': 0,
        'three_of_a_kind': 18,
        'four_of_a_kind': 24,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 30,
        'yahtzee': 50,
    }
    assert all_combos([1, 1, 1, 1, 2]) == {
        'ones': 4,
        'twos': 2,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 2,
        'two_pairs': 0,
        'three_of_a_kind': 3,
        'four_of_a_kind': 4,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 6,
        'yahtzee': 0,
    }
    assert all_combos([1, 2, 3, 4, 5]) == {
        'ones': 1,
        'twos': 2,
        'threes': 3,
        'fours': 4,
        'fives': 5,
        'sixes': 0,
        'pair': 0,
        'two_pairs': 0,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'small_straight': 15,
        'large_straight': 0,
        'full_house': 0,
        'chance': 15,
        'yahtzee': 0,
    }
    assert all_combos([2, 3, 4, 5, 6]) == {
        'ones': 0,
        'twos': 2,
        'threes': 3,
        'fours': 4,
        'fives': 5,
        'sixes': 6,
        'pair': 0,
        'two_pairs': 0,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'small_straight': 0,
        'large_straight': 20,
        'full_house': 0,
        'chance': 20,
        'yahtzee': 0,
    }
    assert all_combos([1, 1, 2, 2, 3]) == {
        'ones': 2,
        'twos': 4,
        'threes': 3,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 4,
        'two_pairs': 6,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 0,
        'chance': 9,
        'yahtzee': 0,
    }
    assert all_combos([1, 1, 1, 2, 2]) == {
        'ones': 3,
        'twos': 4,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'pair': 4,
        'two_pairs': 6,
        'three_of_a_kind': 3,
        'four_of_a_kind': 0,
        'small_straight': 0,
        'large_straight': 0,
        'full_house': 7,
        'chance': 7,
        'yahtzee': 0,
    }

    print('All tests passed!')


if __name__ == '__main__':
    test()

        