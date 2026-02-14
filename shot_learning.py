import apikey
from huggingface_hub import InferenceClient

def gen_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512):
    MODELS = getattr(
        apikey, 
        "HF_MODELS", 
        ["meta-llama/Llama-3.1-8B-Instruct"],
    )

    key = getattr(apikey, "hf_api", None)
    if not key:
        return "Error: hf_api missing in apikey.py"
    
    last_err=None
    for m in MODELS:
        try:
            c=InferenceClient(model=m, token=key)
            r=c.chat_completion(
                messages=[{'role': 'user', 'content': prompt}], 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            content=r.choices[0].message.content
            if content is not None:
                return content
        except Exception as e:
            last_err = e

    return (
        'Hugging Face model failed.\n'
        f"Tried models: {MODELS}\n"
        "Fix:\n"
        "1) Switch to Groq by importing groq.py OR\n"
        "2) Replace HF model.\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )

def main():
    zsl_prompt=input("Enter a prompt:\n")
    print("\nZero-shot learning response:\n\n"+gen_response(zsl_prompt, 0.3, 1024))

    osl_prompt=input("""\nEnter a new prompt. 
One-Shot Learning Example:
    Category: Fruit
    Item: Apple
    Answer: Yes, an apple is a fruit.
Now it's your turn: 
""")
    print("\nOne-shot learning response:\n\n"+gen_response(osl_prompt, 0.3, 1024))

    fsl_prompt=input("""\n
Few-Shot Learning Example:
    Category: Fruit
    Item: Apple
    Answer: Yes, an apple is a fruit.
    
    Category: Vegetable
    Item: Mango
    Answer: No, a mango is not a vegetable.
    
    Now it's your turn: 
    """)
    print("\nFew-shot learning response:\n\n"+gen_response(fsl_prompt, 0.3, 1024))

    print('Please answer the following questions: '
        "\n1. How was the experience for you?"
        "\n2. How was the AI' responses to your questions? "
        "\n3. What is your feedback?")
    
    review = input()
    print(gen_response(review))

main()