# 1. Đánh giá các Cơ hội Nghiên cứu

Dựa trên phân tích trong `result-3.md`, chúng tôi xác định các **cơ hội cải tiến** chủ yếu sau (tập trung theo hướng nâng cao sớm phát hiện dị thường log):

| Cơ hội nghiên cứu                   | Baseline (2025–26)                        | Giới hạn chính                                                | Bằng chứng (Evidence)                                  | Hướng cải tiến                       | Lợi ích kỳ vọng                                             | Tính khả thi (đánh giá)      | Rủi ro chính                                            |
|------------------------------------|-----------------------------------------|-------------------------------------------------------------|-------------------------------------------------------|-------------------------------------|-----------------------------------------------------------|-----------------------------|--------------------------------------------------------|
| **NÂNG CẤP KÉT HỢP LẤY NGỮ CẢNH (RAG)** <br/>(*Retrieval-Augmented Generation*) | Phương pháp LLM/mô hình ngôn ngữ hiện đại (ví dụ prompt-based LLM như LogPrompt/EagerLog)| Thiếu bối cảnh lịch sử; mô hình chỉ xử lý chuỗi log ngắn gọn tại một thời điểm, không tận dụng được log quá khứ quan trọng.                                    | Nghiên cứu đã chỉ ra RAG giúp đưa thông tin lịch sử bổ sung vào đánh giá dị thường. | Thêm thành phần truy vấn/văn bản vào bộ nhớ log (vector DB) cho LLM, phục vụ tăng cường ngữ cảnh lịch sử. | Trung bình: cần xây hệ thống truy xuất cơ sở dữ liệu ngữ cảnh, triển khai LLM thế hệ lớn. | Phụ thuộc dữ liệu log lịch sử chất lượng; tăng độ trễ xử lý vì truy vấn RAG.   |
| **BỘ NHỚ NGẮN/DÀI HẠN (Memory-Augmented)** | Mô hình LLM/RAG hiện tại (như RAGLog)   | Mất thông tin dài hạn: Log phát sinh qua nhiều thời điểm/phát hiện đa giai đoạn không được ghi nhớ; mô hình “quên” các mô-típ cũ.                | Mô hình DM-RAG đề xuất bộ nhớ ngắn hạn và dài hạn giúp nhận diện đa giai đoạn (Độ nhạy tăng lên). | Tích hợp cơ chế bộ nhớ ngoài (faiss, replay buffer) cho LLM/RAG, giúp lưu giữ mẫu log bất thường. | Khá: cơ sở tri thức dạng vector đã có (FAISS), mô hình LLM nhẹ (Phi-4-mini). Thời gian xây dựng vừa phải. | Phức tạp trong duy trì bộ nhớ; cần nghiệm thu phê duyệt mẫu lưu; khả năng trôi dạt bộ nhớ.     |
| **CHAIN-OF-THOUGHT + RL (Giải trình và Tối ưu bằng RL)** | LLM prompt/fine-tune truyền thống (như LogGPT) | Mô hình thiếu khả năng lập luận có cấu trúc; thường tung ra kết quả không giải thích được (“hallucination”); thiếu tin cậy.  | Các báo cáo gần đây (RationAnomaly) cho thấy huấn luyện theo CoT và RL giảm hiện tượng ảo tưởng, cải thiện độ chính xác và minh giải quyết định. | Fine-tune LLM theo chuỗi suy luận (CoT), kết hợp huấn luyện tăng cường với hàm thưởng đa mặt nhằm tối ưu tính chính xác và logic. | Khó: cần bộ dữ liệu có lời giải thích (CoT) và vòng RL. Tuy nhiên, nền tảng mã/mô hình công khai có sẵn (GPT-4o, LoRA) hỗ trợ. | Chi phí huấn luyện cao; thiết kế hàm thưởng phức tạp; LLM có thể mất định tính ban đầu.           |
| **ĐỒ THỊ TRI THỨC (GraphRAG, Knowledge Graph)** | Phân tích log thuần túy (không có KG)    | Không khai thác kiến thức cấu trúc hệ thống; mất mối quan hệ giữa thực thể/thiết bị.                                      | *Chưa có chứng cứ cụ thể trong các tài liệu đầu vào về hiệu quả trên log.*         | Xây KG/quora kế hoạch hệ thống, dùng GraphRAG để truy xuất thông tin liên quan.             | Thấp: cần tạo/sản xuất KG phức tạp; ít bằng chứng ứng dụng cho log anomaly.    | Độ phức tạp cao, khó thu thập KG; rủi ro về sai lệch dữ liệu kiến thức.      |
| **AI Cơ giới hoá (Agentic AI)** | Mô hình đơn thuần                | Thiếu khả năng tự động hoá các bước phức tạp, chỉ đưa ra dự báo một lần.                                   | *Không tìm thấy bằng chứng rõ ràng trong input.*                                             | Sử dụng multi-agent/TO-BEM để chia nhỏ quy trình chẩn đoán.                             | Thấp: không có chuẩn mực, đòi hỏi kiến trúc mới và hiệu chỉnh phức tạp.    | Quá tải kiến trúc, lỗi giữa các tác vụ, tiêu tốn thời gian.          |

- *Lưu ý:* Đã bỏ **GraphRAG** và **Agentic AI** vì bằng chứng yếu và phạm vi quá rộng, không phù hợp hạn mức luận văn. Các cơ hội chính còn lại đều có “baseline” cụ thể và thể hiện rõ hạn chế cần cải tiến.

# 2. Ba Đề xuất Nghiên cứu Ưu tiên

