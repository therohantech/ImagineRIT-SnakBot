import ollama
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

# Load Ollama model (change to your desired model)
model = Ollama(model="mistral")

# Custom behavior prompt
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
    You are a helpful AI assistant trained on custom knowledge. Answer questions based on the data provided.
    
    Question: {question}
    """
)

def chat():
    print("Ollama Chatbot - Type 'exit' to stop")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        prompt = prompt_template.format(question=user_input)
        response = model.invoke(prompt)
        print("Bot:", response)

if __name__ == "__main__":

    chat()
