# ClaimTrace：老师反馈落实行动计划

更新日期：2026-09-29（Asia/Shanghai）。这是落实形成性反馈的工作记录，**不是正式 rubric**。本文保留的旧 Prompt 为历史范本，不是新的执行授权；已完成项目不得再次创建／覆盖。尤其不要重新运行原仓库的指标写出、复核表生成或模型评估命令。当前执行状态与待批准项以下表为准。

| 组别 | 当前状态 | 下一步与证据 |
| --- | --- | --- |
| 1. 修复离线测试冲突 | 已修改，语法已验证；pytest 未运行成功 | `tests/test_metrics.py` 的 main 使用单独模拟 fixture；`conftest.py` 补强网络拦截，日志测试关闭 .env 加载。需先修复环境／批准安装。 |
| 2. README 双口径与完成状态 | 已更新，并从原始 CSV 只读核对 | 专项 12/30 正例与原目标合并 25/30 正例并列；合并自动检出 Recall 17/25=68%，未达 80%。 |
| 3. UI 中英文边界 | 已修改，文本键和语法已验证；真实页面待验证 | 只改 `src/ui_text.py`，不再暗示已派发人工工单；明确普通商品危险医疗宣传初筛与专业决策边界。 |
| 4. 技术权衡与交接 | 已更新 | `README.md`、`HANDOFF.md` 与本文件；自建／复用／托管服务、历史条件与授权证据缺口分开。 |
| 5. 当前工作版本隔离复现 | 副本与全新环境已建立；运行验证待安装授权 | 临时目录 `C:/Users/10231/Documents/Codex/2026-08-22/w-s-m/claimtrace-repro-20260929-audit01` 保存清单与报告。全新 Python 3.12.14 环境没有 pip／项目依赖，未安装、未联网；不是远程仓库零克隆。 |
| 6. 真实 Token／费用／延迟 | 日志已实现，实际测量未完成 | 无可验证真实日志；先另批样本、次数、预算与网络。新请求不能回填历史正式评估。 |
| 7. 当前截图与演示 | 待可运行应用与安全回放方案 | 已有三张旧截图，不证明当前中英文／窄屏状态；只能新增，不覆盖旧图。 |
| 8. 最终课程映射 | 待正式材料 | 需最终 rubric、提交说明、编号 1–6 的原始定义；不能猜评分或提交格式。 |

> 用途：把老师对 Project Problem Statement 的反馈转换成可执行、可验证的项目任务。
>
> 原则：不修改锁定测试集、项目人工参考标签、既有正式评估结果或 0.30 暂定阈值；不得为了改善数字重新调用模型。所有新增结论必须能追溯到仓库中的文件或人工复核记录。

## 1. 当前结论

项目不需要推倒重做，也不需要把主要精力继续放在前端美化上。老师已经肯定：测试前冻结参考标签、锁定 30 条正式测试集、把案例改写与合成文案分组报告，以及用人工复核检查系统输出。

截至更新日，状态为：

1. `evaluation/retrieval_audit_10.csv` 已完成 10 条开发集检索人工核验；精确编号 7/10、人工相关与风险提醒支持各 10/10，仅小样本结论。
2. `results/test_metrics.csv` 已有同一组 30 条上的专项 Precision、Recall、F1、Macro F1；README 已增加原目标合并口径的只读计数。
3. 锁定标签分布为高风险 12、需证据 13、低风险 5，原合并目标正例 25/30。
4. `evaluation/manual_review_20.xlsx` 已结构化，20 个唯一 ID、各组 10 条、全部 completed；`results/manual_review_summary.csv` 已汇总引用支持 10/11、覆盖 11/20。建议可执行性因历史字段缺失仍未验证。
5. 日志代码已实现，但真实 Token、费用、延迟没有记录，继续写尚未测量。
6. 中文 README 与 UI 边界已更新；最终英文材料／录屏格式等待正式提交要求。
7. 自动测试文件已实现并修复入口 fixture 冲突，AST 检查通过；pytest、真实页面与隔离复现尚未验证。没有联网、安装或真实 API 请求。

