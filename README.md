# Alura Agente — NBA2K Tournament Hub

Agente de inteligencia artificial que responde preguntas en lenguaje natural sobre las reglas, equipos y formato de un torneo NBA2K, construido con LangChain y Gemini.

<p align="center">
  <img width="300" height="300" alt="badge-rag-agente-ia" src="https://github.com/user-attachments/assets/64b61599-98f0-4239-9c2d-00737822195a" />
</p>


## 📌 Descripción general

Este proyecto resuelve el problema de tener que leer manualmente un documento extenso (reglas y descripción del torneo) para encontrar una información puntual. El agente permite hacerle preguntas directas ("¿cuántos equipos participan?", "¿cuál es el formato de eliminación?") y recibir la respuesta al instante, basada en el contenido del documento.

Además, el agente es **híbrido**: también puede responder preguntas generales sobre la NBA y el baloncesto (por ejemplo, sobre jugadores, historia o reglas oficiales) usando su propio conocimiento, sin salirse del tema del torneo es decir, si la pregunta es sobre el torneo, siempre prioriza la información del documento por encima de su conocimiento general, y si algo específico del torneo no está en el documento, lo dice claramente en vez de inventarlo.

## 🏗️ Arquitectura

```
                 ┌─────────────────────┐
                 │  Documento (PDF)     │
                 │  Reglas del torneo   │
                 └──────────┬───────────┘
                            │ PyPDFLoader
                            ▼
                 ┌──────────────────────┐
                 │  Text Splitter        │  chunks de ~1000 caracteres
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Embeddings (Gemini)  │  models/gemini-embedding-001
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Base vectorial FAISS │
                 └──────────┬───────────┘
                            │ retriever (top k=4)
                            ▼
                 ┌──────────────────────┐
                 │  LLM: Gemini 3.6      │  Cadena LCEL (LangChain)
                 │  Flash                │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  App Streamlit        │  desplegada en Streamlit
                 │  (streamlit_app.py)   │  Community Cloud
                 └──────────────────────┘
```

## 🛠️ Tecnologías utilizadas

- **Python**
- **LangChain** — orquestación del agente (carga de documento, splitting, cadena de recuperación y respuesta)
- **Google Gemini** (`gemini-3.6-flash` + `gemini-embedding-001`) — modelo de lenguaje y embeddings
- **FAISS** — base de datos vectorial
- **PyPDF** — lectura del documento PDF
- **Streamlit** — interfaz web para el deploy
- **Google Colab** — prototipado del agente
- **Streamlit Community Cloud** — despliegue en la nube (gratis)

## 🚀 Instrucciones para ejecutar el proyecto

### 1. Prototipo en Google Colab

