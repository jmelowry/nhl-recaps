import unittest
import nhl_recaps

class TestRecaps(unittest.TestCase):

    def test_list_length(self):
        game_descriptions = nhl_recaps.get_descriptions()
        assert len(game_descriptions) == 20

if __name__ == '__main__':
    test = TestRecaps().test_list_length()
