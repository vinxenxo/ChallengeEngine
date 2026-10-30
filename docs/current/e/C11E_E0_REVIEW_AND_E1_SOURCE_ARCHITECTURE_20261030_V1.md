# C11-E — revisión E0 y análisis arquitectónico E1

**Fecha:** 2026-10-30 · **Estado:** E0 revisado; E1 en curso.

## 1. Evidencia revisada

### E0

Paquete: `C11E_E0_REVIEW_20261030_080515.zip`  
SHA-256: `780e964b09613f6157fa84165f55b6a6e169bc292dd0abf854af73c111fa6420`  
Tamaño: 170210 bytes.

Resultado: ZIP íntegro; recibo presente; 12/12 hashes de ficheros instalados coinciden con el recibo; 2/2 copias archivadas de `AGENTS.md` y `CONTINUE.md` coinciden con sus hashes pre-E. El recibo registra `main`, HEAD `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`, manifiesto C de 796318 bytes y SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; no renderer, media, commit ni push.

El error de consola por ejecutar `else` separado del `if` no invalida la captura: el recibo está presente en el ZIP y se verificó dentro del paquete.

### E1

Paquete: `C11E_E1_SOURCE_REVIEW_20261030_102020.zip`  
SHA-256: `fd7d1f7b0023a73adfe0e721452bc038de66a560dfa56eb516211a61ac7e93b1`  
Tamaño: 111532 bytes; 32 entradas; CRC íntegro.

Checkout registrado por la captura: `main`, HEAD `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`. Estado Git: exclusivamente cambios documentales E0 no confirmados; no aparecen cambios de código. Las refs locales/remotas C11-E permanecen en el mismo HEAD.

La captura incluye 17 fuentes. Dos `BUILD_MANIFEST.json` están bajo `artifacts/legacy` y son material histórico/compatibilidad. La arquitectura activa de suite está formada por los cinco módulos existentes: `c11c-producer`, `c11c-test`, `c11c-catalog`, `c11c-config` y `c11c-maintenance`. No crear un sexto módulo.

## 2. Hallazgos de integración

1. `c11c-suite/c11c-producer/BUILD_MANIFEST.json` mantiene D9.9/D9.10 como ruta de planificación: `renderer_input_emitted=false` y `production_execution=false`. El GUI de producción definitivo sigue diferido en el contrato D. Este manifiesto no autoriza convertir el adapter D en renderer.
2. `tools/c11d/d9/shared_production_context_service.py` declara una fachada común de preparación D, con estado `PREPARE_ONLY_COMMON_BACKEND_FACADE_NOT_RENDERER_INPUT`. Tiene invariantes de renderer/producción bloqueados. No reutilizarlo como servicio de ejecución E ni relajar sus invariantes.
3. `tools/c11d/d9/universal_editorial_model.py` permite actualmente `title`, `subtitle`, `call_to_action` y `language` en Challenges, Loops y Drills; `player_name` y `challenge_label` son exclusivos de Challenges. `hook`, `preparation_text`, `final_text` y los campos de layout `header_*`, `footer_*`, `show_*` permanecen deshabilitados/reservados.
4. D9.9 `evaluate_universal_request` produce request canónico, hash, resolución editorial y plan. Para Challenge el plan aún sigue la solicitud D4; que el plan contenga `title` no prueba que el render físico lo consuma.
5. `core/presentation/ChallengePresentationBinder.gd` genera `hook_text` desde `content.hook` y estado de fase. El consumidor `HookComponent` pinta ese `hook_text`; no existe un slot de título universal en ese camino. `title` y `hook` son semánticas distintas: nunca mapear uno al otro para conseguir una diferencia visual.
6. `VisualContentPlayer.gd` y los binders Loop/Drill emplean otro camino. La capa `C11CVisualEditorialLayer` está montada en el camino de Drill; el binder Loop no aporta el mismo modelo editorial. No generalizar la conclusión Challenge a todas las familias ni asumir que el layer ya es un consumidor universal.
7. `c11d_music_engine_v5.py` es una pieza D3 separada que recibe `music_seed`; audio/mux sigue siendo gate E3. No mezclar `music_seed` con `request.seed` ni introducir música en la primera prueba visual E2.
8. `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` y `Main.tscn` están incluidos en el manifiesto congelado C. El runner C fija `--scene Main.tscn` y gestiona el pipeline C de captura/FFmpeg/FFprobe; no se modifica para añadir parámetros o despacho E. E debe poseer un runner/adaptador propio, que invoque el mismo runtime C con una escena/adaptador E aislado y un sidecar editorial separado del JSON de Challenge.

