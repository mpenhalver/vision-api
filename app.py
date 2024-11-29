import boto3
import base64
import json

# Cria cliente Bedrock
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)

# Função para processar imagem
def process_image_with_claude(image_path):
    # Converte imagem para base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Payload para API
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Descreva o que vê nesta imagem"
                    }
                ]
            }
        ]
    }

    # Chamada para API
    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0", 
        body=json.dumps(payload)
    )

    # Processa resposta
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# Exemplo de uso
resultado = process_image_with_claude('imagem.jpg')
print(resultado)