1. Abre `Alura_Agente.ipynb` en Google Colab.
2. Ejecuta las celdas en orden.
3. Cuando se te pida, ingresa tu [Google API Key de Gemini](https://aistudio.google.com/apikey).
4. Sube el documento PDF/CSV del torneo cuando se solicite.
5. Prueba el agente con las preguntas de ejemplo o con tus propias preguntas.
6. Al final, descarga `faiss_index.zip` (contiene el índice vectorial ya generado).

### 2. Ejecución local de la app

```bash
git clone <url-de-este-repositorio>
cd alura-agente
pip install -r requirements.txt

# Descomprime faiss_index.zip generado en Colab dentro de esta carpeta
unzip faiss_index.zip -d faiss_index

export GOOGLE_API_KEY="tu-api-key"
streamlit run streamlit_app.py
```

Abre `http://localhost:8501` en el navegador.

### 3. Deploy en Streamlit Community Cloud

1. Sube este repositorio (con `streamlit_app.py`, `requirements.txt` y la carpeta `faiss_index/`) a GitHub.
2. Entra a https://share.streamlit.io y conéctate con tu cuenta de GitHub.
3. Clic en **"New app"**, selecciona el repositorio, la rama (`main`) y el archivo principal `streamlit_app.py`.
4. En **"Advanced settings" → "Secrets"**, agrega:
   ```
   GOOGLE_API_KEY = "tu-api-key"
   ```
5. Clic en **"Deploy"**. Espera unos minutos mientras instala las dependencias.

## 💬 Ejemplos de preguntas y respuestas

| Pregunta | Respuesta del agente |
|---|---|
| ¿Cuántos equipos participan en el torneo? | En el torneo participan 8 equipos, representados por los 8 jugadores inscritos. Los equipos que participan son: 1) Boston Celtics (Bladimir), 2) Golden State Warriors (Carlos), 3) Los Angeles Lakers (Miguel), 4) Miami Heat (Diego), 5) Denver Nuggets (Andrés), 6) Milwaukee Bucks (Luis), 7) Phoenix Suns (Fernando), 8) Oklahoma City Thunder (Roberto). |
| ¿Cuál es el formato de eliminación? | Según la información oficial del torneo, el formato de la Fase de Eliminación es el siguiente: 1) Clasificación: avanzan a esta fase los 2 primeros lugares de cada grupo (4 clasificados en total). 2) Semifinales: se enfrentan en cruces directos: 1º del Grupo A vs. 2º del Grupo B, y 1º del Grupo B vs. 2º del Grupo A. 3) Gran Final: los ganadores de ambas semifinales se enfrentan para definir al campeón del torneo. |
| ¿Qué reglas aplican para las series de playoffs? | Esa información específica no aparece en el reglamento del torneo. El documento únicamente detalla sobre la Fase de Eliminación que los 4 clasificados juegan las Semifinales (1º del Grupo A vs. 2º del Grupo B, y 1º del Grupo B vs. 2º del Grupo A) y posteriormente la Gran Final, pero no especifica las reglas detalladas de las series de playoffs (como al mejor de cuántos partidos se juega, la duración de los cuartos, la dificultad u otra configuración del juego). |
| ¿Quién es Michael Jordan? *(pregunta general de NBA, fuera del documento)* | Michael Jordan es ampliamente considerado por expertos, analistas y aficionados como el mejor jugador de baloncesto de todos los tiempos (GOAT). Fue una leyenda de la NBA que brilló principalmente con los Chicago Bulls, equipo con el que ganó 6 campeonatos de la NBA (1991, 1992, 1993, 1996, 1997 y 1998), siendo elegido MVP de las Finales en cada uno de ellos. Entre sus logros más destacados: 5 premios MVP de la temporada regular, 14 apariciones en el NBA All-Star Game, 10 títulos de máximo anotador de la NBA, y 2 medallas de oro olímpicas con la selección de Estados Unidos (destacando su participación en el icónico Dream Team de 1992). Además, revolucionó la cultura pop mundial y el marketing deportivo gracias a su marca Air Jordan en alianza con Nike, y fue exaltado al Basketball Hall of Fame. |

## ☁️ Evidencia del deploy

- **Enlace público:** https://alura-agente-2fmovmpg58ybs3rgwkxmhk.streamlit.app/

- **Captura de pantalla:**

  <img width="1918" height="1010" alt="deploy" src="https://github.com/user-attachments/assets/06b403e6-9c21-43b1-a2ac-4cabb44ba2cd" />
  <img width="1918" height="1001" alt="deploy 2 " src="https://github.com/user-attachments/assets/e79e88d7-e9f1-4773-bf1f-96a43f4f51f3" />
  <img width="1905" height="977" alt="image" src="https://github.com/user-attachments/assets/c0a464fb-b570-4f53-84fa-6df8172a0a46" />




## 📂 Estructura del repositorio

```
alura-agente/
├── Alura_Agente.ipynb    # Notebook de Colab (prototipo del agente)
├── streamlit_app.py      # App Streamlit para el deploy
├── requirements.txt      # Dependencias
├── faiss_index/          # Índice vectorial (generado en Colab)
├── deploy.png            # Captura de pantalla del deploy funcionando
├── LICENSE
└── README.md
```
