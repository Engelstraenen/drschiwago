#!/bin/bash
# Lädt fertige sjinn-Ergebnisse: tools/fetch.sh ID=URL [ID=URL ...]  (DSM-04T wird als DSM-04 gespeichert)
M=~/Library/CloudStorage/Dropbox-FAVELAClothing/CLAUDE/Content/DRSCHIWAGO/motive
V="$(dirname "$0")/../konzepte/motive-vorschau"
for kv in "$@"; do
  id="${kv%%=*}"; url="${kv#*=}"; [ "$id" = "DSM-04T" ] && id="DSM-04"
  [ -f "$M/$id.png" ] && { echo "$id schon da"; continue; }
  curl -s -f -o "$M/$id.png" "$url" && sips -Z 2000 -s format jpeg "$M/$id.png" --out "$V/$id.jpg" >/dev/null && echo "$id $(sips -g pixelWidth -g pixelHeight "$M/$id.png" | awk '/pixel/{printf "%s ",$2}')"
done
