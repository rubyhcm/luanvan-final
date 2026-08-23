# Đặc tả Thiết kế Kỹ thuật (Technical Design Specification)

## 1. Xác minh Research Design (Design Freeze Verification)  
| **Yếu tố**            | **Theo result-5.md**                                           | **Giải thích kỹ thuật**                                   | **Q1/Q2 / Phát hiện**                    | **Đã thay đổi?** |
|----------------------|---------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------|-----------------|
| **Baseline**         | Li et al., 2025 (Scientific Reports)      | Mô hình *LogSentry*: BERT đối chiếu (contrastive) kết hợp với truy vấn tăng cường (retrieval-augmented). Công bố chính thức, peer-reviewed. | Tạp chí Scientific Reports (Nature) – Q1 | Không          |
| **Hạn chế**          | Không hỗ trợ cảnh báo sớm trước khi lỗi xảy ra.               | Mô hình hiện tại chỉ phát hiện bất thường sau khi các sự kiện bất thường đã xảy ra (reactive), chưa dự báo trước (predictive).      | –                                       | Không          |
| **Cải tiến mục tiêu**| Thêm thành phần dự báo/báo động sớm (**early warning**)       | Kết hợp mô hình ngôn ngữ lớn (LLM) và truy vấn dữ liệu lịch sử để nâng cao khả năng phát hiện sớm. | –                                       | Không          |
| **Đầu vào (Input)**  | Dữ liệu *raw logs* của hệ thống.                              | Dòng log thô, được chuyển thành chuỗi khóa (log key sequence) trước khi đưa vào mô hình. | –                                       | Không          |
| **Đầu ra (Output)**  | Nhãn bất thường (anomaly) và (với cải tiến) thông báo sớm.     | Nhãn phát hiện bất thường (có/không) và thời gian cảnh báo sớm (lead time) trong môi trường cải tiến.  | –                                       | Có (bổ sung lead time) |
| **Đánh giá chính**   | Độ chính xác (Precision), Độ bao phủ (Recall), F1, PR-AUC, Lead Time. | Các chỉ số đánh giá phát hiện (F1, AUC) và chỉ số cảnh báo sớm (lead time, Early Warning Rate). | –                                       | Không          |

Các thông tin trên được xác nhận không mâu thuẫn với nghiên cứu thiết kế đã được phê duyệt (`result-5.md`). Baseline và các thành phần thiết kế (RQ, giả thuyết, hạn chế, mục tiêu cải tiến) giữ nguyên theo tài liệu Design Freeze.

## 2. Phạm vi hệ thống (System Boundary)  
**Trong phạm vi:** Tất cả thành phần cần thiết để tái hiện baseline và triển khai cải tiến: bao gồm thu thập và tiền xử lý log (parser), tạo cửa sổ thời gian (windowing), biểu diễn (embedding), mô hình cơ sở (BERT) và các thành phần truy vấn (vector DB, LLM). Hệ thống chỉ nhằm phục vụ chạy thử nghiệm nghiên cứu: xử lý off-line/online log, đánh giá phát hiện sớm, thu thập số liệu.  

**Ngoài phạm vi:** Xây dựng nền tảng AIOps đầy đủ cho doanh nghiệp (dashboard, multi-tenant, HA, tự động khắc phục), các dịch vụ phụ trợ không cần thiết. Không phát triển giao diện người dùng phức tạp hay tích hợp môi trường vận hành thực tế. Hệ thống chỉ là bản triển khai thử nghiệm thuần túy, không hướng đến deployment sản xuất.

## 3. Đặc tả Triển khai Baseline (Baseline Implementation Specification)  
Trong baseline *LogSentry* được mô tả bởi Li et al. (2025), quy trình phát hiện bất thường gồm các thành phần chính sau (Baselines là _frozen reference_ không thay đổi):  

| **Thành phần**           | **Trách nhiệm**                                                       | **Đầu vào**                          | **Đầu ra**                                  | **Tham số**                          | **Phụ thuộc**         |
|-------------------------|----------------------------------------------------------------------|-------------------------------------|--------------------------------------------|--------------------------------------|----------------------|
| **Parser (Tiền xử lý)** | Phân tích log thô, trích xuất **log key sequence**.                  | Dòng log thô (text)                 | Chuỗi khóa log (mỗi khóa là template log) | Cấu hình log-templates (phần cố định) | Thư viện log parsing (ví dụ Spell/Drain) |
| **Windowing**          | Gom nhóm các log liên tiếp thành cửa sổ thời gian cố định.            | Chuỗi log liên tục theo thời gian    | Các cửa sổ log (danh sách các log key)      | Kích thước cửa sổ, bước trượt (sliding)      | –                    |
| **Biểu diễn (Representation)** | Chuyển đổi chuỗi log key thành véc-tơ đặc trưng.                 | Chuỗi khóa log từ cửa sổ             | Véc-tơ nhúng (embedding)                    | Kích thước embedding (e.g. 768)      | Mạng BERT cơ sở (pretrained)      |
| **Mô hình cơ bản (BERT)** | Phát hiện bất thường dựa trên véc-tơ log.                          | Véc-tơ embedding từ Representation | Điểm bất thường (logits/probability)       | Kiến trúc BERT, trọng số đã huấn luyện | Thư viện Transformers (PyTorch/TensorFlow) |
| **Retrieval (KNN)**     | Lưu trữ véc-tơ log có nhãn từ giai đoạn huấn luyện, tìm kiếm k gần nhất. | Véc-tơ embedding (log mới)          | Nhãn trung bình của k hàng xóm gần nhất     | Giá trị k; Cơ sở dữ liệu véc-tơ đã built từ training | Thư viện tìm kiếm ANN (FAISS/Annoy) |
| **Kết hợp (Mixture)**   | Kết hợp đầu ra mô hình BERT và kết quả KNN.                          | Score_BERT, Score_KNN              | Điểm bất thường cuối cùng (score tổng hợp)  | Trọng số kết hợp (mixture weight)     | –                    |
| **Quyết định (Decision)** | Áp dụng ngưỡng để quyết định có alert hay không.                     | Điểm bất thường cuối cùng           | Nhãn bất thường (có/không)                 | Ngưỡng cố định (ví dụ 0.5)            | –                    |
| **Đầu ra**              | Ghi nhận kết quả phát hiện.                                          | Nhãn bất thường                   | Báo cáo cảnh báo (alert)                   | –                                    | –                    |

