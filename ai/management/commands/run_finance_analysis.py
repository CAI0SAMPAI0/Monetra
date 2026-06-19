from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ai.services.analysis_service import run_analysis_for_all_users, run_analysis_for_user

User = get_user_model()


class Command(BaseCommand):
    help = 'Executa a análise financeira inteligente com IA para os usuários ativos do sistema.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='ID do usuário específico para executar a análise.'
        )

    def handle(self, *args, **options):
        user_id = options.get('user_id')

        if user_id:
            try:
                user = User.objects.get(pk=user_id, is_active=True)
                self.stdout.write(self.style.NOTICE(f'Iniciando análise para o usuário {user.email}...'))
                result = run_analysis_for_user(user)
                if result:
                    self.stdout.write(self.style.SUCCESS(f'Análise gerada com sucesso para {user.email}!'))
                else:
                    self.stdout.write(self.style.ERROR(f'Falha ao gerar análise para {user.email}.'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuário com ID {user_id} ativo não encontrado.'))
        else:
            self.stdout.write(self.style.NOTICE('Iniciando processamento em lote de análise de IA...'))
            summary = run_analysis_for_all_users()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Concluído! Processados: {summary['total']} | "
                    f"Sucessos: {summary['success']} | "
                    f"Erros: {summary['errors']}"
                )
            )
