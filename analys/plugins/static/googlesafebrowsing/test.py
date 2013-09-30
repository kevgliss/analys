def test_submit():
    from googlesafebrowsing import GoogleSafeBrowsing
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('googlesafebrowsing.analys-plugin')
    g = GoogleSafeBrowsing("www.google.com", config.get('Core', 'APIKey'))
    result = g.submit()
    assert  result == "clean"


