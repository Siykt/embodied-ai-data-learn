# Task 4 实施报告：模型条件化数据引擎专题

## 交付范围

本任务新增模型条件化数据引擎专题文档，并创建 brief 指定的两张 SVG 图示。内容围绕具身 AI 数据的采集、处理、对齐、质量控制、评估隔离、数据血缘和部署反馈展开；未修改共享导航、`terms.md`，未加入 Axis-specific case content。

## 文件变更

- `src/content/docs/guides/model-conditioned-data-engine.md`
  - 新增页面 frontmatter，生成 `/guides/model-conditioned-data-engine/`。
  - 说明策略评估日志、失败聚类、任务参数搜索、候选任务队列和仿真/人类采集的关系。
  - 使用成功率以外的失败价值、不确定性、分布漂移、物理违规、覆盖缺口和采集成本构建可解释的采样优先级。
  - 定义程序化任务、评估、质量和部署反馈四类标准化输入，以及任务实例和 episode 的版本、来源、授权、split、时间和空间对齐字段。
  - 描述任务生成、采集、验证、训练与评估、部署、反馈六阶段飞轮。
  - 覆盖版本化、数据血缘、分布监控、重加权、训练/评测隔离、重放验证和停止规则。
  - 引用 DAgGER、VLA 评估、程序化任务生成、仿真器、Open X-Embodiment 和 SIMPLER 资料。
- `public/images/docs/model-conditioned-task-selection.svg`
  - 展示策略评估日志 → 失败聚类 → 任务参数搜索 → 候选任务队列 → 仿真/人类采集 → 验证与入库。
- `public/images/docs/embodied-data-engine-flywheel.svg`
  - 展示任务生成、数据采集、验证、训练与评估、部署、反馈六阶段及版本/血缘要求。

页面仅使用上述两张指定 SVG，并在图示附近提供中文 alt 文本。

## 自审结果

- 文档风格与现有 VLA、仿真、程序化任务生成和 Human-gated DAgger 专题保持一致。
- 明确区分任务成功状态与数据质量状态，保留失败数据的分析和恢复训练价值。
- 明确区分原始观测、派生标签、策略动作、人类动作和安全控制器动作的来源。
- 明确记录观测、动作计划、动作生效的时间语义，以及世界、基座、末端、相机和物体坐标系。
- 明确要求评估集冻结、任务/场景/资产/机器人/操作者/时间隔离和新增数据的触发血缘。
- 检查页面无 `TODO`、`TBD` 或 Axis-specific 内容；未改 `astro.config.mjs` 与 `src/content/docs/reference/terms.md`。
- 两个 SVG 均通过 XML 语法检查。

## 验证

运行：

```bash
pnpm build
git diff --check
```

结果：

- `pnpm build` 成功，Astro 生成 `/guides/model-conditioned-data-engine/index.html`。
- Astro 共构建 20 个页面，Pagefind 搜索索引成功生成。
- `git diff --check` 通过，无空白错误。
- 构建输出提示 sitemap 因项目未设置 `site` 而跳过；这是既有配置提示，不影响本任务页面构建。

## 提交

提交 subject：`docs: 新增模型条件化数据引擎专题`

## Round 1 修复记录（2026-08-26）

### 精确改动

- 使用 `git rm --cached -- .superpowers/sdd/2026-08-26-axis-robotics-data-engine-docs/task-4-report.md` 仅从索引移除报告；报告文件仍保留在本地工作区，供评审和台账使用，最终提交树不再包含该文件。
- 将反馈阶段改为可追加、可修订的“开发反馈日志”（post-evaluation/development feedback log），保留修订审计；明确官方评估集和正式结果日志不可变，且从不作为自适应采样、任务搜索或训练输入。
- 在采样优先级后新增可复现权重转换：`u(v)=exp(priority(v)/temperature)`；同一轮同一目标切片内归一化至均值 1；裁剪 `[0.25, 4.0]`，最小权重 `0.25`；固定示例配置为 `temperature=1.0`、`normalization_scope=round × target_slice`、`min_weight=0.25`，并保存配置、候选集合哈希和归一化分母。
- 修正 `model-conditioned-task-selection.svg`：候选任务队列只流向仿真采集或人类采集；两类采集输出再流向验证与入库，移除队列直达验证的路径。
- 将停止规则改为可执行协议：每个目标切片每轮至少 `n=500` 个有效 episode；固定 holdout 双侧 95% bootstrap 区间，改善至少 `+1.0` 个百分点且区间下界大于 `0` 才算改善；连续 `3` 个完成轮次无改善即停止，并指定数据引擎负责人执行、评估负责人复核，安全/合规触发时由质量负责人共同签字。

### 本轮命令与原始输出

命令：

