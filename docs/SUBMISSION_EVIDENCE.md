# ClaimTrace：提交证据、事实口径与下一步

更新日期：2026-10-01。用户已确认最终提交语言为英语；提交说明要求录制视频，但没有额外规定视频时长或格式；准备日期按 10 月 4 日，不推断具体截止时刻。Rubric 2 未找到，不据此承诺分数。

本次更新：当前本地仓库限定运行 `tests/` 得到 43 passed、0 failed、0 skipped；30 个项目 Python 文件语法解析通过，所有 app/src/evaluation/tests 模块均有文件级 docstring。英文权衡报告的 Word 版包含标题、表格和参考文献的保守正则计数为 1,339 words，Markdown 版为 1,284 words，均在老师给出的 1,200 words ±10–15% 范围内；DOCX 已渲染并逐页检查。两条成功的独立开发请求记录仍是小样本。没有重跑正式评估或修改锁定集、人工标签、历史评估结果。

## 1. 课程要求—证据—状态—缺口—下一步

老师最终要求截图在上述交付物之外补充了：对结果的批判性反思、结构化报告；数据和评估文件需有解释；代码需有运行说明及文件／模块级文档；仓库需附产品说明（persona、输入／输出、架构图、目标与实际指标）；演示须同时显示作者面部与相关屏幕，约 5±3 分钟，超过 8 分钟只看前 8 分钟。`PE6201_Project_Proposal_Watchouts.pdf` 给出问题 15%、权衡 25%、实现 35%、演示 25% 四个方向，但不等于完整 Rubric 2 的等级描述，不据此估分。课程内容用于解释技术与商业取舍，不根据老师邮件的编号猜测概念。

