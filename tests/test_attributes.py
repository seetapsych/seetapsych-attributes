import seetapsych_attributes as pkg


def test_version() -> None:
    print(f"Package: {pkg.__name__}")
    print(f"Version: {pkg.__version__}")
    assert isinstance(pkg.__version__, str)
    assert len(pkg.__version__) > 0
