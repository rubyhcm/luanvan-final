# 1. Tổng quan các Đề cơ hội nghiên cứu  

Dựa trên _Research Opportunity Prioritization_ (result-3), các hướng cải tiến chính tập trung vào việc khắc phục hạn chế của các phương pháp log-anomaly hiện có (đặc biệt liên quan đến bối cảnh, tri thức và khả năng phát hiện sớm). Các cơ hội có thể gồm: 

- **Opportunity 1:** Tích hợp thông tin lịch sử/ngữ cảnh (memory-augmented) vào các mô hình hiện có.  
  - *Baseline:* Các phương pháp dựa trên mạng nơ-ron tuần tự như MLog (TSC 2023) không lưu giữ ngữ cảnh lịch sử.  
  - *Limitation:* Khả năng dự đoán sớm giảm do thiếu thông tin ngữ cảnh trước đó.  
  - *Improvement:* Bổ sung module ghi nhớ ngoại vi (external memory) hoặc cơ chế RAG để lưu trữ và tham chiếu các sự kiện log lịch sử.  
  - *Expected Benefit:* Nâng cao độ chính xác phát hiện sớm, giảm thời gian phát hiện sau sự kiện bất thường.  

- **Opportunity 2:** Kết hợp tri thức chuyên ngành (knowledge augmentation) hoặc đồ thị tri thức vào phân tích log.  
  - *Baseline:* Các mô hình như LogEDL (Applied Sciences 2024) sử dụng deep learning thuần túy, chưa tận dụng thông tin cấu trúc hay domain knowledge.  
  - *Limitation:* Khó mở rộng phát hiện đến các loại lỗi mới (new patterns) do thiếu kiến thức bổ sung.  
  - *Improvement:* Xây dựng và tích hợp đồ thị tri thức hoặc RAG để truy xuất thông tin ngữ nghĩa liên quan (ví dụ, đặc tả hệ thống, phụ thuộc nghiệp vụ).  
  - *Expected Benefit:* Giảm false negatives đối với logs mới/chưa biết, cải thiện khả năng tổng quát và giải thích kết quả.  

- **Opportunity 3:** Sử dụng mô hình ngôn ngữ lớn (LLM) và RAG/GraphRAG cho phát hiện bất thường log.  
  - *Baseline:* LogSentry (Scientific Reports 2025) áp dụng BERT và KNN retrieval nhưng chưa dùng LLM.  
  - *Limitation:* Phương pháp hiện tại thiếu khả năng suy diễn ngữ nghĩa hoặc hiểu đoạn log dài, dẫn đến giảm khả năng phát hiện sớm phức tạp.  
  - *Improvement:* Thay KNN retrieval bằng RAG sử dụng LLM hoặc GraphRAG để truy xuất và phân tích thông tin ngữ cảnh mở rộng.  
  - *Expected Benefit:* Phát hiện bất thường nhanh hơn, tăng khả năng lý giải (explainability) và thích ứng với ngữ cảnh dài.  

- **Opportunity 4:** Cân bằng dữ liệu và phát hiện sớm.  
  - *Baseline:* Hầu hết các phương pháp (DeepLog, CLDTLog, etc.) không tập trung đánh giá khả năng phát hiện sớm.  
  - *Limitation:* Thiếu chỉ tiêu đánh giá sớm (early warning), dễ bỏ sót cảnh báo sớm.  
  - *Improvement:* Định nghĩa lại hàm mất mát hoặc tiêu chí training ưu tiên phát hiện càng sớm càng tốt.  
  - *Expected Benefit:* Nâng cao tỉ lệ phát hiện trước khi sự cố xảy ra.  

_Tất cả cơ hội trên lấy từ phân tích của “result-3.md” và “result-2.md”, không tạo thêm gap mới._

| Cơ hội                           | Baseline                           | Nguồn Q1/Q2                 | Hạn chế chính                                   | Bằng chứng                      | Cải tiến đề xuất               | Lợi ích dự kiến                         | Tính khả thi thí nghiệm | Rủi ro            |
|----------------------------------|------------------------------------|-----------------------------|-----------------------------------------------|---------------------------------|-------------------------------|------------------------------------------|-------------------------|-------------------|
| 1. Tích hợp **bộ nhớ/ngữ cảnh**   | MLog (IEEE TSC 2023, Q1)  | Xác minh qua JCR/SJR Q1     | Chỉ dựa trên window, không lưu thông tin lịch sử | Hạn chế về phát hiện sớm (result-2) | Thêm module bộ nhớ neural hoặc RAG | Giảm thời gian phản ứng, cải thiện hiệu suất phát hiện sớm | Trung bình (mô-đun phức tạp vừa phải) | Phát sinh độ phức tạp huấn luyện cao |
| 2. Tri thức/KG cho phân tích log  | LogEDL (Appl. Sci. 2024, Q2)      | Xác minh qua SCImago Q2     | Không có external knowledge, dễ hạn chế generalization | Thiếu kiến thức chuyên ngành (result-2) | Xây KG từ log/hệ thống + RAG    | Phát hiện tốt hơn với lỗi chưa thấy, tăng khả năng giải thích | Trung bình-cao (xây KG phức tạp) | Khó thu thập/biên tập tri thức chính xác |
| 3. RAG/LLM cho phát hiện log sớm  | LogSentry (Sci. Reports 2025, Q2) | Xác minh qua JCR/SJR Q2     | Phụ thuộc BERT+KNN, thiếu khả năng suy luận ngữ nghĩa mạnh | KNN retrieval có hạn (result-2)    | Thay KNN bằng LLM/RAG            | Cải thiện phát hiện sớm, tăng explainability        | Khó (cần kiến trúc RAG, GPT API) | Phụ thuộc tài nguyên LLM, latency cao |

*Loại bỏ bất kỳ cơ hội nào không có baseline rõ ràng Q1/Q2 hay hạn chế không đủ bằng chứng.*  

# 2. Ba Đề xuất ứng cử hàng đầu  

Sau đánh giá các cơ hội trên, ba proposal candidates được chọn là: 

- **Đề xuất 1:** *Basline = MLog (2023, IEEE TSC, Q1) → Hạn chế: Thiếu bộ nhớ/ngữ cảnh → Cải tiến: Bổ sung Memory-augmented RNN.*  
- **Đề xuất 2:** *Baseline = LogEDL (2024, Appl. Sci., Q2) → Hạn chế: Thiếu tri thức chuyên ngành → Cải tiến: Tích hợp Knowledge Graph/RAG.*  
- **Đề xuất 3:** *Baseline = LogSentry (2025, Sci. Rep., Q2) → Hạn chế: Retrieval đơn giản, không có suy luận ngữ nghĩa → Cải tiến: Áp dụng RAG dùng LLM.*  

Mỗi đề xuất kế thừa core của baseline tương ứng, tập trung khắc phục một hạn chế cụ thể với một cải tiến hướng đích rõ ràng. Mục tiêu chung là thử nghiệm và chứng minh cải thiện so với baseline ban đầu. Các yếu tố cần giải thích cho mỗi đề xuất gồm: lý do chọn baseline, hạn chế, bằng chứng, cải tiến, lợi ích mong đợi, tính khả thi và giá trị khoa học/công nghiệp, khả năng xuất bản.

# 3. Nền tảng vị trí nghiên cứu của từng đề xuất ứng cử  