## 2. 第零步：保护锁定评估资产

### 必须保持不变

- `evaluation/test_set_locked.csv`；
- 项目人工参考标签；
- `results/` 中已有正式评估结果；
- 检索阈值 `0.30`；
- 模型调用和风险判断逻辑；
- `.env` 与 API 密钥；
- 已完成的人工复核结论。

### 意义

看过测试结果后再修改标签、阈值或模型，会形成测试集泄漏，正式结果将失去可信度。后续统计只能读取正式测试结果；阈值选择或检索改进只能使用开发集。

### 完成标准

- 后续统计不覆盖既有结果；
- Git 变更中不出现上述受保护文件的意外改动；
- 不为改善数字重新调用模型。

### Prompt 0：保护性检查

```text
请对以下 ClaimTrace 仓库做一次只读的评估资产保护检查：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

检查并报告：
1. evaluation/test_set_locked.csv 的行数、标签分布和文件状态；
2. results/test_baseline.csv、results/test_full.csv、results/test_summary.csv 是否存在；
3. 当前检索阈值所在文件及其值；
4. Git 未提交改动中是否包含锁定测试集、参考标签、results/ 或 .env；
5. 列出后续工作中必须保持只读的文件。

不得修改任何文件，不得调用模型，不得运行正式评估，不得打印 .env 内容或密钥。若发现受保护文件已有改动，只报告，不要自动恢复。
```

---

## 3. 第一步：补全 Precision、Recall 和规则基线

### 老师反馈对应点

只报告 Recall 会出现“全部标成高风险也能得到高召回”的问题。必须在同一套 30 条锁定测试集上同时报告 Precision，并与规则基线比较。

### 两种并列口径，不事后替换原目标

- 高风险专项：正例为 `high_risk`，负例为 `evidence_needed` 和 `low_risk`；
- 原选题目标合并口径：正例为 `high_risk` 或 `evidence_needed`，负例为 `low_risk`。系统只有预测为两种正类之一才算自动检出；
- `insufficient_evidence`：未自动给出参考类别，在分类指标中按未命中真实类别处理，并单独报告转人工率。

锁定测试集分布：

- `high_risk`：12 条；
- `evidence_needed`：13 条；
- `low_risk`：5 条；
- 总计：30 条。

### 已核对的结果

| 指标 | 规则基线 | ClaimTrace |
| --- | ---: | ---: |
| 高风险正例总数 | 12 | 12 |
| 预测为高风险 | 3 | 17 |
| TP | 3 | 10 |
| FP | 0 | 7 |
| FN | 9 | 2 |
| High-risk Precision | 100.0% | 58.8% |
| High-risk Recall | 25.0% | 83.3% |
| High-risk F1 | 40.0% | 69.0% |
| 三类 Macro F1 | 40.5% | 48.0% |
| 自动判断覆盖率 | 30/30，100% | 20/30，66.7% |
| 转人工率 | 0/30，0% | 10/30，33.3% |

三类 Macro F1 的口径：参考类别固定为 `high_risk`、`evidence_needed`、`low_risk`，`insufficient_evidence` 对其真实类别按未命中处理。

原目标合并口径，正例 25/30：规则基线 TP=8、FP=0、FN=17，Precision=8/8（100%）、Recall=8/25（32%）、F1=48.5%；ClaimTrace TP=17、FP=0、FN=8，Precision=17/17（100%）、Recall=17/25（68%）、F1=81.0%。原报告合并 Recall≥80% **未达成**，不能用专项 Recall 83.3% 替代。上述合并计数来自锁定标签与两个原始结果 CSV，只读计算，不在当前 test_metrics.csv 中，不为此写结果文件。

### 必须披露的限制

ClaimTrace 在这 30 条结果中没有预测出任何 `evidence_needed`。虽然高风险 Recall 较高，但三分类能力仍不稳定，不得只展示最有利的指标。

