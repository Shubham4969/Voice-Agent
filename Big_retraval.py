from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model= "text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding= embedding_model,
    url="http://localhost:6333",
    collection_name="Big_project"
)

def ask_rag (user_query: str):

    search_results = vector_db.similarity_search(query=user_query)

    context = "\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
    f"File Location: {result.metadata.get('source', 'Unknown')}"
    for result in search_results
    ])

    SYSTEM_PROMPT = f"""
        
            You are an AI Customer Support Assistant.

            Answer the user's question only using the provided context.

            The context may come from:
            - PDF documents
            - Websites
            - YouTube transcripts

            If multiple sources provide the same information, combine them into one clear answer.

            If the sources contradict each other, clearly mention the contradiction.

            Always mention the source of the information:
            - PDF name and page number
            - Website URL
            - YouTube timestamp

            If the answer is not present in the context, reply:

            "I couldn't find this information in the available documents."

            Context:
            {context}

        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content":SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message.content



import os
import tempfile

import gradio as gr
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

TIMEOUT = 120


def transcribe_audio(audio_path):
    """Send recorded audio to the FastAPI transcription endpoint."""
    if not audio_path:
        return ""

    try:
        with open(audio_path, "rb") as audio_file:
            response = requests.post(
                f"{API_BASE_URL}/transcribe",
                files={
                    "file": (
                        os.path.basename(audio_path),
                        audio_file,
                        "audio/wav",
                    )
                },
                timeout=TIMEOUT,
            )

        response.raise_for_status()
        data = response.json()

        # Supports common transcription response formats.
        return data.get("text", data.get("transcription", ""))

    except requests.RequestException as exc:
        raise gr.Error(
            f"Transcription failed: {exc}"
        ) from exc


def chat_with_agent(message, history):
    """Send a text message to the FastAPI agent."""
    message = (message or "").strip()

    if not message:
        return history, "", None

    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        data = response.json()
        answer = data.get(
            "response",
            data.get("answer", data.get("message", ""))
        )

        if not answer:
            raise gr.Error(
                "The backend returned no response text."
            )

        # Optional: the backend can return an audio URL.
        audio_url = data.get("audio_url")

        updated_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": answer},
        ]

        return updated_history, "", audio_url

    except requests.RequestException as exc:
        raise gr.Error(
            f"Could not contact the voice agent: {exc}"
        ) from exc


def process_voice(audio_path, history):
    """Transcribe a recording, get the answer, and play audio."""
    if not audio_path:
        raise gr.Error("Please record a message first.")

    transcript = transcribe_audio(audio_path)

    if not transcript.strip():
        raise gr.Error("No speech was detected.")

    updated_history, _, audio_url = chat_with_agent(
        transcript, history
    )

    # If the chat endpoint returned audio_url, Gradio can play it.
    # Otherwise, the text answer is still displayed.
    return updated_history, transcript, audio_url


def clear_chat():
    return [], "", None


with gr.Blocks(title="AI Voice Agent") as demo:

    gr.Markdown(
        """
        # 🎙️ AI Voice Agent
        Chat with your AI assistant using text or your microphone.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation",
                height=430,
                                )

            message = gr.Textbox(
                label="Your message",
                placeholder="Type a message and press Enter...",
                lines=2,
            )

            with gr.Row():
                send_btn = gr.Button(
                    "Send",
                    variant="primary",
                )
                clear_btn = gr.Button("Clear chat")

        with gr.Column(scale=2):
            microphone = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Speak to your assistant",
            )

            voice_btn = gr.Button(
                "🎤 Send voice message",
                variant="primary",
            )

            transcript_box = gr.Textbox(
                label="Recognized speech",
                interactive=False,
            )

            response_audio = gr.Audio(
                label="Assistant voice response",
                autoplay=True,
            )

    send_btn.click(
        fn=chat_with_agent,
        inputs=[message, chatbot],
        outputs=[chatbot, message, response_audio],
    )

    message.submit(
        fn=chat_with_agent,
        inputs=[message, chatbot],
        outputs=[chatbot, message, response_audio],
    )

    voice_btn.click(
        fn=process_voice,
        inputs=[microphone, chatbot],
        outputs=[chatbot, transcript_box, response_audio],
    )

    clear_btn.click(
        fn=clear_chat,
        inputs=[],
        outputs=[chatbot, message, response_audio],
    )


if __name__ == "__main__":
    demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
    )

