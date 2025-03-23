from django.shortcuts import render, redirect, get_object_or_404
from .models import Projects, Inventory, Progress, InventoryHistory, MaintenanceMode, RecentActivity
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

def dashboard_view(request):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    three_days_ago = timezone.now() - timedelta(days=5)
    RecentActivity.objects.filter(timestamp__lt=three_days_ago).delete()
    recent_activity = RecentActivity.objects.all().order_by('-timestamp')
    projects = Projects.objects.filter(is_active = True)
    active_projects_count = len(projects)
    meseaurements_pending_getter = Projects.objects.filter(is_active = True, stage1 = False, stage2 = False, stage3 = False, stage4 = False, stage5 = False, stage6 = False, stage7 = False, stage8 = False, stage9 = False)
    measurements_pending_count = len(meseaurements_pending_getter)
    cutting_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = False, stage3 = False, stage4 = False, stage5 = False, stage6 = False, stage7 = False, stage8 = False, stage9 = False)
    cutting_pending_count = len(cutting_pending_getter)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    measurements_completed_count = active_projects_count - measurements_pending_count
    cutting_completed_count = active_projects_count - cutting_pending_count
    context = {
        "active_projects_count": active_projects_count,
    "measurements_pending_count": measurements_pending_count,
    "cutting_pending_count": cutting_pending_count,
    "orders_pending_count": orders_pending_count,
    "measurements_completed_count": measurements_completed_count,
    "cutting_completed_count": cutting_completed_count,
    "pending_orders_list" : orders_pending_getter,
    "recent_activity" : recent_activity
    }
    return render(request, 'dashboard.html', context )


def projects_view(request):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    projects_getter = Projects.objects.filter(is_active=True)
    projects = []

    for project in projects_getter:
        if project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7 and project.stage8:
            stage = 9
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7:
            stage = 8
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6:
            stage = 7
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5:
            stage = 6
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4:
            stage = 5
        elif project.stage1 and project.stage2 and project.stage3:
            stage = 4
        elif project.stage1 and project.stage2:
            stage = 3
        elif project.stage1 and project.stage2:
            stage = 2
        else:
            stage = 1  # No stages completed

        progress = stage * 11.11

        projects.append({
            'name': project.name,
            'description': project.description,
            'stage': stage,
            'address': project.address,
            'progress': progress,
            'created_at': project.created_at
        })

    return render(request, 'projects.html', {'projects': projects, 'orders_pending_count' : orders_pending_count, "pending_orders_list" : orders_pending_getter})


def inventory_view(request):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    items_getter = Inventory.objects.all()
    items = []
    low = []
    total_items_quantity = 0
    out_of_stock = []
    for item in items_getter:
        if item.quantity == 0:
            out_of_stock.append(item)
            items.append({
                'name': item.name,
                'brand': item.brand,
                'quantity': item.quantity,
                'status': 'out_of_stock',
                'id' : item.id
            })

        elif item.quantity < 10:
            total_items_quantity += item.quantity
            low.append(item)
            items.append({
                'name': item.name,
                'brand': item.brand,
                'quantity': item.quantity,
                'status': 'low',
                'id' : item.id
            })
        
        else:
            total_items_quantity += item.quantity
            items.append({
                'name': item.name,
                'brand': item.brand,
                'quantity': item.quantity,
                'status': 'optimal',
                'id' : item.id
            })
    
    out_of_stock_count = len(out_of_stock)
    low_count = len(low)

    if request.method == 'POST':
        if "add_item" in request.POST:
            name = request.POST.get('name')
            brand = request.POST.get('brand')
            quantity = request.POST.get('quantity')

            Inventory.objects.create(name=name,brand=brand, quantity=quantity)
            return redirect("inventory")
        if "delete_item" in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(Inventory, id=item_id)
            item.delete()
            return redirect("inventory")
        if "edit_item" in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(Inventory, id=item_id)
            item.name = request.POST.get('name')
            item.brand = request.POST.get('brand')
            item.quantity = request.POST.get('quantity')
            item.save()
            return redirect("inventory")
    return render(request, 'inventory.html', {'items': items,'out_of_stock_count': out_of_stock_count, 'low_count': low_count, 'total_items_quantity': total_items_quantity, 'orders_pending_count' : orders_pending_count, "pending_orders_list" : orders_pending_getter})


