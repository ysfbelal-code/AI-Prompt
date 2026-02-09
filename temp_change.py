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

prompt = input(f'{Fore.CYAN}Enter a prompt: {Fore.WHITE}')
type = input(f"""{Fore.CYAN}Would you like a: 
    1. a 'technical' response, 
    2. a 'balanced' response, or         
    3. a 'creative' response? """
    f"\n{Fore.WHITE}")

if type.lower() == 'technical' or int(type) == 1:
    print(f'\n{Fore.LIGHTBLACK_EX}Here is the response at a temperature of 0.1-0.3 (clear explanation and predictable): \n', 
          gen_response(prompt, 0.2, 1024))
elif type.lower() == 'balanced' or int(type) == 2:
    print(f'\n{Fore.LIGHTBLACK_EX}Here is the response at a temperature of 0.4-0.6 (balance between clarity and creativity): \n',
        gen_response(prompt, 0.5, 1024))
elif type.lower() == 'creative' or int(type) == 3:
    print(f'\n{Fore.LIGHTBLACK_EX}Here is the response at a temperature of 0.7-0.9 (creative and less predictable): \n',
        gen_response(prompt, 0.8, 1024))
else:
    print(f'{Fore.MAGENTA}Invalid input! Defaulting to balanced response.')
    print(f'\n{Fore.LIGHTBLACK_EX} {gen_response(prompt, 0.5, 1024)}')

print(f"""\n{Fore.CYAN}Please answer the following questions:
    1. How was the experience for you?
    2. How was the AI' responses to your questions?
    3. What is your feedback?""")
review = input(Fore.WHITE)
print(Fore.LIGHTBLACK_EX + gen_response(review))