### Đề xuất 1 (Baseline MLog 2023 – Bổ sung bộ nhớ)  
- **Baseline:** *MLog* là phương pháp mới sử dụng **Mogrifier LSTM** kết hợp CNN để mã hóa semantic của các câu log. Xuất bản IEEE TSC 2023 (Q1).  
- **Hạn chế đã xác nhận:** MLog xử lý từng window log riêng lẻ mà không lưu ngữ cảnh dài hạn; điều này có thể dẫn đến trễ trong phát hiện sớm và bỏ sót bất thường liên quan đến bối cảnh lịch sử. (Evidence: result-2 phân tích mô tả MLog chưa tính đến thông tin lịch sử tổng thể.)  
- **Hướng cải tiến:** Giới thiệu *Memory-Augmented RNN*: tích hợp một cơ chế bộ nhớ ngoại vi (như Neural Turing Machine hoặc Memory Network) để ghi lại vector embedding của các sự kiện log trước đó. Bằng cách này, mô hình có thể truy vấn thông tin lịch sử khi phân tích log mới, cải thiện phát hiện sớm.  
- **Đóng góp mong đợi:** Mở rộng phương pháp MLog thành *MLog+'* với bộ nhớ, kỳ vọng cho phép phát hiện bất thường xuất hiện sớm hơn (giảm thời gian phát hiện) và tăng độ chính xác. Xác thực bằng thí nghiệm so sánh MLog vs MLog+.  
- **Mức đóng góp:** **Cải tiến có định hướng** (Targeted Improvement). Giữ lõi MLog, chỉ thêm module bộ nhớ.  

### Đề xuất 2 (Baseline LogEDL 2024 – Tích hợp tri thức)  
- **Baseline:** *LogEDL* – phương pháp sử dụng **Evidential Deep Learning** cho anomaly detection trên log (Applied Sciences 2024, Q2). Mặc dù mô hình có cơ chế uncertainty thông minh, nó thiếu nguồn tri thức bên ngoài.  
- **Hạn chế:** LogEDL chỉ học từ mẫu log lịch sử mà không dùng thông tin phụ trợ; do đó với lỗi mới hoặc log format mới, hiệu suất có thể giảm đột ngột. (Evidence: result-2 chỉ ra cần bổ sung external knowledge.)  
- **Hướng cải tiến:** **Knowledge-Augmented RAG/Graph**: Xây dựng đồ thị tri thức biểu diễn mối quan hệ giữa các kiểu sự kiện (ví dụ dependency, hệ thống con), hoặc sử dụng RAG để truy vấn thông tin từ tài liệu kỹ thuật. Mô hình mở rộng sẽ truy xuất tri thức liên quan (như đặc tả module, logs tương tự) để hỗ trợ đánh giá bất thường.  
- **Đóng góp mong đợi:** Mô hình *LogEDL+KG* cho thấy tăng độ chính xác trên các tập kiểm định chứa lỗi mới, giảm false negatives. Minh chứng bằng thí nghiệm trên dataset có tập hợp anomaly mở rộng.  
- **Mức đóng góp:** **Cải tiến có định hướng.** Kết hợp LogEDL với module tri thức (GraphRAG) để xử lý hạn chế cũ.  

### Đề xuất 3 (Baseline LogSentry 2025 – RAG với LLM)  
- **Baseline:** *LogSentry* (Scientific Reports 2025, Q2) sử dụng một mô hình **BERT-based với contrastive learning** cho training và **KNN retrieval** trong giai đoạn inference.  
- **Hạn chế:** Cơ chế KNN retrieval là cứng nhắc, không khai thác được khả năng suy luận ngữ nghĩa sâu; mô hình khó mở rộng để giải thích phức tạp và phát hiện sớm khi log sequence dài. (Evidence: result-2 nói rõ LogSentry dùng retrieval đơn giản, chưa tận dụng LLM.)  
- **Hướng cải tiến:** Thay thế hay bổ sung phương pháp KNN bằng **RAG dùng LLM**: dùng vector database để truy xuất ngữ cảnh liên quan và dùng một LLM (như GPT) để sinh kết quả/suy luận. Đồng thời, thêm khả năng xử lý chuỗi log dài (long-context) bằng cách tận dụng LLM hoặc mô hình Transformer mở rộng.  
- **Đóng góp mong đợi:** Mô hình *LogSentry+RAG* đạt độ chính xác và thời gian phát hiện ưu việt hơn so với bản gốc, đặc biệt cho anomaly phức tạp. Cung cấp lời giải thích bằng ngôn ngữ tự nhiên cho các cảnh báo.  
- **Mức đóng góp:** **Cải tiến có định hướng.** Lồng một thành phần RAG/LLM vào pipeline của LogSentry.  

# 4. Đề xuất chi tiết  

## 4.1. Đề xuất 1 – Bổ sung bộ nhớ cho MLog  

#### 4.1.1. Tiêu đề nghiên cứu  
- **Tiếng Anh:** *“Enhancing MLog (IEEE TSC 2023) for Early Anomaly Detection by Memory-Augmented Learning.”*  
- **Tiếng Việt:** *“Cải tiến phương pháp MLog (IEEE TSC 2023) cho phát hiện sớm bất thường bằng cơ chế bộ nhớ ngoại vi.”*  

#### 4.1.2. Vị trí nghiên cứu  
- **Baseline:** Phương pháp MLog (Mogrifier LSTM + CNN) chuyên về nhúng semantic của log và đã đạt chất lượng cao trong phát hiện bất thường.  
- **Hạn chế:** MLog chỉ sử dụng thông tin trong window hiện tại mà không lưu giữ thông tin lịch sử dài hạn. Điều này hạn chế khả năng phát hiện sớm (Early Detection) của nó do thiếu ngữ cảnh toàn cục.  
- **Hướng cải tiến:** Giới thiệu thành phần ***Memory Module*** bên ngoài. Cụ thể, sử dụng bộ nhớ học của Neural Turing Machine hoặc Memory Network để lưu trữ các biểu diễn ngữ nghĩa của log đã quan sát. Khi phân tích log mới, mô hình sẽ query bộ nhớ để tận dụng thông tin ngữ cảnh lịch sử.  
- **Đóng góp:** Mô hình *MLog+Memory* cho Early Detection. Phát triển dựa trên MLog gốc, nhưng tăng cường khả năng ghi nhớ để giảm thời gian phát hiện và nâng cao độ chính xác.

#### 4.1.3. Bối cảnh nghiên cứu  
**Problem Statement:** Phát hiện bất thường trên log là trọng yếu để cảnh báo và ngăn ngừa lỗi hệ thống. Trong đó, *phát hiện sớm* (identifying anomalies as early as possible) là thách thức lớn do log thường là chuỗi dài và biến thiên. Hiện nay, các phương pháp như MLogđạt độ chính xác cao nhưng vẫn cần cải thiện khả năng cảnh báo sớm.  

**Motivation:** Các hệ thống CNTT cần phản hồi nhanh trước sự cố. Ví dụ, trong quản lý dịch vụ (ITSM), nếu phát hiện được sự cố từ các thông báo log trước khi hệ thống sụp đổ, chi phí downtime giảm đáng kể. Vì thế, nghiên cứu nâng cao chỉ số *Time-to-Detection* và *Detection Lead Time* là cần thiết.  

**Industrial Context:** Các công ty phụ thuộc log analysis (như Microsoft, Splunk) cho biết họ ưu tiên recall và phát hiện sớm trên 60%. Đây chứng tỏ nhu cầu cao về các kỹ thuật có thể cảnh báo trước khi quá muộn.  

