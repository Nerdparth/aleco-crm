from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_view,projects_view,inventory_view, project_flow, project_details,custom_admin_view,maintenance_view
from authentication.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('projects/', projects_view, name='projects'),
    path('inventory/', inventory_view, name='inventory'),
    # path('profile/', profile_view, name='profile'),
    path('project-flow/', project_flow, name='project_flow'),
    path('project-details/<str:project_name>/', project_details, name='project_details'),
    path('admin_view/', custom_admin_view, name="custom_admin_view" ),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('maintenance/', maintenance_view, name="maintenance_view")
]
