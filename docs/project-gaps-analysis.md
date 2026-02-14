# Análisis del Proyecto TuLiga - Gaps y Objetivo

## Contexto

**TuLiga** es una plataforma full-stack para la gestión de ligas de fútbol amateur en Uruguay. Permite a organizadores administrar torneos, equipos, jugadores, árbitros, canchas y pagos. Está en versión **0.2.0 (Beta)**.

**Tech Stack:** FastAPI (Python) + Next.js 15 (TypeScript) + PostgreSQL + Docker

---

## Objetivo del Proyecto

Crear una plataforma integral que permita:
- Organizar torneos y generar fixtures automáticamente
- Gestionar equipos, jugadores y árbitros
- Reservar canchas con integración de pagos (Stripe/MercadoPago)
- Visualizar estadísticas avanzadas y rankings
- Comunicación entre equipos
- Expandirse a móvil (PWA/React Native)

---

## Lo que YA está implementado

- Estructura full-stack funcional (FastAPI + Next.js)
- CRUD de canchas y sistema de reservas (`backend/routes/fields.py`)
- Gestión básica de árbitros y asignación a partidos (`backend/routes/referees.py`)
- Sistema de ranking por puntos (`backend/routes/ranking.py`, `backend/services/ranking.py`)
- Dashboard de estadísticas básicas (`backend/routes/stats.py`)
- Sistema de mensajería básico (`backend/routes/messages.py`)
- Integración básica con API-Football (`backend/services/api_football.py`)
- Tests backend (pytest) y frontend (Jest) con CI/CD en GitHub Actions
- Migraciones con Alembic (auto-ejecutadas al iniciar)
- Documentación en README y carpeta `docs/`

---

## Lo que FALTA para completar el proyecto

### CRÍTICO (Bloquea producción)

| # | Gap | Detalle | Archivos relacionados |
|---|-----|---------|-----------------------|
| 1 | **Sin autenticación** | No hay JWT, login, roles ni permisos. Todos los endpoints son públicos | No existe módulo auth |
| 2 | **Sin Docker files** | README promete `docker-compose up` pero no existen Dockerfile ni docker-compose.yml | Raíz del proyecto |
| 3 | **Modelos de BD incompletos** | Faltan modelos: `Tournament`, `Team`, `Registration`, `Profile` | `backend/models/` |
| 4 | **Fixtures no se persisten** | El generador de fixtures crea datos en memoria pero no los guarda en BD | `backend/core/fixtures.py`, `backend/routes/tournaments.py` |
| 5 | **Ruta de torneos mínima** | Solo 23 líneas, no crea/persiste torneos, no tiene CRUD | `backend/routes/tournaments.py` |

### ALTO (Funcionalidad incompleta)

| # | Gap | Detalle | Archivos relacionados |
|---|-----|---------|-----------------------|
| 6 | **Sin validaciones de entrada** | Falta validar: fechas, horas, niveles de árbitro, contenido de mensajes | Todos los `backend/routes/` |
| 7 | **Pagos son mock** | Stripe/MercadoPago tienen fallbacks, sin webhooks ni tracking real | `backend/core/payments.py` |
| 8 | **Sin manejo de errores en frontend** | Ningún componente tiene error boundaries, loading states ni retry | Todos los `frontend/app/` |
| 9 | **API-Football sin integración real** | Solo fetch básico, no sincroniza datos con el sistema | `backend/services/api_football.py` |
| 10 | **Sin paginación** | Ningún endpoint tiene paginación para listas | Todos los `backend/routes/` |
| 11 | **Migraciones incompletas** | Solo 3 migraciones, faltan tablas para torneos, equipos, registros | `backend/alembic/versions/` |

### MEDIO (Mejoras necesarias)

| # | Gap | Detalle |
|---|-----|---------|
| 12 | **Mensajería usa polling** | Polling cada 5s en vez de WebSockets (`frontend/app/messages/page.tsx`) |
| 13 | **Sin .env frontend** | No existe `.env.example` para Next.js |
| 14 | **Sin seed data** | No hay script para poblar la BD con datos iniciales |
| 15 | **Deploy es placeholder** | CI/CD tiene `echo 'Deploy step'` sin implementación real |
| 16 | **Sin logging** | No hay sistema de logging estructurado en backend |
| 17 | **Sin CORS configurado** | No hay variables de entorno para CORS |

### BAJO (Nice to have / Roadmap futuro)

| # | Gap | Detalle |
|---|-----|---------|
| 18 | App móvil PWA/React Native |
| 19 | Marketplace de canchas |
| 20 | Sistema de ranking nacional |
| 21 | Notificaciones push/email |
| 22 | Tests e2e y de accesibilidad |
| 23 | Pre-commit hooks, ESLint, Prettier |

---

## Resumen

El proyecto tiene una **base sólida** con buena arquitectura y separación de responsabilidades, pero le faltan piezas fundamentales para ser funcional en producción:

1. **Autenticación y autorización** - Sin esto, cualquier persona puede modificar datos
2. **Modelos y persistencia completos** - Torneos, equipos y fixtures no se guardan en BD
3. **Infraestructura de deploy** - Docker files y deployment real
4. **Validaciones y manejo de errores** - Tanto en backend como frontend
5. **Integración de pagos real** - Webhooks y tracking de transacciones

El proyecto necesita completar estos 5 pilares antes de poder considerarse listo para producción.
