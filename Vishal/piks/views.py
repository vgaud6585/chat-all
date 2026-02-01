from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Student, PrivateChat
from .forms import StudentForm
import datetime
from django.views.decorators.csrf import csrf_exempt


# 1. SEARCH STUDENT (Live search logic for set_name page)
@csrf_exempt
def search_student(request):
    query = request.GET.get('term', '')
    # Database se naam search karna jo query se start ho rahe hon
    results = Student.objects.filter(name__icontains=query)[:5]
    data = [{'name': s.name} for s in results]
    return JsonResponse(data, safe=False)

# 2. SET NAME (Entrance point for chat)
@csrf_exempt
def set_name(request):
    if request.method == "POST":
        request.session['user_name'] = request.POST.get('nickname')
        return redirect('chat_lobby')
    return render(request, 'set_name.html')

# 3. CHAT LOBBY (Users list with unread dots and sorting)
def chat_lobby(request):
    my_name = request.session.get('user_name')
    if not my_name:
        return redirect('set_name')
        
    students = Student.objects.exclude(name=my_name)
    
    # Ek purani date default sorting ke liye (TypeError fix karne ke liye)
    min_date = datetime.datetime(1900, 1, 1, tzinfo=datetime.timezone.utc)
    
    user_data = []
    for s in students:
        # Unread messages count
        unread_count = PrivateChat.objects.filter(sender=s.name, receiver=my_name, is_read=False).count()
        
        # Last message ka time nikalna sorting ke liye
        last_msg = PrivateChat.objects.filter(
            Q(sender=my_name, receiver=s.name) | Q(sender=s.name, receiver=my_name)
        ).order_by('-timestamp').first()
        
        user_data.append({
            'info': s,
            'unread': unread_count,
            'last_time': last_msg.timestamp if last_msg else min_date
        })

    # Sort: Naya message top par, jinse baat nahi hui wo niche
    user_data.sort(key=lambda x: x['last_time'], reverse=True)
    
    return render(request, 'chat_lobby.html', {'user_data': user_data})

# 4. PERSONAL CHAT (Real-time page with history)
def personal_chat(request, receiver_name):
    my_name = request.session.get('user_name', 'Anonymous')
    
    # Chat open hote hi messages ko 'Read' mark karna
    PrivateChat.objects.filter(sender=receiver_name, receiver=my_name, is_read=False).update(is_read=True)
    
    # Purani history fetch karna
    old_messages = PrivateChat.objects.filter(
        Q(sender=my_name, receiver=receiver_name) | 
        Q(sender=receiver_name, receiver=my_name)
    ).order_by('timestamp')

    # Unique Room ID for WebSocket
    room_raw = sorted([my_name, receiver_name])
    room_id = f"{room_raw[0]}_{room_raw[1]}".replace(" ", "_")
    
    return render(request, 'personal_chat.html', {
        'receiver': receiver_name,
        'my_name': my_name,
        'room_id': room_id,
        'messages': old_messages
    })

# --- CRUD FUNCTIONS FOR STUDENT TABLE ---

# 5. LIST ALL STUDENTS
def index(request):
    students = Student.objects.all()
    return render(request, 'index.html', {'students': students})

# 6. ADD STUDENT
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

# 7. EDIT STUDENT
def update_data(request, id):
    obj = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'edit_student.html', {'form': form})

# 8. DELETE STUDENT
def delete_data(request, id):
    obj = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    return render(request, 'delete_confirm.html', {'obj': obj})
