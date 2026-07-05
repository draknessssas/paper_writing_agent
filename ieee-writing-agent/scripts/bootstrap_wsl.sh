#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
INSTALL_SCOPE="${1:-user}"
CURRENT_MANUSCRIPT="${IEEE_MANUSCRIPT_PATH:-}"
SUPPORT_PACKAGE="${IEEE_SUPPORT_PACKAGE:-}"

link_path() {
  local source_path="$1"
  local dest_path="$2"
  local backup_suffix
  backup_suffix="$(date +%Y%m%d%H%M%S)"

  mkdir -p "$(dirname "$dest_path")"
  if [ -e "$dest_path" ] && [ ! -L "$dest_path" ]; then
    mv "$dest_path" "$dest_path.backup.$backup_suffix"
  fi
  ln -sfnT "$source_path" "$dest_path"
}

mkdir -p .agents/skills .claude/skills
mkdir -p .codex/agents .claude/agents .claude/output-styles
mkdir -p corpora/my_papers corpora/domain_papers/journal_reference_set corpora/domain_papers/topic_reference_set corpora/current_intro_refs
mkdir -p processed/my_papers processed/domain_papers/journal_reference_set processed/domain_papers/topic_reference_set processed/current_intro_refs
mkdir -p profiles/author_style profiles/journal_style profiles/topic_style profiles/domain_style working manuscript/sections templates/md-inputs

skills=(
  "paper-corpus-ingest"
  "author-style-profiler"
  "journal-style-profiler"
  "topic-style-profiler"
  "domain-style-profiler"
  "intro-reference-miner"
  "ieee-paragraph-writer"
  "ieee-reviewer"
  "ieee-style-extractor"
  "ieee-claim-ledger"
  "ieee-citation-verifier"
  "ieee-section-planner"
  "ieee-figure-caption-writer"
  "ieee-submission-auditor"
  "ieee-response-writer"
  "ieee-page-compressor"
)

for skill in "${skills[@]}"; do
  test -f "skills/$skill/SKILL.md" || {
    echo "Missing skills/$skill/SKILL.md"
    exit 1
  }

  ln -sfn "../../skills/$skill" ".agents/skills/$skill"
  ln -sfn "../../skills/$skill" ".claude/skills/$skill"
done

cat > profiles/active_profile.yml <<'EOF_ACTIVE'
author_style: profiles/author_style/current.md
journal_style: profiles/journal_style/current.md
topic_style: profiles/topic_style/current.md
domain_style: profiles/domain_style/current.md
intro_reference_map: working/intro_reference_map.md
EOF_ACTIVE
{
  printf 'current_manuscript: %s\n' "$CURRENT_MANUSCRIPT"
  printf 'support_package: %s\n' "$SUPPORT_PACKAGE"
} >> profiles/active_profile.yml

if [ "$INSTALL_SCOPE" != "local" ]; then
  mkdir -p "$HOME/.claude/agents" "$HOME/.claude/skills" "$HOME/.claude/output-styles"
  mkdir -p "$HOME/.codex/agents" "$HOME/.codex/skills"

  for skill in "${skills[@]}"; do
    link_path "$ROOT/skills/$skill" "$HOME/.claude/skills/$skill"
    link_path "$ROOT/skills/$skill" "$HOME/.codex/skills/$skill"
  done

  for agent_file in "$ROOT"/.claude/agents/*.md; do
    link_path "$agent_file" "$HOME/.claude/agents/$(basename "$agent_file")"
  done

  for style_file in "$ROOT"/.claude/output-styles/*.md; do
    link_path "$style_file" "$HOME/.claude/output-styles/$(basename "$style_file")"
  done

  for agent_dir in "$ROOT"/.codex/agents/*; do
    if [ -d "$agent_dir" ]; then
      link_path "$agent_dir" "$HOME/.codex/agents/$(basename "$agent_dir")"
    fi
  done
fi

echo "IEEE journal writing workspace bootstrapped."
echo "Codex skills: .agents/skills/"
echo "Claude skills: .claude/skills/"
echo "Codex agents: .codex/agents/"
echo "Claude agents: .claude/agents/"
if [ "$INSTALL_SCOPE" != "local" ]; then
  echo "User Claude skills: $HOME/.claude/skills/"
  echo "User Claude agents: $HOME/.claude/agents/"
  echo "User Codex skills: $HOME/.codex/skills/"
  echo "User Codex agents: $HOME/.codex/agents/"
fi
