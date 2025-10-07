# LangGraph & Flask integration Examples

| File | Description | Key Features |
|------|-------------|--------------|
| `example1.py` | Minimal Flask + LangGraph template | Basic chatbot with memory, session management |
| `example2.py` | Simple Interrupt example | Human-in-the-loop approval workflow |
| `example3.py` | Simple Command example | Dynamic routing with edgeless graph |
| `example4.py` | Combined Interrupt + Command | Approval-based routing after interrupt |


# LangGraph Flask Example 1

This is a simple Flask application that demonstrates how to use LangGraph with OpenAI's API to create a chat endpoint.

## Prerequisites
Generate .env file with your OpenAI API key:

echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

Generate a virtual environment and install dependencies:

```bash
uv venv 
source venv/bin/activate
uv pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

In another terminal, you can test the chat endpoint using curl:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "message": "Hello!"}'
```

## Ejercicio 1
* Modifica el código para que el agente recuerde el contexto de la conversación anterior incluso si el servidor se reinicia.

# LangGraph Flask Example 2

This example extends the previous one by adding an interrupt node that requires human approval for certain messages.

## Ejercicio 2

Indica la secuencia de comandos curl para probar el endpoint /start con un mensaje que active el interruptor y luego apruebe la solicitud.

# LangGraph Flask Example 3

This example demonstrates how to use command nodes in LangGraph to route messages dynamically based on their content.

## Ejercicio 3
Indica la secuencia de comandos curl para probar el endpoint /process con un mensaje que contenga una solicitud de resumen y otro que no lo contenga.

# LangGraph Flask Example 4
This example combines both interrupt and command nodes to create a more complex workflow.

## Ejercicio 4
* Indica la secuencia de comandos curl para probar el agente.
* ¿Qué ocurre si el mensaje de aprobación es "approve" y a continuación se vuelve a enviar el mismo mensaje con un "reject"? ¿Por qué ocurre esto?