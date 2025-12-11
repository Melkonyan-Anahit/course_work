from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from discounts.models import (
    Tenant, Faculty, Program, Student, Enrollment,
    AcademicRecord, StudentAttribute, DiscountCategory,
    DiscountRule, DiscountCondition, AppliedDiscount, 
    Payment, SystemSettings
)


class Command(BaseCommand):
    help = 'Ստեղծել 15 թեստային ուսանողներ տարբեր զեղչի scenarios-ով'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Սկսում ենք ուսանողների ստեղծումը...'))

        tenant = Tenant.objects.filter(is_active=True).first()
        if not tenant:
            self.stdout.write(self.style.ERROR('Tenant չի գտնվել'))
            return
        
        programs = list(Program.objects.filter(tenant=tenant, is_active=True))
        if not programs:
            self.stdout.write(self.style.ERROR('Programs չեն գտնվել'))
            return
        
        discount_rules = {
            rule.code: rule 
            for rule in DiscountRule.objects.filter(tenant=tenant, is_active=True)
        }
        
        self.create_student_1_orphan(tenant, programs, discount_rules)
        self.create_student_2_single_parent(tenant, programs, discount_rules)
        self.create_student_3_young_parent(tenant, programs, discount_rules)
        self.create_student_4_large_family(tenant, programs, discount_rules)
        self.create_student_5_social_high(tenant, programs, discount_rules)
        self.create_student_6_social_low(tenant, programs, discount_rules)
        self.create_student_7_excellent_4sem(tenant, programs, discount_rules)
        self.create_student_8_parent_work_15y(tenant, programs, discount_rules)
        self.create_student_9_parent_work_5y(tenant, programs, discount_rules)
        self.create_student_10_npua_siblings(tenant, programs, discount_rules)
        self.create_student_11_disability(tenant, programs, discount_rules)
        self.create_student_12_military(tenant, programs, discount_rules)
        self.create_student_13_teacher_child(tenant, programs, discount_rules)
        self.create_student_14_multiple_discounts(tenant, programs, discount_rules)
        self.create_student_15_no_discount(tenant, programs, discount_rules)
        
        self.stdout.write(self.style.SUCCESS('15 ուսանողներ հաջողությամբ ստեղծվեցին!'))
    
    def create_student_base(self, tenant, first_name, last_name, birth_date, program, 
                           entry_year, current_semester, enrollment_type='paid'):
        
        enrollment_date = date(entry_year, 9, 1)
        
        student, created = Student.objects.get_or_create(
            tenant=tenant,
            first_name=first_name,
            last_name=last_name,
            defaults={
                'birth_date': birth_date,
                'enrollment_date': enrollment_date,
                'email': f'{first_name.lower()}.{last_name.lower()}@student.npua.am',
                'phone': f'+37499{random.randint(100000, 999999)}',
                'status': 'active',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Ուսանող: {first_name} {last_name}')
        
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student,
            program=program,
            defaults={
                'entry_year': entry_year,
                'enrollment_type': enrollment_type,
                'current_semester': current_semester,
                'enrolled_date': enrollment_date,
                'status': 'active'
            }
        )
        
        return student, enrollment
    
    def create_academic_records(self, student, num_semesters, gpa_values):
        for semester_num in range(1, num_semesters + 1):
            gpa = gpa_values[semester_num - 1] if semester_num <= len(gpa_values) else 70
            
            AcademicRecord.objects.get_or_create(
                student=student,
                semester=f'{semester_num}',
                defaults={
                    'gpa': Decimal(str(gpa)),
                    'credits_earned': 30,
                    'credits_total': 30,
                    'is_scholarship_eligible': gpa >= 60
                }
            )
    
    def apply_discount_and_payment(self, tenant, student, enrollment, discount_rule_code, discount_rules):

        
        base_fee = enrollment.program.base_tuition_fee
        
        if discount_rule_code and discount_rule_code in discount_rules:
            rule = discount_rules[discount_rule_code]
            discount_percentage = rule.percentage_min
    
            AppliedDiscount.objects.get_or_create(
                student=student,
                discount_rule=rule,
                semester=str(enrollment.current_semester),
                defaults={
                    'applied_percentage': discount_percentage,
                    'applied_date': timezone.now(),
                    'is_active': True
                }
            )
            
            final_fee = base_fee * (100 - discount_percentage) / 100
            discount_amount = base_fee - final_fee
            self.stdout.write(f'Վարձ: {int(base_fee):,} → {int(final_fee):,} դրամ ({int(discount_percentage)}% զեղչ)')
        else:
            final_fee = base_fee
            discount_amount = 0
            self.stdout.write(f'Վարձ: {int(base_fee):,} դրամ (զեղչ չկա)')
        
        Payment.objects.get_or_create(
            student=student,
            semester=str(enrollment.current_semester),
            defaults={
                'payment_type': 'tuition',
                'original_amount': Decimal(str(base_fee)),
                'discount_amount': Decimal(str(discount_amount)),
                'final_amount': Decimal(str(final_fee)),
                'status': 'pending',
                'due_date': timezone.now().date() + timedelta(days=30)
            }
        )

    
    def create_student_1_orphan(self, tenant, programs, discount_rules):
        program = next((p for p in programs if p.code == 'CS'), programs[0])
        student, enrollment = self.create_student_base(
            tenant, 'Արման', 'Գրիգորյան',
            date(2003, 5, 15), program, 2021, 7
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='is_orphan',
            defaults={
                'value': 'True',
                'valid_from': date(2021, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 7, [75, 78, 80, 82, 79, 81, 83])
        self.apply_discount_and_payment(tenant, student, enrollment, 'ORPHAN', discount_rules)
    
    def create_student_2_single_parent(self, tenant, programs, discount_rules):
        program = next((p for p in programs if p.code == 'SE'), programs[1])
        student, enrollment = self.create_student_base(
            tenant, 'Նարե', 'Հովհաննիսյան',
            date(2004, 3, 22), program, 2022, 5
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='is_single_parent',
            defaults={
                'value': 'True',
                'valid_from': date(2022, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 5, [72, 74, 76, 75, 77])
        self.apply_discount_and_payment(tenant, student, enrollment, 'SINGLE_PARENT', discount_rules)
    
    def create_student_3_young_parent(self, tenant, programs, discount_rules):
      
        program = next((p for p in programs if p.code == 'IS'), programs[2])
        student, enrollment = self.create_student_base(
            tenant, 'Անի', 'Պետրոսյան',
            date(2002, 8, 10), program, 2020, 9
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='has_young_child',
            defaults={
                'value': 'True',
                'valid_from': date(2024, 1, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 9, [70, 72, 74, 76, 78, 75, 77, 79, 80])
        self.apply_discount_and_payment(tenant, student, enrollment, 'YOUNG_PARENT', discount_rules)
    
    def create_student_4_large_family(self, tenant, programs, discount_rules):
      
        program = next((p for p in programs if p.code == 'AI'), programs[3])
        student, enrollment = self.create_student_base(
            tenant, 'Դավիթ', 'Ավետիսյան',
            date(2005, 1, 5), program, 2023, 3
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='family_children',
            defaults={
                'value': '4',
                'valid_from': date(2023, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 3, [68, 70, 72])
        self.apply_discount_and_payment(tenant, student, enrollment, 'LARGE_FAMILY', discount_rules)
    
    def create_student_5_social_high(self, tenant, programs, discount_rules):
     
        program = next((p for p in programs if p.code == 'CYBER'), programs[4])
        student, enrollment = self.create_student_base(
            tenant, 'Մարիամ', 'Սարգսյան',
            date(2004, 11, 20), program, 2022, 5
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='social_score',
            defaults={
                'value': '35',
                'valid_from': date(2022, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 5, [65, 67, 69, 71, 73])
        self.apply_discount_and_payment(tenant, student, enrollment, 'SOCIAL_HIGH', discount_rules)
    
    def create_student_6_social_low(self, tenant, programs, discount_rules):
     
        program = next((p for p in programs if p.code == 'ELEC'), programs[5])
        student, enrollment = self.create_student_base(
            tenant, 'Արթուր', 'Մխիթարյան',
            date(2003, 7, 12), program, 2021, 7
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='social_score',
            defaults={
                'value': '15',
                'valid_from': date(2021, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 7, [66, 68, 70, 72, 74, 73, 75])
        self.apply_discount_and_payment(tenant, student, enrollment, 'SOCIAL_LOW', discount_rules)
    
    def create_student_7_excellent_4sem(self, tenant, programs, discount_rules):
      
        program = next((p for p in programs if p.code == 'IT'), programs[6])
        student, enrollment = self.create_student_base(
            tenant, 'Լուսինե', 'Գեվորգյան',
            date(2004, 4, 8), program, 2022, 5
        )
        
        self.create_academic_records(student, 5, [85, 87, 89, 86, 88])
        self.apply_discount_and_payment(tenant, student, enrollment, 'EXCELLENT_4SEM', discount_rules)
    
    def create_student_8_parent_work_15y(self, tenant, programs, discount_rules):
       
        program = next((p for p in programs if p.code == 'INFOSEC'), programs[7])
        student, enrollment = self.create_student_base(
            tenant, 'Հայկ', 'Աբրահամյան',
            date(2005, 9, 3), program, 2023, 3
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='parent_npua_years',
            defaults={
                'value': '18',
                'valid_from': date(2023, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 3, [75, 77, 79])
        self.apply_discount_and_payment(tenant, student, enrollment, 'PARENT_WORK_15Y_PLUS', discount_rules)
    
    def create_student_9_parent_work_5y(self, tenant, programs, discount_rules):
       
        program = next((p for p in programs if p.code == 'BLOCKCHAIN'), programs[8])
        student, enrollment = self.create_student_base(
            tenant, 'Էլեն', 'Հակոբյան',
            date(2004, 6, 18), program, 2022, 5
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='parent_npua_years',
            defaults={
                'value': '10',
                'valid_from': date(2022, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 5, [70, 72, 74, 76, 78])
        self.apply_discount_and_payment(tenant, student, enrollment, 'PARENT_WORK_5_15Y', discount_rules)
    
    def create_student_10_npua_siblings(self, tenant, programs, discount_rules):
        
        program = next((p for p in programs if p.code == 'THERMO'), programs[9])
        student, enrollment = self.create_student_base(
            tenant, 'Տիգրան', 'Խաչատրյան',
            date(2005, 2, 25), program, 2023, 3
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='npua_siblings',
            defaults={
                'value': '2',
                'valid_from': date(2023, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 3, [65, 67, 69])
        self.apply_discount_and_payment(tenant, student, enrollment, 'NPUA_SIBLINGS', discount_rules)
    
    def create_student_11_disability(self, tenant, programs, discount_rules):
        
        program = next((p for p in programs if p.code == 'ELPOWER'), programs[10])
        student, enrollment = self.create_student_base(
            tenant, 'Գոհար', 'Բաբայան',
            date(2003, 10, 30), program, 2021, 7
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='parent_disability',
            defaults={
                'value': 'True',
                'valid_from': date(2021, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 7, [68, 70, 72, 74, 76, 75, 77])
        self.apply_discount_and_payment(tenant, student, enrollment, 'DISABILITY', discount_rules)
    
    def create_student_12_military(self, tenant, programs, discount_rules):
       
        program = next((p for p in programs if p.code == 'AUTO'), programs[11])
        student, enrollment = self.create_student_base(
            tenant, 'Վահագն', 'Մանուկյան',
            date(2002, 12, 14), program, 2020, 9
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='military_service',
            defaults={
                'value': 'True',
                'valid_from': date(2024, 1, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 9, [70, 72, 74, 76, 78, 77, 79, 81, 80])
        self.apply_discount_and_payment(tenant, student, enrollment, 'MILITARY', discount_rules)
    
    def create_student_13_teacher_child(self, tenant, programs, discount_rules):
      
        program = next((p for p in programs if p.code == 'ROBOT'), programs[12])
        student, enrollment = self.create_student_base(
            tenant, 'Սոնա', 'Գասպարյան',
            date(2004, 5, 7), program, 2022, 5
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='is_remote_teacher_child',
            defaults={
                'value': 'True',
                'valid_from': date(2022, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 5, [73, 75, 77, 76, 78])
        self.apply_discount_and_payment(tenant, student, enrollment, 'TEACHER_CHILD', discount_rules)
    
    def create_student_14_multiple_discounts(self, tenant, programs, discount_rules):
  
        program = next((p for p in programs if p.code == 'ECON'), programs[13])
        student, enrollment = self.create_student_base(
            tenant, 'Աննա', 'Վարդանյան',
            date(2003, 3, 11), program, 2021, 7
        )
        
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='is_orphan',
            defaults={
                'value': 'True',
                'valid_from': date(2021, 9, 1),
                'is_active': True
            }
        )
        StudentAttribute.objects.get_or_create(
            student=student,
            attribute_type='social_score',
            defaults={
                'value': '35',
                'valid_from': date(2021, 9, 1),
                'is_active': True
            }
        )
        
        self.create_academic_records(student, 7, [70, 72, 74, 76, 78, 75, 77])
        self.apply_discount_and_payment(tenant, student, enrollment, 'ORPHAN', discount_rules)
        self.stdout.write('Իրավասու է նաև SOCIAL_HIGH (30%), բայց կիրառվում է max - ORPHAN (50%)')
    
    def create_student_15_no_discount(self, tenant, programs, discount_rules):

        program = next((p for p in programs if p.code == 'APPMATH'), programs[14])
        student, enrollment = self.create_student_base(
            tenant, 'Արա', 'Մելքոնյան',
            date(2005, 7, 19), program, 2023, 3
        )
        
        self.create_academic_records(student, 3, [60, 62, 64])
        self.apply_discount_and_payment(tenant, student, enrollment, None, discount_rules)