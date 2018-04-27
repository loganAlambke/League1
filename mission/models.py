from django.db import models


REGION_CHOICES = (
    ('na1', 'NA1'),
    ('br1', 'BR1'),
    ('eun1', 'EUN1'),
    ('euw1', 'EUW1'),
    ('jp1', 'JP1'),
    ('kr', 'KR'),
    ('la1', 'LA1'),
    ('la2', 'LA2'),
    ('oc1', 'OC1'),
    ('tr1', 'TR1'),
    ('ru', 'RU')
)

# class Reading(models.Model):
#     summoner_id = models.IntegerField()
#     account_id = models.IntegerField()




class Input(models.Model):
    username = models.CharField(max_length=25)
    summoner_id = models.IntegerField(default=0)
    account_id = models.IntegerField(default=0)
    top_kill = models.IntegerField(default=0)
    region = models.CharField(max_length=6, choices= REGION_CHOICES, default='NA1', )
    item0 = models.IntegerField(default=0)
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    item6 = models.IntegerField(default=0)


    class Meta:
        unique_together = (('username', 'region'))





