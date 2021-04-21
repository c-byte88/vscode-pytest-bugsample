import unittest

import project_pipeline.helpers.acceptance_tests_helpers as Ath

class Test_Acceptance_tests_helpers(unittest.TestCase):

    def test_remove_dbfs_prefix_shortpath_success(self):
        data = '/dbfs/testpath/'
        result = Ath.remove_dbfs_prefix(data)
        self.assertEqual(result,  '/testpath/')
