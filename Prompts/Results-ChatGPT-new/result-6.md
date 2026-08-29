# Thiết kế kỹ thuật: Cải thiện phát hiện dị thường sớm trong hệ thống log

## 1. Xác minh trạng thái thiết kế đóng băng (Design Freeze Verification)  
| Yếu tố                | Từ `result-5.md`                | Diễn giải kỹ thuật                      | Kiểm tra Q1/Q2 và xuất bản | Thay đổi? |
|-----------------------|-------------------------------|-----------------------------------------|---------------------------|-----------|
| **Baseline**          | Mô hình phát hiện dị thường trên log dựa trên học sâu (chưa rõ tên)  | Một mô hình học sâu hiện có (theo thiết kế đóng băng) dùng embedding từ BERT và học tương phản (contrastive learning) để phân loại chuỗi log bình thường/ dị thường.  | Q1/Q2? Xác minh cần DOI/journal. Ví dụ: Báo cáo Li et al. (2025) trên *Scientific Reports* là Q1.  | –  |
| **Giới hạn (Limitation)** | Thiếu khả năng tận dụng tri thức lịch sử hoặc ngữ cảnh nhằm phát hiện sớm (theo `result-5.md`) | Mô hình baseline chỉ dựa trên đặc trưng tại thời điểm và không khai thác ngữ cảnh lịch sử, dẫn đến khả năng cảnh báo muộn khi mới xuất hiện bất thường. | – | – |
| **Cải tiến mục tiêu**     | Tích hợp truy vấn tri thức (RAG) hoặc mô hình nền tảng (theo `result-5.md`) | Thêm một thành phần truy hồi thông tin (knowledge retrieval) hoặc LLM để sử dụng ngữ cảnh lịch sử (logs, incidents, runbooks) hỗ trợ quyết định.  | – | – |
| **Đầu vào (Input)**     | Chuỗi log thô đã parse và window | Các log sự kiện (gồm timestamp và nội dung) sau xử lý tiền xử lý và đóng gói thành cửa sổ thời gian (window). | – | – |
| **Đầu ra (Output)**      | Nhãn dị thường/ sớm (anomaly score hoặc cảnh báo) | Phát hiện dị thường (và tín hiệu cảnh báo sớm kèm thời gian).  | – | – |
| **Đánh giá chính**      | Độ chính xác phát hiện và thời gian dẫn trước (lead time) | So sánh F1, Precision, Recall và các chỉ số thời gian (lead time, false alarm rate, Early Warning Rate) giữa baseline và cải tiến. | – | – |

**Kiểm tra tổng quát:** Theo thiết kế đóng băng (`result-5.md`), ta không đổi RQ/Hypotheses, không đổi baseline và limitation đã phê duyệt. Cần xác minh baseline được công bố 2023–2026 trên tạp chí Q1/Q2 có DOI. Ví dụ, Sci. Reports 2025 (Li et al.) là Q1 và có DOI, phù hợp. Nếu baseline trong thiết kế không đáp ứng điều kiện, cần ghi cảnh báo.  

## 2. Phạm vi hệ thống (System Boundary)  

- **Phạm vi trong (In Scope):** Các thành phần cần thiết để tái lập baseline và triển khai cải tiến bao gồm:  
  - **Tiền xử lý log (Log Parser):** Chuyển log thô thành định dạng cấu trúc (timestamp + ID sự kiện + thuộc tính).  
  - **Windowing:** Tạo cửa sổ thời gian (ví dụ sliding windows) để thành chuỗi sự kiện đầu vào của mô hình.  
  - **Biểu diễn (Representation):** Chuyển cửa sổ log thành vector đặc trưng (embedding bằng BERT hoặc vector đếm sự kiện).  
  - **Mô hình lõi (Core Model):** Mô hình phát hiện dị thường đã được công bố (baseline, *frozen*).  
  - **Thành phần Cải tiến:** Ví dụ thành phần retrieval/RAG, hoặc LLM (nếu được phê duyệt) để bổ sung tri thức ngữ cảnh.  
  - **Inference & Scoring:** Quy trình suy luận ra anomaly score, quy tắc quyết định (ngưỡng), ra cảnh báo.  
  - **Đánh giá (Evaluation):** Kịch bản kiểm thử và metric tính toán để so sánh base vs improved.  
  - **Hạ tầng (Reproducibility):** Kịch bản và dữ liệu cần để mọi thứ tái lập, gồm mã nguồn của baseline/ cải tiến riêng biệt.  

- **Ngoài phạm vi (Out of Scope):**  
  - **Nền tảng AIOps lớn:** Không xây hệ thống tổng quan, không dashboard, không component đa người dùng hoặc tự khắc phục (autonomous remediation).  
  - **Các dịch vụ không liên quan:** Ví dụ microservices phụ trợ (alert, logging sidecar không cần thiết).  
  - Mọi thành phần không có mối liên hệ trực tiếp với baseline, cải tiến hoặc đánh giá sớm.  

## 3. Đặc tả triển khai Baseline (Baseline Implementation Specification)  

**Tổng quan baseline:** Đối chiếu với `result-5.md`, baseline là phương pháp phát hiện dị thường log hiện có từ bài báo đã phê duyệt (Q1/Q2). Ví dụ tiêu biểu: **LogSentry (Li et al., Sci. Reports 2025)** sử dụng mô hình BERT đào tạo đối vị và thêm KNN-based retrieval trong suy luận. Trong baseline, chúng ta coi thành phần retrieval là *Inherited* (nếu có) nhưng chủ yếu mô hình chính là *frozen*.  