## 3. Decisión de arquitectura E1

La capa E será propia y se situará en el módulo existente `c11c-suite/c11c-producer`. Un único servicio E normalizará y validará el request para las dos superficies GUI/CLI, reutilizando D9.9 como resolver/validador canónico cuando sus contratos y pines lo permitan. El servicio E producirá una envoltura de producción E, identidad/hash, contexto editorial resuelto, adapter por familia y receipt E.

D9.10, `shared_production_context_service.py`, los receipts D y las banderas históricas D quedan intactos. El servicio E no falsifica ni hereda la aprobación de un gate D.

### Primer consumidor visual E2

Para Challenge, introducir un consumidor E aditivo y aislado que dibuje `editorial.title` en un slot propio del Header. El slot debe respetar el layout 540×960 y su región Header 0–144, usar la tipografía/perfil vigente y dejar intactos Hook, CTA y Body. La ruta de render debe continuar ejecutando el `GeneradorMaestro.gd` C y el mismo Movie Maker/FFmpeg/FFprobe; el adapter E solo añade presentación.

La primera opción técnica a validar es una escena E derivada de `Main.tscn` con un script E que extienda `GeneradorMaestro.gd`, llame al `_ready()` C sin alterar su ejecución y después monte el slot `title` en Header leyendo un sidecar CLI `--c11e-editorial=...`. El runner E llamaría a Godot con esa escena E, conservaría la configuración C y realizaría su propia validación/entrega FFmpeg/FFprobe. Esto es una propuesta de implementación, no una prueba ya ejecutada.

La forma concreta se cierra tras cotejar hashes del checkout activo para `GeneradorMaestro.gd`, `Main.tscn`, `PresentationUI.gd`, `SocialUIBinder.gd`, `HookComponent.gd`, `TypographyLabel.gd`, `PresentationTheme.gd`, el runner C y la definición `CHALLENGE_001`. No editar esos ficheros protegidos ni suponer que el snapshot equivale a un pin vivo.

## 4. Pines de referencia C

El snapshot de trabajo 2026-10-29 contiene los mismos hashes que el manifiesto congelado C para estos ficheros. Son referencias base del manifiesto, no sustituyen el recálculo desde el checkout antes de cambiar código:

| Ruta | SHA-256 | Bytes |
|---|---|---:|
| `GeneradorMaestro.gd` | `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9` | 36991 |
| `Main.tscn` | `5271714b9a5c31aeda1d7347347f1429ca37a48c081e59e6ec42383626731de7` | 1086 |
| `core/presentation/PresentationUI.gd` | `a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730` | 8981 |
| `core/presentation/SocialUIBinder.gd` | `b15a062bf327d0c2bbc4ead0e877914f912528cc56e388df20dd84eb89863a3c` | 1742 |
| `core/presentation/components/HookComponent.gd` | `52894359fc80f4647493fb37fa185aae3dcdc8daf1ac1fdc37137d13debb7bbe` | 806 |
| `core/presentation/PresentationBinderRegistry.gd` | `bb12400cb748821b191e09db19b85105708d47a50db66c84b5f95fe6ff98ee66` | 2480 |
| `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` | `c3fed414912f50efed1687e258c48c5e85c08989a473ed12c38dc9784db171d5` | 18191 |
| `challenges/CHALLENGE_001.json` | `ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea` | 1085 |

## 5. Foco inmediato

1. Cotejar los ficheros anteriores contra el checkout activo y el manifiesto C; detenerse ante cualquier hash inesperado.
2. Implementar el servicio E compartido GUI/CLI y sus contract tests, sin dispatch físico (E1).
3. Implementar el slot/adapter visual E de Challenge y la ruta de ejecución aislada.
4. Ejecutar únicamente la pareja A/B autorizada de `CHALLENGE_001` al abrir E2; revisar frames/píxeles y comparar gameplay antes de ampliar a Loop/Drill.

No crear otra auditoría general ni volver a ejecutar fases D si sus source pins no han cambiado. Cada test debe responder a un riesgo de integración concreto.
