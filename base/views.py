from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.
from django.http import HttpResponse

# rooms = [
#     {'id': 1, 'name': 'Muqumiy tadbiri'},
#     {'id': 2, 'name': 'Halqaro Stipendiyalar'},
#     {'id': 3, 'name': 'Menejment va Korparatsiya boshqaruvi'},
# ]

def home(request):
    q = request.GET.get('i') if request.GET.get('i') != None else '' # ?i parametr qiymatlarini oladi
    # rooms = Room.objects.filter(topic__name__icontains=q name__icontains=q)
    # (up) agar bunday bolsa hamma filtrdan o'tishi kerak, bizga esa faqat bitta filtrdan otsa kifoya, search bar uchun 
    # (up) biz Room dagi topic attributidagi Topic modelidagi name attributiga murojaat qilishimiz uchun __ (2ta _) qoyamiz
    # (up) icontains = q degani topic__name__ da q bo'lsa o'shani chiqaradi
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |       #dastur hech bolmasa bitta filtrdan o'tishi kerak
        Q(name__icontains=q) |              #shuning uchun mantiqiy amallar uchun Q modeli import qilindi
        Q(host__username__icontains=q) |    # | - or, & - end
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()[:5]
    comments = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    index = {
        'rooms': rooms,
        'topics': topics, 
        'room_count': room_count,
        'comments': comments,
    }
    return render(request, 'base/home.html', index) #HttpResponse('This is home')


def room(request, pk):
    room = Room.objects.get(id=pk) #har bir sub model o'zining id siga ega bo'ladi, va ushbu id bilan aynan shu sub modelga murojaat qilinadi
    # for i in Room.objects.all():
    #     if int(pk) == i['id']:
    #         room  = i
    comments = room.comment.all()#.order_by('-created') (edited 19/03/22 check Model.Message.Meta) #(look model) related_name=comment (by default <Class name>_set: message_set) room objectining child objectini chaqiradi Room modeli uchun Comment modeli child hisoblanadi (models.py/Room ga qaralsin)
    participants = room.participants.all().order_by('username')
    if request.method == 'POST':
        Message.objects.create(#    # maybe .update(), .all(), .delete()
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user) #maybe .remove()
        return redirect('room', pk=room.id)
        
    contex = {'room': room, 'comments': comments, 'participants': participants}
    return render(request, 'base/room.html', contex) #HttpResponse('This is room')




@login_required(login_url='login') # @login_required -- login filter
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) #name=topic_name shu object bolsa create qiladi va created=True boladi yoki aksi
        Room.objects.create(
            name = request.POST.get('name'), # 'name' ni RoomForm bergan
            description = request.POST.get('description'), # 'description' ni RoomForm bergan
            topic = topic,
            host = request.user,
        )

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save
        return redirect('/') #'/' or by name 'home'
    context = {'form': form, 'topics': topics, 'text':'Create'}
    return render(request, 'base/form_room.html', context)


@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowet to edit')
    form = RoomForm(instance=room) #room ni update qiladi
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
            # form.save
        room.save()
        return redirect('/')
    context = {'form': form,'room': room, 'topics': topics, 'text': 'Update'}
    return render(request, 'base/form_room.html', context)


@login_required(login_url='login')
def deleteroom(request, pk):
    room    = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowet to delete')
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete')
    if request.method == 'POST':
        message.delete()
        return redirect('/')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def borwseTopics(request):
    q = request.GET.get('i') if request.GET.get('i') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activities(request):
    comments = Message.objects.all()
    
    context = {'comments': comments}
    return render(request, 'base/activity.html', context)