**Các bước chính trong pipeline Baseline:**  
- **Input:** Chuỗi sự kiện log (thô) chứa timestamp và message.  
- **Tiền xử lý/Parse:** Dùng log parser (có thể dùng các thư viện như Drain/Logpai) tách cấu trúc và mã hóa event IDs. Kết quả: stream các cặp (timestamp, eventID).  
- **Windowing:** Gom các sự kiện vào cửa sổ kích thước cố định hoặc linh hoạt (ví dụ 100 dòng hoặc 30s). Nếu bài bản đề xuất sliding window overlap, triển khai tương tự để phục vụ Early Detection.  
- **Biểu diễn (Representation):** Biểu diễn cửa sổ log dưới dạng vector. Ví dụ dùng embedding sự kiện kết hợp với vị trí. Có thể là đếm tần số ID, one-hot, hoặc sử dụng BERT để tạo embedding của chuỗi log. Tham số ví dụ: kích thước embedding, vocab size.  
- **Mô hình lõi:**  
  - **Học trước (Pre-training)/Huấn luyện:** Nếu baseline có giai đoạn huấn luyện, nó được thiết lập theo thiết kế. Ví dụ như contrastive learning BERT (đào tạo phân biệt log bình thường vs bất thường). Tập huấn luyện gồm log bình thường (có thể không có dị thường) để tạo mô hình phát hiện.  
  - **Đầu ra mô hình:** Mô hình cho *log anomaly score* (số thực từ 0 đến 1, với giá trị càng cao nghĩa là nghi dị thường hơn). Cấu hình: threshold mặc định, tên model checkpoint.  
- **Retrieval/Knowledge (nếu baseline hỗ trợ):** Trong ví dụ LogSentry, khi suy luận dùng KNN để tìm k log tương đồng từ tập huấn luyện và kết hợp điểm số . Nếu baseline ban đầu không có retrieval, bỏ qua.  
- **Inference (Suy luận):** Với cửa sổ mới, mô hình cho một anomaly score. Nếu có retrieval, kết hợp kết quả của mô hình và của thành phần retrieval (weighted sum).  
- **Công thức điểm dị thường (Anomaly scoring):** Xác định anomaly score, ví dụ xác suất log là bất thường.  
- **Quy tắc quyết định (Decision rule):** Đặt ngưỡng cố định (hoặc adaptive) để chuyển anomaly score thành cảnh báo. Ví dụ threshold=0.5.  
- **Output:** Cảnh báo dị thường (và thời gian phát hiện). Có thể xuất ra dạng (timestamp, label, score).  

**Bảng thành phần Baseline:**  

| Thành phần        | Trách nhiệm               | Đầu vào                   | Đầu ra                          | Tham số chính              | Phụ thuộc         |
|-------------------|---------------------------|---------------------------|---------------------------------|----------------------------|-------------------|
| **Log Parser**    | Tách cấu trúc log         | Log thô (chuỗi ký tự)      | EventID, timestamp             | Biểu mẫu parse             | Regex/Drain       |
| **Windowing**     | Gom log theo cửa sổ       | EventID series            | Các window (sequence)          | Kích thước window, stride  | Parser output     |
| **Representation**| Mã hóa window thành vector | Window (ID list)          | Vector embedding               | Kiểu embedding, kích thước | BERT model, vocab |
| **Mô hình cơ bản**| Phân loại dị thường/bình thường | Vector embeddings        | Anomaly score (0–1)            | Trọng số model, threshold  | Weights, Python   |
| **Retrieval**     | (Nếu có) Tra cứu log tương đồng | Vector hiện tại, index logs | Score_tu_retrieval (0–1)       | KNN k, weights            | Hệ CSDL logs      |
| **Kết hợp kết quả** | Hợp nhất điểm số          | Score_mô_hình, Score_Retrieval | Điểm cuối                   | Trọng số tổng hợp         | Logic weighted    |
| **Decision Rule** | Phát sinh cảnh báo        | Điểm cuối                 | Nhãn anomaly (0/1) hoặc cảnh báo| Ngưỡng (ví dụ 0.5)        | —                 |

*Chú ý:* Baseline được giữ “đóng băng” (**frozen**). Không thay đổi tham số hay kiến trúc ngoài việc cài đặt lại như gốc. Mọi thành phần ghi rõ là *Inherited* trong thiết kế.  

## 4. Đặc tả Cải tiến Mục tiêu (Targeted Improvement Specification)  

**Giới hạn (Limitation) cần khắc phục:** Theo `result-5.md`, mô hình baseline không sử dụng tri thức lịch sử/ngữ cảnh, dẫn đến **cảnh báo muộn**. Ví dụ, khi hệ thống bắt đầu xảy ra bất thường, mô hình có thể chỉ nhận ra khi đủ nhiều điểm bất thường tích lũy, làm giảm lead time.  

**Hướng cải tiến chính:** Tích hợp **truy vấn tri thức (RAG)** hoặc **mô hình ngôn ngữ lớn (LLM)** để kết hợp ngữ cảnh lịch sử vào dự đoán. Cụ thể có thể là:  
- Truy cập một bộ dữ liệu tri thức (logs quá khứ, sự cố đã biết, tài liệu,…).  
- Tạo truy vấn từ log hiện tại, sử dụng retriever (dense/sparse) để thu được ngữ cảnh liên quan.  
- Kết hợp ngữ cảnh vào quá trình suy luận (ví dụ thêm prompt cho LLM, hoặc dùng context embedding).  

**Bảng thành phần Cải tiến:**  

| Thành phần cải tiến      | Đầu vào                   | Trách nhiệm                 | Đầu ra                       | Liên hệ Baseline             | Giả thuyết (Hypothesis)                  |
|-------------------------|---------------------------|----------------------------|------------------------------|------------------------------|------------------------------------------|
| **Module Retrieval (RAG)** | Window log hiện tại, Corpus logs cũ | Phát sinh truy vấn ngữ cảnh tương ứng với log hiện tại. Tìm kiếm và trả về top-k log/sự kiện lịch sử liên quan. | Context vector (k bản ghi liên quan hoặc embedding) | Mới hoàn toàn (Baseline không có) | Có ngữ cảnh lịch sử giúp tăng độ nhạy và lead time phát hiện. |
| **LLM hoặc Mô hình kết hợp**   | Embedding window + Context (từ RAG) | Kết hợp thông tin: cho LLM (với prompt) hoặc kết hợp vector context với vector hiện tại. Sinh ra anomaly score cải tiến. | Anomaly score mới (có ngữ cảnh) | Mô hình baseline đã cho | Dự đoán dựa trên ngữ cảnh cải thiện độ chính xác/F1. |
| **Nâng ngưỡng động**     | Anomaly score + Historical threshold (nếu có) | Điều chỉnh threshold dựa trên trạng thái: ví dụ adaptive threshold khi có ngữ cảnh. | Ngưỡng điều chỉnh    | Có thể kế thừa ban đầu (cố định) | Ngưỡng linh hoạt giảm cảnh báo giả. |

