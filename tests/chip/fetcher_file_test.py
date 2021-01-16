import os
import pytest
from chip.fetcher import FileFetcher, CouldNotParseChip, NonExistingChip

definitions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

def test_if_a_chip_is_unknown_an_NonExistingChip_exception_is_raised():
    fetcher = FileFetcher(definitions_path)

    with pytest.raises(NonExistingChip):
        fetcher.fetch('non_existing_chip')

def test_if_a_chip_is_known_but_can_not_be_parsed_an_CouldNotParseChip_exception_is_raised():
    fetcher = FileFetcher(definitions_path)

    with pytest.raises(CouldNotParseChip):
        fetcher.fetch('broken')

def test_if_a_chip_known_and_can_be_parsed_a_blueprint_is_returned():
    fetcher = FileFetcher(definitions_path)

    blueprint = fetcher.fetch('not')

    assert blueprint