import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Անվանում')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Կոդ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Նկարագրություն')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Զեղչի կատեգորիա',
                'verbose_name_plural': 'Զեղչի կատեգորիաներ',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Անվանում')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Կոդ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Ֆակուլտետ',
                'verbose_name_plural': 'Ֆակուլտետներ',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Անուն')),
                ('last_name', models.CharField(max_length=50, verbose_name='Ազգանուն')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Էլ. փոստ')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Հեռախոս')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Ծննդյան ամսաթիվ')),
                ('enrollment_date', models.DateField(verbose_name='Ընդունման ամսաթիվ')),
                ('status', models.CharField(default='active', max_length=20, verbose_name='Կարգավիճակ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ուսանող',
                'verbose_name_plural': 'Ուսանողներ',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Անվանում')),
                ('domain', models.CharField(max_length=50, unique=True, verbose_name='Դոմեյն')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Համալսարան',
                'verbose_name_plural': 'Համալսարաններ',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DiscountRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Անվանում')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Կոդ')),
                ('percentage_min', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Նվազագույն %')),
                ('percentage_max', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Առավելագույն %')),
                ('priority', models.IntegerField(default=1, verbose_name='Առաջնահերթություն')),
                ('is_combinable', models.BooleanField(default=True, verbose_name='Համակցելի է')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Նկարագրություն')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.discountcategory', verbose_name='Կատեգորիա')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան')),
            ],
            options={
                'verbose_name': 'Զեղչի կանոն',
                'verbose_name_plural': 'Զեղչի կանոններ',
                'ordering': ['-priority'],
            },
        ),
        migrations.CreateModel(
            name='DiscountCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_type', models.CharField(max_length=50, verbose_name='Պայմանի տեսակ')),
                ('operator', models.CharField(max_length=10, verbose_name='Օպերատոր')),
                ('value', models.CharField(max_length=100, verbose_name='Արժեք')),
                ('is_required', models.BooleanField(default=True, verbose_name='Պարտադիր է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discount_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.discountrule', verbose_name='Զեղչի կանոն')),
            ],
            options={
                'verbose_name': 'Զեղչի պայման',
                'verbose_name_plural': 'Զեղչի պայմաններ',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Անվանում')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Կոդ')),
                ('base_tuition_fee', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Բազային վարձ')),
                ('duration_years', models.IntegerField(default=4, verbose_name='Տևողություն (տարի)')),
                ('free_seats', models.IntegerField(default=0, verbose_name='Անվճար տեղեր')),
                ('paid_seats', models.IntegerField(default=0, verbose_name='Վճարովի տեղեր')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.faculty', verbose_name='Ֆակուլտետ')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան')),
            ],
            options={
                'verbose_name': 'Մասնագիտություն',
                'verbose_name_plural': 'Մասնագիտություններ',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=20, verbose_name='Կիսամյակ')),
                ('payment_type', models.CharField(max_length=50, verbose_name='Վճարման տեսակ')),
                ('original_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Սկզբնական գումար')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Զեղչի գումար')),
                ('final_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Վերջնական գումար')),
                ('status', models.CharField(default='pending', max_length=20, verbose_name='Կարգավիճակ')),
                ('due_date', models.DateField(verbose_name='Վերջնաժամկետ')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='Վճարման ամսաթիվ')),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True, verbose_name='Վճարման եղանակ')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Գործարքի ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.student', verbose_name='Ուսանող')),
            ],
            options={
                'verbose_name': 'Վճարում',
                'verbose_name_plural': 'Վճարումներ',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_type', models.CharField(max_length=20, verbose_name='Տեղաբաշխման տեսակ')),
                ('current_semester', models.IntegerField(default=1, verbose_name='Ընթացիկ կիսամյակ')),
                ('entry_year', models.IntegerField(verbose_name='Ընդունման տարի')),
                ('status', models.CharField(default='active', max_length=20, verbose_name='Կարգավիճակ')),
                ('enrolled_date', models.DateField(verbose_name='Ընդունման ամսաթիվ')),
                ('graduation_date', models.DateField(blank=True, null=True, verbose_name='Ավարտի ամսաթիվ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.program', verbose_name='Մասնագիտություն')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.student', verbose_name='Ուսանող')),
            ],
            options={
                'verbose_name': 'Տեղաբաշխում',
                'verbose_name_plural': 'Տեղաբաշխումներ',
            },
        ),
        migrations.CreateModel(
            name='StudentAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_type', models.CharField(max_length=50, verbose_name='Հատկանիշի տեսակ')),
                ('value', models.CharField(max_length=200, verbose_name='Արժեք')),
                ('valid_from', models.DateField(verbose_name='Վավեր սկսած')),
                ('valid_to', models.DateField(blank=True, null=True, verbose_name='Վավեր մինչև')),
                ('document_reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Փաստաթուղթ')),
                ('verified_by', models.IntegerField(blank=True, null=True, verbose_name='Հաստատող')),
                ('verified_date', models.DateField(blank=True, null=True, verbose_name='Հաստատման ամսաթիվ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.student', verbose_name='Ուսանող')),
            ],
            options={
                'verbose_name': 'Ուսանողի հատկանիշ',
                'verbose_name_plural': 'Ուսանողի հատկանիշներ',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան'),
        ),
        migrations.AddField(
            model_name='discountcategory',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.tenant', verbose_name='Համալսարան'),
        ),
        migrations.CreateModel(
            name='AppliedDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=20, verbose_name='Կիսամյակ')),
                ('applied_percentage', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Կիրառված %')),
                ('approved_by', models.IntegerField(blank=True, null=True, verbose_name='Հաստատող')),
                ('applied_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Կիրառման ամսաթիվ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('discount_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.discountrule', verbose_name='Զեղչի կանոն')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.student', verbose_name='Ուսանող')),
            ],
            options={
                'verbose_name': 'Կիրառված զեղչ',
                'verbose_name_plural': 'Կիրառված զեղչեր',
                'unique_together': {('student', 'discount_rule', 'semester')},
            },
        ),
        migrations.CreateModel(
            name='AcademicRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=20, verbose_name='Կիսամյակ')),
                ('gpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='ՄԲ')),
                ('credits_earned', models.IntegerField(default=0, verbose_name='Վաստակած կրեդիտներ')),
                ('credits_total', models.IntegerField(default=0, verbose_name='Ընդհանուր կրեդիտներ')),
                ('academic_status', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ակադեմիական կարգավիճակ')),
                ('is_scholarship_eligible', models.BooleanField(default=False, verbose_name='Կրթաթոշակի իրավունք')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.student', verbose_name='Ուսանող')),
            ],
            options={
                'verbose_name': 'Ակադեմիական գրանցում',
                'verbose_name_plural': 'Ակադեմիական գրանցումներ',
                'unique_together': {('student', 'semester')},
            },
        ),
    ]
