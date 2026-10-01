# ClaimTrace

Evidence-grounded preliminary screening for Chinese e-commerce product claims. ClaimTrace combines transparent phrase rules, retrieval from a small public enforcement-case collection, and an optional structured language-model assessment. It is a prototype for review support, not a legal decision or an approval system.

## Quick start (English)

The project was most recently exercised with Python 3.12.14. The dependency file does not pin versions; a fresh environment may resolve different package versions. The embedding model may need to be downloaded the first time the application starts.

```powershell
git clone https://github.com/MiaoJiaxuan/claimtrace-ecommerce-risk-screener.git
Set-Location claimtrace-ecommerce-risk-screener
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add an OpenRouter key only to the local, ignored `.env` file; never paste it into source code, screenshots, or Git. Then start the interface:

```powershell
python -m streamlit run app.py
```

For tests that do not call the API or download an embedding model, run only the dedicated unit-test directory:

```powershell
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
python -B -m pytest -q -p no:cacheprovider tests
```

Do not run `pytest` at the repository root: several scripts under `evaluation/` execute work when launched and some write result files or call external services. See [evaluation safety and file guide](evaluation/README.md) before running any evaluation script.

### Assessor documentation

- [Product, persona, inputs, outputs, architecture and metrics](docs/PRODUCT_DOCUMENTATION_EN.md)
- [Data inventory and label meanings](data/README.md)
- [Evaluation inventory and safe execution guide](evaluation/README.md)
- [Business and technical trade-off analysis](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.docx) ([Markdown source](docs/BUSINESS_TECHNICAL_TRADEOFF_EN.md))
- [English demo script](docs/DEMO_SCRIPT_EN.md)

The demo video itself still needs to be recorded by the author. It must show the presenter and relevant computer/mobile screen together, as requested by the instructor.

---

# ClaimTrace：中文电商广告宣称风险初筛

ClaimTrace 是面向中国小型电商卖家的原型：在发布商品文案前，输入一条中文宣称，查看规则提示、相近公开执法案例，以及一张结构化风险卡。它辅助发现值得修改、补证或复核的表达，不自动发布、删除或批准文案。

> **使用边界：** 本项目只做初筛，不提供法律意见，也不能保证符合现行法律或平台规则。`low_risk` 仅表示在项目有限规则和案例库范围内未识别出配置的风险，不等于法律批准；正式发布仍需使用者或合规人员人工确认。可以筛查普通商品文案中的治愈、疾病预防等危险宣传，但不提供医疗、金融或其他专业领域的决策与合规批准。当前没有自动阻止所有超范围输入或自动派发人工工单的功能。

## 目标用户与使用场景

主要面向没有内部合规专员的小型电商卖家。典型使用方式是在准备商品页面时，逐条输入中文广告宣称，初步了解哪些词句可能有明显风险、哪些宣称需要证明材料、哪些应转人工。案例相似度和模型解释是辅助线索，不是对当前商品或卖家的事实认定。

## 已实现的流程

1. [Streamlit 页面](app.py)接收一条非空中文宣称，先显示[关键词与模式规则基线](src/rules_baseline.py)的标签、命中词和理由。规则基线是独立对照结果，并不直接决定最终风险卡。
2. [案例检索](src/retrieval.py)读取案例标题与文本，使用 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` 多语言 MiniLM 向量模型生成归一化嵌入，以**余弦相似度**排序，默认展示最相近的 3 条案例及其记录的来源网址。
3. [流程控制](src/risk_pipeline.py)比较最高相似度与当前**暂定阈值 0.30**。低于阈值时，不调用大语言模型，返回 `insufficient_evidence` 并建议人工复核；此阈值尚未得到充分校准。高于或等于阈值时，才进入一次模型评估。
4. [模型调用](src/llm_client.py)通过 OpenRouter 对输入和检索证据至多调用一次模型，按[结构化字段](src/schemas.py)返回风险等级、问题片段、理由、引用来源、下一步建议、置信值及是否转人工。默认模型名在 `.env.example` 中为 `openai/gpt-4o-mini`，可由环境变量更改。模型被提示不得把历史执法案例中旧商家的事实认定直接套用到新商家。

