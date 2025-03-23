from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_view,projects_view,inventory_view, project_flow, project_details,custom_admin_view,maintenance_view, accept_order
from authentication.views import login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('projects/', projects_view, name='projects'),
    path('inventory/', inventory_view, name='inventory'),
    # path('profile/', profile_view, name='profile'),
    path('project-flow/', project_flow, name='project_flow'),
    path('project-details/<str:project_name>/', project_details, name='project_details'),
    path('admin_view/', custom_admin_view, name="custom_admin_view" ),
    path('accept-order/', accept_order, name="accept_order"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('maintenance/', maintenance_view, name="maintenance_view")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript')),
]