Các tham số trên có thể tinh chỉnh khi thực hiện để tái lập lại kết quả baseline. Đặc biệt, *LogSentry* sử dụng **contrastive pre-training** trên kiến trúc BERT và sau đó fine-tune nhị phân để phân loại normal/abnormal; thêm vào đó, thành phần KNN dựa vào tính năng log giúp cải thiện tính chính xác thông qua lấy nhãn trung bình từ k hàng xóm gần nhất. Quy tắc quyết định cuối (threshold) được cố định sau khi hiệu chỉnh trên tập validation.

## 4. Đặc tả Cải tiến (Targeted Improvement Specification)  
Dựa trên hạn chế của baseline (không hỗ trợ phát hiện sớm), chỉ có **một hướng chính** được phát triển trong cải tiến:  

| **Thành phần cải tiến**     | **Đầu vào**                                 | **Trách nhiệm**                                                       | **Đầu ra**                                        | **Quan hệ với Baseline**                                        | **Giả thuyết (Hypothesis)**                                   |
|----------------------------|---------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------|
| **Hệ thống RAG-LLM (mô-đun cảnh báo sớm)** | Chuỗi log hiện tại + thông tin lịch sử (log sự cố, runbooks) | Sử dụng **Mô hình Ngôn ngữ Lớn (LLM)** kết hợp với dữ liệu truy vấn được để dự báo sự cố sớm. | Điểm bất thường có tính tới ngữ cảnh, cảnh báo sớm (khoảng thời gian dẫn trước) | Mới (thành phần bổ sung); tận dụng ngữ cảnh lịch sử/log cũ, không có trong baseline | Cải thiện độ chính xác phát hiện **và** tăng thời gian cảnh báo sớm (lead time) |

Thành phần chính này kết hợp **retrieval** từ dữ liệu lịch sử (như log sự cố đã xảy ra, runbooks) và **mô hình ngôn ngữ lớn** (ví dụ GPT-4) để đưa ngữ cảnh và kiến thức bên ngoài vào quá trình nhận dạng bất thường. Mục tiêu đặt ra (theo giả thuyết) là tăng hiệu năng (F1) và khả năng cảnh báo trước (lead time) so với baseline.

## 5. Kiến trúc Tổng thể (Overall System Architecture)  
Kiến trúc hệ thống kết hợp pipeline baseline và phần cải tiến như sau (Mỗi module kèm mô tả ngắn, trạng thái inherited/new/modified):  

- **Log Input / Parser** (Inherited): Đọc log thô, phân tích thành log key sequence. Input: dòng log; Output: khóa log.  
- **Windowing** (Inherited): Gom nhóm liên tiếp, đầu ra là cửa sổ log (nhiều log). Input: log đã parse; Output: danh sách log trong cửa sổ.  
- **Representation** (Inherited): Chuyển chuỗi log thành embedding. Input: chuỗi khóa log; Output: véc-tơ embedding.  
- **Baseline Model (BERT)** (Inherited): Xử lý embedding, cho điểm bất thường. Input: embedding log; Output: điểm anomaly. Tham khảo baseline.  
- **Baseline Retrieval (KNN)** (Inherited): Tìm k véc-tơ gần nhất trong cơ sở dữ liệu đã huấn luyện; tính trung bình nhãn. Input: embedding log; Output: nhãn trung bình (score\_knn).  
- **Improvement Retrieval (Historical KB)** (New): Duy trì cơ sở dữ liệu véc-tơ của log sự cố và tri thức. Input: embedding log; Output: tập k log tương tự (được sử dụng cho LLM).  
- **Context Builder (Prompt)** (New): Kết hợp log hiện tại với thông tin truy vấn (vd. phần trích xuất log cũ, runbook) thành ngữ cảnh cho LLM. Input: log hiện tại + kết quả retrieval; Output: prompt cho LLM.  
- **Foundation Model (LLM)** (New): Model ngôn ngữ lớn (ví dụ GPT-4) nhận prompt, trả về đánh giá nguy cơ bất thường và mô tả. Input: prompt (log + lịch sử); Output: xác suất bất thường và thông tin cảnh báo.  
- **Score Combiner** (Modified): Kết hợp điểm từ BERT và (nếu cần) LLM. Input: score\_bert, score\_llm; Output: điểm tổng hợp cuối cùng.  
- **Decision (Thresholding)** (Inherited): Áp dụng ngưỡng để ra nhãn anomalous hay không. Input: điểm bất thường tổng hợp; Output: nhãn (alert/no alert).  
- **Evaluation / Alert** (Evaluation-only): Thu thập kết quả để đánh giá offline. Input: nhãn/score; Output: báo cáo số liệu.

Mỗi module có mục đích rõ ràng (đã nêu), đầu vào/đầu ra và trạng thái (Inherited/Modified/New). Tất cả thành phần in-scope đều phục vụ mục tiêu tái tạo baseline hoặc thực hiện cải tiến, đảm bảo tính tái lập (reproducibility).

## 6. Liên kết Nghiên cứu – Hệ thống (Research-to-System Traceability)  
| **Câu hỏi nghiên cứu / Giả thuyết** | **Thành phần hệ thống**       | **Thí nghiệm**                                   | **Đo lường (Metric)**            |
|------------------------------------|-----------------------------|-----------------------------------------------|----------------------------------|
| **RQ1:** Hiệu năng phát hiện như thế nào?  | Toàn bộ hệ thống (baseline vs improved) | So sánh pipeline Baseline và Cải tiến           | F1-score (Precision/Recall)      |
| **RQ2:** Khả năng cảnh báo sớm được cải thiện? | Mô-đun cải tiến (RAG-LLM)         | Đo lead time và tỉ lệ cảnh báo trước khi lỗi xảy ra | Trung bình thời gian dẫn trước (Lead Time), Early Warning Rate |
| **RQ3:** Độ hiệu quả & tổng quát?         | Mô hình và cơ sở dữ liệu (efficientcy) | Đánh giá độ trễ, chi phí token; thử nghiệm trên hệ thống khác | Latency, Token Cost, F1-cross-system |
| **H1:** Cải tiến tăng F1 so với baseline.      | Xử lý dòng log, mô hình BERT   | Baseline vs Improved (controlled)            | F1 (Improved > Baseline)         |
| **H2:** Cải tiến tăng Lead Time.         | Hệ thống LLM                 | So sánh thời gian cảnh báo giữa hai phiên bản | Trung bình Lead Time (Improved > Baseline) |
| **H3:** Chi phí bổ sung trong mức cho phép.      | Tăng thêm LLM (overhead)     | Đo độ trễ, sử dụng tài nguyên               | Latency_IMPR – Latency_BASE < Threshold |

