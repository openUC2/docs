#!/bin/bash -eu
parent="$1"

config_files_root=$(dirname "$(realpath "$BASH_SOURCE")")
version="$(cat "$config_files_root/yq-version")"
arch="$(uname -m | sed -e 's~x86_64~amd64~' -e 's~aarch64~arm64~')"
tmp_bin="$(mktemp -d --tmpdir=/tmp bin.XXXXXXX)"

echo "Downloading yq v$version ($arch) to $tmp_bin/yq..."
curl -L "https://github.com/mikefarah/yq/releases/download/v$version/yq_linux_${arch}" >"$tmp_bin/yq"

echo "Moving $tmp_bin/yq to $parent/yq..."
mv "$tmp_bin/yq" "$parent/yq" 2>/dev/null || sudo mv "$tmp_bin/yq" "$parent/yq"
sudo chmod a+x "$parent/yq"
