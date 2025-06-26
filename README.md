# 🏆 TuLiga - Plataforma de Gestión de Ligas de Fútbol Amateur

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-13.5.6-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)

> **Plataforma completa para la gestión de ligas de fútbol amateur en Uruguay**

TuLiga es una solución integral que permite organizar torneos, gestionar equipos, crear fixtures automáticos, procesar pagos y generar estadísticas avanzadas para ligas de fútbol amateur.

## 🌟 Características Principales

- **⚽ Gestión de torneos:** Crea y administra múltiples torneos con diferentes formatos
- **👥 Administración de equipos:** Gestiona plantillas, perfiles de jugadores y asistencia  
- **📅 Fixture automático:** Genera automáticamente el calendario de partidos
- **💳 Procesamiento de pagos:** Integración con MercadoPago para inscripciones y pagos
- **📊 Estadísticas avanzadas:** Seguimiento de rendimiento y estadísticas detalladas
- **🔔 Notificaciones:** Envío de notificaciones por email y push
- **👤 Perfiles de usuario:** Diferentes roles (administrador, organizador, equipo, jugador, árbitro)
- **📱 Diseño responsive:** Funciona perfectamente en dispositivos móviles y de escritorio

## 🚀 Stack Tecnológico

### Backend
- **FastAPI:** Framework moderno de Python para APIs
- **SQLAlchemy:** ORM para interacción con base de datos
- **PostgreSQL:** Base de datos relacional
- **JWT + Supabase:** Autenticación segura
- **Alembic:** Migraciones de base de datos
- **MercadoPago + Stripe:** Procesamiento de pagos

### Frontend
- **Next.js:** Framework de React para el frontend
- **TypeScript:** Tipado estático para JavaScript  
- **Tailwind CSS:** Utilidades CSS para el diseño
- **Radix UI:** Componentes de UI accesibles
- **React Hook Form + Zod:** Manejo y validación de formularios
- **Recharts:** Gráficos y visualizaciones

### DevOps
- **Docker + Docker Compose:** Containerización
- **GitHub Actions:** CI/CD pipeline
- **pytest:** Testing automatizado
- **Alembic:** Migraciones de base de datos

## 🏗️ Arquitectura

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Frontend      │   │     Backend     │   │   Database      │
│   (Next.js)     │◄──┤   (FastAPI)     │◄──┤  (PostgreSQL)   │
│   Port: 3000    │   │   Port: 8000    │   │   Port: 5432    │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────┤   PgAdmin       │──────────────┘
                        │   Port: 5050    │
                        └─────────────────┘
```

## 📋 Requisitos

- **Python 3.11** o superior
- **Node.js 18.16.0** o superior
- **PostgreSQL 12** o superior
- **Docker y Docker Compose** (recomendado)

## ⚡ Instalación Rápida

### Usando Docker (Recomendado)

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/echo-Nitram/tuliga.git
   cd tuliga
   ```

2. **Inicia los contenedores:**
   ```bash
   docker-compose up -d
   ```

3. **Accede a la aplicación:**
   - 🌐 **Frontend:** http://localhost:3000
   - 🔧 **API Backend:** http://localhost:8000
   - 📚 **Documentación API:** http://localhost:8000/api/docs
   - 🗄️ **PgAdmin:** http://localhost:5050 (admin@tuliga.app / admin123)

### Configuración Manual

<details>
<summary>👆 Click para ver instalación manual</summary>

1. **Backend:**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # macOS/Linux  
   source venv/bin/activate
   
   pip install -r requirements.txt
   cp .env.example .env
   # Edita .env con tus configuraciones
   
   python setup_db.py --seed  # Incluye datos de prueba
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edita .env.local si es necesario
   npm run dev
   ```

</details>

## 🗄️ Base de Datos

El sistema incluye un esquema completo con:

- **👥 Profiles:** Usuarios del sistema con roles diferenciados
- **⚽ Teams:** Equipos con información completa
- **🏃 Players:** Jugadores y datos personales/deportivos  
- **🏆 Tournaments:** Torneos con configuraciones flexibles
- **📝 Registrations:** Inscripciones de equipos a torneos
- **⚽ Matches:** Partidos con resultados y estadísticas
- **📊 Player_Stats:** Estadísticas detalladas por jugador/partido
- **💳 Payments:** Transacciones y pagos integrados

Ver esquema completo en `combined-schema.sql`.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests  
cd frontend
npm test
```