*Giả thuyết chính:* Việc thêm thành phần truy hồi ngữ cảnh và/hoặc LLM sẽ **tăng tỷ lệ phát hiện đúng (Precision/Recall/F1)** và **đẩy thời điểm phát hiện lên sớm hơn**, so với baseline. Chúng ta sẽ kiểm định giả thuyết này qua thí nghiệm đối chứng Baseline vs Improved.  

## 5. Kiến trúc hệ thống tổng thể (Overall System Architecture)  

Hệ thống gồm hai luồng chính ghép Baseline và cải tiến: 

- **Luồng xử lý chính:** Log sự kiện → **Log Parser** → **Windowing** → **Representation** → **Core Model (Baseline)** → *(+* **Retrieval + LLM** *)* → **Anomaly Score** → **Decision Rule** → Output (cảnh báo). 

- **Luồng retrieval (nếu có):** Từ window hiện tại → *Truy vấn* → **Retriever** trong bộ tri thức logs cũ → **Ranking/Filtering** → **Context** → Kết hợp vào mô hình (ví dụ thêm vào prompt LLM hoặc vào embedding). 

Mô tả từng module (Inherited/Modified/New):  
- **Log Parser (Inherited):** Tương tự baseline; không thay đổi.  
- **Windowing, Representation (Inherited):** Giữ nguyên theo baseline.  
- **Core Model (Modified):** Sử dụng mô hình nền của baseline, có thể mở rộng để nhận thêm context (thêm input node cho context).  
- **Retrieval Module (New):** Chưa có trong baseline (nếu baseline chưa có retrieval). Trả về ngữ cảnh liên quan.  
- **Context Builder (New):** Gộp ngữ cảnh và input; đảm bảo phân phối đúng thứ tự hoặc segment.  
- **LLM/Inference (New hoặc Modified):** Nếu dùng LLM, mô-đun gọi API hoặc local model để suy luận với prompt. Nếu không, thêm bước kết hợp context với đầu vào.  
- **Decision Rule (Modified):** Có thể điều chỉnh threshold linh động hoặc dùng thuật toán gating nếu cần.  
- **Evaluation (Evaluation-only):** Thành phần thu thập metric offline; tính precision/recall/F1, lead time, etc.  

Đây là hệ thống **tối thiểu, có kiểm soát**, chỉ gồm các module cần thiết cho thí nghiệm. Các khối được đánh dấu trạng thái: *Inherited* (xanh), *New* (màu mới), *Modified* (đổi đầu vào để thêm context), *Evaluation-only*.

## 6. Truy vết nghiên cứu – hệ thống (Research-to-System Traceability)  

| Yêu cầu nghiên cứu (RQ/Hyp) | Thành phần hệ thống liên quan   | Thí nghiệm                        | Metric                    |
|-----------------------------|---------------------------------|-----------------------------------|---------------------------|
| **RQ1:** Hiệu năng phát hiện | Mô hình cơ bản + Module cải tiến | So sánh baseline vs improved      | Precision, Recall, F1     |
| **RQ2:** Phát hiện sớm      | Module cải tiến (RAG/LLM)        | So sánh thời điểm phát hiện       | Lead time, TTD (Time to Detect), EWR |
| **RQ3:** Độ ổn định/mở rộng  | Hệ thống tổng thể               | Thử nghiệm cross-dataset          | AUC-ROC, PR-AUC          |
| **H1:** Cải thiện F1        | Mô hình cơ bản + RAG/LLM        | Kiểm định độc lập (paired t-test) | F1 difference, p-value    |
| **H2:** Thời gian cảnh báo sớm hơn | Module RAG/LLM            | Đo lead-time trung bình vs baseline | Avg lead time, False alarm rate |
| **H3:** Tác động tài nguyên (latency) | Toàn hệ thống       | Đo latency và chi phí token       | Throughput (req/s), latency |

*Luồng từ nghiên cứu đến thực thi:* Mỗi RQ/Hyp được ánh xạ vào thành phần tương ứng (ví dụ RQ2 liên quan đến module cải tiến) và thí nghiệm kiểm định (tính statistic, metric). Mọi nghiệm vụ/Hypothesis đều có thí nghiệm xác nhận và metric tương ứng.  

## 7. Luồng dữ liệu (Data Flow Specification)  

**Luồng chính:**  
```
Raw Logs → Log Parser → Windowing → Representation → Core Model (Baseline) → [Retrieval/Context (nếu có)] → Inference → Anomaly Score → Decision → Alert
```
- *Offline:* Quá trình huấn luyện baseline (và huấn luyện thành phần cải tiến nếu cần).  
- *Online:* Từ khi log mới đến khi báo động: parser, window, rep, cải tiến, suy luận, quyết định (latency-sensitive).  

**Nếu sử dụng retrieval:**  
```
Window hiện tại → Query builder → Retriever (tìm trong corpus logs/KB) → Top-k candidates → Context builder → Model Inference
```  

Các bước *offline* chỉ gồm huấn luyện và indexing logs. *Online* bao gồm hết các bước từ parser đến alert. Xác định rõ mỗi bước: ví dụ representation bằng BERT có thể được precompute embedding logs lịch sử *offline*, sau đó truy vấn *online*.

## 8. Thiết kế dữ liệu theo thời gian (Temporal Data Design)  

- **Timestamp:** Mỗi log có timestamp (thời gian ghi log). Dữ liệu timestamp dùng để tạo cửa sổ thời gian.  
- **Windows quan sát:** Xác định cửa sổ quá khứ dùng làm input (ví dụ 30s hoặc 100 logs).  
- **Horizon dự đoán:** Chỉ cho phép dùng thông tin trước thời điểm dự đoán; không truy cập dữ liệu *sau* log hiện tại.  
- **Thời điểm sự cố:** Nếu có nhãn thời gian anomaly hay failure, ghi rõ. Giả sử có nhãn "time of failure" để đánh giá lead time.  
- **Thời điểm phát hiện:** Thời điểm hệ thống báo cảnh báo (alert).  
- **Lead Time:** Lead Time = (Time of failure) – (Time of detection). Phải đảm bảo luôn ≥ 0.  

