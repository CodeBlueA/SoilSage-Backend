from os import getcwd
from gpt4all import GPT4All


class Llm :
    def __init__(self, *args, **kwargs) :
        self.gpt = GPT4All(model_name= "mistral-7b-instruct-v0.1.Q4_0.gguf",
                      model_path=(getcwd()),
                      allow_download=True)
    
        self.system_template = 'A chat between a curious user and an artificial intelligence assistant expert at botany.'
        self.prompt_template = 'USER: {0}\nASSISTANT: '
    
    def llm_response(self, prompt) :
        with self.gpt.chat_session(self.system_template, self.prompt_template):
            response1 = self.gpt.generate(prompt)
            print(response1)
            
            return response1
        
if __name__ == "__main__" :
    llm = Llm()
    res = llm.llm_response('What are some common diseases for plants?')