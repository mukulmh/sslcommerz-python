from django.db import models

class Transactions(models.Model):
    tran_id = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(default='Pending', max_length=255)
    card_type = models.CharField(max_length=255, null=True, blank=True)
    val_id = models.CharField(max_length=60, blank=True, null=True)
    currency = models.CharField(max_length=10, default='BDT')
    store_amount = models.FloatField(blank=True, null=True)
    card_no = models.CharField(max_length=50, blank=True, null=True)
    card_issuer = models.CharField(max_length=50, blank=True, null=True)
    card_brand = models.CharField(max_length=50, blank=True, null=True)
    card_sub_brand = models.CharField(max_length=50, blank=True, null=True)
    card_issuer_country = models.CharField(max_length=50, blank=True, null=True)
    card_issuer_country_code = models.CharField(max_length=50, blank=True, null=True)
    currency_rate = models.FloatField(blank=True, null=True)
    base_fair = models.FloatField(blank=True, null=True)
    bank_tran_id = models.CharField(max_length=90, blank=True, null=True)
    response_of_val = models.CharField(max_length=2000, blank=True, null=True)
    response_of_failed = models.CharField(max_length=2000, blank=True, null=True)
    risk_title = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.tran_id