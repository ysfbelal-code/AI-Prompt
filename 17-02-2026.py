import apikey
from openai import OpenAI

URL="https://api.groq.com/openai/v1"
MODELS=getattr(apikey, "GROQ_MODELS", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])

def generate_response(prompt:str, temperature:float=0.3, max_tokens:int=512) -> str:
    key=getattr(apikey, "groq_api", None)
    if not key:
        return "ERROR: groq_api key missing in apikey.py/config.py"
    
    c=OpenAI(api_key=key, base_url=URL)
    
    last_err=None
    for m in MODELS:
        try:
            r=c.chat.completions.create(
                model=m,
                messages=[{'role':'user', 'content':prompt}], 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            content = r.choices[0].message.content
            if content is not None:
                return content
        except Exception as e:
            last_err=e
    
    return (
        "Groq model failed.\n"
        "Fix:\n"
        "1) Switch to hf by importing hf.py OR\n"
        "2) Replace Groq model in MODELS\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )

def reinforcement_learning_activity():
    print("\n=== REINFORCEMENT LEARNING ACTIVITY ===\n")
    prompt = input("Enter a prompt for the AI model (e.g., 'Describe the lion'): ").strip()
    if not prompt:
        print("Please enter a prompt to run the activity.")
        return

    initial_response = generate_response(prompt, temperature=0.3, max_tokens=1024)
    print(f"\nInitial AI Response: {initial_response}")

    # Rating + feedback (simulated RL)
    try:
        rating = int(input("Rate the response from 1 (bad) to 5 (good): ").strip())
        if rating < 1 or rating > 5:
            print("Invalid rating. Using 3.")
            rating = 3
    except ValueError:
        print("Invalid rating. Using 3.")
        rating = 3

    feedback = input("Provide feedback for improvement: ").strip()
    improved_response = f"{initial_response} (Improved with your feedback: {feedback})"
    print(f"\nImproved AI Response: {improved_response}")

    print("\nReflection:")
    print("1. How did the model's response improve with feedback?")
    print("2. How does reinforcement learning help AI to improve its performance over time?")

def role_based_prompt_activity():
    print("\n=== ROLE-BASED PROMPTS ACTIVITY ===\n")
    category = input("Enter a category (e.g., science, history, math): ").strip()
    item = input(f"Enter a specific {category} topic (e.g., 'photosynthesis' for science): ").strip()

    if not category or not item:
        print("Please fill in both fields to run the activity.")
        return

    teacher_prompt = f"You are a teacher. Explain {item} in simple terms."
    expert_prompt = f"You are an expert in {category}. Explain {item} in a detailed, technical manner."

    teacher_response = generate_response(teacher_prompt, temperature=0.3, max_tokens=1024)
    expert_response = generate_response(expert_prompt, temperature=0.3, max_tokens=1024)

    print(f"\n--- Teacher's Perspective ---\n{teacher_response}")
    print(f"\n--- Expert's Perspective ---\n{expert_response}")

    print("\nReflection:")
    print("1. How did the AI's response differ between the teacher's and expert's perspectives?")
    print("2. How can role-based prompts help tailor AI responses for different contexts?")

def activity():
    print(
"""\n=== AI Learning Activity ===
Choose an activity:
    1) Reinforcement Learning
    2) Role-Based Prompts""")
    choice=input(">>> ").strip()

    if choice=='1':
        reinforcement_learning_activity()
    elif choice=='2':
        role_based_prompt_activity()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__=='__main__':
    activity()