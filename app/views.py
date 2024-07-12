from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request, 'home.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            login(request, user)
            
            return redirect('dashboard')  
        else:
            
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['email']
        first_name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1, first_name=first_name)
            
            
            profile = UserProfile(user=user, name=first_name)
            profile.save()
            print("Just complete your profile now")
            return redirect(f'/complete_profile/{profile.id}/') 

    return render(request, 'signup.html')

def complete_profile(request,id):
    if request.method == 'POST':
        
        profile = UserProfile.objects.get(id=id)
        
        profile.position_id = request.POST['position']
        profile.department_id = request.POST['department']
        profile.salary = request.POST['salary']
        profile.hire_date = request.POST['hire_date']
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        return redirect('login')  # Redirect to a pending approval page
    
    departments = Department.objects.all()
    positions = Position.objects.all()
    
    return render(request, 'complete_profile.html', {'departments': departments, 'positions': positions})      

    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def dashboard(request):
    if request.user.is_superuser:
        verified_users = UserProfile.objects.filter(verified=True)
        unverified_users = UserProfile.objects.filter(verified=False)
        print(verified_users)
        print(unverified_users)
        context = {
            'superuser': True,
            'verified_users': verified_users,
            'unverified_users': unverified_users
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('profile')
        
    
@login_required(login_url='/login/')
def adminpage(request):
    if request.user.is_superuser:
        unverified_users = UserProfile.objects.filter(verified=False)
        context = {
            'superuser': True,
            'unverified_users': unverified_users
        }
        return render(request, 'admin_approve.html',context)
@login_required(login_url='/login/')
def approve_user(request, user_id):
    if request.user.is_superuser:
        user_profile = get_object_or_404(UserProfile, id=user_id)
        user_profile.verified = True
        user_profile.save()
    return redirect('dashboard')

@login_required(login_url='/login/')
def reject_user(request, user_id):
    if request.user.is_superuser:
        user_profile = get_object_or_404(UserProfile, id=user_id)
        user_profile.delete()
    return redirect('dashboard')
def profile_pending_approval(request):
    user = UserProfile.objects.get(user = request.user)
    context = {
        'user': user
    }
    return render(request, 'profile_status.html',context)

def profile(request):
    user = request.user
    
    profile = UserProfile.objects.get(user=user.id)
    
    
    if not profile.verified:
        return redirect('profile_pending_approval')
    
    return render(request, 'profile.html', {'profile': profile})


def delete_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = profile.user
    profile.delete()
    user.delete()
    return redirect('signup')


def update_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    positions = Position.objects.all()
    departments = Department.objects.all()
    if request.method == 'POST':
        profile.name = request.POST['name']
        profile.position_id = request.POST['position']
        profile.department_id = request.POST['department']
        profile.salary = request.POST['salary']
        profile.hire_date = request.POST['hire_date']
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile')
    return render(request, 'update_profile.html', {
        'profile': profile,
        'positions': positions,
        'departments': departments
    })