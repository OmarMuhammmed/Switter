from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Conversation

User = get_user_model()

@login_required
def users_chat_list(request):
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat_list.html', {'users': all_users})


def chat_room(request, user_id):
    sender = request.user
    receiver = get_object_or_404(User, id=user_id)
    
    # Generate room name
    room_name = f"chat_{min(sender.id, receiver.id)}_{max(sender.id, receiver.id)}"
    
    # Fetch or create the conversation
    try:
        conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).first()
        if not conversation:
            # If conversation doesn't exist, create a new one
            conversation = Conversation.objects.create()
            conversation.participants.add(sender, receiver)
        
        # Fetch messages for this conversation
        messages = conversation.messages.all().order_by('timestamp')
        print(f"Conversation: {conversation}")
        print(f"Messages: {messages}")
    except Conversation.DoesNotExist:
        messages = []

    context = {
        'room_name': room_name,
        'recipient': receiver,
        'current_user': sender,  
        'users': User.objects.exclude(id=request.user.id),
        'messages': messages   
    }
    
    return render(request, 'chat.html', context)