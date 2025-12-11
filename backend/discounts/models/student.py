from django.db import models
from .tenant import Tenant
from .program import Program

class Student(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Համալսարան')
    first_name = models.CharField(max_length=50, verbose_name='Անուն')
    last_name = models.CharField(max_length=50, verbose_name='Ազգանուն')
    email = models.EmailField(blank=True, null=True, verbose_name='Էլ. փոստ')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Հեռախոս')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Ծննդյան ամսաթիվ')
    enrollment_date = models.DateField(verbose_name='Ընդունման ամսաթիվ')
    status = models.CharField(max_length=20, default='active', verbose_name='Կարգավիճակ')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ուսանող'
        verbose_name_plural = 'Ուսանողներ'
        ordering = ['id']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def display_id(self):
        try:
            enrollment = self.enrollment_set.first()
            if enrollment:
                faculty_code = enrollment.program.faculty.code
                year = self.enrollment_date.year
                number = str(self.id).zfill(3)
                return f"{faculty_code}-{year}-{number}"
        except:
            pass
        return str(self.id)

    def __str__(self):
        return f"{self.display_id} - {self.full_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ուսանող')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='Մասնագիտություն')
    enrollment_type = models.CharField(max_length=20, verbose_name='Տեղաբաշխման տեսակ')
    current_semester = models.IntegerField(default=1, verbose_name='Ընթացիկ կիսամյակ')
    entry_year = models.IntegerField(verbose_name='Ընդունման տարի')
    status = models.CharField(max_length=20, default='active', verbose_name='Կարգավիճակ')
    enrolled_date = models.DateField(verbose_name='Ընդունման ամսաթիվ')
    graduation_date = models.DateField(blank=True, null=True, verbose_name='Ավարտի ամսաթիվ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Տեղաբաշխում'
        verbose_name_plural = 'Տեղաբաշխումներ'

    def __str__(self):
        return f"{self.student.full_name} - {self.program.code}"

class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ուսանող')
    semester = models.CharField(max_length=20, verbose_name='Կիսամյակ')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='ՄԲ')
    credits_earned = models.IntegerField(default=0, verbose_name='Վաստակած կրեդիտներ')
    credits_total = models.IntegerField(default=0, verbose_name='Ընդհանուր կրեդիտներ')
    academic_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ակադեմիական կարգավիճակ')
    is_scholarship_eligible = models.BooleanField(default=False, verbose_name='Կրթաթոշակի իրավունք')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ակադեմիական գրանցում'
        verbose_name_plural = 'Ակադեմիական գրանցումներ'
        unique_together = ['student', 'semester']

    def __str__(self):
        return f"{self.student.full_name} - {self.semester}"


class StudentAttribute(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ուսանող')
    attribute_type = models.CharField(max_length=50, verbose_name='Հատկանիշի տեսակ')
    value = models.CharField(max_length=200, verbose_name='Արժեք')
    valid_from = models.DateField(verbose_name='Վավեր սկսած')
    valid_to = models.DateField(blank=True, null=True, verbose_name='Վավեր մինչև')
    document_reference = models.CharField(max_length=100, blank=True, null=True, verbose_name='Փաստաթուղթ')
    verified_by = models.IntegerField(blank=True, null=True, verbose_name='Հաստատող')
    verified_date = models.DateField(blank=True, null=True, verbose_name='Հաստատման ամսաթիվ')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ուսանողի հատկանիշ'
        verbose_name_plural = 'Ուսանողի հատկանիշներ'

    def __str__(self):
        return f"{self.student.full_name} - {self.attribute_type}"