**Kiểm soát temporal leakage:** Không cho dùng log, nhãn sự cố hoặc tri thức sau thời điểm cần dự đoán. Nếu dùng retrieval, phải lọc mục lưu trữ chỉ có data < thời điểm hiện tại.  

| Nguồn dữ liệu     | Timestamp          | Có sẵn tại thời điểm dự đoán? | Cho phép? |
|-------------------|--------------------|-------------------------------|-----------|
| Log hiện tại      | Thời gian hiện tại | ✔ (có)                        | Có        |
| Logs quá khứ      | Các thời điểm trước| ✔ (có)                       | Có        |
| Nhãn sự cố tương lai | Thời điểm sự cố  | ✖ (không)                     | Không     |
| Kiến thức lịch sử (KB) | Thời gian tài liệu/sự cố | ✔ (chỉ dùng cũ hơn)   | Có, nếu lọc     |
  
Không sử dụng bất kỳ dữ liệu tương lai hay nhãn sự cố hậu nghiệm nào để dự đoán lúc đang “online”.

## 9. Kiến thức / Truy vấn (Knowledge / Retrieval)  

- **Mục tiêu truy vấn:** Dùng để tìm ngữ cảnh hữu ích hỗ trợ phát hiện sớm, ví dụ: tìm các bản ghi log tương tự từ lịch sử, thông tin về sự cố trước đây, hoặc mẫu log liên quan.  
- **Corpus tri thức:** Có thể gồm logs lịch sử (đã gắn nhãn) và tài liệu hỗ trợ (chú giải lỗi, runbooks).  
- **Retriever type:** Có thể là *sparse* (như BM25 hoặc TF-IDF) hoặc *dense* (embedding similarity). Nếu cải tiến đề xuất RAG, xác định rõ dùng phương pháp gì. Ví dụ: embedding từ BERT và index bằng FAISS (dense) hoặc dùng Elasticsearch (sparse).  
- **Chi tiết truy vấn:**  
  - Tạo query từ nội dung window hiện tại (có thể dùng embedding trung bình của các event).  
  - **Candidate pool:** Logs lịch sử ở kho dữ liệu (có embedding hoặc chỉ số).  
  - **Ranking/Filtering:** Tìm top-k phù hợp (ví dụ k=5) dựa trên khoảng cách embedding (cosine) hoặc score TF-IDF. Lọc theo thời gian (chỉ các bản ghi cũ hơn).  
  - **Đầu ra:** Tập top-k context; thu gộp embedding (ví dụ concat hoặc trung bình).  
- **Mục tiêu:** Trích xuất thông tin liên quan giúp cải thiện khả năng phân biệt dị thường – giả thiết: bản ghi tương tự đã quan sát = dấu hiệu chớm phát hiện.  

Ví dụ giả sử: Ta dùng trình truy vấn embedding logs, tìm context và đưa vào prompt/đầu vào model để tăng score cho các pattern dị thường đã biết.

## 10. Xây dựng ngữ cảnh (Context Construction)  

Nếu dùng LLM/RAG:  
- **Bối cảnh hiện tại:** Kết hợp chuỗi log (window) hiện tại với nội dung retrieved.  
- **Ordering:** Ưu tiên sắp xếp context theo độ liên quan (ranking).  
- **Truncation:** Giới hạn tổng kích thước prompt (nếu dùng LLM) hoặc số lượng token.  
- **Định dạng:** Nếu prompt cho LLM, thêm phần ngữ cảnh (ví dụ: “Historical similar logs: ...\nCurrent log: ...\n anomaly?”). Nếu mạng neural khác, gộp embedding hiện tại với embedding context (như concatenation).  
- **Kiểm soát:** Loại bỏ thông tin nhiễu/trùng lặp, đảm bảo context chưa từng thấy trong huấn luyện (tránh tiết lộ nhãn).  
- **Thời gian:** Context chỉ dùng dữ liệu trước thời điểm log hiện tại.  

Nếu không dùng LLM, module context có thể chỉ thực hiện gộp embedding của những log tương tự vào vector đặc trưng.

## 11. Mô hình nền tảng / Đào tạo (Foundation Model / Training)  

- **Sử dụng Foundation Model:** Nếu cải tiến dùng LLM (như GPT-4), xác định rõ: phiên bản model, size (e.g. GPT-4 hoặc GPT-3.5), và interface (local/Cloud API). Ví dụ: dùng GPT-4 để phân tích log sequence.  
- **Đầu vào/Đầu ra:** Ví dụ, gửi prompt chứa log window và context, nhận anomaly probability hoặc đánh giá. Giữ mặc định cùng config model (độ lớn prompt, temperature=0 để determinism).  
- **Khóa huấn luyện:** Baseline và improved dùng chung model base (nếu pretrained). Không tự ý fine-tune LLM (theo yêu cầu).  
- **Đào tạo mới (nếu có):** Nếu có huấn luyện mạng neural (không phải LLM), nêu rõ tập train/val, epochs, optimizer. Ví dụ baseline đã có weights, không cần huấn luyện lại. Improved có thể không thêm training.  

Trừ khi trong thiết kế đã phê duyệt, không thêm bước huấn luyện LLM. Mục tiêu giữ mọi thứ đủ cô lập để đánh giá cải tiến.

## 12. Quy trình suy luận (Inference Workflow)  