Sau khi đánh giá các cơ hội với tiêu chí (*bằng chứng*, *tính khả thi*, *mức độ chuyên sâu*), chúng tôi chọn ba đề xuất dưới đây:

- **C1: Mô hình LLM kết hợp RAG cho Phát hiện Dị thường sớm.**  
  *Baseline:* Phương pháp LLM hiện tại (ví dụ prompt-based LLM như EagerLog/LogPrompt) mà không dùng lịch sử log. *Giới hạn:* Ngữ cảnh ngắn, không xem lại log lịch sử → Mất dị thường lâu dài. *Cải tiến:* Thêm bộ nhớ truy vấn (vector DB) chứa log chuẩn/tiền sử và tích hợp Retrieval to Context cho LLM. *Lợi ích:* Mở rộng bối cảnh, tăng khả năng phát hiện các mẫu dị thường lặp lại theo thời gian. *Khả thi:* Chi phí lưu trữ và tính toán chấp nhận được (vector DB có sẵn); sử dụng mô hình có sẵn để thực hiện RAG. *Đánh giá:* So sánh độ nhạy/F1 với baseline và LLM gốc, đo ** thời gian phát hiện** ban đầu (Time-to-Detection). *Giá trị:* Có ý nghĩa thực tiễn cao khi hệ thống giám sát có thể cảnh báo kịp thời. *Xuất bản:* Kết quả tốt có thể gửi Conf. ML/NLP (ICML, ACL Workshops).

- **C2: Mô hình LLM + RAG với Bộ nhớ Ngoại lai (Memory) cho Log Dị thường.**  
  *Baseline:* Phương pháp tương tự RAGLog (2023) hay RAG-enhanced LLM, không có cơ chế nhớ liên tục. *Giới hạn:* Khi log được xử lý theo session ngắn, các mẫu bất thường ở session trước không được ghi nhớ. *Cải tiến:* Thêm thành phần bộ nhớ song song (short-term và long-term memory như DM-RAG) để lưu giữ các biểu hiện log bất thường lâu dài. *Lợi ích:* Tăng khả năng phát hiện dị thường đa giai đoạn (tăng Recall cao) mà vẫn giữ độ phủ sóng rộng. *Khả thi:* Cần training thêm cho LLM dùng memory; sử dụng FAISS-indexed DB; có mã mẫu tham khảo (Phi-4-mini đã dùng). *Đánh giá:* So sánh hiệu năng recall/F1 giữa RAGLog cũ và phiên bản mới, đánh giá tình huống đa giai đoạn (trigger lead-time). *Giá trị:* Kết quả có tính khoa học khi chứng minh giá trị của bộ nhớ kéo dài trong giám sát; nếu thành công, tiềm năng gửi bài cho TPDS hoặc ICLR Workshop.  

- **C3: LLM với Chain-of-Thought & RL cho Độ tin cậy và Giải thích.**  
  *Baseline:* Phương pháp LLM đơn giản (prompt-based hoặc fine-tuned như LogGPT) phát hiện dị thường bằng cách suy diễn trực tiếp. *Giới hạn:* Dễ sinh *hallucination*, thiếu diễn giải logic; ảnh hưởng độ tin cậy và giải thích kết quả. *Cải tiến:* Huấn luyện LLM theo chuỗi suy luận (CoT) với dữ liệu có lời giải thích, kết hợp tinh chỉnh qua Reinforcement Learning để tối ưu accuracy và giảm hallucination. *Lợi ích:* Cải thiện độ chính xác, tăng tính giải thích và độ tin cậy của phát hiện. *Khả thi:* Có thể tận dụng mô hình sẵn (ChatGPT/GPT-4 để tạo tập CoT), dùng LoRA để fine-tune, áp dụng thuật toán RL. *Đánh giá:* So sánh F1, giảm hallucination (ví dụ metric chất lượng giải thích); xác định trade-off về thời gian inference do CoT dài hơn. *Giá trị:* Tăng cường tính minh bạch của hệ thống AIOps; phù hợp với yêu cầu bài toán công nghiệp cần giải thích, có thể đăng tại các hội nghị chuyên ngành AI (NeurIPS Workshop, ICDM).

# 3. Định vị Nghiên cứu (Research Positioning) của mỗi phương án

### *Đề xuất C1: “LLM + RAG”*  
- **Baseline:** Phương pháp LLM hiện đại cho log anomaly (LogPrompt/EagerLog).  
- **Giới hạn:** Mô hình bị giới hạn context window; không khai thác lịch sử log dài. Điều này làm bỏ sót các mẫu bất thường lặp lại theo thời gian.  
- **Cải tiến hướng tới:** Kết hợp Retrieval Augmentation – dùng DB log tiền sử (vector embedding) để cung cấp thêm ngữ cảnh liên quan khi LLM xử lý log mới.  
- **Mức đóng góp:** *Targeted Improvement* – chỉ bổ sung module RAG vào pipeline hiện tại. Mô hình gốc và cấu trúc chính được giữ nguyên, chỉ mở rộng bối cảnh dữ liệu.  

### *Đề xuất C2: “RAG + Bộ nhớ”*  
- **Baseline:** Phương pháp RAGLog (Phan et al., 2023) hoặc tương đương – LLM kết hợp RAG nhưng chưa có bộ nhớ ngoài.  
- **Giới hạn:** Thiếu cơ chế ghi nhớ lâu dài; các anomalis trong quá khứ bị quên đi (issue trong phát hiện đa giai đoạn).  
- **Cải tiến hướng tới:** Thêm hai luồng bộ nhớ song song – bộ nhớ ngắn hạn (ghi nhận pattern mới) và dài hạn (ghi pattern quan trọng) như DM-RAG. Đây là *extension* để lưu lại thông tin hữu ích qua phiên.  
- **Mức đóng góp:** *Targeted Improvement* – mở rộng baseline RAGLog với thành phần memory; giữ phần LLM/RAG cốt lõi và bổ sung mới.  