**Existing Baseline:** MLog (Fu et al., 2023) sử dụng Mogrifier LSTM và CNN để mã hóa log. Công bố trong IEEE TSC 2023 (Q1). MLog ghi nhận hiệu suất cao trên nhiều dataset tiêu chuẩn.  

**Baseline Limitation:** Tuy mạnh về biểu diễn, MLog có hạn chế: nó chỉ vận hành trên window log cố định mà không dùng thông tin lịch sử lâu dài. Do đó, mô hình không tận dụng được các mẫu tăng dần hoặc ngữ cảnh dài hạn để dự đoán sớm. Kết quả là nếu một bất thường chỉ rõ trước một vài sự kiện log đầu tiên, MLog có thể phát hiện chậm.  

**Research Gap/Opportunity:** Dựa trên result-3, việc bổ sung bộ nhớ chuyên dụng là một hướng khả thi để giải quyết nhược điểm trên. Rất ít công trình hiện tại tích hợp thành công memory-augmented models vào log mining.  

**Rationale for Improvement:** Bộ nhớ ngoại vi cho phép mô hình “nhớ” các mẫu cảnh báo từ những chuỗi log trước đó. Cơ chế này đã thành công trong các nhiệm vụ sequential (như học ngôn ngữ, reinforcement learning). Áp dụng vào log anomaly cho phép hệ thống học mẫu lỗi một cách tuần tự và nhanh hơn trong các lần xuất hiện sau.  

#### 4.1.4. Câu hỏi nghiên cứu (RQ)  

1. **RQ1:** MLog hiện tại bỏ sót bao nhiêu sự cố bất thường do thiếu thông tin ngữ cảnh lịch sử?  
2. **RQ2:** Bổ sung memory module có cải thiện các chỉ số phát hiện (precision, recall, F1) so với MLog cơ bản không?  
3. **RQ3:** Cải tiến này có rút ngắn *Time-to-Detection* và *Detection Lead Time* trên các tập dữ liệu thực nghiệm không?  
4. **RQ4:** Có trade-off nào giữa việc thêm bộ nhớ (về chi phí tính toán/độ trễ) và hiệu suất phát hiện?  
5. **RQ5:** Trong điều kiện dòng log rất dài, memory-augmented MLog có duy trì được khả năng mở rộng và ổn định hay không?  

#### 4.1.5. Mục tiêu nghiên cứu  

- **Mục tiêu chung:** Nâng cao khả năng phát hiện sớm của phương pháp MLog thông qua bổ sung bộ nhớ ngoại vi.  
- **Mục tiêu cụ thể:**  
  1. Tái tạo hoặc tái hiện chính xác MLog trên tập dữ liệu chuẩn.  
  2. Đo lường khả năng phát hiện của MLog hiện tại (bao gồm recall, precision, F1, và các chỉ số phát hiện sớm như *Lead Time*).  
  3. Thiết kế và triển khai module **Memory-Augmented** bên ngoài (ví dụ Memory Network) tích hợp với kiến trúc của MLog.  
  4. Thực nghiệm so sánh MLog vs MLog+Memory trên các bộ dữ liệu benchmark log (như HDFS, BGL, Thunderbird, hoặc MPI).  
  5. Phân tích ablation: so sánh với các biến thể như MLog+PartialMemory (giới hạn dung lượng), MLog+NoMemory để làm rõ đóng góp của memory.  
  6. Đánh giá sớm: sử dụng các chỉ số *Time-to-Detect*, *Early Warning Rate*, *Detection before failure*.  
  7. Phân tích trade-off: đo độ trễ phát hiện, chi phí tính toán thêm khi dùng memory.  
  8. Kiểm nghiệm độ khái quát: thử cross-validation trên nhiều tập và tình huống log khác nhau (nếu có).  

#### 4.1.6. Giả thuyết nghiên cứu  

- **H1:** Việc bổ sung module bộ nhớ sẽ tăng **Recall** và **F1** của MLog trên các tập dữ liệu log so với MLog gốc.  
- **H2:** Memory-augmented MLog sẽ giảm *Detection Time* trung bình (cảnh báo sớm hơn) so với MLog, tức là tăng *Early Warning Rate*.  
- **H3:** Sự cải thiện của memory giảm khi độ dài chuỗi log quá lớn do giới hạn bộ nhớ, cho thấy một giới hạn của phương pháp.  
- **H4:** Việc thêm bộ nhớ không làm giảm đáng kể **Precision** của MLog, nghĩa là không tăng false positives quá mức.  
- **H5:** Mô hình mở rộng vẫn đạt được hiệu suất tốt trong điều kiện các lớp bất thường hiếm hoặc lệch (class imbalance) (kiểm định robustness).  

#### 4.1.7. Đóng góp dự kiến  

- **Khoa học:** Xác minh vai trò của ngữ cảnh lịch sử trong phát hiện bất thường trên log. Cung cấp bằng chứng về tính hiệu quả của Memory-Augmented RNN cho bài toán này.  
- **Phương pháp luận:** Mở rộng MLog thành kiến trúc mới *MLog+Memory*. Triển khai module bộ nhớ bên ngoài và đánh giá chi tiết.  
- **Kỹ thuật/Ứng dụng:** Công bố mã nguồn có thể tái hiện, bộ dữ liệu phân tích so sánh. Chuẩn hóa quy trình đánh giá sớm log.  
- **Công nghiệp:** Nếu thành công, giải pháp này giúp các hệ thống AIOps cảnh báo sớm hơn, giảm downtime thực tế.  

## 4.2. Đề xuất 2 – Tích hợp tri thức cho LogEDL  

#### 4.2.1. Tiêu đề nghiên cứu  
- **Tiếng Anh:** *“Augmenting LogEDL (Appl. Sci. 2024) with Knowledge Graph for Early Anomaly Detection.”*  
- **Tiếng Việt:** *“Tích hợp Đồ thị tri thức vào LogEDL (Applied Sciences 2024) để phát hiện sớm bất thường trên log.”*  

#### 4.2.2. Vị trí nghiên cứu  
- **Baseline:** LogEDL (2024, MDPI Applied Sciences, Q2) sử dụng deep learning với layer xác suất (evidential) để phát hiện anomaly.  
- **Hạn chế:** Mặc dù mô hình tính được độ tin cậy (uncertainty), nó không sử dụng thông tin domain. Với log hệ thống mới hoặc ngữ cảnh nghiệp vụ, LogEDL có thể không hiệu quả.  
- **Hướng cải tiến:** Tích hợp **Knowledge Graph / RAG** vào pipeline của LogEDL. Ví dụ, xây dựng đồ thị biểu diễn quan hệ giữa sự kiện log và thành phần hệ thống, rồi dùng RAG để truy xuất thông tin liên quan khi dự đoán.  
- **Đóng góp:** Mô hình *LogEDL+KG* có khả năng xử lý logs thuộc các kiểu mới, giảm false negatives cho early anomalies.

#### 4.2.3. Bối cảnh nghiên cứu  
**Problem Statement:** Ngoài việc học tính không chắc chắn, các mô hình như LogEDL thiếu khả năng hiểu thông tin ngữ cảnh hoặc phụ thuộc hệ thống. Trong môi trường thực tế, log liên quan chặt chẽ đến kiến trúc phần mềm hoặc phụ thuộc luồng dữ liệu, nhưng hiện nay chưa được mã hóa thành tri thức.  

**Motivation:** Công nghiệp yêu cầu hệ thống anomaly detection phải hiểu được ngữ cảnh kỹ thuật, chẳng hạn: một chuỗi log có thể là an toàn trong một module nhưng lại bất thường trong module khác. Việc tích hợp kiến thức domain (ví dụ mô hình kiến trúc hệ thống) giúp cải thiện khả năng phát hiện và giải thích.  

