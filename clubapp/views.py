import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Club, Member, Event, Announcement
from .forms import ClubForm, MemberForm, EventForm, AnnouncementForm

def home(request):
    return redirect('clubs')

def clubs(request):
    clubs = Club.objects.all()
    return render(request, 'clubs.html', {'clubs': clubs})

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    members = Member.objects.filter(club=club)
    events = Event.objects.filter(club=club)
    announcements = Announcement.objects.filter(club=club)
    return render(request, 'club_detail.html', {
        'club': club, 'members': members, 'events': events, 'announcements': announcements
    })

def events(request):
    # Get all upcoming events ordered by date
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    return render(request, 'events.html', {'events': events})

def announcements(request):
    # Get all announcements ordered by posted date (newest first)
    announcements = Announcement.objects.all().order_by('-posted_on')
    return render(request, 'announcements.html', {'announcements': announcements})

def this_week_events(request):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    events = Event.objects.filter(date__range=[start_week, end_week])
    return render(request, 'clubapp/this_week_events.html', {'events': events})

@login_required
def admin_dashboard(request):
    # Check if user is a superuser
    if request.user.is_superuser:
        # Superusers can see all clubs
        user_clubs = Club.objects.all()
        members = Member.objects.all()
        events = Event.objects.all()
        announcements = Announcement.objects.all()
    else:
        # Regular users can only see clubs where they are a member
        user_clubs = Club.objects.filter(member__name=request.user.username)
        members = Member.objects.filter(club__in=user_clubs)
        events = Event.objects.filter(club__in=user_clubs)
        announcements = Announcement.objects.filter(club__in=user_clubs)
    
    return render(request, 'clubapp/admin/dashboard.html', {
        'clubs': user_clubs,
        'members': members,
        'events': events,
        'announcements': announcements,
        'is_superuser': request.user.is_superuser
    })

@login_required
def manage_clubs(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            # Add the user as a member of the club
            Member.objects.create(
                club=club,
                name=request.user.username,
                role='Admin',
                join_date=timezone.now().date()
            )
            messages.success(request, 'Club added successfully!')
            return redirect('manage_clubs')
    else:
        form = ClubForm()
    
    # Get only clubs where the user is a member
    clubs = Club.objects.filter(member__name=request.user.username)
    return render(request, 'clubapp/admin/manage_clubs.html', {
        'form': form,
        'clubs': clubs
    })

@login_required
def manage_members(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('manage_members')
    else:
        form = MemberForm()
    
    # Get members of clubs where the user is a member
    user_clubs = Club.objects.filter(member__name=request.user.username)
    members = Member.objects.filter(club__in=user_clubs)
    return render(request, 'clubapp/admin/manage_members.html', {
        'form': form,
        'members': members
    })

@login_required
def manage_events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('manage_events')
    else:
        form = EventForm()
    
    # Get events of clubs where the user is a member
    user_clubs = Club.objects.filter(member__name=request.user.username)
    events = Event.objects.filter(club__in=user_clubs)
    return render(request, 'clubapp/admin/manage_events.html', {
        'form': form,
        'events': events
    })

@login_required
def manage_announcements(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement added successfully!')
            return redirect('manage_announcements')
    else:
        form = AnnouncementForm()
    
    # Get announcements of clubs where the user is a member
    user_clubs = Club.objects.filter(member__name=request.user.username)
    announcements = Announcement.objects.filter(club__in=user_clubs)
    return render(request, 'clubapp/admin/manage_announcements.html', {
        'form': form,
        'announcements': announcements
    })

@login_required
def edit_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to edit this club.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club updated successfully!')
            return redirect('manage_clubs')
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubapp/admin/edit_club.html', {'form': form})

@login_required
def delete_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to delete this club.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        club.delete()
        messages.success(request, 'Club deleted successfully!')
        return redirect('manage_clubs')
    return render(request, 'clubapp/admin/delete_club.html', {'club': club})

@login_required
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=member.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to edit this member.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully!')
            return redirect('manage_members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'clubapp/admin/edit_member.html', {'form': form})

@login_required
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=member.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to delete this member.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted successfully!')
        return redirect('manage_members')
    return render(request, 'clubapp/admin/delete_member.html', {'member': member})

@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=event.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'clubapp/admin/edit_event.html', {'form': form})

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=event.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('manage_events')
    return render(request, 'clubapp/admin/delete_event.html', {'event': event})

@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=announcement.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to edit this announcement.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully!')
            return redirect('manage_announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'clubapp/admin/edit_announcement.html', {'form': form})

@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # Check if user is a member of this club
    if not Member.objects.filter(club=announcement.club, name=request.user.username).exists():
        messages.error(request, 'You do not have permission to delete this announcement.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully!')
        return redirect('manage_announcements')
    return render(request, 'clubapp/admin/delete_announcement.html', {'announcement': announcement})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'clubapp/login.html')

def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
