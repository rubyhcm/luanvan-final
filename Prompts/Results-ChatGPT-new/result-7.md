# Đặc tả Thiết kế Phần mềm

## 1. Kiểm tra Design Freeze

| Thành phần            | Định nghĩa đã phê duyệt (TDS)                                                                                            | Q1/Q2 & Publication Check                                                                                               | Diễn giải ở mức phần mềm                                                                                    |
|----------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| **Baseline**         | Baseline là framework LogSentry, dùng học đối lập (contrastive learning) kết hợp với phương pháp tăng cường truy xuất (KNN Retrieval). | Journal: *Scientific Reports*, 2025, official peer-reviewed, DOI 10.1038/s41598-025-22208-7. Journal Sci Rep thuộc Multidisciplinary Sciences, top 15% (Q1).    | Cài đặt LogSentry theo đúng mô tả: mô hình BERT huấn luyện đối lập, kết hợp đầu ra KNN cho dự đoán. Không thay đổi thuật toán gốc. |
| **Hạn chế**          | Như đã xác định trong TDS, baseline chỉ sử dụng ngưỡng tĩnh (từ đầu vào huấn luyện) và chỉ truy xuất log lịch sử gần nhất; thiếu ngữ cảnh rộng và khả năng giải thích. | –                                                                                                                      | Baseline hiện tại không khai thác tri thức bên ngoài và không có cơ chế cảnh báo sớm ngoài điểm bất thường. Cần giữ nguyên như TDS mô tả. |
| **Cải thiện có mục tiêu** | Cải thiện đề xuất là bổ sung các thành phần RAG/LLM để tăng khả năng phát hiện sớm và giải thích (theo TDS). Không làm thay đổi định nghĩa metric. | –                                                                                                                      | Thêm module thu thập tri thức và LLM: truy xuất bối cảnh lịch sử hoặc tài liệu, chèn vào prompt, dùng LLM dự đoán. Đảm bảo baseline không bị can thiệp. |
| **Thực nghiệm chính**| So sánh kiểm soát giữa baseline và phiên bản cải thiện (chạy lặp lại).                                                         | –                                                                                                                      | Thực hiện quy trình chạy độc lập cho cả hai chế độ baseline/improved, cùng seed, cùng tập dữ liệu, lưu đầy đủ thông số.    |
| **Metric chính**     | Dựa trên TDS: F1-score phát hiện dị thường, và thời gian dẫn đầu phát hiện (lead time).                                         | –                                                                                                                      | Tính toán chỉ số F1 (precision/recall) cho phát hiện và thời gian phát hiện sớm trung bình.                         |

_Nếu phát hiện mâu thuẫn với result-6.md, sẽ báo cáo và không tự ý sửa đổi TDS; ở trên giữ nguyên định nghĩa baseline và cải thiện theo TDS._

## 2. Phạm vi Phần mềm

**Trong phạm vi:** Triển khai tối thiểu các thành phần để chạy đầy đủ baseline và cải thiện đã xác định, bao gồm:  
- **Chạy baseline:** tải dữ liệu, tiền xử lý, mô hình gốc LogSentry, dự đoán dị thường.  
- **Chạy cải thiện có mục tiêu:** sau khi có dự đoán baseline, thêm thành phần truy xuất tri thức và LLM theo thiết kế.  
- **So sánh kiểm soát:** chạy hai chế độ baseline vs improved trên cùng điều kiện.  
- **Thực nghiệm Ablation:** biến đổi bộ phận cải thiện (ví dụ tắt LLM hoặc thay đổi tham số) để đánh giá hiệu quả từng thành phần.  
- **Đánh giá Phát hiện Sớm:** tính toán các chỉ số phát hiện (F1, precision, recall) và chỉ số phát hiện sớm (thời gian dẫn đầu, tỷ lệ cảnh báo sớm, v.v.).  
- **Lưu artifact thực nghiệm:** cấu hình, mô hình, kết quả, log.

**Ngoài phạm vi:** Các thành phần không cần thiết cho nghiên cứu và khả năng tái lập, bao gồm:  
- **Triển khai production quy mô lớn:** hệ thống tự động đa người dùng, HA, v.v.  
- **Phát triển giao diện người dùng phức tạp hoặc dịch vụ API công nghiệp:** chỉ cần prototype nếu hỗ trợ đánh giá.  
- **Bất kỳ tác vụ không theo TDS đã phê duyệt:** không tìm thêm paper hay đổi câu hỏi, không mở rộng sang AIOps sản xuất.  

_Trong thiết kế này, phần mềm tập trung vào **nghiên cứu minh bạch và có thể tái lập** với các thành phần tối thiểu theo yêu cầu._  

## 3. Kiến trúc Mã nguồn

Đề xuất cấu trúc thư mục tối giản, phân biệt rõ các thành phần như sau:

