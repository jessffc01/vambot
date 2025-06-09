import os
import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Configuração de Log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados da conversação
ESCOLHER_DIA, DATA, HORA_INICIO, HORA_FIM, DESCRICAO = range(5)

# Conexão com Google Sheets
def conectar_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(os.environ['GOOGLE_CREDENTIALS']), scope)
        return gspread.authorize(creds)
    except Exception as e:
        logger.error(f"Erro ao conectar ao Google Sheets: {e}")
        raise

# Handlers (mantenha seus handlers existentes)
# ... [seus handlers aqui] ...

def main():
    # Obtenção das variáveis de ambiente
    TOKEN = os.environ['TELEGRAM_TOKEN']
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ['HEROKU_APP_NAME']
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Configuração do ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ESCOLHER_DIA: [MessageHandler(Filters.text & ~Filters.command, escolher_dia)],
            DATA: [MessageHandler(Filters.text & ~Filters.command, processar_dia)],
            # Adicione outros estados conforme necessário
        },
        fallbacks=[CommandHandler('cancel', cancelar)],
    )

    dp.add_handler(conv_handler)

    # Configuração do Webhook
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_NAME}.herokuapp.com/{TOKEN}"
    )
    updater.idle()

if __name__ == '__main__':
    main()import os
import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Configuração de Log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados da conversação
ESCOLHER_DIA, DATA, HORA_INICIO, HORA_FIM, DESCRICAO = range(5)

# Conexão com Google Sheets
def conectar_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(os.environ['GOOGLE_CREDENTIALS']), scope)
        return gspread.authorize(creds)
    except Exception as e:
        logger.error(f"Erro ao conectar ao Google Sheets: {e}")
        raise

# Handlers (mantenha seus handlers existentes)
# ... [seus handlers aqui] ...

def main():
    # Obtenção das variáveis de ambiente
    TOKEN = os.environ['TELEGRAM_TOKEN']
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ['HEROKU_APP_NAME']
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Configuração do ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ESCOLHER_DIA: [MessageHandler(Filters.text & ~Filters.command, escolher_dia)],
            DATA: [MessageHandler(Filters.text & ~Filters.command, processar_dia)],
            # Adicione outros estados conforme necessário
        },
        fallbacks=[CommandHandler('cancel', cancelar)],
    )

    dp.add_handler(conv_handler)

    # Configuração do Webhook
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_NAME}.herokuapp.com/{TOKEN}"
    )
    updater.idle()

if __name__ == '__main__':
    main()
