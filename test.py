import utils


def test_check_answer_against_exact_match():
    assert utils.check_answer('Boston', 'Boston')


def test_check_answer_incorrect():
    assert not utils.check_answer('Boston', 'Albany')


def test_check_answer_different_case_matches():
    assert utils.check_answer('BoStOn', 'Boston')


def test_check_answer_ignores_leading_trailing_whitespace():
    assert utils.check_answer(' Rome', 'Rome  ')


def test_check_answer_remove_punctuations():
    assert utils.check_answer('Rome.', 'Rome!!!')


def test_check_answer_remove_emoji():
    assert utils.check_answer('Rome', 'Rome 🥪')
