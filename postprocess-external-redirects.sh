#!/bin/bash
config_files_root="$(dirname "$(realpath "$BASH_SOURCE")")"

# Install tools
tmp_bin="$(mktemp -d --tmpdir=/tmp bin.XXXXXXX)"
"$config_files_root/tools/download-yq.sh" "$tmp_bin"
"$config_files_root/tools/download-jq.sh" "$tmp_bin"
"$config_files_root/tools/download-gomplate.sh" "$tmp_bin"
export PATH="$tmp_bin:$PATH"

# Prepare build
rm -rf "$config_files_root/build"
mkdir "$config_files_root/build"

# Generate redirects
readarray redirects < <(yq e -o=j -I=0 '.[]' redirects.yml)
for redirect in "${redirects[@]}"; do
  to="$(jq --raw-output ".to" <<<"$redirect")"
  from="$(jq --raw-output ".from" <<<"$redirect")"
  if [ "$to" == "null" ]; then
    echo "Warning: No redirect target specified from $from"
    to="https://docs.openuc2.com"
  fi
  output_dir="$config_files_root/build$from"
  mkdir -p "$output_dir"
  TARGET="$to" gomplate <redirect.html.tmpl >"$output_dir/index.html"
done

# Clean up
rm -rf tmp_bin
