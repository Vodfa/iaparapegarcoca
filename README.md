# iaparapegarcoca

Robô local integrado com Ollama, YOLO, Arduino Leonardo, microfone e caixa de som.

## Recursos principais
- **IA local via Ollama** com o modelo `chatgpt-120oss`.
- **Visão computacional com YOLO** para detectar objetos.
- **Estimativa de distância** usando:
  - Sensor via Arduino (modo `sensor`).
  - Estimativa visual pelo tamanho da caixa delimitadora (modo `vision`).
- **Controle do Arduino Leonardo** para levantar, mover braço, pegar/soltar e andar.
- **Microfone + TTS** para conversar com o usuário.

## Pré-requisitos
- Python 3.10+
- Ollama rodando localmente (`ollama serve`)
- Modelo YOLO disponível (`yolov8n.pt`)
- Arduino Leonardo conectado na porta correta

## Instalação
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configurações
Existem duas versões prontas:
- **Com sensor de distância:** `config/robot_with_sensor.yaml`
- **Sem sensor (estimativa visual):** `config/robot_no_sensor.yaml`

Ajuste as portas, câmera e modelo conforme o seu ambiente.

## Executar
```bash
python main.py --config config/robot_with_sensor.yaml
```

ou

```bash
python main.py --config config/robot_no_sensor.yaml
```

## Protocolo Arduino (exemplo)
O sketch do Arduino deve responder a comandos simples (uma linha):
- `LIFT`
- `ARM:<angulo>`
- `GRAB`
- `RELEASE`
- `WALK:<direction>:<steps>`
- `ROTATE:<direction>:<degrees>`
- `DIST` (retorna `OK:DIST:<metros>`)

Adapte o firmware conforme o hardware do robô.
