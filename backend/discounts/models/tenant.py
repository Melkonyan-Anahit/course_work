from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100, verbose_name='Անվանում')
    domain = models.CharField(max_length=50, unique=True, verbose_name='Դոմեյն')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Համալսարան'
        verbose_name_plural = 'Համալսարաններ'
        ordering = ['name']

    def __str__(self):
        return self.name