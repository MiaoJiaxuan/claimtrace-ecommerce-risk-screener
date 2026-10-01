# ClaimTrace 项目交接文档

更新时间：2026-09-29（Asia/Shanghai）

## 项目与任务

仓库：C:/Users/10231/Documents/GitHub/claimtrace-ecommerce-risk-screener

本项目是 ClaimTrace 中文电商广告宣称风险初筛原型，面向缺少内部合规专员的小型卖家。当前任务是落实用户确认的八组计划：修复离线测试冲突、纠正文档的双口径指标、修改 UI 边界文字、更新技术权衡与交接、检查隔离复现，并在获得额外授权／正式材料后处理真实用量、当前截图和课程映射。

用户明确要求：骨架、旧 Prompt、TODO 和老师形成性建议不能冒充事实或正式 rubric。参考标签是项目人工标签，不是官方标签；insufficient_evidence 不是参考标签；案例改写不能证明对全新执法案例泛化。已确认保留“高风险专项”和原报告“高风险＋需证据”两种口径，转人工不算自动检出。允许筛查普通商品中的危险医疗功效宣传，不提供医疗、金融等专业决策或批准。

本轮只授权修改 tests/、README.md、src/ui_text.py、本文件与 TEACHER_FEEDBACK_ACTION_PLAN.md；隔离检查的文件只能写入新临时目录。模型、提示词、检索、0.30 阈值、业务判断、API 配置、数据、冻结标签、人工结论与已有 results/ 全部保持不变。不读取／复制 .env，不真实调用模型、不下载模型、不重跑评估、不提交／推送 Git，不删除文件。需要安装、联网、费用或扩大修改范围时必须先征求用户批准。

## 已完成

### README

已经完整阅读 C:/Users/10231/Desktop/README_zh_skeleton.md，并据此改写仓库根目录 README.md。当前 README 是中文审校稿，不是最终英文提交稿。

README 已核对并更新：目标与边界、真实流程和目录、安装命令、两种正类口径、三类 Macro F1、覆盖与转人工、来源分组、20 条复核及引用支持分母、10 条检索核验、Build vs Buy、原计划与当前实现差异、历史结果限制、外部数据传输和授权缺口。它仍是中文审校稿；最终交付语言、报告字数与视频时长需正式提交说明确认。

### 已核对的代码和数据事实

- data/sources.csv：30 条案例记录。
- data/claims.csv：90 条中文文案，其中 case_derived 45 条、synthetic 45 条；development 60 条、test 30 条。
- data/examples.csv：另有 10 条示例。
- evaluation/test_set_locked.csv：30 条锁定测试文案，编号不重复。
- data/label_guide.md：项目人工参考标签为 high_risk、evidence_needed、low_risk；这些不是监管机关的官方标签。
- insufficient_evidence 是系统因证据不足而转人工的输出，不是参考标签。
- src/retrieval.py 使用 sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2，多语言 MiniLM 向量和余弦相似度，默认检索 3 条案例。
- src/risk_pipeline.py 的暂定阈值是 0.30；低于阈值时不调用模型并转人工；达到阈值时最多调用一次模型。
- src/llm_client.py 通过 OpenRouter 调用默认 openai/gpt-4o-mini；不得读取或暴露 .env 真实密钥。
- 当前没有 FAISS、训练的新分类器或自治 agent；独立 LLM judge 是原计划可选项，未实现。
- 当前 UI 有中英文切换，模型理由／建议和案例内容不保证翻译。src/ui_text.py 已改成“系统初筛风险”，不再暗示人工工单已派发；没有自动接收人功能。
- src/schemas.py 定义 highlighted_claim，app.py 对非空值显示 st.info；不是已验证的逐字定位。旧 test_full.csv 没有该字段、next_action、实际模型名、usage 或延迟，无法据当前代码还原全部历史条件。

### 已有评估结果

正式保存结果来自 results/test_baseline.csv、results/test_full.csv、results/test_summary.csv；逐类统计见 results/test_metrics.csv。本轮只读重新计数，样本 ID 与锁定参考标签一致，没有生成或覆盖结果文件：

