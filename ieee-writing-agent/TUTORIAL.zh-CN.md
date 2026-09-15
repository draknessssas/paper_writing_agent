# 使用教程：2026.09.14 版

这套工具共用四个 skills、两类 agent、论文画像和检查脚本。Codex 选择 GPT-6 Astra 属于客户端配置；Claude 保留其模型选择。升级规则不需要重新训练模型或重建语料。

## 安装与入口

Linux/WSL，在工具目录运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash scripts/bootstrap.sh user
python -B scripts/check_parity.py --installed
python -B scripts/profile_status.py
```

完整工具建议 Python 3.11 及以上。`local` 只建立项目入口，适合试用副本；`user` 会更新用户级入口。现代 Codex 技能位于 `~/.agents/skills`，兼容链接保留在 `~/.codex/skills`。Claude 技能和角色位于 `~/.claude`。安装脚本不修改全局模型或账户。

Windows PowerShell，在工具目录运行（示例使用已安装的 Python 3.12）：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Scope user
.\.venv\Scripts\python.exe -B scripts\check_parity.py --installed
```

bootstrap 使用 Python/PyYAML 保留已有自定义配置字段。确需更新时先保存 `.backup.<时间>`；未变化时不重写。`IEEE_MANUSCRIPT_PATH`、`IEEE_BIB_PATH`、`IEEE_VENUE`、`IEEE_PAPER_TYPE` 可覆盖对应字段，显式空值可清除路径或期刊。清空 paper_type 无效，应使用 regular 或 letter。

普通文件/目录与入口重名时会保留备份；Windows 文件可能回退为硬链接或副本，副本不会自动跟随源文件更新。安装完成后开启新客户端会话，以加载新的描述和角色规则。

启动客户端时，从工具目录启动并授予论文目录访问，例如 `codex --add-dir /你的论文目录` 或 `claude --add-dir /你的论文目录`。账户登录和模型可用性由客户端决定。本机已有客户端时无需为更新 skill 再安装客户端。

## 日常请求怎么写

Codex 输入 `使用 $writing-skill`，Claude 输入 `/writing-skill`，然后用正常语言说明任务。结构化 brief 可用，但无需背字段。

```text
压缩下面这段到 120 词，保留意思、工况和引用：<原文>
```

原文可提供既有 claim，不用再写 `claim: unchanged`。保留原数字不代表已经核验原始实验；若只做文字修改，会准确说明验证范围。

```text
继续上次确定的第二段，claim 和参考文献沿用 manuscript_state.md。
```

工具先查前文和状态，不要求你重复填写已经确定的信息。

```text
根据 reference/II/A 提出 II-A 的候选 claim 和证据位置，等我确认后再写。
```

工具可以分析文献并提出候选判断，但会停在你要求的确认点。候选不会自动记为作者已批准。

```text
根据参考文献先提出候选 claim，然后逐段写完 II-A，保存独立草稿，最后检查整节衔接。
```

这明确授权从候选继续起草。工具逐段检查并完成整节，记录候选来源和未解决问题；不冒充作者最终判断。只有关键证据不足或真实科学决策冲突时才暂停相关部分。

```text
直接修改 drafts/II_A/section_II_A.tex 的第二段，统一这里的术语，其他段不改。
```

这已经授权指定修改，不必补填 `insert:`。统一全文某个已指定术语也可直接用自然语言授权。

```text
先分析，不写正文，也不创建或修改任何文件。
```

这种请求保持只读，不创建 manuscript_state、笔记或草稿。

## 输入不足时

“写数字孪生”只是主题，不足以自动决定研究结论。新结果段至少需要可靠的结果、条件和比较对象；文献断言需要来源。工具会说明真正缺少什么，并继续已授权且不依赖这些缺项的分析。不会编数据、文献、图号或创新性。

默认输出为正文加简短重要说明。`annotated` 提供完整 claim/证据表；`clean` 减少说明但仍显示未解决问题；`confirm-first` 是明确暂停点。六种原模式保留，新增 `plan` 表示候选观点规划；文献处理仍是按需分支。

## 画像与论文状态

`profiles/index.md` 是入口。写分类段只读相关 taxonomy/引用组织部分；润色一句不需要读完两层画像。本包不含任何画像。用 `style-profiler <你的论文目录>` 提炼领域画像，用 `style-profiler <目录> author` 提炼你自己的作者画像，再在 `active_profile.yml` 指定路径。没有画像时技能用内置的段落模式，照常可用。

论文状态一般在正文目录的 `manuscript_state.md`。先查已有记录及绑定，必要时向上查两级；不要重复创建。普通粘贴文字修改无需项目状态。记录包含 claim 来源、授权范围、文件路径、段落进度和未解决问题。当前正文比过时状态摘要优先。

## 检查范围与返回码

- prose_gate：BAN 默认返回 1；AUDIT、句长等统计供复核。novel 改为 AUDIT，需要真实依据，不能靠换同义词避开事实问题。
- term_check：默认只报告；`--fail-on-findings` 可使明确登记的残留变体返回 1。`--fix` 预览，`--fix --write` 修改并备份；单独 `--write` 报错。
- check_bib：缺引用键、占位符、书目错误和在线元数据错配会返回 1。网络未解决单独报告，`--require-online` 才要求所有条目完成脚本支持的在线核验；无 DOI 的权威记录需要另外核对。
- check_parity：检查源文件和两端适配是否一致；`--installed` 额外检查当前用户入口。静态通过不代表论文事实正确。

只修改一段时主要查本段与邻接关系；全局术语修改、节整合或投稿审计才扩大到相关全文。已经通过且未变化的检查不反复运行。保留仿真性质、测试条件、负面结果和必要不确定性。

```bash
python -B scripts/profile_status.py --manuscript /你的项目/main.tex --state /你的项目/manuscript_state.md
python -B scripts/prose_gate.py /你的项目/draft.tex --json
python -B scripts/term_check.py /你的项目/draft.tex --registry /你的项目/manuscript_state.md --discover
python -B scripts/check_bib.py --bib /你的项目/references.bib --tex /你的项目/draft.tex --json
```

PDF/DOCX 应先提取文本。PDF 提取器没有 OCR，双栏顺序和表格可能受损；DOCX 提取只读普通段落。引用依赖具体表格或图时，要查看原文位置。

## 升级与回退

已安装技能通常是指向工具源目录的链接，更新源目录会更新两端可读取的版本；旧会话已加载的内容不会自动重载。复制安装需要重新同步。修改前应保存源文件、链接清单和哈希；还原时只回退该次改动，避免覆盖升级后新写的论文或资料。

当前版本将规则组织为：共享原则 → 技能入口 → 条件参考文档 → 角色适配。具体测试和本机备份位置见这次升级的交付报告。
