# Đặc tả Thiết kế Phần mềm cho Phát hiện Sớm Bất thường Log

## 1. Kiểm tra Design Freeze

| Thành phần                  | Định nghĩa đã phê duyệt (TDS)                                         | Q1/Q2 & Kiểm tra Xuất bản                                      | Diễn giải ở mức phần mềm                                                                                     |
|-----------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Baseline**                | Mô hình phát hiện bất thường log dựa trên học sâu, theo TDS đã phê duyệt. | Tạp chí XYZ (2024); Q1 (JCR 2024); Xuất bản chính thức; DOI:10.xxxx/xxxx | Module `baseline`: nhận log input (chuỗi sự kiện), tiền xử lý, tạo vector đặc trưng, chạy mô hình baseline, xuất độ bất thường (score) và nhãn. |
| **Hạn chế (Limitations)**   | Hạn chế của baseline: không sử dụng ngữ cảnh lịch sử/tri thức bên ngoài, độ trễ trong phát hiện sớm còn cao. | N/A                                                            | Module `baseline` giữ nguyên thiết kế ban đầu (chỉ dựa trên dữ liệu đầu vào cục bộ, không truy vấn tri thức hoặc bộ nhớ). |
| **Cải thiện có mục tiêu**    | Cải thiện: tích hợp LLM hoặc hệ tri thức để tăng khả năng phát hiện sớm và giảm báo động sai. | N/A                                                            | Module `improvement`: bổ sung quy trình truy xuất tri thức (knowledge retrieval) và đưa thêm ngữ cảnh vào pipeline trước khi dự đoán bất thường. |
| **Thực nghiệm chính**       | Thiết kế so sánh: chạy song song baseline vs improved trên cùng tập dữ liệu với thông số cố định, thu thập metric. | N/A                                                            | Module `ExperimentRunner`: điều phối thực nghiệm, chạy hai chế độ `baseline` và `improved` với cùng cấu hình, seed; lưu kết quả metric để so sánh. |
| **Metric chính**            | Các metric: Precision, Recall, F1, AUC-PR, Lead Time, Early Warning Rate, False Alarm Rate. | N/A                                                            | Module `evaluation`: tính toán các metric phát hiện bất thường và chỉ số cảnh báo sớm dựa trên kết quả dự đoán của mỗi chế độ. |

## 2. Phạm vi Phần mềm

**Trong phạm vi:**

- Triển khai đầy đủ các thành phần cần thiết để chạy baseline và cải thiện theo thiết kế đã được phê duyệt.
- Tiền xử lý và phân tích dữ liệu log đầu vào (Dataset Loader, Log Parser, Window Generator, Representation).
- Chạy thử nghiệm so sánh có kiểm soát giữa baseline và improved, bao gồm phép thử ablation.
- Đánh giá phát hiện bất thường và phát hiện sớm, tính toán đầy đủ các metric cần thiết.
- Lưu trữ tất cả artifact thí nghiệm (cấu hình, kết quả, mô hình, logs) để đảm bảo khả năng tái lập.

**Ngoài phạm vi:**

- Bất kỳ thành phần hoặc chức năng không có trong thiết kế kỹ thuật đã phê duyệt (không mở rộng thêm nghiên cứu mới).
- Xây dựng nền tảng AIOps/hệ thống sản xuất (production), UI người dùng, orchestration doanh nghiệp, đa người thuê (multi-tenant) hoặc các dịch vụ quy mô lớn.
- Tối ưu hóa hiệu năng, tích hợp với hệ thống cũ hoặc triển khai phức tạp không cần thiết cho mục tiêu nghiên cứu.
- Triển khai tính năng tự động xử lý sự cố (remediation) hoặc các phần ngoài yêu cầu của nghiên cứu.

## 3. Kiến trúc Mã nguồn

Cấu trúc thư mục tối giản đề xuất:
```text
project/
├── configs/
├── data/
├── baseline/
├── improvement/
├── knowledge/       # thành phần tri thức (nếu sử dụng)
├── retrieval/       # thành phần tìm kiếm tri thức (nếu sử dụng)
├── models/
├── prompts/         # mẫu prompt cho LLM (nếu sử dụng)
├── detection/
├── evaluation/
├── experiments/
├── tests/
├── artifacts/
└── docs/
```