### *Đề xuất C3: “LLM + Chain-of-Thought + RL”*  
- **Baseline:** Mô hình LLM gốc (ví dụ LogGPT hoặc GPT-4 prompt-based) cho log anomaly detection.  
- **Giới hạn:** Dễ sinh *hallucination*, thiếu reasoning rõ ràng; đồng thời thiếu khả năng giải thích và tin cậy.  
- **Cải tiến hướng tới:** Áp dụng *Chain-of-Thought supervised fine-tuning* để truyền đạt lô-gíc chuyên gia, kết hợp *Reinforcement Learning Alignment* để tối ưu hóa cho tính chính xác và sự nhất quán.  
- **Mức đóng góp:** *Targeted Improvement* – nâng cấp phương thức huấn luyện LLM, không thay đổi hoàn toàn kiến trúc; thêm bước đào tạo CoT+RL.  

# 4. Ba Đề xuất Luận văn Cụ thể

## Đề xuất 1: **Cải thiện LLM cho Phát hiện Dị thường sớm bằng cách tích hợp Truy Xuất Log Lịch Sử (RAG)**

### 4.1 Tiêu đề nghiên cứu  
- **Tiếng Anh:** *Enhancing a 2025 LLM-based Anomaly Detector for Early Log Anomaly Detection via Retrieval-Augmented Context.*  
- **Tiếng Việt:** *Cải thiện Phương pháp Phát hiện Dị thường Log năm 2025 bằng Truy xuất Ngữ cảnh (RAG).*  

### 4.2 Định vị Nghiên cứu  
- **Baseline:** Phương pháp phát hiện dị thường log dựa trên Large Language Model (LLM) như EagerLog/LogPrompt (prompt-based).  
- **Giới hạn:** Thiếu ngữ cảnh lịch sử: mô hình chỉ xử lý chuỗi log hiện tại, bỏ sót thông tin quan trọng từ logs trước đó.  
- **Cải tiến:** Kết hợp Retrieval-Augmented Generation (RAG) để truy vấn thêm các bản ghi log liên quan từ cơ sở dữ liệu vector. Đây là cấp độ *Targeted Improvement* (mở rộng có chủ đích) bởi nó giữ nguyên lõi LLM và chỉ thêm module RAG.  

### 4.3 Bối cảnh nghiên cứu  
- **Vấn đề:** Các hệ thống phần mềm hiện đại tạo ra khối lượng log rất lớn; phát hiện sớm các dấu hiệu bất thường trong log là then chốt để ngăn chặn lỗi nghiêm trọng. Truy cập bối cảnh lịch sử (ví dụ log chuẩn của tình huống tương tự) có thể giúp xác định bất thường mới.  
- **Động lực:** Kết quả từ RAGLog cho thấy RAG có tiềm năng khi lượng log hiện hữu khổng lồ. Ngược lại, LLM đơn thuần thường bỏ sót dị thường liên tục nếu không có thông tin từ log cũ.  
- **Bối cảnh công nghiệp:** Nhiều tổ chức (telecom, tài chính) ghi nhật ký hàng ngày và cần hệ thống giám sát AIOps chủ động. Mô hình tích hợp RAG giúp tận dụng lịch sử log tổ chức, cung cấp thông tin phong phú hơn so với chuỗi hiện tại.  
- **Baseline tồn tại:** LogPrompt/EagerLog (2025) sử dụng LLM để gán nhãn log mà không xem xét lịch sử [22†L114-119]. Những hạn chế của nó đã được nêu trong phân tích kết quả-2.  
- **Hạn chế của baseline:** Như [10†L22-L30] chỉ ra, không có dị thường trong tập huấn luyện, RAG tăng cường để bổ sung bằng chứng lịch sử. LLM gốc thiếu khả năng so sánh logs liền kề.  
- **Nhu cầu cải tiến:** Từ kết quả ưu tiên (result-3), khả năng thiếu ngữ cảnh lịch sử là lỗ hổng. Nâng cấp bằng RAG được chứng minh giảm sai sót và cải thiện recall.  

### 4.4 Câu hỏi nghiên cứu (RQ)  
1. **RQ1:** Thiếu ngữ cảnh lịch sử (bản ghi log trước) ảnh hưởng nghiêm trọng như thế nào đến hiệu năng baseline?  
2. **RQ2:** Việc tích hợp RAG (truy xuất log lịch sử) có làm giảm lỗi phát hiện thiếu (False Negative)?  
3. **RQ3:** Hệ thống LLM+RAG có nâng cao tốc độ phát hiện sớm (Time-to-Detection, Lead Time) so với LLM gốc không?  
4. **RQ4:** Có đánh đổi nào về độ trễ hay chi phí tính toán khi thêm RAG?  

