def test_submit():
    from bluecoat import Bluecoat
    b = Bluecoat("www.google.com")
    result = b.submit()
    assert result == "Search Engines/Portals"
