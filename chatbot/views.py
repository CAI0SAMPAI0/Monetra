import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage, ChatbotAnalysis
from .services.agent import run_chatbot_agent
from .services.market import fetch_realtime_market_data
from .services.suggestions import generate_profile_suggestions

logger = logging.getLogger(__name__)


@login_required
def chat_view(request):
    """
    Renders the chat interface with conversation session history,
    the active session messages, dynamic suggestions, and AI market snapshot.
    """
    sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    
    session_id = request.GET.get('session_id')
    active_session = None

    if session_id:
        try:
            active_session = sessions.filter(id=session_id).first()
        except Exception:
            active_session = None

    if not active_session:
        active_session = sessions.first()

    if not active_session:
        active_session = ChatSession.objects.create(user=request.user, title='Nova conversa')
        sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')

    messages = active_session.messages.order_by('created_at')
    latest_analysis = ChatbotAnalysis.objects.filter(user=request.user, is_latest=True).first()
    initial_suggestions = generate_profile_suggestions(request.user, active_session)

    context = {
        'sessions': sessions,
        'active_session': active_session,
        'chat_messages': messages,
        'latest_analysis': latest_analysis,
        'initial_suggestions': initial_suggestions,
    }
    return render(request, 'chatbot/chat.html', context)


@csrf_exempt
@require_POST
def create_new_session(request):
    """Creates a new empty chat session for the authenticated user."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado. Faça o login.'}, status=401)
    
    session = ChatSession.objects.create(user=request.user, title='Nova conversa')
    suggestions = generate_profile_suggestions(request.user, session)
    return JsonResponse({
        'status': 'success',
        'session_id': str(session.id),
        'title': session.title,
        'suggestions': suggestions
    })


@csrf_exempt
@require_POST
def delete_session(request, session_id):
    """Deletes a chat session and all its messages."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado. Faça o login.'}, status=401)
    
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    return JsonResponse({'status': 'success', 'message': 'Conversa excluída com sucesso.'})


@csrf_exempt
@require_POST
def send_message(request):
    """
    Handles AJAX POST requests, attaches message to the target or new session,
    runs the AI agent with multi-turn memory, updates suggestions, and returns JSON.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado. Faça o login.'}, status=401)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
    except (json.JSONDecodeError, AttributeError):
        user_message = request.POST.get('message', '').strip()
        session_id = request.POST.get('session_id')

    if not user_message:
        return JsonResponse({'error': 'Mensagem vazia.'}, status=400)

    # 1. Resolve active session
    session = None
    if session_id:
        try:
            session = ChatSession.objects.filter(id=session_id, user=request.user).first()
        except Exception:
            session = None

    if not session:
        session = ChatSession.objects.create(user=request.user, title='Nova conversa')

    # If first user message in session, derive a human-friendly title
    is_first_message = (session.messages.count() == 0)
    if is_first_message:
        title = user_message[:45].strip()
        if len(user_message) > 45:
            title += '...'
        session.title = title
        session.save(update_fields=['title', 'updated_at'])

    # 2. Save user message to database
    ChatMessage.objects.create(
        user=request.user,
        session=session,
        message_text=user_message,
        is_from_bot=False
    )

    # 3. Run AI agent with multi-turn context
    bot_response, suggestions = run_chatbot_agent(request.user.id, user_message, session=session)

    # 4. Save bot response to database
    ChatMessage.objects.create(
        user=request.user,
        session=session,
        message_text=bot_response,
        is_from_bot=True
    )

    # 5. Persist latest suggestions to session
    if suggestions:
        session.latest_suggestions = suggestions
        session.save(update_fields=['latest_suggestions', 'updated_at'])

    # 6. Generate and save a new ChatbotAnalysis
    summary_text = bot_response.split('.')[0][:100]
    if len(summary_text) < len(bot_response.split('.')[0]):
        summary_text += '...'
    if not summary_text.strip():
        summary_text = 'Insight de Finanças Pessoais'

    market_snapshot = fetch_realtime_market_data()

    ChatbotAnalysis.objects.filter(user=request.user).update(is_latest=False)
    analysis = ChatbotAnalysis.objects.create(
        user=request.user,
        session=session,
        analysis_text=bot_response,
        summary=summary_text,
        market_data_snapshot=market_snapshot,
        is_latest=True
    )

    return JsonResponse({
        'response': bot_response,
        'suggestions': suggestions,
        'session_id': str(session.id),
        'session_title': session.title,
        'analysis': {
            'summary': analysis.summary,
            'analysis_text': analysis.analysis_text,
            'created_at': analysis.created_at.strftime('%d/%m/%Y %H:%M'),
            'market_data_snapshot': analysis.market_data_snapshot
        }
    })


@csrf_exempt
@require_POST
def clear_chat(request):
    """Clears messages for the active session or all sessions."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado. Faça o login.'}, status=401)
    
    session_id = request.POST.get('session_id')
    if session_id:
        ChatMessage.objects.filter(user=request.user, session_id=session_id).delete()
    else:
        ChatMessage.objects.filter(user=request.user).delete()
    
    ChatbotAnalysis.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success', 'message': 'Histórico de mensagens deletado com sucesso.'})
