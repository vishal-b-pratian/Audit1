from django.db import models
from configuration import models as config_models
from django.db import models


class Links(models.Model):
    '''
    Model is used to store and relate source data from the configuration micro-service
    channel ID from the Channel table from the configuration module is used as a forigen key 
    '''
    channel = models.ForeignKey(to=config_models.Channel, on_delete = models.CASCADE)
    url = models.URLField()
    parameters = models.TextField(verbose_name='parameters',null= False)
    title=models.TextField(null=False,verbose_name='Title',max_length = 200, default="Content Title")
    def __str__(self):
        return self.channel.channel_name.channel_name

class Content(models.Model):
    
    '''
    Model is used to store data scraped from the source passed in configuration
    one to one relation is established to entries in Links model
    '''

    link = models.OneToOneField(
        Links,
        on_delete=models.CASCADE,
        primary_key=True
    )
    #scraped content
    main_content=models.TextField(verbose_name='Main Content',null= False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.link.channel.channel_name)

class ContentFetchInfo(models.Model):

    '''
    Model is used to store processed words extrated from scraped data 
    one to one relation is established with the Content model
    '''

    content = models.OneToOneField(
        Content,
        on_delete=models.CASCADE,
        primary_key=True
    )
    #processed content - summary keywords - viewContenSummary   
    processed_words = models.TextField(verbose_name = "Processed Words", null = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)


class MappedKeyWords(models.Model):

    '''
    Model is used to store a dictonary of count and a list of processed words that are mapped to audit parameter keywords
    one to one relation is established with the ContentfetchInfo model
    Structure of json for mapped keywords
    {
        'audit-parrameter': {
            'keyword': {
                'louisiana': {
                    'similar': [],
                    'word_count': 0
                },
                'loyal': {
                    'similar': ['notoriously', 'experience', 'extensive', 'personal', 'safe', 'great', 'beat',       'efficient', 'important', 'love', 'affection', 'base', 'long', 'experienced', 'ensure', 'throughout', 'aware', 'local', 'many', 'among'],
                    'word_count': 20}
            },
            'count': 20
        }
    }
    '''

    content_info = models.OneToOneField(
        ContentFetchInfo,
        on_delete=models.CASCADE,
        primary_key=True
    )
    mapped_keywords = models.TextField(verbose_name='Mapped keywords',null= False)
    mapped_keywords_count = models.IntegerField(verbose_name = "No. of Mapped Words", null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content_info)


class UnmappedKeywords(models.Model):
    
    '''
    Model is used to store a list of audit parameter keywords that weren't mapped to any processed words
    one to one relation is established with the ContentfetchInfo model
    '''

    content_info = models.OneToOneField(
        ContentFetchInfo,
        on_delete=models.CASCADE,
        primary_key=True
    )
    unmapped_keywords=models.TextField(verbose_name="Unmapped Keywords",null=True)
    unmapped_keywords_count = models.IntegerField(verbose_name = "Unmapped keyword count", null = True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return str(self.content_info)