Mỗi yêu cầu nghiên cứu (RQ) và giả thuyết (H) được ánh xạ đến thành phần hệ thống tương ứng, thí nghiệm kiểm chứng và chỉ số đo đạc cụ thể.

## 7. Luồng Dữ liệu (Data Flow Specification)  
Luồng chính của hệ thống: 

- **Offline (Huấn luyện / Chuẩn bị):** Huấn luyện mô hình baseline; xây dựng cơ sở dữ liệu véc-tơ (vector DB) từ embedding log đã huấn luyện; (nếu cần) tạo cơ sở dữ liệu tri thức (runbooks, cảnh báo cũ).  
- **Online (Inference):** 
  1. Log mới đến → Parser chuyển thành khóa log.  
  2. Gộp vào cửa sổ (windowing) → tạo chuỗi khóa.  
  3. Biểu diễn (embedding) → đưa vào mô hình BERT baseline.  
  4. Kết quả BERT cho score\_bert. Đồng thời, **Improvement**: Query véc-tơ embedding log tới vector DB lịch sử (ví dụ log sự cố) → nhận top-k tương tự.  
  5. Kết hợp prompt: log hiện tại + thông tin log cũ thu được → gửi vào LLM.  
  6. LLM trả về score\_llm (điểm bất thường) và nội dung giải thích.  
  7. **Combine:** Tính tổng hợp score = w1·score_bert + w2·score_llm.  
  8. So sánh với ngưỡng → output cảnh báo bất thường và thời gian.  
- **Đánh giá:** So sánh kết quả với ground truth, tính metrics (precision, recall, lead time, v.v.). Luồng này offline/offline-detect và online ảnh hưởng đến độ trễ.

Các thành phần offline (huấn luyện BERT, xây dựng DB) và online (phân tích log, truy vấn, inference) được tách bạch. Phần latency-sensitive: tiền xử lý log, embed và gọi mô hình BERT; phần LLM có độ trễ lớn hơn nhưng cần để kiểm thử hiệu quả cải tiến.

## 8. Thiết kế Dữ liệu theo Thời gian (Temporal Data Design)  
| **Nguồn dữ liệu**          | **Dấu thời gian**           | **Có sẵn tại thời điểm dự đoán?** | **Cho phép sử dụng?** |
|----------------------------|----------------------------|----------------------------------|---------------------|
| **Log hệ thống (dòng log)** | Thời gian tạo log (t)        | Có (log được sinh liên tục)      | Được (dữ liệu hiện tại)    |
| **Nhãn bất thường (ground truth)** | Thời gian sự kiện lỗi (t_failure) | Không (chỉ biết sau khi xảy ra) | Không (dùng chỉ để đánh giá) |
| **Log lịch sử / sự cố cũ**   | Thời gian sinh mỗi log cũ   | Có (từng xảy ra trước đó)        | Được (dùng cho retrieval)   |
| **Runbooks / Tài liệu**    | Ngày cập nhật tài liệu      | Có (luôn có sẵn)                | Được (kiến thức nền)      |
| **Dữ liệu tương lai**      | Thời gian > hiện tại        | Không (chưa xảy ra)             | Không cho phép              |

Thiết kế dữ liệu đảm bảo không dùng thông tin “tương lai” vượt quá thời điểm dự đoán. Mọi dữ liệu sử dụng (như log đã thu thập và sự cố đã diễn ra) đều có timestamp ≤ thời điểm hiện tại của luồng chạy. Các bản ghi nhãn lỗi chỉ để đánh giá sau khi dự đoán, không dùng làm input.

## 9. Kiến thức / Thu hồi (Knowledge / Retrieval)  
- **Kiến thức (Knowledge):** Dữ liệu lịch sử liên quan đến lỗi/bất thường: log sự cố đã biết, runbooks, tài liệu xử lý sự cố, cơ sở tri thức (KB) về lỗi hệ thống. Những nguồn này cung cấp ngữ cảnh thêm cho việc phát hiện sớm.  
- **Thu hồi (Retrieval):** Sử dụng phương pháp **dense retrieval** (vector) để tìm kiếm thông tin liên quan. Cụ thể:  
  - **Truy vấn (Query):** Sử dụng embedding của log hiện tại (hoặc đoạn log gần đây) làm truy vấn.  
  - **Kho ứng viên (Candidate Pool):** Tập véc-tơ của log lịch sử hoặc các mảnh thông tin trong KB.  
  - **Embedding:** Giữ embedding của các log/KB trong cơ sở dữ liệu (từ bước offline).  
  - **Sắp xếp (Ranking):** Tính độ tương đồng cosine giữa query và tất cả candidates.  
  - **Top-k:** Chọn k mục tiêu top (ví dụ k=5 hoặc 10).  
  - **Lọc (Filtering):** Chỉ sử dụng mục có timestamp ≤ hiện tại (không dùng thông tin tương lai). Có thể giới hạn độ khác biệt thời gian nếu cần (ví dụ chỉ các sự cố gần nhất về mặt thời gian hoặc về log pattern).  
- **Mục đích thu hồi:** Cung cấp ngữ cảnh liên quan từ lịch sử để LLM có thể sử dụng thông tin tương tự trong dự đoán anomaly. Các mục tiêu liên quan giúp LLM cải thiện độ chính xác và dự đoán sớm (tương ứng với giả thuyết H1, H2).

