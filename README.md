# 🍃 KonohAPI - Naruto Series Data API

Una API REST moderna y asincrónica para consultar datos del universo de Naruto. Construida con **FastAPI**, **PostgreSQL** y las mejores prácticas de desarrollo.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Stack Tecnológico](#stack-tecnológico)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Base de Datos](#base-de-datos)
- [Desarrollo](#desarrollo)

---

## ✨ Características

- ✅ **API REST completamente asincrónica** con FastAPI
- ✅ **Base de datos relacional** PostgreSQL con SQLModel ORM
- ✅ **Validación de datos** con Pydantic
- ✅ **Migraciones de BD** automáticas con Alembic
- ✅ **Documentación automática** con Swagger UI (`/docs`)
- ✅ **Type-safe** con type hints completos en Python
- ✅ **Manejo de errores** robusto con códigos HTTP estándar
- ✅ **Dependency Injection** limpio y profesional
- ✅ **Configuración centralizada** con variables de entorno

---

## 🏗️ Arquitectura

### Patrón: **Layered Architecture** (Arquitectura en Capas)

KonohAPI implementa una arquitectura en capas que separa responsabilidades de forma clara:

```
┌─────────────────────────────────────────┐
│     Presentation Layer (Routers)        │ ← HTTP Endpoints
│   app/routers/*.py                      │
├─────────────────────────────────────────┤
│      Domain Layer (Models)              │ ← DTOs & ORM Models
│   app/models/*.py                       │
├─────────────────────────────────────────┤
│    Data Access Layer (Session)          │ ← DB Connection & Queries
│   app/db/session.py                     │
├─────────────────────────────────────────┤
│   Configuration Layer (Settings)        │ ← Environment Vars
│   app/config/settings.py                │
├─────────────────────────────────────────┤
│      PostgreSQL Database                │ ← Persistent Storage
│   konohapi database                     │
└─────────────────────────────────────────┘
```

### Flujo de una Solicitud

```
1. Cliente HTTP → POST /characters
2. FastAPI valida entrada con CharacterCreate (Pydantic DTO)
3. Router llama handler con sesión BD inyectada
4. Handler ejecuta query SQL async a PostgreSQL
5. Resultado ORM se convierte a CharacterRead (Pydantic DTO)
6. API devuelve JSON al cliente
```

### Patrones Implementados

| Patrón | Ubicación | Propósito |
|--------|-----------|----------|
| **MVC** | routers/ + models/ | Separar lógica de presentación |
| **ORM** | models/db_models.py | Mapeo objeto-relacional |
| **DTO** | models/schemas.py | Validación y transformación de datos |
| **Dependency Injection** | routers/ | Inyectar sesión BD en endpoints |
| **Repository-like** | db/session.py | Centralizar acceso a BD |

---

## 🛠️ Stack Tecnológico

| Componente | Herramienta | Versión | Propósito |
|-----------|-----------|---------|----------|
| **Framework Web** | FastAPI | ^0.104 | API REST asincrónica |
| **Server ASGI** | Uvicorn | ^0.24 | Servidor de desarrollo |
| **Base de Datos** | PostgreSQL | 15+ | RDBMS relacional |
| **Driver Async** | asyncpg | ^0.29 | Driver async para PostgreSQL |
| **ORM** | SQLModel | ^0.0.14 | ORM híbrido SQLAlchemy+Pydantic |
| **Validación** | Pydantic | ^2.0 | Validación y serialización |
| **Migraciones** | Alembic | ^1.13 | Versionado de esquemas BD |
| **Config** | python-dotenv | ^1.0 | Variables de entorno |
| **Python** | Python | 3.10+ | Lenguaje base |

---

## 📦 Instalación

### Requisitos Previos

- Python 3.10+
- PostgreSQL 15+ (o Docker)
- pip o poetry

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/danigpas/KonohAPI.git
cd KonohAPI
```

### Paso 2: Crear Entorno Virtual

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar PostgreSQL

#### Opción A: Docker (Recomendado)

```bash
docker run --name konohapi-db \
  -e POSTGRES_USER=dani \
  -e POSTGRES_PASSWORD=dani \
  -e POSTGRES_DB=konohapi \
  -p 5432:5432 \
  -d postgres:15
```

#### Opción B: PostgreSQL Local

Crea una BD llamada `konohapi`:

```sql
createdb konohapi
```

### Paso 5: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+asyncpg://dani:dani@localhost:5432/konohapi
```

### Paso 6: Ejecutar Migraciones

```bash
cd app
alembic upgrade head
```

### Paso 7: Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

---

## ⚙️ Configuración

### Variables de Entorno (`.env`)

```env
# Base de datos (obligatorio)
DATABASE_URL=postgresql+asyncpg://usuario:contraseña@host:puerto/base_datos

# Ejemplo local
DATABASE_URL=postgresql+asyncpg://dani:dani@localhost:5432/konohapi
```

### Archivo de Configuración

`app/config/settings.py` carga y valida las variables de entorno:

```python
class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en .env")

settings = Settings()
```

---

## 🚀 Uso

### Documentación Interactiva

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Ejemplos con cURL

#### Crear un Personaje

```bash
curl -X POST "http://localhost:8000/characters" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Naruto",
    "full_name": "Naruto Uzumaki",
    "rank": "Hokage",
    "clan_id": 1,
    "biography": "El héroe protagonista de Naruto",
    "image_url": "https://example.com/naruto.jpg"
  }'
```

#### Obtener Todos los Personajes

```bash
curl "http://localhost:8000/characters"
```

#### Obtener un Personaje por ID

```bash
curl "http://localhost:8000/characters/1"
```

### Ejemplos con Python

```python
import httpx
import asyncio

async def fetch_characters():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/characters")
        print(response.json())

asyncio.run(fetch_characters())
```

---

## 📁 Estructura del Proyecto

```
KonohAPI/
├── app/                          # Aplicación principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada FastAPI
│   │
│   ├── config/                   # Capa de Configuración
│   │   ├── __init__.py
│   │   └── settings.py           # Variables de entorno centralizadas
│   │
│   ├── db/                       # Capa de Persistencia
│   │   ├── __init__.py
│   │   └── session.py            # Engine, sessionmaker, get_session()
│   │
│   ├── models/                   # Capa de Modelos
│   │   ├── __init__.py
│   │   ├── db_models.py          # SQLModel ORM (Character, Clan, Jutsu)
│   │   └── schemas.py            # Pydantic DTOs (CharacterCreate, CharacterRead)
│   │
│   └── routers/                  # Capa de Presentación
│       ├── __init__.py
│       ├── characters.py         # Endpoints de personajes
│       ├── clans.py              # Endpoints de clanes (próximamente)
│       └── jutsus.py             # Endpoints de jutsus (próximamente)
│
├── alembic/                      # Migraciones de BD
│   ├── env.py                    # Configuración de Alembic
│   ├── script.py.mako
│   └── versions/
│       └── 44ab00d87364_create_initial_tables.py
│
├── .env                          # Variables de entorno (NO commitear)
├── .gitignore                    # Archivos ignorados por Git
├── .vscode/                      # Configuración de VS Code
│   └── settings.json             # Type checking mode: standard
├── requirements.txt              # Dependencias Python
├── alembic.ini                   # Configuración de Alembic
└── README.md                     # Este archivo
```

### Archivos Clave

#### `app/main.py`

Punto de entrada de la aplicación. Inicializa FastAPI e incluye los routers:

```python
from fastapi import FastAPI
from .routers import characters

app = FastAPI()
app.include_router(characters.router)

@app.get('/')
async def hello():
    return {'Hello ninjas!'}
```

#### `app/db/session.py`

Gestiona la conexión a la BD con soporte async:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import Session, select

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session
```

#### `app/models/db_models.py`

Define los modelos ORM que se mapean a tablas BD:

```python
class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    clan: Optional[Clan] = Relationship(back_populates="members")
    jutsus: List[Jutsu] = Relationship(link_model=CharacterJutsuLink)
```

#### `app/models/schemas.py`

Define los DTOs Pydantic para validación de entrada/salida:

```python
class CharacterCreate(BaseModel):
    name: str
    full_name: Optional[str] = None

class CharacterRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
```

#### `app/routers/characters.py`

Endpoints HTTP para operaciones CRUD:

```python
@router.get('', response_model=List[CharacterRead])
async def list_all_characters(session: AsyncSession = Depends(get_session)):
    # Lógica de lista

@router.get('/{character_id}', response_model=CharacterRead)
async def get_character_by_id(character_id: int, session: AsyncSession = Depends(get_session)):
    # Lógica de obtener por ID

@router.post('', response_model=CharacterRead, status_code=201)
async def create_character(character_data: CharacterCreate, session: AsyncSession = Depends(get_session)):
    # Lógica de creación
```

---

## 🔌 Endpoints

### Characters

| Método | Ruta | Descripción | Status Code |
|--------|------|-------------|------------|
| GET | `/characters` | Obtener todos los personajes | 200 |
| GET | `/characters/{character_id}` | Obtener un personaje por ID | 200 / 404 |
| POST | `/characters` | Crear un nuevo personaje | 201 |
| PUT | `/characters/{character_id}` | Actualizar personaje | 200 / 404 |
| DELETE | `/characters/{character_id}` | Eliminar personaje | 204 / 404 |

### Clans (Próximamente)

- GET `/clans`
- GET `/clans/{clan_id}`
- POST `/clans`

### Jutsus (Próximamente)

- GET `/jutsus`
- GET `/jutsus/{jutsu_id}`
- POST `/jutsus`

---

## 🗄️ Base de Datos

### Modelo Relacional

```
┌─────────────┐
│   CLAN      │
├─────────────┤
│ id (PK)     │
│ name        │
└─────────────┘
      ▲
      │ 1:N
      │
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│ CHARACTER   │──N:N─│ CHARACTER_JUTSU  │──N:N─│   JUTSU     │
├─────────────┤      │    (Link)        │      ├─────────────┤
│ id (PK)     │      ├──────────────────┤      │ id (PK)     │
│ name        │      │ character_id (FK)│      │ name        │
│ clan_id(FK) │      │ jutsu_id (FK)    │      │ type        │
│ created_at  │      └──────────────────┘      └─────────────┘
└─────────────┘
```

### Tablas

#### `character`
- `id` (INT, PRIMARY KEY)
- `external_id` (VARCHAR)
- `name` (VARCHAR, NOT NULL)
- `full_name` (VARCHAR)
- `rank` (VARCHAR)
- `clan_id` (INT, FOREIGN KEY)
- `biography` (TEXT)
- `image_url` (VARCHAR)
- `created_at` (TIMESTAMP)

#### `clan`
- `id` (INT, PRIMARY KEY)
- `name` (VARCHAR, NOT NULL)
- `description` (TEXT)

#### `jutsu`
- `id` (INT, PRIMARY KEY)
- `name` (VARCHAR, NOT NULL)
- `type` (VARCHAR)
- `rank` (VARCHAR)

#### `character_jutsu` (Tabla de Unión)
- `character_id` (INT, FOREIGN KEY, PRIMARY KEY)
- `jutsu_id` (INT, FOREIGN KEY, PRIMARY KEY)
- `learned_in_episode` (INT)

---

## 🔧 Desarrollo

### Crear una Migración Nueva

```bash
cd app
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

### Agregar un Nuevo Endpoint

1. Define el modelo ORM en `app/models/db_models.py`
2. Crea los DTOs en `app/models/schemas.py`
3. Implementa los handlers en `app/routers/new_entity.py`
4. Incluye el router en `app/main.py`

### Ejecutar Tests (Próximamente)

```bash
pytest
```

### Linting y Formateo

```bash
# Pylint
pylint app/

# Black (formateo)
black app/
```

---

## 🐛 Troubleshooting

### Error: `DATABASE_URL no está configurada`

**Solución:** Crea un archivo `.env` con la variable `DATABASE_URL`.

### Error de Conexión a PostgreSQL

```bash
# Verifica que PostgreSQL está corriendo
psql -U dani -d konohapi -c "SELECT 1"
```

### Pylance Type Checking

Si Pylance muestra errores con SQLModel, asegúrate que en `.vscode/settings.json` tengas:

```json
{
  "python.analysis.typeCheckingMode": "standard"
}
```

---

## 📝 Próximas Mejoras

- [ ] Endpoints PUT y DELETE para Characters
- [ ] Endpoints CRUD completos para Clans y Jutsus
- [ ] Autenticación y autorización (JWT)
- [ ] Rate limiting
- [ ] Paginación en listados
- [ ] Tests unitarios e integración
- [ ] Documentación de API en OpenAPI 3.0
- [ ] Docker Compose para ambiente completo
- [ ] CI/CD con GitHub Actions
- [ ] Frontend React/Vue

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Daniel González**  
GitHub: [@danigpas](https://github.com/danigpas)

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

Para reportar bugs o sugerencias, abre un [issue](https://github.com/danigpas/KonohAPI/issues).

---

**¡Happy coding! 🥷🍃**