页面同时呈现规则结果、检索案例和风险卡；模型被调用时，页面可展示服务返回的单次 Token 用量和成本字段。页面 UI 提供中英文切换，但模型生成的 `reason`、`next_action` 和部分外部案例内容仍可能是英文，**界面和模型解释尚未完全中文化**。模型返回非空 `highlighted_claim` 时，页面显示该字段；检索证据不足而直接转人工时该字段为空。现有正式测试结果未保存 `highlighted_claim`，其历史覆盖率与片段质量尚未统计。模型调用或页面处理失败时，页面提示转人工，而不是给出批准结论。

## Build vs Buy 与原计划的实现差异

以下取舍依据当前代码可观察的结构，不是对商业收益或替代产品的实测比较。

| 层面 | 当前做法与文件证据 | 取舍与限制 |
| --- | --- | --- |
| 自建工作流与评估 | `app.py`、`src/rules_baseline.py`、`src/risk_pipeline.py`、`src/schemas.py`、`evaluation/`、`tests/` 组织页面、规则、阈值拒答、字段验证及结果核验 | 可以检查每个阶段与分母；维护规则、案例和测试仍由项目承担。规则不是完整法律规则库，schema 验证也不证明理由或引用正确。 |
| 复用库和嵌入模型 | `requirements.txt`、`src/retrieval.py` 使用 Streamlit、pandas、Pydantic、sentence-transformers、scikit-learn 等现有库与多语言 MiniLM | 不训练新分类器；模型首次加载可能下载文件，依赖尚未锁定版本，检索阈值与新类别覆盖仍需验证。 |
| 使用托管基础模型服务 | `src/llm_client.py` 通过 OpenRouter 发送一次结构化评估请求，默认模型 `openai/gpt-4o-mini` | 减少自托管模型工作，但依赖外部服务、网络与使用费用。当前有 2 条独立开发集请求的成功用量记录；它们不是 30 条锁定测试的成本，也不足以估计稳定的平均延迟或长期费用。 |
| 保留人工确认 | `app.py`、`src/ui_text.py` 提示证据不足和发布前人工确认；`evaluation/manual_review_20.xlsx` 记录内部复核 | 页面没有任务派发、工单或人工接收人功能，不是自动合规批准系统。 |

原选题报告计划使用英文 `all-MiniLM-L6-v2` 与 FAISS。当前 `src/retrieval.py` 实际使用 **`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`＋scikit-learn 余弦相似度排序**，没有 FAISS 索引。已有 10 条开发集中文查询人工核验，不能据此宣称对所有中文类别充分验证，也没有替代检索方案的实测基准。

当前没有训练新分类器，没有实现自治 agent。原计划中的独立 LLM judge 是可选项，本版本未实现；已完成的 20 条内部人工复核不能写成 LLM judge 评估。模型提示词与引用限制不是对所有幻觉或提示注入的安全保证。

**数据传输边界：** 检索在本地进行；达到阈值、调用 OpenRouter 时，代码会发送完整输入文案与检索案例文本。最小化日志不保存完整文案，不等于文案不会离开本地。不要输入密钥、个人信息或未经允许外发的商业秘密。仓库没有外部服务数据保留政策或生产隐私合规核验的证据。

**历史结果边界：** 本 README 描述当前工作版本和已经保存的历史评估结果。`results/test_full.csv` 没有保存历史请求的模型名、提示词版本、`highlighted_claim`、`next_action`、usage 或延迟，不能仅凭当前默认配置完整还原旧评估条件。本次 UI、测试和日志改进没有重跑正式评估，也不是旧结果的生成条件。

## 标签与人工复核

以下三项是用于评估的**项目人工参考标签**，定义见[标签指南](data/label_guide.md)。它们由项目人员在评估前编写，**不是监管机关给出的官方标签**；官方案例也不能自动成为新文案的真实标签。

