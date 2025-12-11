from django.db import models
from .tenant import Tenant

class Faculty(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    name = models.CharField(max_length=200, verbose_name='Անվանում')
    code = models.CharField(max_length=20, unique=True, verbose_name='Կոդ')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ֆակուլտետ'
        verbose_name_plural = 'Ֆակուլտետներ'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"