## 10. Xây dựng Ngữ cảnh (Context Construction)  
Khi sử dụng LLM/Hoạt RAG, cần kết hợp thông tin truy vấn vào prompt:  
- **Nội dung chính:** Ghi lại các mẫu log gần đây (log current) dưới dạng văn bản hoặc biểu diễn có ý nghĩa.  
- **Ngữ cảnh bổ sung:** Thêm các bản tóm tắt hoặc trích đoạn từ log lịch sử, sự cố tương tự tìm được (qua retrieval), hoặc runbook (nếu liên quan).  
- **Metadata:** Kèm theo thông tin thời gian, độ nghiêm trọng, component liên quan.  
- **Thứ tự:** Tổ chức theo thời gian hoặc mức độ liên quan (ví dụ, sự kiện gần với log mới nhất trước).  
- **Giới hạn ngữ cảnh:** Đảm bảo tổng số token không vượt quá giới hạn (ví dụ 2048 token). Nếu cần, ưu tiên giữ lại các đoạn quan trọng nhất (log nhiều thông tin, lỗi liên quan).  
- **Kiểm soát nhiễu:** Loại bỏ nội dung không liên quan hoặc quá cũ (độ tương tự quá thấp). Chỉ sử dụng ngữ cảnh phù hợp với thời điểm hiện tại.  

Đảm bảo **không để lọt thông tin tương lai**. Tất cả ngữ cảnh được chọn phải có timestamp trước hoặc bằng thời điểm dự đoán.

## 11. Mô hình Nền tảng / Huấn luyện (Foundation Model / Training)  
- **Mô hình nền tảng (Foundation Model):** Sử dụng một LLM có sẵn (ví dụ GPT-4 qua API) làm lõi phân tích ngữ cảnh. Phiên bản của mô hình phải cố định và ghi lại (ví dụ: GPT-4, version tại thời điểm năm 2026).  
- **Giao diện mô hình:** Input: prompt (kết quả Context Builder); Output: xác suất bất thường hoặc nhãn anomaly (và có thể một đoạn giải thích). Cấu hình inference: nhiệt độ = 0 (deterministic), top-k/top-p thích hợp để đảm bảo kết quả ổn định.  
- **Huấn luyện:** Không đào tạo thêm hay fine-tune mô hình. Mô hình được sử dụng nguyên bản (có thể từ OpenAI/GPT hoặc mô hình tương đương). Điều này giữ cho baseline và improved sử dụng chung mô hình nền nếu có (trong trường hợp baseline cũng dùng LLM, nhưng baseline hiện tại không dùng LLM).  
- **Các thông số:** Ghi lại rõ version model, phương thức gọi (API), giới hạn token và phí (nếu tính).

## 12. Luồng Inference (Inference Workflow)  
1. **Log tới (arrival):** Log mới được ghi nhận (Online).  
2. **Parser:** Chuyển đổi log thành khóa log (Online; latency-sensitive).  
3. **Windowing:** Tập hợp thành cửa sổ (Online; latency-sensitive).  
4. **Embedding:** Tạo embedding (Online; latency-sensitive).  
5. **Baseline Inference:** Mô hình BERT dự đoán điểm bất thường (Online; latency-sensitive).  
6. **Retrieval:** Tính query embedding, truy vấn cơ sở dữ liệu lịch sử, lấy top-k (Online; có độ trễ trung bình).  
7. **Context:** Kết hợp log mới với thông tin truy vấn, tạo prompt (Online; preprocessing).  
8. **LLM Inference:** Gửi prompt đến LLM, nhận kết quả anomaly score (Online; latency cao).  
9. **Score Combine:** Kết hợp điểm từ BERT và LLM (Online).  
10. **Thresholding:** Áp dụng ngưỡng, tạo cảnh báo (Online; latency thấp).  
11. **Output:** Xuất cảnh báo sớm (alert) hoặc cảnh báo muộn, lưu trữ cho đánh giá (Online/Evaluation).  

Các bước (2-5) và (9-10) cần đáp ứng thời gian thực (nhanh), trong khi bước LLM (8) có thể chịu độ trễ lớn hơn (sẽ được đánh giá trong phần hiệu năng). Bước offline (chuẩn bị vector DB, cấu hình LLM) được tách riêng.

## 13. Giao diện Anomaly/Early Detection (Interface)  
- **Anomaly Score:** Giá trị liên tục (trong [0,1]) do mô hình cung cấp, đo độ lệch so với bình thường (cao = khả năng anomaly cao). Score tổng hợp được lấy sau khi kết hợp BERT và LLM. Interpret: 0 nghĩa chắc chắn bình thường, 1 chắc chắn bất thường.  
- **Quy tắc quyết định:** Ngưỡng cố định (ví dụ 0.5) được áp dụng lên score để phân lớp nhị phân (normal vs anomalous). Ngưỡng này được hiệu chỉnh (calibrated) trên tập valid (có thể dùng percentile hoặc độ dư liệu phù hợp). Tham số ngưỡng nằm trong `baseline.yaml`.  
- **Early Detection:** Định nghĩa “cảnh báo sớm” là khi mô hình phát hiện bất thường trước thời điểm thực tế xảy ra sự cố. Lead time được tính = (thời điểm sự cố xảy ra) – (thời điểm cảnh báo). Nếu >0 thì là cảnh báo trước; nếu ≤0 thì cảnh báo muộn hoặc quá trễ. Các chỉ số sẽ ghi nhận tỷ lệ cảnh báo trước failure, thời gian dẫn trước trung bình (mean lead time). **Lưu ý:** Score bất thường không đồng nhất với cảnh báo sớm – chúng ta tách riêng khái niệm: score thể hiện xác suất anomaly, trong khi early detection đo khoảng cách thời gian so với sự kiện thực.

## 14. Cấu hình (Configuration)  
Cấu hình được quản lý qua các file YAML:  

- **dataset.yaml:**  
  - `path`: (string) đường dẫn dataset;  
  - `split_ratio`: (float) tỷ lệ chia tập train/valid/test;  
  - `seed`: (int) hạt giống ngẫu nhiên cho chia tập.  
- **baseline.yaml:**  
  - `model_checkpoint`: (string) đường dẫn tới trọng số BERT;  
  - `threshold`: (float, default=0.5, range [0,1]) ngưỡng phân lớp;  
  - `window_size`: (int) kích thước cửa sổ log;  
  - `slide_step`: (int) bước trượt;  
