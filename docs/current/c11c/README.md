# C11-C 2.19.6 current documentation

`C11-C_2.19.6_CONSOLIDATED_STATE.md` is the active state authority.

The current repair is the per-worker Godot class-cache bootstrap required after excluding source `.godot` from the isolated worker copies. It preserves real `Workers=7` capture concurrency and does not introduce a global mutex.
