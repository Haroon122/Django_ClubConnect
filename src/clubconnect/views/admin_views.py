from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from ..models import Club, ClubMembership, AdminProfile
from ..forms import ClubForm  # You'll need to create this form

from ..forms import ClubForm
def is_admin(user):
    """Check if the user is a site admin."""
    try:
        return user.adminprofile.is_site_admin
    except AdminProfile.DoesNotExist:
        return False

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard home view showing overview statistics."""
    total_clubs = Club.objects.count()
    total_users = User.objects.count()
    active_clubs = Club.objects.filter(is_active=True).count()
    
    # Recent clubs
    recent_clubs = Club.objects.order_by('-created_at')[:5]
    
    # Users with most clubs
    users_with_clubs = User.objects.annotate(
        club_count=Count('clubs')
    ).order_by('-club_count')[:5]
    
    context = {
        'total_clubs': total_clubs,
        'total_users': total_users,
        'active_clubs': active_clubs,
        'recent_clubs': recent_clubs,
        'users_with_clubs': users_with_clubs,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_manage_clubs(request):
    """View for managing all clubs."""
    clubs = Club.objects.all().order_by('name')
    
    context = {
        'clubs': clubs,
    }
    
    return render(request, 'admin/manage_clubs.html', context)

@login_required
@user_passes_test(is_admin)
def admin_edit_club(request, club_id):
    """View for editing a specific club."""
    club = get_object_or_404(Club, id=club_id)
    
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, f"Club '{club.name}' updated successfully.")
            return redirect('admin_manage_clubs')
    else:
        form = ClubForm(instance=club)
    
    context = {
        'form': form,
        'club': club,
    }
    
    return render(request, 'admin/edit_club.html', context)

@login_required
@user_passes_test(is_admin)
def admin_delete_club(request, club_id):
    """View for deleting a club."""
    club = get_object_or_404(Club, id=club_id)
    
    if request.method == 'POST':
        club_name = club.name
        club.delete()
        messages.success(request, f"Club '{club_name}' deleted successfully.")
        return redirect('admin_manage_clubs')
    
    context = {
        'club': club,
    }
    
    return render(request, 'admin/delete_club.html', context)

@login_required
@user_passes_test(is_admin)
def admin_manage_users(request):
    """View for managing all users."""
    users = User.objects.all().order_by('username')
    
    context = {
        'users': users,
    }
    
    return render(request, 'admin/manage_users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_toggle_user_admin(request, user_id):
    """Toggle whether a user is a site admin."""
    user = get_object_or_404(User, id=user_id)
    
    # Don't allow removing admin from yourself
    if user == request.user:
        messages.error(request, "You cannot remove your own admin privileges.")
        return redirect('admin_manage_users')
    
    admin_profile, created = AdminProfile.objects.get_or_create(user=user)
    
    if admin_profile.is_site_admin:
        admin_profile.is_site_admin = False
        admin_profile.save()
        messages.success(request, f"Admin privileges removed from {user.username}.")
    else:
        admin_profile.is_site_admin = True
        admin_profile.save()
        messages.success(request, f"{user.username} is now a site admin.")
    
    return redirect('admin_manage_users')


