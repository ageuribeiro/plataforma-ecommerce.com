"""Importação de bibliotecas"""
import logging
import os
import uuid
import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest)-> func.HttpResponse:
    """Método principal"""
    try:
        # Dados do formulário
        nome = req.form['nome']
        imagem = req.form['imagem']


        # Conexao com o blob storage
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client("produtos")


        # Nome único para o arquivo
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)


        # Upload da Imagem
        blob_client.upload_blob(imagem.stream, overwrite=True)

        # URL pública
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/produtos/{blob_name}"

        # Resposta
        return func.HttpResponse(
            f'{{"nome": "{nome}", "url": "{blob_url}"}}',
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro no upload: {e}")
        return func.HttpResponse("Erro interno", status_code=500)
