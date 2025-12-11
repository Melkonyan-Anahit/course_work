from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter  # ← Ավելացրու ChoiceDropdownFilter
from django.conf import settings
from .models import (
    Tenant, Faculty, Program, Student, Enrollment, 
    AcademicRecord, StudentAttribute, DiscountCategory,
    DiscountRule, DiscountCondition, AppliedDiscount, Payment,
    SystemSettings
)
admin.site.site_header = 'Ադմինիստրացիա'
admin.site.site_title = 'ՆՊՈՒԱ - Զեղչերի համակարգ'
admin.site.index_title = 'Կառավարման վահանակ'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name']
    ordering = ['code']
    
    def has_module_permission(self, request):
        return request.user.is_superuser
    
    def save_model(self, request, obj, form, change):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        if not obj.tenant_id:
            current_tenant = get_current_tenant()
            if current_tenant:
                obj.tenant = current_tenant
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        qs = super().get_queryset(request)
        current_tenant = get_current_tenant()
        if current_tenant:
            qs = qs.filter(tenant=current_tenant)
        return qs

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty', 'base_tuition_fee', 'free_seats', 'paid_seats']
    list_filter = ['faculty', 'is_active']
    search_fields = ['code', 'name']
    ordering = ['code']
    
    def has_module_permission(self, request):
        return request.user.is_superuser
    
    def save_model(self, request, obj, form, change):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        if not obj.tenant_id:
            current_tenant = get_current_tenant()
            if current_tenant:
                obj.tenant = current_tenant
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        qs = super().get_queryset(request)
        current_tenant = get_current_tenant()
        if current_tenant:
            qs = qs.filter(tenant=current_tenant)
        return qs



# ========== CUSTOM FILTERS ==========

# ========== CUSTOM FILTERS ==========

