import apikey
from openai import OpenAI
import colorama
from colorama import Fore,Style

colorama.init(autoreset=True)

groq_url="https://api.groq.com/openai/v1"
models=getattr(apikey, 'GROQ_MODELS', ['llama-3.1-8b-instant', 'mixtral-8x7b-32768'])

def gen_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    last_err = None
    key = getattr(apikey, 'groq_api', None)
    if not key:
        return "Error: groq_api missing in apikey.py"
    for m in models:
        try:
            c = OpenAI(api_key=key, base_url=groq_url)
            r = c.chat.completions.create(
                model=m,
                messages=[{'role': 'user', 'content': prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content or ""
        except Exception as e:
            last_err = e
    if last_err is None:
        return "Error: no models available"
    return f"Error: {last_err}"

vague = input(f'{Fore.CYAN}Enter a vague prompt: {Fore.WHITE}')
print(Fore.LIGHTBLACK_EX + gen_response(vague))

specific = input(f'{Fore.CYAN}Enter a specific prompt: {Fore.WHITE}')
print(Fore.LIGHTBLACK_EX + gen_response(specific, 0.3, 1024))

context = input(f'{Fore.CYAN}Enter a contextual prompt: {Fore.WHITE}')
print(Fore.LIGHTBLACK_EX + gen_response(context))

print(f'{Fore.CYAN}Please answer the following questions: ' \
        "1. How was the experience for you?" \
        "2. How was the AI' responses to your questions? " \
        "3. What is your feedback?")
review = input(Fore.WHITE)
print(Fore.LIGHTBLACK_EX + gen_response(review))