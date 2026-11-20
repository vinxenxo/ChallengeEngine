# V4 evidence reconciliation — L2 QImage composition repair V5

The operator evidence archive contains `E6L2RGB24V4_20261120T095847Z_A8AA1CA7`. The V4 receipt SHA-256 is `b36f319a3b7e3290be965dfc1bfa28fdff789b6054e89fc9c3cba182130aad88` and its sidecar matches. The receipt is BLOCKED only after successful capture because Python raised `AttributeError: 'NoneType' object has no attribute '__dict__'`. Both recorded Godot processes exited 0.

`godot_import.log` registers `TypographyLabel`; `godot_capture.log` records `C11E_L2_CAPTURE=PASS/ONE_FRAME`. The 720x1280 `source_frame.png` and the 2,764,800-byte RGB24 buffer are present and SHA-pinned. This overlay reuses those exact artifacts and does not rerun Godot.