class CourseFilter(admin.SimpleListFilter):
    """Կուրսերի ֆիլտր (1-4 կուրս)"""
    title = 'Կուրս'
    parameter_name = 'course'
    
    def lookups(self, request, model_admin):
        return (
            ('1', '1 կուրս'),
            ('2', '2 կուրս'),
            ('3', '3 կուրս'),
            ('4', '4 կուրս'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(enrollment__current_semester__in=[1, 2])
        elif self.value() == '2':
            return queryset.filter(enrollment__current_semester__in=[3, 4])
        elif self.value() == '3':
            return queryset.filter(enrollment__current_semester__in=[5, 6])
        elif self.value() == '4':
            return queryset.filter(enrollment__current_semester__in=[7, 8])
        return queryset

# ========== ADMIN CLASSES ==========

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'display_id', 
        'full_name', 
        'get_program',
        'get_course',
        'get_base_tuition',
        'get_discount_percentage',
        'get_final_tuition'
    ]
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_filter = [
        ('enrollment__program', RelatedDropdownFilter),  # Dropdown - Մասնագիտություն
        CourseFilter,  # Dropdown - Կուրս (1-4)
        'status',
        'is_active',
    ]
    ordering = ['id']
    
    def display_id(self, obj):
        return obj.display_id
    display_id.short_description = 'ID'
    
    def get_program(self, obj):
        """Մասնագիտություն"""
        enrollment = obj.enrollment_set.first()
        return enrollment.program.name if enrollment else '-'
    get_program.short_description = 'Մասնագիտություն'
    
    def get_course(self, obj):
        """Կուրս (1-4)"""
        enrollment = obj.enrollment_set.first()
        if enrollment:
            # Կիսամյակ → Կուրս (1-2 = 1, 3-4 = 2, 5-6 = 3, 7-8 = 4)
            course = (enrollment.current_semester + 1) // 2
            return f'{course} կուրս'
        return '-'
    get_course.short_description = 'Կուրս'
    
    def get_base_tuition(self, obj):
        """Սկզբնական վարձ"""
        enrollment = obj.enrollment_set.first()
        if enrollment:
            return f'{int(enrollment.program.base_tuition_fee):,} ֏'
        return '-'
    get_base_tuition.short_description = 'Սկզբնական վարձ'
    
    def get_discount_percentage(self, obj):
        """Զեղչ %"""
        discount = obj.applieddiscount_set.filter(is_active=True).first()
        if discount:
            return f'{int(discount.applied_percentage)}%'
        return '0%'
    get_discount_percentage.short_description = 'Զեղչ'
    
    def get_final_tuition(self, obj):
        """Վերջնական վարձ"""
        payment = obj.payment_set.first()
        if payment:
            return f'{int(payment.final_amount):,} ֏'
        return '-'
    get_final_tuition.short_description = 'Վերջնական վարձ'
    
    def get_queryset(self, request):
        """Optimize queries"""
        qs = super().get_queryset(request)
        qs = qs.select_related('tenant')
        qs = qs.prefetch_related(
            'enrollment_set__program__faculty',
            'applieddiscount_set__discount_rule',
            'payment_set'
        )
        return qs
    
    def changelist_view(self, request, extra_context=None):
        """Փոխել list view-ի վերնագիրը"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Ուսանողների պատմություն'
        return super().changelist_view(request, extra_context)

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'gpa', 'credits_earned', 'credits_total', 'academic_status']
    list_filter = ['semester', 'academic_status', 'is_scholarship_eligible']
    search_fields = ['student__first_name', 'student__last_name', 'semester']
    ordering = ['-semester', 'student']

@admin.register(StudentAttribute)
class StudentAttributeAdmin(admin.ModelAdmin):
    list_display = ['student', 'attribute_type', 'value', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['attribute_type', 'is_active', 'valid_from']
    search_fields = ['student__first_name', 'student__last_name', 'attribute_type', 'value']
    ordering = ['student', 'attribute_type']

@admin.register(DiscountCategory)
class DiscountCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'tenant', 'is_active']
    search_fields = ['name', 'code']
    list_filter = ['tenant', 'is_active']
    ordering = ['code']

# ========== INLINE CLASSES ==========

class DiscountConditionInline(admin.TabularInline):
    model = DiscountCondition
    extra = 1  # Քանի՞ դատարկ տող ցույց տալ
    fields = ['condition_type', 'operator', 'value', 'is_required']
    verbose_name = 'Պայման'
    verbose_name_plural = 'Պայմաններ'

@admin.register(DiscountRule)
class DiscountRuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'percentage_min', 'percentage_max', 'priority', 'is_combinable', 'is_active']
    list_filter = ['category', 'tenant', 'is_active', 'is_combinable']
    search_fields = ['code', 'name']
    ordering = ['-priority', 'code']
    inlines = [DiscountConditionInline]


@admin.register(AppliedDiscount)
class AppliedDiscountAdmin(admin.ModelAdmin):
    list_display = ['student', 'discount_rule', 'semester', 'applied_percentage', 'applied_date', 'is_active']
    list_filter = ['semester', 'is_active', 'discount_rule__category']
    search_fields = ['student__first_name', 'student__last_name', 'discount_rule__code']
    ordering = ['-applied_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'payment_type', 'original_amount', 'discount_amount', 'final_amount', 'status', 'due_date']
    list_filter = ['semester', 'status', 'payment_type', 'payment_method']
    search_fields = ['student__first_name', 'student__last_name', 'transaction_id']
    ordering = ['-created_at']
    
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['setting_key', 'setting_value', 'value_type', 'description', 'is_active']
    list_filter = ['value_type', 'is_active']
    search_fields = ['setting_key', 'description']
    ordering = ['setting_key']
    
    fieldsets = (
        ('Հիմնական', {
            'fields': ('setting_key', 'setting_value', 'value_type')
        }),
        ('Լրացուցիչ', {
            'fields': ('description', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        if not obj.tenant_id:
            current_tenant = get_current_tenant()
            if current_tenant:
                obj.tenant = current_tenant
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        from discounts.middleware.tenant_middleware import get_current_tenant
        
        qs = super().get_queryset(request)
        current_tenant = get_current_tenant()
        if current_tenant:
            qs = qs.filter(tenant=current_tenant)
        return qs