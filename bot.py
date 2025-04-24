
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from openai import OpenAI

# TOKEN e chave API
api_telegram = "API-BOT-TELEGRAM"
TOKEN = api_telegram
openrouterkey = "API-OPENROUTER"  # api key openrouter
model_mistral = "mistralai/mistral-7b-instruct:free"

# Histórico de mensagens para cada usuário
user_histories = {}

def open_ai(user_id: str, text: str) -> str:
    """
    Função que envia uma mensagem para a API OpenAI (openrouter.ai)
    e retorna a resposta, mantendo o histórico de conversa.
    """
    # Recupera o histórico das mensagens ou cria um novo para o usuário
    if user_id not in user_histories:
        user_histories[user_id] = []

    # Adiciona a nova mensagem do usuário ao histórico
    user_histories[user_id].append({"role": "user", "content": text})

    # Configura a chamada para a API
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouterkey,
    )

    # Envia o histórico completo para a API para manter o contexto
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Opcional
            "X-Title": "<YOUR_SITE_NAME>",       # Opcional
        },
        model=model_mistral,
        messages=user_histories[user_id]
    )

    # Obtém a resposta do bot e adiciona ao histórico
    bot_message = completion.choices[0].message.content
    user_histories[user_id].append({"role": "assistant", "content": bot_message})

    return bot_message

async def start(update: Update, context: CallbackContext) -> None:
    """Responde ao comando /start."""
    await update.message.reply_text("Fala furioso! Como posso ajudar?")

async def echo(update: Update, context: CallbackContext) -> None:
    """Recebe uma mensagem e retorna a resposta da API OpenAI."""
    user_id = update.message.from_user.id
    text = update.message.text
    try:
        response = await asyncio.to_thread(open_ai, user_id, text)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Desculpe, ocorreu um erro ao processar sua solicitação.")
        print(f"Erro ao chamar open_ai: {e}")

def main():
    """Configura e inicia o bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()


