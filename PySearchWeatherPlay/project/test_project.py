from project import check,check_winner,calculator
def test_check():
    assert check(500,2) == "Too small, Try again"
    assert check(2,500) == "Too large"
    assert check(2,2) ==   "Yes you got it right"


def test_check_winner():
    assert check_winner("scissors","rock") == "You Win"
    assert check_winner("paper","scissors") == "You Win"
    assert check_winner("rock","paper") == "You Win"
    assert check_winner("rock","rock") == "It's a tie game"


def test_calculator():
    assert calculator("1 * 20") == 20
    assert calculator("5 + 3") == 8
    assert calculator("10 * 20") == 200
    assert calculator("5 + 30") == 35
    assert calculator("5 - 3") == 2
    assert calculator("5 + 6") == 11