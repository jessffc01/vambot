import os
import logging
import json

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

# Configuração do log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados da conversação
ESCOLHER_DIA, DATA, HORA_INICIO, HORA_FIM, DESCRICAO = range(5)

# Função para conectar ao Google Sheets
def conectar_google_sheets():
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(os.environ['GOOGLE_SHEETS_CREDENTIALS']), scope)
        client = gspread.authorize(creds)
        sheet_id = os.environ['GOOGLE_SHEET_ID']
        sheet = client.open_by_key(sheet_id).sheet1  # A primeira aba
        return sheet
    except Exception as e:
        logger.error(f"Erro ao conectar ao Google Sheets: {e}")
        raise

# Handler de /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Você gostaria de adicionar um plantão? Responda com S para sim ou N para não")
    return ESCOLHER_DIA

# Handler escolhendo se vai inserir
def escolher_dia(update: Update, context: CallbackContext):
    resposta = update.message.text.strip().upper()
    if resposta == 'N':
        update.message.reply_text("Operação cancelada.")
        return ConversationHandler.END
    if resposta != 'S':
        update.message.reply_text("Responda S para sim ou N para não.")
        return ESCOLHER_DIA
    update.message.reply_text("Qual dia da semana foi o plantão?")
    return DATA

# Handler para processar o dia
def processar_dia(update: Update, context: CallbackContext):
    dia = update.message.text.strip()
    context.user_data['dia_semana'] = dia
    update.message.reply_text("Qual a data do plantão? (Formato: DD/MM/AAAA)")
    return HORA_INICIO

# Handler para processar hora início
def processar_hora_inicio(update: Update, context: CallbackContext):
    data = update.message.text.strip()
    context.user_data['data'] = data
    update.message.reply_text("Qual o horário de início? (Formato: HH:MM)")
    return HORA_FIM

# Handler para processar hora fim
def processar_hora_fim(update: Update, context: CallbackContext):
    hora_inicio = update.message.text.strip()
    context.user_data['hora_inicio'] = hora_inicio
    update.message.reply_text("Qual o horário de término? (Formato: HH:MM)")
    return DESCRICAO

# Handler para processar a descrição e salvar na planilha
def processar_descricao(update: Update, context: CallbackContext):
    hora_fim = update.message.text.strip()
    context.user_data['hora_fim'] = hora_fim
    update.message.reply_text("Adicione uma descrição (opcional, pode enviar só um ponto final).")
    return ConversationHandler.END  # Última etapa

# Handler final para gravar na planilha
def salvar(update: Update, context: CallbackContext):
    descricao = update.message.text.strip()
    context.user_data['descricao'] = descricao

    # Salvar na Google Sheets
    try:
        sheet = conectar_google_sheets()
        sheet.append_row([
            context.user_data.get('dia_semana', ''),
            context.user_data.get('data', ''),
            context.user_data.get('hora_inicio', ''),
            context.user_data.get('hora_fim', ''),
            descricao
        ])
        update.message.reply_text("Plantão registrado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao gravar na planilha: {e}")
        update.message.reply_text("Erro ao salvar na planilha. Fale com o admin.")
    return ConversationHandler.END

# Handler para cancelar a operação
def cancelar(update: Update, context: CallbackContext):
    update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

def main():
    # Variáveis de ambiente
    TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ['HEROKU_APP_NAME']

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ESCOLHER_DIA: [
                MessageHandler(Filters.text & ~Filters.command, escolher_dia)
            ],
            DATA: [
                MessageHandler(Filters.text & ~Filters.command, processar_dia)
            ],
            HORA_INICIO: [
                MessageHandler(Filters.text & ~Filters.command, processar_hora_inicio)
            ],
            HORA_FIM: [
                MessageHandler(Filters.text & ~Filters.command, processar_hora_fim)
            ],
            DESCRICAO: [
                MessageHandler(Filters.text & ~Filters.command, salvar)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancelar)],
    )

    dp.add_handler(conv_handler)

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{APP_NAME}.herokuapp.com/{TOKEN}"
    )

    updater.idle()

if __name__ == '__main__':
    main()
