# C11-C Studio v0.4.1

## UX/UI
- Bright/light theme replacing the previous dark theme.
- High-contrast form controls with readable text, visible borders and readable dropdown lists.
- Navigation buttons inherit the global theme instead of carrying dark inline styling.
- Generate screen spacing tightened for a cleaner production control surface.

## Command adapter hotfix
- PowerShell array parameters such as `-Seeds` are serialized as one comma-separated process argument.
- Applied consistently to Art Direction Review, Production Bulk and all three review export commands.
- Canonical commands retain the project root as working directory.
- No backend C11-B/C rendering or generation logic is modified.
