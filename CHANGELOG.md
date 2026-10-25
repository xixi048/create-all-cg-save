# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [1.3.0] - 2026-10-26

### Added

- **MCP server**（`mcp/server.py`，stdio / JSON-RPC 2.0 / 零依赖）：把整套工具暴露给任意 MCP 客户端
  - `save_scout` · `engine_inspect` · `plan_unlock_switches` · `diff_saves` · `infer_unlock_plan` · `apply_plan`
  - `apply_plan` 用 `action` 区分 dry_run / apply / verify / rollback，写入仍然先自动备份
- **自建发现端点**：`docs/.well-known/agent-skills/index.json`，经 GitHub Pages 发布
  （附空的 `docs/.nojekyll` —— Jekyll 默认跳过点目录，不加会 404）

## [1.2.0] - 2026-10-26

### Changed

- **仓库结构改为标准技能布局**：技能本体从仓库根目录的 `create-all-cg-save/`
  移到 `skills/create-all-cg-save/`
  - 原因：GitHub 爬取型目录站（skills.sh / SkillsMP / `npx skills` / Claude Code 插件市场）
    只索引 `skills/<name>/SKILL.md`。技能放在仓库根目录，**永远不会被自动发现**
  - 迁移后 `npx skills add xixi048/create-all-cg-save` 与
    `/plugin marketplace add xixi048/create-all-cg-save` 均可直接使用

### Added

- `.claude-plugin/marketplace.json`：本仓库自身即为一个 Claude Code 插件市场
- README 增加「一行命令安装」段落与布局说明

### Fixed

- README / README.zh-CN / STORE-LISTING 中所有指向旧路径的链接

## [1.1.0] - 2026-10-26

### Added

- **RGSS 快速通道**（`scripts/engines/rgss_save.py`）
  - `inspect`：解析存档结构并列出所有开关 / 变量的当前值
  - `plan-switches`：按 ID 范围或 `--all` 生成解锁计划（JSON）
  - RPG Maker XP / VX / VX Ace 全自动；MV / MZ 明文 JSON 存档可直接套用
- **零依赖 Ruby Marshal 解析器 / 编码器**（`scripts/engines/ruby_marshal.py`）
  - 支持 String / Symbol / Array / Hash / Object / ivar / link / userdef / usrmarshal / bignum / float 等全部常见类型
  - 整数、布尔双向编解码，`_selftest()` 往返自校验
  - `--streams`：正确处理「多个 Marshal 流首尾相接」的 VX Ace 存档
- **通用差分通道**
  - `save_diff.py`：两份存档做字节差分，输出结构化 diff JSON
  - `infer_plan.py`：从差分拟合 `start + stride` 位阵列，并推断式外扩到未触发槽位
- **`apply_plan.py` 安全写入层**
  - 自动备份 `<存档>.allcg-bak-<时间戳>`，回滚前二次校验备份 sha256
  - 原子写（临时文件 + `os.replace`），plan 内嵌 sha256 锚点防止打错文件
  - `--dry-run` / `verify` / `rollback` 三个子命令构成闭环
- **`save_scout.py` 存档定位**：扫描常见存档位置并按扩展名权重排序

### Changed

- `save_scout.py` 改为优先扫描用户指定的游戏安装目录，避免 AppData 遍历耗尽文件预算
- `save_scout.py` 将 `.rvdata2` / `.rpgsave` 等存档专用扩展名单独加权，避免与普通 `.dat` 混排

### Verified

- RPG Maker VX Ace 实战样本：59 个开关槽位全置 ON → 重新解析确认 → `rollback` 精确回到原始 `[1, 5, 12]`
- 补丁为**等长替换**（布尔位 1 字节 → 1 字节），写入后文件长度一字未变（617987 → 617987）

## [1.0.0] - 2026-10-26

### Added

- 初始版本：Skill 骨架、SKILL.md 主流程、四份参考文档、MIT 许可