### 4.5 Mục tiêu nghiên cứu  
- **Mục tiêu chung:** Cải thiện một hạn chế cụ thể (ngữ cảnh lịch sử bị bỏ sót) của phương pháp 2025 bằng cách tích hợp RAG, nhằm nâng cao khả năng phát hiện dị thường sớm.  
- **Mục tiêu cụ thể:**  
  1. Xây dựng lại/bắt chước baseline LLM (LogPrompt/EagerLog).  
  2. Đo lường hiệu năng baseline (F1, recall, time-to-detection).  
  3. Thiết kế và triển khai module RAG: xây dựng cơ sở dữ liệu vector logs, thiết lập pipeline truy vấn.  
  4. Thử nghiệm so sánh baseline vs phiên bản có RAG trên cùng tập dữ liệu.  
  5. Phân tích ablation: so sánh với các cấu hình thay thế (ví dụ chỉ truy vấn 10 log gần nhất, không RAG).  
  6. Đánh giá khả năng phát hiện sớm: đo thời gian trung bình và tỷ lệ cảnh báo trước lỗi thực tế (nếu dữ liệu hỗ trợ).  
  7. Phân tích đánh đổi: tăng độ chính xác có đi kèm với độ trễ/tranh phí tính toán (latency, token-cost).  
  8. Rà soát thất bại: trong trường hợp RAG không cải thiện, phân tích nguyên nhân (ví dụ log lịch sử ít liên quan).  

### 4.6 Giả thuyết (Hypotheses)  
- **H1:** Hệ thống LLM+RAG sẽ có *Recall* chính tốt hơn (độ nhạy dị thường) so với LLM gốc (giúp phát hiện dị thường bị bỏ sót).  
- **H2:** Hệ thống LLM+RAG sẽ giảm tỷ lệ sai sót (FN) liên quan đến các mẫu bất thường lặp lại qua các phiên log.  
- **H3:** Thời gian phát hiện trung bình sẽ thấp hơn (cảnh báo sớm hơn) so với baseline LLM.  
- **H4:** Sử dụng RAG không làm tăng độ trễ vượt quá giới hạn cho phép (ví dụ <20% so với baseline).  

### 4.7 Đóng góp mong đợi  
- **Khoa học:** Chứng minh rằng tích hợp truy xuất ngữ cảnh lịch sử (RAG) thực sự cải thiện hiệu năng phát hiện dị thường sớm. Xác định điều kiện hiệu quả (vd: loại logs, tỷ lệ mất lẻ của dị thường).  
- **Phương pháp luận:** Mở rộng một giải pháp baseline bằng cách thêm thành phần RAG cụ thể; công bố mã nguồn và quy trình tái tạo cho LLM+RAG trên bộ dữ liệu benchmark.  
- **Kỹ thuật:** Đóng gói pipeline RAG cho vấn đề log anomaly detection. Cung cấp tài liệu và hướng dẫn reproducible.  
- **Công nghiệp:** Nếu có chứng cứ từ dữ liệu thực tiễn (logs hệ thống), chỉ ra giá trị tích hợp RAG trong giám sát.  

## Đề xuất 1 – Phương pháp luận (Methodology)

**Cấu hình Baseline:**  
- **Đầu vào:** Chuỗi log của hệ thống (templates, timestamps).  
- **Mô hình core:** LLM (ví dụ GPT-4o hay LLaMA) nhận log sequence, đưa ra phán đoán bất thường.  
- **Quá trình phát hiện:** Không có thành phần truy xuất.  
- **Đầu ra:** Xác suất dị thường hoặc nhãn normal/abnormal cho mỗi entry.  

**Cải tiến (RAG):**  
- **Thành phần thêm:** Cơ sở dữ liệu embedding log lịch sử (vector store).  
- **Chi tiết:** Với mỗi log đầu vào, sinh query embedding và truy xuất `k` log tương tự từ DB. Kết hợp chúng vào prompt cho LLM (ví dụ dưới dạng “{recent logs}: ..., current log: ...”).  
- **Giải quyết giới hạn:** Giúp LLM có bối cảnh rộng hơn, giảm bỏ sót pattern lặp lại.  
- **Giữ nguyên:** Tất cả phần còn lại của pipeline (preprocessing, lõi LLM) giữ giống baseline.  

**Mô hình cải tiến:**  
- **LLM input:** *Baseline component + Retrieved context logs* → xử lý bởi cùng LLM.  
- **Output:** Các phán đoán với ngữ cảnh thêm, kỳ vọng cải thiện recall.  

## Đề xuất 2: **Thêm Bộ nhớ cho RAG-Based LLM** 

### 4.1 Tiêu đề nghiên cứu  
- **Tiếng Anh:** *Incorporating Episodic Memory into a RAG-based Log Anomaly Detector to Improve Early Detection.*  
- **Tiếng Việt:** *Tích hợp Bộ nhớ bên ngoài vào Mô hình RAG cho Phát hiện Dị thường sớm trong Log.*  

### 4.2 Định vị Nghiên cứu  
- **Baseline:** Phương pháp RAGLog (RAG + LLM) đời 2023–2025.  
- **Giới hạn:** Chưa có cơ chế ghi nhớ dài hạn; khi xử lý nhiều phiên, model không tích lũy thông tin.  
- **Cải tiến:** Thêm cơ chế nhớ (persistent memory) hai cấp như DM-RAG, ghi lại các mẫu log quan trọng theo thời gian. *Đóng góp:* Targeted Improvement – mở rộng pipeline, thêm thành phần memory.  

### 4.3 Bối cảnh nghiên cứu  
- **Vấn đề:** Đối với các hệ thống dài hạn, pattern bất thường có thể xuất hiện rải rác theo thời gian. Mô hình chỉ nhìn vào session hiện tại bỏ lỡ tri giác liên tục.  
- **Baseline:** RAGLog cho phép truy xuất bối cảnh, nhưng mỗi truy vấn độc lập.  
- **Hạn chế:** Theo Guo et al. (2025), LLM/RAG cố định context không duy trì dấu vết qua nhiều phiên. Hệ thống dễ mất các cuộc tấn công kéo dài qua nhiều bước.  
- **Nhu cầu:** Do đó cần bộ nhớ dài hạn. DM-RAG đã thành công tăng recall trong ngữ cảnh bảo mật. Áp dụng tương tự cho dị thường hệ thống chung.  

