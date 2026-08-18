#!/usr/bin/env bash
# Install Remit's skills so they can actually reach the framework they reference.
#
#   ./install.sh            # symlink into ~/.claude/skills
#   ./install.sh --copy     # copy instead of symlink
#   ./install.sh --uninstall
#
# Why this exists rather than a cp one-liner: every skill refers to the framework by
# relative path (../../framework/diagnostic-manual.md and friends — 13 references). Copy
# the skills folder alone, as the README used to advise, and every one of those dangles.
# The skills still load; they just quietly lose the manual, the schema, and the tier model.
#
# Symlinks are the default so `git pull` in this checkout updates your installed skills.

set -euo pipefail

REMIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${REMIT_SKILLS_DIR:-$HOME/.claude/skills}"
PARENT="$(dirname "$SKILLS_DIR")"
MODE="link"

for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    --uninstall) MODE="uninstall" ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

names() { for d in "$REMIT"/skills/*/; do basename "$d"; done; }

if [ "$MODE" = "uninstall" ]; then
  for n in $(names); do rm -rf "${SKILLS_DIR:?}/$n"; done
  rm -rf "$PARENT/framework"
  echo "Removed Remit skills from $SKILLS_DIR and framework from $PARENT"
  exit 0
fi

mkdir -p "$SKILLS_DIR"

# The skills sit at $SKILLS_DIR/<name>/, so ../../framework resolves to $PARENT/framework.
# That is the whole trick, and getting it wrong is why the old instructions failed.
rm -rf "$PARENT/framework"
if [ "$MODE" = "link" ]; then
  ln -s "$REMIT/framework" "$PARENT/framework"
else
  cp -R "$REMIT/framework" "$PARENT/framework"
fi

for n in $(names); do
  rm -rf "${SKILLS_DIR:?}/$n"
  if [ "$MODE" = "link" ]; then
    ln -s "$REMIT/skills/$n" "$SKILLS_DIR/$n"
  else
    cp -R "$REMIT/skills/$n" "$SKILLS_DIR/$n"
  fi
done

# Verify rather than assume — the failure this script exists to prevent is silent.
fail=0
for n in $(names); do
  while IFS= read -r ref; do
    [ -e "$SKILLS_DIR/$n/$ref" ] || { echo "  ✗ $n → $ref"; fail=1; }
  done < <(grep -oh '\.\./\.\./[a-zA-Z0-9._/-]*' "$SKILLS_DIR/$n/SKILL.md" 2>/dev/null \
           | grep -v '/$' | sort -u)
done

echo
if [ "$fail" -eq 0 ]; then
  echo "✓ Installed $(names | wc -l | tr -d ' ') skills to $SKILLS_DIR ($MODE)"
  echo "✓ Every framework reference resolves"
  echo
  echo "Try it — describe a system in plain language and the right skill should fire:"
  echo "  \"we're putting a model into the loan decisioning flow, what do we need to do\""
else
  echo "✗ Installed, but some references do not resolve (listed above)." >&2
  exit 1
fi