def maintenance_view(request):
    maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
    if maintenance_mode == False:
        return redirect("dashboard")
    user = request.user
    if user.is_authenticated:
        return redirect ("custom_admin_view")
    return render(request, 'maintenance.html')


def project_flow(request):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    projects_getter = Projects.objects.filter(is_active=True)
    projects = []
    for project in projects_getter:
        progress = Progress.objects.get(project=project)
        stage1_progress_percentage = int((progress.stage1_window * 100) / project.windows)
        stage2_progress_percentage = int((progress.stage2_window * 100) / project.windows)
        stage3_progress_percentage = int((progress.stage3_window * 100) / project.windows)
        stage4_progress_percentage = int((progress.stage4_window * 100) / project.windows)
        stage5_progress_percentage = int((progress.stage5_window * 100) / project.windows)
        stage6_progress_percentage = int((progress.stage6_window * 100) / project.windows)
        stage7_progress_percentage = int((progress.stage7_window * 100) / project.windows)
        stage8_progress_percentage = int((progress.stage8_window * 100) / project.windows)
        stage9_progress_percentage = int((progress.stage9_window * 100) / project.windows)

        if project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7 and project.stage8:
            stage = 9
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7:
            stage = 8
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6:
            stage = 7
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5:
            stage = 6
        elif project.stage1 and project.stage2 and project.stage3 and project.stage4:
            stage = 5
        elif project.stage1 and project.stage2 and project.stage3:
            stage = 4
        elif project.stage1 and project.stage2:
            stage = 3
        elif project.stage1:
            stage = 2
        else:
            stage = 1  # No stages completed
        projects.append({
            'name': project.name,
            'stage1_window': progress.stage1_window,
            'stage2_window': progress.stage2_window,
            'stage3_window': progress.stage3_window,
            'stage4_window': progress.stage4_window,
            'stage5_window': progress.stage5_window,
            'stage6_window': progress.stage6_window,
            'stage7_window': progress.stage7_window,
            'stage8_window': progress.stage8_window,
            'stage9_window': progress.stage9_window,
            'address': project.address,
            'created_at': project.created_at,
            'windows' : project.windows,
            'id' : project.id,
            'stage1_completion_date' : project.stage1_date,
            'stage1_completion_status' : project.stage1,
            'stage2_completion_date' : project.stage2_date,
            'stage2_completion_status' : project.stage2,
            'stage3_completion_date' : project.stage3_date,
            'stage3_completion_status' : project.stage3,
            'stage4_completion_date' : project.stage4_date,
            'stage4_completion_status' : project.stage4,
            'stage5_completion_date' : project.stage5_date,
            'stage5_completion_status' : project.stage5,
            'stage6_completion_date' : project.stage6_date,
            'stage6_completion_status' : project.stage6,
            'stage7_completion_date' : project.stage7_date,
            'stage7_completion_status' : project.stage7,
            'stage8_completion_date' : project.stage8_date,
            'stage8_completion_status' : project.stage8,
            'stage9_completion_date' : project.stage9_date,
            'stage9_completion_status' : project.stage9,
            'stage1_progress_percentage' : stage1_progress_percentage,
            'stage2_progress_percentage' : stage2_progress_percentage,
            'stage3_progress_percentage' : stage3_progress_percentage,
            'stage4_progress_percentage' : stage4_progress_percentage,
            'stage5_progress_percentage' : stage5_progress_percentage,
            'stage6_progress_percentage' : stage6_progress_percentage,
            'stage7_progress_percentage' : stage7_progress_percentage,
            'stage8_progress_percentage' : stage8_progress_percentage,
            'stage9_progress_percentage' : stage9_progress_percentage,
            'current_stage' : stage
        })


    if request.method == 'POST':
        if "stage1_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage1 = True
            project_update.stage1_date = timezone.now().date()
            project_update.save()
            progress_update.stage1_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "measurement")
            return redirect("project_flow")
        if "stage2_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage2 = True
            project_update.stage2_date = timezone.now().date()
            project_update.save()
            progress_update.stage2_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "cutting frames")
            return redirect("project_flow")
        if "stage3_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage3 = True
            project_update.stage3_date = timezone.now().date()
            project_update.save()
            progress_update.stage3_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "cutting sashes")
            return redirect("project_flow")
        if "stage4_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage4 = True
            project_update.stage4_date = timezone.now().date()
            project_update.save()
            progress_update.stage4_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "jalli palle")
            return redirect("project_flow")
        if "stage5_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage5 = True
            project_update.stage5_date = timezone.now().date()
            project_update.save()
            progress_update.stage5_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "assembled")
            return redirect("project_flow")
        if "stage6_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage6 = True
            project_update.stage6_date = timezone.now().date()
            project_update.save()
            progress_update.stage6_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "packed")
            return redirect("project_flow")
        if "stage7_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage7 = True
            project_update.stage7_date = timezone.now().date()
            project_update.save()
            progress_update.stage7_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "beading")
            return redirect("project_flow")
        if "stage8_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage8 = True
            project_update.stage8_date = timezone.now().date()
            project_update.save()
            progress_update.stage8_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "delivered")
            return redirect("project_flow")
        if "stage9_complete" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            project_update.stage9 = True
            project_update.stage9_date = timezone.now().date()
            project_update.save()
            progress_update.stage9_window = project_update.windows
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "installation")
            return redirect("project_flow")
        if "edit_stage1" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage1_window = request.POST.get('stage1_window')
            progress_update.save()
            print(progress_update.stage1_window)
            print(project_update.windows)
            print(progress_update.stage1_window == project_update.windows)
            if int(progress_update.stage1_window) == int(project_update.windows):
                project_update.stage1 = True
            project_update.stage1_date = timezone.now().date()
            project_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "measurement")
            return redirect("project_flow")
        if "edit_stage2" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage2_window = request.POST.get('stage2_window')
            progress_update.save()
            if int(progress_update.stage2_window) == int(project_update.windows):
                project_update.stage2 = True
            project_update.stage2_date = timezone.now().date()
            project_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "cutting frames")
            return redirect("project_flow")
        if "edit_stage3" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage3_window = request.POST.get('stage3_window')
            progress_update.save()
            if int(progress_update.stage3_window) == int(project_update.windows):
                project_update.stage3 = True
            project_update.stage3_date = timezone.now().date()
            project_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "cutting sashes")
            return redirect("project_flow")
        if "edit_stage4" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage4_window = request.POST.get('stage4_window')
            project_update.save()
            if int(progress_update.stage4_window) == int(project_update.windows):
                project_update.stage4 = True
            project_update.stage4_date = timezone.now().date()
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "jalli palle")
            return redirect("project_flow")
        if "edit_stage5" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage5_window = request.POST.get('stage5_window')
            project_update.save()
            if int(progress_update.stage5_window) == int(project_update.windows):
                project_update.stage5 = True
            project_update.stage5_date = timezone.now().date()
            
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "assembled")
            return redirect("project_flow")
        if "edit_stage6" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage6_window = request.POST.get('stage6_window')
            project_update.save()
            if int(progress_update.stage6_window) == int(project_update.windows):
                project_update.stage6 = True
            project_update.stage6_date = timezone.now().date()
            
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "packed")
            return redirect("project_flow")
        if "edit_stage7" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage7_window = request.POST.get('stage7_window')
            project_update.save()
            if int(progress_update.stage7_window) == int(project_update.windows):
                project_update.stage7 = True
            project_update.stage7_date = timezone.now().date()
            
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "beading")
            return redirect("project_flow")
        if "edit_stage8" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage8_window = request.POST.get('stage8_window')
            project_update.save()
            if int(progress_update.stage8_window) == int(project_update.windows):
                project_update.stage8 = True
            project_update.stage8_date = timezone.now().date()
            
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "delivered")
            return redirect("project_flow")
        if "edit_stage9" in request.POST:
            project_id = request.POST.get('project_id')
            project_update = get_object_or_404(Projects, id=project_id)
            progress_update = get_object_or_404(Progress, project=project_update)
            progress_update.stage9_window = request.POST.get('stage9_window')
            project_update.save()
            if int(progress_update.stage9_window) == int(project_update.windows):
                project_update.stage9 = True
            project_update.stage9_date = timezone.now().date()
            
            progress_update.save()
            RecentActivity.objects.create(site = project_update, activity_type = "installation")
            return redirect("project_flow")
    return render(request, 'project-flow.html', {'projects': projects,'orders_pending_count' : orders_pending_count, "pending_orders_list" : orders_pending_getter})