## 🚀 Despliegue

### Producción con Docker

```bash
# Construir para producción
docker-compose -f docker-compose.prod.yml up -d

# Variables de entorno importantes:
# - ENVIRONMENT=production
# - SECRET_KEY (segura)
# - CORS_ORIGINS (dominios permitidos)
# - Variables de conexión a BD
```

### Plataformas Recomendadas
- **Backend:** AWS ECS, GCP Cloud Run, Railway
- **Frontend:** Vercel, Netlify (integración óptima con Next.js)
- **Base de datos:** AWS RDS, Google Cloud SQL, Supabase

## 📖 Documentación

- 📋 **[API Docs](http://localhost:8000/api/docs)** - Documentación interactiva Swagger
- 🏗️ **[Arquitectura](docs/architecture.md)** - Diseño y patrones del sistema
- 💾 **[Base de Datos](docs/database.md)** - Esquema y relaciones  
- 🚀 **[Deployment](docs/deployment.md)** - Guía de despliegue
- 👨‍💻 **[Development](docs/development.md)** - Guía para desarrolladores

## 🛣️ Roadmap

### ✅ Completado
- [x] Arquitectura full-stack completa
- [x] Sistema de autenticación con roles
- [x] Gestión de equipos y jugadores
- [x] Creación y gestión de torneos
- [x] Sistema de pagos con MercadoPago
- [x] Estadísticas básicas por jugador
- [x] Docker y testing automatizado

### 🔄 En Desarrollo
- [ ] **Integración API-Football.com** - Datos externos de ligas profesionales
- [ ] **Generador automático de fixtures** - Algoritmos optimizados
- [ ] **Dashboard estadísticas avanzadas** - Gráficos y métricas
- [ ] **CI/CD Pipeline** - GitHub Actions

### 📋 Próximas Funcionalidades
- [ ] **Sistema de comunicaciones** interno entre equipos
- [ ] **Módulo de árbitros completo** con disponibilidad
- [ ] **App móvil** PWA o React Native
- [ ] **Marketplace de canchas** para alquileres
- [ ] **Sistema de ranking** nacional uruguayo

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. 🍴 **Fork** el repositorio
2. 🌿 **Crea una rama:** `git checkout -b feature/nueva-funcionalidad`
3. ✅ **Commit cambios:** `git commit -m 'Add: nueva funcionalidad'`
4. 📤 **Push a la rama:** `git push origin feature/nueva-funcionalidad`
5. 🔄 **Abre un Pull Request**

## 🐛 Reportar Issues

Encontraste un bug? [Crea un issue](https://github.com/echo-Nitram/tuliga/issues/new) con:
- 📝 Descripción detallada del problema
- 🔧 Pasos para reproducir
- 💻 Información del entorno (OS, navegador, etc.)
- 📸 Screenshots si es posible

## 📊 Estado del Proyecto

- **📈 Versión:** 0.2.0 (Beta)
- **🏗️ Estado:** En desarrollo activo
- **🧪 Cobertura tests:** En implementación
- **📱 Compatibilidad:** Chrome, Firefox, Safari, Edge
- **🌍 Soporte:** Español (Uruguay)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Contacto & Soporte

- 📧 **Email:** soporte@tuliga.app
- 🌐 **Website:** https://tuliga.app
- 🐛 **Issues:** [GitHub Issues](https://github.com/echo-Nitram/tuliga/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/echo-Nitram/tuliga/discussions)

---

<div align="center">

**⭐ Si te gusta TuLiga, dale una estrella en GitHub! ⭐**

*Hecho con ❤️ para la comunidad futbolística de Uruguay*

</div>