| 要求或反馈 | 仓库／提供材料中的证据 | 当前状态 | 缺口 | 下一步 |
| --- | --- | --- | --- | --- |
| 问题与用户 | 已提交的原始选题 Word；[中文审校稿](SUBMISSION_REVIEW_ZH.md) 第 1 节 | 原报告已提交；当前定位已说明 | 用户画像未经真实访谈验证，痛点未量化 | 作者补充真实样本数、收集方式、耗时和频率；没有记录就披露 |
| ≤1,200 words 权衡分析与结果批判 | [英文 Markdown](BUSINESS_TECHNICAL_TRADEOFF_EN.md)、[Word](BUSINESS_TECHNICAL_TRADEOFF_EN.docx)、保存结果 | 英文稿含结果批判、困难、未达目标、技术取舍与后续路径；DOCX 保守计数 1,339 words，Markdown 1,284 words | 最终仍需作者确认第一人称经验表述准确；字数按含表格、标题与参考文献的宽口径计算 | Word 页面排版已逐页检查；不得用高风险专项 83.3% 替代合并口径 68% |
| 中文检索可行性，优先处理 | [retrieval.py](../src/retrieval.py)；[10 条开发集核验](../evaluation/retrieval_audit_10.csv)；[dev_retrieval.csv](../results/dev_retrieval.csv) | 多语言模型已实现；10 条人工核验已记录 | 只选了开发集的少量案例改写，不是总体检索测试 | 保留限定范围；不使用锁定集调参，不重跑模型 |
| Precision 与 Recall 并列，基线同样本 | 锁定集、test_baseline.csv、test_full.csv、test_metrics.csv | 保存结果已核算验证 | 原目标合并召回未达标，不能混用两个正类定义 | 报告两种口径及正例数，不宣称目标已达成 |
| 质量、引用与人工核验 | manual_review_20.xlsx、manual_review_summary.csv | 20 条复核可验证；引用支持率有汇总 | 建议可执行性没有历史字段；未证实新真实案例泛化 | 保留 not_applicable 和有限分母；不要回填历史字段 |
| 端到端实现与运行代码 | app.py、src/、tests/；隔离复现报告；当前截图 | 当前工作版本可启动；本轮 43 项离线测试通过；另有两次真实 API 请求记录 | GitHub 最新版本与可访问性未验证；自动测试不等于正式模型评估 | 提交前单独检查远程；提交／推送须再次授权 |
| 数据与评估解释 | [data/README.md](../data/README.md)、[evaluation/README.md](../evaluation/README.md)、保存数据和结果 | 已新增英文数据目录说明、标签／holdout 边界、评估文件清单和脚本副作用说明 | 源案例转载授权与链接持续可用仍未验证；合成数据没有完整可复现生成记录 | 保留许可限制；提交前确认所需资产是否可公开分享 |
| 代码可读性与运行说明 | [README English quick start](../README.md)、src/ 与 evaluation/ module docstrings | 已补充运行、安全测试指令和模块说明；对 span／citation 字段加离线 grounding guard；43 项离线测试通过 | 测试不证明真实模型推理或新指标，UI 未在本轮以非空输入实测 | 不重跑正式评估或改业务标签；后续提交前检查远程版本 |
| 产品文档与架构 | [Product documentation](PRODUCT_DOCUMENTATION_EN.md) | persona、输入／输出、Mermaid 高层架构及目标／实际指标已整理 | 小型卖家子群体未经访谈验证；结果仍是历史评估，新增 guard 未用于重算 | 将其随代码仓库提交；不把设计 persona 写成研究发现 |
| 商业与技术取舍 | 中文稿技术选择、质量／成本／风险章节 | 实现取舍已写明 | 没有竞品实测、真实收益与用户成本记录 | 只写有证据的取舍，不补造商业数字 |
| 实际成本和运行时间 | `src/usage_logging.py`、`src/llm_client.py`、`logs/request_metrics.jsonl` | 两条独立开发集请求有成功 usage／服务返回费用／请求阶段耗时记录 | 正式 30 条评估成本、稳定延迟分布与页面端到端响应仍未测量 | 报告两个请求的样本事实及边界；不外推长期成本或延迟 |
| 演示视频 | [English recording script](DEMO_SCRIPT_EN.md)、当前截图与隔离回放工具 | 英文 5–7 分钟工作脚本已准备；回放与替身状态已验证 | 视频尚未录制；老师要求作者面部与相关屏幕同时可见，并清楚、有条理、简洁 | 作者按脚本录制，控制在 2–8 分钟，检查可播放、声音和面屏同框；脚本不是视频交付件 |
| GitHub、秘密与许可 | 当前 Git 状态、.gitignore、公开资产复制清单、data/sources.csv | 当前工作版本已隔离；.env 当前不跟踪且被忽略 | 最新文档尚未上传；完整历史秘密审计、转载和代码许可未验证 | 未获批准不提交；不复制秘密；许可未确认不擅自选择 |
| 完整评分和提交细则 | 提交截图、Watch-outs、老师反馈；Rubric 2 未找到；用户已确认英文提交 | 交付物、语言和视频无额外时长／格式要求已明确 | 缺少 Rubric 2 的等级描述 | 按已知交付物准备；不猜测等级或保证分数 |

原 Word 与课程 PDF 保持原样。Watch-outs 还强调问题、技术选择与验证、商业／技术权衡、面向不同受众解释；这不是要求必须使用 agent 或低代码工具。当前直线工作流不冒充 agent，人工复核不冒充独立 LLM judge。

## 2. 本次运行验证

隔离目录：`C:\Users\10231\Documents\Codex\2026-08-22\w-s-m\claimtrace-repro-20260929-audit01`。来源是包含未提交工作在内的文件快照，不是 GitHub 零克隆。复制清单 `COPY_MANIFEST.json` 记录 63 个公开文件；仅复制 .env.example，不复制 .env、.git、原 .venv、logs 或缓存。源 HEAD 为 `009fa9ea8cc171daa95238b83194b3fb31b8f09d`。