```text
git rm --cached -- .superpowers/sdd/2026-08-26-axis-robotics-data-engine-docs/task-4-report.md
```

输出：

```text
rm '.superpowers/sdd/2026-08-26-axis-robotics-data-engine-docs/task-4-report.md'
```

命令：

```text
test -f .superpowers/sdd/2026-08-26-axis-robotics-data-engine-docs/task-4-report.md
git diff --check
for svg in public/images/docs/model-conditioned-task-selection.svg public/images/docs/embodied-data-engine-flywheel.svg; do xmllint --noout "$svg"; done
```

输出：无输出，退出码 `0`。

命令：`pnpm build`

输出：

```text
$ astro build
12:20:22 [content] Syncing content
12:20:22 [content] Synced content
12:20:22 [types] Generated 359ms
12:20:22 [build] output: "static"
12:20:22 [build] mode: "static"
12:20:22 [build] directory: /Users/admin/Documents/work/embodied-ai-data-learn/dist/
12:20:22 [build] Collecting build info...
12:20:22 [build] ✓ Completed in 474ms.
12:20:22 [build] Building static entrypoints...
12:20:23 [vite] ✓ built in 380ms
12:20:23 [vite] ✓ built in 49ms
12:20:23 [build] Rearranging server assets...

 generating static routes 
12:20:23   ├─ /404.htmlEntry docs → 404 was not found.
 (+11ms) 
12:20:23   ├─ /guides/aria-ego4d-egoexo4d-formats/index.html (+4ms) 
12:20:23   ├─ /guides/browser-teleoperation-crowdsourced-data/index.html (+2ms) 
12:20:23   ├─ /guides/camera-intrinsics-data-requirements/index.html (+2ms) 
12:20:23   ├─ /guides/ego-world-operation-umi-video/index.html (+2ms) 
12:20:23   ├─ /guides/episode-trajectory-design/index.html (+9ms) 
12:20:23   ├─ /guides/human-gated-dagger-correction-data/index.html (+3ms) 
12:20:23   ├─ /guides/isaac-lab-embodied-data/index.html (+2ms) 
12:20:23   ├─ /guides/meta-vrs-data-standard/index.html (+2ms) 
12:20:23   ├─ /guides/mobile-imu-data-collection/index.html (+2ms) 
12:20:23   ├─ /guides/model-conditioned-data-engine/index.html (+2ms) 
12:20:23   ├─ /guides/mujoco-embodied-data/index.html (+2ms) 
12:20:23   ├─ /guides/procedural-task-generation-embodied-data/index.html (+1ms) 
12:20:23   ├─ /guides/simulators-embodied-data/index.html (+1ms) 
12:20:23   ├─ /guides/turn-for-embodied-data/index.html (+2ms) 
12:20:23   ├─ /guides/visual-inertial-slam/index.html (+1ms) 
12:20:23   ├─ /guides/vla-models-and-evaluation/index.html (+1ms) 
12:20:23   ├─ /guides/yuv-algorithms-android/index.html (+1ms) 
12:20:23   ├─ /index.html (+3ms) 
12:20:23   ├─ /reference/terms/index.html (+2ms) 
12:20:23 ✓ Completed in 86ms.

12:20:23 [build] ✓ Completed in 536ms.
12:20:23 [starlight:pagefind] Building search index with Pagefind...
12:20:23 [starlight:pagefind] Found 20 HTML files.
12:20:23 [starlight:pagefind] Finished building search index in 103ms.
12:20:23 [WARN] [@astrojs/sitemap] The Sitemap integration requires the `site` astro.config option. Skipping.
12:20:23 [build] 20 page(s) built in 1.13s
12:20:23 [build] Complete!
```

构建中的 sitemap `site` 配置提示为既有提示，不影响本任务页面构建。

## Round 2 修复

### 根因

原图使用 `M485 487h480` 作为仿真采集输出线。该路径从仿真节点右侧直接横穿人类采集节点，造成线条遮挡节点，并使输出关系产生歧义。

### 修复

仅修改 `public/images/docs/model-conditioned-task-selection.svg`：

- 仿真采集输出改为 `M485 487v98h445v-45h35`，从人类采集节点下方绕行后进入验证与入库节点。
- 人类采集输出保持独立的 `M860 487h105`，从人类采集节点右侧直接进入验证与入库节点。
- 保留候选任务队列分别指向仿真采集和人类采集的路径，以及两类采集分别进入验证与入库的输出关系。
- 修改后的路径不穿过或遮挡任何节点。

### Round 2 验证证据

执行目录：`/Users/admin/Documents/work/embodied-ai-data-learn`

```text
$ xmllint --noout public/images/docs/model-conditioned-task-selection.svg
xmllint --noout exit=0
$ git diff --check
git diff --check exit=0
```