| 参考标签 | 在本项目范围内的含义 |
| --- | --- |
| `high_risk` | 明显绝对化、强误导或医疗功效保证等值得重点核查的表达，或与已有案例高度相关的表达。 |
| `evidence_needed` | 价格、销量、材料、性能、效果等宣称需要可靠的产品或交易记录支持。 |
| `low_risk` | 在有限项目范围内未发现明显风险表达或特别补证需求；不代表法律批准。 |

`insufficient_evidence` **不是参考标签**，而是系统因检索证据不足而拒绝判断、提示需要人工复核的输出；当前没有自动派发工单或指定人工接收人的功能。

项目内部结构化人工复核记录见 [20 条人工复核表](evaluation/manual_review_20.xlsx)：20 条锁定测试样本均标为 `completed`，其中案例改写文案 10 条、合成新文案 10 条。复核表记录了判断支持情况、引用支持性、建议可执行性、不确定性表达和人工最终标签。结构化汇总见 [人工复核汇总](results/manual_review_summary.csv)：

| 复核组别 | 复核记录数 | 已给出引用的支持率 | 引用覆盖率 | 引用支持性 `uncertain` / `not_applicable` 数 |
| --- | ---: | ---: | ---: | ---: |
| 全部 | 20 | 10/11，90.9% | 11/20，55.0% | 0 / 9 |
| 案例改写 | 10 | 8/9，88.9% | 9/10，90.0% | 0 / 1 |
| 合成新文案 | 10 | 2/2（仅 2 条可判定引用） | 2/10，20.0% | 0 / 8 |

支持率分母只包括 `review_status=completed`、`citation_present=yes` 且 `citation_supported` 为 `yes` 或 `no` 的记录；分子为其中 `citation_supported=yes` 的记录。`uncertain` 与 `not_applicable` 单独统计，不纳入该分母。汇总文件将该指标命名为 `citation_accuracy`，这里称为“引用支持率”，因为它衡量这批已给出引用能否支持风险提醒／理由，不证明当前商家违法，也不是系统总体准确率或法律正确率。这是项目内部人工编码的结论，不等于独立外部审查。

由于锁定测试结果文件没有保存 `next_action`，20 条记录的 `recommendation_actionable` 均为 `not_applicable`，因此**复核记录已完成，但建议可执行性尚未验证**。人工复核记录系统错误和证据局限，不会事后修改锁定测试集、参考标签或原始系统输出；`low_risk` 不代表法律批准，正式发布仍需人工确认。原有的 [早期人工复核记录](evaluation/manual_review.csv) 仅包含 6 条早期工作记录（1 条 `completed`、5 条 `pending`），不代表上述 20 条项目内部复核。

## 数据与来源

| 文件 | 已核对内容 |
| --- | --- |
| [案例记录](data/sources.csv) | 30 条项目整理的公开广告执法案例记录，含发布机构、日期、标题、案例文本、风险类型和来源网址。 |
| [评估文案](data/claims.csv) | 90 条中文宣称及英文翻译：45 条 `case_derived`（依据现有案例改写），45 条 `synthetic`（合成新文案）。开发集 60 条、测试集 30 条；两组各占一半。 |
| [示例文案](data/examples.csv) | 另有 10 条示例，不计入上述 90 条开发／测试文案。 |
| [锁定测试集](evaluation/test_set_locked.csv) | 30 条测试文案的固定副本；正式测试不应依据测试输出修改参考标签。 |

案例文件中的 `source_url` 用于追溯原始发布页，但**本版尚未逐条验证链接可访问性、案例文本转载／再分发授权**。合成文案是项目构造的评估样本，不是真实市场文案的随机抽样；仓库没有可核实的合成脚本或生成提示词，故不宣称可按同样过程重建全部文案。

`CLAIM031`–`CLAIM045` 等案例改写文案与案例库较相近，适合检验表达改写后的表现；这类测试**不能单独证明系统对全新执法案例的泛化能力**。合成新文案提供另一种压力测试，但样本规模仍有限。

## 实际目录

