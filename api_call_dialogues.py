import requests
import json

def ask_llm(prompt):
    url = "http://10.xx.xxx.2xxx4:1234/v1/chat/completions"   

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    
    data = response.json()

   
    return data["choices"][0]["message"]["content"]



if __name__ == "__main__":
    prompt = "Explain quantum computers in one paragraph."
    reply = ask_llm(prompt)
    print("\nLLM Response:\n", reply)
