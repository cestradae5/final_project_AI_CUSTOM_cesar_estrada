# Proyecto Examen Final - Módulo 3

Asistente educativo con **CAG (Context-Augmented Generation)** que retiene contexto de usuario y lo inyecta junto con RAG (recuperación de base de conocimiento) en las respuestas.

Stack: **Python 3.14+** puro (stdlib `http.server`) · Frontend estático (HTML/CSS/JS vanilla) · `unittest`

---

## Inicio rápido

```powershell
# 1. Pararse en la raíz del proyecto
cd final_project_AI_CUSTOM_cesar_estrada

# 2. Ejecutar todas las pruebas
$env:PYTHONPATH="."; python -m unittest discover -s tests -p "test_*.py"

# 3. Iniciar el backend
$env:PYTHONPATH="."; python -m backend.server

# 4. Abrir el frontend
#    Simplemente abra frontend/index.html en su navegador
```

---

## Estructura

| Ruta | Contenido |
|---|---|
| `backend/` | Servidor HTTP (`server.py`) + lógica del asistente |
| `backend/context_store.py` | Almacenamiento en memoria de contexto por usuario |
| `backend/cag.py` | Reglas de aumentación contextual (`audience`, `language`, `include_examples`) |
| `backend/assistant.py` | Orquestación RAG + CAG: recupera snippets, aplica contexto |
| `backend/knowledge.py` | Búsqueda por términos en `data/knowledge_base.json` |
| `frontend/` | Interfaz web estática (`index.html`, `app.js`, `styles.css`) |
| `data/knowledge_base.json` | Base de conocimiento del curso (4 entradas) |
| `tests/` | Suites de prueba organizadas por capa |
| `tests/unit/` | Tests unitarios TDD para `ContextStore` y `apply_context` |
| `tests/base/` | Tests base del proyecto (deben pasar siempre) |
| `tests/validation/` | Tests de validación del contrato CAG |
| `scripts/` | Scripts auxiliares para tests y validación |
| `openspec/` | Artefactos SDD (proposal, specs, design, tasks) |
| `docs/` | Documentación y evidencias del estudiante |

---

## Tests

**Estado actual: 17/17 tests green** 🟢

| Capa | Archivo | Tests | Estado |
|---|---|---|---|
| Unit — ContextStore | `tests/unit/test_unit_context_store.py` | 6 | ✅ |
| Unit — apply_context | `tests/unit/test_unit_cag.py` | 5 | ✅ |
| Base API | `tests/base/test_base_api.py` | 3 | ✅ |
| Validación CAG | `tests/validation/test_cag_contract.py` | 3 | ✅ |

```powershell
# Ejecutar todas las pruebas
$env:PYTHONPATH="."; python -m unittest discover -s tests -p "test_*.py" -v

# O por capa
$env:PYTHONPATH="."; python -m unittest tests.unit.test_unit_context_store -v
$env:PYTHONPATH="."; python -m unittest tests.unit.test_unit_cag -v
$env:PYTHONPATH="."; python -m unittest tests.base.test_base_api -v
$env:PYTHONPATH="."; python -m unittest tests.validation.test_cag_contract -v
```

---

## API REST

| Método | Ruta | Body | Respuesta |
|---|---|---|---|
| `GET` | `/health` | — | `{"status": "ok"}` |
| `POST` | `/api/ask` | `{"user_id": "...", "question": "..."}` | `{answer, sources, context_used}` |
| `POST` | `/api/context` | `{"user_id": "...", "key": "...", "value": "..."}` | `{"saved": true}` |
| `GET` | `/api/context?user_id=...` | — | `{user_id, context: [{key, value}]}` |

---

## CAG — Context-Augmented Generation

El asistente combina dos fuentes de información para responder:

1. **RAG** — `knowledge.py` busca en la base de conocimiento del curso
2. **CAG** — `context_store.py` recupera contexto persistente del usuario, y `cag.py` adapta la respuesta

### Contextos soportados

| Clave | Valores | Se detecta automáticamente cuando decís... |
|---|---|---|
| `audience` | `explicar como principiante` | "explicame como principiante...", "soy nuevo..." |
| `language` | `español`, `ingles` | "...en español", "...en inglés" |
| `include_examples` | `si` | "...con ejemplos", "dame ejemplos..." |

### Ejemplo de uso

```
PRIMERA PREGUNTA:
  "explicame como principiante que es RAG"
  → Se guarda automáticamente: audience = "explicar como principiante"
  → Respuesta adaptada + badge "Contexto usado: audience"
  → Panel CAG muestra: AUDIENCE | explicar como principiante

SEGUNDA PREGUNTA (sin repetir contexto):
  "y que es CAG?"
  → El contexto audience SIGUE activo
  → Respuesta adaptada nuevamente
  → Badge: "Contexto usado: audience" (retención)
```

El contexto se retiene durante toda la sesión (mientras el servidor esté corriendo).

---

## Ejecutar backend

```powershell
$env:PYTHONPATH="."; python -m backend.server
```

El backend queda disponible en `http://127.0.0.1:8000`.

## Abrir frontend

Abra `frontend/index.html` en un navegador. El panel CAG se carga automáticamente.

También puede servir la carpeta con un servidor estático local si lo prefiere.

---

## Validación final

```powershell
.\test.sh
```

---

## Sprints de desarrollo

### Sprint 1: Backend — Módulo CAG

Implementación del sistema de contexto persistente en el backend.

| Archivo | Cambio |
|---|---|
| `backend/context_store.py` | `ContextStore` con dict en memoria `{user_id: {key: value}}` |
| `backend/cag.py` | `apply_context()` con reglas para `audience`, `language`, `include_examples` |
| `backend/assistant.py` | Integración RAG + CAG, singleton `context_store`, retorna `context_used` |
| `backend/server.py` | Import compartido de `context_store` desde `assistant.py` |
| `tests/unit/test_unit_context_store.py` | 6 tests TDD para `ContextStore` |
| `tests/unit/test_unit_cag.py` | 5 tests TDD para `apply_context` |

**Resultado:** 17/17 tests green 🟢

---

### Sprint 2: Frontend — Panel CAG y auto-detección

Conexión del frontend con el backend CAG para visualizar la retención de contexto.

| Archivo | Cambio |
|---|---|
| `frontend/index.html` | Panel CAG con lista dinámica + formulario colapsable |
| `frontend/app.js` | Auto-detección de contexto desde preguntas, badge `context_used` |
| `frontend/styles.css` | Estilos para context-items, badges, formulario |

**Características:**
- Carga automática de contexto al abrir la página
- Detección automática: "explicame como principiante" → guarda `audience`
- Badge que muestra qué contexto se usó en cada respuesta
- El contexto persiste entre preguntas (retención visible)

---

## SDD (Spec-Driven Development)

Todo el desarrollo del módulo CAG se realizó siguiendo SDD. Los artefactos están en `openspec/`:

- `openspec/changes/cag-context-augmentation/proposal.md` — Propuesta
- `openspec/changes/cag-context-augmentation/specs/` — Especificaciones
- `openspec/changes/cag-context-augmentation/design.md` — Diseño técnico
- `openspec/changes/cag-context-augmentation/tasks.md` — Desglose de tareas
