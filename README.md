# Ejemplos de integración LangGraph & Flask

| Archivo       | Descripción                           | Características clave                               |
| ------------- | ------------------------------------- | --------------------------------------------------- |
| `example1.py` | Plantilla mínima de Flask + LangGraph | Chatbot básico con memoria, gestión de sesiones     |
| `example2.py` | Ejemplo simple de interrupción        | Flujo de trabajo con aprobación humana              |
| `example3.py` | Ejemplo simple de comando             | Enrutamiento dinámico con grafo sin definición de arcos          |
| `example4.py` | Interrupt + Command      | Enrutamiento basado en aprobación tras interrupción |

# Ejemplo 1 de LangGraph Flask

Sencilla aplicación Flask que demuestra cómo usar LangGraph con la API de OpenAI para crear un endpoint de chat.

## Prerrequisitos

Genera un archivo .env con tu OPENAI_API_KEY:

```
echo "OPENAI_API_KEY=tu_clave_openai_aquí" > .env
```

Crea un entorno virtual e instala las dependencias:

```bash
uv venv
source venv/bin/activate # en Windows usa `venv\Scripts\activate`
uv pip install -r requirements.txt
```

Ejecuta la aplicación Flask:

```bash
python example.py
```

En otra terminal, puedes probar el endpoint de chat usando curl:

```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "message": "¡Hola!"}'
```

## Ejercicio 1

- Modifica el código para que el agente recuerde el contexto de la conversación anterior incluso si el servidor se reinicia.

El objetivo es que el agente ejecutado tras la aplicación web recuerde nuestro nombre:

```bash
curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"user_id": "test", "message": "Hi, I am Juanan"}'
{
  "reply": "Hello Juanan! How can I assist you today?"
}
```

```bash
curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"user_id": "test", "message": "do you remember my name"}'
{
  "reply": "Yes, your name is Juanan."
}
```

# Ejemplo 2 de LangGraph Flask

Este ejemplo extiende el anterior añadiendo un nodo de interrupción que requiere aprobación humana para ciertos mensajes.

## Ejercicio 2

Indica la secuencia de comandos curl para probar el endpoint /start con un mensaje que active el interrupt y luego apruebe la solicitud.

# Ejemplo 3 de LangGraph Flask

Este ejemplo demuestra cómo usar nodos Command en LangGraph para enrutar mensajes dinámicamente según su contenido.

## Ejercicio 3
Indica la secuencia de comandos curl para probar el endpoint /process con un mensaje que contenga una solicitud de resumen y otro que no lo contenga.

# Ejemplo 4 de LangGraph Flask
Este ejemplo combina nodos con interrupt() y Command para crear un flujo de trabajo más complejo.

## Ejercicio 4
* Indica la secuencia de comandos curl para probar el agente.
* ¿Qué ocurre si el mensaje de aprobación es "approve" y a continuación se vuelve a enviar el mismo mensaje con un "reject"? ¿Por qué ocurre esto?

* Genera un nuevo endpoint /status que devuelva el nodo en el que se ha quedado el agente. Consulta https://reference.langchain.com/python/langgraph/graphs/ para conocer qué metodo podemos usar