def project_details(request, project_name):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    project = get_object_or_404(Projects, name=project_name)
    progress = Progress.objects.get(project=project)
    stage1_progress_percentage = int((progress.stage1_window * 100) / project.windows)
    stage2_progress_percentage = int((progress.stage2_window * 100) / project.windows)
    stage3_progress_percentage = int((progress.stage3_window * 100) / project.windows)
    stage4_progress_percentage = int((progress.stage4_window * 100) / project.windows)
    stage5_progress_percentage = int((progress.stage5_window * 100) / project.windows)
    stage6_progress_percentage = int((progress.stage6_window * 100) / project.windows)
    stage7_progress_percentage = int((progress.stage7_window * 100) / project.windows)
    stage8_progress_percentage = int((progress.stage8_window * 100) / project.windows)
    stage9_progress_percentage = int((progress.stage9_window * 100) / project.windows)
    if project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7 and project.stage8:
            current_stage = 9
    elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6 and project.stage7:
            current_stage = 8
    elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5 and project.stage6:
            current_stage = 7
    elif project.stage1 and project.stage2 and project.stage3 and project.stage4 and project.stage5:
            current_stage = 6
    elif project.stage1 and project.stage2 and project.stage3 and project.stage4:
            current_stage = 5
    elif project.stage1 and project.stage2 and project.stage3:
            current_stage = 4
    elif project.stage1 and project.stage2:
            current_stage = 3
    elif project.stage1:
            current_stage = 2
    else:
            current_stage = 1
    inventory_history_getter = InventoryHistory.objects.filter(given_to=project)
    inventory_history = []
    for item in inventory_history_getter:
        item_name_getter = get_object_or_404(Inventory, name = item.inventory.name )
        item_name = item_name_getter.name
        inventory_history.append({
            'item_name' : item_name,
            'item_quantity' : item.quantity,
            'item_bought_date' : item.date
        })
    if len(inventory_history_getter) == 0:
        inventory_history = False
    context = {
        'project': project,
        'stage1_progress_percentage': stage1_progress_percentage,
        'stage2_progress_percentage': stage2_progress_percentage,
        'stage3_progress_percentage': stage3_progress_percentage,
        'stage4_progress_percentage': stage4_progress_percentage,
        'stage5_progress_percentage': stage5_progress_percentage,
        'stage6_progress_percentage': stage6_progress_percentage,
        'stage7_progress_percentage': stage7_progress_percentage,
        'stage8_progress_percentage': stage8_progress_percentage,
        'stage9_progress_percentage': stage9_progress_percentage,
        'current_stage': current_stage,
        'inventory_history': inventory_history,
        'last_updated_date' : getattr(project, f'stage{current_stage - 1}_date'),
        'orders_pending_count' : orders_pending_count,
        "pending_orders_list" : orders_pending_getter
    }
    
    return render(request, 'project-details.html', context)


