# Arquitectura

## Criterios de Ranking

El servicio de ranking consolida los resultados de los partidos y calcula la
clasificación de los equipos utilizando los siguientes criterios:

1. **Puntos:** 3 por victoria, 1 por empate y 0 por derrota.
2. **Diferencia de goles:** goles a favor menos goles en contra.
3. **Goles a favor:** se usa como tercer criterio de desempate.

Los equipos se ordenan de forma descendente considerando, en ese orden, los
puntos obtenidos, la diferencia de goles y los goles a favor.

## Integración con API-Football

El backend puede consultar datos de ligas externas a través del endpoint `/external-leagues`.
El flujo de integración es el siguiente:

1. `main.py` recibe la petición REST.
2. Se llama al servicio `services/api_football.py`.
3. El servicio realiza la solicitud HTTP a API-Football usando las variables de entorno `API_FOOTBALL_HOST` y `API_FOOTBALL_KEY`.
4. La respuesta de la API externa se devuelve al cliente sin modificaciones.

Para ejecutar localmente se deben definir dichas variables de entorno (ver `.env.example`).
