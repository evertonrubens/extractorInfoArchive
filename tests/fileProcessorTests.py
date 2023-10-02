"""
Info: Este módulo se encarregará de processar arquivos .xml.
Autor: Everton Martins
Dt. 2023-09-29
version 1.0.0

"""

import unittest
from src.fileProcessor import processZip

class fileProcessorTests(unittest.TestCase):
    
    def test_processZip(self):
        
        zip_path  = ''
        zip_name  = ''
        val_names = ['Project', 'XMLFile', 'Line', 'FlowNameCount', 'ContextDescribe', 'FolderPath', 'FilePath']
        
        result = processZip(zip_path, zip_name, val_names)
        
        self.assertIsInstance(result,list)
        self.assertGreater(len(result),0)
        