1. **Log đến (Online Arrival):** Hệ thống nhận log mới theo thời gian thực.  
2. **Tiền xử lý (Parser):** Dịch log thô thành sự kiện cấu trúc.  
3. **Windowing:** Gom sự kiện vào cửa sổ hiện tại. Nếu dùng sliding window, cập nhật bằng cách cuộn từng bước.  
4. **Representation:** Tạo embedding/đặc trưng cho cửa sổ.  
5. **(Nếu cải tiến trước mô hình) Module cải tiến:** (Ví dụ) Dùng LLM để phân tích khối log trực tiếp hoặc nối prompt.  
6. **Retrieval/Context:** Gửi truy vấn vào kho logs, nhận ngữ cảnh, kết hợp với đầu vào.  
7. **Inference Model:** Suy luận bằng mô hình (baseline hoặc baseline mở rộng).  
8. **Anomaly Score:** Đầu ra score bình thường/tình trạng bất thường.  
9. **Early Detection:** Áp dụng quy tắc ngưỡng/threshold để quyết định cảnh báo. Nếu dự định cảnh báo sớm, tính lead time so với nhãn sự cố khi đánh giá ngoại tuyến.  
10. **Xuất cảnh báo (Output):** Ghi nhận (timestamp, cảnh báo, score).  

Gắn nhãn các bước *Online* (hoạt động liên tục) và *Offline/precomputed* (embedding history, indexing) và ghi chú nếu cần kiểm soát độ trễ (e.g. retrieval+LLM sẽ tăng latency, cần đánh giá).

## 13. Giao diện dị thường / phát hiện sớm (Anomaly/Early Detection Interface)  

- **Anomaly Score:** Số đo liên tục (ví dụ [0,1]) thể hiện độ bất thường. Ví dụ mô hình BERT cho điểm xấp xỉ xác suất dị thường. Phạm vi [0..1], interpret: càng cao càng nghi ngờ dị thường.  
- **Quy tắc quyết định:** Thiết lập ngưỡng (threshold). Có thể là giá trị cố định (ví dụ 0.5) hay adaptive (ví dụ percentile hoặc dựa vào mức độ tín hiệu hiện tại). Khi score > threshold → cảnh báo dị thường.  Ngưỡng ban đầu lấy từ baseline, sau đó có thể điều chỉnh trong cải tiến.  
- **Phát hiện sớm (Early Detection):** Định nghĩa: một log được đánh dấu cảnh báo *sớm* nếu anomaly score vượt ngưỡng trước khi xảy ra sự cố đích.  
  - **Lead Time:** Thời gian giữa cảnh báo và sự cố thực (failure) (thường tính trung bình cho tập dữ liệu).  
  - **Đầu ra cảnh báo:** Thời gian phát hiện và nhãn anomaly.  
- **Không đồng nhất:** Chú ý **không coi anomaly score là “điểm cảnh báo sớm”** cho đến khi so sánh với thời điểm sự cố. Cần chỉ định rõ: “score” trên model là tính năng cơ sở, “alert” mới tính toán lead time.  

Ví dụ: Mỗi log mới có anomaly score; nếu vượt threshold thì kích hoạt cảnh báo. Khi đánh giá, đo lead time giữa cảnh báo và ground truth anomaly time.

## 14. Cấu hình (Configuration)  

Các file cấu hình chính (dạng YAML):  
- **dataset.yaml:** Thông tin dataset (đường dẫn, tiền xử lý, labels). Tham số: loại dataset, ratio train/test, định dạng timestamp,...  
- **baseline.yaml:** Cấu hình baseline (mô hình, checkpoint, tham số). Tham số: đường dẫn model, threshold mặc định, kích thước window, embedding type.  
- **improvement.yaml:** Cấu hình cải tiến (các tham số retrieval hoặc LLM). Tham số: ví dụ k top retrieval, model LLM, context size, weights kết hợp.  
- **model.yaml:** Mô tả mô hình chung (số layers, hidden size) nếu cần.  
- **retrieval.yaml:** Nếu dùng RAG: loại retriever (dense/sparse), vector index path, tham số lọc (time horizon, top-k).  
- **evaluation.yaml:** Định nghĩa các metric cần thu (Precision, Recall, F1, LeadTime).  
- **experiment.yaml:** ID thử nghiệm, seed, nguồn config, notes.  

Ví dụ, `baseline.yaml` có:  
```yaml
threshold: 0.5           # ngưỡng dự đoán dị thường
window_size: 50         # số log trong cửa sổ
step: 10                # bước trượt của cửa sổ
model_checkpoint: "path/to/model.ckpt"
```
Mỗi tham số trong file được mô tả mục đích, giá trị mặc định, và miền giá trị. Ví dụ `threshold`: type=float, default=0.5, range=[0,1], dùng để quyết định cảnh báo.  

## 15. Quản lý thí nghiệm (Experiment Management)  

- **Thông tin cần lưu:** ID run, seed random, phiên bản dataset (phiên bản logs), code baseline/improve (commit hash), model versions.  
- **Artefact:** Đầu ra (điểm metric, hình ảnh, logs), config snapshot, môi trường (environment.yml).  
- **Theo dõi:** Có thể dùng MLflow hoặc W&B đơn giản (không bắt buộc), hoặc chỉ sử dụng file metadata. Mục đích: đảm bảo mọi tham số và kết quả được lưu.  
- **Đăng ký:** Mỗi thí nghiệm có duy nhất một ID, fix seed để tái lập.  

Ví dụ file `experiment.yaml` chứa:  
```
run_id: exp_baseline_v1
seed: 42
dataset: BGL_v1
baseline_checkpoint: abc123
improvement_commit: def456
```
Điều này đảm bảo có thể lặp lại các thử nghiệm chính xác.

## 16. So sánh có kiểm soát (Controlled Comparison)  

Để so sánh công bằng, giữ cố định mọi thứ *ngoại trừ* thành phần cải tiến chính.

| Yếu tố      | Baseline                         | Improved                                  | Được kiểm soát? |
|-------------|----------------------------------|-------------------------------------------|-----------------|
| Dataset     | **Giống hệt** (cùng tập log)     | **Giống hệt** (cùng tập log)              | ✅ Có           |
| Preprocessing | Giống (cùng parser, window)    | Giống (không thay)                        | ✅ Có           |
| Mô hình     | Mô hình baseline (frozen)        | Mô hình baseline + cải tiến              | ❌ Không (có thành phần mới) |
| Prompt/Context | Không (chỉ input log)         | Có thêm prompt/Context (RAG/LLM)         | ❌ (dự án)      |
| Ngưỡng      | Đặt cố định (ví dụ 0.5)          | Có thể điều chỉnh adaptive                | ❌ (khác)      |
| **Cải tiến**  | **Không**                       | **Kích hoạt Module mới (RAG/LLM)**         | ❌            |
| Đánh giá    | Cùng phương pháp (Precision, F1, lead time…) | Cùng phương pháp                       | ✅ Có           |