- **improvement.yaml:**  
  - `knn_k`: (int, default=5, range ≥1) số hàng xóm trong retrieval;  
  - `llm_model`: (string) tên/phiên bản LLM sử dụng (ví dụ “gpt-4”);  
  - `context_max_tokens`: (int, default=2048) giới hạn tổng token cho prompt;  
  - `combine_weight`: (float, default=0.5) hệ số kết hợp điểm từ BERT và LLM.  
- **model.yaml:** (cấu hình mô hình BERT)  
  - `embedding_dim`: (int, default=768);  
  - `num_layers`: (int) số lớp transformer;  
  - `dropout`: (float, default=0.1).  
- **retrieval.yaml:**  
  - `index_path`: (string) lưu trữ vector DB;  
  - `metric`: (string) kiểu đo khoảng cách (ví dụ “cosine”);  
  - `time_filter`: (duration) chỉ lấy log trong khoảng thời gian gần nhất (tuỳ chọn).  
- **evaluation.yaml:**  
  - `metrics`: (list) danh sách metrics cần tính (Precision, Recall, F1, LeadTime, v.v.);  
  - `early_window`: (int) thời gian (phút/giây) xem xét là cảnh báo sớm.  
- **experiment.yaml:**  
  - `exp_id`: (string) mã chạy thử nghiệm;  
  - `seed`: (int) hạt giống cho tái lập;  
  - `baseline_version`: (string) commit hoặc nhãn version baseline;  
  - `improvement_version`: (string) commit/improvement;  
  - `dataset_version`: (string) nhãn data;  
  - `git_commit`: (string) hash mã nguồn hiện tại.

Mỗi tham số trên bao gồm kiểu, giá trị mặc định và ý nghĩa cụ thể (ví dụ threshold để điều khiển tỉ lệ dương giả).

## 15. Quản lý Thí nghiệm (Experiment Management)  
Mỗi lần chạy thí nghiệm được ghi lại đầy đủ:  
- **ID thí nghiệm (Run ID):** mã định danh (UUID hoặc timestamp).  
- **Hạt giống ngẫu nhiên (Seed):** để sao chép kết quả.  
- **Phiên bản dữ liệu (Dataset version):** commit/git tag của data (hoặc checksum).  
- **Phiên bản mô hình Baseline/Improvement:** commit hash hoặc version thư viện dùng cho baseline và cải tiến.  
- **Cấu hình (Config snapshot):** lưu trữ các file YAML cấu hình (dataset.yaml, baseline.yaml, ...).  
- **Kết quả và artifacts:** bao gồm file metrics (F1, AUC, lead time), log chi tiết (stdout), model weights (nếu mới huấn luyện), vector DB (nếu có).  
- **Quản lý:** Sử dụng công cụ thích hợp (ví dụ MLflow, W&B, hoặc ghi chép thủ công) để theo dõi và lưu trữ. Mục tiêu cho phép bất kỳ ai tái tạo đúng kết quả từ các thông tin trên.  

## 16. So sánh Có Kiểm soát (Controlled Comparison)  
Để đảm bảo chỉ khác biệt ở cải tiến chính, so sánh giữa hai trường hợp sau:  
- **A — Baseline nguyên bản (Original Q1/Q2 Baseline)**  
- **B — Baseline + Cải tiến chính**  

Giữ cố định tối đa các yếu tố sau:  

| **Yếu tố**       | **Baseline**                         | **Improved**                             | **Kiểm soát?** |
|------------------|--------------------------------------|------------------------------------------|---------------|
| **Dataset**      | Dataset gốc (phân chia train/test)  | Giống Baseline                           | Có            |
| **Tiền xử lý**   | Parser, windowing như baseline      | Giống Baseline                           | Có            |
| **Mô hình**      | BERT dự đoán (LogSentry) | BERT giống Baseline + LLM (thêm module)   | Không (LLM mới) |
| **Prompt**       | Không (chỉ BERT)                    | Có (thành phần prompt cho LLM)           | Không         |
| **Threshold**    | Ngưỡng cố định (ví dụ 0.5)          | Cùng ngưỡng                              | Có            |
| **Cải tiến**     | Không                               | RAG + LLM (main improvement)             | Không         |
| **Đánh giá**     | Bằng nhau (Precision, Recall, etc.) | Bằng nhau                                | Có            |

Ngoại trừ thành phần cải tiến (LLM/RAG) và các thành phần liên quan (prompt, retrieval lịch sử), tất cả các yếu tố khác như dữ liệu, tiền xử lý, sơ đồ huấn luyện và đánh giá đều được giữ nguyên giữa hai trường hợp.

## 17. Ablation  
Nếu cải tiến có nhiều thành phần phụ trợ, tiến hành thử nghiệm **ablation** để đánh giá đóng góp của từng phần:  
- **Full cải tiến:** Triển khai đầy đủ RAG + LLM.  
- **Loại bỏ thành phần chính:** Ví dụ, chạy lại pipeline chỉ với BERT (cơ sở) để so sánh (đây cơ bản là Baseline).  
- **Thử nghiệm tùy chọn:** Nếu có thể, nghiệm thu thành phần con của cải tiến (ví dụ chỉ dùng retrieval cũ mà không dùng LLM) để tách biệt hiệu quả.  

Mục tiêu là xác định phần nào của cải tiến góp phần chính vào sự cải thiện quan sát được. Trong trường hợp cải tiến chỉ thêm một mô-đun LLM, so sánh Baseline vs Cải tiến thường là đủ để đánh giá.  

## 18. Hạ tầng Đánh giá (Evaluation Infrastructure)  
- **Phát hiện (Detection):** Sử dụng các chỉ số chuẩn: Precision, Recall, F1-score cho nhãn anomaly. Ngoài ra tính các chỉ số PR-AUC, ROC-AUC nếu cần.  
- **Cảnh báo sớm (Early Detection):** 
  - *Time-to-Detection:* Thời gian từ lúc anomaly thực sự xảy ra đến lúc cảnh báo.  
  - *Lead Time:* Trung bình (sự cố – cảnh báo) trong trường hợp phát hiện trước.  
  - *Early Warning Rate:* Tỷ lệ anomaly được cảnh báo trước sự cố.  
  - *False Alarm Rate:* Số cảnh báo sai tính trên tổng cảnh báo.  
  - *Detection Before Failure:* Tỉ lệ những lần cảnh báo được xảy ra trước failure.  
