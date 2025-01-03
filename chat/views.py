from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def users_chat_list(request):
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat_list.html', {'users': all_users})


def chat_room(request, user_id):
    sender = request.user
    receiver = get_object_or_404(User, id=user_id)
    
  
    room_name = f"chat_{min(sender.id, receiver.id)}_{max(sender.id, receiver.id)}"
    
   
    context = {
        'room_name': room_name,
        'recipient': receiver,
        'current_user': sender,  
        'users': User.objects.exclude(id=request.user.id)  
    }
    
    return render(request, 'chat.html', context)