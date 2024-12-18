import chainlit as cl
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
conversation_history = [
    {"role": "system", "content": "You are a renowned Harvard Professor, Professor Williams Andrew. You are known for your expertise in artificial intelligence, algorithms, and software engineering. You provide valuable insights on technology trends and mentor students, simplifying complex concepts through innovative teaching methods."}
]

@cl.on_chat_start
async def start():
    await cl.Message(
        content="Welcome! I'm Dr. Williams Andrew, a Professor of Computer Engineering at Harvard University. I'm here to address any queries my students may have. What would you like to know?",
        author="Dr. Williams Andrew",
    ).send()

@cl.on_message
async def main(message: cl.Message):
    try:
        conversation_history.append({"role": "user", "content": message.content})
        msg = cl.Message(content="", author="Dr. Williams Andrew")
        await msg.send()

        stream = client.chat.completions.create(
            messages=conversation_history,
            model="llama-3.2-90b-vision-preview",
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                full_response += content
                await msg.stream_token(content)

        conversation_history.append({"role": "assistant", "content": full_response})
        await msg.update()

    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}", author="Error").send()
