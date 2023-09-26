from django.db import models

# Create your models here.
class Ratechange(models.Model):
    cur_unit = models.TextField(unique=True)     # 통화코드
    cur_nm = models.TextField()       # 국가/통화명
    deal_bas_r = models.TextField()   # 매매 기준율
    dataDate = models.TextField(blank=True)
