#from django.db import models
import math
from collections import defaultdict
import json
import unicodedata
from django.db import models
from django.utils.timezone import now
import datetime
# instituicoes_request pode ser referenciada pelos cnpj das instituicoes, caso algum problema de dupla referencia

class ChartRequestsMemory(models.Model):
    instituicoes_request = models.CharField(unique=True, null=False, max_length=100) #instituicoes Requisitados
    request_amount = models.IntegerField(default=1, db_index=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        # Retain only the last 50 items based on `request amount`
        if ChartRequestsMemory.objects.count() > 50:
            items_to_delete = ChartRequestsMemory.objects.order_by('request_amount')[:ChartRequestsMemory.objects.count() - 50]
            ChartRequestsMemory.objects.filter(pk__in=items_to_delete).delete()
            
    def __str__(self):
        return f"{self.instituicoes_request} - {self.request_amount} vezes"
    
    # ALTER TABLE app_dashboard_tf_idf MODIFY palavra VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
    

    