- 规则基线：12/30 一致。
- ClaimTrace 全部：20/30 已判断，13/20 已判断文案一致，10/30 转人工。
- 案例改写组：7/14 已判断文案一致，14/15 覆盖，1/15 转人工。
- 合成新文案组：6/6 已判断文案一致，6/15 覆盖，9/15 转人工。

6/6 不能写成“新文案准确率 100%”，因为另外 9/15 条转了人工。案例改写组与已有案例相近，不能单独证明对全新执法案例的泛化能力。

| 口径 | 正例数 | 规则基线 Precision / Recall | ClaimTrace Precision / Recall |
| --- | ---: | --- | --- |
| high_risk 专项 | 12/30 | 3/3、3/12（100.0%、25.0%） | 10/17、10/12（58.8%、83.3%） |
| high_risk＋evidence_needed 合并 | 25/30 | 8/8、8/25（100.0%、32.0%） | 17/17、17/25（100.0%、68.0%） |

合并口径只将预测为上述两类算自动检出，正例转人工算 FN。原报告 Recall ≥80% 的合并目标未达到，不能用专项 83.3% 宣称达标。合并指标由原始 CSV 只读核算，尚未写入 test_metrics.csv。三类 Macro F1 基线 40.5%、ClaimTrace 48.0%，均在全部 30 条上算三个固定类别的平均，转人工在真实类别按未命中；不是已判断子集指标。ClaimTrace 预测 17 高风险、0 需证据、3 低风险、10 证据不足。

开发集结果来自 results/dev_full.csv、results/dev_summary.csv，仅是开发阶段观察：

- 47/60 已判断；
- 31/47 已判断文案一致；
- 13/60 转人工。

### 人工复核状态

evaluation/manual_review_20.xlsx 是当前正式内部复核表：工作表“复核记录”A6:Z26，表头第 6 行、20 条数据第 7–26 行；20 个唯一 claim_id，case_derived 和 synthetic 各 10 条，review_status 全部 completed。中文读取正常，Excel 肉眼检查仍应由用户确认。自然语言备注与人工结论不得自动重判。

results/manual_review_summary.csv 已有结构化汇总：有引用 11/20，支持 10/11；案例改写支持 8/9、引用覆盖 9/10；合成支持 2/2、引用覆盖 2/10。支持率分母只纳入 completed、有引用且 citation_supported=yes/no 的记录；uncertain=0、not_applicable=9 单列。它是引用对风险提醒的支持性，不证明商家违法。

20 条 recommendation_actionable 均 not_applicable，因为历史 test_full.csv 未保存 next_action；已完成复核不等于建议可执行性已验证。早期 evaluation/manual_review.csv 有 6 条工作记录，CLAIM031 completed，其余 5 条 pending，不能替代 20 条正式复核。

evaluation/retrieval_audit_10.csv 已完成 10 条开发集 case_derived 中文查询核验，复用 results/dev_retrieval.csv。Top-1 案例编号精确命中 7/10，人工语义相关与风险提醒支持均 10/10；不得称为对所有中文查询的检索准确率或用锁定集调参。

用户已经补充 CLAIM031 的备注：官方案例可支持“相似表达存在风险”的提醒，但案例涉及另一家公司，不能单独证明当前新卖家的 9 元不限量高速流量承诺虚假；应核对当前商品资费、流量限制和销售凭证。由于 results/test_full.csv 没有保存 next_action，所以建议可执行性目前无法从结果文件核查。

当前 HEAD：009fa9ea8cc171daa95238b83194b3fb31b8f09d。用户已有多项未提交前端、日志、复核及文档改动，新测试、metrics_test.py、检索核验、指标汇总、assets/、tokens.css 等尚未跟踪。必须重新执行 git status 核对，不假定它们已进入 GitHub。本轮未提交 Git，未恢复用户已有改动；manual_review_20.xlsx 的既有修改来自本轮开始前，不能自动撤销。

### 日志与离线测试

src/usage_logging.py 与客户端已实现未来请求的元数据日志，默认 logs/request_metrics.jsonl；截至本轮检查未发现真实日志，历史 Token、实际费用、延迟仍未测量。request latency 是 HTTP＋解析／schema 验证，不含检索和页面处理。服务 usage.cost 与估算分开，估算价格和日期目前为空。代码会在模型调用时外发完整输入与案例证据；日志不记录全文不等于无需隐私提醒。