```
project/
├── configs/         # Cấu hình (YAML) của dataset, baseline, improvement, model, retrieval, evaluation, experiment
├── data/            # Tập dữ liệu (raw, parsed, windowed)
├── baseline/        # Cài đặt thuật toán baseline (LogSentry)
├── improvement/     # Cài đặt thành phần cải thiện (LLM, RAG)
├── knowledge/       # (nếu cần) Tài nguyên tri thức tĩnh (tài liệu, logs cũ)
├── retrieval/       # Mã cho truy xuất ngữ cảnh (vector index, embedding)
├── models/          # Định nghĩa mô hình (mạng nơ-ron, BERT, v.v.)
├── prompts/         # Mẫu prompt cho LLM (task prompt, system prompt, v.v.)
├── detection/       # Kết hợp dự đoán (kết quả anomaly) từ baseline và cải thiện
├── evaluation/      # Tính toán metric và so sánh kết quả
├── experiments/     # Tập lệnh chạy (runner) cho các chế độ và cấu hình
├── tests/           # Kiểm thử (unit, tích hợp, end-to-end)
├── artifacts/       # Lưu trữ kết quả, đồ thị, báo cáo
└── docs/            # Tài liệu kỹ thuật (README, hướng dẫn sử dụng)
```

Với mỗi module/thư mục:

