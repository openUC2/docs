#!/bin/bash -eu
parent="$1"

config_files_root=$(dirname "$(realpath "$BASH_SOURCE")")
version="$(cat "$config_files_root/jq-version")"
arch="$(uname -m | sed -e 's~x86_64~amd64~' -e 's~aarch64~arm64~')"
tmp_bin="$(mktemp -d --tmpdir=/tmp bin.XXXXXXX)"

echo "Downloading jq v$version ($arch) to $tmp_bin/jq..."
curl -L "https://github.com/jqlang/jq/releases/download/jq-$version/jq-linux-${arch}" >"$tmp_bin/jq"

echo "Moving $tmp_bin/jq to $parent/jq..."
mv "$tmp_bin/jq" "$parent/jq" 2>/dev/null || sudo mv "$tmp_bin/jq" "$parent/jq"
sudo chmod a+x "$parent/jq"
