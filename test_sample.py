# content of test_sample.py
#Note: any files that match test_*.py or *_test.py will be checked for tests to run
def func(x):
    return x + 1

def test_answer():
    #assert func(3) == 5
    assert func(4) == 5
