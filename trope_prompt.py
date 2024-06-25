import openai 
from openai import OpenAI

def gerar_trope(sinopse, critics_consensu, audience_consensu):
    client= OpenAI(api_key = "")
    
    if critics_consensu != "empty" and audience_consensu != "empty":
        prompt= [{"role":"user", "content":"what is the most important trope of the movie with this sinopse: \
{} And those reviews: {} {} Tell me only the trope name.".format(sinopse, critics_consensu, audience_consensu)}]
    elif critics_consensu != "empty":
        prompt= [{"role":"user", "content":"what is the most important trope of the movie with this sinopse: \
{} And this review: {} Tell me only the trope name.".format(sinopse, critics_consensu)}]
    elif audience_consensu != "empty":
        prompt= [{"role":"user", "content":"what is the most important trope of the movie with this sinopse: \
{} And this review: {} Tell me only the trope name.".format(sinopse, audience_consensu)}]
    else:
        prompt= [{"role":"user", "content":"what is the most important trope of the movie with this sinopse: {} Tell me only the trope name.".format(sinopse)}]
        
    response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = prompt,
            max_tokens = 50,
            temperature = 1
        )

    trope = response.choices[0].message.content
    
    return trope