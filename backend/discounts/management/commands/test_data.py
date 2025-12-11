from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from discounts.models import (
    Tenant, Faculty, Program, Student, Enrollment,
    AcademicRecord, StudentAttribute, DiscountCategory,
    DiscountRule, DiscountCondition, AppliedDiscount, 
    Payment, SystemSettings
)

class Command(BaseCommand):
    help = 'Ստեղծել test data - Tenant, Faculty, Programs, SystemSettings, Discounts'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Սկսում ենք test data ստեղծել...'))
    
        tenant = self.create_tenant()
        
        faculties = self.create_faculties(tenant)
    
        programs = self.create_programs(tenant, faculties)
        
        self.create_system_settings(tenant)
        
        categories = self.create_discount_categories(tenant)
    
        self.create_discount_rules(tenant, categories)
        
        self.stdout.write(self.style.SUCCESS('Test data հաջողությամբ ստեղծվեց!'))
    
    def create_tenant(self):
        tenant, created = Tenant.objects.get_or_create(
            domain='npua.am',
            defaults={
                'name': 'ՆՊՈՒԱ',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Tenant ստեղծվեց: {tenant.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Tenant-ը արդեն կա: {tenant.name}'))
        return tenant
    
    def create_faculties(self, tenant):
        faculties_data = [
            {'code': 'TXTIE', 'name': 'ՏՀՏԷ - Տեղեկատվական և հաղորդակցական տեխնոլոգիաների ու էլեկտրոնիկայի ինստիտուտ'},
            {'code': 'EEI', 'name': 'ԷԷ - Էներգետիկայի էլեկտրատեխնիկայի ինստիտուտ'},
            {'code': 'MMTHD', 'name': 'ՄՄԹՀԴ - Մեխանիկա մեքենաշինական, տրանսպորտային համակարգերի և դիզայնի ինստիտուտ'},
            {'code': 'LMQT', 'name': 'ԼՄՔՏ - Լեռնամետալուրգիայի և քիմիական տեխնոլոգիաների ինստիտուտ'},
            {'code': 'KMF', 'name': 'ԿՄՖ - Կիրառական մաթեմատիկայի և ֆիզիկայի ֆակուլտետ'},
            {'code': 'ITKF', 'name': 'ԻՏԿՖ - Ինժեներական տնտեսագիտության և կառավարման ֆակուլտետ'},
        ]
        
        faculties = []
        for data in faculties_data:
            faculty, created = Faculty.objects.get_or_create(
                tenant=tenant,
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'is_active': True
                }
            )
            faculties.append(faculty)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Faculty: {faculty.code}'))
        
        return faculties
    
    def create_programs(self, tenant, faculties):

        txtie = next((f for f in faculties if f.code == 'TXTIE'), None)
        eei = next((f for f in faculties if f.code == 'EEI'), None)
        mmthd = next((f for f in faculties if f.code == 'MMTHD'), None)
        lmqt = next((f for f in faculties if f.code == 'LMQT'), None)
        itkf = next((f for f in faculties if f.code == 'ITKF'), None)
        kmf = next((f for f in faculties if f.code == 'KMF'), None)
        
        all_programs = []
        
        if txtie:
            txtie_programs = [
                {'code': 'CS', 'name': 'Տվյալագիտություն', 'fee': 948000},
                {'code': 'SE', 'name': 'Ծրագրային ճարտարագիտություն', 'fee': 948000},
                {'code': 'CE', 'name': 'Համակարգչային ճարտարագիտություն', 'fee': 948000},
                {'code': 'CTN', 'name': 'Քոմփյութերային տեխնոլոգիաներ և ցանցեր', 'fee': 948000},
                {'code': 'IS', 'name': 'Տեղեկատվական համակարգեր', 'fee': 948000},
                {'code': 'AI', 'name': 'Արհեստական բանականությամբ համակարգեր', 'fee': 948000},
                {'code': 'IT', 'name': 'Տեղեկատվական տեխնոլոգիաներ', 'fee': 948000},
                {'code': 'INFOSEC', 'name': 'Տեղեկատվական անվտանգություն', 'fee': 948000},
                {'code': 'BLOCKCHAIN', 'name': 'Բլոկչեյն և Վեբ3 տեխնոլոգիաներ', 'fee': 948000},
                {'code': 'ELEC', 'name': 'Էլեկտրոնիկա', 'fee': 852000},
                {'code': 'RADIO', 'name': 'Ռադիոտեխնիկա', 'fee': 852000},
                {'code': 'TELECOM', 'name': 'Հեռահաղորդակցություն և ազդանշանների մշակում', 'fee': 852000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, txtie, txtie_programs))
        
        if eei:
            eei_programs = [
                {'code': 'THERMO', 'name': 'Ջերմաէներգետիկա', 'fee': 780000},
                {'code': 'NUCLEAR', 'name': 'Ատոմային էներգետիկա', 'fee': 780000},
                {'code': 'ELPOWER', 'name': 'Էլեկտրաէներգիա', 'fee': 780000},
                {'code': 'ELTECH', 'name': 'Էլեկտրատեխնիկա,էլեկտրամեխանիկա և էլեկտրատեխնոլոգիաներ', 'fee': 780000},
                {'code': 'ELDESIGN', 'name': 'Շինությունների էլեկտրամատակարարման քոմփյութերային նախագծում', 'fee': 780000},
                {'code': 'AUTO', 'name': 'Ավտոմատացում', 'fee': 852000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, eei, eei_programs))
        
        if mmthd:
            mmthd_programs = [
                {'code': 'ENVDESIGN', 'name': 'Միջավայրի դիզայն', 'fee': 780000},
                {'code': 'GRAPHDES', 'name': 'Գրաֆիկական դիզայն', 'fee': 780000},
                {'code': 'COMPGRAPH', 'name': 'Համակարգչային գրաֆիկա', 'fee': 780000},
                {'code': 'ROBOT', 'name': 'Ռոբոտատեխնիկա և մեխատրոնիկա', 'fee': 780000},
                {'code': 'MECHCAD', 'name': 'Մեխանիկական համակարգերի քոմփյութերային նախագծում', 'fee': 780000},
                {'code': 'MACH', 'name': 'Մեքենաշինություն և նյութերի մշակում', 'fee': 780000},
                {'code': 'CARS', 'name': 'Ավտոմոբիլներ', 'fee': 780000},
                {'code': 'TRANSPORT', 'name': 'Փոխադրումների և ճանապարհային երթևեկության կազմակերպում և կառավարում', 'fee': 780000},
                {'code': 'BIOMED', 'name': 'Կենսաբժշկական ճարտարագիտություն', 'fee': 780000},
                {'code': 'MEASURE', 'name': 'Չափիչ սարքավորումներ և համակարգեր', 'fee': 780000},
                {'code': 'AVIATION', 'name': 'Թռչող ապարատների ավիացիոն սարքավորումներ', 'fee': 852000},
                {'code': 'AEROSPACE', 'name': 'Ավիատիեզերական ճարտարագիտություն', 'fee': 852000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, mmthd, mmthd_programs))
        
        if lmqt:
            lmqt_programs = [
                {'code': 'CHEM', 'name': 'Քիմիական տեխնոլոգիա', 'fee': 780000},
                {'code': 'METAL', 'name': 'Մետալուրգիա', 'fee': 780000},
                {'code': 'MINING', 'name': 'Լեռնային գործ և օգտակար հանածոների արդյունահանում', 'fee': 780000},
                {'code': 'MINERALS', 'name': 'Օգտակար հանածոների հարստացում', 'fee': 780000},
                {'code': 'ENVPROT', 'name': 'Շրջակա միջավայրի պահպանություն', 'fee': 780000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, lmqt, lmqt_programs))
        
        if itkf:
            itkf_programs = [
                {'code': 'ECON', 'name': 'Տնտեսագիտություն', 'fee': 852000},
                {'code': 'MGMT', 'name': 'Կառավարում (ըստ ոլորտի)', 'fee': 852000},
                {'code': 'LOG', 'name': 'Լոգիստիկա', 'fee': 852000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, itkf, itkf_programs))
        
        if kmf:
            kmf_programs = [
                {'code': 'APPMATH', 'name': 'Ինֆորմատիկա և կիրառական մաթեմատիկա', 'fee': 948000},
                {'code': 'SEMICOND', 'name': 'Կիսսահաղորդիչների ֆիզիկա և միկրոէլեկտրոնիկա', 'fee': 852000},
                {'code': 'COMPLIN', 'name': 'Հաշվողական լեզվաբանություն', 'fee': 780000},
            ]
            all_programs.extend(self._create_programs_for_faculty(tenant, kmf, kmf_programs))
        
        return all_programs
    
    def _create_programs_for_faculty(self, tenant, faculty, programs_data):
        created_programs = []
        for data in programs_data:
            program, created = Program.objects.get_or_create(
                tenant=tenant,
                faculty=faculty,
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'base_tuition_fee': data['fee'],
                    'duration_years': 4,
                    'free_seats': 25,
                    'paid_seats': 100,
                    'is_active': True
                }
            )
            created_programs.append(program)
            if created:
                self.stdout.write(self.style.SUCCESS(f'{faculty.code} | {program.code} - {program.name} ({program.base_tuition_fee:,} դրամ)'))
        return created_programs
    
    def create_system_settings(self, tenant):
        settings_data = [
            {'key': 'gpa_excellent', 'value': '81', 'type': 'int', 'desc': 'Գերազանց ուսանողի ՄՕԳ սահմանը'},
            {'key': 'gpa_scholarship_min', 'value': '60', 'type': 'int', 'desc': 'Նպաստի համար ՄՕԳ սահմանը'},
            {'key': 'social_score_threshold', 'value': '30', 'type': 'int', 'desc': 'Սոցիալական գնահատականի սահմանը'},
            {'key': 'age_orphan_min', 'value': '18', 'type': 'int', 'desc': 'Որբի նվազագույն տարիք'},
            {'key': 'age_orphan_max', 'value': '23', 'type': 'int', 'desc': 'Որբի առավելագույն տարիք'},
            {'key': 'family_children_min', 'value': '3', 'type': 'int', 'desc': 'Բազմազավակ ընտանիքի նվազագույն երեխաների թիվ'},
            {'key': 'work_years_30_percent', 'value': '3', 'type': 'int', 'desc': 'Աշխատանքային ստաժ 30% զեղչի համար'},
            {'key': 'work_years_50_percent', 'value': '5', 'type': 'int', 'desc': 'Աշխատանքային ստաժ 50% զեղչի համար'},
        ]
        
        for data in settings_data:
            setting, created = SystemSettings.objects.get_or_create(
                tenant=tenant,
                setting_key=data['key'],
                defaults={
                    'setting_value': data['value'],
                    'value_type': data['type'],
                    'description': data['desc'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Setting: {setting.setting_key} = {setting.setting_value}'))
    
    def create_discount_categories(self, tenant):
        categories_data = [
            {'code': 'SOCIAL', 'name': 'Սոցիալական'},
            {'code': 'ACADEMIC', 'name': 'Ակադեմիական'},
            {'code': 'WORK', 'name': 'Աշխատանքային'},
            {'code': 'FAMILY', 'name': 'Ընտանեկան'},
            {'code': 'SPECIAL', 'name': 'Հատուկ'},
        ]
        
        categories = []
        for data in categories_data:
            category, created = DiscountCategory.objects.get_or_create(
                tenant=tenant,
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category: {category.code} - {category.name}'))
        
        return categories
    
    def create_discount_rules(self, tenant, categories):
        social = next((c for c in categories if c.code == 'SOCIAL'), None)
        academic = next((c for c in categories if c.code == 'ACADEMIC'), None)
        work = next((c for c in categories if c.code == 'WORK'), None)
        family = next((c for c in categories if c.code == 'FAMILY'), None)
        special = next((c for c in categories if c.code == 'SPECIAL'), None)
        
        rules_data = [
            {'code': 'SOCIAL_HIGH', 'name': 'Սոցիալապես անապահով (բարձր)', 'category': social, 'min': 30, 'max': 30, 'priority': 5},
            {'code': 'SOCIAL_LOW', 'name': 'Սոցիալապես անապահով (ցածր)', 'category': social, 'min': 20, 'max': 20, 'priority': 4},
            {'code': 'ORPHAN', 'name': 'Որբեր 18-23 տարեկան', 'category': social, 'min': 50, 'max': 50, 'priority': 10},
            {'code': 'SINGLE_PARENT', 'name': 'Միակողմանի ծնողազուրկ', 'category': social, 'min': 50, 'max': 50, 'priority': 10},
            {'code': 'YOUNG_PARENT', 'name': 'Մինչև 1 տարեկան երեխա ունեցող', 'category': family, 'min': 50, 'max': 50, 'priority': 9},
            {'code': 'LARGE_FAMILY', 'name': '3+ երեխա ունեցող ընտանիք', 'category': family, 'min': 30, 'max': 30, 'priority': 6},
            {'code': 'DISABILITY', 'name': '1-2 խմբի հաշմանդամ ծնող', 'category': social, 'min': 30, 'max': 30, 'priority': 7},
            {'code': 'MILITARY', 'name': 'Մարտական հերթապահություն', 'category': special, 'min': 30, 'max': 30, 'priority': 7},
            {'code': 'SCHOLARSHIP_MISS', 'name': '0.1 միավորով զրկված նպաստից', 'category': academic, 'min': 50, 'max': 50, 'priority': 8},
            {'code': 'NPUA_SIBLINGS', 'name': '2+ ուսանող երեխա ՆՊՈՒԱ-ում', 'category': family, 'min': 20, 'max': 20, 'priority': 5},
            {'code': 'TEACHER_CHILD', 'name': 'Հեռավոր դպրոցի ուսուցչի երեխա', 'category': special, 'min': 30, 'max': 30, 'priority': 6},
            {'code': 'EXCELLENT_4SEM', 'name': '4+ կիսամյակ գերազանց', 'category': academic, 'min': 35, 'max': 35, 'priority': 8},
            {'code': 'WORK_3_5Y', 'name': 'ՆՊՈՒԱ-ում 3-5 տարի աշխատած', 'category': work, 'min': 30, 'max': 30, 'priority': 6},
            {'code': 'WORK_5Y_PLUS', 'name': 'ՆՊՈՒԱ-ում 5+ տարի աշխատած', 'category': work, 'min': 50, 'max': 50, 'priority': 9},
            {'code': 'PARENT_WORK_5_15Y', 'name': 'Ծնողը ՆՊՈՒԱ-ում 5-15 տարի', 'category': work, 'min': 50, 'max': 50, 'priority': 9},
            {'code': 'PARENT_WORK_15Y_PLUS', 'name': 'Ծնողը ՆՊՈՒԱ-ում 15+ տարի', 'category': work, 'min': 60, 'max': 60, 'priority': 10},
            {'code': 'COUNCIL_DECISION', 'name': 'Գիտական խորհրդի որոշում', 'category': special, 'min': 20, 'max': 50, 'priority': 5},
        ]
        
        for data in rules_data:
            if data['category']:
                rule, created = DiscountRule.objects.get_or_create(
                    tenant=tenant,
                    code=data['code'],
                    defaults={
                        'category': data['category'],
                        'name': data['name'],
                        'percentage_min': data['min'],
                        'percentage_max': data['max'],
                        'priority': data['priority'],
                        'is_combinable': False,  
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Rule: {rule.code} ({rule.percentage_min}%)'))