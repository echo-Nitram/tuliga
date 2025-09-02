# Desarrollo - Estadísticas Avanzadas

Esta sección describe los nuevos endpoints agregados al backend y cómo visualizarlos desde el frontend.

## Endpoints agregados

- `GET /stats/summary`: devuelve métricas consolidadas de la liga.
- `GET /stats/players/top`: lista de jugadores destacados con goles y asistencias.

Para incluir estas rutas en tu aplicación FastAPI:

```python
from fastapi import FastAPI
from backend.routes import stats

app = FastAPI()
app.include_router(stats.router, prefix="/api")
```

## Visualización en el dashboard

En el frontend se añadió la página `frontend/app/dashboard/advanced.tsx` que consume los endpoints anteriores y muestra:

- **LineChart** con estadísticas generales de equipos, jugadores y partidos.
- **BarChart** con los máximos goleadores.

Para probarlo durante el desarrollo:

```bash
cd frontend
npm run dev
# luego visita http://localhost:3000/dashboard/advanced
```
