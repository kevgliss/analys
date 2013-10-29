import unittest

class TestFile(unittest.TestCase):
    def test_create_temp_file(self):
        from analys.plugins.interfaces import File
        file_obj = File("filename", "data")

        root = file_obj.create_temp_file().split('/')[1]
        self.assertEqual("var", root)
    
    def test_delete_temp_file(self):
        from analys.plugins.interfaces import File
        file_obj = File("filename", "data")
        file_path = file_obj.create_temp_file()
        file_obj.delete_temp_file()
        try: 
            with open(file_path): pass
            assert False
        except:
            assert True

    def test_extension(self):
        from analys.plugins.interfaces import File
        file_obj = File("filename", "data")
        self.assertEqual(('text/plain', 'html'), file_obj.extension())

    def test_md5(self):
        from analys.plugins.interfaces import File
        file_obj = File("filename", "data")
        self.assertEqual("8d777f385d3dfec8815d20f7496026dc", file_obj.md5())

    def test_sha1(self):
        from analys.plugins.interfaces import File
        file_obj = File("filename", "data")
        self.assertEqual("a17c9aaa61e80a1bf71d0d850af4e5baa9800bbd", file_obj.sha1())

class TestURL(unittest.TestCase):
    def test_deobfuscate(self):
        from analys.plugins.interfaces import URL
        url = URL("hxxp://example[.]com")
        self.assertEqual("http://example.com", url.deobfuscate(url.url))
        
        url = URL("example[.]com")
        self.assertEqual("http://example.com", url.deobfuscate(url.url))

    def test_get_url_parts(self):
        from analys.plugins.interfaces import URL
        url = URL("http://www.example.com:80/test?a=2&b=3")
        self.assertEqual(['http', 
                          'www.example.com:80', 
                          '/test', 
                          '', 
                          'a=2&b=3', 
                          ''], list(url.get_url_parts()))

    def test_obfuscate(self):
        from analys.plugins.interfaces import URL
        url = URL("http://www.example.com")
        self.assertEqual("hxxp://www.example.com", url.obfuscate(url.url))


class TestParser(unittest.TestCase):
    def test_traverse(self):
        # parser = Parser(analysis_type, result_doc)
        # self.assertEqual(expected, parser.traverse(data))
        assert False # TODO: implement your test here

class TestSearch(unittest.TestCase):
    def test_run(self):
        assert False # TODO: implement your test here


    def test_cancel(self):
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