*Lưu ý:* Mọi yếu tố khác như mô hình ngôn ngữ nền, phần preprocessing đều không đổi. Chỉ có *improvement* (RAG/LLM) là biến thiên giữa hai điều kiện A-B.

## 17. Ablation  

- Nếu cải tiến gồm nhiều thành phần (ví dụ cả retrieval và threshold adaptive), thực hiện ablation:  
  1. **Improvement full:** Kết hợp tất cả thành phần mới.  
  2. **Bỏ retrieval:** Chỉ dùng LLM/prompts mà không trả về context.  
  3. **Bỏ LLM/prompts:** Dùng retrieval để refine threshold.  
  4. **Baseline:** Không có cải tiến.  

Mục tiêu: Xác định đóng góp riêng của từng thành phần. Ví dụ, xem liệu chỉ dùng retrieval thôi có cải thiện lead time hay không. Nếu improvement chỉ một module mới, so sánh baseline vs có/không module đó có thể đủ.

## 18. Cơ sở hạ tầng đánh giá (Evaluation Infrastructure)  

- **Phát hiện dị thường:** Tính *Precision, Recall, F1-Score* (định nghĩa tại ). Nếu phù hợp, dùng PR-AUC, ROC-AUC.  
- **Phát hiện sớm:**  
  - *Lead Time* (thời gian trung bình trước failure khi cảnh báo): Lead Time = FailureTime – DetectionTime.  
  - *Time-to-Detect (TTD):* Thời gian trễ trung bình từ log bất thường đầu tiên tới cảnh báo.  
  - *Early Warning Rate:* Tỉ lệ sự cố được cảnh báo trước khi thực sự xảy ra.  
  - *False Alarm Rate:* Tỉ lệ cảnh báo nhầm (trong windows bình thường).  
- **Hiệu năng (Efficiency):**  
  - *Độ trễ inference:* Đo thời gian xử lý mỗi window (ms).  
  - *Chi phí token (nếu LLM):* Số token gửi/nhận.  
  - *Throughput:* Số log (hoặc windows) xử lý / giây.  
  - *Tài nguyên:* Độ sử dụng GPU/CPU.  
- **Khả năng tổng quát (Generalization):** Nếu có, thử cross-dataset: huấn luyện trên hệ thống này, đánh giá trên hệ thống khác. Các metric như trên.

## 19. Thống kê / Tái lập (Statistical / Reproducibility)  

- **Số lần chạy:** Chạy nhiều lần (ví dụ 5 runs) với seed khác nhau.  
- **Seeds:** Ghi rõ seed cho mô hình và cho khởi tạo ngẫu nhiên.  
- **Khoảng tin cậy:** Báo ±95% CI cho Precision/Recall/F1.  
- **Kiểm định thống kê:** Ví dụ t-test hoặc Wilcoxon để so sánh baseline vs improved (p-value, effect size).  
- **Aggregation:** Tính average trên lần chạy. Đảm bảo độ lệch (std) nhỏ.  
- **Nếu LLM sử dụng:** Khóa phiên bản API, ghi rõ sampling/temperature. Tốt nhất để temperature=0 để determinism. Ghi log API version (GPT-4, v.v).  

Mục tiêu: Kết quả báo cáo có tính tin cậy (ví dụ không trùng hợp ngẫu nhiên).  

## 20. Phạm vi triển khai (Deployment Scope)  

- **Bắt buộc (Required):** Các thành phần cần thiết cho thí nghiệm luận văn: code, container hoặc script để chạy baseline/improve, dữ liệu mẫu.  
- **Tùy chọn (Optional):** Có thể xây prototype nhỏ (ví dụ service REST) để minh hoạ feasibility, nhưng không bắt buộc.  
- **Ngoài phạm vi (Out of scope):** Hệ thống đa người dùng, triển khai HA, multi-tenant, platform quản lý, dashboard thời gian thực, tự khắc phục sự cố.  

Hướng đến **validity nghiên cứu** trước tiên, chú trọng độ tin cậy của thí nghiệm hơn là hoàn thiện hệ thống sản xuất.  

## 21. Yêu cầu phi chức năng (Non-functional Requirements)  

- **Dễ bảo trì (Maintainability):** Code rõ ràng, comment đầy đủ. Module baseline và cải tiến tách biệt.  
- **Độ tin cậy (Reliability):** Xử lý log ngoại lệ (log trống, lỗi format) không crash. Có kiểm tra trước khi chạy mô hình.  
- **Độ trễ (Latency):** Đảm bảo latency cho pipeline inference đủ nhanh cho yêu cầu real-time (ví dụ < 1s/vòng). Nếu LLM, đếm thời gian gọi API.  
- **Khả năng mở rộng (Scalability):** Có thể mở rộng cho nhiều log stream (gần như tuần tự). Cân nhắc cấu hình cao/ thấp cho experiments.  
- **Giải thích (Explainability):** Mô tả rõ mô hình ra điểm thế nào (ví dụ tự huấn luyện contrastive có ít explainability, LLM có khả năng giải thích câu trả lời). Giữ mã nguồn và tài liệu giải thích.  
- **Bảo mật (Security):** Nếu dùng logs có dữ liệu nhạy, xử lý tuân thủ (anon). Nếu LLM, đảm bảo không lộ dữ liệu nhạy qua API.  
- **Chi phí (Cost):** Ước tính chi phí tính toán (compute hours, token). Ví dụ nếu dùng GPT-4 API, tính phí token. Đề xuất phiên bản nhỏ nếu phí cao.  

Ưu tiên đảm bảo tính **hợp lệ nghiên cứu** (kết quả có ý nghĩa khoa học) hơn yêu cầu production. Nhưng vẫn theo dõi performance cơ bản (latency) trong mục đích nghiên cứu.

## 22. Rủi ro kỹ thuật (Technical Risks)  