### 操作方法

以下指标脚本与输出已存在且已核对，**不需要再新建或执行原仓库写出命令**。这些步骤仅记录原先如何完成；后续 CLI 验证在隔离副本或测试临时目录进行。入口 main 会检查已核对的正式数字，单元测试用专用模拟 fixture，不能修改生产断言来适配通用 fixture。

1. 新建 `evaluation/metrics_test.py`；
2. 只读取 `evaluation/test_set_locked.csv`、`results/test_baseline.csv` 和 `results/test_full.csv`；
3. 输出混淆计数、逐类 Precision/Recall/F1、Macro F1、覆盖率和转人工率；
4. 新增 `results/test_metrics.csv`，不覆盖旧结果；
5. 人工核对输出是否与上表一致；
6. 确认脚本不导入或调用模型客户端。

### Windows 验证命令

仅在隔离副本中使用；会写出 `results/test_metrics.csv`。当前环境未验证能运行。

```powershell
.\.venv\Scripts\python.exe -m evaluation.metrics_test
```

若脚本不是模块方式：

```powershell
.\.venv\Scripts\python.exe .\evaluation\metrics_test.py
```

### 完成标准

- 明确 `high_risk` 正例为 12 条；
- Precision 和 Recall 同时出现；
- 两套系统使用同一批 30 条样本；
- 不把 13/20 写成总体准确率；
- 不把转人工算成自动分类正确；
- 脚本不调用网络或模型。

### Prompt 1：生成正式指标脚本

```text
请在以下仓库中完成“只读取已有结果的正式指标统计”：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

允许新增：
- evaluation/metrics_test.py
- results/test_metrics.csv

只允许读取：
- evaluation/test_set_locked.csv
- results/test_baseline.csv
- results/test_full.csv

要求：
1. 不调用模型、不访问网络、不重新运行正式评估；
2. 不修改或覆盖任何已有 CSV；
3. 验证三个输入文件均为 30 个唯一 claim_id，并检查 claim_id 集合一致；
4. 以 high_risk 为主要二分类正例，输出 TP、FP、TN、FN、Precision、Recall、F1；
5. 规则基线和 ClaimTrace 必须使用同一套 30 条样本；
6. 计算 high_risk、evidence_needed、low_risk 三个固定参考类别的逐类 Precision、Recall、F1 和 Macro F1；
7. insufficient_evidence 不是参考标签，对真实类别按未命中处理，并单独报告覆盖率和转人工率；
8. 输出每类真实数量和预测数量；
9. 将机器可读结果写入 results/test_metrics.csv，并打印摘要；
10. 增加断言，防止分母或样本集合错误。

预期核对值包括：high_risk 12 条；规则基线 high-risk Precision 100.0%、Recall 25.0%；ClaimTrace high-risk Precision 58.8%、Recall 83.3%；ClaimTrace 转人工 10/30。若不同，不要强行写入预期值，请停止并报告差异。

完成后说明修改文件、每个指标的分母，以及如何确认脚本未调用模型。不要修改 README，不要提交 Git。
```

---

## 4. 第二步：完成 10 条中文查询检索核验

### 当前状态与意义

原问题陈述计划使用英文训练的 `all-MiniLM-L6-v2`。当前仓库已经改为：

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

模型选择已调整，并已有 `evaluation/retrieval_audit_10.csv` 的 10 条开发集核验，全部 completed，复用 `results/dev_retrieval.csv`。Top-1 精确编号 7/10，人工语义相关和支持风险提醒各 10/10。它区分相同案例与相关案例，不证明所有中文查询准确率，也没有重新编码、检索、调阈值或调用模型。以下为已完成步骤的记录，不重复创建表格。

### 操作方法

1. 从开发集选择 10 条中文文案，不使用锁定测试集；
2. 优先选择有 `related_case_id` 的案例改写样本；
3. 复用 `results/dev_retrieval.csv` 的 Top-1 和相似度，不重新运行模型；
4. 人工打开来源案例，判断主题相关性和证据支持性；
5. 记录：