def custom_admin_view(request):
    user = request.user
    if not user.is_authenticated:
        maintenance_mode = MaintenanceMode.objects.get(id=1).maintenace_mode
        if maintenance_mode == True:
            return redirect(maintenance_view)
    orders_pending_getter = Projects.objects.filter(is_active = True, stage1 = True, stage2 = True, stage3 = True, stage4 = True, stage5 = True, stage6 = False, stage7 = False, stage8 = False, stage9 = False, is_ordered = False)
    orders_pending_count = len(orders_pending_getter)
    maintenance_mode_getter = MaintenanceMode.objects.get(id=1).maintenace_mode
    sites_getter = Projects.objects.all()
    sites = []
    for site in sites_getter:
        if site.stage1 and site.stage2 and site.stage3 and site.stage4 and site.stage5 and site.stage6 and site.stage7 and site.stage8:
            current_stage = 8
        elif site.stage1 and site.stage2 and site.stage3 and site.stage4 and site.stage5 and site.stage6 and site.stage7:
            current_stage = 7
        elif site.stage1 and site.stage2 and site.stage3 and site.stage4 and site.stage5 and site.stage6:
            current_stage = 6
        elif site.stage1 and site.stage2 and site.stage3 and site.stage4 and site.stage5:
            current_stage = 5
        elif site.stage1 and site.stage2 and site.stage3 and site.stage4:
            current_stage = 4
        elif site.stage1 and site.stage2 and site.stage3:
            current_stage = 3
        elif site.stage1 and site.stage2:
            current_stage = 2
        elif site.stage1:
            current_stage = 1
        else:
            current_stage = 1
        sites.append({
            "id" : site.id,
            "name" : site.name,
            "current_stage" : current_stage,
            "is_active" : site.is_active
        })
    items = Inventory.objects.filter(quantity__gt = 0)
    if request.method == 'POST':
        if "maintenance_mode" in request.POST:
            maintenance_mode = request.POST.get('maintenance_mode')
            print(maintenance_mode)
            if maintenance_mode == "on":
                maintenance_mode_updater = MaintenanceMode.objects.get(id=1)
                maintenance_mode_updater.maintenace_mode = True
                maintenance_mode_updater.save()
                return redirect("custom_admin_view") 
            if maintenance_mode == "off":
                maintenance_mode_updater = MaintenanceMode.objects.get(id=1)
                maintenance_mode_updater.maintenace_mode = False
                maintenance_mode_updater.save()
                return redirect("custom_admin_view")
        if "create_site" in request.POST:
            site_name = request.POST.get("site_name")
            site_address = request.POST.get("site_address")
            site_description = request.POST.get("site_description")
            total_windows = request.POST.get("total_windows")
            project = Projects.objects.create(name = site_name, description = site_description, windows = total_windows, address = site_address)
            Progress.objects.create(project = project)
            RecentActivity.objects.create(site = project, activity_type = "new-site")
            return redirect("custom_admin_view")
        if "assign_resources" in  request.POST:
            site_id = request.POST.get('resource_site')
            item_id = request.POST.get('resource_item')
            item_quantity = request.POST.get('resource_quantity')
            project_getter = get_object_or_404(Projects, id = site_id)
            inventory_item_getter = get_object_or_404(Inventory, id=item_id)
            inventory_item_quantity_getter = get_object_or_404(Inventory, id=item_id).quantity
            if int(item_quantity) > inventory_item_getter.quantity:
                messages.error(request, "insufficient stock in inventory")
                return redirect("custom_admin_view")
            else:
                inventory_item_getter.quantity = inventory_item_quantity_getter - int(item_quantity) 
                inventory_item_getter.save()
                InventoryHistory.objects.create(inventory = inventory_item_getter, given_to = project_getter, quantity = item_quantity)
                RecentActivity.objects.create(site = project_getter, activity_type = "inventory")
                return redirect("custom_admin_view")
        if "update_site" in request.POST:
            progress_site = request.POST.get("progress_site")
            stage_number = request.POST.get("stage_number")
            windows_completed = request.POST.get("windows_completed")
            to_be_updated_project =  get_object_or_404(Projects, id = progress_site)
            progress_model_of_to_be_updated_project = get_object_or_404(Progress, project = to_be_updated_project)
            if to_be_updated_project.windows < int(windows_completed):
                messages.error(request, f"No of windows cannot be greater than {to_be_updated_project.windows} ")
                return redirect("custom_admin_view")
            elif to_be_updated_project.windows == int(windows_completed):
                setattr(to_be_updated_project, f"stage{stage_number}", True)
                setattr(to_be_updated_project, f"stage{stage_number}_date", timezone.now().date())
                to_be_updated_project.save()
                setattr(progress_model_of_to_be_updated_project, f"stage{stage_number}_window", windows_completed)
                progress_model_of_to_be_updated_project.save()
                RecentActivity.objects.create(site = to_be_updated_project, activity_type = "updated")
                return redirect("custom_admin_view")
            else:
                setattr(to_be_updated_project, f"stage{stage_number}", False)
                to_be_updated_project.save()
                setattr(progress_model_of_to_be_updated_project, f"stage{stage_number}_window", windows_completed)
                progress_model_of_to_be_updated_project.save()
                RecentActivity.objects.create(site = to_be_updated_project, activity_type = "updated")
                return redirect("custom_admin_view")
        if "site_activity" in request.POST:
            project_id_getter = request.POST.get("site_id")
            project_to_be_inactive = get_object_or_404(Projects, id = project_id_getter)
            project_to_be_inactive.is_active = not project_to_be_inactive.is_active
            project_to_be_inactive.save()
            return redirect("custom_admin_view")

    return render(request, "admin.html", {"maintenance_mode" : maintenance_mode_getter, "sites" : sites, "inventory_items" : items, 'orders_pending_count' : orders_pending_count, "pending_orders_list" : orders_pending_getter } )

def accept_order(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            project_id = request.POST.get('project_id')
            project = get_object_or_404(Projects, id=project_id)
            project.is_ordered = True
            project.save()
            RecentActivity.objects.create(site = project, activity_type = "ordered")
    return redirect(request.META.get('HTTP_REFERER', '/'))