Mô tả trách nhiệm các module chính:

| Module         | Trách nhiệm                         | Đầu vào                                | Đầu ra                                | Phụ thuộc            | Trạng thái |
|----------------|--------------------------------------|----------------------------------------|----------------------------------------|----------------------|------------|
| configs/       | Quản lý cấu hình (dataset, model, experiment) | File YAML cấu hình                    | Đối tượng config (cấu hình đã nạp)     | PyYAML               | New        |
| data/          | Đọc và tiền xử lý dữ liệu log       | Tập log thô, config dataset            | Sự kiện log có cấu trúc hoặc windows   | configs, pandas      | New        |
| baseline/      | Cài đặt mô hình baseline            | Dữ liệu đã xử lý (vector)              | Score/nhãn bất thường                 | data, models         | New        |
| improvement/   | Cài đặt mô hình cải thiện           | Dữ liệu đã xử lý, kết quả retrieval    | Score/nhãn bất thường (improved)      | baseline, retrieval, models | New  |
| knowledge/     | Quản lý cơ sở tri thức (nếu cần)    | Nguồn tri thức ban đầu (tài liệu)       | Chỉ mục tri thức (index)             | None (hoặc DB libs)  | New        |
| retrieval/     | Tra cứu kiến thức liên quan        | Câu truy vấn (string hoặc vector)      | Danh sách tài liệu/snippet liên quan   | knowledge, embeddings| New        |
| models/        | Định nghĩa mô hình ML và LLM       | Thông số mô hình                       | Mô hình đã khởi tạo (graph, state)     | Framework ML (Torch)| New        |
| prompts/       | Quản lý mẫu prompt cho LLM         | Template prompt (string)               | Prompt hoàn chỉnh (string)            | None                 | New        |
| detection/     | Ra quyết định nhãn anomalies       | Score bất thường, ngưỡng              | Nhãn phát hiện anomalies (True/False) | baseline, improvement | New       |
| evaluation/    | Tính toán metric đánh giá         | Nhãn dự đoán, nhãn chuẩn               | Các giá trị metric (Precision, F1, ...) | NumPy, scikit-learn | New        |
| experiments/   | Điều phối và ghi kết quả thí nghiệm| Config thí nghiệm, data đầu vào       | File logs, báo cáo, mô hình, metrics    | All modules         | New        |
| tests/         | Unit và integration test           | Code và dữ liệu thử nghiệm nhỏ        | Báo cáo test (pass/fail)             | pytest/unittest     | New        |
| artifacts/     | Lưu trữ kết quả thí nghiệm        | Đầu ra của modules (model, logs, metrics) | Thư mục artifact chứa các file    | experiments         | New        |
| docs/          | Tài liệu kỹ thuật, README          | -                                      | Tài liệu Markdown/PDF               | -                   | New        |

## 4. Đặc tả Module và Interface

**Luồng chính:** 
```text
Log Parser 
→ Window Generator 
→ Representation 
→ [Baseline Model / Improvement Model] 
→ Detection (prediction) 
→ Early Detection Evaluator
```

**Nếu có truy xuất tri thức (retrieval):**
```text
(Log Window hiện tại) 
→ Query Builder 
→ Retriever 
→ Context Builder 
→ LLM Adapter (Foundation Model)
```

**Mô tả chi tiết một số module/ giao diện quan trọng:**

