import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ChatMessage, ChatbotAnalysis
from .services.agent import run_chatbot_agent
from .services.market import fetch_realtime_market_data

logger = logging.getLogger(__name__)


@login_required
def chat_view(request):
    """
    Renders the chat interface with message history and the latest AI analysis.
    """
    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    latest_analysis = ChatbotAnalysis.objects.filter(user=request.user, is_latest=True).first()
    
    context = {
        'chat_messages': messages,
        'latest_analysis': latest_analysis,
    }
    return render(request, 'chatbot/chat.html', context)


@login_required
@require_POST
def send_message(request):
    """
    Handles AJAX POST requests, runs the AI agent, persists messages and the analysis,
    and returns the JSON response.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except json.JSONDecodeError:
        user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({'error': 'Mensagem vazia.'}, status=400)

    # 1. Save user message to database
    ChatMessage.objects.create(
        user=request.user,
        message_text=user_message,
        is_from_bot=False
    )

    # 2. Run Langchain agent
    bot_response = run_chatbot_agent(request.user.id, user_message)

    # 3. Save bot response to database
    ChatMessage.objects.create(
        user=request.user,
        message_text=bot_response,
        is_from_bot=True
    )

    # 4. Generate and save a new ChatbotAnalysis
    # Summarize response (first sentence or first 100 characters)
    summary_text = bot_response.split('.')[0][:100]
    if len(summary_text) < len(bot_response.split('.')[0]):
        summary_text += '...'
    if not summary_text.strip():
        summary_text = 'Insight de Finanças Pessoais'

    # Get market snapshot
    market_snapshot = fetch_realtime_market_data()

    # Update previous analyses to is_latest=False
    ChatbotAnalysis.objects.filter(user=request.user).update(is_latest=False)

    # Create new latest analysis
    analysis = ChatbotAnalysis.objects.create(
        user=request.user,
        analysis_text=bot_response,
        summary=summary_text,
        market_data_snapshot=market_snapshot,
        is_latest=True
    )

    return JsonResponse({
        'response': bot_response,
        'analysis': {
            'summary': analysis.summary,
            'analysis_text': analysis.analysis_text,
            'created_at': analysis.created_at.strftime('%d/%m/%Y %H:%M')
        }
    })
