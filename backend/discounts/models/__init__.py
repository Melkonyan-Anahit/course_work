from .tenant import Tenant
from .faculty import Faculty
from .program import Program
from .student import Student, Enrollment, AcademicRecord, StudentAttribute
from .discount import DiscountCategory, DiscountRule, DiscountCondition, AppliedDiscount
from .payment import Payment
from .system_settings import SystemSettings 

__all__ = [
    'Tenant',
    'Faculty',
    'Program',
    'Student',
    'Enrollment',
    'AcademicRecord',
    'StudentAttribute',
    'DiscountCategory',
    'DiscountRule',
    'DiscountCondition',
    'AppliedDiscount',
    'Payment',
    'SystemSettings', 
]