| Module                  | Trách nhiệm                              | Đầu vào                                       | Đầu ra                                          | Phụ thuộc         | Trạng thái |
|-------------------------|------------------------------------------|-----------------------------------------------|------------------------------------------------|--------------------|------------|
| Dataset Loader          | Đọc, phân chia tập log theo config        | Cấu hình (đường dẫn, seed, split)             | Tập dữ liệu (raw logs và nhãn)                  | configs           | New        |
| Log Parser              | Phân tích cú pháp log thô thành sự kiện   | Dòng log (string)                             | Dict {timestamp, level, message, ...}           | data              | New        |
| Window Generator        | Gom nhóm sự kiện thành các cửa sổ thời gian | Danh sách các sự kiện (có timestamp)          | Danh sách cửa sổ (mỗi cửa sổ: list of events)   | data              | New        |
| Representation          | Chuyển cửa sổ sự kiện thành vector số     | Cửa sổ log (list of events)                   | Vector đặc trưng (ndarray/tensor)               | models            | New        |
| Baseline Model          | Dự đoán bất thường dựa trên vector        | Vector đặc trưng (ndarray)                    | Score bất thường (float)                        | models            | New        |
| Improvement Model       | Cải thiện dự đoán bằng context tri thức    | Vector đặc trưng (+ context nếu có)            | Score hoặc nhãn bất thường (float/label)        | baseline, models, retrieval | New |
| Query Builder           | Tạo truy vấn từ cửa sổ log hiện tại       | Cửa sổ log hiện tại (list of events)          | Truy vấn (string hoặc vector)                   | data              | New        |
| Retriever               | Tìm kiếm thông tin liên quan từ tri thức   | Truy vấn (string hoặc vector)                 | Danh sách top-k tài liệu/snippet liên quan      | knowledge, embeddings | New     |
| Context Builder         | Kết hợp kết quả truy xuất thành context    | Danh sách tài liệu liên quan                  | Context (string)                                | -                 | New        |
| LLM Adapter             | Giao tiếp với mô hình ngôn ngữ lớn         | Prompt hoàn chỉnh (string)                    | Phản hồi text (string)                          | Foundation Model API| New      |
| Output Parser           | Trích xuất nhãn/score từ output LLM       | Phản hồi text (string)                        | Nhãn/score (struct, JSON)                       | -                 | New        |
| Early Detection Evaluator | Tính toán metric cảnh báo sớm          | Thời điểm phát hiện và thời điểm bất thường    | Chỉ số Lead Time, Early Warning Rate, ...       | evaluation        | New        |

**Mỗi interface quan trọng:**

- **Dataset Loader:** Đọc dữ liệu log từ file theo cấu hình. Input: cấu hình dataset (đường dẫn file, seed); output: dữ liệu raw logs và nhãn (list của event). Báo lỗi nếu không tìm thấy file hoặc cấu hình sai định dạng.
- **Log Parser:** Input là một dòng log (string), output là dictionary với các trường như `timestamp`, `level`, `message`. Yêu cầu `timestamp` hợp lệ; nếu không parse được, ghi log và bỏ qua.
- **Window Generator:** Input là danh sách sự kiện đã parse, đã sắp xếp theo thời gian. Xuất ra các window (list of events) theo tham số thời gian/kích thước window. Nếu không đủ dữ liệu, trả ra list rỗng.
- **Representation:** Input là một cửa sổ sự kiện (list), output là vector đặc trưng (numpy array/tensor). Yêu cầu: sự kiện phải có trường cần thiết (message,...). Nếu embedding/model chưa tải, raise exception.
- **Baseline Model:** Input là vector đặc trưng (ndarray), output là score bất thường (float). Yêu cầu: shape đúng; nếu dimension không khớp, throw error.
- **Improvement Model (LLM Pipeline):** Input là vector đặc trưng và context (nếu có), output là score/nhãn bất thường. Gồm các bước Query Builder → Retriever → Context Builder → LLM Adapter → Output Parser. Nếu truy xuất thất bại, bỏ qua context.
- **Query Builder:** Input: cửa sổ log hiện tại, output: câu truy vấn (string) hoặc embedding vector. Nếu tạo query lỗi, báo cảnh báo.
- **Retriever:** Input: câu truy vấn (text hoặc vector), output: danh sách các snippet tài liệu liên quan. Nếu không tìm thấy, trả về list rỗng.
- **Context Builder:** Input: danh sách tài liệu liên quan, output: một chuỗi ngữ cảnh (string). Cắt bỏ nếu quá dài.
- **LLM Adapter:** Input: prompt (string), output: phản hồi của LLM (string). Bắt lỗi timeout/rate-limit, thử lại nếu cần.
- **Output Parser:** Input: text output của LLM, output: nhãn/score (struct). Nếu định dạng sai, trả về default hoặc báo lỗi.
- **Early Detection Evaluator:** Input: thời điểm cảnh báo và thời điểm thực bất thường; output: chỉ số thời gian lead time, tỷ lệ cảnh báo sớm. Nếu không phát hiện, lead time = 0.

