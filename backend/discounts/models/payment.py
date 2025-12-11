from django.db import models
from .student import Student

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ուսանող')
    semester = models.CharField(max_length=20, verbose_name='Կիսամյակ')
    payment_type = models.CharField(max_length=50, verbose_name='Վճարման տեսակ')
    original_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Սկզբնական գումար')
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Զեղչի գումար')
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Վերջնական գումար')
    status = models.CharField(max_length=20, default='pending', verbose_name='Կարգավիճակ')
    due_date = models.DateField(verbose_name='Վերջնաժամկետ')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='Վճարման ամսաթիվ')
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name='Վճարման եղանակ')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Գործարքի ID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Վճարում'
        verbose_name_plural = 'Վճարումներ'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.semester} - {self.final_amount}"