#!/usr/bin/env bash
# Portable bootstrap for the manuscript writing workspace.
# Works on Linux, WSL, and macOS. For native Windows use scripts/bootstrap.ps1.
#
# Usage:
#   ./scripts/bootstrap.sh          # link skills/agents into the repo AND into $HOME (user scope)
#   ./scripts/bootstrap.sh local    # link only inside the repo, leave $HOME untouched
#
# Optional environment variables (existing values in profiles/active_profile.yml are kept when unset):
#   IEEE_MANUSCRIPT_PATH=/path/to/main.tex
#   IEEE_BIB_PATH=/path/to/refs.bib
#   IEEE_VENUE=tpel               (blank = venue-neutral)
#   IEEE_PAPER_TYPE=regular|letter
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
INSTALL_SCOPE="${1:-user}"
PROFILE="profiles/active_profile.yml"

case "$INSTALL_SCOPE" in user|local) ;; *) echo "Scope must be user or local" >&2; exit 2 ;; esac
PYTHON="${IEEE_PYTHON:-python3}"
"$PYTHON" "$ROOT/scripts/profile_config.py" --root "$ROOT"

# Portable symlink helper (GNU `ln -sfnT` is not available on macOS/BSD).
link_path() {
  local source_path="$1"
  local dest_path="$2"
  mkdir -p "$(dirname "$dest_path")"
  if [ -L "$dest_path" ] && [ "$(readlink "$dest_path")" = "$source_path" ]; then
    return
  fi
  if [ -L "$dest_path" ]; then
    rm -f "$dest_path"
  elif [ -e "$dest_path" ]; then
    mv "$dest_path" "$dest_path.backup.$(date +%Y%m%d%H%M%S).$$"
  fi
  ln -s "$source_path" "$dest_path"
}

# Remove a stale symlink (never a real file or directory).
prune_link() {
  local path="$1"
  if [ -L "$path" ]; then
    rm -f "$path"
    echo "pruned stale link: $path"
  fi
}

skills=(
  "writing-skill"
  "style-profiler"
  "citation-verifier"
  "manuscript-reviewer"
)

# Names used by earlier versions of this workspace; their symlinks are removed.
legacy_skills=(
  paper-corpus-ingest author-style-profiler journal-style-profiler topic-style-profiler
  domain-style-profiler intro-reference-miner ieee-paragraph-writer ieee-reviewer
  ieee-style-extractor ieee-claim-ledger ieee-citation-verifier ieee-section-planner
  ieee-figure-caption-writer ieee-submission-auditor ieee-response-writer ieee-page-compressor
)
legacy_claude_agents=(ieee-writing-agent.md ieee-technical-skeptic.md)
legacy_codex_agents=(ieee-writer ieee-technical-skeptic)
legacy_output_styles=(ieee-writer.md)

mkdir -p .agents/skills .claude/skills .codex/agents .claude/agents .claude/output-styles
mkdir -p corpora/exemplars corpora/my_papers processed/exemplars processed/my_papers processed/refs
mkdir -p profiles working/briefs working/drafts working/ref_notes refs manuscript/sections templates knowledge/venues

for skill in "${skills[@]}"; do
  test -f "skills/$skill/SKILL.md" || { echo "Missing skills/$skill/SKILL.md"; exit 1; }
  link_path "../../skills/$skill" ".agents/skills/$skill"
  link_path "../../skills/$skill" ".claude/skills/$skill"
done
for skill in "${legacy_skills[@]}"; do
  prune_link ".agents/skills/$skill"
  prune_link ".claude/skills/$skill"
done


if [ "$INSTALL_SCOPE" != "local" ]; then
  mkdir -p "$HOME/.claude/agents" "$HOME/.claude/skills" "$HOME/.claude/output-styles"
  mkdir -p "$HOME/.codex/agents" "$HOME/.codex/skills" "$HOME/.agents/skills"

  for skill in "${skills[@]}"; do
    link_path "$ROOT/skills/$skill" "$HOME/.claude/skills/$skill"
    link_path "$ROOT/skills/$skill" "$HOME/.codex/skills/$skill"
    link_path "$ROOT/skills/$skill" "$HOME/.agents/skills/$skill"
  done
  for skill in "${legacy_skills[@]}"; do
    prune_link "$HOME/.claude/skills/$skill"
    prune_link "$HOME/.codex/skills/$skill"
    prune_link "$HOME/.agents/skills/$skill"
  done

  for agent_file in "$ROOT"/.claude/agents/*.md; do
    link_path "$agent_file" "$HOME/.claude/agents/$(basename "$agent_file")"
  done
  for name in "${legacy_claude_agents[@]}"; do prune_link "$HOME/.claude/agents/$name"; done

  for style_file in "$ROOT"/.claude/output-styles/*.md; do
    link_path "$style_file" "$HOME/.claude/output-styles/$(basename "$style_file")"
  done
  for name in "${legacy_output_styles[@]}"; do prune_link "$HOME/.claude/output-styles/$name"; done

  for agent_dir in "$ROOT"/.codex/agents/*; do
    [ -d "$agent_dir" ] && link_path "$agent_dir" "$HOME/.codex/agents/$(basename "$agent_dir")"
  done
  for name in "${legacy_codex_agents[@]}"; do prune_link "$HOME/.codex/agents/$name"; done
fi

echo "Writing workspace bootstrapped ($INSTALL_SCOPE scope)."
echo "Active profile: $PROFILE"
echo "Status: $PYTHON scripts/profile_status.py"
echo "Parity check: python3 scripts/check_parity.py"
echo "Codex skills: .agents/skills/   Claude skills: .claude/skills/"
echo "Codex agents: .codex/agents/    Claude agents: .claude/agents/"
if [ "$INSTALL_SCOPE" != "local" ]; then
  echo "User Claude skills/agents/output-styles: $HOME/.claude/"
  echo "User Codex skills: $HOME/.agents/skills/ (legacy aliases: $HOME/.codex/skills/)"
  echo "User Codex agents: $HOME/.codex/agents/"
fi
