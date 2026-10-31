# C11-E — reconciliación de HEAD antes de E2 (V1)

**Fecha:** 2026-10-30.

El instalador E2 V2 esperaba `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`. El checkout de operador estaba en `main` / `a3c7c5d284a96ce115ca52208b4039002502753b`.

El registro Git proporcionado por el operador identifica:

- Commit `a3c7c5d284a96ce115ca52208b4039002502753b`.
- Subject `C11-E foundation overlay`.
- Parent único `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.
- Diff contiene el overlay fundacional E y los seis fuentes E1 (service, CLI, GUI main, producer manifest, self_test y GUI contract), documentación actual e histórica E.
- `git status --porcelain` vacío; `main` ahead 1 de `origin/main`.

Los recibos E1 comunicados confirman que los seis source postimages están instalados y sus hashes coinciden con el commit. Por tanto, `a3c7c5d` es la continuación legítima de E1, no una divergencia externa ni una modificación protegida C.

El paquete E2 V2 abortó en checkout preflight, antes de la primera escritura. El wrapper informó expresamente que el renderer físico no fue invocado. No se crearon AVI/MP4 ni recibos de render E2.

La nueva versión E2 V3 no acepta cualquier descendiente: exige el branch `main`, HEAD exacto `a3c7c5d`, parent exacto `bc8330e`, tree limpio, C11-C manifest inmutable, recibos E1 Windows en Documents y seis source pins E1. Solo entonces permite instalar E2.
