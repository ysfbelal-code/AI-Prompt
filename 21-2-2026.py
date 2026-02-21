import apikey
from huggingface_hub import InferenceClient

def generate_response(prompt, temperature=0.3, max_token=1024):
    MODELS=getattr(
        apikey, 
        "HF_MODELS",
        ['meta-llama/Llama-3.1-8B-Instruct']
    )
    key=getattr(apikey, 'hf_api', None)
    if not key:
        return "Error: hf_api missing in apikey.py"
    
    last_err=None
    for m in MODELS:
        try:
            c=InferenceClient(model=m, token=key)
            r=c.chat_completion(
                messages=[{'role': 'user', 'content': prompt}],
                temperature=temperature, 
                max_tokens=max_token
            )
            content=r.choices[0].message.content
            if content is not None:
                return content
        except Exception as e:
            last_err=e
    
    return (
        "Hugging Face model failed.\n"
        f'Tried models: {MODELS}\n'
        'Fix:\n'
        "1) Switch to Groq OR\n"
        "2) Replace HF model\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )

def main():
    print("Choose an option:")
    print("1) Bias Mitigation")
    print("2) Token Limit")
    choice=int(input("Enter your choice as a number: "))
    if choice==1:
        print("===== BIAS MITIGATION =====")
        bias_prompt=input("Enter a biased prompt (e.g 'Describe the ideal football player'):\n")
        print(generate_response(bias_prompt))
        neutral_prompt=input("Enter a neutral prompt (e.g 'Describe the qualities of a good doctor'):\n")
        print(generate_response(neutral_prompt))

        print("""
Reflection:
    1. How did the neutral prompt influence the response?
    2. Did you notice any bias or stereotype in the initial response?
    3. What can be done to avoid reinforcing biases in AI responses?""")

    elif choice==2:
        print("===== TOKEN LIMIT =====")
        long_prompt=input("Enter a long prompt (more than 300 words):\n")
        print(generate_response(long_prompt))
        condensed_prompt=input("Now, enter a concise version of that prompt (e.g 'Describe the qualities of a good doctor'):\n")
        print(generate_response(condensed_prompt))

        print("""
Reflection:
    1. How did the AI's response change what you condensed the prompt?
    2. Did the AI still provide enough detail? Did it omit any important information?
    3. How can understanding token limits help in optimizing AI responses?""")
  
main()