| 字段 | 含义 |
| --- | --- |
| query_id | 查询文案编号 |
| query_text | 中文查询文案 |
| expected_case_id | 预设关联案例 |
| retrieved_case_id | Top-1 检索案例 |
| top_score | 余弦相似度 |
| exact_case_match | 案例编号是否相同 |
| semantically_relevant | 人工判断是否相关 |
| supports_risk_reminder | 是否支持风险提醒 |
| reviewer_note | 判断依据 |
| review_status | 待复核/已完成 |

现有开发集前 10 条案例改写文案的 Top-1 精确案例编号命中为 7/10。这只能作为核对起点，不能直接称为正式“检索准确率 70%”。相似度也不是违法概率。

### 完成标准

- 恰好 10 条开发集中文查询；
- 每条都有人工相关性判断和理由；
- 区分相同案例与相关案例；
- 不修改 0.30 阈值；
- 不重新调用模型。

### Prompt 2：制作检索核验表

```text
请在以下 ClaimTrace 仓库中制作一份“10 条中文查询检索人工核验表”：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

先核对 src/retrieval.py 中当前真实使用的向量模型，不要根据 README 或旧问题陈述猜测。

要求：
1. 只从开发集选择 10 条中文查询，优先使用有 related_case_id 的 case_derived 样本；
2. 复用 results/dev_retrieval.csv 中已有结果，不重新编码语料、不重新运行检索、不调用模型；
3. 不使用锁定测试集调参，不修改 0.30 阈值；
4. 新建 evaluation/retrieval_audit_10.csv，不覆盖现有文件；
5. 字段至少包括 query_id、query_text、expected_case_id、retrieved_case_id、top_score、exact_case_match、semantically_relevant、supports_risk_reminder、reviewer_note、review_status；
6. 可以自动填充客观字段，但人工判断字段必须保留为空或 pending，不得虚构；
7. 给出逐条人工核验说明，说明什么情况下填写 yes、no 或 uncertain；
8. 不得把余弦相似度写成违法概率，也不得把案例编号不同自动判为不相关。

完成后报告所选记录及其选择理由。不要修改 README，不要提交 Git。
```

---

## 5. 第三步：把 20 条人工复核转换为可统计证据

### 当前状态

`evaluation/manual_review_20.xlsx` 已有 20 条结构化分层人工复核，case_derived 与 synthetic 各 10 条，review_status 全部 completed；工作表“复核记录”表头 A6:Z6、记录 A7:Z26。`results/manual_review_summary.csv` 已有汇总，无需重新做人工判断或生成新 coded 工作簿。早期 `evaluation/manual_review.csv` 有 1 条 completed、5 条 pending，不是这 20 条正式复核。

### 意义与字段

现有长文本备注已保留，以下结构化字段已经存在；不能再次把自然语言备注自动重判为 yes/no：

| 字段 | 允许值 |
| --- | --- |
| citation_present | yes/no |
| citation_supported | yes/no/not_applicable/uncertain |
| reason_supported | yes/no/uncertain/not_applicable |
| recommendation_actionable | yes/no/uncertain/not_applicable |
| uncertainty_clear | yes/no/uncertain/not_applicable |
| human_final_label | 三个参考标签之一 |
| review_status | completed |

引用准确率：

```text
已完成记录中 citation_present=yes 且 citation_supported=yes 的数量
÷ 已完成且 citation_present=yes、citation_supported 为 yes/no 的数量
```

按已确认编码：全部支持 10/11（90.9%）、引用覆盖 11/20；案例改写支持 8/9、覆盖 9/10；合成支持 2/2、覆盖 2/10。citation_supported 的 uncertain=0、not_applicable=9，均单列、不进入支持率分母。它衡量风险提醒的引用支持性，不证明当前商家违法。20 条 recommendation_actionable 都是 not_applicable，因为旧 test_full.csv 没有 next_action，不能当作该项已验证。中文读取未出现替换字符，用户仍需在 Excel 肉眼确认。

