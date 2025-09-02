# Arquitectura

## Criterios de Ranking

El servicio de ranking consolida los resultados de los partidos y calcula la
clasificación de los equipos utilizando los siguientes criterios:

1. **Puntos:** 3 por victoria, 1 por empate y 0 por derrota.
2. **Diferencia de goles:** goles a favor menos goles en contra.
3. **Goles a favor:** se usa como tercer criterio de desempate.

Los equipos se ordenan de forma descendente considerando, en ese orden, los
puntos obtenidos, la diferencia de goles y los goles a favor.