| 检查 | 实际结果 | 不能据此声称的事项 |
| --- | --- | --- |
| 离线 pytest（2026-09-29 隔离副本，仅 tests/） | 41 passed，0 failed，0 skipped，7.17s；网络拦截、HF 离线标志开启 | 真实模型、外部 API 或完整生产端到端通过 |
| 离线 pytest（2026-10-01 当前本地仓库，仅 tests/） | 本轮当前代码 43 passed，0 failed，0 skipped，8.59s；网络拦截与 HF 离线模式 | 不等于正式模型评估；不证明锁定集指标变化 |
| 首次不限定目录的 pytest（2026-10-01 当前本地仓库） | pytest 误收集 `evaluation/` 中会执行读／写操作的脚本，4 个 collection errors；结果文件因只读保护未被覆盖，随后限定为 `tests/` 后通过 | 不是 `tests/` 中的 4 项失败；必须限定测试目录，不能删保护或隐藏该现象 |
| Python 语法与模块说明 | app.py、src/、tests/、evaluation/ 共 30 个 .py 文件用 AST 解析通过；均有模块 docstring | AST 不执行模块，不等于功能测试 |
| 指标脚本 | 读取副本历史 CSV，59 行统计与保存的 test_metrics.csv 相同；输出只到新临时 CSV | 没有重新评估模型，没有覆盖正式结果 |
| Streamlit 当前工作版本 | 中文／英文空页面、切换保留输入、3 示例、清空、空输入反馈验证通过 | 没有在真实应用提交非空文案，没有下载嵌入模型 |
| 响应式 | 中文和英文分别检查 320、375、768、1440px；无横向溢出，主要按钮高度 44px | 不是所有设备或全部长结果的无障碍认证 |
| 键盘 | 3 个示例、清空、开始按钮可键盘访问，焦点轮廓可见；键盘触发清空与空输入提示成功 | 未做完整读屏器／WCAG 审计 |
| 加载和错误 | 独立替身页面出现加载提示、RuntimeError 后安全的人工复核提示；中英文错误界面已查看 | 替身等待 3 秒是演示时序，不是 API 延迟；不是历史模型失败 |
| 历史回放 | CLAIM031、CLAIM032、CLAIM084 已展示保存字段；有持续标识，语言切换保留所选样本 | 不是新模型推断，也不证明当前模型与历史生成条件相同 |
| 浏览器错误 | 三个本地页面采集的 console error 记录为空 | 不保证整个服务永远没有错误；预期的替身 RuntimeError 是测试内容 |
| 保护核查 | 复制清单中的 63 个原文件和副本文件 SHA-256 均保持相同 | 不能代替全仓库秘密审计或远程状态验证 |
| OpenRouter 真实请求（非锁定开发样本） | 两条成功日志：782/105/887 Token、US$0.0001803、3.044005 秒；809/173/982 Token、US$0.00022515、3.827186 秒；均为 `openai/gpt-4o-mini` | 小样本请求阶段数据，不代表正式 30 条评估成本或端到端延迟；日志未保存文案／claim_id，不能由日志独立回溯输入 |

环境：Python 3.12.14；pytest 9.1.1；Streamlit 1.64.0；pandas 3.0.6；Pydantic 2.13.5；sentence-transformers 6.1.0；scikit-learn 1.9.1；requests 2.34.2。依赖安装为前序已获授权的准备工作；本轮没有再次安装依赖。

可重复执行的离线命令（在隔离目录 PowerShell 运行）：

```powershell
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
& '.\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests
& '.\.venv\Scripts\python.exe' -B '.\.verification\verify_saved.py'
```

测试的网络保护由 `tests/conftest.py` 和替身实现提供。上表的 2026-10-01 结果来自当前本地仓库重建后的环境；命令只运行 `tests/`，没有运行正式评估。README 已同步最新测试与两条真实请求记录。

详细机器记录保留在隔离目录 `.verification/saved_verification_20260929.json`、`.verification/screenshots/browser_checks_20260929.json`，完整过程见 `REPRODUCTION_REPORT.md`。

## 3. 数字、分母与来源

核心来源：

- [冻结测试集](../evaluation/test_set_locked.csv)：30 条唯一 ID；高风险 12、需证据 13、低风险 5。
- [规则基线](../results/test_baseline.csv) 与 [ClaimTrace 保存结果](../results/test_full.csv)：同一 30 条 ID 与参考标签。
- [三类指标](../results/test_metrics.csv)、[分组汇总](../results/test_summary.csv)、[计算脚本](../evaluation/metrics_test.py)：历史统计与计算口径。
- [20 条人工复核](../evaluation/manual_review_20.xlsx) 与 [人工汇总](../results/manual_review_summary.csv)：保留原人工最终标签、备注、来源及结构化判断。

