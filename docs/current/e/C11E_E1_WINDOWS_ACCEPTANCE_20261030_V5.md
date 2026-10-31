# C11-E E1 — aceptación Windows (V5)

**Estado:** `E1_AUTOMATED_WINDOWS_TESTS_PASS_GUI_OPERATOR_RUNTIME_PENDING`

- Instalación: 8/8 archivos verificados.
- Pruebas Windows: `producer_gui_contract` y `producer_self_test`, 2/2 exit code 0.
- Runtime: Python 3.13.14.
- Checkout de la instalación: `main`, HEAD `bc8330e`.
- Consolidación posterior: commit `a3c7c5d284a96ce115ca52208b4039002502753b`, padre exacto `bc8330e`, árbol limpio, `main` ahead 1.
- E1 install receipt y Windows test receipt confirmaron los source pins del servicio, CLI, GUI, manifiesto Producer, self-test, AGENTS/CONTINUE y archivo de implementación.
- `renderer_input_emitted=false`, `renderer_dispatch_invoked=false`, `production_execution=false`, `media_created=false`, `release_authority=NONE`.

Las dos pruebas automatizadas son PASS. La observación manual de la GUI sigue pendiente y se registra separadamente; no invalida los dos tests ni debe describirse como ejecutada.
