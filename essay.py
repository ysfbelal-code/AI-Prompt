import apikey
from openai import OpenAI
from colorama import init, Fore, Style

init(autoreset=True)

groq_url="https://api.groq.com/openai/v1"
models = getattr(apikey, 'GROQ_MODELS', ['llama-3.1-8b-instant', 'mixtral-8x7b-32768'])

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 1024)->str:
    last_err = None
    key = getattr(apikey, 'groq_api', None)
    if not key:
        return "Error: groq_api missing in apikey.py"
    for m in models:
        try:
            c = OpenAI(api_key=key, base_url=groq_url)
            r = c.chat.completions.create(
                model=m, 
                messages = [{'role': 'user', 'content': prompt}], 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            content = r.choices[0].message.content
            if content is not None:
                return content
        except Exception as e:
            last_err  = e
        if last_err is None:
            return "Error: no models available"
    return f"Error: {last_err}"

print("=== AI ESSAY ASSISTANT === ")
mode = None
while mode != 3:
    mode = int(input("Choose an activity -> 1. Whole Essay Generation, 2. Step-by-step Generation, or 3. Quit.\nChoose by number: "))
    if mode == 1:
        prompt = input("What do you want to talk about in your essay??\n")
        ai_prompt = f"Subject: {prompt}. Do not drift into a whole discussion. This is suppossed to be an essay."
    elif mode == 3:
        print("Goodbye!")
        break
    elif mode == 2:
        genre = input("What is the theme of your essay (e.g Sports)?\n").lower()
        subject = input(f"What thing relating to {genre} do you want to talk about?\n").lower()
        audience = input("What audience is this essay for?\n").strip()
        ai_prompt = f"I want to make an essay about {subject} in the field of {genre}. The essay should appeal to a {audience} audience. Do not drift into a whole discussion. This is suppossed to be an essay."
    else:
        print("Invalid input. Choose an activity -> 1. Whole Essay Generation, 2. Step-by-step Generation, or 3. Quit. Choose by number:")
        while mode > 3 or mode < 1 or mode is None:
            mode = int(input())
    
    temp = float(input("Enter a temperature for the response (0.1 - technical and deterministic, 0.9 - imaginative and random):\n"))
    if temp < 0.1 or temp > 0.9 or temp is None:
        print("Invalid input. Defaulting temperature to 0.3")
        temp = 0.3
    
    response = generate_response(prompt=ai_prompt, temperature=temp, max_tokens=1024)
    print(f"AI Response:\n\n{response}")