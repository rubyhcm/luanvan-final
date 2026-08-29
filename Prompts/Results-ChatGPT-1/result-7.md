# Đặc tả Thiết kế Phần mềm

## 1. Kiểm tra Design Freeze
| Thành phần                    | Định nghĩa đã phê duyệt                                      | Diễn giải ở mức phần mềm                                                                                   |
|-------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Baseline**                  | Định nghĩa baseline trong result-6.md (Baseline 2025–2026) | Module `baseline/` triển khai đúng mô hình/phương pháp cơ bản đã được chấp thuận (ví dụ: mạng LSTM/CNN chuẩn) |
| **Hạn chế**                   | Hạn chế đã xác nhận của baseline (ví dụ: độ trễ phát hiện, ít ngữ cảnh) | Phần mềm giữ nguyên hạn chế trừ khi được cải thiện; phần `improvement/` mới khắc phục mục tiêu đã định nghĩa |
| **Cải thiện có mục tiêu**     | Mục tiêu cải thiện chính theo result-6.md (ví dụ: tích hợp tri thức, LLM) | Module `improvement/` chứa các thành phần bổ sung để đạt mục tiêu (ví dụ: truy xuất kiến thức, LLM prompt)    |
| **Thực nghiệm chính**         | Thiết kế thí nghiệm kiểm soát (baseline vs improved) đã phê duyệt | `Experiment Runner` chạy độc lập các chế độ baseline/improved với biến kiểm soát cố định                      |
| **Metric chính**              | Metric chủ đạo (ví dụ: F1-score, AUC, thời gian lead time) theo result-6.md | Module đánh giá thu thập và lưu metric này cho cả hai chế độ để so sánh                                        |

## 2. Phạm vi Phần mềm

### Trong phạm vi
- Chỉ bao gồm các thành phần cần thiết để **chạy baseline** (nạp dữ liệu, parsing, tạo cửa sổ, biểu diễn, mô hình baseline, đo lường).
- Các thành phần để **chạy cải thiện mục tiêu** (gồm module `improvement/`: truy xuất tri thức, xây dựng ngữ cảnh, prompt, LLM nếu có).
- **So sánh có kiểm soát**: hỗ trợ chạy hai chế độ đối chứng (`baseline` và `improved`) để so sánh công bằng.
- **Thực hiện ablation**: chế độ `ablation` cho phép loại bỏ hoặc tắt các thành phần cải thiện để đánh giá đóng góp riêng biệt.
- **Đánh giá Phát hiện Sớm**: tính toán chỉ số phát hiện sớm (TTD, lead time, v.v.) như yêu cầu.
- **Lưu artifact thực nghiệm**: lưu kết quả metrics, biểu đồ, logs cho mỗi experiment run.

### Ngoài phạm vi
- Không phát triển thành nền tảng AIOps production đầy đủ.
- Không triển khai cho môi trường multi-tenant, clustering, HA phức tạp.
- **Chỉ xây dựng phần mềm nghiên cứu tối thiểu** (proof-of-concept) nhưng đảm bảo **tái lập được kết quả**.
- Không có UI, không cần REST API (trừ trường hợp cần thử nghiệm performance như Docker hay streaming là tùy chọn).

## 3. Kiến trúc Mã nguồn

Cấu trúc thư mục mẫu:

```
project/
├── configs/        # Cấu hình YAML (dataset, baseline, improvement, model, evaluation, experiment)
├── data/           # Raw dataset (log files)
├── baseline/       # Cài đặt baseline (mô hình, detection)
├── improvement/    # Cài đặt cải thiện (ví dụ: Retrieval, LLM)
├── knowledge/      # (tùy chọn) Nạp và xử lý cơ sở tri thức
├── retrieval/      # (tùy chọn) Module truy xuất thông tin
├── models/         # Lưu trữ mô hình (baseline/improved)
├── prompts/        # (tùy chọn) Templates prompt cho LLM
├── detection/      # Kết hợp đầu ra để ra dự đoán cuối cùng
├── evaluation/     # Tính toán metrics, phân tích kết quả
├── experiments/    # Script chạy experiment (baseline/improved/ablation)
├── tests/          # Unit & integration tests
├── artifacts/      # Lưu kết quả (metrics, plots, logs)
└── docs/           # Tài liệu SDS, hướng dẫn sử dụng
```

