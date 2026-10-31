# C11-E E2 V3 — incidente del guard de rutas (2026-10-30)

- Paquete: `C11E_E2_EXECUTION_PACKAGE_20261030_V3.zip`.
- Checkout reportado: `main`, HEAD `a3c7c5d284a96ce115ca52208b4039002502753b`, padre `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.
- Resultado: `Overlay destination escapes repository root: c11c-suite/c11c-producer/main.py`.
- El error sucede en `Assert-SafeRelativePath` antes de la primera escritura del overlay. El runner indica que renderer físico no fue invocado.
- Causa: `$RepositoryRoot.TrimEnd('\') + '\'` utiliza dos caracteres de barra inversa en cada literal PowerShell single-quoted. El prefijo resultante contiene dos separadores consecutivos, mientras que la ruta absoluta normalizada contiene uno; `StartsWith()` rechaza falsamente una ruta válida.
- Corrección V4: `GetFullPath` para raíz y destino; trim con `char[]` de `DirectorySeparatorChar`/`AltDirectorySeparatorChar`; añadir un único `DirectorySeparatorChar`; convertir `/` a separador nativo con `String.Replace(char,char)`; mantener rechazos para rooted/traversal y reparse points.
- No revertir ni modificar el checkout para reparar el paquete. Reintentar desde el mismo commit con instalador corregido y preflight completo.
