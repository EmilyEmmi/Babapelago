from .bases import BabaIsYouTestBase


# Does base tests and nothing else.
class TestStartingLogic(BabaIsYouTestBase):
    options = {
        "goal": 5,
    }

    # Base tests:
    # - If you have every item, every location can be reached
    # - If you have no items, you can still reach something ("Sphere 1" is not empty)
    # - The world successfully generates (Fill does not crash)