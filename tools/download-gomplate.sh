#!/bin/bash -eu
parent="$1"

config_files_root=$(dirname "$(realpath "$BASH_SOURCE")")
version="$(cat "$config_files_root/gomplate-version")"
arch="$(uname -m | sed -e 's~x86_64~amd64~' -e 's~aarch64~arm64~')"
tmp_bin="$(mktemp -d --tmpdir=/tmp bin.XXXXXXX)"

echo "Downloading gomplate v$version ($arch) to $tmp_bin/gomplate..."
curl -L "https://github.com/hairyhenderson/gomplate/releases/download/v$version/gomplate_linux-${arch}" >"$tmp_bin/gomplate"

echo "Moving $tmp_bin/gomplate to $parent/gomplate..."
mv "$tmp_bin/gomplate" "$parent/gomplate" 2>/dev/null || sudo mv "$tmp_bin/gomplate" "$parent/gomplate"
sudo chmod a+x "$parent/gomplate"
