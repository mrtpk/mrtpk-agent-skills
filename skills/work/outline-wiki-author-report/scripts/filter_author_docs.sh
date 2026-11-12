#!/usr/bin/env bash
# Filter Outline `list_documents` page files to the docs authored by one user.
#
# Usage:
#   filter_author_docs.sh <userId> <page1.txt> [<page2.txt> ...]
#
# Each page file is the raw output of a list_documents MCP call (one JSON object
# per line, each with a top-level ".document"). Output: one TSV row per authored
# document, deduped by document id and sorted newest-first:
#   created<TAB>title<TAB>url<TAB>archived<TAB>breadcrumb
#
# Requires: jq
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <userId> <page1.txt> [<page2.txt> ...]" >&2
  exit 2
fi

user_id="$1"
shift

cat "$@" \
  | jq -rc --arg uid "$user_id" '
      select(.document.createdBy.id == $uid)
      | { id: .document.id,
          created: (.document.createdAt[0:10]),
          title: .document.title,
          url: .document.url,
          archived: (if .document.archivedAt then "archived" else "" end),
          breadcrumb: (.breadcrumb // "") }' \
  | jq -sr '
      unique_by(.id)
      | sort_by(.created) | reverse
      | .[]
      | [.created, .title, .url, .archived, .breadcrumb] | @tsv'
