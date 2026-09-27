# C11-C Producer 0.4.0

Producer mínimo basado en la interfaz de C11-C Producer 0.2.0. Se conserva el formulario original y se añade únicamente un selector superior de tipo de vídeo: CHALLENGES / VISUAL LOOPS / VISUAL DRILLS.

En esta fase solo VISUAL LOOPS tiene generación conectada. CHALLENGES y VISUAL DRILLS están presentes en el selector para preparar la expansión posterior, pero no ejecutan ningún launcher.

Fuente única de verdad del backend: `ChallengeEngineV01_STATELESS-C11-C2.9.1.zip`. El Producer usa el `C11CVariationProfile.gd` real del proyecto y verifica su SHA-256.

La misma familia + seed reproduce el mismo perfil; seeds nuevas producen variantes nuevas. Los parámetros se dejan en `ALEATORIO (seed)` por defecto.