- **configs/**: Chịu trách nhiệm nạp và xác thực cấu hình (định dạng YAML). Đầu vào: file cấu hình. Đầu ra: đối tượng cấu hình Python. Phụ thuộc: thư viện đọc YAML (PyYAML). Trạng thái: *New*.
- **data/**: Quản lý dữ liệu thô và tiền xử lý. Đầu vào: file log gốc. Đầu ra: dữ liệu đã parsed và chia theo cửa sổ. Phụ thuộc: utils parsing. Trạng thái: *New*.
- **baseline/**: Cài đặt thuật toán LogSentry từ TDS. Đầu vào: dữ liệu sau tiền xử lý (cửa sổ log). Đầu ra: điểm anomaly (score) hoặc nhãn. Phụ thuộc: thư viện ML (PyTorch/TensorFlow), BERT embedding. Trạng thái: *New* (theo thiết kế gốc).
- **improvement/**: Chứa các thành phần cải thiện mục tiêu (LLM, RAG). Đầu vào: dữ liệu hiện tại, ngữ cảnh từ retrieval. Đầu ra: thông tin bổ sung (ví dụ: nhãn anomaly, giải thích). Phụ thuộc: modules `retrieval/`, `prompts/`, adapter LLM. Trạng thái: *New*.
- **knowledge/**: (Optional) Lưu trữ tài liệu tri thức (hướng dẫn, codelog, bài viết). Đầu vào: các nguồn tri thức. Đầu ra: văn bản đã indexing. Trạng thái: *New*.
- **retrieval/**: Xây dựng và truy vấn vector index cho knowledge hoặc lịch sử log. Đầu vào: văn bản tri thức/log lịch sử. Đầu ra: danh sách các mục liên quan (top-k). Phụ thuộc: thư viện embedding (ví dụ SentenceTransformers), faiss hoặc ElasticSearch. Trạng thái: *New*.
- **models/**: Định nghĩa kiến trúc mạng, mô hình embedding. Đầu vào: cấu hình mô hình. Đầu ra: đối tượng mô hình đã huấn luyện/định nghĩa. Trạng thái: *New*.
- **prompts/**: Tổ chức các mẫu prompt (system, user, template). Đầu vào: cấu hình prompt. Đầu ra: văn bản prompt hoàn chỉnh. Trạng thái: *New*.
- **detection/**: Kết hợp đầu ra từ baseline và cải thiện thành dự đoán cuối. Đầu vào: anomaly scores (baseline), kết quả LLM. Đầu ra: nhãn anomaly chung. Trạng thái: *New*.
- **evaluation/**: Tính toán metric (Precision, Recall, F1, TTD, v.v.). Đầu vào: dự đoán và ground truth. Đầu ra: báo cáo metric. Trạng thái: *New*.
- **experiments/**: Script thực nghiệm (runner) điều phối các chế độ (baseline/improved/ablation). Đầu vào: cấu hình experiment. Đầu ra: artifact kết quả (logs, metrics). Trạng thái: *New*.
- **tests/**: Kiểm thử tự động. Bao gồm unit test cho parser, windowing, retrieval, context, scoring, metric. Trạng thái: *New*.
- **artifacts/**: Lưu các kết quả thô (metrics, biểu đồ, logs) của mỗi thử nghiệm. Trạng thái: *New*.
- **docs/**: Tài liệu hướng dẫn, mô tả kiến trúc. Trạng thái: *New*.

Tách riêng rõ ràng phần **cài đặt baseline** (trong `baseline/`) và **cải thiện** (`improvement/` và liên quan), cũng như **đánh giá** (`evaluation/`). Không có circular dependency giữa các module.  

## 4. Đặc tả Module và Interface

Bảng sau liệt kê các module chính và giao diện giữa chúng:

| Module            | Trách nhiệm                                                       | Đầu vào                                   | Đầu ra                                  | Phụ thuộc                  | Trạng thái       |
|-------------------|--------------------------------------------------------------------|-------------------------------------------|-----------------------------------------|----------------------------|------------------|
| **DataLoader/Parser**  | Tải và chuyển đổi log thô thành danh sách sự kiện (timestamp, template, params) | Raw log line (string), timestamp           | Mảng sự kiện: {timestamp, template, params} | Biểu thức regex, config   | New              |
| **WindowGenerator**    | Gom nhóm sự kiện thành các cửa sổ thời gian (fixed window hoặc sliding) | Mảng sự kiện đã parse                      | Danh sách cửa sổ: mỗi cửa sổ = tập sự kiện  | DataLoader                 | New              |
| **Representation**     | Mã hóa mỗi cửa sổ log thành vector số (đặc trưng)     | Cửa sổ log (chuỗi hoặc danh sách messages) | Vector embedding (numpy array)           | Pre-trained BERT model     | New              |
| **BaselineDetector**   | Tính anomaly score hoặc nhãn dựa trên mô hình contrastive learning | Vector embedding của cửa sổ               | Điểm anomaly hoặc nhãn (anomaly/normal) | weights của mô hình         | New (Inherited)  |
| **Retriever**         | Tìm kiếm các log hoặc tri thức liên quan (top-k)     | Context hiện tại (chuỗi log gần nhất)      | Đầu vào ngữ cảnh: list các log/trích dẫn liên quan | Index tri thức/log, embedding model | New      |
| **PromptBuilder**    | Xây dựng prompt cho LLM từ log hiện tại và ngữ cảnh    | Log hiện tại, ngữ cảnh retrieved           | Prompt text (string)                     | Templates trong `prompts` | New              |
| **LLMAdapter**       | Gọi API LLM (ví dụ GPT-4) để dự đoán anomaly             | Prompt text                               | Kết quả thô từ LLM (text/JSON)           | API LLM (OpenAI/HuggingFace) | New            |
| **OutputParser**     | Trích xuất kết quả anomaly từ output của LLM             | Kết quả thô LLM (text hoặc JSON)           | Nhãn anomaly, độ tin cậy (float)         | -                          | New              |
| **EarlyDetectionEvaluator** | Tính toán chỉ số phát hiện sớm (lead time, EWR, False Alarm Rate, v.v.) | Dự đoán anomaly với timestamp, ground truth | Metrics báo cáo (F1, Time-to-Detection, EWR, v.v.) | -                        | New              |

Luồng giao diện chính giữa các module:

```text
Raw Log → DataLoader/Parser → WindowGenerator → Representation → BaselineDetector → Prediction
                                            ↘ Improvement (Retriever + LLM)
Prediction → EarlyDetectionEvaluator
```

Trong đó, nếu có thành phần RAG: 

```text
Current Log (Context) → Retriever → PromptBuilder → LLMAdapter → OutputParser → Prediction
```

**Ví dụ chi tiết giao diện:**  
- **Log Parser → WindowGenerator:** đầu vào là danh sách sự kiện (kèm timestamp, template) do Log Parser sinh ra; đầu ra là danh sách các cửa sổ (mỗi cửa sổ là tập sự kiện liền kề). Phải bảo toàn thứ tự thời gian. Yêu cầu trường `timestamp` hợp lệ; lỗi nếu log không parse được.  
- **WindowGenerator → Representation:** đầu vào là một cửa sổ (tập các sự kiện); đầu ra là vector đặc trưng (có thể có độ dài cố định). Trường đầu vào bắt buộc: `events[]` không rỗng; lỗi nếu cửa sổ trống.  
- **PromptBuilder → LLMAdapter:** đầu vào prompt text (kết hợp log hiện tại + ngữ cảnh); đầu ra là JSON/chuỗi chứa nhãn anomaly và giải thích. Đảm bảo schema: ví dụ `{ "anomaly": bool, "explanation": string }`. Nếu LLM trả về format không đúng, OutputParser sẽ phát hiện lỗi và ghi log.  

Mỗi interface nêu rõ mục đích, định dạng dữ liệu đầu vào/ra, các trường bắt buộc, và cách xử lý lỗi (ví dụ trường bị thiếu hoặc giá trị ngoài phạm vi đều phải bắt ngoại lệ và ghi log cảnh báo). Thiết kế tránh circular dependency (các module chỉ phụ thuộc theo hướng tuyến tính hoặc star pattern).

## 5. Tách biệt Baseline và Cải thiện

Baseline (LogSentry) được triển khai độc lập, không phụ thuộc vào thành phần cải thiện. Ba chế độ chính của phần mềm:

- **Baseline mode:** Chạy thuật toán LogSentry thuần túy.  
- **Improved mode:** Chạy baseline và bổ sung các bước cải thiện (retrieval + LLM) để tinh chỉnh kết quả.  
- **Ablation mode:** Chạy baseline với loại bỏ (disable) một hoặc các thành phần cải thiện (ví dụ, không sử dụng LLM hoặc sử dụng fewer context) để phân tích tác động từng thành phần.  

Trong chế độ improved, không thay đổi định nghĩa metric hay cấu trúc baseline ban đầu. Các tham số cải thiện có thể bật/tắt qua cấu hình (e.g. `use_llm: true/false`). Cải thiện chỉ ảnh hưởng thêm ngữ cảnh hoặc lý giải, không thay đổi tiêu chí đánh giá lỗi bất thường so với baseline.

## 6. Đặc tả Cấu hình

Sử dụng file YAML cho từng nhóm cấu hình, ví dụ: `dataset.yaml`, `baseline.yaml`, `improvement.yaml`, `model.yaml`, `retrieval.yaml`, `evaluation.yaml`, `experiment.yaml`. Mỗi trường gồm kiểu, giá trị mặc định, miền hợp lệ, mô tả, và trạng thái cố định/điều chỉnh:

- **dataset.yaml**  
  - `name` (string, *bắt buộc*): tên dataset. Mặc định: `"BGL"`. *Status*: fixed.  
  - `data_path` (string, *bắt buộc*): đường dẫn tới file log.  
  - `window_size` (int, default=10): độ dài cửa sổ (số sự kiện). Miền: [1, 100]. *Status*: tunable.  
  - `window_step` (int, default=5): bước trượt của cửa sổ. Miền: [1, window_size]. *Status*: tunable.  

- **baseline.yaml**  
  - `representation_model` (string, default="bert-base-uncased"): mô hình embedding. Miền: danh sách model được hỗ trợ. *Status*: fixed.  
  - `contrastive_temp` (float, default=0.5): hệ số nhiệt độ trong loss contrastive. Miền: (0,1]. *Status*: tunable.  
  - `detection_threshold` (float, default=0.8): ngưỡng phân loại anomaly. Miền: [0,1]. *Status*: tunable.  

- **improvement.yaml**  
  - `use_llm` (bool, default=false): bật sử dụng LLM. *Status*: fixed (để bật/tắt cải thiện).  
  - `llm_model` (string, default="gpt-4"): phiên bản LLM sử dụng. *Status*: fixed.  
  - `retrieve_k` (int, default=5): số log/tri thức lấy về (top-k). Miền: [0, 20]. *Status*: tunable.  
  - `include_corpus_knowledge` (bool, default=true): có dùng tri thức tập đoàn hay không.  

- **model.yaml** (cấu hình chung mô hình)  
  - `batch_size` (int, default=32): kích thước batch. *Status*: tunable.  
  - `learning_rate` (float, default=1e-4): tốc độ học. Miền: (0,1). *Status*: tunable.  
  - `epochs` (int, default=10): số epoch huấn luyện. *Status*: tunable.  

- **retrieval.yaml**  
  - `embedding_model` (string, default="all-MiniLM-L6-v2"): mô hình embedding dùng cho tìm kiếm. *Status*: fixed.  
  - `knowledge_base_path` (string): đường dẫn tới tri thức (đã index). *Status*: fixed.  
  - `top_k` (int, default=5): số kết quả trả về. *Status*: tunable.  

- **evaluation.yaml**  
  - `metrics` (list, default=["precision","recall","f1","ttd","lead_time"]): danh sách chỉ số đánh giá. *Status*: fixed.  
  - `early_warning_window` (int, default=30): ngưỡng thời gian (phút/giây) để tính cảnh báo sớm. *Status*: fixed.  

- **experiment.yaml**  
  - `seed` (int, default=42): giá trị seed cho ngẫu nhiên. *Status*: fixed.  
  - `runs` (int, default=3): số lần lặp thử nghiệm. *Status*: fixed.  
  - `mode` (string, default="baseline"): chế độ chạy (`baseline`, `improved`, `ablation`). *Status*: tunable.  

Các tham số **cố định (fixed)** như tên mô hình, sử dụng LLM hay không, đường dẫn dữ liệu không đổi trong toàn bộ thử nghiệm. Tham số **điều chỉnh (tunable)** như batch size, learning rate, threshold có thể hiệu chỉnh dựa trên tập validation. Tham số **thí nghiệm** (như `seed`, `runs`, `mode`) để lập lịch chạy và lưu kết quả.

## 7. Thiết kế LLM / Prompt / Model

**Prompt/system design:**  
- **System Prompt (task prompt):** Ví dụ: `"You are a log anomaly detection expert. Given a log entry and context, determine if it's anomalous."` (định nghĩa nhiệm vụ).  
- **User Prompt (in-context):** Chèn log hiện tại và các ví dụ/giải thích thu thập (ví dụ format: **Input:** `<log_current>`; **Context:** `<retrieved_logs>`).  
- **Output Schema:** Yêu cầu LLM trả về JSON với các trường: `{"anomaly": <true/false>, "confidence": <float>, "explanation": "<reason>"}`. Bằng cách này, `OutputParser` có thể phân tích và trích xuất kết quả.  

**Phiên bản Prompt/Model:** Ghi rõ phiên bản prompt (có thể kèm timestamp hoặc định danh) và model LLM (ví dụ GPT-4, GPT-3.5, Llama2). Cả baseline và improved nên sử dụng cùng phiên bản LLM nếu baseline yêu cầu (nhưng trong bản TDS, baseline không dùng LLM; chỉ improved dùng).  
**Temperature/Sampling:** Đặt temperature=0 (đã tinh chỉnh) để đầu ra định lượng nhất quán.  

**Model Interface:** Định nghĩa một lớp `LLMAdapter` chung để gọi API của nhà cung cấp LLM (Ví dụ: `call_llm(prompt)`). Ranh giới rõ ràng giữa phần code của dự án và provider (ví dụ một adapter cho OpenAI). Ghi metadata phiên bản của model (ID API, hash, v.v.) trong `experiment.yaml`.  

Nếu dùng Foundation Model:  
- Input của LLM: JSON `{ "log": "...", "context": "..." }` hoặc bản văn bản tóm tắt.  
- Output: JSON/nhãn như trên.  
- Giao diện độc lập với provider (đảm bảo thay model/provider bằng cách thay adapter).

## 8. Tính Toàn vẹn Dữ liệu và Thời gian

Phần mềm **luôn bảo toàn thứ tự thời gian** của log. Mỗi bản ghi log gồm trường `timestamp` (định dạng ISO 8601), nội dung sự kiện, mã template, v.v. Khi tạo cửa sổ, đảm bảo thứ tự tăng dần theo timestamp. Định nghĩa các thời điểm quan trọng:
- **Timestamp:** thời điểm ghi log thực.  
- **Observation time:** thời điểm cửa sổ log được hình thành (cuối cửa sổ).  
- **Prediction time:** thời điểm đưa ra dự đoán (có thể ngay sau cửa sổ).  
- **Anomaly time (failure):** thời điểm sự cố/anomaly thực xảy ra (ground truth).  

Khi dùng Retrieval/Memory: TUYỆT ĐỐI chỉ sử dụng thông tin có trước thời điểm dự đoán (prediction time). Cần ngăn chặn:
- Rò rỉ log tương lai: không lấy nội dung log sau prediction time.  
- Rò rỉ sự cố tương lai: nếu có sự cố (failure) sau prediction time, không dùng thông tin đó.  
- Rò rỉ thông tin test: không dùng GT để tạo context.  

Ví dụ: Nếu dự đoán tại time T, chỉ được phép truy xuất log và tri thức <= T. Việc sắp xếp ngữ cảnh theo thời gian (gần đây nhất trước prediction) giúp đảm bảo tính hợp lệ. Có thể gắn tag phiên bản dữ liệu (versioning) cho tri thức tại thời điểm xử lý.

## 9. Phần mềm Knowledge / Retrieval

- **Knowledge:** Thành phần *ingestion* tải các nguồn tri thức liên quan (tài liệu hệ thống, code logs, report). Lưu metadata như nguồn gốc, timestamp cập nhật cuối cùng. Phiên bản (version) của tri thức phải được lưu (ví dụ commit hash của dataset tri thức). Bảo đảm tính **valid thời gian** của tri thức (ví dụ tri thức từ tháng 1/2025 chỉ được dùng cho dự đoán sau ngày đó).  

- **Retrieval:**  
  - **Query:** Xây dựng truy vấn (query) từ ngữ cảnh hiện tại (ví dụ log hiện tại hoặc tóm tắt).  
  - **Embedding:** Sử dụng mô hình embedding (như SBERT) để chuyển văn bản (log/thuật toán) thành vector.  
  - **Search:** Tìm kiếm trong chỉ mục (vector index) dựa trên truy vấn.  
  - **Ranking:** Sắp xếp kết quả theo độ tương đồng (cosine, dot).  
  - **Filtering:** Lọc theo ngữ cảnh (chỉ giữ log cùng loại hoặc không vượt quá giới hạn token).  
  - **Top-K:** Lấy K kết quả hàng đầu (tham số `top_k`).  

- **Context Construction:**  
  - **Ordering:** Xếp kết quả truy xuất theo thời gian hoặc độ tương đồng ưu tiên.  
  - **Relevance Filtering:** Loại bỏ kết quả không phù hợp (theo domain tri thức).  
  - **Truncation:** Ghép các đoạn truy xuất vào prompt, cắt ngắn nếu vượt giới hạn model (token limit).  
  - **Context Limit:** Giới hạn tổng độ dài ngữ cảnh để đảm bảo LLM xử lý được.  

Mục tiêu là trích xuất **tri thức sẵn có** phù hợp nhất tại thời điểm dự đoán, không dùng dữ liệu từ tương lai. Có thể cập nhật chu kỳ index (phiên bản) nếu nguồn tri thức thay đổi.

## 10. Đặc tả Phần mềm Thực nghiệm

Xây dựng `ExperimentRunner` để tự động hoá các chế độ sau:

- **A — Baseline Run:** Chạy thuần baseline với cấu hình chỉ định (không bật LLM). Ghi lại kết quả và metric baseline.  
- **B — Improved Run:** Chạy baseline kèm cải thiện (LLM + retrieval). Cùng cấu hình khác biệt với Bật LLM. Ghi kết quả improved.  
- **C — Ablation:** Thay đổi hoặc tắt thành phần cải thiện (ví dụ set `use_llm=false` nhưng vẫn loader retrieval) để đánh giá tác động.  
- **D — Robustness (nếu cần):** Kiểm thử thêm (ví dụ thêm noise, thay phân phối logs) – thực hiện nếu được xác định trong RQ.  
- **E — Efficiency (nếu cần):** Thử nghiệm đánh giá chi phí (latency, token usage) – nếu cải thiện trade-off tài nguyên.  

Mỗi lần chạy cần lưu (artifact):  
- ID thử nghiệm (timestamp).  
- Phiên bản code (git commit), cấu hình dùng (toàn bộ YAML).  
- Phiên bản dataset (commit hoặc hash).  
- Phiên bản model/LLM.  
- Giá trị seed.  
- Kết quả metrics.  
- Artifact đầu ra (log, bảng kết quả, hình).

Người dùng có thể kích hoạt các chế độ chạy qua cấu hình experiment. Kết quả mỗi chế độ được gắn tag rõ ràng (A, B, C, ...).

## 11. Phần mềm Đánh giá

Sử dụng cùng giao thức đánh giá cho baseline và improved. Các chỉ số chính:

- **Đánh giá phát hiện (Detection):** Precision, Recall, F1-score, Area under PR curve (PR-AUC), ROC-AUC (nếu phù hợp).  
- **Đánh giá sớm (Early Detection):**  
  - *Time-to-Detection:* thời gian trung bình từ anomaly xảy ra đến khi dự đoán.  
  - *Detection Lead Time:* thời gian dự đoán trước anomaly thực (bằng TTD nếu tính ngược).  
  - *Early Warning Rate:* tỷ lệ anomaly được phát hiện trước khi xảy ra.  
  - *Detection Before Failure:* số anomaly được dự đoán trước failure thời điểm.  
  - *False Alarm Rate:* tỷ lệ dương tính giả/trên tổng cảnh báo.  

- **Đánh giá hiệu quả (Efficiency):** nếu cần đánh giá cải thiện có ảnh hưởng:  
  - *Latency:* thời gian inference mỗi cửa sổ.  
  - *Token cost:* số token mỗi prompt (nếu dùng LLM API).  
  - *Compute & memory:* sử dụng GPU/CPU (Giờ/GPU, RAM).  
  - *Throughput:* số log/cửa sổ xử lý trên giây.

Các metric được tính từ đầu ra của `EarlyDetectionEvaluator`. Kết quả so sánh baseline vs improved phải được thu thập và lưu vào reports.

## 12. Logging và Xử lý Lỗi

**Logging:** Phục vụ mục đích nghiên cứu (không giống observability production).  
- Ghi log thử nghiệm: bao gồm timestamp bắt đầu/kết thúc, ID experiment, seed, tham số cấu hình.  
- Ghi log module: thông tin gọi API LLM, vector search, trạng thái training, v.v.  
- Ghi log lỗi: bất kỳ ngoại lệ hoặc sự cố nào.  
- Ghi kết quả trung gian: theo bước (ví dụ anomaly score, top-k retrieved, output LLM).  
- Ghi metric cuối: lưu tổng hợp Precision, Recall, TTD... để truy vết.  

**Xử lý lỗi:**  
- *Input không hợp lệ:* nếu cấu hình thiếu trường bắt buộc hoặc định dạng sai, dừng chạy và báo lỗi.  
- *Dữ liệu thiếu/hỏng:* kiểm tra chất lượng dữ liệu (ví dụ cửa sổ rỗng). Nếu có log rỗng, ghi cảnh báo.  
- *Retrieval failure:* nếu không có kết quả (empty top-k), vẫn tiếp tục với context trống, ghi log cảnh báo.  
- *Model failure:* nếu gọi LLM bị lỗi (timeout, rate limit), có thể thử lại vài lần. Nếu hết retry, ghi lỗi và bỏ trường hợp đó.  
- *Timeout/Rate limit:* cấu hình timeout cho API LLM, bắt và log timeout.  
- *Output invalid:* nếu LLM trả về định dạng không parse được, ghi log và đếm như lỗi.  

Tất cả lỗi và cảnh báo phải được ghi log có timestamp. Hệ thống thử nghiệm nên có cơ chế dừng an toàn khi gặp lỗi nghiêm trọng và chuyển sang thử nghiệm tiếp theo.

## 13. Chiến lược Kiểm thử

- **Unit Test:**  
  - Parser: đầu vào mẫu log đã biết, kiểm tra output event đúng.  
  - Windowing: đảm bảo chia chính xác các cửa sổ theo cấu hình.  
  - Retrieval: cho query mẫu, đảm bảo thu được kết quả mong đợi và xử lý trường hợp empty.  
  - Prompt/Output: cho đầu vào mẫu, kiểm tra prompt dựng và parse đúng.  
  - Metrics: tính toán F1, TTD đúng với input giả lập.  

- **Integration Test:**  
  - Liên kết Parser→Window→Representation→Baseline: đầu ra anomaly score hợp lý cho tập mẫu.  
  - Liên kết Retrieval→LLM: đảm bảo khi bật cải thiện, pipeline có thể chạy qua LLM mà không lỗi.  
  - Kiểm thử kết hợp: ví dụ chạy qua một loạt log, chạy cả baseline và improved để so sánh sơ bộ.  

- **End-to-End Test:** Một chạy thực nghiệm hoàn chỉnh từ đầu (tải log) đến cuối (metrics) với tập dữ liệu nhỏ, cả hai chế độ baseline/improved. Đầu ra final phải giống cấu hình mong đợi.

- **Regression Test:** Khi cập nhật code, test lại baseline pipeline (với seed cố định) để đảm bảo kết quả metrics không thay đổi ngoài phạm vi dung sai cho phép.  

- **Research Validity Checks:**  
  - Đảm bảo sử dụng cùng tập train/test (no data leakage).  
  - Xử lý dữ liệu, tiền xử lý giống hệt giữa các lần thử.  
  - Tính toàn vẹn thời gian (chronology) được kiểm tra tự động (log must be sorted).  
  - Không có future leak: unit test đảm bảo không sử dụng thông tin `timestamp` vượt quá thời điểm hiện tại.  

Bộ kiểm thử nên được tích hợp CI/CD để tự động chạy trước mỗi merge vào nhánh chính.

## 14. Quản lý Artifact và Phiên bản

Mỗi thử nghiệm (run) phải lưu đầy đủ thông tin để tái lập:  
- **Cấu hình:** toàn bộ file YAML (dataset, model, baseline, improvement).  
- **Phiên bản source code:** commit hash của repo chính.  
- **Dataset identifier:** tên và phiên bản (hoặc hash) của tập dữ liệu.  
- **Model/LLM phiên bản:** nếu dùng model huấn luyện sẵn, ghi version; nếu dùng LLM, ghi model ID.  
- **Prompt version:** nội dung prompt hoặc metadata.  
- **Retrieval settings:** embed model và top-k.  
- **Metrics (raw/aggregated):** Precision, Recall, F1, lead time, EWR, FAR, latency…  
- **Plots/Tables:** biểu đồ ROC/PR, bảng kết quả.  
- **Logs:** toàn bộ logs (training, inference, error).  

Phiên bản hoá:  
- Source code và configs trên Git (có tag/version release cho SDS).  
- Dataset được tham chiếu qua commit hoặc ID nguồn (nếu có).  
- Model/prompt cũng version (ví dụ config cho model).  
- Kết quả thử nghiệm: lưu theo thư mục `artifacts/` với tên bao gồm ID run.  

Không được sửa các kết quả thử nghiệm đã freeze; nếu thay đổi code, tạo run mới với ID khác. Mọi artifact đều phải truy vết được trở lại code và cấu hình đã dùng.

## 15. Bảo mật và Quyền riêng tư

- **API secrets:** Không lưu khóa API (OpenAI, v.v.) trong mã nguồn. Sử dụng biến môi trường hoặc file .env được ignore.  
- **Quyền dataset:** Nếu dữ liệu log nhạy cảm, kiểm soát quyền truy cập (chỉ nhóm nghiên cứu).  
- **Thông tin nhạy cảm trong log:** Có thể thực hiện mask/redaction (ví dụ token IP, user) trước khi đưa vào LLM.  
- **Privacy for LLM:** Trước khi gửi log thật lên LLM, kiểm tra xem có thông tin nhạy cảm (PII) không. Nếu có, loại bỏ hoặc ẩn.  
- Không lưu thông tin bí mật trong logs/đầu ra (passwords, keys).  

Nếu dùng LLM bên ngoài, đánh giá rủi ro bảo mật (ví dụ terms of service về dữ liệu). Logging chỉ nên lưu hash hoặc mã hóa nếu có PII.

## 16. Phạm vi Triển khai

- **Bắt buộc:** Môi trường cục bộ/nhóm nghiên cứu (laptop/cluster), batch inference. Dùng GPU nếu cần (cho training BERT).  
- **Tùy chọn:**  
  - Triển khai REST API cho prototyping (ví dụ flask) để thử nghiệm gọi dịch vụ.  
  - Docker container hóa toàn bộ project để đảm bảo reproducibility môi trường.  
  - Prototype streaming (nhưng chỉ nếu phục vụ kiểm thử tính khả thi).  
- **Ngoài phạm vi:**  
  - Orchestration doanh nghiệp, multi-tenant, high-availability.  
  - Hệ thống tự động khắc phục (remediation) tại doanh nghiệp.  

Chỉ xây dựng prototype deployment nếu thực sự cần cho đánh giá hiệu suất hoặc khả thi nghiên cứu.

## 17. Lộ trình Phát triển

- **Mốc 1 — Môi trường:** Thiết lập repository (Git), cài đặt dependencies, tạo template configs/tests.  
  - *Mục tiêu:* Có thể clone repo và chạy các test cơ bản.  
  - *Deliverables:* Repo cấu trúc, requirements, lệnh chạy.  
  - *Acceptance:* CI chạy sạch.  
  - *Rủi ro:* xung đột package.  

- **Mốc 2 — Baseline:** Tải dataset, cài đặt log parser, windowing, triển khai LogSentry (theo mô tả TDS). Huấn luyện/baseline inference.  
  - *Mục tiêu:* Đạt được performance tham chiếu của LogSentry.  
  - *Deliverables:* Code baseline, script chạy baseline, log output.  
  - *Acceptance:* Kết quả F1 tương tự TDS (± tolerance).  
  - *Dependencies:* Mốc 1.  
  - *Risks:* Sai tiền xử lý, thiếu dữ liệu.  

- **Mốc 3 — Improvement:** Cài đặt RAG + LLM: xây dựng index tri thức, tạo prompt, tích hợp adapter gọi LLM. Kết hợp vào pipeline baseline.  
  - *Mục tiêu:* Pipeline improved chạy được (có trả prediction).  
  - *Deliverables:* Code retrieval & LLM, script improved mode.  
  - *Acceptance:* Hệ thống không lỗi, trả output giải thích và nhãn.  
  - *Dependencies:* Mốc 2.  
  - *Risks:* Lỗi API LLM, vượt token limit.  

- **Mốc 4 — Thực nghiệm chính:** Chạy thử nghiệm baseline vs improved nhiều lần. Thu thập metrics đầy đủ.  
  - *Mục tiêu:* Có dữ liệu so sánh F1, lead time.  
  - *Deliverables:* Logs kết quả, summary table.  
  - *Acceptance:* Hoàn thành đủ số run định sẵn, metric được ghi lại.  
  - *Dependencies:* Mốc 3.  
  - *Risks:* Sai config, tốn thời gian.  

- **Mốc 5 — Ablation/Robustness:** Thực hiện ablation (ví dụ bỏ LLM), và kiểm thử robustness nếu cần (ví dụ thêm nhiễu).  
  - *Mục tiêu:* Đánh giá ảnh hưởng từng thành phần cải thiện.  
  - *Deliverables:* Kết quả ablation, phân tích.  
  - *Acceptance:* Có biểu đồ/báo cáo cho ablation.  
  - *Dependencies:* Mốc 4.  
  - *Risks:* Kết quả không rõ ràng.  

- **Mốc 6 — Artifact cuối:** Hoàn thiện chạy cuối cùng, thống kê toàn diện, viết báo cáo SDS.  
  - *Mục tiêu:* Tất cả artifact (code, config, results) sẵn sàng cho public release.  
  - *Deliverables:* Báo cáo SDS (this doc), plots cuối, hướng dẫn chạy.  
  - *Acceptance:* Kết quả có thể tái lập bởi người khác.  
  - *Dependencies:* Các mốc trước.  
  - *Risks:* Thiếu reproducibility do môi trường khác nhau.  

Mỗi mốc đều kiểm tra kết quả và code, đảm bảo chuẩn bị cho mốc tiếp theo.

## 18. Tiêu chí Chấp nhận

- **Baseline:**  
  - Chạy thành công (không lỗi) với config mẫu.  
  - Các metric tham chiếu (Precision, Recall, F1) đạt gần với báo cáo gốc (± tolerance).  

- **Improvement:**  
  - Chạy độc lập (chỉ bật/improvement).  
  - Giao diện rõ ràng (có toggle `use_llm`).  
  - Có thể bật/tắt cải thiện mà không ảnh hưởng baseline.  
  - Không làm thay đổi định nghĩa metric hay data pipeline.  

- **Thực nghiệm chính:**  
  - Các biến kiểm soát (seed, split, config) được giữ cố định giữa các chế độ.  
  - Thu thập đầy đủ metric cho cả baseline và improved.  
  - Hoàn thành số lần lặp (run) đã định.  

- **Artifact:**  
  - Tất cả cấu hình (YAML) được lưu cùng kết quả.  
  - Các phiên bản code, dataset, model được ghi rõ trong metadata.  
  - Kết quả có thể theo dõi (traceability) đến các thành phần tương ứng trong mã.  

Nếu các tiêu chí trên không thỏa mãn, phần mềm cần được rà soát và chỉnh sửa trước khi kết luận.

## 19. Ma trận Truy vết

| Research Element | TDS Element                        | Software Module       | Experiment        | Metric                               |
|------------------|------------------------------------|-----------------------|-------------------|--------------------------------------|
| **RQ1**         | So sánh chất lượng phát hiện      | BaselineDetector, ImprovementModule | A vs B           | Precision, Recall, F1               |
| **RQ2**         | Phát hiện sớm (lead time)         | Retriever, LLMAdapter, EarlyDetectionEvaluator | A vs B | Time-to-Detection, Early Warning Rate |
| **RQ3**         | Độ ổn định/khả năng mở rộng       | WindowGenerator, Retriever, LLMAdapter | C (ablation)     | False Alarm Rate, latency            |
| **H1**           | H1: Improved tăng F1              | BaselineDetector & Improved logic   | A vs B           | F1                                 |
| **H2**           | H2: Improved giảm thời gian phát hiện | Retriever+LLM pipeline                | A vs B           | Lead Time, TTD                      |
| **H3**           | H3: Cải thiện không tăng FAR     | End-to-end pipeline                  | A vs B, C        | False Alarm Rate                    |

Mỗi mục trên được mapping từ **Câu hỏi nghiên cứu (RQ)** và **Giả thuyết (H)** sang thành phần phần mềm tương ứng, để đảm bảo traceability giữa design và experiments/metrics.

## 19A. Final Baseline Eligibility Verification

- [x] Baseline được công bố trong 2023–2026. (Sci Rep, Nov 2025)  
- [x] Bài báo là journal article chính thức, peer-reviewed. (Scientific Reports là tạp chí chính thức thuộc Nature).  
- [x] Tạp chí là Q1. (Sci Rep top 15% Multidisciplinary Sciences)  
- [x] Có DOI: 10.1038/s41598-025-22208-7.  
- [x] Bài báo này trùng khớp với baseline đã phê duyệt trong result-6.md. (Không thay baseline khác.)  
- [x] Không thay đổi baseline/limitation/improvement ngoài Design Freeze.

Nếu bất kỳ điều kiện trên không thỏa, SDS này chưa được chốt.

## 20. Q1/Q2 Ranking và Publication Verification

Đã xác minh: Journal *Scientific Reports* (Springer Nature) là tạp chí thuộc nhóm Q1 (Multidisciplinary) dựa trên SCImago/Clarivate. Mức độ uy tín và ấn phẩm năm 2025 đều hợp lệ. Các thông tin chi tiết (IF, quartile) được thu thập từ trang chính của tạp chí.

## 21. Chốt Thiết kế Phần mềm

Bản thiết kế cuối cùng này sử dụng **một phần mềm** duy nhất với baseline **LogSentry (Q1, Sci Rep 2025)**, cải thiện chính bằng **RAG/LLM** (chứa KNN retrieval + LLM gọi ra giải thích). Các phần **không đổi**: pipeline baseline, metric. **Thêm** thành phần mới: `retrieval/`, `prompts/`, `LLMAdapter`. Chế độ chạy: `baseline`, `improved`, `ablation`. Tất cả kết quả được lưu trữ (config, code version, logs, metrics) để có thể tái lập. Phần mềm đảm bảo tiến trình *Baseline → Improvement* và lưu artifact cho reproducibility. Thiết kế tuân thủ nguyên tắc: **baseline Q1/Q2 → cải thiện mục tiêu → baseline đã cải thiện → thực nghiệm có kiểm soát → artifact tái lập**.

**Nguồn trích dẫn:** Thông tin baseline được tham khảo từ bài Sci Rep và công bố của tạp chí. Các phương pháp RAG/LLM minh hoạ theo các nghiên cứu mới.