'''
TESTE 5
O objetivo desse programa é simular a chamada da API da engenharia para API centralizadora.
Agora vou realmente fazer uma requisição a alguma api qualquer na internet
Quero retornar tbm quantos segundos cada chamada demorou.
'''
import asyncio
import time
import aiohttp
from datetime import datetime
import csv
import pandas as pd

async def fazer_requisicao(mini_batch: str):
    """
    Função que chama de fato a API da engenharia
    """
    print(f'Start {mini_batch}')
    start = time.time()
    timeout = aiohttp.ClientTimeout(total=1.5) # Não é necessario esse timeout pois já temos o da task em si que é obrigatório.
    async with aiohttp.ClientSession(timeout=timeout) as session:
        result_post = await session.post("https://jsonplaceholder.typicode.com/posts", json=mini_batch)
        response_data = await result_post.json()

    print(f'End {mini_batch}')
    end = time.time()
    tempo_decorrido = end - start
    return [response_data, tempo_decorrido]


async def main():
    # URL da API pública
    url = "https://jsonplaceholder.typicode.com/posts"
    start_time = time.time()
    batches = [{
        "title": "Mini batch 1",
        "body": "Este é o conteúdo do meu novo post 1.",
        "userId": 1
    },
    {
        "title": "Mini batch 2",
        "body": "Este é o conteúdo do meu novo post 2.",
        "userId": 2
    },
    {
        "title": "Mini batch 3",
        "body": "Este é o conteúdo do meu novo post 3.",
        "userId": 3
    }]


    tasks = []
    for mini_batch in batches:
        task = asyncio.create_task(asyncio.wait_for(fazer_requisicao(mini_batch), timeout=1.5))
        tasks.append(task)

    responses = []
    for task in tasks:
        try:
            result_task = await task # A task so vai ser de fato executada aqui nessa linha...
            responses.append(result_task)
        except asyncio.TimeoutError:
            responses.append([500,"falhou devido ao tempo limite"])

    end_time = time.time()
    tempo_total_decorrido = end_time - start_time
    print(f"Resultado: {responses}")
    print(f"Tempo decorrido: {tempo_total_decorrido}")
  
    ####################################################################
    # salvando as respostas em um dataframe e depois salvando como csv # 
    ####################################################################
    responses_dataframe = pd.DataFrame(responses, columns=["response", "tempo_decorrido"])
    print(responses_dataframe)
    responses_dataframe.to_csv(f"teste_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)
    # with open(f"teste_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(responses)
    
if __name__ == "__main__":
    asyncio.run(main())
