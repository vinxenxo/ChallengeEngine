# C11-D D8.4 Artifact Eligibility Fix V5

Root cause fixed: Windows PowerShell 5.1 overload binding for String.TrimStart when a string is passed to a char[] overload.

Changed:
- `.TrimStart('\\')` -> `.TrimStart([char]'\\')`
- `.TrimStart('./')` -> `.TrimStart([char[]]@('.', '/'))`

No D8.4 governance, D7 authority, media scope or eligibility rule is changed.
