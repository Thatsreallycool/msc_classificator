import unittest
from zb_msc_classificator.config.definition import ConfigEntityLinking
from zb_msc_classificator.entity_linking import EntityLink
from tests.testfiles.example_text import example_text


class EntityLinkingTest(unittest.TestCase):
    def test_tokenization_coordinates(self):
        el = EntityLink(
            config=ConfigEntityLinking()
        )
        cleaned = el.harmonize.remove_punctuation_text(
                example_text
        )
        test_text_coords = el.tokenize(cleaned)

        assert all(
            [
                item['token'] == example_text[item['start']:item['end']]
                for item in test_text_coords
            ]
        )


if __name__ == '__main__':
    unittest.main()