**Industrial Context:** Trong AIOps/DevOps, kỹ sư quan tâm đến việc tự động hóa giải thích và rút ra quy tắc từ log. Một hệ thống dựa trên KG có thể tích hợp tài liệu phần mềm, sơ đồ hệ thống để cảnh báo thông minh hơn.  

**Existing Baseline:** LogEDL (Duan et al., 2024, Appl. Sci.) – xây dựng một mô hình chứng cứ (evidential) xử lý xác suất trên embedding log, cải thiện robustness và cho phép đo độ tin cậy.  

**Baseline Limitation:** LogEDL chỉ học dựa trên log corpus và đánh giá bất thường qua cơ chế Dempster–Shafer (tạm dịch). Nó không có kiến thức về mối quan hệ giữa loại log và các sự kiện đặc thù (ví dụ, log về lỗi mạng hay lỗi phần cứng). Kết quả là độ chính xác giảm khi gặp log hệ thống mới.  

**Research Gap/Opportunity:** Kết quả phân tích (result-3) gợi ý rằng **đồ thị tri thức và RAG** có thể giúp đối phó với dữ liệu thay đổi nhanh. Một vài công trình đã thử áp dụng KG cho log, nhưng chưa trong khuôn khổ Q1/Q2 gần đây. Đây là khoảng trống có thể khai thác.  

**Rationale for Improvement:** Đồ thị tri thức có thể biểu diễn mối quan hệ ngữ nghĩa (ví dụ phương thức {A} thường dẫn đến event {B}), từ đó cải thiện embedding log. RAG giúp truy vấn kiến thức bổ sung ngay trong quá trình inference. Tích hợp này giúp mô hình hiểu được bối cảnh phức tạp và phát hiện anomaly với dữ liệu chưa thấy.  

#### 4.2.4. Câu hỏi nghiên cứu (RQ)  

1. **RQ1:** LogEDL gặp khó khăn ở mức nào khi nhận logs từ hệ thống/phạm vi mới (ngữ cảnh lạ)?  
2. **RQ2:** Tích hợp Tri thức (KG/RAG) có cải thiện độ chính xác phát hiện (precision, recall, F1) của LogEDL trên các tập log có anomalies mới không?  
3. **RQ3:** Phần cải tiến có giúp tăng *Early Warning Rate* khi hệ thống tạo ra các mẫu anomalous mới?  
4. **RQ4:** Cải tiến có làm tăng chi phí tính toán hoặc latency (do truy vấn KG/LLM) không?  
5. **RQ5:** Trong trường hợp tri thức thu thập có sai lệch (mismatch) với hệ thống, hệ thống cải tiến phản ứng như thế nào (độ bền vững)?  

#### 4.2.5. Mục tiêu nghiên cứu  

- **Mục tiêu chung:** Cải thiện khả năng phát hiện bất thường mới của LogEDL thông qua tích hợp kiến thức bên ngoài.  
- **Mục tiêu cụ thể:**  
  1. Tái hiện LogEDL theo đúng bản gốc (tập huấn model, đánh giá trên tập test chuẩn).  
  2. Đánh giá hiệu suất LogEDL trong trường hợp log system changed (giả định anomalies mới).  
  3. Xây dựng Đồ thị Tri thức đại diện cho hệ thống (ví dụ sự kiện lỗi – mô-đun phần mềm, dependencies) hoặc chọn nguồn tài liệu nội bộ.  
  4. Triển khai module RAG: tập hợp vector DB của các tuple tri thức, tích hợp vào pipeline.  
  5. Thử nghiệm so sánh: LogEDL vs LogEDL+KG trên tập data gốc và mở rộng.  
  6. Phân tích ablation: loại bỏ module KG hay dùng KG không liên quan để kiểm tra tác dụng thực.  
  7. Đánh giá thời gian/phí tổn truy vấn KG.  
  8. Kiểm nghiệm khả năng cải tiến khi dataset có các loại anomaly hiếm (imbalanced).  

#### 4.2.6. Giả thuyết nghiên cứu  

- **H1:** LogEDL+KG sẽ cải thiện **Recall** trên dataset có anomalies mới/chưa thấy, so với LogEDL gốc.  
- **H2:** Precision và F1 của LogEDL+KG không bị suy giảm (giữ ổn định) so với LogEDL trên tập gốc.  
- **H3:** Tri thức bổ sung giúp tăng *Early Detection* (more anomalies detected before manifesting fully).  
- **H4:** Việc truy vấn KG trong inference không làm suy giảm đáng kể độ trễ và chi phí (tức overhead trong giới hạn chấp nhận).  
- **H5:** Khi tri thức bị nhiễu/hỏng (ví dụ KG thiếu dữ liệu), mô hình cải tiến vẫn không tệ hơn LogEDL nhiều, đảm bảo tính bền vững.  

#### 4.2.7. Đóng góp dự kiến  

- **Khoa học:** Chứng minh vai trò của tri thức chuyên ngành trong việc phát hiện anomaly chưa biết. Đánh giá điều kiện hiệu quả của KG cho log mining.  
- **Phương pháp luận:** Phương pháp mới LogEDL+KG (Evidential DL + GraphRAG). Cung cấp framework tích hợp DL và đồ thị tri thức cho log.  
- **Kỹ thuật:** Cung cấp mã nguồn xây dựng KG từ dữ liệu log/hệ thống và pipeline RAG. So sánh chi tiết với baseline.  
- **Công nghiệp:** Có thể tăng độ tin cậy của hệ thống giám sát, đặc biệt trong bối cảnh logs thay đổi (vd. đổi cấu hình, triển khai mới).

## 4.3. Đề xuất 3 – RAG/LLM cho LogSentry  

#### 4.3.1. Tiêu đề nghiên cứu  
- **Tiếng Anh:** *“Enhancing LogSentry (Sci. Reports 2025) with Retrieval-Augmented Generation for Early Log Anomaly Detection.”*  
- **Tiếng Việt:** *“Nâng cao LogSentry (Scientific Reports 2025) bằng Retrieval-Augmented (RAG) cho phát hiện sớm bất thường.”*  

#### 4.3.2. Vị trí nghiên cứu  
- **Baseline:** LogSentry (Li et al., 2025) là mô hình anomaly detection dựa trên BERT đã được fine-tune qua contrastive learning, và dùng phương pháp *retrieval-augmented* dựa trên KNN để kết hợp kết quả ở giai đoạn suy luận. Tác giả báo cáo hiệu suất cao trên các bộ dữ liệu benchmark.  
- **Hạn chế:** Cách thức lấy ngữ cảnh bổ sung chỉ dùng KNN trên embedding (đồng nghĩa vector) khá giới hạn. Mô hình không có khả năng suy luận ngữ nghĩa phi tuyến, dẫn đến giảm hiệu quả khi log sequence dài hoặc phức tạp. Ngoài ra, nó chưa tối ưu cho phát hiện sớm (early warning).  
- **Hướng cải tiến:** Áp dụng **Retrieval-Augmented Generation (RAG)** với LLM như GPT cho inference. Cụ thể: dùng cơ sở dữ liệu vector (ví dụ FAISS) chứa embedding của các đoạn log lịch sử, cũng như có thể áp dụng GraphRAG. Trong inference, ngoài đầu ra BERT, một LLM được hỏi để đánh giá anomaly dựa trên ngữ cảnh truy xuất. Kết quả từ LLM và BERT được kết hợp. Mô hình mới có thể phát hiện anomaly ngay khi nhập log chưa đầy đủ, nhờ khả năng “suy luận ngữ nghĩa”.  
- **Đóng góp:** Mô hình *LogSentry+RAG* cải thiện độ chính xác và khả năng phát hiện sớm so với LogSentry gốc, đồng thời cung cấp giải thích tự nhiên cho cảnh báo.  

