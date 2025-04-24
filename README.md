# PanteraBot
O PanteraBot é um bot de Telegram feito em Python, com integração à API da plataforma OpenRouter, com capacidade de memória de conversa por usuário. Ele simula diálogos com contexto e continuidade, ideal para uma experiência imersiva de atendimento ou interação com fãs da FURIA.

## Tecnologias e APIs Utilizadas
Python – Linguagem principal.

Telegram Bot API – Para criar o bot e interagir com usuários.
OpenRouter – Plataforma intermediária para acesso a diversos modelos de linguagem (neste caso, Mistral).

FFmpeg - Transcrição de audio para texto-prompt

## Modelos utilizados:
mistralai/mistral-7b-instruct:free
openai/gpt-4o (exemplo separado incluído)

Dialogflow (Google Cloud) – Mencionado como base teórica de inspiração para gerenciamento de conversas e intents.

API utilizada: Text-to-Text Translation API (Google Cloud).

## Como Funciona

Usuário envia uma mensagem no Telegram
O bot recebe a mensagem através do MessageHandler da biblioteca `python-telegram-bot`.

**Identificação do Usuário**
- O `user_id` é capturado para diferenciar as conversas de cada pessoa.

**Histórico de mensagens para cada usuário**
- O dicionário `user_histories` é usado para manter um histórico separado para cada usuário.

**Recupera o histórico das mensagens ou cria um novo para o usuário**
- Se for a primeira mensagem do usuário, cria-se uma nova lista de histórico. Se já houver interações anteriores, o histórico é carregado.

**Adiciona a nova mensagem do usuário ao histórico**
- A mensagem recém-enviada é adicionada como entrada do tipo `{"role": "user", "content": texto}` no histórico.

**Envia o histórico completo para a API para manter o contexto**
- Todo o histórico de mensagens é enviado para a API do OpenRouter, permitindo ao modelo considerar o contexto da conversa anterior.

**Obtém a resposta do bot e adiciona ao histórico** 
- A resposta gerada pela IA é adicionada ao histórico com `{"role": "assistant", "content": resposta}` para garantir a continuidade nas próximas mensagens.

Resposta enviada de volta ao Telegram
A resposta gerada é enviada de volta ao usuário através da função reply_text() do Telegram.

## Transcrição de audio para prompt

1. Baixa o arquivo `.ogg` com await `file.download_to_drive(...)`.

2. Converte para `.wav` (se necessário).

3. Usa o Whisper local para transcrever.

4. O texto transcrito é enviado como prompt para a IA (OpenRouter).
   
## Como Rodar Localmente
```
  git clone https://github.com/FabricioLz/PanteraBot/.git
  cd nome-do-repo
```
### Dependencias

ffmpeg para o audio

Baixe em: https://www.gyan.dev/ffmpeg/builds/

Extraia e adicione à variável de ambiente `PATH` o caminho da pasta `bin`.

```
pip install python-telegram-bot openai-whisper requests

```
### Configure suas chaves de API no código:
No arquivo bot.py, altere:
```
api_telegram = "SUA_CHAVE_DO_BOT_DO_TELEGRAM"
social_credit = "SUA_CHAVE_DA_API_OPENROUTER"
```
### Inicie o bot.

>## Observações
>1. Este bot não possui conexão com a internet em tempo real. Os modelos usados são pré-treinados com dados até 2022.
>2. Os modelos disponíveis gratuitamente no OpenRouter (como o Mistral) não acessam dados atualizados da internet.
>3. A memória de conversa existe apenas durante a execução — se o script for  finalizado, a memória será perdida.


