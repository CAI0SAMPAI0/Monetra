import logging
import re
from decouple import config
from openai import OpenAI

logger = logging.getLogger(__name__)


def build_antia_financial_system_prompt(financial_data: str, market_data: str) -> str:
    """
    Constrói o System Prompt canônico AntIA | v3 adaptado para o assistente financeiro MonetraBot.
    Garante voz humana, continuidade sintática, precisão de dados e ausência de vícios de IA.
    """
    return (
        "# System Prompt MonetraBot | AntIA v3 Finance Engine\n\n"
        "## 1. IDENTIDADE E PAPEL\n"
        "Você é o MonetraBot, um assistente financeiro pessoal inteligente integrado ao sistema Monetra / Finanpy. "
        "Sua função é analisar dados financeiros reais, esclarecer dúvidas sobre movimentações bancárias, "
        "identificar oportunidades concretas de economia e orientar o usuário com sobriedade, didatismo e precisão técnica.\n\n"
        "## 2. VOZ E ESTILO EDITORIAL (AntIA v3)\n"
        "Sua escrita deve ser:\n"
        "- Responda SEMPRE e OBRIGATORIAMENTE em Português do Brasil (pt-BR). É terminantemente proibido responder em inglês ou expor notas internas em outro idioma;\n"
        "- Natural, contínua, articulada e genuinamente humana;\n"
        "- Didática e empática, sem infantilização nem formalismo excessivo;\n"
        "- Baseada em dados observáveis e fatos financeiros verificáveis;\n"
        "- Fluida, preservando artigos, preposições, conjunções e pronomes necessários à clareza e à coesão sintática;\n"
        "- Formatada em Markdown limpo (use títulos curtos, listas com marcadores e ênfases pontuais em negrito).\n\n"
        "## 3. PADRÕES E TERMOS PROIBIDOS\n"
        "Evite rigorosamente os vícios típicos de texto gerado por IA:\n"
        "- Não use oposições formulaicas como 'Não é sobre X, é sobre Y' ou 'Não faça isso. Faça aquilo.';\n"
        "- Não use antecipações teatrais como 'E isso muda tudo', 'O segredo é', 'A verdade é que', 'Aqui está o ponto';\n"
        "- Não use reticências (...) para criar suspense, exclamações em série (!!) nem travessões soltos;\n"
        "- Evite termos genéricos e muletas como: 'clareza', 'destravar', 'jornada', 'transformar sua vida', 'game changer', 'mudar tudo', 'chave do sucesso', 'absurdo', 'incrível', 'de verdade';\n"
        "- Anti-promessa: Nunca prometa enriquecimento rápido, rentabilidade garantida ou soluções mágicas. O foco é controle orçamentário, reserva de emergência e organização de gastos.\n\n"
        "## 4. DADOS REAIS DO USUÁRIO E DO MERCADO\n"
        "Baseie todas as suas respostas exclusivamente no contexto real abaixo. Não invente valores ou movimentações ausentes.\n\n"
        f"=== DADOS FINANCEIROS CONSOLIDADOS DO USUÁRIO ===\n{financial_data}\n\n"
        f"=== DADOS DE MERCADO ATUAIS ===\n{market_data}\n\n"
        "## 5. FORMATO DA RESPOSTA E SUGESTÕES CONTEXTUAIS OBRIGATÓRIAS\n"
        "- Entregue diretamente a resposta completa em Markdown estruturado, sem metacomentários.\n"
        "- REGRA CRÍTICA: Ao final ABSOLUTO da sua resposta, adicione impreterivelmente o bloco '---SUGESTÕES---' "
        "com 3 opções de perguntas curtas (máximo 8 palavras cada) para o usuário dar continuidade à conversa com base no que foi analisado.\n"
        "Exemplo de fechamento obrigatório:\n"
        "---SUGESTÕES---\n"
        "- Qual é o impacto nas despesas do mês?\n"
        "- Devo priorizar Selic ou CDI agora?\n"
        "- Como acelerar a meta de 6 meses?"
    )