### 操作方法

以下工作已经完成；保留为历史步骤，不覆盖原表或复核结论。

1. 在 Excel 中肉眼检查中文是否正常；
2. 不覆盖原文件，制作新版本；
3. 保留原始 `review_note`；
4. 你本人逐条确认结构化字段；
5. 再由脚本汇总，不让模型代替人工裁决。

### Prompt 3A：只读检查人工复核表

```text
请只读检查：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener\evaluation\manual_review_20.xlsx

请：
1. 列出工作表、行数和列名；
2. 核对是否为 20 条唯一 claim_id，case_derived 与 synthetic 是否各 10 条；
3. 检查 completed、pending 和空值数量；
4. 判断哪些现有字段能支持 citation_present、citation_supported、reason_supported、recommendation_actionable、uncertainty_clear、human_final_label 和 review_status；
5. 明确缺少哪些字段；
6. 检查自动读取是否出现中文乱码，并提醒我在 Excel 中肉眼确认；
7. 提出最小修改方案和引用准确率分母定义。

不得修改 Excel，不得重写人工结论，不得调用模型，不得把自然语言备注自动判定为 yes/no。最后给出“现有字段 → 建议字段”映射表。
```

### Prompt 3B：人工确认后生成统计版副本

```text
我已经人工确认 evaluation/manual_review_20.xlsx 中 20 条记录的结构化复核字段。请先验证字段完整性，再创建新统计版，不覆盖原文件。

允许新增：
- evaluation/manual_review_20_coded.xlsx
- results/manual_review_summary.csv

要求：
1. 保留原始记录、review_note、来源标题和 URL；
2. 不改变人工最终标签和结论；
3. 验证 claim_id 唯一、review_status 全部为 completed；
4. 引用准确率分母只包含 citation_present=yes 且 citation_supported 为 yes/no 的记录；
5. not_applicable 与 uncertain 分别列出；
6. 分别报告全部、case_derived 和 synthetic；
7. 输出结构化字段的分类计数；
8. 若字段缺失或矛盾，停止并报告，不要猜测补值。

不要调用模型，不要修改原始工作簿、锁定测试集、results/test_full.csv 或 README，不要提交 Git。
```

---

## 6. 第四步：处理 Token、成本和响应时间

### 当前状态

原问题陈述中的单次费用是依据假设 Token 得出的估算，不是正式运行记录。仓库目前没有足够证据验证总 Token、总成本、平均响应时间或 P50/P95 延迟。没有证据时必须写“尚未测量”，不能填 0，也不能把估算写成实际结果。

### 解决顺序

1. 检查 OpenRouter 控制台或历史导出是否能对应到评估运行；
2. 有真实历史数据时保存导出和统计口径；
3. 没有历史数据时，不要为补指标重跑锁定测试；
4. 当前已实现 `src/usage_logging.py`，默认 `logs/request_metrics.jsonl`，本轮未发现真实记录；不要重复改客户端或回填历史；
5. 将估算成本与实际成本明确分开。

实际日志字段包括请求 ID、时间、请求／返回模型、prompt_tokens、completion_tokens、total_tokens、provider_cost_usd、estimated_cost_usd、pricing_source、pricing_date、latency_seconds、状态和错误类型；不保存全文或密钥。provider cost 是服务返回值，estimate 与计价来源／日期当前为空。request latency 仅 HTTP＋解析／验证，不含检索／页面处理，不能称端到端响应时间。

真实采集必须另外确认开发集或另列非锁定样本、请求数量、费用上限、网络与输出位置，不能用新测量冒充旧 30 条评估统计。原问题陈述的 token 假设与费用估算不是实际账单；不在本轮核实外部价格。

### Prompt 4A：证据审计