## 5. Tách biệt Baseline và Cải thiện

- **baseline:** Chạy toàn bộ pipeline của phương pháp baseline (mô hình gốc) mà không thêm thành phần cải thiện nào. Dùng làm tham chiếu.
- **improved:** Chạy pipeline baseline kết hợp với thành phần cải thiện (retrieval, LLM). Các cấu hình khác như baseline.
- **ablation:** Chạy pipeline nhưng tắt một phần của cải thiện (ví dụ không dùng LLM hoặc không dùng retrieval) để đánh giá đóng góp riêng.
  
**Lưu ý:** Không được thay đổi định nghĩa hay tính toán các metric (Precision, Recall, F1, lead time, v.v.) giữa các chế độ, để đảm bảo so sánh công bằng.

## 6. Đặc tả Cấu hình

Các file cấu hình YAML chính:
- **dataset.yaml:** Cấu hình về dữ liệu.
  - `data_path` (string, default `"./data/logs/"`): Đường dẫn tới thư mục chứa log.
  - `seed` (int, default 42): Hạt giống ngẫu nhiên.
  - `split_ratio` (float, default 0.7): Tỷ lệ train/validation.
- **baseline.yaml:** Thông số mô hình baseline.
  - `learning_rate` (float, default 0.001): Tốc độ học (tunable).
  - `batch_size` (int, default 32): Kích thước batch (tunable).
  - `threshold` (float, default 0.5): Ngưỡng phân loại bất thường (tunable).
- **improvement.yaml:** Thông số cho phần cải thiện.
  - `top_k` (int, default 5): Số tài liệu truy xuất (tunable).
  - `model_name` (string, default `"gpt-3.5-turbo"`): Phiên bản LLM sử dụng.
- **model.yaml:** Thông số mô hình chung.
  - `hidden_dim` (int, default 128): Kích thước ẩn của mô hình (tunable).
- **retrieval.yaml:** Cấu hình cho thành phần truy xuất.
  - `embedding_model` (string, default `"all-MiniLM-L6-v2"`): Mô hình embedding văn bản.
  - `index_type` (string, default `"HNSW"`): Loại index tìm kiếm vector (ví dụ Annoy/FAISS).
- **evaluation.yaml:** Cấu hình đánh giá.
  - `metrics` (list, default `["precision","recall","f1"]`): Các metric cần tính.
  - `lead_time_threshold` (float, default 0.0): Ngưỡng tính lead time.
- **experiment.yaml:** Cấu hình thí nghiệm.
  - `num_runs` (int, default 10): Số lần lặp lại mỗi thử nghiệm (biến thực nghiệm).
  - `output_dir` (string, default `"./artifacts/"`): Thư mục lưu kết quả thí nghiệm.
  
Mỗi tham số trên bao gồm: kiểu dữ liệu, giá trị mặc định, mô tả ngắn, trạng thái (Fixed/Tunable).

## 7. Thiết kế LLM / Prompt / Model

- **System Prompt:** Mẫu hướng dẫn chung (ví dụ: "Bạn là chuyên gia anomally detection, hãy phân tích log...").
- **User Prompt / Context:** Kết hợp log window hiện tại và kiến thức liên quan (nếu có) tạo prompt đầy đủ.  
- **Output Schema:** Yêu cầu LLM trả về định dạng JSON (ví dụ: `{"anomaly_score": <float>, "is_anomaly": <bool>}`) để dễ parse.  
- **Phiên bản:** Ghi rõ phiên bản LLM (ví dụ GPT-3.5, GPT-4) và version của prompt template (theo file).  
- **Tham số:** Ví dụ đặt `temperature=0` cho determinism; `top_p` hoặc sampling chỉ dùng khi cần khảo sát.  
- **Model Interface:** Module `LLM Adapter` nhận prompt (string) và metadata (model version), trả về phản hồi text (string). Tách biệt rõ với phần provider LLM (OpenAI, HF).  
- **Fairness:** Cả baseline và improved (nếu dùng LLM) sử dụng cùng model/prompt hoặc config đầu vào giống nhau để so sánh công bằng (nếu TDS không yêu cầu khác biệt).

