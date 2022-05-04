import backend
import unittest
import logger

class TestBackend(unittest.TestCase):
    def test_start(self):
        self.log = logger.log_module()
        path = "C:/Users/19785/Documents/MGH/Tasks/dicom_deidentification/Dicom_Deidentify_1.0/test_files/John_Smith"
        site_ID = "607"
        patient_ID = "1234567890"
        scan_session_ID = "12345678901234567890123456789012"
        results = []
        parent = 'test'
        self.dataset = backend.run(path, site_ID, patient_ID, scan_session_ID, results, self.log, parent)
        self.assertEqual(self.dataset.site_ID, site_ID)


if __name__ == '__main__':
    unittest.main()