```text
请对 ClaimTrace 仓库现有 Token、API 成本和响应时间证据做只读审计：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

检查代码、results/、evaluation/ 和文档中是否保存模型名、输入/输出/总 Token、单次延迟、调用次数、单次成本或总成本。

要求：
1. 不读取或输出 .env 的秘密值；
2. 不调用模型，不访问 API，不重跑评估；
3. 区分计划估算、页面单次返回值和完整正式评估统计；
4. 对每个指标给出已有证据、缺失证据、是否可计算和来源文件；
5. 证据不足时建议写“尚未测量”，不要估算或补零；
6. 只提出未来日志设计，不修改代码。

最终输出证据矩阵，不修改任何文件。
```

### Prompt 4B：以后增加日志（确认后才使用）

```text
根据已经确认的 ClaimTrace 模型响应结构，为未来新请求增加最小化 Token 与延迟日志。开始修改前先列出计划修改文件、OpenRouter 响应中真实可用的 usage 字段和日志位置；字段不清楚时先停下来询问。

要求：
- 不改变模型、提示词、检索、阈值、风险判断或页面结果；
- 不读取或暴露密钥；
- 不重新运行锁定测试，不回填历史数据；
- 日志不得保存完整用户文案或秘密；
- 成本估算必须记录计价来源和日期，并与实际 usage 分开；
- 先增加单元测试，再进行最小修改；
- 只用本地模拟响应验证，不进行真实 API 调用；
- 不提交 Git。
```

---

## 7. 第五步：统一 README、英文报告和录屏口径

### 必须更新的事实

1. 向量模型已从原计划的英文模型改为多语言 MiniLM；
2. 主要结果同时报告 Precision 与 Recall；
3. 明确专项 `high_risk` 正例为 12/30、原目标合并正例为 25/30；两种口径并列，68% 未达 80%；
4. 规则基线与 ClaimTrace 放在同一张表；
5. 分开报告覆盖率、转人工率和已判断文案一致率；
6. 披露 ClaimTrace 没有输出 `evidence_needed`；
7. 检索人工核验与引用支持汇总已完成；真实成本／延迟、建议可执行性、当前页面实测仍未完成，分别标注；
8. 保留“初筛而非法律意见，低风险不等于法律批准”；
9. 不把人工参考标签称为监管机关官方标签；
10. 不声称案例改写证明对全新执法案例的泛化。

老师理解的产品包含风险等级、具体风险片段、引用案例以及证据不足时需要人工。仓库已有 `highlighted_claim` 字段，非空时 UI 用 st.info 显示；没有保存历史片段，不能声称其质量已验证。错误分支显示整段输入不是成功定位风险片段的证明。当前没有自动派单或人工接收人，UI 已明确请用户自行交由人工。模型解释仍可能是英文。新增截图和回放必须在安全范围验证，不能为演示编造缺失字段。

### Prompt 5A：先做事实一致性审计

```text
请对 ClaimTrace 最终文档做一次“先核对、后建议”的一致性审计，暂时不要修改文件。

仓库：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

交叉核对 README.md、src/retrieval.py、src/schemas.py、evaluation/、results/ 和人工复核汇总，生成待更新清单：
1. 当前真实向量模型；
2. 30 条锁定测试集标签分布；
3. 两套系统的 high-risk Precision、Recall、F1；
4. 三类 Macro F1 口径；
5. 覆盖率和转人工率；
6. 两个来源组的分母；
7. 20 条人工复核和引用准确率是否已有可验证汇总；
8. Token、成本和延迟是否有真实记录；
9. highlighted_claim 是否真实存在并在 UI 显示；
10. 哪些表述可能被误解为法律结论、官方标签或泛化证明。

不得调用模型，不得修改 README，不得重跑评估。每条建议必须给出来源文件；证据不足写“尚未验证”。
```

### Prompt 5B：确认后更新 README

