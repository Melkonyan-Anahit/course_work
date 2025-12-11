from django.db import models
from django.utils import timezone
from .tenant import Tenant
from .student import Student

class DiscountCategory(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    name = models.CharField(max_length=100, verbose_name='Անվանում')
    code = models.CharField(max_length=20, unique=True, verbose_name='Կոդ')
    description = models.TextField(blank=True, null=True, verbose_name='Նկարագրություն')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Զեղչի կատեգորիա'
        verbose_name_plural = 'Զեղչի կատեգորիաներ'

    def __str__(self):
        return self.name

class DiscountRule(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    category = models.ForeignKey(DiscountCategory, on_delete=models.CASCADE, verbose_name='Կատեգորիա')
    name = models.CharField(max_length=200, verbose_name='Անվանում')
    code = models.CharField(max_length=50, unique=True, verbose_name='Կոդ')
    percentage_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Նվազագույն %')
    percentage_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Առավելագույն %')
    priority = models.IntegerField(default=1, verbose_name='Առաջնահերթություն')
    is_combinable = models.BooleanField(default=True, verbose_name='Համակցելի է')
    description = models.TextField(blank=True, null=True, verbose_name='Նկարագրություն')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Զեղչի կանոն'
        verbose_name_plural = 'Զեղչի կանոններ'
        ordering = ['-priority']

    def __str__(self):
        return f"{self.code} - {self.name}"

class DiscountCondition(models.Model):
    discount_rule = models.ForeignKey(DiscountRule, on_delete=models.CASCADE, verbose_name='Զեղչի կանոն')
    condition_type = models.CharField(max_length=50, verbose_name='Պայմանի տեսակ')
    operator = models.CharField(max_length=10, verbose_name='Օպերատոր')
    value = models.CharField(max_length=100, verbose_name='Արժեք')
    is_required = models.BooleanField(default=True, verbose_name='Պարտադիր է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Զեղչի պայման'
        verbose_name_plural = 'Զեղչի պայմաններ'

    def __str__(self):
        return f"{self.discount_rule.code} - {self.condition_type}"

class AppliedDiscount(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ուսանող')
    discount_rule = models.ForeignKey(DiscountRule, on_delete=models.CASCADE, verbose_name='Զեղչի կանոն')
    semester = models.CharField(max_length=20, verbose_name='Կիսամյակ')
    applied_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Կիրառված %')
    approved_by = models.IntegerField(blank=True, null=True, verbose_name='Հաստատող')
    applied_date = models.DateTimeField(default=timezone.now, verbose_name='Կիրառման ամսաթիվ')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')

    class Meta:
        verbose_name = 'Կիրառված զեղչ'
        verbose_name_plural = 'Կիրառված զեղչեր'
        unique_together = ['student', 'discount_rule', 'semester']

    def __str__(self):
        return f"{self.student.full_name} - {self.discount_rule.code} - {self.applied_percentage}%"