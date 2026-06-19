import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from ai.services.analysis_service import run_analysis_for_user

logger = logging.getLogger(__name__)


@login_required
@require_GET
def generate_summary_api(request):
    """
    Gera uma análise financeira em tempo real para o usuário usando o Langchain Agent,
    persiste na base de dados Neon e retorna os dados via JSON.
    """
    try:
        user = request.user
        
        # Chama a camada de serviço para rodar o agente e salvar a análise
        analysis = run_analysis_for_user(user)
        
        if analysis:
            formatted_summary = (
                f"<strong>Com base na análise inteligente da sua carteira para {user.email}:</strong><br><br>"
                f"{analysis.analysis_text.replace('\n', '<br>')}"
            )
            return JsonResponse({
                'status': 'success',
                'summary': formatted_summary,
                'message': 'Análise financeira gerada com sucesso pela inteligência artificial!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Não foi possível conectar com o agente de IA para gerar o resumo. Verifique seus dados.'
            }, status=500)
    except Exception as e:
        logger.error(f"Erro no endpoint de geração de resumo de IA: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f"Erro ao processar requisição: {str(e)}"
        }, status=500)