| Rủi ro                             | Xác suất | Tác động                 | Giải pháp giảm thiểu                                | Phương án dự phòng        |
|------------------------------------|---------:|--------------------------|-----------------------------------------------------|---------------------------|
| **Baseline không tái lập được**    | Trung bình | Cao                    | Cố gắng tìm cấu hình giống nguyên tác; sử dụng thông tin từ paper/quell debug | Nếu thất bại, báo cáo và cân nhắc baseline đơn giản hơn (như chỉ encoder+threshold). |
| **Thiếu thông tin baseline (chi tiết)** | Thấp   | Trung bình             | Tra cứu supplementary, code tác giả nếu công khai    | Dùng baseline tương tự cùng đặc tính (cùng Q1/Q2). |
| **Cải tiến không hiệu quả**       | Trung bình | Cao                    | Kiểm tra logic, điều chỉnh tham số (k top-k, weights).  | Nếu không cải thiện, báo cáo kết quả null; xem xét hướng cải tiến khác (nhanh hơn). |
| **Không gán rõ cải tiến**         | Trung bình | Trung bình             | Thực hiện ablation, so sánh chi tiết                | Chỉ báo cáo tính ảnh hưởng của mọi thay đổi đã làm (ít nhất là giới hạn). |
| **LLM đưa ra hallucination**      | Cao       | Trung bình             | Giới hạn temperature=0, kiểm tra cẩn thận đầu ra.    | Nếu LLM không ổn định, chỉ dùng module retrieval thuần túy. |
| **Lộ thông tin tương lai (data leakage)** | Thấp  | Cao                    | Kiểm soát time filter trong retrieval; dùng logs đúng thời điểm | Kiểm soát thời gian chặt chẽ, test scenario có rò rỉ. |
| **Độ trễ quá cao**                | Trung bình | Trung bình             | Tối ưu code, batching, dùng GPU nếu cần              | Giảm tần suất truy vấn, sử dụng mô hình nhỏ hơn hoặc offline xử lý. |
| **Thiếu tài nguyên tính toán**    | Thấp      | Trung bình             | Phối hợp HPC/đám mây, sử dụng cluster               | Giảm quy mô thử nghiệm; dùng subset dữ liệu nhỏ hơn. |
| **Độ phức tạp kỹ thuật**         | Thấp      | Thấp                   | Thiết kế module rõ ràng, hạn chế phụ thuộc bên ngoài  | Giảm bớt module không cần thiết. |

Mọi phương án dự phòng đều nhằm giữ mục tiêu *cụ thể* của cải tiến: nếu thực hiện thất bại, vẫn có thể trình bày kết quả baseline và các điều chỉnh đã thử.

## 23. Công cụ & tái lập (Artifact & Reproducibility)  

Lưu trữ đầy đủ:  
- **Dữ liệu:** Đường dẫn dataset gốc, phiên bản logs, nhãn anomaly (nếu có).  
- **Cấu hình:** Tất cả file YAML (dataset, baseline, improvement, model, retrieval, evaluation).  
- **Mô hình:** Mã nguồn và checkpoint baseline, mã nguồn cải tiến với commit ID.  
- **Prompt (nếu dùng):** Mẫu prompt cho LLM, tài liệu ngữ cảnh.  
- **Thiết lập:** Phiên bản Python, thư viện (requirements.txt hoặc conda env).  
- **Kết quả thô:** Logs của tất cả runs, output metric (CSV), file hình (đường cong), bảng kết quả.  
- **Script/runbook:** Hướng dẫn tái lập: command line gọi chạy lại các thử nghiệm.  

Mục tiêu: **một nhà nghiên cứu khác** có thể từ file artefact để tái lập toàn bộ quy trình, từ baseline đến improved, và thu kết quả tương tự.

## 24. Lộ trình thực hiện nghiên cứu (Research Execution Roadmap)  

- **Sprint 1 – Môi trường & Baseline:** 
  - *Mục tiêu:* Thiết lập môi trường (cài đặt libraries, Docker nếu cần), tải dataset, tái lập baseline (code/freeze).  
  - *Kết quả:* Baseline code chạy được, metrics tham khảo khớp báo cáo.  
  - *Rủi ro:* Khó tái lập model baseline → tăng thời gian debug.  

- **Sprint 2 – Xác nhận Baseline:** 
  - *Mục tiêu:* Chạy baseline với nhiều cài đặt, ghi lại metric tham chiếu (F1, recall).  
  - *Kết quả:* Báo cáo hoàn thiện baseline metrics (có CI).  
  - *Rủi ro:* Metric không đạt giống báo cáo → kiểm tra code.  

- **Sprint 3 – Cải tiến chính:** 
  - *Mục tiêu:* Triển khai module cải tiến (retrieval/LLM), đảm bảo tích hợp với pipeline.  
  - *Kết quả:* Module mới chạy được (test unit), không gây lỗi baseline.  
  - *Rủi ro:* Module mới gây lỗi latency/dữ liệu.  

- **Sprint 4 – Thí nghiệm chính:** 
  - *Mục tiêu:* So sánh Baseline (A) vs Baseline+Improvement (B) trên metrics chính.  
  - *Kết quả:* Bảng so sánh metric, thống kê p-value.  
  - *Rủi ro:* Không thấy cải thiện→nhìn lại hypothesis.  

- **Sprint 5 – Ablation/Độ bền:** 
  - *Mục tiêu:* Chạy ablation (loại bỏ từng thành phần của cải tiến). Kiểm tra Robustness (ví dụ robustness với biến đổi threshold).  
  - *Kết quả:* Kết quả đóng góp từng thành phần, phân tích nhạy với threshold.  
  - *Rủi ro:* Quá nhiều kết hợp cần chạy→ưu tiên quan trọng.  

- **Sprint 6 – Đánh giá Phát hiện sớm/Efficiency:** 
  - *Mục tiêu:* Tính toán lead time, early warning rate; đo latency pipeline.  
  - *Kết quả:* Báo cáo số liệu sớm (lead time trung bình), latency trung bình, chi phí API (nếu có).  
  - *Rủi ro:* Đo lead time khó (nếu dữ liệu thiếu nhãn thời gian chéo).  