- **configs/**: các file YAML định nghĩa tham số, cấu trúc dữ liệu, hyperparameters. Không chứa logic; *Status: New*.
- **data/**: chứa dữ liệu log gốc. Đầu vào cho Dataset Loader. *Status: Inherited* (từ kết quả nghiên cứu).
- **baseline/**: chứa code mô hình baseline và logic phát hiện dị thường cơ bản. Đầu vào: embedding của log; đầu ra: scores/labels. Phụ thuộc: `models/`, `configs/`. *Status: Inherited/Modified*.
- **improvement/**: chứa code cho cải thiện mục tiêu (ví dụ: hàm xây dựng truy vấn, gắn context, gọi LLM). Đầu vào: log representation (+context nếu có); đầu ra: features hoặc dự đoán bổ sung. Phụ thuộc: `retrieval/`, `knowledge/`, `prompts/`, `models/`. *Status: New*.
- **knowledge/**: (nếu dùng) xử lý dữ liệu tri thức (ingestion, định nghĩa metadata, version, temporal validity). Đầu vào: file tri thức; đầu ra: objects/index dùng cho retrieval. *Status: New*.
- **retrieval/**: xử lý truy vấn, embedding, search, ranking. Đầu vào: query (text hoặc vector); đầu ra: danh sách tài liệu liên quan. *Status: New*.
- **prompts/**: templates prompt (system/task, chỗ chèn context). Đầu vào: thông tin cần chèn; đầu ra: prompt string. *Status: New*.
- **models/**: lưu trữ weight/model checkpoint. *Status: New*.
- **detection/**: hợp nhất output của baseline và cải thiện thành dự đoán cuối (ví dụ: logic kết hợp score/label). Đầu vào: score từ baseline và output cải thiện; đầu ra: dự đoán cuối. *Status: New*.
- **evaluation/**: tính metrics. Đầu vào: predictions, ground truth; đầu ra: giá trị metrics. Phụ thuộc: `configs/` cho thông số metrics. *Status: New*.
- **experiments/**: scripts khởi chạy experiment (xử lý config, gọi pipeline). Đầu vào: config, mode; đầu ra: lưu kết quả. *Status: New*.
- **tests/**: tests tự động (unit test cho từng module, integration test cả pipeline). *Status: New*.
- **artifacts/**: không code, dùng lưu kết quả/run artifacts. *Status: New*.
- **docs/**: bao gồm SDS, README. *Status: New*.

**Luồng dữ liệu chính**:

```
Log Parser
  → Window Generator
  → Representation
  → [Baseline Model] / [Improvement Modules]
  → Detection (Prediction)
  → Early Detection Evaluator
```

Nếu sử dụng retrieval/LLM:

```
Current Context (log window)
  → Query Builder
  → Retriever
  → Context Builder
  → (Kết hợp với Representation hoặc LLM)
  → Model (Baseline/LLM)
  → Prediction
```

Mỗi interface xác định rõ mục đích, kiểu đầu vào (schema) và đầu ra, trường bắt buộc và cách xử lý lỗi. Ví dụ, Log Parser nhận log entry raw, trả về object có timestamp; Window Generator nhận list log đã parse, trả về mảng log windows. Xử lý lỗi: nếu thiếu timestamp hoặc format sai, ghi log lỗi và có thể bỏ entry đó.

Không có vòng lặp phụ thuộc (circular dependency): đường dẫn dữ liệu là tuyến tính hoặc cây.

## 4. Đặc tả Module và Interface

| Module                | Trách nhiệm                                                 | Đầu vào               | Đầu ra                       | Phụ thuộc               | Status      |
|-----------------------|-------------------------------------------------------------|-----------------------|------------------------------|-------------------------|-------------|
| **Dataset Loader**    | Đọc nạp dữ liệu log thô, chia train/test                     | File log raw          | DataFrame/List log entries   | configs (dataset)       | New         |
| **Log Parser**        | Xử lý từng entry log (tách fields, chuẩn hóa timestamp)      | Một log entry thô     | Structured log entry         | Dataset Loader          | New         |
| **Window Generator**  | Tạo các cửa sổ liên tiếp từ log đã parse                     | Danh sách log entries | List of log windows          | Log Parser              | New         |
| **Representation**    | Biểu diễn cửa sổ log (embedding, feature extraction)        | Một log window        | Vector đặc trưng (embedding) | Window Generator        | New         |
| **Core Model (Baseline)** | Mô hình phát hiện bất thường chuẩn (ví dụ: RNN)         | Log embedding         | Anomaly score hoặc label     | models, configs (baseline) | Inherited |
| **Targeted Improvement** | Thành phần cải thiện (LLM, retrieval)                    | Log embedding + context | Feature bổ sung hoặc score | retrieval, knowledge, prompts | New |
| **Knowledge Loader**  | Nạp cơ sở tri thức (logs lịch sử, incidents)                 | File tri thức         | Objects/Index tri thức       | configs (knowledge)     | New         |
| **Index/Embedding**   | Xây dựng index ANN cho tri thức                              | Knowledge objects     | ANN index                    | Knowledge Loader        | New         |
| **Query Builder**     | Tạo truy vấn (embedding/text) từ ngữ cảnh log hiện tại       | Log window/context    | Query vector hoặc text       | Representation, prompts | New         |
| **Retriever**         | Tìm kiếm tài liệu liên quan trong tri thức                   | Query                 | Ranked documents             | Index/Embedding        | New         |
| **Context Builder**   | Kết hợp tài liệu truy xuất với context hiện tại (truncation) | Documents, log window | Kết quả context tích hợp     | Retriever, prompts     | New         |
| **LLM Adapter**       | Gửi prompt + context đến mô hình ngôn ngữ, nhận output        | Prompt, Context text  | Raw LLM output (text)        | prompts, Context Builder | New        |
| **Output Parser**     | Chuyển output của LLM thành dự đoán hoặc features            | Raw LLM output        | Anomaly score/label          | LLM Adapter            | New         |
| **Detection**         | Kết hợp output baseline và improvement để ra quyết định cuối | Baseline score/label, Improvement output | Final score/label | Core Model, Improvement | New |
| **Metrics**           | Tính toán các chỉ số đánh giá (Precision, Recall, v.v.)      | Predictions, GT labels| Metric values               | Detection output, configs | New      |
| **Result Aggregator** | Tổng hợp kết quả nhiều runs (mean, std)                     | Metrics per run       | Báo cáo tổng hợp             | Metrics                | New         |
| **Experiment Runner** | Quản lý chạy experiment theo mode (baseline, improved, etc.)  | Config, seed, mode    | Lưu experiment results       | All modules            | New         |

**Luồng interface chính**:
- **Parser → Window → Representation → Baseline/Core Model**: pipeline cơ bản xử lý log và cho đầu ra anomaly score.
- **Parser → Window → Representation → Improvement Modules → Detection**: pipeline có cải thiện (nhúng retrieval/LLM), đầu ra tích hợp vào detection.
- **Prediction → Early Detection Evaluator**: module đánh giá sớm nhận output cuối để tính metrics liên quan.

Ví dụ interface cụ thể:  
- **Log Parser → Window Generator**: Mục đích tạo windows từ log. Đầu vào: list log entries (có timestamp). Đầu ra: list window (mỗi window là list log). Bắt buộc: timestamp hợp lệ; Lỗi: nếu thiếu timestamp, bỏ entry đó hoặc dừng pipeline.  
- Các interface khác được định nghĩa tương tự (dữ liệu đầu vào/ra là JSON, numpy array, v.v., và xử lý ngoại lệ rõ ràng).

Không có dependency vòng tròn trong thiết kế module.

## 5. Tách biệt Baseline/Cải thiện
- **Chế độ `baseline`**: chỉ chạy pipeline baseline (data→parser→representation→baseline model→evaluation).
- **Chế độ `improved`**: bao gồm cả baseline và các thành phần cải tiến mục tiêu. 
- **Chế độ `ablation`**: tắt bỏ hoặc thay đổi các thành phần cải thiện (ví dụ: `use_retrieval=false`) để đánh giá tác động.
- Cải thiện **không làm thay đổi ngầm metric**: cả hai chế độ dùng chung định nghĩa metric và quy trình đánh giá để so sánh công bằng.
- Module `Experiment Runner` chuyển đổi mode (qua config) và đảm bảo giữ cố định tất cả biến không phải mục tiêu thí nghiệm.

## 6. Đặc tả Cấu hình
Các file YAML cấu hình:

- **dataset.yaml**:  
  - `dataset_path` (string): đường dẫn đến dữ liệu log, default: `./data/logs`, fixed.  
  - `train_split` (float 0–1): tỉ lệ dữ liệu train/test, default: 0.8, tunable.  
  - `window_size` (int): số log trong 1 window, default: 50, tunable.  
  - `window_stride` (int): bước trượt của window, default: 1, fixed.  
  - `timestamp_field` (string): tên trường thời gian, default: `timestamp`, fixed.  
- **baseline.yaml**:  
  - `model_type` (string): loại mô hình (e.g., `LSTM`), default: `LSTM`, fixed.  
  - `hidden_size` (int): kích thước ẩn, default: 128, tunable.  
  - `learning_rate` (float): tốc độ học, default: 0.001, tunable.  
  - `epochs` (int): số epoch, default: 20, fixed.  
  - `batch_size` (int): default: 64, tunable.  
- **improvement.yaml**:  
  - `use_retrieval` (bool): có dùng retrieval không, default: False, tunable.  
  - `top_k` (int): số tài liệu truy xuất, default: 5, tunable.  
  - `use_llm` (bool): có dùng LLM không, default: False, tunable.  
  - `llm_model` (string): tên mô hình LLM (vd. `gpt-3.5-turbo`), default: `gpt-3.5-turbo`, fixed.  
  - `prompt_version` (string): phiên bản prompt, default: `v1`, fixed.  
- **model.yaml**:  
  - `seed` (int): random seed, default: 42, fixed.  
  - `device` (string): `cpu` hoặc `cuda`, default: `cuda`, fixed.  
  - `save_interval` (int): số epoch giữa mỗi lần lưu model, default: 5, fixed.  
- **retrieval.yaml** (nếu dùng retrieval):  
  - `embedding_model` (string): mô hình embedding (vd. `all-MiniLM-L6-v2`), default: `all-MiniLM-L6-v2`, fixed.  
  - `index_type` (string): `FAISS` hoặc `Annoy`, default: `FAISS`, fixed.  
  - `max_context_length` (int): giới hạn token context, default: 512, tunable.  
- **evaluation.yaml**:  
  - `metrics` (list): các metrics tính toán (vd. `[precision, recall, f1, auc]`), fixed.  
  - `early_metrics` (list): metrics phát hiện sớm (vd. `[TTD, lead_time]`), fixed.  
- **experiment.yaml**:  
  - `mode` (string): `baseline`/`improved`/`ablation`, default: `baseline`, fixed.  
  - `runs` (int): số lần lặp experiment, default: 1, fixed.  
  - `random_seed` (int): seed experiment, default: 42, tunable.  
  - `log_level` (string): `INFO`/`DEBUG`, default: `INFO`, fixed.  

**Trạng thái tham số**:  
- **Tham số cố định**: seed, thiết lập model, modes không thay đổi khi chạy lại (fixed).  
- **Tham số tunable**: hyperparameters (learning_rate, hidden_size, window_size, top_k,…), được điều chỉnh qua validation.  
- **Biến thực nghiệm**: mode chạy, số runs, bật/tắt cải tiến.

## 7. Thiết kế LLM / Prompt / Model
- **Prompt quản lý**: Định nghĩa system/task prompt và chỗ chèn context bằng template. Ví dụ: prompt cơ bản “Dựa trên ngữ cảnh log sau, hãy dự đoán xem có dị thường hay không:” với chỗ `{context}`.
- **Context insertion**: Module `Context Builder` chèn ngữ cảnh (từ Retriever) vào template prompt. Chừa chỗ `{context}` hoặc sử dụng JSON Schema để đảm bảo định dạng đầu ra.
- **Schema đầu ra**: Định dạng mong đợi từ LLM (ví dụ JSON: `{"anomaly": true, "confidence": 0.9}`) để `Output Parser` dễ xử lý.
- **Phiên bản prompt/model**: Ghi nhận `prompt_version` và `llm_model` trong cấu hình và lưu cùng artifacts để đảm bảo truy vết.
- **Sampling/Temperature**: Nếu LLM generative, thiết lập `temperature` (ví dụ mặc định 0.7) trong `improvement.yaml`.
- **So sánh công bằng**: Nếu baseline không dùng LLM, thì improved bật `use_llm=true`; các tham số như model LLM, prompt cho hai chế độ giống nhau (nếu applicable) để so sánh công bằng.
- Nếu sử dụng Foundation Model (LLM):
  - Định nghĩa interface chung (e.g., class `LLMAdapter`) để tách biệt provider (OpenAI, local) và adapter (logic gọi API).
  - Provider/Adapter rõ ràng: Adapter gọi API, provider lưu key hoặc endpoint.
  - Lưu metadata model (tên, version) trong config và artifact.

## 8. Tính Toàn vẹn Dữ liệu và Thời gian
- **Bảo toàn thứ tự thời gian**: Đảm bảo logs được sắp xếp tăng dần theo timestamp. Thông số:
  - `timestamp`: định dạng ISO hoặc epoch, dùng để sắp xếp log.
  - `observation_time`: thời điểm bắt đầu quan sát (ví dụ bắt đầu window).
  - `prediction_time`: thời điểm kết thúc window (thời điểm đưa ra dự đoán).
  - `anomaly_time`: thời điểm thực sự xảy ra sự cố (ground truth).
- **Chỉ dùng thông tin hiện có**: Mọi truy xuất hoặc thuật toán chỉ nhận đầu vào là thông tin đã có tại thời điểm `prediction_time`.
- **Ngăn chặn rò rỉ tương lai**:
  - Window Generator không chứa log sau `prediction_time`.
  - Retriever chỉ trả về tài liệu có `timestamp` ≤ `prediction_time`.
  - Kiểm tra dataset split chặt chẽ: training/validation/test không có overlap.
- **Tích hợp kiểm tra**: Ở mỗi bước, validate không sử dụng thông tin future. Test case kiểm tra future leakage phải có trong test suite.

## 9. Phần mềm Knowledge / Retrieval

### Knowledge
- **Ingestion**: Module `Knowledge Loader` đọc và xử lý dữ liệu tri thức (historical incidents, docs kỹ thuật). Chuẩn hóa định dạng.
- **Metadata & Version**: Gắn nhãn thời gian, phiên bản, nguồn gốc cho mỗi tài liệu tri thức.
- **Temporal validity**: Mỗi document có nhãn hiệu lực (ví dụ chỉ sử dụng trước một ngày nhất định). Quy định chỉ dùng tri thức phù hợp mốc dự đoán.

### Retrieval
- **Query**: Xây truy vấn từ ngữ cảnh hiện tại (có thể là text hoặc embedding từ log context).
- **Embedding**: Mã hóa query và corpus tri thức bằng mô hình embedding.
- **Search**: Tìm kiếm trong index (FAISS/Annoy) để lấy những vector gần nhất.
- **Ranking**: Sắp xếp kết quả theo độ tương đồng (cosine).
- **Filtering**: Loại bỏ tài liệu không phù hợp (vd. khoảng thời gian ngoài mốc, nội dung không liên quan).
- **Top-k**: Lấy `k` tài liệu hàng đầu (cấu hình `top_k`).

### Context
- **Ordering**: Sắp xếp thông tin theo tính liên quan (ví dụ: gần nhất thời gian, hoặc dựa trên score).
- **Relevance filtering**: Trong tài liệu retrieved, loại bỏ các phần không liên quan (ví dụ cắt câu).
- **Truncation**: Nếu ngữ cảnh vượt kích thước tối đa (`max_context_length` tokens), cắt bớt giữ thông tin quan trọng nhất.
- **Giới hạn context**: Đảm bảo tổng tokens không vượt giới hạn của LLM/model; hạn chế kích thước để không quá lớn.

## 10. Đặc tả Phần mềm Thực nghiệm
Thiết kế **Experiment Runner** để quản lý các kịch bản:

- **A — Baseline**: Chỉ chạy pipeline baseline; lưu metrics.
- **B — Improved**: Chạy pipeline bao gồm cải thiện; lưu metrics.
- **C — Ablation**: Tắt từng cải thiện cụ thể (ví dụ `use_llm=false` hoặc `use_retrieval=false`); chạy và so sánh.
- **D — Robustness**: (Nếu có yêu cầu) thêm biến thể như noise trong log, thay đổi độ dài, để đánh giá độ ổn định.
- **E — Efficiency**: (Nếu có) đánh giá chi phí (token, thời gian) khi cải tiến được bật.

Mỗi run ghi lại: 
- **Experiment ID**, cấu hình (config files dùng, mode, seed), phiên bản dataset/model, thời gian bắt đầu/kết thúc, metrics (raw và tổng hợp), artifacts (mô hình, plots, logs).

Artifact này cho phép tái lập chạy thử nghiệm đầy đủ.

## 11. Phần mềm Đánh giá
**Sử dụng chung protocol** đánh giá baseline và improved:

- **Phát hiện (Detection)**: 
  - *Precision*: Tỉ lệ dự đoán đúng (TP) trên tổng dự đoán dương (TP+FP). (Precision = TP/(TP+FP))
  - *Recall*: Tỉ lệ phát hiện đúng (TP) trên tổng thực sự dương (TP+FN). (Recall = TP/(TP+FN))
  - *F1-Score*: Trung bình điều hòa của precision và recall.
  - *PR-AUC*: Diện tích dưới đường cong Precision-Recall (ưu tiên khi mất cân bằng).
  - *ROC-AUC*: Diện tích dưới đường cong ROC (tùy mức phù hợp).
- **Phát hiện Sớm (Early Detection)**:
  - *Time-to-Detection (TTD)*: Thời gian từ anomaly xảy đến khi hệ thống cảnh báo.
  - *Detection Lead Time*: Thời gian cảnh báo trước khi sự cố thực sự xảy ra.
  - *Early Warning Rate*: Tỉ lệ cảnh báo đúng trước khi lỗi.
  - *Detection Before Failure*: Phần trăm lỗi được cảnh báo trước khi xảy ra.
  - *False Alarm Rate*: Tỉ lệ cảnh báo sai (FP/ tổng window).
- **Hiệu quả (Efficiency)**:
  - *Latency*: Thời gian xử lý đầu vào thành dự đoán (ms).
  - *Token Cost*: (Nếu dùng LLM) số token chi phí, hoặc ước lượng chi phí.
  - *Compute*: Thời gian CPU/GPU sử dụng (sec).
  - *Memory*: Bộ nhớ (RAM/VRAM) dùng.
  - *Throughput*: Số window hoặc log xử lý mỗi giây.

Các metrics đều được tính toán và lưu dưới dạng số (với định nghĩa rõ trong docs). Precision, recall định nghĩa theo chuẩn (tham khảo Azure Anomaly Detector).

## 12. Logging và Xử lý Lỗi
- **Logging** (cho nghiên cứu, không prod): 
  - Ghi lại log experiment (timestamp bắt đầu/kết thúc, mode, config).
  - Log hoạt động các module (ví dụ: "Loaded 1000 logs", "Model inference done", "Prompt sent to LLM").
  - Ghi metrics kết quả cuối mỗi run.
  - Log errors/exceptions (có stack trace).
  - Lưu log ở định dạng có timestamp, dễ filter (JSON hoặc text).
- **Xử lý lỗi**:
  - *Input không hợp lệ*: Dữ liệu sai format, báo lỗi rõ trước khi chạy. 
  - *Dữ liệu thiếu*: nếu mất field quan trọng (vd. timestamp), bỏ entry đó với cảnh báo hoặc dừng nếu nghiêm trọng.
  - *Retrieval failure*: nếu không lấy được tài liệu, có thể tiếp tục với context rỗng và log cảnh báo.
  - *Model failure*: NaN, divergence khi train/inference; ghi log và dừng experiment.
  - *Timeout/API limit*: khi gọi LLM quá giới hạn; catch exception, ghi log, tùy chọn retry hoặc bỏ qua run.
  - *Output không hợp lệ*: nếu parse kết quả LLM không đúng định dạng, ghi lỗi, có thể bỏ run đó.

## 13. Chiến lược Kiểm thử
- **Unit Test**:
  - *Log Parser*: test parsing với log mẫu có timestamp khác nhau, kiểm tra kết quả đầu ra.
  - *Window Generator*: test tạo window với các cấu hình khác nhau.
  - *Retriever/Context*: giả lập query và documents, kiểm tra kết quả chọn lọc.
  - *Detection & Metrics*: cho input giả, kiểm tra precision/recall đúng.
- **Integration Test**:
  - *Data → Baseline*: pipeline end-to-end với data mẫu, so sánh output với kết quả biết trước.
  - *Data → Improvement*: pipeline với improvement đơn giản (vd. retrieval trả context tĩnh).
  - *Retrieval → LLM*: test từng bước nối tiếp khi kết hợp tri thức và LLM.
  - *Model → Detection*: test kết hợp output từ model và output cải thiện.
- **End-to-End**:
  - Thực hiện một experiment run hoàn chỉnh (baseline/improved) trên tập nhỏ, đảm bảo không lỗi và output hợp lý.
- **Regression**:
  - Khi thay đổi code, chạy lại test suite và so sánh metrics với phiên bản trước (trong tolerance).
  - Kiểm tra không có thay đổi ngầm đối với baseline metrics nếu cải thiện không bật.
- **Research Validity**:
  - Sử dụng cùng data split, preprocess.
  - Cùng metric definitions.
  - Kiểm tra không future leakage (xem mục 8).
  - Đảm bảo rằng các phép tính là ổn định (ví dụ, fix seed, đủ runs).

## 14. Quản lý Artifact và Phiên bản
- **Lưu artifact** cho mỗi experiment run:
  - Cấu hình đã dùng (file YAML).
  - Phiên bản source code (git commit hash).
  - Identifier của dataset (tên file, checksum).
  - Model versions (ví dụ `baseline_v1`, `improved_v2`).
  - Prompt version (vd. `v1`).
  - Retrieval settings (embedding model, index version).
  - Metrics (raw logs, aggregated).
  - Các plots/bảng thống kê kết quả.
  - Logs chi tiết của run.
- **Version control**:
  - Code quản lý bởi Git; ghi chú tag hoặc commit cho từng milestone.
  - Dataset reference: ghi checksum hoặc tag repo chứa dataset.
  - Cấu hình baseline/improvement version (nếu lưu configs theo version).
  - Model/prompt version (lưu checkpoint với tag).
  - Kết quả experiment: mỗi run có ID cố định, không sửa sau đó.
- **Reproducibility**:
  - Không chỉnh sửa run đã lưu; nếu cần thay đổi config, tạo run mới.
  - Đảm bảo tất cả dữ liệu để chạy lại (code + config + data) đều khả dụng.

## 15. Bảo mật và Quyền riêng tư
- **API keys**: Không lưu trực tiếp trong source; sử dụng biến môi trường.
- **Quyền dữ liệu**: Giới hạn ai có thể truy cập dataset (cấu hình quyền trên hệ thống file).
- **Log nhạy cảm**: Kiểm tra và mask/redact dữ liệu nhạy cảm (PII) trong log. Ví dụ: thay địa chỉ IP, user IDs bằng placeholder.
- Không lưu secrets (key, token) trong source hay artifacts.
- **Trước khi gửi log lên LLM**: Đánh giá chứa dữ liệu nhạy cảm; nếu có, loại bỏ hoặc ẩn trước khi chèn vào prompt.

## 16. Phạm vi Triển khai

- **Bắt buộc**:
  - Chạy tại môi trường research/local (có thể trên máy có GPU).
  - Batch inference (không yêu cầu real-time thấp).
  - Sử dụng GPU cho train/inference nếu mô hình lớn.
- **Tùy chọn**:
  - Cung cấp REST API phục vụ inference đơn giản (cho demo).
  - Container hoá (Docker) để dễ tái lập môi trường.
  - Streaming prototype (nếu cần chứng minh khả thi xử lý luồng log).
- **Ngoài phạm vi**:
  - Triển khai doanh nghiệp (cluster, orchestration).
  - Multi-tenant, HA.
  - Hệ thống tự động khắc phục.
  - Chỉ làm prototype nếu hỗ trợ mục tiêu đánh giá tính khả thi.

## 17. Lộ trình Phát triển

### Mốc 1 — Môi trường
- **Mục tiêu**: Thiết lập repository, cài đặt dependency, cấu trúc thư mục, tạo config mẫu.
- **Deliverables**:
  - Repo với file `requirements.txt`, `dataset.yaml`, `baseline.yaml`.
  - Khung code trống (skeleton) cho modules (parser, model).
  - Các unit test đơn giản (e.g., parser đọc được log mẫu).
- **Acceptance**:
  - Code compile/run được; tests cơ bản pass.
  - Cấu trúc thư mục được phê duyệt.
- **Dependencies**: TDS đã approved.
- **Rủi ro**: Thiếu thư viện, xung đột môi trường.

### Mốc 2 — Baseline
- **Mục tiêu**: Triển khai đầy đủ pipeline baseline.
- **Deliverables**:
  - Data Loader, Log Parser, Window Generator.
  - Mô hình baseline (ví dụ LSTM) đã train được với data mẫu.
  - Chạy được pipeline end-to-end (train/test).
  - Đo được metrics giống tham chiếu (trong tolerance).
  - Unit/Integration tests cho baseline.
- **Acceptance**:
  - Pipeline chạy mà không lỗi trên sample data.
  - Metrics tái tạo tham chiếu trong giới hạn dung sai.
- **Dependencies**: Mốc 1.
- **Rủi ro**: Preprocessing phức tạp, thiếu data.

### Mốc 3 — Improvement
- **Mục tiêu**: Thêm các thành phần cải thiện mục tiêu.
- **Deliverables**:
  - Module knowledge/retrieval: nạp và index tri thức demo.
  - Prompt template + LLM Adapter (nếu dùng).
  - Tích hợp vào pipeline (có thể ở mức đơn giản).
  - Test nhỏ cho retrieval và LLM.
- **Acceptance**:
  - Baseline pipeline vẫn chạy khi `use_improvement=false`.
  - Với cải thiện, pipeline chạy qua (có thể dummy context).
- **Dependencies**: Mốc 2.
- **Rủi ro**: API LLM, nạp tri thức thất bại.

### Mốc 4 — Thực nghiệm chính
- **Mục tiêu**: Chạy và so sánh baseline vs improved.
- **Deliverables**:
  - Experiment Runner chạy 2 chế độ.
  - Kết quả metrics được lưu.
  - Sơ đồ so sánh (table, chart) các metric chính.
- **Acceptance**:
  - Biến kiểm soát (seed, data) không đổi giữa runs.
  - Thu thập đủ metrics đã định.
  - Thực hiện số run đúng config (`runs`).
- **Dependencies**: Mốc 2,3.
- **Rủi ro**: Thời gian train lâu, lỗi runtime.

### Mốc 5 — Ablation/Robustness
- **Mục tiêu**: Phân tích các thành phần cải thiện và độ ổn định.
- **Deliverables**:
  - Các runs ablation (tắt retrieval hoặc LLM).
  - Thêm thử nghiệm robustness (ví dụ: tăng noise).
  - Báo cáo sơ bộ cho từng biến thể.
- **Acceptance**:
  - Hoàn thành các kịch bản thêm.
  - Hiểu được tác động của từng thành phần cải thiện.
- **Dependencies**: Mốc 4.
- **Rủi ro**: Số lượng run nhiều, tốn tài nguyên.

### Mốc 6 — Artifact cuối
- **Mục tiêu**: Hoàn thiện kết quả và tài liệu.
- **Deliverables**:
  - Kết quả cuối cùng (mean/std) cho baseline & improved.
  - Lưu tất cả artifact (metrics, plots, logs).
  - SDS hoàn chỉnh và hướng dẫn reproducibility.
  - Tài liệu báo cáo (bảng, hình).
- **Acceptance**:
  - Kết quả reproducible (chạy lại thu được kết quả tương tự).
  - Documentation rõ ràng đầy đủ.
- **Dependencies**: Các mốc trước.
- **Rủi ro**: Giới hạn thời gian, lỗi chưa khắc phục kịp.

## 18. Tiêu chí Chấp nhận

- **Baseline**: Chạy end-to-end không lỗi; metrics tham chiếu được tái tạo trong tolerance định trước.
- **Improvement**: Chạy độc lập (improved) không lỗi; giao diện bật/tắt rõ; khi tắt cải tiến, kết quả baseline không đổi ngoài dự kiến.
- **Thực nghiệm chính**: Biến kiểm soát cố định; đã thu thập đủ metrics; số lần run hoàn thành.
- **Artifact**: Cấu hình và phiên bản được lưu; kết quả có thể truy vết (traceability đến code/data).

## 19. Ma trận Truy vết

| Research Element | TDS Element                 | Software Module        | Experiment           | Metric             |
|------------------|-----------------------------|------------------------|----------------------|--------------------|
| RQ1              | (định nghĩa trong result-6) | Baseline Pipeline      | Experiment A (Baseline)| Precision, Recall |
| RQ2              | (định nghĩa trong result-6) | Improved Pipeline      | Experiment B (Improved)| Lead Time, F1     |
| RQ3              | (định nghĩa trong result-6) | Ablation Studies       | Experiment C (Ablation) | EWR, FAR          |
| H1               | (TDS)                       | Baseline vs Improved   | A vs B               | (theo H1)          |
| H2               | (TDS)                       | (tương ứng)            | B vs C               | (theo H2)          |
| H3               | (TDS)                       | (tương ứng)            | C vs D/E            | (theo H3)          |

*Bảng trên minh họa sự liên kết giữa câu hỏi nghiên cứu/hypotheses với thành phần TDS, module phần mềm, experiment và metric tương ứng.*

## 20. Chốt Thiết kế Phần mềm
- **Baseline 2025–2026**: Được giữ nguyên như định nghĩa ban đầu (nằm trong `baseline/`).
- **Cải thiện mục tiêu**: Tích hợp thêm các module truy xuất tri thức và/hoặc LLM (nằm trong `improvement/`, `knowledge/`, `retrieval/`, `prompts/`).
- **Các phần giữ nguyên**: Dữ liệu gốc, pipeline baseline, protocol đánh giá, experiment runner.
- **Các phần thêm/sửa**: Module knowledge/retrieval, prompt builder, context builder, cấu hình bật/tắt cải tiến.
- **Chế độ experiment**: `baseline`, `improved`, `ablation` được thực thi qua Experiment Runner.
- **Artifacts**: Lưu đầy đủ input, config, model, output, logs để có thể tái lập (reproducible).

Thiết kế này rõ ràng phân biệt baseline và improved, đảm bảo so sánh công bằng, đồng thời lưu giữ artifact cần thiết để kết quả nghiên cứu có thể tái lập được.