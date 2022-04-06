from django.shortcuts import redirect, render
from base.models import Topic
from .models import User
from .forms import UserForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'comments': comments,
        'topics': topics
    }
    return render(request, 'user/profile.html', context)


def registerUser(request):
    form = MyUserCreationForm
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else: 
            messages.error(request, 'Error has occured')
    context = {'form': form}
    return render(request, 'user/login_register.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # try:
        #     User.objects.get(email=email)
        # except:
        #     messages.error(request, "User does not exist")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or password is Incorrect')
    context = {'page': page}
    return render(request, 'user/login_register.html', context)

def logoutUser(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    return redirect('home')


def editUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

        
    context = {'form': form}
    return render(request, 'user/edit-user.html', context)