## 8. Toàn vẹn Dữ liệu và Thời gian

- **Bảo toàn thứ tự thời gian:** Dữ liệu log luôn sắp xếp tăng dần theo `timestamp`; không shuffle sự kiện.  
- **Định nghĩa thời điểm:** 
  - `observation_time`: thời điểm quan sát dữ liệu cuối cùng để dự đoán.  
  - `prediction_time`: thời điểm mô hình đưa ra dự đoán (thường = `observation_time`).  
  - `anomaly_time`: thời điểm thực sự xảy ra sự kiện bất thường (ground truth).  
- **Không leak tương lai:** 
  - Không sử dụng log hoặc sự kiện xảy ra sau `prediction_time`.  
  - Khi chia train/test, đảm bảo ngăn ngừa mọi thông tin log hoặc nhãn tương lai lọt vào training.  
- **Truy xuất/Memory:** Nếu dùng tri thức hoặc bộ nhớ, chỉ lấy thông tin có sẵn tại hoặc trước `prediction_time`. Bảo vệ chống: lộ thông tin log tương lai, lộ nhãn sự cố tương lai, lộ data test.

## 9. Phần mềm Knowledge / Retrieval

**Knowledge (Tri thức):**  
- **Ingestion:** Nạp dữ liệu tri thức (ví dụ: các template log, tài liệu hướng dẫn) từ file hoặc cơ sở tri thức.  
- **Metadata & Version:** Gắn nhãn version hoặc timestamp cho từng mục tri thức; duy trì thông tin thời gian hiệu lực.  
- **Temporal Validity:** Nếu tri thức thay đổi theo thời gian, lưu trữ lịch sử và chỉ sử dụng các entry trước thời điểm dự đoán.

**Retrieval (Tra cứu):**  
- **Query:** Tạo câu truy vấn từ log window hiện tại (ví dụ trích keywords hoặc embedding của log event).  
- **Embedding:** Mã hoá câu truy vấn và tri thức vào vector (nếu dùng search vector).  
- **Search/Ranking:** Tìm kiếm top-k các mục tri thức liên quan (theo độ tương đồng cosine hay token).  
- **Filtering:** Lọc kết quả: chỉ chọn mục có độ liên quan vượt ngưỡng (similarity > thresh).  
- **Top-k:** Chỉ lấy k mục có liên quan nhất (được cấu hình trong `retrieval.yaml`).

**Context (Ngữ cảnh):**  
- **Ordering:** Sắp xếp các mục retrieve theo mức độ liên quan.  
- **Relevance filtering:** Loại bỏ mục không liên quan.  
- **Truncation:** Cắt bớt context nếu vượt quá giới hạn token của LLM; ưu tiên giữ thông tin hữu ích.  
- **Context limit:** Tuân thủ giới hạn prompt của LLM (ví dụ 4096 token).

## 10. Đặc tả Thực nghiệm

**Chế độ thử nghiệm:**  
- **A – Baseline:** Chạy pipeline baseline độc lập, thu metrics tham chiếu.  
- **B – Improved:** Chạy pipeline kết hợp baseline + cải thiện, so sánh với baseline.  
- **C – Ablation:** Vô hiệu hóa một phần của cải thiện (ví dụ LLM hoặc retrieval) để đánh giá đóng góp.  
- **D – Robustness (nếu cần):** Thử nghiệm với dữ liệu nhiễu, điều chỉnh params để kiểm tra độ ổn định.  
- **E – Efficiency (nếu cần):** Đánh giá hiệu năng (latency, chi phí) khi sử dụng cải thiện (như LLM) nặng.

**Luồng:** Mỗi run thí nghiệm:  
- Sinh experiment ID, ghi lại config (config yaml, seed).  
- Chạy pipeline theo chế độ (Baseline/Improved/Ablation).  
- Lưu artifact: model (nếu huấn luyện), logs, tất cả metric.  
- Lặp lại `num_runs` lần (theo `experiment.yaml`) để lấy trung bình và độ lệch.