tests/ 已有 schema、规则、检索、管线、客户端、指标与日志测试；旧 test_pipeline.py 仍为空。2026-09-29 仅改 test_metrics.py、conftest.py、test_usage_logging.py：保留通用纯计算 fixture，给 metrics.main() 单独构造 30 条模拟 fixture（不用真实锁定数据），修复其与硬编码保存结果检查的冲突；补强网络拦截；关闭日志测试的真实 .env 加载。

9 个测试文件以及现有 src/、app.py、evaluation/ 的 AST 语法检查通过。pytest 启动失败，尚未收集／执行测试，没有通过、失败、跳过数量。项目 .venv 的 Python 启动器报无法找到所配置的基础 Python；备用 Python 缺 pytest、requests、dotenv、sklearn、sentence_transformers、streamlit 等。没有安装、联网或真实模型请求。

### 隔离复现准备

已建立 C:/Users/10231/Documents/Codex/2026-08-22/w-s-m/claimtrace-repro-20260929-audit01，保存明确清单的当前工作版本副本、COPY_MANIFEST.json 和 REPRODUCTION_REPORT.md。未复制原 .env、.git、.venv、logs 或缓存。它是工作版本快照，不是远程仓库零克隆验证。

使用备用 Python 3.12.14 创建了全新虚拟环境（--without-pip --copies），确认 sys.prefix 与 sys.base_prefix 不同；为遵守安装前申请要求，尚未引导安装 pip 或项目依赖，环境内没有 pytest／Streamlit。全新环境、文件复制与语法检查不等于运行复现通过。必须先获批安装依赖，才能继续 pytest、Streamlit、隔离指标写出和当前截图；临时目录保留，不自动删除。

## 当前卡点

1. 隔离 Python 虚拟环境已创建，但依赖未安装；原项目环境失效，阻碍 pytest、Streamlit 和运行复现。安装或网络必须单独获批。
2. 20 条复核已完成，但历史 next_action 缺失，建议可执行性无法核查；highlighted_claim 历史片段质量也未验证。
3. 正式分类指标与引用支持汇总已有证据；真实 Token、费用、请求延迟和端到端时间仍未测量，不能用页面单次值或计划估算补缺。
4. 现有 docs/screenshots/ 三张截图属于旧版，不能替代当前中英文和窄屏实测；未进行安全历史回放。
5. 正式最终 rubric、提交说明和老师编号 1–6 的定义尚未提供，不能猜评分、语言、字数、视频时长或必须公开 GitHub。
6. 依赖未锁版，合成文案生成脚本／提示词缺失；官方链接、转载授权、代码许可证、零克隆复现与 Git 历史密钥审计未验证。

## 下一步计划

### 1. 已完成的人工复核不要重做

已复核的 20 条锁定测试样本：

- 案例改写：CLAIM031、CLAIM032、CLAIM034、CLAIM035、CLAIM036、CLAIM037、CLAIM039、CLAIM040、CLAIM042、CLAIM044。
- 合成新文案：CLAIM076、CLAIM077、CLAIM078、CLAIM079、CLAIM080、CLAIM081、CLAIM084、CLAIM086、CLAIM089、CLAIM090。

已有结构化字段 citation_present、citation_supported、reason_supported、recommendation_actionable、uncertainty_clear、human_final_label、review_status，见 workbook。不要因旧任务清单再次新建／覆盖表格或重写人工结论。缺失 next_action 不能凭空补造。若用户保留了历史页面证据，需先核实关联记录及来源，再单独征求补充授权。

### 2. 先恢复环境，后验证已有测试与隔离副本

无需重跑正式评估来补统计。当前分类与引用数字已有文件；README 合并 Recall 68% 未达标说明必须保留。请先让用户确认恢复／安装环境方案，再运行限定目录的 python -B -m pytest -p no:cacheprovider tests。隔离副本只复制明确清单，排除 .env、.git、.venv、logs 与缓存；记录 HEAD 和未提交文件，称“当前工作版本隔离复现”，不冒充远程零克隆。指标写出命令只能在临时副本执行；报告与目录保留，不自动删除。

### 3. 最终材料