| 指标 | 规则基线 | ClaimTrace | 分母／定义 |
| --- | --- | --- | --- |
| 高风险 Precision | 3/3 = 100% | 10/17 = 58.8% | TP / (TP + FP)；预测高风险数为 3、17 |
| 高风险 Recall | 3/12 = 25% | 10/12 = 83.3% | TP / (TP + FN)；正例均为 12 |
| 高风险 F1 | 40.0% | 69.0% | Precision 与 Recall 的调和平均 |
| 合并 Precision | 8/8 = 100% | 17/17 = 100% | 预测为 high_risk 或 evidence_needed 的样本；不是拒答也算命中 |
| 合并 Recall | 8/25 = 32% | 17/25 = 68% | 参考标签为上述两类的 25 条；拒答计未检出 |
| 合并 F1 | 48.5% | 81.0% | 只读原始 CSV 后合并计算；不是三类 Macro F1 |
| 三类 Macro F1 | 40.5% | 48.0% | 全部 30 条，固定三类的 F1 均值；拒答是其真实类别的 FN，不作为第四参考类 |
| 已判断文案一致率 | 12/30 = 40.0% | 13/20 = 65.0% | 分母不同；不能单凭这两个百分比概括系统优劣 |
| 覆盖率 | 30/30 = 100% | 20/30 = 66.7% | 未拒答数 / 全部 30 条；不是免人工确认比例 |
| 拒答／转人工提示率 | 0/30 = 0% | 10/30 = 33.3% | 拒答数 / 全部 30 条；无真实工单派发 |

合并指标由保存的 test_baseline.csv／test_full.csv 直接核算，未写入或改动正式 CSV。高风险专项 TP/FP/FN：基线 3/0/9，ClaimTrace 10/7/2；合并口径：基线 8/0/17，ClaimTrace 17/0/8。原 80% 合并召回目标未达到。

ClaimTrace 输出分布：高风险 17、需证据 0、低风险 3、证据不足 10。需证据 Precision 为 0/0，没有定义；指标脚本按零分约定记 0 以计算 Macro F1，不意味着实际 Precision 已测得为零。需证据 Recall 为 0/13。

| 来源组 | 全部数 | 已判断一致／已判断数 | 覆盖率 | 转人工提示率 |
| --- | --- | --- | --- | --- |
| case_derived | 15 | 7/14 = 50% | 14/15 = 93.3% | 1/15 = 6.7% |
| synthetic | 15 | 6/6 = 100% | 6/15 = 40% | 9/15 = 60% |

6/6 只说明已判断的 6 条与项目标签一致；不是合成组整体准确率，更不是对全新真实文案的 100% 泛化证明。

| 人工复核指标 | 全部 | 案例改写 | 合成 | 适用范围 |
| --- | --- | --- | --- | --- |
| completed | 20/20 | 10/10 | 10/10 | 唯一 claim_id；pending 和空 review_status 为 0 |
| 引用覆盖 | 11/20 = 55% | 9/10 = 90% | 2/10 = 20% | 所选复核样本中 citation_present=yes |
| 引用支持率 | 10/11 = 90.9% | 8/9 = 88.9% | 2/2 = 100% | completed 且 present=yes、supported 为 yes/no；不是全部30条 |
| 引用 not_applicable / uncertain | 9 / 0 | 1 / 0 | 8 / 0 | 单独披露，不补作 yes/no |
| 建议可执行性 not_applicable | 20 | 10 | 10 | 历史 next_action 缺失，尚未验证，不能称 100%可执行 |

理由支持分类：yes 13、no 2、uncertain 5；不确定性表达：yes 9、no 4、uncertain 7。它们来自原人工汇总，没有把自然语言备注自动编码。正式人工复核不同于早期 manual_review.csv 的 6 条工作记录。

## 4. 技术与成本证据边界

当前 [检索代码](../src/retrieval.py) 使用多语言 MiniLM 与余弦排序；[管线](../src/risk_pipeline.py) 暂定阈值为 0.30，判断条件为 >=。没有 FAISS、agent 或新训练分类器。10 条开发集人工核验为 completed：7 条案例编号精确一致、10 条语义相关／支持风险提醒；编号不一致不自动判为不相关，少量优先选择样本不代表全体检索准确率。

