# Claims

Local claim records for active or recent GitHub Issue work.

GitHub Issue comments are the primary audit trail. Files here are local coordination helpers.

Active records should contain a lease and use `claimed` or `running`.

Every record carries a `project` field recording which project the claimed issue
belongs to (e.g. `fx-strategy-research`) or `self-evo` for the operating method
itself. This value MUST equal the issue's `project:<name>` label and the
matching `projects/<name>/` directory. It is consumed by the run validator's
project-consistency check to prevent a worker from writing into the wrong
project's tree.

Before an Issue moves to `status:review`, update the record to `review` or `released`, add `released_at`, and remove the active lease. Keep the file as an audit record unless a later cleanup policy archives it.
