# Diretrizes e Padrões

Para manter a consistência do código e a qualidade do projeto, todos os contribuidores devem seguir as diretrizes abaixo.

## Código (Python/Django)

- **Linguagem**: Todo o código (nomes de variáveis, funções, classes, comentários e logs) deve ser escrito em **inglês**.
- **Estilo**: Siga rigorosamente a **PEP 8**.
- **Strings**: Utilize **aspas simples** (`'`) por padrão para strings literais, a menos que a string contenha aspas simples.
- **Responsabilidades**: Cada app deve ter uma responsabilidade bem definida. Evite acoplamento excessivo entre apps diferentes.
- **Modelos**: Todo modelo deve incluir, sempre que possível, os campos `created_at` e `updated_at` para rastreabilidade.

## Frontend (Templates/CSS)

- **TailwindCSS**: Utilize classes do Tailwind para estilização. Evite criar arquivos CSS customizados a menos que seja estritamente necessário.
- **Responsividade**: Siga uma abordagem *mobile-first*. Garanta que a interface funcione bem em resoluções a partir de 320px.
- **Idioma da UI**: A interface com o usuário (textos visíveis no navegador) deve ser em **Português (Brasil)**.

## Git e Versionamento

- **Commits**: Escreva mensagens de commit claras e concisas (preferencialmente em português ou inglês, seguindo o padrão do time).
- **Branches**: Utilize nomes descritivos para branches (ex: `feature/nova-transacao`, `fix/erro-login`).