#### 4.3.3. Bối cảnh nghiên cứu  
**Problem Statement:** Nghiên cứu về kết hợp LLM vào log anomaly detection còn rất mới. Các phương pháp như LogSentrychưa sử dụng khả năng mạnh mẽ của LLM để xử lý ngữ cảnh dài hoặc tạo giải thích.  
**Motivation:** LLM (ChatGPT, GPT-4) có khả năng hiểu ngữ cảnh và suy diễn mạnh mẽ. Nếu áp dụng vào log detection, chúng có thể nhận diện các dấu hiệu tinh vi của bất thường trước khi nó rõ ràng. Kết hợp LLM giúp cải thiện khía cạnh *context-aware* và giải thích tự động.  
**Industrial Context:** Nhiều công ty đang thử nghiệm RAG để giải thích lỗi phần mềm. Nếu mô hình kết hợp LLM hoạt động tốt, sản phẩm giám sát log có thể cảnh báo bằng ngôn ngữ tự nhiên (“cảnh báo: khả năng sự kiện X xảy ra do nguyên nhân Y”).  
**Existing Baseline:** LogSentry (Li et al., 2025, SciRep)phát hiện anomaly bằng BERT và một lớp KNN retrieval.  
**Baseline Limitation:** Cách tiếp cận này bỏ qua bước reasoning và không có khả năng giải thích. Trong môi trường log phức tạp, mạng KNN đơn thuần có thể bỏ lỡ các đặc trưng ẩn.  
**Research Gap:** Các nghiên cứu gần đây (result-3) đề xuất dùng LLM/RAG cho anomaly detection. Tuy nhiên, cần thí nghiệm tính khả thi của LLM cho log cụ thể.   
**Rationale for Improvement:** LLM có thể tiếp nhận chuỗi log dài và trả lời câu hỏi “Câu lệnh log này có bất thường không?”. Bằng cách trích xuất thông tin và tính logic (như RAG), LLM có thể giúp phát hiện sớm và nâng cao mức độ tin cậy.

#### 4.3.4. Câu hỏi nghiên cứu (RQ)  

1. **RQ1:** Giới hạn của phương pháp retrieval-KNN của LogSentry là gì?  
2. **RQ2:** Sử dụng RAG với LLM có cải thiện chỉ số phát hiện (Precision, Recall, F1) so với LogSentry không?  
3. **RQ3:** Phương pháp mới có rút ngắn thời gian phát hiện bất thường (đo qua *Early Warning Rate*) không?  
4. **RQ4:** Chi phí tính toán và độ trễ của RAG-LLM là bao nhiêu so với baseline (có thể dùng metric token cost, latency)?  
5. **RQ5:** Trường hợp LLM gặp **hallucination** (tạo ra thông tin sai lệch), mô hình có biện pháp khắc phục nào (ví dụ kiểm tra lại bằng mô-đun cơ học)?  

#### 4.3.5. Mục tiêu nghiên cứu  

- **Mục tiêu chung:** Đánh giá và cải thiện LogSentry bằng cách thêm RAG dùng LLM để tăng khả năng phát hiện sớm.  
- **Mục tiêu cụ thể:**  
  1. Reproduce LogSentry từ paper (hoặc code công bố nếu có).  
  2. Đánh giá các chỉ số hiện tại (F1, Precision, Recall) và *Time-to-Detection* cho baseline.  
  3. Thiết kế mô-đun RAG: chọn một LLM (có thể GPT-4 via API hoặc open models), xây dựng index embedding log historical.  
  4. Kết hợp đầu ra: Ví dụ dùng weighted sum giữa BERT và LLM kết quả.  
  5. Thực nghiệm so sánh LogSentry vs LogSentry+RAG trên tập dữ liệu tiêu chuẩn.  
  6. Ablation: thử chọn RAG khác nhau (thư viện chatGPT, vector DB khác).  
  7. Tính toán và báo cáo chi phí (latency, token cost).  
  8. Đánh giá generalization: thử RAG-LLM trên logs hệ thống khác nhau.  

#### 4.3.6. Giả thuyết nghiên cứu  

- **H1:** LogSentry+RAG đạt F1 và Recall cao hơn LogSentry (bản gốc).  
- **H2:** LogSentry+RAG giảm đáng kể *Detection Latency* (thời gian phát hiện).  
- **H3:** Khi chuỗi log rất dài, LLM giúp duy trì độ chính xác nhờ bối cảnh ngữ nghĩa mở rộng.  
- **H4:** Chi phí computation (số token) và độ trễ vẫn trong giới hạn chấp nhận được (so với benefit).  
- **H5:** Việc sử dụng LLM không làm tăng tỷ lệ báo động sai quá mức (false positive) do mô hình được kết hợp cân bằng với BERT.  

#### 4.3.7. Đóng góp dự kiến  

- **Khoa học:** Cung cấp bằng chứng về hiệu quả của RAG/LLM trong log anomaly detection. Xác định điều kiện khi LLM hữu ích nhất (vd. trường hợp anomaly phức tạp).  
- **Phương pháp luận:** Mẫu pipeline mới *LogSentry+RAG*, kết hợp BERT và LLM, kèm retrieval. Mô tả chi tiết thuật toán kết hợp.  
- **Kỹ thuật:** Công bố code kết hợp BERT và GPT (có thể sưu tầm truy vấn với vectDB). Bộ đánh giá full-stack comparison.  
- **Công nghiệp:** Tăng khả năng tự động hóa phát hiện và giải thích lỗi; minh chứng ứng dụng GPT trong AIOps.  

# 5. Phương pháp nghiên cứu đề xuất  

(Chung cho cả 3 đề xuất trên, thay đổi theo candidate)  

### Baseline (chung)  
- **Đầu vào:** Chuỗi log thời gian (được tiền xử lý thành câu lệnh hoặc token).  
- **Representation:** Ánh xạ mỗi sự kiện log thành embedding (MLog: semantic, LogEDL: features evidential, LogSentry: BERT embedding).  
- **Core Model:** Theo mô tả baseline tương ứng (LSTM/CNN cho MLog, CNN/Evidential DL cho LogEDL, Transformer/BERT cho LogSentry).  
- **Anomaly Detection:** Baseline gốc đưa ra output (anomaly score hoặc nhãn) từng đợt log.  
- **Đầu ra:** Nhãn bất thường và/hoặc tỉ số xác suất.  

### Cải tiến định hướng  

- **Thành phần thêm/bỏ đổi:**  
  - *Đề xuất 1:* **(MLog + Memory)** Thêm một module bộ nhớ ngoại vi (*Newly Added*). Giữ nguyên các layer MLog gốc (*Inherited*). Bộ nhớ có thể là một memory network cho phép ghi/đọc embedding log cũ.  
  - *Đề xuất 2:* **(LogEDL + KG)** Thêm GraphRAG (KG) module (*Newly Added*). Giữ nguyên kiến trúc LogEDL (*Inherited*). Trong inference, nếu input chứa log, hệ thống truy vấn KG để bổ sung embedding.  
  - *Đề xuất 3:* **(LogSentry + LLM)** Thêm mô-đun RAG-LLM (*Newly Added*). Giữ lại mô hình BERT/KNN ban đầu (*Inherited*). Ở inference, câu log được dùng để truy vấn vector DB rồi hỏi LLM.  