[RiskCard schema](../src/schemas.py) 与 UI 实现存在 highlighted_claim 字段，但历史 test_full.csv 没有保存该字段；本轮没有新的模型高亮质量验证。历史 next_action、实际模型、usage、费用和延迟同样缺失。当前模型配置默认值不冒充历史结果的实际模型。

[日志实现](../src/usage_logging.py) 会记录 `prompt_tokens`、`completion_tokens`、`total_tokens`、服务返回 cost、模型名、请求状态及请求耗时。本地 `logs/request_metrics.jsonl` 当前保存两条成功的独立开发集请求记录（详见 README）；这是小样本真实服务数据，不是锁定集评估或长期成本证据。日志没有保存 claim_id／文案，第一条无法从日志追溯到具体输入。正式 30 条评估的 Token／成本、稳定延迟分布和页面端到端响应仍“尚未测量”。估算金额／来源／日期仍缺失，不补零；本地替身和单元测试数字不是运行成本。

成本框架：模型 Token 费用 + 其他变动成本 + 每条正式发布的人工核查成本 + 固定成本按真实任务量摊销；价格要有对应模型、来源与日期。没有访谈、耗时、流量、单价或正式成功标准时，不计算 ROI 或“每成功任务成本”。真实请求会将文案和检索案例发送至外部服务；不保存文案的日志不等于整条请求不外传。

## 5. 新截图与演示证据

截图只证明当时可见状态，不冒充录制完成的视频。历史回放与本地替身都有固定顶部说明，不与实时模型请求混淆。

- [中文桌面](screenshots/verification-20260929/home-zh-1440-viewport.jpg)／[英文桌面](screenshots/verification-20260929/home-en-1440-viewport.jpg)
- [中文 320px](screenshots/verification-20260929/home-zh-320-viewport.jpg)／[英文 375px 工作台](screenshots/verification-20260929/workbench-en-375-viewport.jpg)
- [CLAIM031 历史标签分歧](screenshots/verification-20260929/history-claim031-zh-detail.jpg)／[CLAIM032 历史高风险](screenshots/verification-20260929/history-claim032-zh-viewport.jpg)
- [CLAIM084 历史拒答](screenshots/verification-20260929/history-claim084-zh-viewport.jpg)／[英文拒答回放](screenshots/verification-20260929/history-claim084-en-viewport.jpg)
- [本地模拟加载](screenshots/verification-20260929/local-mock-loading-zh-viewport.jpg)／[中文模拟错误](screenshots/verification-20260929/local-mock-error-zh-viewport.jpg)／[英文模拟错误](screenshots/verification-20260929/local-mock-error-en-viewport.jpg)

其他 375／768px 截图同目录保留。原有截图没有删除或覆盖。采集工具的全页截图不适应 Streamlit 内部滚动容器，已选择真实视口截图作为交付证据，没有把坏截图当成页面故障或有效证据。工具实际返回 JPEG，本轮新截图已校正为 .jpg 扩展名，像素内容没有改动。

## 6. 提交前最小清单（按影响／工作量）

1. **已完成：** 英文报告 word count 与 DOCX 逐页视觉验收；报告正文含对指标、评估规模、未达 80% 目标、模型／阈值选择和 rough edges 的批判。
2. **高影响／作者本人操作：** 按 [English demo script](DEMO_SCRIPT_EN.md) 录制 5±3 分钟视频，面部与屏幕同框；不把历史回放说成实时请求。视频尚未制作。
3. **已完成：** 限定 `tests/` 的离线测试与 30 个 Python 文件语法检查；本轮没有重跑正式评估或模型请求。
4. **高影响／需授权：** 审查待提交文件，确认忽略秘密与不必要缓存；获明确批准后才提交／推送，再验证远程文件与链接。许可与转载未确认前不擅自添加许可证或宣称可开源再分发。
5. **已知边界：** 最终提交语言为英语；老师已明确演示建议时长、面屏同框及前 8 分钟审阅上限。本次没有完整 Rubric 2，仍不能据此保证评分。

暂不做：新模型、agent、更多装饰、真实 API 采集、锁定集调参。原提案、人工结论、锁定集和正式结果保持历史性质，不回填缺失字段。