### 4.4 Câu hỏi nghiên cứu  
1. **RQ1:** Thiếu bộ nhớ dài hạn ảnh hưởng thế nào đến khả năng phát hiện dị thường đa giai đoạn?  
2. **RQ2:** Thêm thành phần bộ nhớ (kết hợp cả bộ nhớ ngắn/dài hạn) có tăng recall và giảm false negatives?  
3. **RQ3:** Kết hợp bộ nhớ ngoài có giảm *thời gian phát hiện trung bình* không?  
4. **RQ4:** Chi phí lưu trữ và truy vấn bộ nhớ có phù hợp giới hạn thực nghiệm?  

### 4.5 Mục tiêu nghiên cứu  
1. Tái hiện baseline RAGLog (LLM + RAG) và đo lường hiệu năng.  
2. Đánh giá mức độ hạn chế của baseline về thông tin ngắn hạn (độ nhạy qua thời gian).  
3. Thiết kế module bộ nhớ: xây FAISS vector store cho memory, chính sách thêm log mẫu (promotion strategy) theo Guo et al. [12†L69-L77].  
4. Đào tạo LLM/RAG với việc dùng memory (bổ sung prompt với logs từ memory).  
5. So sánh baseline vs hệ thống mới (precision, recall, F1, lead time).  
6. Thử nghiệm ablation: không có bộ nhớ ngắn, không có bộ nhớ dài; chỉ RAG.  
7. Đánh giá khả năng phát hiện sớm của bộ nhớ: liệu nó giữ được cảnh báo cho kỳ hạn dài hơn?  
8. Phân tích latency: đánh giá chi phí truy vấn bộ nhớ.  

### 4.6 Giả thuyết  
- **H1:** Hệ thống RAG+Memory có độ *Recall* dị thường cao hơn baseline RAG đơn.  
- **H2:** Thêm bộ nhớ giảm đáng kể *False Negatives* với các mẫu bất thường xuất hiện theo đợt.  
- **H3:** Hệ thống mới cảnh báo dị thường muộn hơn ít nhất một phiên log trước khi sự cố so với baseline.  
- **H4:** Độ trễ xử lý tăng thêm do truy vấn memory nằm trong giới hạn chấp nhận được (<10%).  

### 4.7 Đóng góp mong đợi  
- **Khoa học:** Cung cấp bằng chứng về hiệu quả của bộ nhớ lâu dài trong anomaly detection (chưa nhiều tài liệu). Xác định điều kiện (loại anomaly, khoảng cách thời gian).  
- **Phương pháp luận:** Mô hình DM-RAG mở rộng cho log chung, đưa ra quy trình reproducible.  
- **Kỹ thuật:** Triển khai module memory (index và retrieval) kết hợp với LLM. Đóng gói code.  
- **Công nghiệp:** Thể hiện cách tích hợp logs lâu dài (phiên gia tăng) vào hệ AIOps, cải thiện tính liên tục của phát hiện.

## Đề xuất 2 – Phương pháp luận

**Baseline:** RAGLog (Phi-4-mini hay GPT-4 với prompt): Xử lý log mới + truy xuất lịch sử, **không** có memory.  
**Cải tiến (Memory):**  
- **Component thêm:** Hai bộ nhớ **ngắn hạn** (recent summary buffer) và **dài hạn** (FAISS-indexed).  
- **Hoạt động:** Mỗi phiên log mới, LLM nhận cả log và các trích dẫn từ memory (theo cơ chế DM-RAG). Bộ nhớ cập nhật: nếu LLM phân loại tin tưởng, log bất thường được push vào memory lâu dài sau quá trình tóm tắt.  
- **Mục tiêu:** Giữ lại thông tin về các bất thường đã phát hiện để dùng trong tương lai, cải thiện phát hiện đa giai đoạn.  

**Mô hình cải tiến:**  
- **LLM input:** *Log hiện tại* + *Retrieved context* + *Summary từ memory dài hạn*.  
- **Kết quả:** Nhanh hơn trong phát hiện pattern tái lặp.

## Đề xuất 3: **LLM với Chain-of-Thought và RL cho Phát hiện Dị thường**

### 4.1 Tiêu đề nghiên cứu  
- **Tiếng Anh:** *Improving LLM-Based Log Anomaly Detection via Chain-of-Thought Fine-Tuning and Reinforcement Learning Alignment.*  
- **Tiếng Việt:** *Cải thiện Phát hiện Dị thường Log dựa trên LLM bằng Chain-of-Thought và Tối ưu tăng cường.*  

### 4.2 Định vị Nghiên cứu  
- **Baseline:** LLM đơn (LogGPT/GPT-4) không có huấn luyện CoT, chỉ trả về kết quả đúng/sai.  
- **Giới hạn:** Hallucination cao, thiếu giải trình (đã thấy trong [22†L80-L85]).  
- **Cải tiến:** Huấn luyện theo CoT (dữ liệu mẫu bước suy luận) và RLAlignment để giảm hallucination. *Loại đóng góp:* *Targeted Improvement* về huấn luyện LLM.  

### 4.3 Bối cảnh nghiên cứu  
- **Vấn đề:** Nhiều giải pháp LLM cho log anomaly chưa tập trung vào khả năng giải thích. Giải sử lỗi và độ tin cậy quan trọng trong AIOps.  
- **Baseline:** LogGPT, RAGLog, SuperLog (2024) cho phép phát hiện nhưng không có cơ chế reasoning rõ ràng.  
- **Hạn chế:** [22†L80-L85] chỉ ra rằng các phương pháp prompt/fine-tune chuẩn thường bị sai lầm do thiếu logic; kết quả thiếu minh bạch.  
- **Cơ hội:** Áp dụng ý tưởng từ RationAnomaly – huấn luyện LLM với dữ liệu có lời giải thích hệ thống và cho máy học qua RL nhằm tăng độ chính xác và giảm hallucin.  