```text
claimtrace-ecommerce-risk-screener/
├─ app.py                         # Streamlit 页面
├─ requirements.txt               # Python 依赖
├─ .env.example                   # 环境变量占位示例
├─ .streamlit/config.toml         # Streamlit 主题与浏览器配置
├─ tokens.css                     # 现有前端样式 token
├─ assets/                        # 本地证据轨迹插画
├─ docs/screenshots/              # 已有历史截图，非本次当前页面验证
├─ data/
│  ├─ sources.csv                 # 30 条案例记录
│  ├─ claims.csv                  # 90 条开发／测试文案
│  ├─ examples.csv                # 10 条另列示例
│  └─ label_guide.md              # 人工参考标签定义
├─ src/
│  ├─ rules_baseline.py           # 规则基线
│  ├─ retrieval.py                # 向量检索
│  ├─ risk_pipeline.py            # 阈值与转人工控制
│  ├─ llm_client.py               # OpenRouter 请求
│  ├─ schemas.py                  # 风险卡字段验证
│  ├─ usage_logging.py            # 模型请求的最小化 usage／延迟日志
│  ├─ ui_components.py            # 页面组件与样式
│  └─ ui_text.py                  # 中英文 UI 文本
├─ evaluation/
│  ├─ test_set_locked.csv         # 锁定测试集
│  ├─ manual_review.csv           # 早期 6 条工作记录（1 条 completed、5 条 pending）
│  ├─ manual_review_20.xlsx       # 已完成的 20 条分层人工复核
│  ├─ retrieval_audit_10.csv      # 10 条开发集中文查询人工检索核验
│  ├─ metrics_test.py             # 只读取既有结果的正式指标统计
│  ├─ baseline_test.py            # 测试集规则基线
│  ├─ test_full.py                # 测试集完整流程，支持续跑
│  ├─ summarize_test.py           # 测试集汇总
│  ├─ compare_test.py             # 两系统逐条对照
│  └─ ...                         # 实存的开发集及其他评估脚本
├─ results/
│  ├─ test_baseline.csv           # 正式测试规则结果
│  ├─ test_full.csv               # 正式测试完整流程结果
│  ├─ test_summary.csv            # 正式测试汇总
│  ├─ test_comparison.csv         # 逐条对照
│  ├─ test_metrics.csv            # Precision、Recall、F1 与覆盖／转人工统计
│  ├─ manual_review_summary.csv   # 20 条人工复核的结构化汇总
│  ├─ dev_full.csv                # 开发集完整流程结果
│  └─ dev_summary.csv             # 开发集汇总
└─ tests/
   ├─ conftest.py                 # 未 mock 网络请求的拦截
   ├─ test_schemas.py             # 真实 Pydantic schema 验证
   ├─ test_rules_baseline.py      # 规则与优先级
   ├─ test_retrieval.py           # 临时 CSV 与假向量检索
   ├─ test_risk_pipeline.py       # 0.2999／0.30 边界与单次模型调用 mock
   ├─ test_llm_client.py          # 本地模拟 HTTP／JSON 响应
   ├─ test_metrics.py             # 样本集合、标签和指标分母；输出仅临时目录
   ├─ test_usage_logging.py       # 本地模拟响应的日志单元测试
   └─ test_pipeline.py            # 文件说明占位，目前不含测试用例
```

上表是主要文件的实存结构摘要，省略号不是功能承诺；其他开发集脚本和 CSV 可在仓库目录查看。

## Windows 安装与运行

以下命令依据当前仓库文件和已使用的 Windows PowerShell 启动方式编写。**从零克隆后在全新环境安装并完整运行，尚未做独立验证**；安装向量模型可能需要下载模型文件。仓库没有已验证的固定 Python 版本要求。

