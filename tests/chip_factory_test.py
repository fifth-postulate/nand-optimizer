from chip.factory import Factory

def test_if_chip_is_not_build_in_it_is_fetched():
    mockFetcher = MockFetcher()
    factory = Factory(buildins = {}, fetcher = mockFetcher)

    factory.chip('non_existing_chip')

    assert mockFetcher.fetch_count('non_existing_chip') == 1
    assert mockFetcher.total_fetch_count() == 1
    
def test_if_chip_is_build_in_nothing_is_fetched():
    mockFetcher = MockFetcher()
    factory = Factory(buildins = {'nand': MockBuilder()}, fetcher = mockFetcher)

    blueprint = factory.chip('nand')

    assert mockFetcher.fetch_count('nand') == 0
    assert mockFetcher.total_fetch_count() == 0

def test_if_chip_is_fetched_only_once():
    mockFetcher = MockFetcher()
    factory = Factory(buildins = {}, fetcher = mockFetcher)

    factory.chip('nor')
    factory.chip('nor')

    assert mockFetcher.fetch_count('nor') == 1
    assert mockFetcher.total_fetch_count() == 1

class MockFetcher:
    def __init__(self):
        self.count = {}

    def fetch(self, name):
        if not name in self.count:
            self.count[name] = 0
        self.count[name] += 1
        return MockBuilder()

    def fetch_count(self, name):
        if not name in self.count:
            self.count[name] = 0
        return self.count[name]

    def total_fetch_count(self):
        total = 0
        for name in self.count:
            total += self.count[name]
        return total

class MockBuilder:
    pass 

