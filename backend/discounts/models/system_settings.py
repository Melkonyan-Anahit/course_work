from django.db import models
from .tenant import Tenant

class SystemSettings(models.Model):
    
    VALUE_TYPES = [
        ('int', 'Ամբողջ թիվ'),
        ('float', 'Տասնորդական'),
        ('string', 'Տեքստ'),
        ('boolean', 'Այո/Ոչ')
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    setting_key = models.CharField(max_length=100, verbose_name='Կարգավորման բանալի')
    setting_value = models.CharField(max_length=200, verbose_name='Արժեք')
    value_type = models.CharField(
        max_length=20,
        choices=VALUE_TYPES,
        default='string',
        verbose_name='Տիպ'
    )
    description = models.TextField(blank=True, verbose_name='Նկարագրություն')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Համակարգային կարգավորում'
        verbose_name_plural = 'Համակարգային կարգավորումներ'
        unique_together = ['tenant', 'setting_key']
        ordering = ['setting_key']
    
    def __str__(self):
        return f"{self.setting_key} = {self.setting_value}"
    
    def get_value(self):
        """Վերածել string-ը ճիշտ տիպի"""
        if self.value_type == 'int':
            return int(self.setting_value)
        elif self.value_type == 'float':
            return float(self.setting_value)
        elif self.value_type == 'boolean':
            return self.setting_value.lower() in ['true', '1', 'yes']
        return self.setting_value