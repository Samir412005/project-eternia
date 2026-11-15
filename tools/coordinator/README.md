# Coordinator
Agent collaboration rules (brief §09):
- One agent edits one file set at a time; no concurrent edits to the
  same files without coordination.
- Git checkpoint before every major change.
- Every agent report lists: task, files changed, commands run,
  test results, remaining problems.
- No API keys or secrets in the repo, ever.
