# 1. Mục tiêu thí nghiệm và khả năng truy vết

| Nghiên cứu phần tử | Thí nghiệm       | Đơn vị đo chính      | Bằng chứng kỳ vọng                                |
| -------------------| ---------------- | -------------------- | ------------------------------------------------ |
| **RQ1**            | E2 (So sánh)     | F1, Precision, Recall | Cải thiện đáng kể các chỉ số phát hiện (đặc biệt F1) so với baseline. |
| **RQ2**            | E3 (Phát hiện sớm) | Thời gian phát hiện, Lead Time (LT) | Phát hiện lỗi/sự cố sớm hơn baseline theo thống kê, tỉ lệ cảnh báo trước (early warning rate) cao hơn. |
| **RQ3**            | E7 (Tổng quát hóa) | F1, Recall          | Hiệu năng ổn định hoặc cải thiện trên hệ thống/dữ liệu khác so với baseline. |

| Phỏng đoán (Hypothesis) | Thí nghiệm   | Đơn vị đo chính      | Bằng chứng kỳ vọng                                      |
| ----------------------- | ------------ | -------------------- | ------------------------------------------------------ |
| **H1** (Accuracy)        | E2          | F1, Precision, Recall | Baseline + cải tiến có F1/Recall cao hơn baseline (p<0.05). |
| **H2** (Early Detection) | E3          | Lead Time, Early Warning Rate | Baseline + cải tiến phát hiện sớm hơn (lead time tăng) và tăng tỉ lệ cảnh báo trước. |
| **H3** (Robustness)      | E5          | F1, False Alarm Rate  | Sau xáo trộn/noise, baseline + cải tiến duy trì kết quả tốt hơn hoặc tương đương baseline gốc. |

Mỗi RQ/H sẽ được kiểm chứng bằng một hoặc nhiều thí nghiệm tương ứng. Ví dụ, E2 đảm nhận H1 và RQ1, E3 dành cho H2/RQ2, E7 (nếu có) cho RQ3, v.v.

# 2. Môi trường thí nghiệm

- **Phần cứng:**  
  - CPU: Intel Xeon hoặc AMD EPYC (nhiều nhân) hoặc GPU NVIDIA (ví dụ RTX 3090 hoặc A100) tùy theo thiết kế phần mềm.  
  - Bộ nhớ RAM: ≥32 GB để xử lý mô hình ngôn ngữ và cơ sở dữ liệu lớn.  
  - Lưu trữ: SSD tốc độ cao, dung lượng ≥500 GB cho lưu trữ bộ dữ liệu log và vector embeddings.

- **Phần mềm:**  
  - Hệ điều hành: Ubuntu 20.04/22.04 LTS (64-bit).  
  - Ngôn ngữ: Python 3.8–3.10.  
  - Thư viện Machine Learning: PyTorch (≥1.12) hoặc TensorFlow (nếu phù hợp với thiết kế), Transformers (Hugging Face) cho BERT/LLM.  
  - CUDA/cuDNN tương ứng (nếu dùng GPU).  
  - Các thư viện phụ trợ: NumPy, Pandas, scikit-learn, Scipy.  
  - Phiên bản mô hình: BERT-base (như trong baseline), LLM nếu có (ví dụ OpenAI GPT-4 thông qua API hoặc một mô hình LLM open-source tương đương) kèm các tham số (tokenizer, phiên bản).  
  - Nếu có thành phần Retrieval: Elasticsearch/Pinecone hoặc thư viện Faiss cho tìm kiếm vector.  
  - Quản lý thí nghiệm: Weights & Biases hoặc MLflow (nếu có).  
  - Lưu trữ phiên bản mã nguồn (Git), container Docker để tái lập hoàn chỉnh.

Tất cả phiên bản và cấu hình phải được ghi lại để đảm bảo khả năng tái lập. Không khóa công nghệ nếu chưa quyết; tuy nhiên, đề xuất nên cố định phiên bản mô hình/ngôn ngữ (checkpoint), seed ngẫu nhiên.