def extract_response_and_suggestions(raw_text: str) -> tuple[str, list[str]]:
    """
    Separa o texto limpo da resposta e a lista de sugestões contextuais dinâmicas.
    """
    if not raw_text:
        return '', []

    suggestions = []
    clean_text = raw_text

    # 1. Procura delimitador explícito ---SUGESTÕES--- ou variantes
    delim_pattern = re.compile(r'(?:[\r\n]+|^)(?:[-=]{3,}\s*(?:SUGEST[ÕO]ES|SUGEST[ÃA]O)\s*[-=]{3,}|(?:###?|[*]{2})\s*(?:Sugest[õo]es|Pr[óo]ximos passos)[^:\n]*:?(?:[*]{2})?)', re.IGNORECASE)
    match = delim_pattern.search(raw_text)

    if match:
        clean_text = raw_text[:match.start()].strip()
        suggestions_raw = raw_text[match.end():].strip()
        for line in suggestions_raw.splitlines():
            line = line.strip()
            if not line:
                continue
            # Remove marcadores de lista como -, *, 1., 2., •, etc.
            line = re.sub(r'^[ \t]*[\-\*\•\d\.\)]+[ \t]*', '', line).strip()
            # Remove colchetes se o modelo tiver formatado como [Sugestão]
            if line.startswith('[') and line.endswith(']'):
                line = line[1:-1].strip()
            if line and len(line) >= 4:
                suggestions.append(line)

    suggestions = suggestions[:4]

    # Fallback caso o modelo não tenha gerado ou o delimitador não tenha sido encontrado
    if not suggestions:
        suggestions = [
            'Onde gastei mais este mês?',
            'Como posso economizar com base nos meus gastos?',
            'Qual é meu saldo consolidado?',
            'Analise meus hábitos de consumo'
        ]

    return clean_text, suggestions


def run_chatbot_agent(user_id: int, user_input: str, session=None) -> tuple[str, list[str]]:
    """
    Executa o assistente financeiro MonetraBot aplicando o System Prompt AntIA v3.
    Retorna uma tupla: (resposta_limpa, lista_de_sugestoes_contextuais).
    Suporta multi-turn memory com histórico da sessão ativa e sugestões dinâmicas.
    """
    from django.contrib.auth import get_user_model
    from chatbot.services.tools import get_user_financial_data, get_market_data_summary
    from chatbot.services.suggestions import generate_profile_suggestions

    user = get_user_model().objects.filter(id=user_id).first()

    # 1. Coleta dados locais do usuário e mercado
    financial_data = get_user_financial_data(user_id)
    
    # Identifica se o usuário mencionou um ativo específico
    asset_query = None
    user_words = user_input.lower().split()
    keywords = ['petr4', 'vale3', 'itub4', 'bbas3', 'mglu3', 'wege3', 'btc', 'bitcoin', 'eth', 'ethereum', 'usd', 'dolar', 'dólar', 'eur', 'euro']
    for word in user_words:
        word_clean = ''.join(c for c in word if c.isalnum())
        if word_clean in keywords:
            asset_query = word_clean
            break
            
    market_data = get_market_data_summary(asset_query)

    default_fallback_suggestions = generate_profile_suggestions(user, session) if user else [
        'Qual é meu saldo consolidado?',
        'Onde gastei mais este mês?',
        'Como posso economizar?'
    ]

    # DeepSeek API configuration via Hugging Face Router
    api_key = config('HF_TOKEN_SEEK', default=config('HF_TOKEN', default=''))
    if not api_key:
        logger.error('HF_TOKEN_SEEK is not defined in .env')
        return 'Erro: HF_TOKEN_SEEK não configurada no arquivo de ambiente.', default_fallback_suggestions

    client = OpenAI(
        base_url='https://router.huggingface.co/v1',
        api_key=api_key,
        timeout=60.0,
    )

    system_instruction = build_antia_financial_system_prompt(financial_data, market_data)

    try:
        messages = [
            {'role': 'system', 'content': system_instruction}
        ]
        # Multi-turn conversational memory: adiciona as últimas mensagens da sessão
        if session:
            recent_msgs = list(session.messages.order_by('created_at'))[-8:]
            for r_msg in recent_msgs:
                role = 'assistant' if r_msg.is_from_bot else 'user'
                messages.append({'role': role, 'content': r_msg.message_text})

        messages.append({'role': 'user', 'content': user_input})

        completion = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V4.1-Flash:novita',
            messages=messages,
            temperature=0.35,
            max_tokens=4000,
        )
        msg = completion.choices[0].message
        content = msg.content or ''
        
        # Nunca expor reasoning_content (raciocínio interno em inglês) ao usuário!
        if not content.strip():
            logger.warning('DeepSeek retornou conteúdo vazio na resposta final.')
            content = (
                'Analisei suas informações com sucesso. Gostaria de focar na reserva de emergência, '
                'no seu saldo consolidado ou em opções de economia para este mês?'
            )

        clean_resp, suggestions = extract_response_and_suggestions(content)

        if not suggestions and user:
            suggestions = generate_profile_suggestions(user, session)

        if session and suggestions:
            session.latest_suggestions = suggestions
            session.save(update_fields=['latest_suggestions', 'updated_at'])

        return clean_resp, suggestions
    except Exception as e:
        logger.error(f'Error executing agent: {e}')
        # Resposta de contingência com tom AntIA v3
        fallback_msg = (
            'O serviço de inteligência artificial apresentou uma oscilação temporária de conexão com o provedor. '
            'Com base nas informações sincronizadas do seu perfil, você pode consultar suas contas, '
            'saldos e histórico de transações diretamente no Dashboard e na aba de Contas.'
        )
        return fallback_msg, default_fallback_suggestions