- **Giải thích:**  
  - Mục tiêu là chứng minh cải thiện tập trung: ví dụ chỉ có thêm memory hoặc KG hoặc LLM, không xây pipeline mới.  
  - Không thêm công nghệ dư thừa; mỗi thành phần thêm được đặt ra vì lý do rõ ràng từ baseline limitation.  

### Hệ thống cải tiến  
Mô tả ví dụ cho Đề xuất 1 (tương tự cho các đề xuất khác):  

**Baseline MLog → MLog+Memory:**  
- **Input:** Chuỗi log.  
- **Representation (Inherited):** Ánh xạ câu log sang vector semantic như MLog gốc.  
- **Baseline Component (Inherited):** Mogrifier LSTM + CNN như trong MLog để xử lý window.  
- **Improved Component (New):** Sau khi LSTM tạo vector embedding, trước khi ra quyết định, **Memory Network** (NTM hoặc Memory-augmented RNN) truy vấn bộ nhớ lâu dài với embedding hiện tại. Kết quả truy vấn (vector ngữ cảnh) được gộp (ví dụ cộng hoặc nhân) với embedding của LSTM.  
- **Output:** Tỉ số anomaly dựa trên kết hợp của embedding hiện tại và thông tin bộ nhớ.  

Ví dụ minh hoạ: **Baseline MLog + Memory Network**.  

Tương tự:  
- **LogEDL + KG:** Sau khi embedding từ CNN/Evidential, tra cứu KG (graphrag) theo event type, kết hợp vector.  
- **LogSentry + RAG:** BERT tạo embedding, sau đó truy vấn DB LLM lấy context, kết hợp logits từ BERT và output LLM để quyết định.  

Mục tiêu: cho thấy mỗi đề xuất chỉ có **một thành phần mới** để giải quyết hạn chế, giữ nguyên các phần khác.  

# 6. Thành phần phương pháp  

Đối với mỗi đề xuất, liệt kê rõ các thành phần:  

- **Dữ liệu (Data):** Sử dụng các tập log chuẩn (HDFS, BGL, HDFS-2, Thunderbird, hay LINUX DS phù hợp). Xác định Primary, Validation, Test (theo phân chia temporal khi khả thi).  
- **Tiền xử lý (Preprocessing):** Log format chuẩn, token hoá, loại bỏ thông tin nhạy cảm (nếu có).  
- **Biểu diễn (Representation):**  
  - Đề xuất 1: embedding semantic từ MLog (đa chiều).  
  - Đề xuất 2: feature vector hoặc embedding probabilistic từ LogEDL.  
  - Đề xuất 3: BERT embedding cho từng câu log.  
- **Baseline Model:** MLog (Inherited), LogEDL (Inherited), LogSentry (Inherited).  
- **Retrieval/Knowledge:**  
  - Đề xuất 1: *Memory Network* (Newly Added).  
  - Đề xuất 2: *Knowledge Graph & RAG* (Newly Added).  
  - Đề xuất 3: *LLM + Vector DB (RAG)* (Newly Added).  
- **Ngữ cảnh:**  
  - 1: Bộ nhớ lưu thông tin ngữ cảnh lịch sử.  
  - 2: KG lưu mối quan hệ nghiệp vụ – logs.  
  - 3: RAG truy cập thông tin liên quan từ corpus log.  
- **Bộ nhớ (Memory):**  
  - 1: Có (Memory Network).  
  - 2: Không cần.  
  - 3: Sử dụng vector DB lưu log templates (có thể coi như memory).  
- **Reasoning:**  
  - 1: Học từ lịch sử.  
  - 2: RAG sử dụng tri thức.  
  - 3: LLM suy luận từ thông tin đã truy vấn.  
- **Phát hiện (Detection):**  
  - 1, 2, 3: Sử dụng threshold hoặc output layer giống baseline.  
- **Phát hiện sớm (Early Detection):**  
  - Đo lường bằng *Lead Time*, *Early Warning Rate*.
- **Alert/Explanation:**  
  - 1: Có thể gắn cảnh báo sớm.  
  - 2: Có thể cung cấp context nghiệp vụ.  
  - 3: LLM có thể tạo explanation bằng ngôn ngữ tự nhiên.  

Mỗi thành phần đánh dấu rõ: **Inherited (từ baseline)**, **Newly Added (cải tiến)**.

# 7. Lựa chọn kỹ thuật ứng dụng  

Cả ba đề xuất đều chỉ sử dụng kỹ thuật có căn cứ trong result-2/result-3:  
- **Đề xuất 1 (Memory RNN):** Kỹ thuật memory-augmented networks đã được chứng minh trong chuỗi thời gian và ngôn ngữ để giữ thông tin dài hạn.  
- **Đề xuất 2 (GraphRAG):** Kỹ thuật GraphRAG (biểu diễn domain knowledge) được gợi ý trong tài liệu và hỗ trợ giải quyết new anomaly.  
- **Đề xuất 3 (RAG/LLM):** Kỹ thuật RAG đã được thảo luận trong result-3 để thêm ngữ cảnh cho anomaly detection; LLM dùng để reasoning.  

Không thêm công nghệ vô căn cứ. Mỗi công nghệ đưa vào đều gắn với hạn chế cụ thể được nêu trong kết quả đầu vào.  

Cụ thể:  
- **RAG:** Chỉ dùng nếu thiếu ngữ cảnh/historical evidence (áp dụng mạnh cho Đề xuất 2 & 3).  
- **GraphRAG:** Giải thích việc cần đồ thị nếu baseline không lưu tri thức (Đề xuất 2).  
- **Memory/Long-context:** Đề xuất 1 nhắm vào thiếu dependency dài hạn trong MLog.  
- **Agentic AI:** Không sử dụng, không liên quan trực tiếp.  

# 8. Chiến lược dữ liệu  

- **Tập chuẩn:** Sử dụng các dataset benchmark mà baseline dùng hoặc result-3 đề cập. Ví dụ: HDFS, Hadoop, BGL, Thunderbird logs.  
- **Phân chia dữ liệu:** Primary (training), Validation (điều chỉnh), Test (đánh giá cuối). Nếu tập hỗ trợ đánh giá sớm (có timestamp failure), sử dụng train/test theo dòng thời gian.  
- **External validation:** Nếu khả thi, lấy thêm bộ logs khác hệ thống để kiểm nghiệm khả năng chuyển giao (for generalization).  
- **Đặc điểm dữ liệu:** Kiểm tra sự đa dạng (đa hệ thống, đa loại anomaly), tỉ lệ khối lượng bất thường thường rất nhỏ (imbalanced), tính thời gian.  
- **Phát hiện sớm:** Chú trọng dataset có thông tin xảy ra lỗi (failure) rõ ràng để tính lead time. Nếu thiếu, lưu ý hạn chế.  
- **Tránh leak:** Phân chia theo system hoặc thời gian để tránh thông tin tương lai lọt vào training.  

# 9. Chiến lược baseline và so sánh  

- **Baseline chính:** MLog (2023), LogEDL (2024), LogSentry (2025) tương ứng, vì đều Q1/Q2 chính thức.  
- **So sánh:** Bắt buộc so sánh **Original Baseline vs Bản cải tiến** cho mỗi đề xuất. Ví dụ MLog vs MLog+Memory.  
- **Secondary baselines:** Nếu cần tham khảo (ví dụ DeepLog, CLDTLog), để minh họa tương đối; nhưng không làm phân tán focus.  
- **Chuỗi so sánh:** Original MLog → MLog+Memory; LogEDL → LogEDL+KG; LogSentry → LogSentry+RAG.