# 3. Đề cương bộ dữ liệu

Sử dụng các bộ dữ liệu log chuẩn quốc tế liên quan đến phát hiện bất thường. Ví dụ:

- **HDFS (LogHub)**  
  - *Nguồn:* Dữ liệu hệ thống Hadoop (NASA) tại [Loghub](https://github.com/logpai/loghub/tree/master/HDFS).  
  - *Quy mô:* Hàng trăm ngàn bản ghi log; trong tập huấn luyện ~283k sự kiện với ~16 sự cố (theo Oliner et al.).  
  - *Loại log:* Log hệ thống MapReduce, mỗi bản ghi gồm timestamp và bản mẫu sự kiện. Nhãn bất thường là sự cố hệ thống.  
  - *Đặc điểm thời gian:* Dữ liệu có thứ tự thời gian; sẽ được chia theo khoảng thời gian để huấn luyện (các ngày/phiên đầu) và kiểm thử (các ngày/phiên sau). Không cho phép rò rỉ thông tin tương lai.  
  - *Mục đích:* Huấn luyện và kiểm thử chính cho bài toán LAD và ELD.  
  - *Chia tách:* Theo baseline, chia theo log keys (42 khóa cho huấn luyện, 5 khóa chưa biết cho kiểm thử); đồng thời đảm bảo tập huấn luyện và test tách theo thời gian (tránh sử dụng sự kiện sau cho huấn luyện).

- **BGL (BlueGene/L LogHub)**  
  - *Nguồn:* LogHub NASA ([BGL dataset](https://github.com/logpai/loghub/tree/master/BGL)).  
  - *Quy mô:* Hơn 4 triệu bản ghi; tập lớn hơn, có nhiều sự kiện lỗi do Oliner mã định.  
  - *Loại log:* Log máy chủ HPC. Nhãn bất thường đánh dấu lỗi phần cứng/hệ thống.  
  - *Đặc điểm thời gian:* Giống HDFS, phân chia theo trật tự thời gian.  
  - *Mục đích:* Huấn luyện và kiểm thử, bổ sung tính tổng quát.  
  - *Chia tách:* Theo baseline, dùng 414 log keys huấn luyện, 8 còn lại kiểm thử. Cũng chia theo thời gian (ví dụ 70% đầu làm train, 30% cuối làm test) nếu cần.

- **(Tùy chọn) Bộ dữ liệu khác:** Có thể bổ sung một bộ log khác (Spirit, Thunderbird, hay OpenStack logs) để đánh giá tổng quát E7. Tập này phải tương thích (về định dạng log) để thử cross-dataset.

**Kiểm soát thông tin tương lai (Temporal Rule):** Tất cả tập dữ liệu phải được phân chia sao cho mô hình không được phép truy cập bất kỳ thông tin sự kiện xảy ra sau thời điểm hiện tại trong khi huấn luyện hay truy vấn. Cụ thể, không dùng nhãn sự cố/kiến thức hậu nghiệm (future incident) trong huấn luyện. Nếu baseline không hỗ trợ phát hiện sớm thực thụ (ví dụ chỉ phát hiện sau khi lỗi xảy ra), phải nêu rõ giới hạn và cách tính sớm (ví dụ tính Lead Time so với thời điểm lỗi được ghi nhãn).

# 4. Baseline và quy trình so sánh công bằng

## Baseline chính

Baseline được phê duyệt (2025–2026, Q1/Q2) là **LogSentry** (Cui et al., *Scientific Reports*, 2025). Cấu hình và kết quả báo cáo:

- **Phiên bản mô hình:** BERT-base (hoặc tương đương) dùng phương pháp huấn luyện đối sánh (contrastive learning) theo bản gốc. Sau đó fine-tune cho phân loại nhị phân anomaly/normal.  
- **Tiền xử lý:** Sử dụng kết quả log parsing (LogKey sequences) như tác giả.  
- **Thuật toán truy vấn (nếu có):** Trong giai đoạn suy luận, áp dụng KNN trên embedding feature (đã lưu với nhãn cứng). Kết quả KNN trung bình được kết hợp weighted sum với dự đoán của mô hình để ra kết quả cuối cùng.  
- **Ngưỡng phân loại:** Ngưỡng ngầm (threshold) được tác giả đặt (ví dụ 0.5) để phân nhãn. Giữ nguyên như báo cáo.  
- **Kết quả báo cáo:** Theo báo cáo tác giả, LogSentry đạt *F1*-Score cao nhất so với các baseline khác trên bộ HDFS và BGL. Sẽ tái tạo kết quả này để làm mốc so sánh.

Mọi cấu hình của baseline (siêu tham số, preprocessing, code) phải được sao chép chính xác theo tài liệu (tham khảo mã nguồn đính kèm của tác giả nếu có). Kết quả baseline tái tạo sẽ được dùng làm tham chiếu.

## So sánh kiểm soát

So sánh giữa **A: Baseline gốc** và **B: Baseline + Cải tiến mục tiêu**. Các yếu tố cố định:

- Dữ liệu và chia tách (như phần 3).
- Tiền xử lý logs và biểu diễn (embedding).
- Cấu trúc và thông số của mô hình gốc (BERT-base, tầng phân loại).
- Phần retrieval (KNN) sử dụng cùng tham số (như K value).
- Phần cài đặt phần mềm, phần cứng.
- Chính sách ngưỡng phân loại (threshold) nếu cần dùng.

Chỉ thêm/bỏ cải tiến: Ví dụ, nếu cải tiến thêm thành phần LLM, phần B sẽ tích hợp LLM đó; phần A không có. Nếu cần đổi ngưỡng để kiểm soát độ nhạy, phải cho lý do (ví dụ cải tiến có phân phối score khác).

Nếu có baseline phụ (secondary baseline), chỉ dùng khi cần đối chứng phụ (theo yêu cầu từ result-4/5, nhưng ưu tiên tập trung vào baseline chính đã phê duyệt).

# 5. Các kịch bản thí nghiệm

- **E1 – Baseline Reproduction:** Chạy lại hoàn toàn baseline gốc (LogSentry) trên dữ liệu. Mục đích xác nhận code chạy được và tái tạo kết quả tác giả báo cáo trên HDFS/BGL. Kết quả này sẽ là phép so sánh tham chiếu (reference).

- **E2 – Kiểm tra cải tiến chính (Main Improvement Test):** So sánh trực tiếp A (baseline) vs B (baseline + cải tiến). Mục tiêu: đánh giá sự khác biệt về chỉ số phát hiện (Precision, Recall, F1). Thí nghiệm này trung tâm nhất để kiểm chứng liệu cải tiến có khắc phục limitation đã xác định.

- **E3 – Phát hiện sớm (Early Detection Test):** Mô phỏng luồng log (streaming) hoặc chia log theo mốc thời gian sự kiện. Đo các chỉ số Early Detection: Lead Time (thời gian dự báo trước so với sự kiện), Tỉ lệ cảnh báo trước (Early Warning Rate), Tỉ lệ cảnh báo sai (False Alarm Rate). So sánh A vs B để xem cải tiến có đẩy nhanh thời điểm phát hiện không.

- **E4 – Ablation (Thành phần):** Nếu cải tiến gồm nhiều thành phần (ví dụ: thành phần bộ nhớ + thành phần LLM), xây dựng các biến thể: Baseline, Baseline + cải tiến đầy đủ, Baseline + chỉ thành phần 1, Baseline + chỉ thành phần 2, v.v. Mục tiêu phân tích đóng góp riêng của mỗi thành phần.

- **E5 – Độ bền (Robustness):** Thử nghiệm với các biến thể liên quan limitation: thêm nhiễu vào log, bớt sự kiện (missing events), format log mới, hoặc ngẫu nhiên làm mờ dữ liệu. So sánh hiệu năng A và B trong điều kiện bất thường. Mục tiêu: xem cải tiến có làm tăng tính bền bỉ khi gặp dữ liệu thay đổi không.

- **E6 – Hiệu suất (Efficiency):** Nếu cải tiến tốn thêm tài nguyên (ví dụ dùng LLM có độ trễ cao), đo độ trễ xử lý (latency) cho mỗi log/batch, lượng token sử dụng (đối với LLM), thời gian truy vấn retrieval, bộ nhớ GPU, chi phí tính toán. So sánh A vs B để định lượng chi phí-thời gian của cải tiến.

- **E7 – Tổng quát hóa (Generalization):** Đánh giá khả năng áp dụng ở hệ thống khác: ví dụ huấn luyện/baseline trên HDFS, kiểm thử trên BGL hoặc ngược lại (cross-dataset). Hoặc dùng bộ dữ liệu log thứ 3. Mục đích xem cải tiến có cải thiện tính tổng quát so với baseline.

# 6. Các chỉ số đánh giá

- **Phát hiện bất thường (Detection):** Precision, Recall, F1-Score. Ngoài ra có thể dùng PR-AUC, và ROC-AUC nếu phù hợp (nhưng log anomaly thường imbalance, PR-AUC ưu tiên hơn).

- **Phát hiện sớm (Early Detection):**  
  - *Lead Time:* trung bình thời gian giữa khi hệ thống cảnh báo (theo cải tiến) và khi lỗi thật xảy ra.  
  - *Thời gian phát hiện (Time-to-Detection):* tỷ lệ phần sự kiện/ thời gian còn lại trước khi lỗi nếu phát hiện ngay thời điểm.  
  - *Tỉ lệ cảnh báo trước (EAR – Early Alarm Rate):* phần trăm số sự cố được cảnh báo trước thời điểm xảy ra.  
  - *Tỉ lệ phát hiện trước lỗi (Detection Before Failure):* số lượng cảnh báo (ít nhất 1) trước khi lỗi xảy ra.  
  - *Tỉ lệ cảnh báo sai (False Alarm Rate):* FP/(FP+TN), quan trọng đánh đổi.  

  **Lưu ý:** Không chỉ dựa vào F1 chung để đánh giá khả năng phát hiện sớm. Cần báo cáo riêng các chỉ số thời gian.

- **Hiệu năng (Efficiency):** Độ trễ xử lý, số token (nếu LLM), thời gian truy vấn retrieval, chi phí điện toán, lưu lượng nhớ GPU, throughput (số log/s), nếu cải tiến gây overhead.

- **Nếu thành phần cải tiến có chỉ số phụ:** Ví dụ retrieval: Recall@k, Precision@k, MRR. Nếu dùng LLM: tỉ lệ hallucinaton, độ chính xác lập luận (nếu tính được qua bài kiểm thử), chất lượng giải thích (nếu có thuật đánh giá).

# 7. Phân tích thống kê

- Thực hiện **nhiều lần chạy độc lập** (ví dụ 10 lần với các seed khác nhau) cho mỗi thí nghiệm để tính độ lệch chuẩn.  
- Tính **khoảng tin cậy (confidence interval)** cho các metric (ví dụ 95% CI).  
- So sánh có thể dùng **kiểm định phi tham số có ghép đôi** (Wilcoxon signed-rank) giữa baseline và cải tiến trên cùng tập con chạy. (Nếu không ghép đôi, dùng t-test tương ứng.)  
- Tính **kích thước hiệu ứng (effect size)** (như Cohen’s d) để đánh giá mức độ khác biệt.  
- Nếu thực hiện nhiều so sánh (ví dụ nhiều metric hoặc nhiều bộ thử nghiệm), áp dụng **điều chỉnh đa kiểm định** (Bonferroni hoặc Benjamini-Hochberg).  
- Cố định seed, kiểm soát nhiệt độ (đối với LLM), phiên bản model. Ghi lại variance và seed.  

# 8. Tiêu chí thành công

- **Tiêu chí chính:** Chỉ số trực tiếp liên quan đến limitation đã xác nhận (ví dụ F1 hoặc Recall nếu limitation là thiếu detection; Lead Time nếu limitation là phát hiện muộn). Cải tiến được xem “đạt” nếu chỉ số này của nhóm B tăng có ý nghĩa so với A (theo phân tích thống kê).  
- **Tiêu chí phụ:** Bao gồm khả năng phát hiện sớm (Lead Time, EAR), độ bền (khi thêm nhiễu), và hiệu suất (độ trễ, chi phí) ở mức chấp nhận được.  
- **Luật đánh đổi (Trade-off):** Không coi cải tiến thành công chỉ vì F1 tăng nếu: (a) Chi phí tính toán hoặc độ trễ tăng quá nhiều, (b) False Alarm tăng đột biến, (c) Hiệu năng trên tập khác giảm nghiêm trọng. Nếu các yếu tố này tăng đáng kể, cân nhắc coi cải tiến chỉ “một phần thành công”.  
- Không đặt ngưỡng tùy ý. Nếu không có quy chuẩn sẵn, chỉ ghi rõ tiêu chí cần đạt (ví dụ “lead time phải tăng ít nhất 10% so với baseline”).

# 9. Kịch bản Ablation

Nếu cải tiến gồm nhiều thành phần (ví dụ phần truy vấn RAG và phần xử lý LLM riêng biệt), thiết lập thí nghiệm như sau:

- A: Baseline (không có cải tiến).  
- B: Baseline + Cải tiến đầy đủ.  
- C: Baseline + Một phần cải tiến (vd. chỉ thêm retrieval, không dùng LLM).  
- D: Baseline + Thành phần khác (vd. chỉ dùng LLM, không dùng retrieval).  

Mục tiêu: xác định thành phần nào mang lại đóng góp chính. Ví dụ, nếu bỏ một thành phần mà performance giảm về mức baseline, phần đó là nhân tố quan trọng.

# 10. Phân tích lỗi (Error Analysis)

Xác định và phân loại nguyên nhân sai của kết quả B (cải tiến) và A (baseline):

- **False Positive (FP):** Những cảnh báo sai (bình thường bị gán là bất thường). Nguyên nhân: ngưỡng thấp, tín hiệu nhiễu, LLM gây hallucination.  
- **False Negative (FN):** Những bất thường bị bỏ sót. Nguyên nhân: mẫu log mới không học được, thiếu ngữ cảnh.  
- **Early Detection Miss:** Bất thường được phát hiện sau khi nó xảy ra (lead time ≤ 0). Mục: lý do tại sao cải tiến không cảnh báo sớm hơn.  
- **Lỗi trong Retrieval/Context:** Nếu sử dụng RAG, khi retrieval trả về thông tin không phù hợp (irrelevant) dẫn đến dự đoán sai.  
- **Lỗi trong Reasoning/Hallucination của LLM:** Nếu LLM phân tích/giải thích log nhưng tạo thông tin sai, xác định tình huống.  
- **Khoảng kiến thức (Knowledge Gap):** Các trường hợp log hay mẫu hệ thống mới chưa có trong cơ sở tri thức.

Với mỗi loại lỗi, phân tích điều kiện xuất hiện (log dạng gì, giai đoạn nào), nguyên nhân gốc rễ, ảnh hưởng đến giả thuyết. Điều này giúp hiểu tại sao cải tiến không đạt mục tiêu nếu có.

# 11. Phân tích độ bền (Robustness)

Chỉ tập trung vào các phép biến đổi liên quan limitation:

- **Nhiễu trong log:** Thêm log không liên quan, sai định dạng, dữ liệu mất gói, kiểm tra độ ổn định A vs B.  
- **Thiếu sự kiện (Missing events):** Xoá ngẫu nhiên một phần log để xem hệ thống phản ứng thế nào.  
- **Mẫu mới:** Đưa log có keys chưa từng thấy (giống scenario ban đầu của BGL).  
- **Thay đổi định dạng:** Chuyển log từ text sang dạng khác (nếu dự án xử lý thẳng text).  
- **Shift thời gian:** Dữ liệu thời gian khác (log mới từ giai đoạn khác).  
- **Retrieval noise:** Nếu dùng RAG, thử thất bại trong việc truy vấn (tức KNN trả nhãn sai).  
- **Giảm ngữ cảnh:** Chỉ cho mô hình ít sự kiện (giảm window size) và đo độ suy giảm.

# 12. Phân tích hiệu suất và chi phí

Nếu cải tiến dùng LLM/RAG/Memory/Agent:

- Đo **độ trễ (latency):** thời gian để xử lý 1 log hoặc 1 batch log.  
- **Token usage:** Số token gửi/nhận qua API LLM (có thể quy ra chi phí thực tế).  
- **Thời gian truy vấn retrieval:** Thời gian tìm kiếm trong bộ vector/memory.  
- **Số lần gọi model:** Số lần inference LLM/mô hình transformer.  
- **Bộ nhớ GPU:** Đỉnh bộ nhớ cần cho mô hình.  
- **Chi phí tính toán:** Ước tính thời gian GPU-giờ hoặc tiền điện nếu có thể.  

So sánh A vs B; nếu B tăng mạnh các yếu tố trên, đánh giá điều đó liệu có chấp nhận được.

# 13. Kế hoạch khả tái lập

Mỗi kết quả thí nghiệm phải ghi lại chi tiết:

- Dữ liệu: Phiên bản tập dữ liệu (repo & commit, hoặc version loghub), seed tách random (nếu có).  
- Phiên bản code: commit Git cho baseline và cải tiến.  
- Mô hình: Phiên bản/commit của mô hình (BERT base, checkpoint LLM), tokenizer, prompt version nếu dùng.  
- Cấu hình: Tham số hyper (learning rate, epochs, K value, thresholds).  
- Môi trường: Mô tả OS/ Python/ thư viện (có thể requirements.txt hoặc environment.yml).  
- Thông tin ngẫu nhiên: Seed random cho PyTorch, NumPy; nhiệt độ cho LLM; thuật toán tương đương.  
- Kết quả: Lưu kết quả raw (log điểm, confusion matrices, output), và processed (bảng metric). Không lưu khoá API hay credential.  

Tất cả nhằm cho phép người khác tái tạo kết quả một cách đầy đủ.

# 14. Ma trận thí nghiệm

| Thí nghiệm | Baseline (A) | Cải tiến (B) | Mục đích chính      |
| ---------- | ------------ | ------------ | ------------------- |
| **E1**     | ✓            | (không)       | Xác thực baseline   |
| **E2**     | ✓            | ✓            | Cải tiến chính      |
| **E3**     | ✓            | ✓            | Phát hiện sớm       |
| **E4**     | ✓            | ✓/một phần   | Ablation (loại bỏ)  |
| **E5**     | ✓            | ✓            | Độ bền (Robustness) |
| **E6**     | ✓            | ✓            | Hiệu suất (Efficiency) |
| **E7**     | ✓            | ✓            | Tổng quát hóa       |

# 15. Mẫu báo cáo kết quả

Báo cáo kết quả sẽ trình bày theo các mục:

1. **Baseline Reproduction:** Hiện thực lại baseline và kết quả tái tạo; so sánh với kết quả công bố (nếu có). Đánh giá tốt/xấu của việc tái tạo.  
2. **So sánh chính (Main Comparison):** Biểu đồ/bảng kết quả A vs B trên các metric chính (Precision, Recall, F1). Kết luận bất biến hay cải tiến.  
3. **Phát hiện sớm (Early Detection):** Biểu đồ lead-time (ví dụ CDF lead-time), các số liệu EAR, False Alarm. So sánh A vs B.  
4. **Ablation:** Các thử nghiệm loại bỏ thành phần, thể hiện mức đóng góp của từng phần.  
5. **Robustness:** Kết quả khi thêm biến động (noise, missing data). Đánh giá xu hướng khác biệt.  
6. **Efficiency/Cost:** Bảng/biểu đồ chi phí thời gian, tài nguyên; so sánh.  
7. **Bằng chứng thống kê (Statistical evidence):** Bảng giá trị trung bình ± CI cho mỗi metric; p-value và effect size cho các so sánh chính.  
8. **Phân tích lỗi (Error Analysis):** Mô tả các mẫu lỗi quan sát được, ví dụ trường hợp nổi bật dẫn đến FP/FN. Thảo luận nguyên nhân.  
9. **Hạn chế (Limitations):** Thực tiễn, giả định hoặc bất kỳ vấn đề nào của thiết kế thí nghiệm (ví dụ tính khả dụng của tập dữ liệu).

# 16. Quy tắc diễn giải kết quả

- **Supported (Có ý nghĩa):** Cải tiến cho kết quả tốt hơn và khác biệt thống kê (p<0.05) cho metric chính.  
- **Weakly Supported (Hỗ trợ nhẹ):** Có xu hướng cải thiện nhưng không đủ mạnh (e.g. p~0.05–0.1 hoặc variance lớn).  
- **Not Supported (Không được chứng minh):** Không thấy cải tiến (mức tương đương, hoặc hiệu quả tăng không đáng kể).  
- **Contradicted (Ngược lại):** Cải tiến làm giảm hiệu năng hoặc các metric tệ hơn đáng kể.

Không kết luận chỉ dựa vào một metric đơn lẻ hoặc một bộ dữ liệu duy nhất. Ví dụ F1 tăng nhưng Recall giảm nhiều có thể coi là chưa hỗ trợ. Nếu cải tiến không hiệu quả (Not Supported/Contradicted), vẫn báo cáo trung thực và phân tích tại sao. Đây là kết quả nghiên cứu có ý nghĩa.

# 17. Nguy cơ ảnh hưởng tính hợp lệ

- **Nội bộ (Internal validity):** Rủi ro do cài đặt sai (implementation bias), điều chỉnh tham số thiếu công bằng, rò rỉ dữ liệu (data leakage) giữa train/test, khác biệt cấu hình môi trường. *Giảm thiểu:* Kiểm tra code, dùng seed cố định, đảm bảo pipeline hẹp đúng.  
- **Bên ngoài (External validity):** Mức độ tổng quát hóa hạn chế nếu chỉ dùng một vài bộ dữ liệu chuẩn. *Giảm thiểu:* Dùng nhiều bộ dữ liệu (E7), nêu rõ phạm vi áp dụng.  
- **Cấu trúc (Construct validity):** Các metric có đo đúng Early Detection? Nếu label không ghi rõ thời điểm sớm, có thể không phản ánh đúng. *Giảm thiểu:* Sử dụng kết hợp nhiều metric, nêu rõ tiêu chí tính Lead Time.  
- **Kết luận (Conclusion validity):** Số lần chạy quá ít, variance cao, thiếu năng lực thống kê. *Giảm thiểu:* Chạy lặp, test thống kê thích hợp.  
- **Mô hình nền (Foundation Model):** Nếu dùng LLM, lưu ý drift (thay đổi theo phiên bản), nondeterministic output (nhiệt độ). *Giảm thiểu:* Cố định model/version, test nhiều seed prompt.  
- **Retrieval/Context:** Cơ sở kiến thức cũ (stale data) hoặc irrelevant retrieval có thể gây sai. *Giảm thiểu:* Xây dựng cơ sở dữ liệu phù hợp tách theo thời gian, kiểm thử retrieval với dữ liệu mới.  

Mỗi nguy cơ đều cần được bàn luận ngắn gọn và phương án giảm thiểu (như trên).

# 18. Độ sẵn sàng công bố

Kiểm tra các tiêu chí:

- RQ/H đã được xác định, thiết kế thí nghiệm đáp ứng, không thay đổi từ proposal.  
- Baseline đã được tái tạo đúng (E1) và so sánh công bằng.  
- So sánh chính (A vs B) minh bạch, công bằng (thuật toán, tập dữ liệu giống nhau).  
- Đã đo đủ metric Early Detection riêng biệt (không chỉ F1).  
- Ablation thực hiện để xác nhận tính hiệu quả của thành phần cải tiến.  
- Bằng chứng thống kê được cung cấp (p-value, CI, effect size).  
- Các artifact (dataset splits, code, kết quả) được ghi nhận để tái tạo.  
- Hạn chế thí nghiệm được báo cáo trung thực (ví dụ: dữ liệu tập nhỏ, giả định...).  

Nếu tất cả các mục trên được đáp ứng, báo cáo sẵn sàng cho đánh giá.

# 19. Xác minh thông tin xếp hạng Q1/Q2 và xuất bản

| Tạp chí        | Năm | Nguồn Xếp hạng    | Hạng (Quartile) | Xuất bản chính thức | DOI                          |
| ---------------| --- | ----------------- | --------------- | ------------------- | ---------------------------- |
| *Scientific Reports* | 2025/2026 | Clarivate JCR (2024) | Q1 (NATURE Portfolio) | Official (open access, peer-reviewed) | 10.1038/s41598-025-22208-7 |

- **Kết luận:** Baseline *LogSentry* được xuất bản trên *Scientific Reports* năm 2025 (online 2026), tạp chí thuộc Clarivate Q1 (dữ liệu JCR 2024), có DOI chính thức. Đáp ứng mọi tiêu chí (2023–2026, Q1/Q2, peer-review, DOI).  

Nếu không đủ bằng chứng thì sẽ ghi chú “Không đủ bằng chứng → không hợp lệ” (trong trường hợp không tìm được xếp hạng), nhưng ở đây chúng ta có xác minh năm xuất bản và DOI, và xác minh hạng Q1.  

# 20. Kết luận thí nghiệm cuối cùng

| Nghiên cứu phần tử | Bằng chứng                | Kết luận        | Độ tin cậy |
| -------------------| ------------------------- | --------------- | ---------- |
| **RQ1**            | Chưa có (chờ chạy E2)    | Chưa đánh giá được | Rất thấp (0%) |
| **RQ2**            | Chưa có (chờ chạy E3)    | Chưa đánh giá được | Rất thấp |
| **RQ3**            | Chưa có (chờ chạy E7)    | Chưa đánh giá được | Rất thấp |
| **H1**             | Chưa có (chờ E2)        | Chưa đánh giá được | Rất thấp |
| **H2**             | Chưa có (chờ E3)        | Chưa đánh giá được | Rất thấp |
| **H3**             | Chưa có (chờ E5)        | Chưa đánh giá được | Rất thấp |

- **Kết luận chính:** Do chưa thực hiện thí nghiệm thực tế, hiện chưa có bằng chứng để xác nhận hay bác bỏ cải tiến so với baseline.  
- **Hạn chế lớn:** Thiếu kết quả thực nghiệm, không thể khẳng định cải tiến giải quyết limitation thế nào.  
- **Thương lượng:** Chưa áp dụng được (chờ đánh giá chi phí-lợi ích).  
- **Bước tiếp theo:** Triển khai hoàn chỉnh cải tiến (theo design), chạy các kịch bản E1–E7, thu thập dữ liệu và đánh giá.  

*Lưu ý:* Kết luận và độ tin cậy sẽ được cập nhật sau khi có kết quả thực nghiệm. Các giá trị trên là mặc định khi chưa có thử nghiệm thực tế. 

