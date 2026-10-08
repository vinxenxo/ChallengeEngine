# C11-D D7.5 Runner V9 — PS 5.1 TrimStart Fix

V9 is a minimal overlay over the D7.5 Runner V8.

Fix:
- replaces the PowerShell 5.1-incompatible `TrimStart('\\\\','/')` call with `TrimStart([char]92,[char]47)`;
- no change to the D7.5 builder, mutation policy, C11-C source, simulation, RNG, evidence contract, or freeze data.

SHA-256 of the V9 overlay ZIP is provided with the artifact.