- **Hiệu năng (Efficiency):** Độ trễ xử lý mỗi log (latency), chi phí token (số token đốt cho LLM), sử dụng bộ nhớ/compute. Đo throughput (logs/giây) nếu cần.  
- **Tổng quát hoá (Generalization):** Thử nghiệm trên các dataset hoặc hệ thống khác nhau (nếu có) để kiểm tra tính ổn định (ví dụ *cross-system* test).  

## 19. Thống kê / Tái lập (Statistical / Reproducibility)  
- **Số lần chạy (Runs):** Thực hiện nhiều lần chạy (ví dụ ≥5) với các hạt giống khác nhau để đo độ ổn định.  
- **Hạt giống:** Ghi chép rõ seed ngẫu nhiên cho từng thử nghiệm.  
- **Khoảng tin cậy:** Tính trung bình và độ tin cậy (95% CI) của các chỉ số chính (F1, lead time, v.v.).  
- **Kiểm định thống kê:** Sử dụng kiểm định phù hợp (ví dụ t-test) để so sánh kết quả giữa Baseline và Improved, báo p-value.  
- **Kích thước hiệu ứng:** Nếu có, tính Cohen’s d hoặc khác để đo mức độ khác biệt.  
- **Tính lặp lại:** Nếu dùng LLM, ghi phiên bản, cấu hình sampling (đã đặt temperature=0, …) để đảm bảo kết quả có thể tái tạo. Lưu prompt và trả lời từ LLM.  
- **Tài liệu:** Mọi tham số ngẫu nhiên, cấu hình đều phải ghi lại để người khác có thể tái lập thử nghiệm.

## 20. Phạm vi Triển khai (Deployment Scope)  
- **Bắt buộc:** Môi trường thử nghiệm đầy đủ (script/Python, Docker container, GPU nếu cần) cho các chạy thí nghiệm trong luận án. Mã nguồn cần được version control.  
- **Tùy chọn:** (Nếu cần) Cấu hình đơn giản để demo khái niệm (ví dụ API REST đơn giản cho LLM), nhưng không yêu cầu.  
- **Ngoài phạm vi:** Xây dựng hạ tầng production phức tạp (multi-tenant, high-availability, cảnh báo tự động, giao diện người dùng) không nằm trong scope. Chỉ triển khai sơ bộ (Docker/GPU) để minh hoạ khả năng thực thi kết quả nghiên cứu nếu cần.

## 21. Yêu cầu Phi Chức năng (Non-functional Requirements)  
- **Khả năng duy trì (Maintainability):** Mã nguồn được tổ chức rõ ràng, có tài liệu. Cấu hình linh hoạt (YAML) để dễ thay đổi tham số.  
- **Độ tin cậy (Reliability):** Pipeline xử lý lỗi ổn định, tường minh (log thông báo rõ ràng).  
- **Độ trễ (Latency):** Giới hạn thời gian inference (đặc biệt baseline). LLM làm tăng độ trễ; cần đo và đảm bảo trong phạm vi chấp nhận (như ≤ vài giây).  
- **Khả năng mở rộng (Scalability):** Hạ tầng có thể xử lý lượng log lớn (tăng kích thước cửa sổ hoặc tốc độ log). Vector DB và LLM cần scale.  
- **Giải thích (Explainability):** LLM cung cấp khả năng giải thích ngữ cảnh (cháu) nhằm tăng tính minh bạch. BERT kết hợp feature input rõ ràng (log keys).  
- **Bảo mật (Security):** Log có thể chứa thông tin nhạy cảm, vì vậy giao tiếp với LLM (nếu dùng dịch vụ bên ngoài) cần xem xét ẩn danh hóa hoặc hạn chế thông tin.  
- **Chi phí (Cost):** Sử dụng LLM thường tốn phí (token); cần giám sát và tối ưu token usage. Pipeline cần tối ưu về tài nguyên (GPU vs CPU).  
Ưu tiên tập trung vào giá trị nghiên cứu (độ chính xác, phát hiện sớm) hơn là các yêu cầu sản xuất (chi phí thấp, uptime cao).

## 22. Rủi ro Kỹ thuật (Technical Risks)  
| **Rủi ro**                            | **Xác suất** | **Tác động** | **Biện pháp giảm thiểu**                                | **Phương án dự phòng (Fallback)**                      |
|---------------------------------------|------------:|-------------|-------------------------------------------------------|-------------------------------------------------------|
| **Reproduce Baseline**               | Trung bình  | Cao         | Liên hệ tác giả để làm rõ chi tiết; sử dụng dataset mẫu công khai. | Giảm phạm vi: sử dụng baseline đơn giản hơn hoặc dataset khác (nếu không tái tạo được). |
| **Cải tiến không cải thiện**         | Trung bình  | Trung bình  | Thử nghiệm tuning tham số; kiểm tra các giá trị của `combine_weight`.  | Nếu thất bại, hủy bỏ LLM chỉ dùng retrieval đơn; hoặc dừng cải tiến, tập trung phân tích nguyên nhân. |
| **LLM (Hallucination, biến thiên)** | Cao         | Cao         | Thiết lập temperature=0, sử dụng version model cố định; kiểm tra output sanity. | Ngưng dùng LLM nếu không tin cậy, chuyển sang chỉ dùng baseline/KNN. |
| **Retrieval không phù hợp**         | Trung bình  | Trung bình  | Thiết lập ngưỡng tương tự tối thiểu; lọc theo thời gian; tinh chỉnh k.  | Giới hạn truy vấn, fallback là không dùng retrieval (giống baseline). |
| **Chi phí/Độ trễ cao**             | Cao         | Cao         | Tối ưu pipeline (xử lý bất đồng bộ, caching kết quả LLM); chỉ dùng LLM khi cần. | Giảm độ phức tạp: xử lý offline nhiều hơn, hoặc chuyển sang mô hình nhẹ hơn (tinyGPT) nếu cần. |
| **Độ phức tạp Đường dẫn**          | Trung bình  | Trung bình  | Thiết kế pipeline theo mô-đun rõ ràng, kiểm thử từng phần.                | Nếu quá phức tạp, tập trung vào phiên bản nhỏ hơn của cải tiến (ví dụ chỉ retrieval hoặc chỉ LLM) để đảm bảo tính khả thi. |