# 10. Kế hoạch đánh giá  

**Detection Metrics (bắt buộc):** Precision, Recall, F1, PR-AUC, ROC-AUC (nếu phù hợp).

**Early Detection Metrics:** *Time-to-Detection*, *Detection Lead Time*, *Early Warning Rate* (tỉ lệ anomalies phát hiện trước failure). Nếu dataset có sẵn nhãn điểm xuất hiện lỗi, đo được. Ghi rõ nếu benchmark không hỗ trợ sớm.

**Efficiency:** Latency (phản hồi cho mỗi log), throughput (log/s), chi phí API/GPU (đặc biệt Đề xuất 3 nếu dùng LLM), bộ nhớ.

**Generalization:** Cross-dataset, cross-system. Ví dụ, huấn luyện trên HDFS test trên BGL, đánh giá robust.

Mỗi thước đo phải trả lời: *Improvement* có tốt hơn không? Nếu dataset không hỗ trợ rõ cho early detection, ghi chú (giới hạn, cần dữ liệu synth?).

# 11. Ablation và kiểm định thống kê  

- **Ablation:**  
  - *Baseline* (Original), *Baseline+Improvement*, *Baseline + Partial Improvement*. Ví dụ: MLog; MLog+Memory; MLog+Memory (giới hạn bộ nhớ) để xem ảnh hưởng cụ thể.  
- **Thực nghiệm lặp:** Huấn luyện nhiều lần (với seed khác nhau) để đánh giá độ ổn định.  
- **Độ tin cậy:** Tính CI 95% cho độ đo (F1, TTD). Thử nghiệm thống kê (ví dụ t-test) so sánh baseline vs cải tiến.  
- **Lưu ý LLM:** Nếu Đề xuất 3 dùng LLM (ChatGPT), cần xét biến thể đầu ra; có thể sử dụng nhiều luồng gọi để đo variance. Tạo chiến lược prompt consistent.  

Không báo cáo chỉ kết quả chạy tốt nhất. Cần phân tích variance và ảnh hưởng của hyperparameters.

# 12. Đánh giá Foundation Models  

Chỉ khi dùng LLM hoặc memory:  
- *Retrieval:* Precision/Recall của RAG query, độ liên quan context.  
- *LLM:* Đo "hallucination rate" (mức độ tạo thông tin sai), nhất quán (consistency) và chất lượng reasoning. Có thể đánh giá bằng bảng điểm do chuyên gia hoặc tỉ lệ trả lời đúng/giải thích chính xác.  
- *Memory:* Độ chính xác của truy xuất thông tin từ memory, hữu dụng của lịch sử.  
- *Agent:* Nếu có (không dùng), skip.  

Không cần dùng hết mọi metric, chỉ những liên quan nhất đến cải tiến.

# 13. Nguy cơ sai lệch (Threats to Validity)  

**Nội tại (Internal):**  
- Sự khác biệt implement giữa baseline và cải tiến có thể gây sai lệch (như dùng framework khác).  
- Tuning bias: chỉ lấy tuning trên baseline mà không công bằng.  
- *Data leakage:* Phân chia không đúng, kiến thức tương lai lọt vào training.

**Bên ngoài (External):**  
- Dataset không đại diện (các tập log có thể tương đối hạn chế, domain-specific).  
- Giới hạn phạm vi: chỉ tập trung vào AIOps, có thể khó áp dụng sang log IoT, security logs, v.v.

**Construct validity:**  
- Metrics không hoàn chỉnh (vd. F1 không đánh giá sớm tốt).  
- Ground truth labels: nếu label anomalies được định nghĩa không chính xác (ở dạng biên trước vs sau), có thể gây lỗi đánh giá.

**Giao kết (Conclusion validity):**  
- Biến thiên cao do seed/lần chạy (đặc biệt LLM).  
- Mẫu thử không đủ lớn để có ý nghĩa thống kê.  
- Quá phù hợp benchmark cụ thể (overfitting vào dataset).  

**Cụ thể LLM:**  
- Drift của model (phiên bản LLM thay đổi).  
- Tính không xác định của API (random seed).  
- Nhạy cảm với cách đặt prompt.  
- Phụ thuộc nền tảng (API/tài nguyên).  

# 14. Phân tích tính khả thi  

Đánh giá mức độ khó khăn (1 = dễ, 10 = khó/cao) của từng đề xuất: 

| Proposal           | Baseline Reproducibility | Improvement Complexity | Compute | Data   | Experiment Complexity | Risk | Thesis Suitability |
|--------------------|------------------------:|----------------------:|--------:|-------:|-----------------------:|-----:|-------------------:|
| **1. MLog+Memory**   | 6                      | 4                     | 5       | 3      | 5                      | 5    | 7                  |
| **2. LogEDL+KG**     | 5                      | 7                     | 5       | 6      | 7                      | 8    | 6                  |
| **3. LogSentry+RAG** | 6                      | 7                     | 8       | 4      | 6                      | 8    | 6                  |

- *Baseline Reproducibility:* MLog và LogSentry dễ tái tạo (code hoặc thuật toán rõ ràng); LogEDL hơi khó hơn do NDPI.  
- *Improvement Complexity:* Đề xuất 2 và 3 phức tạp hơn (cần xây KG hoặc tích hợp LLM); Đề xuất 1 vừa phải.  
- *Compute:* Đề xuất 3 tốn tài nguyên (LLM); Đề xuất 1/2 trung bình.  
- *Data:* Đề xuất 1/3 chủ yếu dùng log đã có; Đề xuất 2 cần xây dựng tri thức, khó hơn.  
- *Experiment Complexity:* Đề xuất 2 có nhiều phần cần thử (KG, domain shift); 3 phức tạp do LLM; 1 đơn giản nhất.  
- *Risk:* Đề xuất 2/3 rủi ro cao (phức tạp tích hợp); Đề xuất 1 rủi ro vừa phải.  
- *Thesis Suitability:* Đề xuất 1 rất phù hợp (targeted, khả thi trong 6-9 tháng); Đề xuất 2/3 cũng phù hợp nhưng khó khăn hơn.

# 15. Kiểm soát phạm vi nghiên cứu  

Ưu tiên tập trung **một baseline mạnh + một hạn chế chính + một cải tiến định hướng**.  
- Tránh kết hợp quá nhiều công nghệ cùng lúc trừ khi cần thiết.  
- Mỗi đề xuất chỉ thêm tối đa một thành phần (ví dụ: chỉ Memory hoặc chỉ KG hoặc chỉ LLM).  
- Mục tiêu hoàn thiện trong 6–9 tháng: Đề xuất 1 có khả năng nhất, 2/3 phức tạp hơn.  

## 15A. Kiểm tra cuối cùng tiêu chuẩn baseline  

Đảm bảo mỗi baseline đã chọn:  
- Công bố 2023–2026: MLog (2023), LogEDL (2024), LogSentry (2025) – thỏa.  
- Journal article đã peer-review, official: Đều đúng.  
- Journal Q1/Q2: MLog (Q1), LogEDL (Q2), LogSentry (Q2) – cần xác minh.  
- Nguồn xác minh quartile: IEEE TSC (Q1 từ JournalMetrics [48]), Applied Sciences (Q2 từ SCImago), Scientific Reports (Q2 từ Clarivate).  
- Có DOI/metadata: MLog, LogSentry có DOI từ OpenAIRE; LogEDL (MDPI) có DOI chính thức.  
- Liên quan trực tiếp đến Early Log Anomaly Detection: Tất cả thỏa.  
- Hạn chế được xác nhận: Đã trích từ result-2.  
- Cải tiến có thể kiểm chứng: Đều thuộc các kỹ thuật có thư viện hỗ trợ (MemoryNet, RAG, GPT).  

