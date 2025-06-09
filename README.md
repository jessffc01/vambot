# Vallourec Bot - Registro de Plantões via Telegram

Este projeto é um **bot do Telegram** para facilitar o registro de plantões em uma planilha do Google Sheets, ideal para equipes que precisam agendar e documentar turnos de trabalho de forma automatizada, segura e acessível.  
Desenvolvido em Python, utiliza Heroku para hospedagem e integração direta com Google Sheets via API.

---

## Funcionalidades

- Registro rápido de plantões diretamente no Telegram.
- Integração com Google Sheets para armazenamento e consulta.
- Interface intuitiva para facilitar uso por diferentes usuários.
- Hospedagem na nuvem (Heroku) para disponibilidade contínua.

---

## Tecnologias utilizadas

- **Python 3.9+**
- **python-telegram-bot**
- **gspread**
- **Heroku (deploy)**
- **Google Sheets API**

---

## Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/vallourec-bot.git
cd vallourec-bot
```

### 2. Instale as dependências

(Aconselhável uso de ambiente virtual)

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Você deve definir as seguintes variáveis de ambiente, localmente ou no Heroku:

- `TELEGRAM_BOT_TOKEN`: Token do seu bot, gerado pelo BotFather.
- `GOOGLE_SHEETS_CREDENTIALS`: JSON das credenciais da conta de serviço (ou caminho para o arquivo).
- `GOOGLE_SHEET_ID`: ID da planilha do Google Sheets.

Exemplo para Linux/Mac:
```bash
export TELEGRAM_BOT_TOKEN="SEU_TOKEN_DO_BOT"
export GOOGLE_SHEETS_CREDENTIALS="CAMINHO/PARA/credenciais.json"
export GOOGLE_SHEET_ID="ID_DA_PLANILHA"
```

No Heroku, configure isso em **Settings → Reveal Config Vars**.

### 4. Inicie o bot localmente

```bash
python bot.py
```

---

## Deploy no Heroku

1. Faça login no Heroku CLI.

2. Crie um app:
   ```bash
   heroku create nome-do-seu-app
   ```
3. Adicione as variáveis de ambiente no painel do Heroku (Settings → Reveal Config Vars).

4. Faça push do código:
   ```bash
   git push heroku master
   ```
5. O bot vai rodar como *worker* (verifique que o Procfile possui o conteúdo: `worker: python bot.py`).

---

## Personalização

- Edite o código em **bot.py** para alterar lógica de comando, formatação de mensagens ou integração com outras ferramentas.
- Caso deseje utilizar webhooks no futuro, será necessário configurar endpoint web (por exemplo, usando Flask).

---

## Troubleshooting

- Verifique os logs do Heroku com `heroku logs --tail` para eventuais erros.
- Confirme se as variáveis de ambiente estão corretas.
- Veja se seu bot está configurado como *worker* (não *web*, já que está em polling).

---

## Contribuição

1. Faça um fork do repositório.
2. Crie um branch para sua feature (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -am 'Minha nova feature'`).
4. Faça push para o branch (`git push origin minha-feature`).
5. Abra um Pull Request.

---

## Licença

[MIT License](LICENSE)