Các phương án dự phòng nhằm duy trì ít nhất một phiên bản hoạt động (ví dụ chỉ baseline hoặc một phần cải tiến tối giản) nếu rủi ro xảy ra.

## 23. Artifact & Tái lập (Artifact & Reproducibility)  
Lưu trữ đầy đủ các thành phần cần thiết cho tái lập kết quả:  
- **Dữ liệu:** Link đến nguồn dataset, hoặc mã định danh (hash) nếu dataset private.  
- **Cấu hình:** Tất cả file YAML (dataset.yaml, baseline.yaml, etc.) kèm ý nghĩa tham số.  
- **Mã nguồn:** Repository chứa code tiền xử lý, mô hình baseline và mã cải tiến.  
- **Phiên bản mô hình:** Ghi rõ version/framework và weights (hoặc đường dẫn tải).  
- **Prompt:** Tập hợp prompt mẫu và kết quả trả lời từ LLM để kiểm tra.  
- **Thiết lập retrieval:** Thông tin cách xây dựng vector DB (embedding model, log sử dụng).  
- **Tham số thí nghiệm:** Seed, timestamp, exp ID, ghi nhận outputs.  
- **Kết quả thô:** Bao gồm file metrics, log chạy và đồ thị/chính xác.  
- **Môi trường:** File yêu cầu thư viện (requirements.txt) hoặc Dockerfile để dựng môi trường.  

Mục tiêu: **đảm bảo người khác có thể tái lập đầy đủ so sánh giữa Baseline và Improved** chỉ dựa trên các artifact này.

## 24. Lộ trình Thực thi Nghiên cứu (Research Execution Roadmap)  
**Sprint 1 – Môi trường & Baseline:** Thiết lập môi trường phát triển (Python, GPU). Tích hợp mã hoặc viết lại baseline (*LogSentry*).  
- *Mục tiêu:* Cài đặt và chạy được pipeline baseline trên dataset.  
- *Kết quả:* Model baseline chạy ổn định, cho ra output anomaly.  
- *Tiêu chí:* Phân tích kết quả giống (±5%) so với kết quả đã công bố (nếu có).  
- *Rủi ro:* Thiếu tài liệu baseline (tìm thêm thông tin); thiếu dữ liệu (sử dụng synthetic logs mẫu).  

**Sprint 2 – Xác thực Baseline:** Chạy baseline trên tập thử, ghi lại các metrics.  
- *Mục tiêu:* Định vị bộ tham số baseline tốt (ngưỡng, window) để tái lập F1 gốc.  
- *Kết quả:* Bảng kết quả baseline (Precision, Recall, F1, AUC).  
- *Tiêu chí:* F1 và các chỉ số trong khoảng dung sai so với công bố.  

**Sprint 3 – Triển khai Cải tiến:** Phát triển phần retrieval và tích hợp LLM.  
- *Mục tiêu:* Xây dựng chức năng truy vấn cơ sở dữ liệu log lịch sử và gọi LLM.  
- *Kết quả:* Mô-đun cải tiến trả về score\_llm.  
- *Tiêu chí:* Cải tiến module chạy ổn định trên input giả lập (log bất thường và một số ngữ cảnh). Không ảnh hưởng xấu đến baseline.  

**Sprint 4 – Thực nghiệm chính:** Chạy thí nghiệm đối chứng Baseline vs Improved.  
- *Mục tiêu:* Thu thập số liệu đối chiếu (độ chính xác, lead time).  
- *Kết quả:* Số liệu F1, Recall, Precision và lead time của cả hai trường hợp.  
- *Tiêu chí:* Đảm bảo dùng chung protocol, cùng dữ liệu để so sánh.  

**Sprint 5 – Ablation / Robustness:** Thực hiện thí nghiệm loại bỏ thành phần. Phân tích những trường hợp lỗi.  
- *Mục tiêu:* Xác nhận cải thiện là do thành phần chính (LLM). Kiểm tra độ nhạy với parameter.  
- *Kết quả:* Số liệu F1 khi loại bỏ LLM, báo cáo lỗi mẫu.  
- *Tiêu chí:* Hiệu suất giảm về mức baseline khi LLM bị loại.  

**Sprint 6 – Phân tích Early Detection / Hiệu năng:** Đánh giá lead time, tỉ lệ cảnh báo trước, và đo đạc độ trễ/chi phí.  
- *Mục tiêu:* Kiểm chứng giả thuyết về cảnh báo sớm. Ước lượng chi phí (token, latency).  
- *Kết quả:* Giá trị lead time trung bình, tỉ lệ cảnh báo sớm, độ trễ trung bình mỗi log.  
- *Tiêu chí:* Lead time tăng so với baseline, latency chấp nhận được (e.g., không vượt 5s).  

**Sprint 7 – Đánh giá cuối & Hoàn thiện:** Chạy lại tất cả thử nghiệm, tổng hợp kết quả, tính thống kê, đóng gói artifact.  
- *Mục tiêu:* Hoàn thiện thử nghiệm cuối cùng, tạo báo cáo và chuẩn bị nộp tài liệu.  
- *Kết quả:* Đồ thị, bảng, số liệu tổng hợp; script cho reproducibility.  
- *Tiêu chí:* Tất cả metric được thu thập; phân tích thống kê được thực hiện; artifact (code + data) đã lưu.

## 25. Tiêu chí Chấp nhận (Acceptance Criteria)  
- **Baseline:** Chạy được pipeline baseline, thu được các metric tham khảo tương đương (trong dung sai định sẵn). Dữ liệu và mô hình đã xác định.  
- **Cải tiến:** Mô-đun cải tiến triển khai độc lập, không làm thay đổi kết quả baseline ngoài mục tiêu. Đầu ra hợp lệ (score, lead time) sinh ra đúng định dạng.  
- **Thử nghiệm chính:** Cùng cấu hình đánh giá giữa Baseline và Improved. Thu thập đầy đủ metrics đã định. Thực hiện nhiều lần chạy hoàn chỉnh.  
- **Tái lập:** Cấu hình và mã nguồn phải cho phép tái sinh kết quả. Mọi tham số, seed được ghi lại. Artifact versioning đảm bảo phục hồi môi trường.

