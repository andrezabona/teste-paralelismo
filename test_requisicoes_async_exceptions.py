'''
TESTE 4
O objetivo desse programa é simular a chamada da API da engenharia para API centralizadora.
Porém, dessa vez, queria que se uma requisição demorasse mais do que 2.4 segundos, ela fosse simplesmente deixada para la
e na fila de respostas, a posição dela fosse preenchida com "falhou devido ao tempo limite"
'''

import asyncio
import time


async def fazer_requisicao(mini_batch: str):
    """
    Função que simula um pod da centralizadora, respondendo cada requisição a 2 segundos
    """
    print(f'Start {mini_batch}')

    if mini_batch == 'mini_batch_1':
        await asyncio.sleep(5)  # simulando o primeiro mini_batch ir para um pod lento...
    else:
        await asyncio.sleep(2)

    print(f'End {mini_batch}')
    return f"{mini_batch} feito"


async def main():
    start_time = time.time()

    batches = ['mini_batch_1', 'mini_batch_2', 'mini_batch_3', 'mini_batch_4']
    tasks = []
    for mini_batch in batches:
        task = asyncio.create_task(asyncio.wait_for(fazer_requisicao(mini_batch), timeout=2.4))
        tasks.append(task)

    responses = []
    for task in tasks:
        try:
            result = await task # A task so vai ser de fato executada aqui nessa linha...
            responses.append(result)
        except asyncio.TimeoutError:
            responses.append("falhou devido ao tempo limite")

    end_time = time.time()
    tempo_decorrido = end_time - start_time
    print(f"Resultado: {responses}")
    print(f"Tempo decorrido: {tempo_decorrido}")


if __name__ == "__main__":
    asyncio.run(main())