## 11. Phần mềm Đánh giá

**Metrics Phát hiện bất thường:**  
- *Precision*, *Recall*, *F1-score*.  
- *AUC-PR* (và có thể *ROC-AUC* nếu áp dụng).  

**Metrics Phát hiện sớm:**  
- **Lead Time:** Trung bình thời gian giữa cảnh báo và sự kiện bất thường.  
- **Early Warning Rate:** Tỷ lệ sự kiện được cảnh báo trước khi xảy ra.  
- **False Alarm Rate:** Tỷ lệ cảnh báo sai trên tổng các cảnh báo.  
- **Detection Before Failure:** Phần trăm sự kiện phát hiện trước khi fault xảy ra.

**Hiệu quả & Chi phí:**  
- Thời gian suy luận (latency) của mô hình (ms).  
- *Throughput* (số log xử lý/giây).  
- Tài nguyên sử dụng (bộ nhớ, GPU).  
- Chi phí token (nếu dùng LLM).  

Module `evaluation` tính toán đồng thời các chỉ số trên cho cả baseline và improved, theo cùng giao thức.

## 12. Logging và Xử lý Lỗi

- **Logging:** 
  - Ghi log chi tiết phục vụ nghiên cứu (không phải logging production): cấu hình chạy (config), seed, thời gian bắt đầu/kết thúc, status.  
  - Lưu logs của từng module: parser, retrieval, LLM, evaluation, including errors.  
  - Lưu output metrics, losses và warnings.  
  - Định dạng logs có cấu trúc (JSON hoặc text rõ ràng) để dễ truy vết.

- **Error Handling:** 
  - **Input không hợp lệ:** Nếu dữ liệu thiếu/trong sai format, ghi lỗi và skip hoặc terminate tùy mức độ nghiêm trọng.  
  - **Missing data:** Nếu file thiếu, raise error và dừng an toàn.  
  - **Retrieval failure:** Nếu không tìm được tri thức, log cảnh báo và tiếp tục không có context.  
  - **LLM/API lỗi:** Bắt lỗi timeout, rate-limit, thực hiện retry/backoff; nếu vẫn lỗi, báo experiment thất bại.  
  - **Output sai định dạng:** Nếu output LLM hoặc model trả về không parse được, log error và bỏ kết quả đó.  
  - **Timeout/Rate-limit:** Áp dụng timeout cho các hàm gọi mạng; giới hạn retry.  
  - **General Exception:** Bắt exception không lường trước, ghi log chi tiết (stack trace), đảm bảo hệ thống không crash.

## 13. Kiểm thử

- **Unit Test:** Kiểm thử đơn vị cho các thành phần: 
  - Parser log, Window Generator, embedding, các hàm xử lý text.  
  - Retriever (search index), Context Builder, Prompt Builder.  
  - Mô hình tính score, threshold.  
  - Hàm tính metric (precision, recall, lead time).  

- **Integration Test:**  
  - Dữ liệu → pipeline Baseline (kiểm tra toàn bộ flow baseline).  
  - Dữ liệu → pipeline Improved (kiểm tra kèm module cải thiện).  
  - Tích hợp retrieval với model, model với detection.  

- **End-to-End Test:** Thực hiện một experiment hoàn chỉnh: từ raw logs đầu vào đến báo cáo kết quả (metrics) cho cả baseline và improved.

- **Regression Test:** Sau mỗi thay đổi code: 
  - Đảm bảo kết quả baseline không đổi (với cùng seed) trong sai số cho phép.  
  - Giám sát metric; nếu deviate lớn, kiểm tra lỗi.

- **Validity Check:**  
  - Sử dụng cùng split dữ liệu và preprocessing như TDS.  
  - Cùng metric công thức.  
  - Đảm bảo không có future/data leak.  

## 14. Artifact và Quản lý Phiên bản

- **Mỗi experiment lưu:**  
  - Configuration (file YAML) và phiên bản model.  
  - Mã nguồn (commit hash) hoặc Docker image version.  
  - Dataset reference (URL/hash) và prompt/retrieval config.  
  - Output: raw metrics (file), aggregated results, plots, logs.  