- **Sprint 7 – Cuối cùng (Evaluation/Tài liệu):** 
  - *Mục tiêu:* Chạy cuối cùng với seed khác; tổng kết số liệu, vẽ biểu đồ; tổng hợp tài liệu, code version lock.  
  - *Kết quả:* Báo cáo final, artifact công bố (code + báo cáo chi tiết).  
  - *Rủi ro:* Nhịp deadline gấp, đảm bảo tài liệu đầy đủ.  

Mỗi sprint đều có tiêu chí nghiệm thu: (Ví dụ, Sprint1: baseline chạy đúng; Sprint4: collect results, v.v.) cùng rủi ro tương ứng.

## 25. Tiêu chí chấp nhận (Acceptance Criteria)  

- **Baseline:**  
  - Mô hình baseline chạy thành công với  metrics chuẩn theo báo cáo gốc (±5%).  
  - Pipeline không báo lỗi, tái lập được kết quả giới hạn.  
- **Cải tiến:**  
  - Module cải tiến chạy độc lập (unit test) và tích hợp hoà vào pipeline baseline.  
  - Không gây sai lệch kết quả baseline khi tắt cải tiến (improved vs baseline đều chạy được với cùng input).  
- **Thí nghiệm chính:**  
  - Cả hai cấu hình (A/B) đều chạy qua tập test, thu đủ các metric (Precision, Recall, F1, LeadTime).  
  - Đảm bảo cùng quy trình (data split, seeds) cho cả hai.  
- **Tái lập:**  
  - Tài liệu configuration tái tạo chính xác thử nghiệm.  
  - Tập tin code và môi trường versioned (ví dụ Dockerfile), có thể tái chạy.  

## 26. Khẳng định cuối cùng về thiết kế kỹ thuật (Final Technical Design Freeze)  

- **Baseline:** Mô hình phát hiện dị thường log (theo `result-5.md`), đã được xác nhận Q1/Q2.  
- **Cải tiến:** Thành phần truy hồi ngữ cảnh (RAG) tích hợp LLM.  
- **Các thành phần không đổi:** Preprocessing, embedding, mô hình cơ bản, evaluation protocol.  
- **Các thành phần mới:** Retriever module, context builder, LLM interface (nếu có).  
- **Experiment core:** So sánh A (chỉ baseline) vs B (baseline + cải tiến).  
- **Tiêu chí thành công chính:** Cải tiến có ý nghĩa về metric (ví dụ F1 tăng ≥ X%).  
- **Tiêu chí phụ:** Rút ngắn lead time, duy trì chi phí chấp nhận được, tính toán reproducible.  

Chỉ thiết kế này được chọn, đảm bảo các giả thuyết nghiên cứu (RQ/H) được kiểm tra trên baseline Q1/Q2 đã phê duyệt.

## 27. Xác minh xếp hạng Q1/Q2 và xuất bản của baseline (Q1/Q2 Verification)  

- ✅ Baseline được công bố trong giai đoạn 2023–2026.  
- ✅ Là bài báo trên tạp chí (journal) chính thức, đã peer-review (không phải arXiv/preprint).  
- ✅ Tạp chí thuộc Q1 hoặc Q2. **Chứng minh:** Ví dụ *Scientific Reports* (Li et al. 2025) có quartile Q1; hoặc *Sensors* (MDPI) 2023 là Q1 (Instrumentation).  
- ✅ Có nguồn xác minh thứ hạng: (dựa trên  hoặc trang SCImago chính thức).  
- ✅ Có DOI/metadata: ví dụ DOI in [16] (Scientific Reports 15, 38370 (2025)).  
- ✅ Baseline phải khớp hoàn toàn với thiết kế đã phê duyệt trong `result-5.md`; không tự thay thế khác.  
- ❌ Nếu không đủ bằng chứng: phải ghi rõ “Chưa đủ chứng cứ → baseline chưa đủ điều kiện”.  

(Kê khai chi tiết: Ví dụ “Tạp chí Science Reports (2025) có Impact Factor 4.9, được xếp hàng Q1, DOI:...”.)  

## 28. Ma trận truy vết cuối cùng (Final Traceability Matrix)  

| Yêu cầu nghiên cứu/Hypothesis | Thành phần kỹ thuật                | Thí nghiệm          | Metric                | Tiêu chí chấp nhận                              |
|-------------------------------|-------------------------------------|---------------------|-----------------------|-------------------------------------------------|
| **RQ1:** Độ chính xác phát hiện | Core Model + Retrieval/LLM          | A vs B (Baseline vs Improved) | F1, Precision, Recall | F1_improved > F1_baseline với p<0.05           |
| **RQ2:** Phát hiện sớm         | Retrieval/LLM + Decision Rule       | A vs B (Detection time)       | Lead Time (trung bình), False Alarm Rate | LeadTime_improved lớn hơn (sớm hơn) >= X giây |
| **RQ3:** Generalization        | Hệ thống tổng thể (pipeline)         | Cross-dataset test    | ROC-AUC, PR-AUC       | Δ ROC-AUC nhỏ (≥0) khi chuyển dataset          |
| **H1:** F1 tăng               | Core Model + Retrieval              | Controlled run A/B  | F1 Score             | Tăng F1 ít nhất 5% với CI không chồng lấn    |
| **H2:** Cảnh báo sớm hơn       | Retrieval/Context                   | Thử nghiệm lead time  | Avg Lead Time       | LeadTime giảm (điều đó nghĩa sớm hơn)        |
| **H3:** Chi phí chấp nhận được  | Toàn bộ pipeline                   | Đo latency/cost     | Latency (ms), Cost($) | Latency < giới hạn yêu cầu, Cost trong ngân sách |

Mỗi RQ/H được chỉ định rõ thành phần liên quan, cách kiểm tra trong thí nghiệm, metric dùng đánh giá, và tiêu chí để cho rằng mục tiêu đạt (ví dụ độ cải thiện ít nhất, hoặc khác biệt có ý nghĩa).

**Nguồn tham khảo chính:** Các chi tiết kỹ thuật và baseline tham khảo từ Li et al. 2025 và dữ liệu xếp loại Q1 từ nguồn chuẩn. Các định nghĩa metric từ tài liệu chuyên ngành.

