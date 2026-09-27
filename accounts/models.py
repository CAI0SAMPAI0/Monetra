from django.conf import settings
from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CHECKING', 'Conta Corrente'),
        ('SAVINGS', 'Poupança'),
        ('WALLET', 'Carteira'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField('nome da conta', max_length=100)
    bank_name = models.CharField('nome do banco', max_length=100)
    account_type = models.CharField(
        'tipo de conta',
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='CHECKING'
    )
    balance = models.DecimalField(
        'saldo',
        max_digits=12,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField('ativa', default=True)
    pluggy_item_id = models.CharField('Item ID na Pluggy', max_length=255, blank=True, null=True, help_text='UUID do Item na Pluggy')
    pluggy_account_id = models.CharField('Account ID na Pluggy', max_length=255, blank=True, null=True, help_text='UUID da Conta na Pluggy')
    logo_url = models.URLField('URL da logo', max_length=500, blank=True, null=True, help_text='URL da logo do banco ou conector')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'name']),
        ]

    def __str__(self):
        return self.name

    @property
    def bank_brand(self):
        name_lower = f'{self.name} {self.bank_name}'.lower()

        # Check if connected to another account with known bank via same pluggy_item_id
        if 'banco conectado' in name_lower and self.pluggy_item_id and self.user_id:
            sibling = Account.objects.filter(
                user_id=self.user_id,
                pluggy_item_id=self.pluggy_item_id
            ).exclude(id=self.id or 0).exclude(bank_name='Banco Conectado').first()
            if sibling:
                name_lower = f'{name_lower} {sibling.name} {sibling.bank_name}'.lower()

        if any(k in name_lower for k in ['santander']):
            return {
                'name': 'Santander',
                'bg_class': 'bg-[#EC0000]/15',
                'text_class': 'text-[#EC0000]',
                'border_class': 'border-[#EC0000]/30',
                'initials': 'SAN',
                'color': '#EC0000',
                'logo_svg': 'images/banks/santander.svg',
            }
        is_investment = self.account_type == 'INVESTMENT' or any(k in self.name.lower() for k in ['invest', 'nuinvest'])
        if is_investment and any(k in name_lower for k in ['nubank', 'nu ', 'nuinvest']):
            return {
                'name': 'NuInvest',
                'bg_class': 'bg-[#530082]/15',
                'text_class': 'text-[#A644FF]',
                'border_class': 'border-[#530082]/30',
                'initials': 'Nu',
                'color': '#530082',
                'logo_svg': 'images/banks/nuinvest.svg',
            }
        elif any(k in name_lower for k in ['nubank', 'nu ', 'nu pagamentos', 'nuconta']):
            return {
                'name': 'Nubank',
                'bg_class': 'bg-[#820AD1]/15',
                'text_class': 'text-[#A644FF]',
                'border_class': 'border-[#820AD1]/30',
                'initials': 'Nu',
                'color': '#820AD1',
                'logo_svg': 'images/banks/nubank.svg',
            }
        elif any(k in name_lower for k in ['itaú', 'itau', 'iti']):
            return {
                'name': 'Itaú',
                'bg_class': 'bg-[#EC7000]/15',
                'text_class': 'text-[#FF851B]',
                'border_class': 'border-[#EC7000]/30',
                'initials': 'Itaú',
                'color': '#EC7000',
                'logo_svg': 'images/banks/itau.svg',
            }
        elif any(k in name_lower for k in ['bradesco', 'next']):
            return {
                'name': 'Bradesco',
                'bg_class': 'bg-[#CC092F]/15',
                'text_class': 'text-[#FF3355]',
                'border_class': 'border-[#CC092F]/30',
                'initials': 'BRA',
                'color': '#CC092F',
                'logo_svg': 'images/banks/bradesco.svg',
            }
        elif any(k in name_lower for k in ['inter', 'banco inter']):
            return {
                'name': 'Inter',
                'bg_class': 'bg-[#FF7A00]/15',
                'text_class': 'text-[#FF7A00]',
                'border_class': 'border-[#FF7A00]/30',
                'initials': 'inter',
                'color': '#FF7A00',
                'logo_svg': 'images/banks/inter.svg',
            }
        elif any(k in name_lower for k in ['brasil', 'bb', 'banco do brasil']):
            return {
                'name': 'Banco do Brasil',
                'bg_class': 'bg-[#003882]/20',
                'text_class': 'text-[#FFD700]',
                'border_class': 'border-[#FFD700]/30',
                'initials': 'BB',
                'color': '#FFD700',
                'logo_svg': 'images/banks/bb.svg',
            }
        elif any(k in name_lower for k in ['c6', 'c6 bank']):
            return {
                'name': 'C6 Bank',
                'bg_class': 'bg-[#1C2A38]',
                'text_class': 'text-[#E2EAF0]',
                'border_class': 'border-[#374B5C]',
                'initials': 'C6',
                'color': '#E2EAF0',
                'logo_svg': 'images/banks/c6.svg',
            }
        elif any(k in name_lower for k in ['caixa', 'cef', 'economica federal', 'econômica federal']):
            return {
                'name': 'Caixa',
                'bg_class': 'bg-[#005CA9]/15',
                'text_class': 'text-[#2196F3]',
                'border_class': 'border-[#005CA9]/30',
                'initials': 'CX',
                'color': '#2196F3',
                'logo_svg': 'images/banks/caixa.svg',
            }
        elif any(k in name_lower for k in ['mercado pago', 'mercadopago', 'mercado livre', 'pago']):
            return {
                'name': 'Mercado Pago',
                'bg_class': 'bg-[#009EE3]/15',
                'text_class': 'text-[#00AEF0]',
                'border_class': 'border-[#009EE3]/30',
                'initials': 'MP',
                'color': '#009EE3',
                'logo_svg': 'images/banks/mercadopago.svg',
            }
        elif any(k in name_lower for k in ['btg', 'btg pactual']):
            return {
                'name': 'BTG Pactual',
                'bg_class': 'bg-[#001E62]/20',
                'text_class': 'text-[#4D88FF]',
                'border_class': 'border-[#001E62]/40',
                'initials': 'BTG',
                'color': '#4D88FF',
                'logo_svg': 'images/banks/btg.svg',
            }
        elif any(k in name_lower for k in ['xp ', 'xp invest', 'xp corretora']):
            return {
                'name': 'XP Investimentos',
                'bg_class': 'bg-[#000000]',
                'text_class': 'text-[#EAA93B]',
                'border_class': 'border-[#EAA93B]/30',
                'initials': 'XP',
                'color': '#EAA93B',
                'logo_svg': 'images/banks/xp.svg',
            }
        elif any(k in name_lower for k in ['rico']):
            return {
                'name': 'Rico',
                'bg_class': 'bg-[#FF4D00]/15',
                'text_class': 'text-[#FF4D00]',
                'border_class': 'border-[#FF4D00]/30',
                'initials': 'rico',
                'color': '#FF4D00',
                'logo_svg': 'images/banks/rico.svg',
            }
        elif any(k in name_lower for k in ['clear']):
            return {
                'name': 'Clear Corretora',
                'bg_class': 'bg-[#002B49]/30',
                'text_class': 'text-[#00C9FF]',
                'border_class': 'border-[#00C9FF]/30',
                'initials': 'CLR',
                'color': '#00C9FF',
                'logo_svg': 'images/banks/clear.svg',
            }
        elif any(k in name_lower for k in ['safra']):
            return {
                'name': 'Safra',
                'bg_class': 'bg-[#0B1B3D]/30',
                'text_class': 'text-[#D4AF37]',
                'border_class': 'border-[#D4AF37]/30',
                'initials': 'SAF',
                'color': '#D4AF37',
                'logo_svg': 'images/banks/safra.svg',
            }
        elif any(k in name_lower for k in ['sicredi']):
            return {
                'name': 'Sicredi',
                'bg_class': 'bg-[#00843D]/15',
                'text_class': 'text-[#00843D]',
                'border_class': 'border-[#00843D]/30',
                'initials': 'SIC',
                'color': '#00843D',
                'logo_svg': 'images/banks/sicredi.svg',
            }
        elif any(k in name_lower for k in ['sicoob']):
            return {
                'name': 'Sicoob',
                'bg_class': 'bg-[#003641]/20',
                'text_class': 'text-[#78BE20]',
                'border_class': 'border-[#78BE20]/30',
                'initials': 'SCB',
                'color': '#78BE20',
                'logo_svg': 'images/banks/sicoob.svg',
            }
        elif any(k in name_lower for k in ['pagbank', 'pagseguro']):
            return {
                'name': 'PagBank',
                'bg_class': 'bg-[#00A868]/15',
                'text_class': 'text-[#00A868]',
                'border_class': 'border-[#00A868]/30',
                'initials': 'PAG',
                'color': '#00A868',
                'logo_svg': 'images/banks/pagbank.svg',
            }
        elif any(k in name_lower for k in ['picpay']):
            return {
                'name': 'PicPay',
                'bg_class': 'bg-[#11C76F]/15',
                'text_class': 'text-[#11C76F]',
                'border_class': 'border-[#11C76F]/30',
                'initials': 'PIC',
                'color': '#11C76F',
                'logo_svg': 'images/banks/picpay.svg',
            }
        elif any(k in name_lower for k in ['neon']):
            return {
                'name': 'Neon',
                'bg_class': 'bg-[#00E5FF]/15',
                'text_class': 'text-[#00E5FF]',
                'border_class': 'border-[#00E5FF]/30',
                'initials': 'NEO',
                'color': '#00E5FF',
                'logo_svg': 'images/banks/neon.svg',
            }
        elif any(k in name_lower for k in ['nomad']):
            return {
                'name': 'Nomad',
                'bg_class': 'bg-[#FFDE00]/15',
                'text_class': 'text-[#FFDE00]',
                'border_class': 'border-[#FFDE00]/30',
                'initials': 'NOM',
                'color': '#FFDE00',
                'logo_svg': 'images/banks/nomad.svg',
            }
        elif any(k in name_lower for k in ['avenue']):
            return {
                'name': 'Avenue',
                'bg_class': 'bg-[#121212]',
                'text_class': 'text-[#E31B23]',
                'border_class': 'border-[#E31B23]/30',
                'initials': 'AVE',
                'color': '#E31B23',
                'logo_svg': 'images/banks/avenue.svg',
            }
        elif any(k in name_lower for k in ['pan', 'banco pan']):
            return {
                'name': 'Banco Pan',
                'bg_class': 'bg-[#0099FF]/15',
                'text_class': 'text-[#0099FF]',
                'border_class': 'border-[#0099FF]/30',
                'initials': 'PAN',
                'color': '#0099FF',
                'logo_svg': 'images/banks/pan.svg',
            }
        elif any(k in name_lower for k in ['original', 'banco original']):
            return {
                'name': 'Banco Original',
                'bg_class': 'bg-[#008542]/15',
                'text_class': 'text-[#008542]',
                'border_class': 'border-[#008542]/30',
                'initials': 'ORI',
                'color': '#008542',
                'logo_svg': 'images/banks/original.svg',
            }
        elif any(k in name_lower for k in ['binance', 'crypto', 'bitcoin', 'btc']):
            return {
                'name': 'Binance',
                'bg_class': 'bg-[#1E2026]',
                'text_class': 'text-[#F0B90B]',
                'border_class': 'border-[#F0B90B]/30',
                'initials': 'BIN',
                'color': '#F0B90B',
                'logo_svg': 'images/banks/binance.svg',
            }
        elif self.account_type == 'INVESTMENT' or 'invest' in name_lower:
            return {
                'name': self.bank_name if self.bank_name and self.bank_name != 'Banco Conectado' else 'Investimentos',
                'bg_class': 'bg-[#0FC4B3]/15',
                'text_class': 'text-[#0FC4B3]',
                'border_class': 'border-[#0FC4B3]/30',
                'initials': 'INV',
                'color': '#0FC4B3',
                'logo_svg': 'images/banks/investment.svg',
            }
        else:
            return {
                'name': self.bank_name if self.bank_name and self.bank_name != 'Banco Conectado' else (self.name or 'Banco'),
                'bg_class': 'bg-[#C09B2A]/10',
                'text_class': 'text-[#C09B2A]',
                'border_class': 'border-[#C09B2A]/20',
                'initials': (self.name[:2] if self.name else 'BK').upper(),
                'color': '#C09B2A',
                'logo_svg': 'images/banks/bank.svg',
            }


