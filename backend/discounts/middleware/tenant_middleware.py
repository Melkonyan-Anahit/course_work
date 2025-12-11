from threading import local
from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()

def get_current_tenant():
    return getattr(_thread_locals, 'tenant', None)


def set_current_tenant(tenant):
    _thread_locals.tenant = tenant

class TenantMiddleware(MiddlewareMixin):

    def process_request(self, request):
        from discounts.models import Tenant
        
        tenant_id = request.session.get('tenant_id')
        
        if tenant_id:
            try:
                tenant = Tenant.objects.get(id=tenant_id, is_active=True)
                set_current_tenant(tenant)
            except Tenant.DoesNotExist:
               
                tenant = Tenant.objects.filter(is_active=True).first()
                set_current_tenant(tenant)
                if tenant:
                    request.session['tenant_id'] = tenant.id
        else:
            tenant = Tenant.objects.filter(is_active=True).first()
            set_current_tenant(tenant)
            if tenant:
                request.session['tenant_id'] = tenant.id
    
    def process_response(self, request, response):
        if hasattr(_thread_locals, 'tenant'):
            del _thread_locals.tenant
        return response