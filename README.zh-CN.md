# 创建一个全 CG 存档 · create-all-cg-save

[English](README.md) | 简体中文

一个 agent skill（附带一套零依赖 Python 工具）：为**本地单机游戏**的存档产出「全 CG 版本」。

它不下载游戏、不碰 CG 图片、不改游戏本体 —— 只做一件事：**在你自己的存档上，
精确定位承载 CG 解锁状态的字节，做最小代价的修改，并且随时可以回滚。**

## 它能做什么

- 在本机常见位置扫出某款游戏的候选存档
- 识别游戏引擎（RPG Maker / Ren'Py / Kirikiri / Unity / Siglus / BGI 等）
- 对可解析的存档格式（如 RPG Maker 的 Ruby Marshal）**直接算出每个解锁位的精确字节偏移**
- 对看不懂的私有二进制，用「解锁前 / 解锁后两份存档做差分」反推解锁位，
  再推断出 CG 标志阵列结构，一次性解锁全部
- 生成可读的解锁计划 JSON，支持预演、校验、一键回滚

## 两条技术路线

| 路线 | 适用 | 手段 |
|---|---|---|
| 引擎快速通道 | 存档格式已知且可解析 | 语义解析，直接定位到 `switch[N]` / `variable[N]` |
| 通用差分通道 | 私有二进制、看不懂结构 | 字节差分 → 拟合 `start + stride` 阵列 → 外扩解锁 |

决策树见 [`skills/create-all-cg-save/SKILL.md`](skills/create-all-cg-save/SKILL.md)。

## 快速开始

```bash
# 1. 找存档
python skills/create-all-cg-save/scripts/save_scout.py --game <游戏名>

# 2. RPG Maker VX/VX Ace/XP：直接看结构与当前开关状态
python skills/create-all-cg-save/scripts/engines/rgss_save.py inspect "Save01.rvdata2"

# 3. 生成解锁计划（把指定开关置 ON）
python skills/create-all-cg-save/scripts/engines/rgss_save.py plan-switches \
    "Save01.rvdata2" --ids 1,3,5-40 --out plan.json

# 4. 预演 → 写入 → 校验（写入会自动备份）
python skills/create-all-cg-save/scripts/apply_plan.py plan.json --dry-run
python skills/create-all-cg-save/scripts/apply_plan.py plan.json
python skills/create-all-cg-save/scripts/apply_plan.py plan.json verify

# 出问题就回滚
python skills/create-all-cg-save/scripts/apply_plan.py plan.json rollback
```

未知引擎走差分：

```bash
python skills/create-all-cg-save/scripts/save_diff.py A.save B.save --json ab.diff.json
python skills/create-all-cg-save/scripts/infer_plan.py ab.diff.json \
    --target A.save --stride 4 --count 128 --out unlock-plan.json
```

> `--stride` / `--start` 很关键：只观测到一两个解锁位点时，拟合步长必然歧义
> （步长 4 的阵列只解锁了第 0、5 项时，GCD 会给出 20）。脚本会明确告警，
> 能钉死阵列结构时就直接钉死。

## 已验证过的目标

**RPG Maker VX Ace（RGSS3）** —— 例如 `Save0X.rvdata2`：

- Ruby Marshal 存档，文件里是**两段 Marshal 流首尾相接**
  （第 1 段 `make_save_header`，第 2 段 `make_save_contents` 的 11 项 Hash）
- `:switches` 的 `@data` 是布尔数组，`'T'`/`'F'` 各 1 字节，**等长替换，文件长度一字不变**
- 实战结果：59 个开关槽位一次性置 ON，文件大小 617987 → 617987，重新解析为真 ON，回滚后逐字节一致

## 目录结构

```
create-all-cg-save/                    # 仓库
├── .claude-plugin/
│   └── marketplace.json              插件市场清单（/plugin marketplace add）
└── skills/
    └── create-all-cg-save/           技能本体（skills.sh 等目录站按此路径自动索引）
        ├── SKILL.md                  技能主入口（给 AI 读的工作流）
        ├── scripts/
        │   ├── save_scout.py         定位候选存档 + 引擎识别
        │   ├── save_diff.py          字节差分
        │   ├── infer_plan.py         推断解锁阵列 → 解锁计划
        │   ├── apply_plan.py         应用 / 校验 / 回滚
        │   ├── common.py             备份、原子写、哈希
        │   └── engines/
        │       ├── ruby_marshal.py   零依赖 Ruby Marshal 解析器 + 编码器
        │       └── rgss_save.py      RPG Maker RGSS 存档适配器
        └── references/
            ├── engines.md            各引擎存档位置与格式速查
            ├── diff-method.md        差分法完整手册
            ├── unlock-plan-schema.md JSON 结构定义
            └── safety.md             安全与合规红线
```

## 安装

不克隆也能装（直接读公开仓库）：

```bash
npx skills add xixi048/create-all-cg-save           # skills.sh / npx skills
```

```text
/plugin marketplace add xixi048/create-all-cg-save  # Claude Code 插件市场
```

或者把 `skills/create-all-cg-save/` 整个目录放进 agent 的技能目录即可：

- 用户级：`~/.workbuddy/skills/create-all-cg-save/`
- 项目级：`<仓库>/.workbuddy/skills/create-all-cg-save/`

目录名必须与 `SKILL.md` frontmatter 里的 `name`（`create-all-cg-save`）一致。

> 为什么多一层 `skills/`？GitHub 爬取型目录站（skills.sh、SkillsMP、`npx skills`、
> Claude Code 插件市场）只认 `skills/<name>/SKILL.md`。技能文件夹放在仓库根目录，
> 永远不会被发现——再好的技能也一样。

> `SKILL.md` 里的相对路径都相对**技能目录**，不是当前工作目录。执行前先 `cd` 进去，
> 或直接拼成绝对路径。

## 环境要求

Python 3.8+，**零第三方依赖**（全部使用标准库）。

Windows 控制台若中文乱码，先 `chcp 65001` 或设 `PYTHONIOENCODING=utf-8`。

## 安全模型

- 任何写入前先备份 `<存档名>.allcg-bak-<时间戳>`，不做原地覆盖
- 写入前校验 `sha256_before`，计划与目标存档不匹配直接拒绝
- 会改变文件长度的补丁默认拒绝，需显式 `--allow-resize`
- 先 `--dry-run` 预演，写入后必须进游戏确认

完整清单见 [`references/safety.md`](skills/create-all-cg-save/references/safety.md)。

## 已知限制

- RPG Maker XP / VX / VX Ace 已完整自动化；MV / MZ 在明文 JSON 时同样简单
- Ren'Py / Kirikiri / Unity / Siglus / BGI 等通常只能走差分法，整份加密或压缩的存档差分也会失效
- 云存档必须先同步到本地
- 开关全开可能连带触发剧情分支或 Game Over 条件，建议先在游戏里验证再批量写入

## 免责声明

本工具仅用于用户对自己合法拥有的**离线单机游戏**存档做个人研究与修改。
请勿用于联网 / 多人游戏、在线排行榜或其他可能影响他人的场景。
使用者需自行承担修改存档带来的任何后果 —— 好在每次写入都会自动备份。

## 开源

MIT License，见 [LICENSE](LICENSE)。
