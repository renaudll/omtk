import omtk_test


class SampleTests(omtk_test.TestCase):
    @omtk_test.open_scene('./test_interactivefk01.ma')
    def test_interactivefk01(self):
        self._build_unbuild_build_all(test_translate=False, test_rotate=False, test_scale=False)  # todo: re-enabled test t/r/s

    @omtk_test.open_scene('./test_interactivefk02.ma')
    def test_interactivefk02(self):
        self._build_unbuild_build_all(test_translate=False, test_rotate=False, test_scale=False)  # todo: re-enabled test t/r/s

    @omtk_test.open_scene('./test_interactivefk03.ma')
    def test_interactivefk03(self):
        self._build_unbuild_build_all(test_translate=False, test_rotate=False, test_scale=False)  # todo: re-enabled test t/r/s
