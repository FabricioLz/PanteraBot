import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from openai import OpenAI
import whisper
import os


# TOKEN e chave API
api_telegram = "API-BOT-TELEGRAM"
TOKEN = api_telegram
openrouterkey = "API-ROUTER"  # api key openrouter
model_mistral = "mistralai/mistral-7b-instruct:free"


user_histories = {}

def open_ai(user_id: str, text: str) -> str:
    """
    Função que envia uma mensagem para a API OpenAI (openrouter.ai)
    e retorna a resposta, mantendo o histórico de conversa.
    """

    if user_id not in user_histories:
        user_histories[user_id] = []

   
    user_histories[user_id].append({"role": "user", "content": text})

   
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouterkey,
    )


    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  
            "X-Title": "<YOUR_SITE_NAME>",      
        },
        model=model_mistral,
        messages=user_histories[user_id]
    )

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
        await update.message.reply_text("Desculpe, não entendi... Vamos tentar novamente?")
        print(f"Erro ao chamar open_ai: {e}")


#transcrição de audio para prompt
model_whisper = whisper.load_model("base")

async def handle_voice(update: Update, context: CallbackContext) -> None:
    """Recebe uma mensagem de voz, transcreve localmente e envia como prompt."""
    user_id = update.message.from_user.id

    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)

        audio_path_ogg = f"audio_{user_id}.ogg"
        audio_path_wav = f"audio_{user_id}.wav"

        await file.download_to_drive(audio_path_ogg)

        os.system(f"ffmpeg -i {audio_path_ogg} -ar 16000 -ac 1 {audio_path_wav}")

       
        result = model_whisper.transcribe(audio_path_wav)
        transcript = result["text"]

       
        response = await asyncio.to_thread(open_ai, user_id, transcript)
        await update.message.reply_text(response)

        # Limpa os arquivos temporários
        os.remove(audio_path_ogg)
        os.remove(audio_path_wav)

    except Exception as e:
        await update.message.reply_text("Não entendimuito bem... Pode falar denovo?")
        print(f"Erro ao transcrever/processar áudio: {e}")

def main():

    """Configura e inicia o bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