```text
请根据已经确认的事实核对清单更新 ClaimTrace 的 README.md。只修改 README.md，不修改代码、数据、锁定测试集、人工标签、人工复核表或 results/。

要求：
- 同时报告 high-risk Precision 与 Recall，并与规则基线使用相同 30 条样本；
- 写明 high_risk 正例为 12/30；
- 分开写覆盖率、转人工率和已判断文案一致率；
- 明确三类 Macro F1 口径；
- 披露系统没有预测出 evidence_needed；
- 准确说明当前多语言模型与 0.30 暂定阈值；
- 只在有正式汇总文件时写引用准确率；
- 没有日志的 Token、成本和延迟写“尚未测量”；
- 保留非法律意见、低风险不等于批准和正式发布需人工确认；
- 不把 6/6 写成新文案准确率 100%；
- 不声称案例改写证明对全新案例的泛化。

完成后列出每个数字对应的仓库文件和分母。不要提交 Git。
```

---

## 8. 第六步：补自动测试和从零复现

### 当前问题

- 旧 `tests/test_pipeline.py` 为空，但已有 7 个非空测试模块与网络拦截 fixture；本轮修复了 main 的独立模拟数据与 .env 隔离。
- 语法检查通过，pytest 启动失败，没有可报告的通过／失败／跳过数量；项目虚拟环境启动器无法找到配置的基础 Python，备用环境缺 pytest 等依赖。未安装或联网。
- 本机启动历史不能替代全新目录验证；当前未提交工作版本的隔离副本不能冒充远程 GitHub 提交的复现。
- 源码、测试、指标与复核文件不能因环境问题自动恢复或删除；先取得安装／网络批准。

### 推荐最小测试

1. 规则基线输出字段；
2. 低于 0.30 时返回 `insufficient_evidence` 且不调用模型；
3. 结构化模型返回值的 schema 验证；
4. 无效 URL 或缺失字段处理；
5. 中文输入与中英文 UI 文本不报错；
6. 指标脚本的样本集合和分母正确。

测试必须使用模拟响应，不允许真实 API 调用。

### 从零复现方法

1. 当前工作版本有重要未提交文件，先以明确允许清单创建新临时副本，并记录 HEAD／未提交清单；将来远程零克隆另行验证；
2. 新建虚拟环境；
3. 检查解释器和所需依赖；需要安装或网络时先停止询问，再按 README 操作；
4. 不配置真实密钥也能启动页面并查看空状态；
5. 使用 `.env.example` 检查变量，不复制真实 `.env`；
6. 运行离线测试；
7. 核对示例数据与评估命令，指标输出仅在临时副本；来源链接验证须另获网络授权；
8. 不复制 .env、.git、.venv、logs 或缓存，不点击真实筛查；保留报告和临时目录，不自动删除。

### Prompt 6A：先设计测试

```text
请审查 ClaimTrace 的现有测试状态并设计最小可信测试方案：
C:\Users\10231\Documents\GitHub\claimtrace-ecommerce-risk-screener

只读检查 tests/、src/schemas.py、src/rules_baseline.py、src/retrieval.py、src/risk_pipeline.py 和模型客户端。告诉我：
1. 当前有哪些真实测试、哪些文件为空；
2. 哪些核心行为可完全离线测试；
3. 如何 mock 模型和检索，确保不访问网络；
4. 建议新增的测试文件、测试名称、输入和预期；
5. 如何测试低于 0.30 必须转人工；
6. 如何测试指标脚本的样本集合和分母。

本轮不要修改文件、安装依赖或调用 API，不要声称 pytest 已通过。
```

### Prompt 6B：实施测试

```text
请按照我确认的最小测试方案，为 ClaimTrace 增加离线自动测试。

要求：
- 只修改 tests/；如必须修改生产代码，先停止并说明原因；
- 不访问网络、不下载模型、不调用 OpenRouter；
- 使用固定 fixture 和 mock；
- 不修改阈值、业务逻辑、数据、锁定测试集或 results/；
- 每个测试说明保护的业务边界；
- 运行 pytest 并报告通过、失败和跳过数量；
- 缺依赖或无法运行时如实报告；
- 不提交 Git。
```