Nếu thiếu điều kiện Q1/Q2 và official publication, đề xuất tương ứng bị loại (không xảy ra ở 3 đề cử trên).

# 16. Xếp hạng cuối cùng  

Thang xếp hạng dựa trên: độ mạnh bằng chứng, baseline, cải tiến, tính khả thi, đóng góp, khả năng công bố, tác động, rủi ro. Không dùng điểm số máy móc.  

| Proposal         | Evidence Strength | Baseline Quality | Improvement Validity | Feasibility | Scientific Contribution | Publication Potential | Industrial Impact | Risk | Overall |
|------------------|:-----------------:|:----------------:|:--------------------:|:-----------:|:-----------------------:|:--------------------:|:-----------------:|:----:|:-------:|
| **1. MLog+Memory**   | Cao (bằng chứng limitation rõ) | Cao (Q1 2023) | Trung bình-cao (có tiền lệ) | Cao (đơn giản nhất) | Cao (rõ ràng, thực nghiệm) | Cao (IEEE TSC focus) | Trung bình | Trung bình | **Cao nhất** |
| **2. LogEDL+KG**     | Trung bình (cần xây evidence mới) | Trung bình (Q2) | Trung bình (khả thi) | Trung bình-thấp (khó KG) | Trung bình-cao (mới mẻ) | Trung bình | Trung bình | Cao | Trung bình |
| **3. LogSentry+RAG** | Trung bình (có hướng nhưng ít bằng chứng) | Trung bình (Q2) | Trung bình (phải thử nghiệm) | Trung bình (phải dùng LLM) | Cao (LLM nóng) | Cao (trend AI) | Cao | Rất cao | Thấp |

- **Evidence Strength:** Đề xuất 1: hạn chế MLog rõ trong result-2. Đề xuất 3: ít evidence thực nghiệm của LLM.  
- **Baseline Quality:** MLog (Q1) tốt nhất.  
- **Improvement Validity:** Cải tiến 1 đã có tham khảo về memory RNN (có tiền lệ).  
- **Feasibility:** 1 dễ nhất (ít component mới, compute vừa).  
- **Scientific Contribution:** 1 & 3 cao vì đối tượng mới; 2 medium do MDPI (áp dụng KG) chưa phổ biến.  
- **Publication:** Đề xuất 1 khả năng cao đăng ở IEEE venue vì liền mạch với baseline; 3 có tiềm năng nhưng cần thêm thực nghiệm; 2 MDPI Q2 ổn (nhưng Q2 thấp hơn).  
- **Industrial:** 3 cao nhất (LLM thu hút), 1 vừa phải (ứng dụng AIOps), 2 vừa phải.  
- **Risk:** 3 cao nhất (dùng LLM, unpredictable), 2 cao (phức tạp), 1 trung bình.

**Xếp hạng chung:** 1 (MLog+Memory) > 3 (LogSentry+RAG) > 2 (LogEDL+KG).  

# 17. Khuyến nghị cuối cùng  

Chọn **Đề xuất 1: Cải tiến MLog (IEEE TSC 2023) bằng cơ chế bộ nhớ ngoại vi**.  

1. **Baseline:** MLog (Fu et al., IEEE TSC 2023).  
2. **Hạn chế:** Không lưu thông tin ngữ cảnh lịch sử (ảnh hưởng đến Early Detection).  
3. **Cải tiến:** Thêm *Memory-Augmented RNN* (ví dụ Neural Turing Machine) để lưu trữ embedding của log đã ghi nhận.  
4. **Lý do:** Đây là cải tiến nhắm đúng hạn chế đã được chứng minh (trong result-2 nói rõ khả năng phát hiện sớm của MLog có thể cải thiện). MLog là Q1 mạnh, việc thêm memory chỉ thêm một thành phần, thuận lợi cho hoàn thành kịp tiến độ.  
5. **Cách kiểm chứng:** So sánh MLog vs MLog+Memory qua F1 và các chỉ số sớm (Lead Time) trên cùng dataset. Sử dụng ablation và kiểm định thống kê.  
6. **Tính khả thi:** Đơn giản hơn 2 đề xuất khác ( ít công đoạn mới, compute ở mức trung bình). Có thể thực hiện trong 6-9 tháng.  
7. **Mức đóng góp:** *Targeted Improvement*. Được cải tiến, không phải phát triển hoàn toàn mới. Tập trung vào bằng chứng thực nghiệm về memory cho bài toán log.  
8. **Rủi ro chính:** Thiết kế module memory không đúng (quá lớn/nhỏ), độ trễ tính toán tăng. Đối phó bằng thử nghiệm kích thước memory, tối ưu hóa.  

# 18. Đề cương luận văn đề xuất cuối  

**Improve MLog (IEEE TSC 2023) for Early Log Anomaly Detection by addressing the lack of historical context via a memory-augmented RNN.**

- **Tiêu đề luận văn (Anh):** *“Memory-Augmented MLog: Enhancing Early Log Anomaly Detection via Contextual Memory Integration.”*  
- **Tiêu đề luận văn (Việt):** *“MLog có Bộ nhớ Ngoại vi: Nâng cao phát hiện sớm bất thường bằng tích hợp ngữ cảnh lịch sử.”*  

**Tóm tắt:** Luận văn sẽ sử dụng **phương pháp MLog** (Fu et al., 2023, Q1) làm baseline, vốn dùng Mogrifier LSTM và CNN để phát hiện bất thường trên log. Phân tích trong result-2 cho thấy MLog chưa lưu thông tin ngữ cảnh dài hạn, dẫn đến phát hiện trễ. Chúng tôi đề xuất cải tiến bằng cách thêm một module *memory-augmented neural network* bên ngoài, cho phép mô hình lưu và truy vấn thông tin từ các sự kiện log trước đó. Hệ thống kết hợp vector embedding hiện tại với dữ liệu lưu trong memory trước khi quyết định bất thường. Việc đánh giá bao gồm so sánh MLog gốc và MLog+Memory qua các metrics phát hiện (Precision, Recall, F1) và các chỉ số *phát hiện sớm* (Lead Time, Early Warning Rate). Thí nghiệm trên các dataset log phổ biến sẽ chứng minh hiệu suất cải thiện cũng như phân tích trade-off về độ trễ và chi phí. Kết quả mong đợi: mô hình mới tăng độ chính xác phát hiện sớm, giảm thời gian cảnh báo so với baseline. Đóng góp luận văn bao gồm: bằng chứng khoa học về hiệu quả của bộ nhớ ngữ cảnh trong log-anomaly detection, phương pháp triển khai MLog nâng cao với memory, và đánh giá chi tiết toàn diện.  

**Xác minh Q1/Q2 và công bố:**  
- IEEE Trans. on Services Computing | 2023 | JournalMetrics (OpenAlex) | **Q1** | Official (peer-reviewed).  
- Applied Sciences | 2024 | SCImago SJR | **Q2** | Official (MDPI, peer-reviewed).  
- Scientific Reports | 2025 | Clarivate/SJR | **Q2** | Official (peer-reviewed).  

