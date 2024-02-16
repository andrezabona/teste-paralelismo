'''
TESTE 3
O objetivo desse programa é simular a chamada da API da engenharia para API centralizadora...
'''

import asyncio
import time


async def fazer_requisicao(mini_batch: str) -> str:
    """
    Função que simula um pod da centralizadora, respondendo cada requisição a 2 segundos
    """
    print(f'Start {mini_batch}')

    if mini_batch == 'mini_batch_1':
        await asyncio.sleep(5) #simulando o primeiro mini_batch ir para um pod lento...
    else:
        await asyncio.sleep(2)
    
    print(f'End {mini_batch}')
    return f"{mini_batch} feito"


async def main():
    start_time = time.time()

    batches = ['mini_batch_1','mini_batch_2','mini_batch_3','mini_batch_4']
    # Aqui vamos mandar 4 requisições em paralelo para 4 pods diferentes...
    responses = asyncio.gather(*(fazer_requisicao(mini_batch) for mini_batch in batches))
    # O resultado vem ordenado pela fila que mandei e não pelo tempo de execução!!!
    # Ou seja, o primeiro que eu mandei vai ser o primeiro da lista de retorno, mesmo que seja o mais demorado a ser resolvido...
    # Ah mas e se o primeiro demorar demais ou falhar? vai engargalar? Otima pergunta! Para isso, podemos definir um timeout... (olhe o codigo test_requisicoes_async_exceptions.py)
    resultado = await responses
    
    end_time = time.time()
    tempo_decorrido = end_time - start_time
    print(f"Resultado: {resultado}")
    print(f"Tempo decorrido: {tempo_decorrido}")

if __name__ == "__main__":
    asyncio.run(main())