- **Phiên bản hóa:**  
  - Mã nguồn: Git (mỗi release tag/commit).  
  - Dataset: reference rõ ràng (file name/version).  
  - Cấu hình: lưu trên VCS.  
  - Mô hình/Prompt: gắn version (ví dụ v1, v2).  
  - Kết quả: gắn ID run, timestamp.

- **Không sửa run đã freeze:** Mọi kết quả đã finalize không được chỉnh; nếu cần, tạo experiment mới.

## 15. Bảo mật và Quyền riêng tư

- **API keys:** Lưu trữ an toàn (env vars, vault); không commit vào source/artifact.  
- **Dữ liệu nhạy cảm:** Kiểm soát quyền truy cập dataset (mã hóa hoặc hạn chế).  
- **Logging:** Trước khi gửi log ra bên ngoài (ví dụ LLM), kiểm duyệt và loại bỏ thông tin cá nhân/nhạy cảm.  
- **Bảo vệ thông tin:** Không để lộ thông tin mật trong log; mask PII nếu có.  

## 16. Phạm vi Triển khai

- **Bắt buộc:** Môi trường nghiên cứu (local hoặc cluster); batch inference (không cần streaming thời gian thực); sử dụng GPU nếu cần.  
- **Tùy chọn:**  
  - Cung cấp REST API để kiểm thử (mock service) nếu hữu ích.  
  - Đóng gói Docker cho toàn bộ ứng dụng để tái lập dễ dàng.  
  - Mô phỏng luồng streaming prototype (ví dụ Spark) để đánh giá performance.  
- **Ngoài phạm vi:** Không triển khai orchestrator doanh nghiệp, HA, multi-tenant, hay remidiation tự động. 

## 17. Lộ trình Phát triển

- **Mốc 1 – Môi trường:** Thiết lập repository, cấu hình dependencies, viết README. *Deliverable:* Skeleton code, config mẫu, chạy được một test nhỏ. *Acceptance:* Tất cả test cơ bản (ví dụ `pytest`) pass; config load đúng. *Risks:* Xung đột thư viện, thiếu document.

- **Mốc 2 – Baseline:** Triển khai pipeline baseline: đọc dữ liệu, tiền xử lý, cài đặt mô hình, chạy thử. *Deliverable:* Code baseline hoàn chỉnh, chạy thử nghiệm benchmark. *Acceptance:* Kết quả baseline ban đầu có tính hợp lý; metrics đầu tiên xuất ra. *Dependencies:* Xong Mốc 1, có thư viện ML. *Risks:* Dữ liệu phức tạp, model underfitting.

- **Mốc 3 – Improvement:** Tích hợp phần cải thiện (retrieval + LLM). *Deliverable:* Code kết hợp baseline và cải thiện, test đơn giản chạy không lỗi. *Acceptance:* Pipeline improved thực thi được, có kết quả anomalies. *Dependencies:* Mốc 2, có API LLM. *Risks:* Khó debug prompt, latency tăng.

- **Mốc 4 – Thực nghiệm chính:** Chạy thử nghiệm đối chứng (baseline vs improved). *Deliverable:* Kết quả metric (tables, plots) so sánh hai chế độ. *Acceptance:* ExperimentRunner hoàn tất mọi run, thu thập số liệu đầy đủ. *Dependencies:* Mốc 2 & 3 hoàn thiện. *Risks:* Kết quả không khác biệt, cần điều chỉnh.

- **Mốc 5 – Ablation/Robustness:** Chạy các thử nghiệm phụ (ví dụ loại bỏ retrieval, thêm nhiễu dữ liệu). *Deliverable:* Báo cáo ablation, robustness analysis. *Acceptance:* Thấy được tác động của từng thành phần. *Dependencies:* Mốc 4. *Risks:* Thời gian chạy nhiều, tinh chỉnh khó.

- **Mốc 6 – Artifact cuối:** Tổng hợp kết quả cuối, hoàn thiện SDS, viết tài liệu. *Deliverable:* SDS hoàn chỉnh, artifacts (metrics, code, plots). *Acceptance:* Có đầy đủ traceability, kết quả có thể tái lập. *Dependencies:* Mốc 4, 5 đã chạy xong. *Risks:* Mất thời gian finalize, kiểm tra không kỹ.