## 25A. Xác minh Cuối Baseline (Final Baseline Eligibility Verification)  
- [x] **Baselines xuất bản 2023–2026:** Li et al., 2025.  
- [x] **Bài báo chính thức, peer-review:** Scientific Reports (Nature) – đã peer-review.  
- [x] **Tạp chí Q1/Q2:** Scientific Reports – Quartile Q1.  
- [x] **Nguồn xác minh Quartile:** Nguồn Scimago (Nature website).  
- [x] **Có DOI/metadata:** DOI: 10.1038/s41598-025-22208-7.  
- [x] **Đúng baseline đã phê duyệt:** Đây chính là *LogSentry (Li et al. 2025)* như trong result-5.  
- [x] **Không thay baseline khác:** Giữ nguyên baseline đã phê duyệt.  
- [x] **Hạn chế và cải tiến đúng:** Hạn chế “thiếu phát hiện sớm” và cải tiến “thêm LLM/RAG” vẫn khớp với Design Freeze.

Nếu bất kỳ điều kiện nào trên không đáp ứng, phải báo và không bàn giao thiết kế.

## 26. Kết luận Thiết kế Kỹ thuật (Final Technical Design Freeze)  
- **Baseline:** Mô hình LogSentry (Li et al. 2025, Scientific Reports Q1) sử dụng BERT đối chiếu + truy vấn KNN.  
- **Cải tiến chính:** Thêm hệ thống RAG-LLM tích hợp (mô hình ngôn ngữ lớn + truy vấn kiến thức lịch sử) để cảnh báo sớm.  
- **Không đổi:** Các thành phần xử lý log ban đầu (parser, windowing, BERT, KNN retrieval) vẫn giữ nguyên.  
- **Thêm/sửa đổi:** Thêm modules: Cơ sở dữ liệu kiến thức (log lịch sử, runbook); Xây dựng prompt; Gọi LLM; Kết hợp score. Sửa đổi quyết định: kết hợp thêm score từ LLM.  
- **Thí nghiệm cốt lõi:** So sánh có kiểm soát giữa (A) Baseline và (B) Baseline + RAG-LLM (Improved). Đảm bảo chỉ có cải tiến ảnh hưởng.  
- **Tiêu chí chính:** Tăng hiệu năng phát hiện (F1) so với baseline.  
- **Tiêu chí phụ:** Tăng lead time (cảnh báo sớm hơn); cải thiện robustness. Giữ latency trong giới hạn chấp nhận được.

## 27. Xác minh Q1/Q2 và Xuất bản (Q1/Q2 Ranking and Publication Verification)  
**Scientific Reports | 2025 | Scimago SJR | Q1 | Xuất bản chính thức (peer-reviewed) | DOI: 10.1038/s41598-025-22208-7**  

Tạp chí Scientific Reports là tạp chí đa ngành của Nature (Q1 theo Scimago). Bài báo “Log anomaly detection based on contrastive learning and retrieval augmented” (Li et al., 2025) được xuất bản chính thức, có DOI và đã peer-review. Các thông tin này đảm bảo Baseline thỏa mãn mọi tiêu chí yêu cầu.

## 28. Ma trận Liên kết RQ/HP (Final Traceability Matrix)  
| **RQ / Giả thuyết (H)**            | **Thành phần hệ thống**       | **Thí nghiệm**            | **Đo lường (Metric)**      | **Tiêu chí chấp nhận**                     |
|------------------------------------|-----------------------------|-------------------------|---------------------------|-------------------------------------------|
| **RQ1:** Hiệu năng phát hiện       | Pipeline đầy đủ             | Baseline vs Improved    | F1-score                  | F1<sub>Impr</sub> ≥ F1<sub>Base</sub> + δ  |
| **RQ2:** Cảnh báo sớm tốt hơn?     | Module RAG-LLM              | Đo lead time            | Lead Time trung bình      | Lead Time<sub>Impr</sub> > 0 (cao hơn baseline) |
| **RQ3:** Tổng quát/Hiệu quả       | Pipeline + Hạ tầng (GPU)    | Thử nghiệm cross-dataset | F1, Latency              | Khả năng general tốt (F1 ổn định), Latency trong hạn |
| **H1:** F1 cải tiến                | BERT + LLM                  | A vs B (controlled)     | F1-score                  | F1<sub>Impr</sub> > F1<sub>Base</sub>      |
| **H2:** Lead time tăng            | LLM module                 | Đo lead time            | Thời gian cảnh báo sớm    | Lead Time trung bình tăng so với baseline |
| **H3:** Chi phí hợp lý            | Pipeline RAG-LLM            | Đo latency và token     | Latency (ms), Token cost | Latency tăng không quá X%; chi phí token có thể chấp nhận |

Mỗi RQ/H được gắn với thành phần hệ thống chịu trách nhiệm, phương pháp thí nghiệm và chỉ số tương ứng. Tiêu chí chấp nhận đặt ra ngưỡng hiệu quả (ví dụ F1 tăng Δ) và đảm bảo tính tin cậy cũng như hiệu suất đủ tốt cho mục tiêu nghiên cứu.

**Tổng hợp:** Bản thiết kế kỹ thuật trên đảm bảo định nghĩa rõ ràng Baseline đã đóng băng, giới hạn hệ thống, pipeline baseline chi tiết, mô-đun cải tiến và kế hoạch thí nghiệm đầy đủ. Việc triển khai phải tuân thủ nghiêm ngặt design freeze: không thay đổi RQ/hypotheses, chỉ thêm một cải tiến duy nhất, giữ mọi thứ còn lại không đổi, tập trung đánh giá phát hiện sớm và tính tái lập của nghiên cứu. Các nguồn tham khảo đã được trích dẫn ở những phần tương ứng để minh chứng cho tính hợp lệ của baseline và các đặc tả kỹ thuật.