等待用户上传正式 rubric、最终提交说明与编号 1–6 的定义，再决定英文 README、权衡报告、录屏的语言与格式；此前“1200 词”是旧计划／截图建议，未由正式要求验证。报告必须保留双口径分母、原目标未达成、参考标签不是官方判定、案例改写不证明全新案例泛化、人工确认边界和缺失指标。真实用量采集需另批样本、请求次数、预算与网络，不回填历史正式评估。

### 4. 提交前检查

环境可用后，先验证真实中英文初始状态、输入、空输入反馈与窄屏，新增截图、不覆盖旧图。结果展示仅可在安全隔离回放中使用真实保存字段；缺失高亮、建议、usage 不得补值。无法安全回放就询问用户。链接核查需要网络授权；Git 提交／推送仍需独立授权。当前结果目录不得为复现或达标被覆盖。

## 绝对不要重复的坑

### CSV 整行替换会删记录

之前修改 CLAIM031 时整行替换误删了 CLAIM039，后来已恢复。以后只编辑 review_note 字段，或使用可靠的 CSV 编辑方式；不要选中整行再粘贴长文本。备注含英文逗号时必须放在成对双引号内。

### 不要改文件来提高结果

不要修改 data/claims.csv 的标签、evaluation/test_set_locked.csv、results/test_full.csv、results/test_baseline.csv、results/test_summary.csv、results/dev_full.csv、results/dev_summary.csv 或任何已有案例／评估结果。人工复核是记录意见，不是改标签。

### 不要混淆分母

13/20 是已判断文案的一致数／已判断数，不是 13/30 总体准确率；20/30 是覆盖率；10/30 是转人工率；合成组 6/6 不是 6/15。

### 不要把开发集当正式测试

31/47 只属于开发阶段观察。锁定测试集标签必须固定。

### 不要混淆系统输出和参考标签

insufficient_evidence 只是系统证据不足并转人工，不属于 high_risk、evidence_needed、low_risk。

### 不要把相似案例写成法律裁决

案例只能说明特定来源记录的特定案件事实。相似措辞不能单独证明新卖家或新产品作了同样的虚假宣传。low_risk 不等于合法或获批。

### 不要以为一次命令会从头重跑

evaluation/test_full.py 和开发集完整流程会按 claim_id 跳过已有结果。一次运行不代表重新调用模型或重新生成全部结果。重新运行必须使用隔离副本、有效 API 密钥并记录模型、环境和时间。

### 不要声称 pytest 通过

旧 test_pipeline.py 为空不等于全部测试为空；当前新测试已经存在，但本轮未成功启动 pytest。AST 检查不等于自动测试通过。metrics.main() 有保存结果核对断言，入口测试必须使用单独模拟 fixture，不能删断言、改生产代码或标记跳过来掩盖冲突。

### 不要暴露密钥

不要读取、复制或回复 .env 的真实内容；只可引用 .env.example 的占位变量名。

## 关键文件

入口：app.py

规则：src/rules_baseline.py

检索：src/retrieval.py

阈值与转人工：src/risk_pipeline.py

模型请求：src/llm_client.py

字段验证：src/schemas.py

标签：data/label_guide.md

案例：data/sources.csv

文案：data/claims.csv

锁定测试：evaluation/test_set_locked.csv

人工复核：evaluation/manual_review_20.xlsx（早期 manual_review.csv 仅工作记录）

人工复核汇总：results/manual_review_summary.csv

检索核验：evaluation/retrieval_audit_10.csv

分类统计：evaluation/metrics_test.py、results/test_metrics.csv

未来请求日志：src/usage_logging.py（尚无真实记录）

正式测试汇总：results/test_summary.csv

开发集汇总：results/dev_summary.csv

测试逐条结果：results/test_full.csv

基线逐条结果：results/test_baseline.csv

## 最短交接结论

README、UI 边界与交接资料已更新，20 条人工复核、10 条检索核验和分类统计已有证据。原合并目标 Recall 68% 未达到 80%；专项 83.3% 不能替代它。测试实现与语法检查已完成，pytest 和当前页面实测因环境问题未验证。真实用量、建议可执行性、授权及最终提交材料仍有缺口；下一步先取得环境方案批准与正式 rubric，不重跑正式评估或重做已确认人工判断。