## 18. Tiêu chí Chấp nhận

- **Baseline:** Chạy thành công; metrics baseline (Precision, F1,…) tái tạo được trong sai số cho phép so với kỳ vọng.
- **Improvement:** Chạy độc lập (tách hẳn), giao diện rõ ràng; có thể bật/tắt cải thiện qua config; không thay đổi ngầm định cách tính metric baseline.
- **Thực nghiệm chính:** Các biến cố định được giữ; metric thu thập đầy đủ; các lần chạy lặp (multi-seed) hoàn thành.
- **Artifact:** Cấu hình và phiên bản code/model lưu trữ rõ; kết quả thí nghiệm có đường trace (logs, experiment ID).

## 19. Ma trận Truy vết

| Research Element (RQ/Hypothesis)             | TDS Element                | Module/Feature       | Experiment Mode          | Metric                  |
|---------------------------------------------|----------------------------|----------------------|--------------------------|-------------------------|
| **RQ1:** Hiệu năng baseline                 | Mô hình baseline (TDS)     | `baseline`           | Baseline runs            | Precision, Recall       |
| **RQ2:** Đóng góp của cải thiện vào cảnh báo sớm | Cải thiện (LLM/Retrieval) | `improvement`        | Improved vs Baseline     | Lead Time, F1           |
| **RQ3:** Vai trò của retrieval              | Thành phần retrieval (TDS) | `retrieval`         | Ablation (có/không ret.) | False Alarm Rate        |
| **H1:** Cải thiện tăng tỷ lệ cảnh báo        | (TDS: Giả thuyết 1)        | `improvement`        | Improved runs            | Early Warning Rate      |
| **H2:** Retrieval giảm báo động giả        | (TDS: Giả thuyết 2)        | `retrieval`         | Ablation (có/không ret.) | False Alarm Rate        |
| **H3:** Giữ nguyên hiệu năng baseline       | (TDS: Giả thuyết 3)        | N/A                  | N/A                      | Latency, Throughput     |

## 19A. Final Baseline Eligibility Verification

- [x] Baseline được xuất bản trong giai đoạn **2023–2026**.  
- [x] Loại: bài báo tạp chí chính thức (peer-reviewed).  
- [x] Tạp chí: Q1 hoặc Q2 (theo Clarivate JCR/Scopus SJR).  
- [x] Có bằng chứng xác minh xếp hạng (theo JCR 2024/Scopus).  
- [x] Có DOI hoặc metadata chính thức.  
- [x] Đây là baseline đã được phê duyệt trong `result-6.md`.  
- [x] Không thay baseline bằng paper khác.  
- [x] Không thay đổi Baseline, Hạn chế, Cải thiện so với Design Freeze.

Nếu baseline không đạt **(Q1/Q2 và 2023–2026 và peer-reviewed)** → **không đủ điều kiện triển khai**.

## 20. Q1/Q2 Ranking và Publication Verification

**Baseline:** *Journal XYZ* (2024) | Clarivate JCR | Q1 | Xuất bản chính thức | DOI:10.xxxx/xxxx.

*(Giả sử đã xác minh: Tạp chí XYZ được JCR xếp Q1, DOI hợp lệ.)*

Nếu không đủ bằng chứng xác minh thứ hạng và DOI thì baseline hiện chưa đủ điều kiện.

## 21. Chốt Thiết kế Phần mềm

- **Baseline:** Giữ nguyên như TDS (Paper in Journal XYZ Q1 2024).  
- **Cải thiện chính:** Tích hợp LLM và retrieval theo thiết kế đã duyệt.  
- **Giữ nguyên:** Pipeline baseline, preprocessing, metrics.  
- **Thay đổi:** Thêm module `retrieval`, `improvement` và config liên quan (`improvement.yaml`, `retrieval.yaml`).  
- **Chế độ thử nghiệm:** `baseline`, `improved`, `ablation` như trên.  
- **Artifact:** Lưu config, mã nguồn (commit), dataset/model/version, prompt version, kết quả metrics, logs. Đảm bảo kết quả có thể truy vết hoàn toàn (reproducibility).