### 4.4 Câu hỏi nghiên cứu  
1. **RQ1:** Baseline LLM mắc bao nhiêu lỗi do hallucination?  
2. **RQ2:** Huấn luyện CoT có giảm sai lệch phân loại không (tăng độ chính xác)?  
3. **RQ3:** RLAlignment có cải thiện độ tin cậy và logic khi phát hiện (giảm các trường hợp sai lô-gíc)?  
4. **RQ4:** Có độ trễ hoặc sai lệch nào do pipeline dài (CoT) gây ra?

### 4.5 Mục tiêu nghiên cứu  
1. Triển khai baseline LLM (LogGPT hoặc GPT-4) để dự đoán nhãn (normal/abnormal) cho từng log.  
2. Xác định và đo lỗi chủ yếu (hallucinations, thiếu logic) trên bộ dữ liệu đã hiệu chỉnh.  
3. Tạo tập dữ liệu Chain-of-Thought: sử dụng GPT-4o tạo lời giải thích từng bước cho các logs (theo chuyên gia).  
4. Huấn luyện LLM qua CoT (LoRA fine-tuning theo huấn luyện có giám sát các bước suy luận).  
5. Tiếp theo, áp dụng RL (cơ chế giống RLA trong [22]) với reward kết hợp: tăng thưởng cho phát hiện đúng anomaly, cho reasoning logic (theo reward think).  
6. Đánh giá sau mỗi giai đoạn: đo accuracy/F1 baseline, CoT, CoT+RL.  
7. Thử nghiệm so sánh: baseline vs CoT vs CoT+RL.  
8. Đánh giá trade-off: kiểm tra độ trễ inference với prompt dài hơn; phân tích trường hợp RL thất bại.  

### 4.6 Giả thuyết  
- **H1:** CoT-SFT làm tăng đáng kể *accuracy*/F1 so với baseline bằng cách học logic.  
- **H2:** RLAlignment giảm hallucination (được đo bằng tỷ lệ ví dụ LLM đưa thông tin sai).  
- **H3:** CoT và RL không làm tăng sai sót cơ bản (precision) quá mức.  
- **H4:** Ưu điểm về độ chính xác và minh giải vượt trội so với chi phí thêm thời gian (trong giới hạn chấp nhận).  

### 4.7 Đóng góp mong đợi  
- **Khoa học:** Bằng chứng bước đầu rằng CoT+RL cải thiện detection trong ngữ cảnh log, xác định điều kiện (log phức tạp, tỷ lệ label false).  
- **Phương pháp:** Mở rộng kỹ thuật huấn luyện LLM với CoT cho log; công bố tập dữ liệu đã hiệu chỉnh và CoT-driven.  
- **Kỹ thuật:** Mô hình CoT+RL đã tinh chỉnh và quy trình RLAlignment (reward) cho log.  
- **Công nghiệp:** Hệ thống có khả năng giải thích chi tiết nguyên nhân dị thường, phù hợp nhu cầu audit/truy vết.  

## Đề xuất 3 – Phương pháp luận

**Baseline:** LLM (GPT-4, LLaMA fine-tuned) với prompt.  
**Cải tiến:**  
- **CoT-SFT:** Huấn luyện LLM theo tập data mỗi log kèm phân tích từng bước (sử dụng GPT-4o tạo dataset CoT, sau đó fine-tune with LoRA).  
- **RLAlignment:** Áp dụng policy optimization (ví dụ GRPO) với reward đa mặt: (1) Format đúng, (2) Kết quả đúng (anomaly detection), (3) Suy luận có lý (penalize output rời rạc).  
- **Hướng giải quyết:** LLM input gồm log, LLM output gồm `<think>... <answer>`; huấn luyện iteratively.  

**Mô hình cải tiến:** LLM đầu ra chứa phân tích (“tư duy”) + kết luận, cho phép người dùng/quản trị viên đánh giá logic.

# 5. Phân tích Tính khả thi

Đánh giá các đề xuất (1–3) theo thang điểm 1–10 (10: tốt nhất):

| Proposal   | Reproducibility Baseline | Complexity Cải tiến | Tính toán (Compute) | Dữ liệu | Độ phức thí nghiệm | Rủi ro | Tính phù hợp luận văn | Điểm tổng (ước tính) |
|------------|:------------------------:|:-------------------:|:-------------------:|:------:|:------------------:|:------:|:---------------------:|:--------------------:|
| **C1 (RAG)** | 8 (dùng mô hình có sẵn, dataset chung) | 5 (thêm DB vector & query) | 6 (embedding+LLM nhưng không quá lớn) | 7 (log hiện hữu nhiều) | 5 (vài thử nghiệm so sánh) | 4 (rủi ro chấp nhận) | 8 (vừa tầm) | 43 |
| **C2 (Memory)** | 7 (tương tự C1, thêm memory module) | 7 (thiết kế memory, chính sách phức tạp) | 7 (LLM + memory processing) | 6 (cần logs dài hạn) | 6 (kịch bản đa tập) | 5 (rủi ro ~ vừa) | 7 (nặng hơn C1) | 45 |
| **C3 (CoT+RL)** | 6 (huấn luyện đặc biệt, dataset CoT) | 8 (CoT dataset + RL reward) | 8 (RL training chi phí cao) | 5 (cần tập gán nhãn rất chất lượng) | 7 (nhiều vòng lặp training) | 6 (RL khó ổn định) | 6 (tương đối phức tạp) | 46 |

