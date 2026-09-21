# ClaimTrace 项目交接文档

更新时间：2026-09-21（Asia/Shanghai）

## 项目与任务

仓库：C:/Users/10231/Documents/GitHub/claimtrace-ecommerce-risk-screener

本项目是 ClaimTrace 中文电商广告宣称风险初筛原型。当前任务是按照老师要求，用仓库实际代码、数据和结果整理可信 README，并完成正式评估所需的人工复核及最终报告材料。

用户明确要求：骨架中的“计划”“开发中”和 TODO 不是已实现事实；不能把项目人工标签说成官方标签；不能把 insufficient_evidence 当作参考标签；不能把案例改写测试当作全新执法案例泛化证明；没有可验证记录的指标、成本或复现检查必须写尚未测量／尚未验证；不要修改代码、原始数据、人工参考标签、锁定测试集或已有评估结果。

## 已完成

### README

已经完整阅读 C:/Users/10231/Desktop/README_zh_skeleton.md，并据此改写仓库根目录 README.md。当前 README 是中文审校稿，不是最终英文提交稿。

README 已包含：项目目标和目标用户；初筛而非法律意见的边界；规则基线—案例检索—阈值拒答—一次模型调用—人工复核流程；真实目录；Windows 安装与运行命令；数据数量与来源说明；正式测试和开发集结果；分母区分；局限性；授权、许可证和复现检查的未验证状态；页面和模型解释仍含英文的说明。

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

### 已有评估结果

正式锁定测试结果来自 results/test_baseline.csv、results/test_full.csv、results/test_summary.csv：

- 规则基线：12/30 一致。
- ClaimTrace 全部：20/30 已判断，13/20 已判断文案一致，10/30 转人工。
- 案例改写组：7/14 已判断文案一致，14/15 覆盖，1/15 转人工。
- 合成新文案组：6/6 已判断文案一致，6/15 覆盖，9/15 转人工。

6/6 不能写成“新文案准确率 100%”，因为另外 9/15 条转了人工。案例改写组与已有案例相近，不能单独证明对全新执法案例的泛化能力。

开发集结果来自 results/dev_full.csv、results/dev_summary.csv，仅是开发阶段观察：

- 47/60 已判断；
- 31/47 已判断文案一致；
- 13/60 转人工。

### 人工复核状态

evaluation/manual_review.csv 目前有 6 条记录：CLAIM001、CLAIM072、CLAIM031、CLAIM039、CLAIM084、CLAIM090。6 条 status 都是 pending。没有完成老师要求的 20 条人工复核。

用户已经补充 CLAIM031 的备注：官方案例可支持“相似表达存在风险”的提醒，但案例涉及另一家公司，不能单独证明当前新卖家的 9 元不限量高速流量承诺虚假；应核对当前商品资费、流量限制和销售凭证。由于 results/test_full.csv 没有保存 next_action，所以建议可执行性目前无法从结果文件核查。

当前 Git 工作树已知改动：

- README.md：中文版审校稿；
- evaluation/manual_review.csv：用户补充 CLAIM031 备注，且 CLAIM039 已恢复；
- HANDOFF.md：本文件；
- 尚未提交 Git。

## 当前卡点

1. 20 条人工复核未完成，目前只有 6 条 pending。
2. manual_review.csv 只有 claim_id、reference_label、system_label、status、review_note 五列，未分别记录输入支持、引用支持、建议可执行性和不确定性。
3. test_full.csv 没有 next_action；该项不能假装已核查，应记录为“现有结果无法核查”，除非用户保留了页面截图。
4. tests/test_pipeline.py 文件大小为 0，不能声称 pytest 已通过。
5. Macro F1、风险类别召回率、引用准确率、平均响应时间、跨全部请求的总 Token、总 API 成本都没有完整可验证记录。页面的单次 Token／成本不能冒充总体统计。
6. 官方案例链接逐条可访问性、案例文本转载／再分发授权、代码许可证、全新克隆安装运行和 Git 历史密钥审计尚未验证。

## 下一步计划

### 1. 完成人工复核

建议固定复核以下 20 条锁定测试样本：

- 案例改写：CLAIM031、CLAIM032、CLAIM034、CLAIM035、CLAIM036、CLAIM037、CLAIM039、CLAIM040、CLAIM042、CLAIM044。
- 合成新文案：CLAIM076、CLAIM077、CLAIM078、CLAIM079、CLAIM080、CLAIM081、CLAIM084、CLAIM086、CLAIM089、CLAIM090。

不要先改 test_set_locked.csv、claims.csv 或 results/*.csv。建议先征得用户确认后，建立独立的详细复核表，字段至少包括：

claim_id、claim_text、source_type、reference_label、system_label、abstained、reason、cited_source、input_evidence_support、citation_support、next_action_feasible、uncertainty_clear、reviewer_decision、review_note、reviewer、review_date。

每条复核：读取 results/test_full.csv 的输入、理由、abstained、来源标题和 URL；查看 data/sources.csv 与官方来源页；判断输入和证据是否支持系统结论；判断引用是否支持结论；检查下一步建议（若结果没有保存则写无法核查）；检查不确定性；最后记录人工结论。未完成的状态保留 pending，完成后才改为项目约定的完成状态。

### 2. 再计算指标

人工复核完成后，计算 Macro F1 和风险类别召回率，并明确区分全部测试集、已判断子集、覆盖率和转人工率。引用准确率只能依据人工核查，不可由标签匹配推断。没有完整记录的延迟、总 Token、总成本继续写“尚未测量”。

### 3. 最终材料

再将 README 从中文审校稿整理成最终英文 README，并写不超过 1200 词的英文权衡报告。报告必须保留分母、转人工机制、人工标签不是官方判定、案例改写不证明全新案例泛化、低风险不等于法律批准，以及缺失指标。

### 4. 提交前检查

在隔离副本或新目录验证安装、页面启动、来源链接和评估命令，再录屏和提交。当前结果目录不要为了重跑而覆盖锁定测试集或已有结果。

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

tests/test_pipeline.py 为空，除非以后添加并运行有效测试，否则不要写“pytest 已通过”。

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

人工复核：evaluation/manual_review.csv

正式测试汇总：results/test_summary.csv

开发集汇总：results/dev_summary.csv

测试逐条结果：results/test_full.csv

基线逐条结果：results/test_baseline.csv

## 最短交接结论

README 中文审校稿已完成，但 20 条人工复核、最终英文材料和缺失指标尚未完成。当前 6 条 manual_review.csv 记录全部 pending。后续任何结论都必须写清分母、转人工率和样本类型，不能把案例改写测试或合成组的已判断一致率夸大成全新案例泛化能力。
