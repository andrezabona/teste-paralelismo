'''
TESTE 1
O objetivo desse programa é verificar a execução assíncrona de duas funções: fazer_ovo e fazer_suco
Pontos interessantes percebido:
- O asyncio.gather traz o resultado na ordem em que elas foram enviadas
- O tempo de processamento da função assíncrona não é mais a somatória dos processamentos individuais,
na verdade, fica o processamento maior (no caso, o do fazer_suco)
'''

import asyncio
import time

async def fazer_ovo() ->str:
    print('Start ovo')
    await asyncio.sleep(1)
    print('End ovo')
    return "Ovo feito"

async def fazer_suco()-> str:
    print('Start suco')
    await asyncio.sleep(2)
    print('End suco')
    return "Suco feito"

async def main():
    start_time = time.time()

    batch = asyncio.gather(fazer_suco(), fazer_ovo())
    result_suco, result_ovo = await batch # o batch vem com os resultados em sequencia!

    end_time = time.time()
    tempo_decorrido = end_time - start_time
    print(f"Resultado de fazer o ovo {result_ovo}")
    print(f"Resultado de fazer o suco {result_suco}")
    print(f"Tempo decorrido: {tempo_decorrido}")

if __name__ == "__main__":
    asyncio.run(main())