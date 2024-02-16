'''
TESTE 2
O objetivo desse programa é verificar como poderíamos chamar várias funções assincronas no mesmo asyncio.gather
Perceba que para isso usamos um artificio de list compreension (for _ in _) + unpack (*)
Ao mesmo tempo, queríamos testar o uso de "create_task"
'''

import asyncio
import time

async def fazer_ovo(coisa:str) -> str:
    print(f'Start {coisa}')
    await asyncio.sleep(1)
    print(f'End {coisa}')
    return f"{coisa} feito"

async def fazer_suco(coisa:str) -> str:
    print(f'Start {coisa}')
    await asyncio.sleep(2)
    print(f'End {coisa}')
    return f"{coisa} feito"

async def fazer_coisa(coisa:str) -> str:
    if 'suco' in coisa:
        suco = asyncio.create_task(fazer_suco(coisa))
        result_suco = await suco
        print(f'{coisa} feita!')
        return result_suco
    if 'ovo' in coisa:
        ovo = asyncio.create_task(fazer_ovo(coisa))
        result_ovo = await ovo
        print(f'{coisa} feita!')
        return result_ovo


async def main():
    start_time = time.time()

    comidas = ['suco1','suco2','ovo1','ovo2']
    batch = asyncio.gather(*(fazer_coisa(coisa) for coisa in comidas))
    resultado = await batch
    end_time = time.time()
    tempo_decorrido = end_time - start_time
    print(f"Resultado: {resultado}")
    print(f"Tempo decorrido: {tempo_decorrido}")

if __name__ == "__main__":
    asyncio.run(main())