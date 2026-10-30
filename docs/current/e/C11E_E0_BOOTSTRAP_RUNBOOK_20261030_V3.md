# C11-E — runbook E0: foundation sobre la rama local `main`

**Versión:** V3 · **Fecha:** 2026-10-30 · **Estado antes de ejecución V3:** overlay pendiente de aplicación.

## 1. Decisión de operación Git

El usuario ha indicado expresamente que quiere trabajar localmente en la rama `main` dentro de `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. C11-E es el workstream técnico/documental, no una exigencia de cambiar la rama Git activa. El instalador V3 debe permanecer en `main`: no crea, cambia, borra, avanza ni publica ramas. Las refs local y remota `c11e-unified-editorial-production` observadas en E0-R3 quedan preservadas en `bc8330e`; no se actualizan.

## 2. Precondiciones

1. Windows PowerShell 5.1.
2. Root Git exacto indicado por el usuario.
3. Branch actual `main`.
4. HEAD `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`, cuyo padre único es `8f6905003a4dff979ed97dc2e721d1abc4375de8`; el commit toca solo los catálogos D JSON/Markdown.
5. Árbol de trabajo limpio.
6. Manifiesto C con 796318 bytes y SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
7. Preimages: `AGENTS.md` SHA `0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37`; `.continue/rules/CONTINUE.md` SHA `52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86`.
8. ZIP V3 hash verificado por el instalador.

## 3. Operaciones

- Extrae el ZIP a una carpeta temporal y valida manifest, número de ficheros, tamaños y SHA-256.
- Preflight de todos los destinos antes de escribir: si una ruta existe con distinto contenido, aborta. Si una ruta E ya existe con el SHA esperado, la considera instalada y no la sobrescribe.
- Copia `AGENTS.md` y `CONTINUE.md` originales, byte por byte, a `docs/history/c11d/` y verifica los dos SHA preimages.
- Instala los documentos de E y sustituye las dos instrucciones activas por las versiones E, verificando cada hash.
- Comprueba que HEAD sigue siendo `bc8330e`, branch sigue siendo `main` y manifiesto C conserva tamaño/hash.
- Escribe `C11E_E0_BOOTSTRAP_RECEIPT.json` fuera del repositorio bajo `Documents/C11E_E0_BOOTSTRAP_*`.

No hace `git switch`, `git branch`, `git push`, `git commit`, `git reset`, `git clean`, renderer, Godot, FFmpeg ni generación de media. No modifica código de producción.

## 4. Ejecución

Coloca `C11E_FOUNDATION_OVERLAY_20261030_V3.zip` y `APPLY_C11E_FOUNDATION_OVERLAY_20261030_V3.ps1` en la misma carpeta, preferiblemente `Downloads`, y ejecuta:

```powershell
Set-Location 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\APPLY_C11E_FOUNDATION_OVERLAY_20261030_V3.ps1" -Root 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
```

## 5. Resultado y revisión

- Branch activa: `main`, sin cambios de HEAD.
- Ref local/remota `c11e-unified-editorial-production`: sin modificaciones.
- 12 ficheros del overlay verificados (incluye las instrucciones de enrutamiento y documentos E).
- Dos copias históricas pre-E verificadas.
- Manifiesto C intacto.
- Árbol de trabajo modificado solo por los paths declarados en el overlay.
- Receipt externo en estado `E0_BOOTSTRAP_APPLIED_NOT_YET_REVIEWED`.
- Sin render, MP4, commit ni push.

Comparte el output y receipt. E0 solo se cierra PASS después de revisar diff, lista de paths, hashes, branch/HEAD, pin C y receipt.
