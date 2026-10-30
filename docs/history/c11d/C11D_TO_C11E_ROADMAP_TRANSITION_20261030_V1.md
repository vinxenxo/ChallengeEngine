# Transición histórica C11-D → C11-E — roadmap funcional

**Fecha de corte:** 2026-10-30.

Este addendum no reescribe los checkpoints ni receipts D. Registra por qué se abre E y cómo se reutilizan los activos D sin convertir los bloqueos históricos en autorizaciones ficticias.

## Qué aporta D

- Universal Editorial Model y resolver por capas.
- Solicitud universal D9.9 y planes GUI/CLI con identidad/hash.
- Catálogo y perfiles.
- Propuestas/bridges D9.10 y fachada común D de preparación.
- Motor D3 de música desacoplado por `music_seed`.

## Qué quedó sin demostrar

- El plan universal no es entrada física del renderer.
- La fachada compartida D y D9.10 mantienen `PREPARE_ONLY`; no ejecutar producción.
- La resolución de `title` no prueba consumo en un slot visual físico.
- La ruta Challenge C captura desde configuración de Challenge y su binder visual actual consume `content.hook`, CTA y telemetría, no un título editorial universal.
- La presencia de D3 no prueba aún el mux completo de la petición universal.

## Cambio de enfoque E

La meta E es un único servicio GUI/CLI de producción, con adapters por familia, que reutiliza el motor C y componentes D ya certificados. E posee sus propios contratos, receipts, gates de render aislado y decisión de promoción. No modifica los estados históricos D ni el manifiesto congelado C.

### Roadmap

1. E0 — fundación sobre `main` (PASS verificado).
2. E1 — servicio único GUI/CLI; request canónico, hashes, validación y errores; sin render.
3. E2 — primera evidencia de extremo a extremo: title-to-pixels en `CHALLENGE_001`, dos MP4 A/B aislados.
4. E3 — D3, audio y FFmpeg mux.
5. E4 — integración física Loop y Drill.
6. E5 — determinismo y regresión C.
7. E6 — Smoke 18.
8. E7 — Matrix 101, con exclusiones explícitas 008/009 si persiste su inconsistencia temporal.
9. E8 — aceptación, freeze y eventual promoción E, decisión independiente.

## No-go permanentes

No alterar C11-C 2.19.12, no mover las refs existentes, no usar `c11d-control`, no añadir un sexto módulo a `c11c-suite`, no reutilizar la fachada D como dispatcher, no compartir `request.seed` y `request.music_seed`, no mapear `title` a `hook`, no cambiar registros D y no afirmar promoción antes de E8.
