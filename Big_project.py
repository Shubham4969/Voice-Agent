import asyncio
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from Big_retraval import ask_rag
from Tools import get_weather, web_search
from llm import ask_llm

load_dotenv()
client = OpenAI()
async_client = AsyncOpenAI()

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions= "Speak in chairfull and positive tone.",
        response_format= "pcm"
    )as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()      

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  
        r.pause_threshold = 2

        SYSTEM_PROMPT = f"""
        -> You are an voice Agent. You are given a transcript of what user
            has says using audio.
        -> You need to output as if you are an voice agent and what ever you
            speak will be converted back to audio using AI and play back to user.
        
        """
        messages = [
            {"role":"system", "content": SYSTEM_PROMPT}
        ]

        while True:
            print("🎙️.....")
            audio = r.listen(source)
            
            print("Process Audio...(SST)" )
            sst = r.recognize_google(audio)

            if "weather" in sst.lower():
               query = sst.lower()
               
               city = query.replace("what is the weather of", "")
               city = city.replace("what is the weather in", "")
               city = city.replace("weather of", "")
               city = city.replace("weather in", "")
               city = city.strip().title()

               ai_response = get_weather.invoke({"city": city})
               print(ai_response)
               asyncio.run(tts(ai_response))
               continue

            if "hey news" in sst.lower():
                print("Search tool calling..")
                query = sst.lower()

                query = query.replace("hey news", "")
                query = query.strip()

                response = web_search.invoke({"query": query})
                print("Reaponse", response)
                asyncio.run(tts(response))
                continue


            exit_word = ["bey", "Ok bey", "quit", "stop", "bey chat", "exit"]
            if any(word in sst.lower() for word in exit_word):
                print("GoodBey!🙋")
                asyncio.run(tts("Have a good day 😊"))
                break
            print("You say:", sst)

            query = sst.lower()
            if any(word in query for word in [
                "employee",
                "handbook",
                "leave",
                "company",
                "policy"
            ]):          
                ai_response = ask_rag(sst)
            else:
                ai_response = ask_llm(sst)       
            print("AI Response:", ai_response)
            asyncio.run(tts(ai_response))
main()