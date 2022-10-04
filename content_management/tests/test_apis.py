from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from content_management.models import *
from content_management.api.views import *

###Test APIs###

class TestAddressAPI(APITestCase):

    def setUp(self):
        pass
    
    def testPostThenGet(self):
        url = reverse(LinksViewSet)
        data =     {
                "channel_id": "test7",
                "url": "https://www.lwcc.com/resources/dont-just-hydrate-acclimate",
                "parameters": "{'differentiator': ['elevate', 'love', 'elevating', 'louisiana', 'elevating', 'our state', 'celebrate', 'louisiana', 'celebrating', 'louisiana', 'celebrate', 'our state', 'celebrating', 'our state', 'elevate', 'the state', 'elevating', 'the state', 'celebrate', 'the state', 'celebrating', 'the state'], 'posmotag': ['champion', 'louisiana', 'champions', 'louisiana', 'champion', 'our state', 'champions', 'our state', 'champion', 'the state', 'champions', 'the state'], 'position': ['model', 'louisiana', 'champion', 'excellence', 'execution', 'workers comp', 'model', 'louisianas', 'champion', 'excellence', 'execution', 'workers comp', 'model', 'louisiana', 'champion', 'excellence', 'execution', 'workers compensation', 'model', 'louisianas', 'champion', 'excellence', 'execution', 'workers compensation'], 'valueprop': ['excellence', 'execution'], 'tagline': ['louisiana', 'loyal']}",
                "title": "Lwcc test"
            }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Links.objects.count(), 1)
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(ContentFetchInfo.objects.count(), 1)
        self.assertEqual(MappedKeyWords.objects.count(), 1)
        self.assertEqual(UnmappedKeywords.objects.count(), 1)
        self.assertEqual(Links.objects.get().title, 'Lwcc test')

    def tearDown(self):
        pass