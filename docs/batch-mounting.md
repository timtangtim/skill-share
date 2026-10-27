# Batch mounting

Use `./mount-skill.sh --all` to mount every immediate non-hidden skill folder
under the script's adjacent `skill/` directory. This works from other working
directories and keeps the existing single-skill command available.

Sources are resolved and validated, including duplicate resolved names, before
all destinations are checked for conflicts. No links are created for a batch
with invalid input or a pre-existing conflict. Runtime I/O failures can still
leave earlier links installed; mounting is not transactional. Correct the error
and rerun. An empty collection succeeds without creating destination directories.

## Verification

- `bash -n mount-skill.sh`: passed.
- `python3 -B -m unittest discover -s tests -v`: all 14 tests passed on macOS.
- Batch coverage: multiple skills across all three destinations, repeat mounting,
  calling from another directory, spaces in repository paths, ignored files,
  empty/missing collections, invalid later skills, later conflicts, and duplicate
  resolved names. Original single-skill regression checks still pass.
- `git diff --check`: passed.

Tests use temporary home directories. Actual discovery and execution in host
agents and execution on GNU/Linux remain unverified. The source collection is
still empty; add real skill folders before mounting. No installed skills were
changed during this work.