### Prompt 6C：从零复现

```text
请为 ClaimTrace 执行一次安全、可回收的从零复现检查。开始前先告诉我临时目录，不得删除或移动原仓库。

要求：
1. 从当前提交或远程仓库创建全新副本；
2. 创建全新虚拟环境并按 README 安装依赖；
3. 不复制原仓库 .env，不读取或输出密钥；
4. 验证 Streamlit 能否启动；
5. 验证不需要 API 的自动测试和指标脚本；
6. 不运行正式模型评估，不产生 API 费用；
7. 记录 README 命令、依赖、示例和引用链接的问题；
8. 结束后保留复现报告，临时目录是否删除由我决定。

如果需要网络、额外权限或真实密钥，先停止询问。不要修改原仓库，不要提交或推送 Git。
```

---

## 9. 可选指标：工作流分流能力

若把 `high_risk`、`evidence_needed` 和 `insufficient_evidence` 都解释为“需要行动或转人工”，现有结果为：

- 真实需要行动：25 条；
- 系统升级处理：27 条；
- TP：25；
- FP：2；
- Recall：100%；
- Precision：92.6%。

这最多反映“提示需要进一步行动”的工作流口径，不表示真的派发给人工或自动判断正确。系统提示处理 27/30 条，接近广泛预警，不能代替主要成绩。用户已确认转人工单独报告；正文应并列使用第 3 节的专项与原目标合并自动检出口径，不用该可选指标宣称原目标达成。

## 10. 暂时不能确定的课程编号

老师邮件中的课程覆盖编号 `1、2、3、4、5、6` 无法仅凭邮件判断具体含义。在看到正式 rubric 前，不应猜测第 4、5 项。

### Prompt 7：拿到 rubric 后进行课程映射

```text
下面我会提供 PE6201 的正式 rubric/作业要求和老师对 ClaimTrace 的反馈。请逐条建立“课程要求—仓库证据—当前状态—缺口—下一步”的映射表。

要求：
- 只使用我提供的 rubric 和仓库真实文件；
- 不根据编号猜测课程概念；
- 每个“已完成”必须有文件、结果或截图证据；
- 区分已实现、已验证、计划中、未测量和不适用；
- 不修改文件；
- 最后按提交影响和工作量排序。
```

## 11. 推荐执行顺序

八组当前状态见文首。已完成内容不要再执行旧创建 Prompt。下一步优先获批恢复有效环境并做隔离复现；真实用量待费用与网络授权，截图待应用可用，课程映射／最终语言格式待正式 rubric。Git 提交与推送仍需单独授权。

## 12. 最终检查清单

- [x] 已核对同一组 30 个唯一 ID 和锁定标签，未修改它们；
- [x] 专项 12/30 与合并 25/30 正例、Precision／Recall 并列报告；
- [x] 明确合并自动检出 Recall 68% 未达原目标；
- [x] 覆盖率、转人工率和已判断一致率分开；
- [x] 披露没有预测出 `evidence_needed`；
- [x] 10 条开发集中文检索核验与 20 条人工复核已有记录；
- [x] 引用支持率只使用有引用且支持性可判定的已完成记录；
- [x] 缺证据的 Token、费用和延迟标为尚未测量，不补零或估算；
- [x] 保留非法律意见、人工标签非官方、相似度非违法概率与泛化限制；
- [x] 测试使用替身且有网络拦截，语法已检查（不代表 pytest 运行通过）；
- [ ] 有效环境下完成 pytest 并记录实际数量；
- [ ] 当前页面／窄屏和安全历史回放截图完成；
- [ ] 当前工作版本隔离复现完成，远程零克隆另验证；
- [ ] Git 历史密钥及发布材料安全审计完成（本轮未读取 .env、未提交 Git）；
- [ ] 最终 Git diff 已人工检查；
- [x] 本轮没有自动提交或推送 Git；
- [ ] 已收到正式 rubric、提交说明和编号定义，再完成课程映射。