```powershell
git clone https://github.com/MiaoJiaxuan/claimtrace-ecommerce-risk-screener.git
cd claimtrace-ecommerce-risk-screener
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

在本地 `.env` 中自行填入有效的 `OPENROUTER_API_KEY`；不要将真实密钥提交到仓库或公开材料。当前 `.env.example` 仅有占位值和默认模型名。启动页面：

```powershell
python -m streamlit run app.py
```

浏览器打开终端给出的本地地址，输入一条中文商品宣称并点击“开始风险审查 / Start risk review”。页面是单条文案的交互式演示；没有证据、API 无法使用或输出处理失败时，需要人工复核。README 不提供真实密钥，也不承诺无密钥即可完成模型评估。

## 评估命令与续跑说明

下面是实存脚本的命令，不表示本次核验执行了它们。它们会写入 `results/`：第一项产生规则结果，第二项生成分组汇总，第三项生成逐条对照，第四项生成指标统计。**要保护当前正式结果，请只在隔离副本中运行这些写出命令。** README 数字的核对采用只读计算，不覆盖既有 CSV。

```powershell
python -m evaluation.baseline_test
python -m evaluation.summarize_test
python -m evaluation.compare_test
python -m evaluation.metrics_test
```

完整流程脚本 `python -m evaluation.test_full` **需要有效 API 密钥**，且对已存在的 `results/test_full.csv` 按 `claim_id` 跳过已完成行、接着续跑。因此在当前已有结果的仓库执行一次命令，**不意味着会重新调用模型或从头生成 30 条结果**。开发集的 `evaluation.full_dev` 同样按已有结果续跑。若要从空结果进行独立复现，应先在隔离副本中安排结果文件和密钥，并记录模型、环境与时间；该从零复现检查尚未完成。不要为了重跑而覆盖本仓库的锁定测试标签或已有结果。

## 项目锁定测试集评估

下表来自[规则结果](results/test_baseline.csv)、[完整流程逐条结果](results/test_full.csv)、[测试汇总](results/test_summary.csv)和[指标统计](results/test_metrics.csv)，比较对象是项目人工参考标签，不是监管机关的法律判定。锁定测试集共 30 条，其中 `high_risk` 12 条、`evidence_needed` 13 条、`low_risk` 5 条。以 `high_risk` 为正类时，测试集正例数为 **12/30（40.0%）**。规则基线与 ClaimTrace 均在相同的这 30 条测试样本上评估。

并列报告两种预先说明的正类口径，均使用同一组 30 条样本：**高风险专项**以 `high_risk` 为正类，正例 12/30；**原选题目标的合并口径**以 `high_risk` 或 `evidence_needed` 为正类，正例 25/30。合并口径中，只有预测为这两类才算自动检出；`insufficient_evidence` 不算自动检出，在正例上计入 FN，转人工率另列。

Precision = TP / (TP + FP)，Recall = TP / (TP + FN)，F1 = 2TP / (2TP + FP + FN)。三类 Macro F1 的口径为：在同一组全部 30 条样本上，分别计算 `high_risk`、`evidence_needed`、`low_risk` 的一对其余 F1，再取三者的算术平均，每类权重相同。它不是二分类 F1，也不是只在已判断文案上计算的平均。`insufficient_evidence` 不作为第四个参考类别；转人工样本在其真实参考类别的 F1 计算中按未命中处理，并另行计入转人工率。若某类别没有任何预测正例，项目统计脚本按约定将该类别 Precision 和 F1 记为 0；这是零分母约定，不表示测量到了 0/0。

### 高风险专项（正例 12/30）

| 系统 | 预测为 `high_risk` | TP / FP / FN | High-risk Precision | High-risk Recall | High-risk F1 | 三类 Macro F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 规则基线 | 3 | 3 / 0 / 9 | 3/3，100.0% | 3/12，25.0% | 40.0% | 40.5% |
| ClaimTrace | 17 | 10 / 7 / 2 | 10/17，58.8% | 10/12，83.3% | 69.0% | 48.0% |

### 高风险＋需证据合并口径（正例 25/30）

| 系统 | 自动检出为两类之一 | TP / FP / FN | Precision | Recall | 二分类 F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 规则基线 | 8 | 8 / 0 / 17 | 8/8，100.0% | 8/25，32.0% | 48.5% |
| ClaimTrace | 17 | 17 / 0 / 8 | 17/17，100.0% | 17/25，68.0% | 81.0% |

原选题报告的目标是对“高风险或需证据”宣称达到 Recall ≥ 80%。按上述合并口径，当前自动检出 Recall 为 **17/25（68.0%），尚未达到该目标**。不能改用高风险专项的 10/12（83.3%）宣称原目标达成，也不能把转人工算作模型已判断正确。合并后的 Precision 为 100.0% 仅表示已标出的 17 条都属于这两个项目参考类别；它不证明能区分二者，更不是总体准确率。

合并数字直接从锁定标签与两个原始结果文件按 `claim_id` 一一对应、只读计数得出；现有 `test_metrics.csv` 保存的是三类一对其余和 Macro F1 指标，未保存这一合并口径。本版没有为此新增或覆盖结果文件。

ClaimTrace 在这 30 条结果中**没有预测出任何 `evidence_needed`**：预测分布为 17 条 `high_risk`、3 条 `low_risk` 和 10 条 `insufficient_evidence`。因此，高风险 Recall 较高不代表三分类能力已经稳定，也不能只展示最有利的 Recall。

“一致”只表示标签字符串相同。ClaimTrace 的**已判断文案一致率**分母是未转人工条数，**覆盖率**分母是该组全部条数，**转人工率**分母也为该组全部条数；三者不可合并为“总体准确率”。

| 系统／组别 | 全部文案数 | 已判断且与参考标签一致 | 已判断文案一致率（分母：已判断数） | 覆盖率（分母：全部文案数） | 转人工率（分母：全部文案数） |
| --- | ---: | ---: | ---: | ---: | ---: |
| 规则基线（全部） | 30 | 12/30 | 40.0%（基线对全部 30 条给出标签） | 30/30，100.0% | 0/30，0% |
| ClaimTrace（全部） | 30 | 13/20 | 65.0%（仅已判断文案） | 20/30，66.7% | 10/30，33.3% |
| ClaimTrace：案例改写 | 15 | 7/14 | 50.0%（仅已判断文案） | 14/15，93.3% | 1/15，6.7% |
| ClaimTrace：合成新文案 | 15 | 6/6 | 100.0%（仅 6 条已判断文案） | 6/15，40.0% | 9/15，60.0% |

合成新文案的 `6/6` 仅表示**已判断的 6 条**与项目参考标签一致，另有 9 条转人工；这不是“新文案准确率 100%”，也不能证明系统对未见真实案例的判断能力。案例改写样本与案例库存在来源关联，不能单独证明系统能泛化到全新执法案例。规则基线一致数 `12/30` 和 ClaimTrace 已判断一致数 `13/20` 的分母不同，不能把两个比例当作相同覆盖范围下的总体准确率直接比较。

### 数字来源与分母

| 数字 | 仓库证据 | 计算口径／分母 |
| --- | --- | --- |
| 12 条高风险、13 条需证据、5 条低风险；合并正例 25 条 | `evaluation/test_set_locked.csv` | 30 条唯一 `claim_id` 的 `label` 分布；合并为 12 + 13 |
| 高风险专项：基线 3/3、3/12；ClaimTrace 10/17、10/12 | `results/test_baseline.csv`、`results/test_full.csv` 与锁定标签；`results/test_metrics.csv` | 分别为 TP/(TP+FP) 与 TP/(TP+FN)，在相同 30 条上计算 |
| 合并：基线 8/8、8/25；ClaimTrace 17/17、17/25 | 两个原始结果文件与锁定标签 | 预测为高风险或需证据才算自动检出；转人工不计为检出 |
| 专项 F1 40.0%、69.0%；合并 F1 48.5%、81.0% | 同上；专项另与 `results/test_metrics.csv` 核对 | 2TP/(2TP+FP+FN)；合并指标未写入结果文件 |
| 三类 Macro F1 40.5%、48.0% | `results/test_metrics.csv`，与两个原始结果文件核对 | 全部 30 条上固定三类 F1 的算术平均；基线为 (0.4000 + 0.4444 + 0.3704)/3，ClaimTrace 为 (0.6897 + 0 + 0.7500)/3，按未四舍五入值计算 |
| 17 / 0 / 3 / 10 条预测分布 | `results/test_full.csv`、`results/test_metrics.csv` | 分别为高风险／需证据／低风险／证据不足的条数，总数 30 |
| 一致 12/30；13/20；覆盖 20/30；转人工 10/30 | 原始结果及 `results/test_summary.csv` | 一致率分母为已判断数；覆盖／转人工率分母为全部 30 条 |
| 案例改写 7/14、14/15、1/15；合成 6/6、6/15、9/15 | `results/test_full.csv`、`results/test_summary.csv` | 两组各 15 条，依次为已判断一致／覆盖／转人工 |
| 人工复核 20 条、各组 10 条；引用支持 10/11、8/9、2/2；覆盖 11/20、9/10、2/10 | `evaluation/manual_review_20.xlsx`、`results/manual_review_summary.csv` | 支持率只纳入有引用且支持性为 yes/no 的已完成记录；覆盖率分母为该组全部复核记录；20 条建议可执行性均 not_applicable |
| 检索精确编号 7/10、语义相关 10/10、支持风险提醒 10/10 | `evaluation/retrieval_audit_10.csv`、原始 `results/dev_retrieval.csv` | 10 条开发集人工核验，不是锁定测试或违法概率 |
| 开发集 31/47、47/60、13/60 | `results/dev_full.csv`、`results/dev_summary.csv` | 分别为已判断一致／覆盖／转人工，非正式测试结果 |

这些是保存结果的离线核算与汇总，不是本次重跑模型得到的新结果。

### 10 条中文查询检索人工核验

[检索核验表](evaluation/retrieval_audit_10.csv)复用了开发集已有检索结果，没有重新编码语料、修改阈值或调用模型。10 条查询均为带 `related_case_id` 的 `case_derived` 中文文案：Top-1 案例编号精确相同为 **7/10**；人工复核认为 10/10 在语义上相关，且 10/10 能支持风险提醒。后两个数字是小样本人工核验结论，不是违法概率，也不能称为正式检索准确率；案例编号不同也没有被自动判为不相关。

### 开发集观察，不属于正式测试结果

[开发集逐条结果](results/dev_full.csv)和[开发集汇总](results/dev_summary.csv)显示：ClaimTrace 对 60 条中的 47 条作出判断，**31/47** 条已判断文案与项目参考标签一致（66.0%）；**覆盖率 47/60**（78.3%），**转人工率 13/60**（21.7%）。开发集用于观察与调试，不应与锁定测试集混写或当作独立泛化证明。

### 尚缺的评估证据

仓库的最小化 usage／延迟日志写入本地 `logs/request_metrics.jsonl`。截至 2026-10-01，该文件有 **2 条成功的独立开发集请求记录**，两次请求使用的模型均为 `openai/gpt-4o-mini`：

| 记录时间（UTC） | 输入 Token | 输出 Token | 总 Token | 服务返回费用（USD） | 请求阶段耗时 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-09-30 11:08:18 | 782 | 105 | 887 | $0.0001803 | 3.044005 秒 |
| 2026-10-01 04:16:13 | 809 | 173 | 982 | $0.00022515 | 3.827186 秒 |

以上是两个新请求各自的服务返回用量与费用，不是锁定 30 条正式评估的用量或成本。日志不保存文案或 `claim_id`，因此不能仅凭日志把记录对应到具体输入；也不能据此推算稳定的平均成本、P50/P95 或长期调用次数。完整正式评估的跨请求用量与成本、页面端到端响应时间仍**尚未测量**。`latency_seconds` 只计 HTTP 请求和响应解析／验证，不包括检索、模型加载及页面处理；不得称为完整页面响应时间。日志把服务返回的 `usage.cost` 与估算成本分开，目前没有估算价格记录。保存的 `llm_called` 标记也不足以证明服务端实际计费调用总数。

High-risk Precision／Recall／F1、三类 Macro F1 和覆盖／转人工率已有 [`evaluation/metrics_test.py`](evaluation/metrics_test.py) 与保存的统计结果；引用支持率见 20 条人工复核结构化汇总。建议可执行性因历史 `next_action` 缺失，仍未验证。

### 离线自动测试状态

`tests/` 已包含 schema、规则、假向量检索、阈值管线、模型客户端（包括 exact-span 和 retrieved-source 校验）、指标和日志测试；`tests/test_pipeline.py` 目前只有模块说明，没有测试用例。检索与 HTTP 使用固定替身，网络请求受 `conftest.py` 拦截，日志测试关闭 `.env` 加载。指标入口测试另用 30 条人工构造的模拟记录，保留通用 fixture 的纯计算测试；输入、输出及日志在临时目录，不读取真实锁定集作为 fixture。

2026-10-01 在本地 `.venv` 中关闭 Python 字节码／pytest 缓存写入，启用 Hugging Face 离线模式并由 `tests/conftest.py` 拦截网络，限定运行 `tests/`：**43 passed，0 failed，0 skipped（8.59 秒）**。这证明离线单元测试通过，不证明真实模型质量、外部 API 可用性或锁定集指标已重新评估。本轮对包含 exact-span 与 source-grounding guards 的当前代码运行测试；未重跑正式评估。首次不限定目录运行时，pytest 收集了 `evaluation/` 下有读写副作用的脚本并报错，没有覆盖 `results/`，因此必须限定测试目录。

在项目根目录的 PowerShell 中，可重复运行限定的离线测试：

```powershell
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
& '.\.venv\Scripts\python.exe' -B -m pytest tests/ -q -p no:cacheprovider
```

测试目录包含网络拦截和模型／HTTP 替身；不要用无目录限制的 `pytest` 命令，以免误收集 `evaluation/` 中的脚本。

## 已观察到的局限与下一步

- **案例相近不等于事实相同。** 已完成的 20 条人工复核显示，`CLAIM031`、`CLAIM039` 等文案虽然与历史案件存在相似风险，但历史案件中的虚假价格、商品来源或证书问题不能直接证明当前商家存在同样事实。此类文案仍需要当前商品、供应商或交易记录支持。
- **引用必须直接支持系统理由。** 人工复核发现，`CLAIM034` 当前保存的引用页面并未直接包含该果冻减肥效果或消费者证明真实性的事实，只能提供普通食品功效宣传的类别层面参考。该引用可以提示同类风险，但不能直接证明当前文案不实。
- **没有匹配案例不等于宣传真实。** 早期工作记录中的 `CLAIM072` 涉及“纯钛材质”声明，需要商品或供应商凭证；系统给出的 `low_risk` 不能替代事实核验，该条目前仍保留为待复核记录。
- **阈值与规则覆盖可能挡住明显风险。** `CLAIM084`、`CLAIM090` 的文案包含疾病预防或治疗保证等明显需要重点核查的表达，但系统因检索分数低于阈值而返回 `insufficient_evidence`。转人工比无依据地给出确定结论更审慎，但也说明规则和案例检索覆盖仍有限；当前 `0.30` 阈值只是暂定值，尚未经过充分校准。

- **结果受样本与模型条件限制。** 案例库仅 30 条，文案 90 条，合成样本并非真实流量抽样；模型、案例文本和外部服务变化可能影响复现。模型解释与引用仍需人工核实，不能据分数作精确法律判断。
- **提交证据与后续工作：** 10 条中文检索核验、锁定测试集指标、20 条分层人工复核与引用汇总，以及 43 项离线自动测试已有记录。两条独立开发请求有真实 usage／费用／请求阶段耗时，但不能代表正式 30 条评估或稳定延迟。建议可执行性仍未验证。英文商业与技术权衡报告、英文产品／数据／评估说明、运行指南和演示脚本现已准备；报告未达 80% 合并召回目标，须如实呈现。仍需作者录制面部与屏幕同框视频，并最终审查 GitHub 待提交文件、来源转载授权、代码许可及远程版本。阈值校准只能使用开发集，不能为达标修改锁定测试集或参考标签。

## 代码与数据授权状态

仓库当前可见 `.env.example` 不包含真实密钥，但**Git 历史是否曾出现密钥尚未审计**。官方案例的转载／再分发授权、代码许可证与从零克隆安装运行均**未验证**；在确认前，不应将案例文本或代码直接宣称为已经获准开源再分发。来源网址见 `data/sources.csv`，引用可核查性仍需逐条确认。
