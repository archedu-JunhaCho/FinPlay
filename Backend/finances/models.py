from django.db import models
from accounts.models import * 

# 추천 문구
class Recommendation(models.Model):
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Recommendproducts(models.Model):
    products = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# 정기예금 상품
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField(choices=[
        ('1','제한없음'),
        ('2','서민전용'),
        ('3','일부제한')
    ])
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    dcls_month = models.TextField()
class Dkeyword(models.Model):
    keyword = models.TextField(blank=True, null=True)
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)

# 정기예금 옵션
class DepositOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
    save_trm = models.IntegerField()


# 적금 상품
class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField(choices=[
        ('1','제한없음'),
        ('2','서민전용'),
        ('3','일부제한')
    ])
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    dcls_month = models.TextField()
class Skeyword(models.Model):
    keyword = models.TextField(blank=True, null=True)
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)

# 적금 옵션
class SavingOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
    save_trm = models.IntegerField()