- **Độ reproducible:** Cả 3 đều dùng baseline đã công bố; C3 đòi hỏi data CoT đặc biệt.  
- **Độ phức tạp cải tiến:** C3 phức tạp nhất (yêu cầu RL); C1 đơn giản nhất.  
- **Tính toán:** C3 cần nhiều (RL), C2 (LLM+index), C1 thấp nhất.  
- **Dữ liệu:** C2 cần logs dài hạn, C3 cần dữ liệu có giải thích; C1 đơn giản nhất.  
- **Complexity & Rủi ro:** C1 có rủi ro thấp (chỉ extension đơn giản), C3 rủi ro cao hơn do RL.  
- **Thích hợp luận văn:** C1 & C2 phù hợp thời gian 6-9 tháng, C3 có thể kéo dài do RL.  

Nhìn chung, cả 3 đều khả thi, trong đó C1 đơn giản và nhanh triển khai nhất; C2 và C3 cần nhiều nỗ lực hơn nhưng tiềm năng đóng góp lớn. Điểm tổng tương đối cao cho cả 3 (so sánh: C3=46, C2=45, C1=43). 

# 6. Kế hoạch Đánh giá Thí nghiệm

**Metrics Phát hiện:** Precision, Recall, F1 score trên tập test. Dùng thêm PR-AUC nếu dữ liệu nhãn phân bố chuẩn.  
**Metrics Phát hiện sớm:** Thời gian cảnh báo (Time-to-Detection) tính từ log đầu tiên tới log thật có lỗi. Tỷ lệ cảnh báo trước (tỉ lệ cảnh báo thành công trước lỗi). Nếu dữ liệu không có ngưỡng lỗi cụ thể, dùng **Early Warning Rate** (phát hiện anom trước một chu kỳ) hoặc **Detection Lead Time** trung bình. Đặc biệt, đo trade-off giữa độ chính xác và lead time (tức có thể báo sớm được đến đâu).  
**Metrics Hiệu năng:** Độ trễ inference (ms/log), tài nguyên (GPU). Đối với RAG: Recall retriever; đối với RL: số bước hội tụ.  
**Generalization:** (nếu có điều kiện) Kiểm tra cross-dataset (nếu cùng loại logs từ system khác). Chuẩn hoá input để thử nghiệm.  

Mỗi proposal cần so sánh ít nhất:
- **Chủ yếu:** Baseline gốc vs. Hệ thống cải tiến (C1, C2, hoặc C3).  
- **Nếu có điều kiện:** So sánh với một phương pháp liên quan (vd baseline khác) như RAGLog (dành cho C2), EagerLog (cho C1), LogGPT (cho C3).  
- Đảm bảo đánh giá trên cùng bộ dữ liệu, nhiều chạy để tránh nhiễu (seed/biến động LLM).

# 7. Phân tích Ablation & Kiểm định thống kê

- **Thiết lập ablation:**  
  - C1: (a) Baseline LLM, (b) LLM+RAG (proposal), (c) LLM+retrievalのみ.  
  - C2: (a) Baseline RAG, (b) RAG+Memory Proposal, (c) RAG + chỉ short-term memory, (d) RAG + chỉ long-term.  
  - C3: (a) Baseline LLM, (b) LLM+CoT, (c) LLM+CoT+RL.  
- **Thực hiện:** Chạy nhiều lần (với random seed LLM) để tính khoảng tin cậy, kiểm định ý nghĩa (t-test, Wilcoxon) giữa các cấu hình.  
- **Lưu ý:** Không chỉ báo cáo kết quả tốt nhất; báo cáo trung bình ± CI.  

# 8. Đánh giá Mô hình Nền tảng (Foundation Model)

- Đối với C1/C2 (retrieval): Đánh giá độ chính xác truy xuất (precision@k) của thành phần RAG bằng cách đo log thu về có liên quan hay không (ví dụ bằng cosine similarity threshold). 
- Đối với C3 (LLM): Đánh giá mức độ **hallucination** của LLM (tỉ lệ thông tin sai trong output CoT); độ nhất quán logic (có thể dùng metric Kintsch  hoặc BLEU giữa giải thích và ground-truth logic nếu có).  
- Đánh giá khả năng tổng hợp thông tin: % câu trả lời có format <think>-<answer> đúng chuẩn.  
- Đảm bảo metric liên quan không đẩy lệch mục tiêu chính (phát hiện).

# 9. Nguy cơ và Đe dọa Tính hợp lệ

- **Internal validity:** Hiệu suất phụ thuộc vào triển khai LLM (model, phiên bản API). Tuning hyperparameters (batch size, LR) có thể bias kết quả. Cẩn thận tránh leak dữ liệu giữa training và test.  
- **External validity:** Kết quả trên một bộ benchmark (VD BGL, Spirit, hoặc benchmark tổng hợp) có thể không tổng quát cho mọi log. Số lượng và tính đa dạng logs giới hạn.  
- **Construct validity:** Đảm bảo metric đánh giá thực sự đo *early detection*. Nếu chỉ dùng F1, có thể bỏ sót khía cạnh sớm; do đó cần các metric sớm riêng (lead time). Nhãn anomaly có thể không phân biệt rõ “thời điểm anomalous nhất”.  
- **Model risks (LLM):** LLM có thể thay đổi khi update; huấn luyện RL dễ bị bất ổn. Cần nhiều phiên lặp và giám sát output.  

# 10. Xếp hạng Cuối cùng

