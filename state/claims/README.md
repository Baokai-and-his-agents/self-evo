# Claims

Local claim records for active or recent GitHub Issue work.

GitHub Issue comments are the primary audit trail. Files here are local coordination helpers.

Active records should contain a lease and use `claimed` or `running`.

Before an Issue moves to `status:review`, update the record to `review` or `released`, add `released_at`, and remove the active lease. Keep the file as an audit record unless a later cleanup policy archives it.
