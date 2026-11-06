#!/usr/bin/env bash
# Install the `prism` command: the Prism API from your terminal with one Fliar API key.
#   curl -fsSL https://radar-api.fliarbi.com/prism/install.sh | bash
# Installs to ~/.local/bin (no sudo, no services) and sets PRISM_URL for new shells.
# Set FLIAR_API_KEY=rdr_... before running to save your key as well.
set -euo pipefail

PRISM_URL="${PRISM_URL:-https://radar-api.fliarbi.com/prism}"
BIN="${PRISM_BIN_DIR:-$HOME/.local/bin}"

command -v python3 >/dev/null 2>&1 || { echo "prism needs Python 3.8 or newer (python3 not found)." >&2; exit 1; }
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' || { echo "prism needs Python 3.8 or newer." >&2; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "prism install needs curl." >&2; exit 1; }

mkdir -p "$BIN"
tmp="$(mktemp)"
curl -fsSL "$PRISM_URL/cli/prism" -o "$tmp"
head -1 "$tmp" | grep -q python3 || { echo "Download did not return the prism CLI." >&2; rm -f "$tmp"; exit 1; }
install -m 0755 "$tmp" "$BIN/prism"
rm -f "$tmp"

line="export PRISM_URL=\"$PRISM_URL\""
for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
  [ -f "$rc" ] || continue
  grep -qs '^export PRISM_URL=' "$rc" || printf '\n# Prism API (prism CLI)\n%s\n' "$line" >> "$rc"
done
case ":$PATH:" in *":$BIN:"*) ;; *)
  for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    [ -f "$rc" ] && ! grep -qs "$BIN" "$rc" && printf 'export PATH="%s:$PATH"\n' "$BIN" >> "$rc"
  done;;
esac

if [ -n "${FLIAR_API_KEY:-}" ]; then
  PRISM_URL="$PRISM_URL" "$BIN/prism" login "$FLIAR_API_KEY" >/dev/null && echo "Saved your API key."
fi

echo "Installed prism to $BIN/prism"
echo "Next:  prism login            (paste your rdr_ key from https://fliarbi.com/radar/dashboard?tab=radarapi)"
echo "       prism entity \"tata motors\"    prism compare \"narendra modi\" \"donald trump\"    prism mcp claude"
echo "Open a new shell (or run: $line) to use PRISM_URL."