| Đề xuất      | Evidence mạnh | Baseline chất lượng | Cải tiến hợp lý | Tính khả thi luận văn | Đóng góp KH | Tiềm năng xuất bản | Ảnh hưởng CN | Rủi ro | Đánh giá tổng |  
|--------------|:------------:|:-------------------:|:-------------:|:-------------------:|:---------:|:---------------:|:----------:|:-----:|:-------------:|  
| **C1 (RAG)**  | 7            | 7                   | 8             | 9                   | 7         | 7               | 7          | 4     | **54**         |  
| **C2 (Memory)** | 8          | 8                   | 7             | 7                   | 8         | 8               | 8          | 5     | **51**         |  
| **C3 (CoT+RL)** | 8          | 6                   | 8             | 6                   | 9         | 9               | 6          | 6     | **48**         |  

- **Evidence:** C2 (DM-RAG) và C3 (RationAnomaly) có tài liệu 2025 mạnh. C1 dựa trên bằng chứng RAGLog 2023, ít mới hơn.  
- **Baseline:** C2 & C3 đều kế thừa mô hình mới nhất (DM-RAG & RationAnomaly). C1 baseline chỉ LLM cơ bản.  
- **Cải tiến:** C1 và C3 đều hợp lý; C2 cần thử chính sách memory mới (rủi ro thực nghiệm cao hơn).  
- **Feasibility:** C1 dễ nhất (đã xếp 9), C3 khó nhất (6), C2 trung bình.  
- **Đóng góp:** C3 về minh giải rất lớn, C2 về recall, C1 về cải thiện timeliness.  
- **Xuất bản/ công nghiệp:** C3 và C2 cao (đã có model, nhiều workshop), C1 tương đối.  
- **Rủi ro:** C3 RL cao, C1 thấp.

**Xếp hạng tổng:** C1 > C2 > C3 dựa trên cân bằng giữa tính thực tế và đóng góp. C1 ít phức tạp, dễ hoàn thành trong 6–9 tháng. C3 tuy hấp dẫn nhưng phức tạp thời gian hơn. 

# 11. Khuyến nghị Cuối cùng

Chúng tôi chọn **Đề xuất C1 (LLM + RAG)** là hướng luận văn cuối cùng:

- **Baseline:** Phương pháp LLM (như LogPrompt/EagerLog) không có ngữ cảnh lịch sử.  
- **Giới hạn:** Mô hình này có giới hạn window ngắn, dễ bỏ sót dị thường lặp lại qua thời gian.  
- **Cải tiến:** Thêm thành phần *Retrieval-Augmented Generation* (RAG) để truy vấn log lịch sử liên quan và cung cấp ngữ cảnh bổ sung cho LLM.  
- **Tại sao cải tiến này:** Vì RAG đã chứng minh tăng hiệu suất anomaly detection nhờ thông tin lịch sử; hướng này trực tiếp giải quyết giới hạn bối cảnh của baseline.  
- **Cách kiểm chứng:** Thực nghiệm so sánh nghiêm ngặt giữa baseline và hệ thống LLM+RAG, đánh giá metric phát hiện truyền thống (F1, recall) và metric sớm (lead time). So sánh hiệu năng trên benchmark thực tế.  
- **Tính khả thi 6–9 tháng:** Phạm vi hạn chế (chỉ thêm RAG vào pipeline sẵn); nhiều công cụ sẵn có (vector DB, LLM) hỗ trợ; có thể tái sử dụng code baseline.  
- **Đóng góp:** Mức *Targeted Improvement*: cung cấp bằng chứng cho lợi ích của RAG trong phát hiện dị thường log, mở rộng mã nguồn.  
- **Rủi ro:** Cần đảm bảo có log lịch sử đầy đủ; đánh giá xem retrieval có thực hữu ích hay không; chi phí truy vấn phải được tối ưu.  

# 12. Đề cương Luận văn Cuối cùng

**Thesis Definition:** *Improve a 2025 LLM-based method for Early Log Anomaly Detection by addressing limited historical context via Retrieval-Augmented Generation.*  

- **Tiêu đề tiếng Anh:** *“Enhancing LLM-based Log Anomaly Detection for Early Warning by Retrieval-Augmented Historical Context.”*  
- **Tiêu đề tiếng Việt:** *“Cải thiện Phát hiện Dị thường Log bằng LLM cho Cảnh báo Sớm thông qua Bối cảnh Lịch sử qua RAG.”*  

**Tóm tắt:** Bài luận văn này kế thừa phương pháp phát hiện dị thường log dựa trên mô hình ngôn ngữ lớn năm 2025, vốn chỉ xử lý luồng log hiện tại và thiếu thông tin lịch sử quan trọng. Chúng tôi xác định giới hạn về *ngữ cảnh* của baseline, gây giảm độ nhạy với các mẫu bất thường tái lặp. Để khắc phục, đề xuất tích hợp *Retrieval-Augmented Generation (RAG)*: xây dựng cơ sở dữ liệu embedding cho các bản ghi log lịch sử và thiết kế luồng tra cứu khi LLM xử lý log mới. Hệ thống **LLM+RAG** sau đó được đánh giá trên benchmark log truyền thống, so sánh với baseline về độ chính xác phát hiện và thời gian cảnh báo sớm. Kết quả mong đợi là chứng minh được RAG giúp cải thiện chỉ số phát hiện (F1, recall) và giảm thời gian phát hiện lỗi so với baseline, đồng thời phân tích chi phí/độ trễ tăng thêm. Đóng góp của luận văn bao gồm bằng chứng thực nghiệm cho việc sử dụng bối cảnh lịch sử trong anomaly detection, một bản mở rộng phương pháp baseline có thể tái tạo được, và các khuyến nghị kỹ thuật cho triển khai trong AIOps.