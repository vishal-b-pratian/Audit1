from django.test import TestCase
from MyContentAnalyser.models import *

###TEST MODELS###

class TestLinks(TestCase):
    '''Validates CRUD operations on the Links table in the Database'''
    def setUp(self):
        Links.objects.create(
            channel_id = "test1",
            url = "https://www.lwcc.com/resources/dont-just-hydrate-acclimate",
            parameters = {'valueprop': ['excellence', 'execution'], 'tagline': ['louisiana', 'loyal']}
        )

    def testCreationByRead(self):
        link = Links.objects.get(channel_id="test1")
        self.assertEqual(link.url, "https://www.lwcc.com/resources/dont-just-hydrate-acclimate")
    
    def testUpdate(self):
        link = Links.objects.get(channel_id="test1")
        link.url = "https://www.lwcc.com/workers-comp/why-lwcc"
        self.assertEqual(link.url, "https://www.lwcc.com/workers-comp/why-lwcc")

    def testDelete(self):
        link = Links.objects.get(channel_id="test1")
        link.delete()
        self.assertFalse(Links.objects.filter(channel_id="test1").exists())

    def tearDown(self):
        pass