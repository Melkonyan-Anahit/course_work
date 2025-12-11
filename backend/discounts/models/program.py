from django.db import models
from .tenant import Tenant
from .faculty import Faculty

class Program(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name='Ֆակուլտետ')
    name = models.CharField(max_length=200, verbose_name='Անվանում')
    code = models.CharField(max_length=20, unique=True, verbose_name='Կոդ')
    base_tuition_fee = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Բազային վարձ')
    duration_years = models.IntegerField(default=4, verbose_name='Տևողություն (տարի)')
    free_seats = models.IntegerField(default=0, verbose_name='Անվճար տեղեր')
    paid_seats = models.IntegerField(default=0, verbose_name='Վճարովի տեղեր')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Մասնագիտություն'
        verbose_name_plural = 'Մասնագիտություններ'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"