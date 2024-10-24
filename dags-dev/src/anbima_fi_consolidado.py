 # %%
import asyncio
from playwright.async_api import async_playwright
import os

async def download_file():
    # Configurações para o diretório de download
    # download_dir = os.path.join(os.getcwd(), "dags")

    async with async_playwright() as p:
        # Inicializa o navegador com headless = False
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            accept_downloads=True,
            viewport={"width": 1280, "height": 1024},
        )

        # Abre uma nova página
        page = await context.new_page()

        # Navega até o site
        await page.goto("https://www.anbima.com.br/pt_br/informar/estatisticas/fundos-de-investimento/fi-consolidado-diario.htm")

        # Aguarda até que o elemento esteja visível e clica nele
        element = await page.wait_for_selector('[data-anbima-arquivo-contentid]', timeout=10000)
        await element.click()

        # Aguarda o download e salva o arquivo no diretório especificado
        download = await page.wait_for_event("download")
        
        # Espera o download ser concluído
        download_path = download.path()
        print(f"Arquivo baixado para: {download_path}")

        # Mova o arquivo para o diretório de downloads
        new_file_path = os.path.join("include", download.suggested_filename)
        await download.save_as(new_file_path)

        print(f"Arquivo salvo em: {new_file_path}")

        # Fecha o contexto e o navegador
        await context.close()
        await browser.close()

# Verifica se estamos em um loop de eventos
if __name__ == "__main__":
    try:
        # Tenta rodar o loop de eventos
        asyncio.run(download_file())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            # Se já houver um loop em execução, obtemos o loop atual e executamos a corrotina
            loop = asyncio.get_event_loop()
            loop.run_until_complete(download_file())
        else:
            raise e