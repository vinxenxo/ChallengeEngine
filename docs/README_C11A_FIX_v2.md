# C11-A runner fix v2

This package fixes the PowerShell parser/runtime issue in `Invoke-GodotChecked`.

## Root cause

The previous script used `\` as line continuation characters in a `Start-Process`
call. PowerShell does not use backslash for line continuation, so `-FilePath` was
parsed as an independent command/token.

## Fix

`Start-Process` is now invoked as one syntactically valid command with `-Wait` and
`-PassThru`, preserving the required process synchronization.

The C11-A output remains isolated under:

`qa/c11a_visual_qa/`

Nothing in the historical `output/`, `output_batch_audit/`, `output_c7/` or C10 frozen
artifacts is touched by this fix.
