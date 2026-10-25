# 商店上架物料包

> 用途：把 `create-all-cg-save` 推到国内外技能商店时，需要手填的字段都已写好，直接复制即可。
> 更新日期：2026-10-26 · 对应版本：**v1.2.0**（技能路径已改为 `skills/create-all-cg-save/`）

---

## 0. 本轮实际提交（有回执才算数）

| 渠道 | 结果 | 回执 |
|---|---|---|
| GitHub | ✅ 已推送 v1.2.0 + topics + description | `5682bba` / tag `v1.2.0` |
| **skillstore.io** | ✅ 排队中（机器人已开 PR） | submission `307dc4ca-…` → PR [aiskillstore/marketplace#3934](https://github.com/aiskillstore/marketplace/pull/3934) |
| **skillbay.sh** | ✅ 已提交待人工审 | id `jkgw4ddbuid5f16x`，status `new` |
| **skillsmd.dev** | ✅ 已提交 | id `44233d3a-32f6-44f9-817a-2efade2b45cf` |
| **buildwithclaude** | ✅ PR 已开 | [PR #561](https://github.com/davepoon/buildwithclaude/pull/561) |
| **Cindy SkillHub** | ⚠️ 私有版已上传，公开版被自己占名 | `create-all-cg-save` v1.0.2（private），需先删旧记录 |
| skills.sh / SkillsMP / claude-plugins.dev | 🟡 自动索引，布局已修好 | 等爬虫 + 需要安装量 / ≥2 stars |
| 其余登录型 / 托管型 | ⏸ 物料已备，等账号 | 见第 2 节 |

## 1. 关键 URL（别填错）

⚠️ 本机 git remote 被 `insteadof` 改写成 ghfast 镜像，提交商店时**必须换成原始地址**：

| 用途 | URL |
|---|---|
| 仓库首页 | `https://github.com/xixi048/create-all-cg-save` |
| **技能目录（推荐填这个）** | `https://github.com/xixi048/create-all-cg-save/tree/main/skills/create-all-cg-save` |

v1.2.0 之前技能在仓库根的 `create-all-cg-save/`，**旧地址已失效**；
爬取型目录站只认 `skills/<name>/SKILL.md`，这次迁移就是为了被它们收录。

## 2. 定价：能收费的渠道一律标价

用户口径：**所有支持付费的渠道都设置付费**。

| 渠道 | 定价 | 到手 | 门槛 |
|---|---|---|---|
| **skillbay.sh** | **$5**（≈¥35） | 100%（平台 0 抽成） | 邀请制 + Stripe |
| **扣子 Coze** | ¥0.5/次 起 或 ¥9.9/月 | 约 70% | 需入驻商户 |
| 阿里云百炼 | 建议 ¥9.9 | 未公开 | 阿里云账号 |
| GPT Store / Windows Agent Store | $4.99 | 85% | 需相应开发者账号 |
| skillstore.io / skillsmd.dev / Cindy / BuildWithClaude | 免费 | — | 这些渠道**本身不支持收费** |

> 低于 $3 会被当成"自用玩具"，所以基线定 **$5**。
> 免费渠道保留引流版；付费渠道未来挂 Pro 适配器包（Ren'Py / Kirikiri / Unity）**$6.9**。

**为什么现在还不能全量挂价**：定价发生在「卖家账号 / 商户」层，不在提交层。
skillstore / skillsmd 的匿名接口根本设不了价；skillbay 的 `price` 字段在
`POST /api/v1/sellers/{org}/listings` 上，必须有 seller 账号 + Stripe onboarding。
所以流程是：**先用匿名接口抢免费曝光位，付费 listing 字段备好等账号。**

## 3. 各渠道状态与下一步

| 渠道 | 形态 | 状态 | 下一步 |
|---|---|---|---|
| GitHub | 仓库本身 | ✅ | 维持 topics / README / release |
| skills.sh | 自动索引 | 🟡 布局已修 | 让 `npx skills add xixi048/create-all-cg-save` 产生安装量 |
| SkillsMP | 自动索引 | 🟡 需 ≥2 stars | 先攒 star |
| claude-plugins.dev | 自动索引 | 🟡 | 已有 `.claude-plugin/marketplace.json` |
| skillstore.io | 公开 API | ✅ 排队 | 等审核；**改版后 1 小时内不能重复提交（409）** |
| skillbay.sh | 公开 API | ✅ `new` | 等邀请 → 建 seller listing，`price: 5` |
| skillsmd.dev | 公开 API | ✅ | 等索引 |
| buildwithclaude | GitHub PR | ✅ PR #561 | 等维护者 review |
| Cindy SkillHub | 宿主工具 | ⚠️ | **删掉私有版 `create-all-cg-save` 后重新以 public 创建** |
| Cow Skill Hub | 登录 + zip | ⏸ | 用 `dist/create-all-cg-save-v1.2.0-skillroot.zip` |
| agentskill.sh | SPA 表单 | ⏸ | 需人工贴 URL |
| ClawHub | `clawhub login` + publish | ⏸ | 需登录 |
| Tank | `tank login` + publish | ⏸ | 需登录 |
| 腾讯 SkillHub / 字节 Find Skill / 智谱 AgentMore | 平台侧 | ⏸ | 平台账号 |
| 扣子 Coze | **需移植** | ⏸ | 平台读不到用户磁盘，得做成服务形态 |

## 4. skillstore.io 提交字段（已提交，留档）

**GitHub Repository URL**
```
https://github.com/xixi048/create-all-cg-save
```

**Additional context**
```
create-all-cg-save — byte-level "all CG" save unlocker for offline single-player games.

Repository restructured in v1.2.0: the skill now lives at skills/create-all-cg-save/SKILL.md
(was create-all-cg-save/SKILL.md at the repo root), and .claude-plugin/marketplace.json
makes the repo installable as a Claude Code plugin marketplace.

WHAT IT IS
Two routes: a fast path that parses known save formats (ships with a from-scratch
zero-dependency Ruby Marshal parser for RPG Maker XP/VX/VX Ace, which needs split-stream
handling because those saves are two concatenated Marshal streams), and a generic byte-diff
path for unknown or encrypted saves (before/after diff -> fit start+stride array -> extrapolate).

SECURITY NOTES
- Python 3.8+ standard library only; zero third-party dependencies.
- NO network access anywhere: no urllib / requests / socket calls. Fully offline.
- NO eval / exec / subprocess / os.system / dynamic import.
- All writes are user-directed and absolute-path-gated.
- Every write is preceded by an automatic timestamped backup, applied via atomic
  os.replace, and reversible with one rollback command that re-verifies sha256 first.
- --dry-run is available on every write path. Length-changing patches are refused by default.
- Scope guard: refuses online / multiplayer / leaderboard games and DRM circumvention.
  See references/safety.md.

Verified against a real RPG Maker VX Ace title: 59 switch slots flipped ON, re-parsed to
confirm, then rolled back to the exact original state.
```

## 5. skillbay.sh listing（等邀请后照着填）

**Title** `create-all-cg-save`
**Category** `coding & dev tools`
**Price** `5`（整数美元）
**Summary**（≤140）
```
Produce an all-CG save for offline single-player games: locate, parse, diff and byte-patch
unlock flags, with automatic backup and one-command rollback.
```
**Examples**（必填，1–5 条，`{prompt, without, with}`）
```json
[
  {
    "prompt": "I have a save from an RPG Maker game at D:\\games\\Save02.rvdata2. Unlock every CG but don't do anything I can't undo.",
    "without": "I can't safely modify a binary save file, and I can't tell which bytes control CG unlocks. You could replay the game, or look for a save editor for this title. Hex editing risks corrupting the save.",
    "with": "Engine: RPG Maker VX Ace (RGSS3), two concatenated Marshal streams parsed clean. 59 switch slots found. Plan built (59 equal-length patches) -> dry-run OK -> backup Save02.rvdata2.allcg-bak-<ts> -> applied atomically, size unchanged 617987 -> 617987 -> re-parsed: 59/59 ON. Rollback verified byte-for-byte."
  }
]
```

## 6. 中文渠道文案（Cow Skill Hub / 腾讯 SkillHub / 扣子）

**技能名称** `create-all-cg-save`
**显示名称** `创建一个全 CG 存档`
**分类** `游戏 / 工具`
**一句话简介**
```
给本地单机游戏做「全 CG 存档」：自动定位存档、识别引擎、字节差分找到解锁位，带备份写入并可一键回滚。
```
**详细描述**
```
支持两条通道：
1. 引擎快速通道 — 自带零依赖 Ruby Marshal 解析器，RPG Maker XP / VX / VX Ace 全自动
   （VX Ace 的存档是两段 Marshal 流拼接，通用解析器会读错位，这里专门处理了）；
2. 通用差分通道 — 格式未知或加密时，用「解锁前/解锁后」两份存档做字节差分反推解锁位，
   并可推断式外扩到全部 CG。

安全设计：零第三方依赖、完全离线、写入前自动备份、原子写、一键回滚（回滚前二次校验 sha256）、
每次写入都支持 --dry-run。

红线：只做离线单机游戏中你自己合法拥有的副本；不涉及联机、排行榜、反作弊、DRM 绕过。
```

## 7. 只剩三件「必须用户本人做」的事

1. **Cindy SkillHub**：删掉私有版 `create-all-cg-save`（Skills 页），我才能用 public 重新创建
2. **skillbay.sh**：收到邀请后建 seller 账号 + Stripe，然后把第 5 节字段粘进 listing（`price: 5`）
3. **登录型渠道**（ClawHub / Tank / Cow Skill Hub / agentskill.sh）：各自登录一次即可发；zip 已备好

其余全部已自动化完成或已排进自动索引。
