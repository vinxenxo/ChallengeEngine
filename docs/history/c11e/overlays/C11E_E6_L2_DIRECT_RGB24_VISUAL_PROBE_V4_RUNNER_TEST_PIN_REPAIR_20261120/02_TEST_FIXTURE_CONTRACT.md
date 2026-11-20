# V4 focused-test fixture contract

The installer remains a package-root member and is not copied into the active repository. The V4 unit suite obtains its exact file path through `C11E_L2_INSTALLER_SOURCE`, supplied by the operator from the fresh ZIP extraction directory.

This keeps install tooling separate from repository destinations while still allowing the focused suite to inspect the exact installer source that passed the package member SHA checks. When the variable is missing, the suite reports a direct assertion with the required environment variable; it does not attempt a guessed repository-root path.
