'''
TESTE 5
O objetivo desse programa é mostrar como chamar uma api de forma paralela usando asyncio
Irei mandar 3 requisições em paralelo e vou salvar quantos segundos cada chamada demorou.
'''
import asyncio
import time
import aiohttp
from pandas import DataFrame
from datetime import datetime
import csv

async def fazer_requisicao(mini_batch: str, url: str):
    """
    Função que chama de fato a API da engenharia
    Input:
        mini_batch = payload da requisição
        url = endpoint que será acionado via post, passando o payload mini_batch
    Output:
        lista -> [resposta, tempo decorrido]
    """
    print(f'Start {mini_batch}')
    start = time.time()
    
    timeout = aiohttp.ClientTimeout(total=1.5) # Não é necessario esse timeout pois já temos o da task em si que é obrigatório.
    async with aiohttp.ClientSession(timeout=timeout) as session:
        result_post = await session.post(url, json=mini_batch)
        response_data = await result_post.json()

    print(f'End {mini_batch}')
    end = time.time()
    tempo_decorrido = end - start
    return [response_data, tempo_decorrido]


async def main():
    # URL da API pública
    start_time = time.time()
    url = "https://jsonplaceholder.typicode.com/posts"
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
        task = asyncio.create_task(asyncio.wait_for(fazer_requisicao(mini_batch, url), timeout=1.5))
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

    #####################################################################
    # SALVANDO AS RESPOSTAS EM UM DATAFRAME E DEPOIS SALVANDO EM UM CSV #
    #####################################################################
    responses_dataframe = DataFrame(responses, columns=["response", "tempo_decorrido"])
    responses_dataframe.to_csv(f"teste_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)
    print(responses_dataframe)
    # with open(f"teste_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(responses)
    


if __name__ == "__main__":
    asyncio.run(main())