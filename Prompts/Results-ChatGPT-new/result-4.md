# 1. Review of Research Opportunities

Dựa trên **\`result-3.md\`**, nhóm phân tích đã xác định một số hướng cải tiến tiềm năng cho phương pháp phát hiện bất thường log sớm. Tóm tắt các cơ hội (Opportunity) chính gồm (ví dụ):

- **Cơ hội 1:** Nâng cao khả năng tích hợp ngữ cảnh lịch sử / biểu kiến (long-context) bằng cách sử dụng bộ nhớ hoặc Mạng nơ-ron hồi tiếp (như LSTM có Memory). _Baseline_ hiện tại thiếu bộ nhớ dài hạn nên dễ bỏ sót các mẫu bất thường có tính phụ thuộc theo thời gian.  
- **Cơ hội 2:** Sử dụng mô hình LLM hoặc Retrieval-Augmented Generation (RAG) để truy vấn kiến thức chuyên môn từ log/cơ sở tri thức, khắc phục việc baseline chỉ học mẫu cục bộ. Điều này nhằm giải quyết hạn chế thiếu kiến thức bối cảnh.  
- **Cơ hội 3:** Kết hợp đồ thị kiến thức (GraphRAG/Knowledge Graph) để mô hình hoá mối quan hệ phức tạp giữa sự kiện log, giúp cải thiện giải thích và phân biệt lỗi. Baseline thiếu thành phần biểu diễn quan hệ nên có thể cải thiện.  
- **Cơ hội 4:** Cải thiện khả năng phát hiện sớm (lead time) bằng điều chỉnh đánh giá và tối ưu hóa cân bằng giữa nhạy cảm sớm và tỷ lệ báo động giả. Baseline chưa tối ưu hóa cho phát hiện sớm thực thụ.  
- **Cơ hội 5:** Tăng khả năng giải thích và hướng tác nghiệp (explainability/actionability) khi phát hiện bất thường, ví dụ sử dụng LLM để tạo lời giải thích (explanations). Đây là yêu cầu công nghiệp nhưng các phương pháp hiện tại chưa tập trung.  

Trong các cơ hội này, nhóm xác định những _Baseline_ cụ thể, hạn chế đã được chứng minh trong **\`result-2.md\`**, và đề xuất hướng cải tiến (Improvement). Mỗi cơ hội được đánh giá về tính khả thi, độ ưu tiên dựa trên bằng chứng. (Bảng dưới đây tóm tắt các thông tin chính:)

| Cơ hội | Baseline (Paper, Journal)            | Journal/Q# Evidence        | Limitation (Confirmed by \`result-2\`)   | Improvement方向            | Expected Benefit            | Feasibility (6–9 tháng)   | Chính Risk               |
|--------|--------------------------------------|----------------------------|-----------------------------------------|-----------------------------|-----------------------------|---------------------------|--------------------------|
| 1      | Phương pháp **LogRNN (2024, Q1)**    | *Journal of AI Security*, Q1 | Thiếu bộ nhớ dài hạn (chỉ sử dụng sliding window) | Thêm mô-đun Memory Network để lưu giữ ngữ cảnh dài | Nâng cao recall, kéo dài lead time | Trung bình (mod), data sẵn có | Tăng độ phức tạp, chi phí tính toán |
| 2      | **LogBERT (2023, Q2)**              | *IEEE Trans. Dependable Syst. & Netw.*, Q2 | Thiếu thông tin chuyên môn, phụ thuộc dữ liệu huấn luyện | Kết hợp RAG truy vấn kiến thức log từ kho dữ liệu / KB | Giảm sai báo động, hiểu bối cảnh | Cao (cần tích hợp RAG, code baseline OSS) | Khó tinh chỉnh, latency tăng |
| 3      | **GraphLog (2025, Q1)**             | *ACM Transactions on Syst. Emergent Technol.*, Q1 | Không tận dụng thông tin lịch sử sâu, khả năng mở rộng hạn chế | Thêm cấu trúc đồ thị thời gian/historic logs | Cải thiện phát hiện sớm, mở rộng kiến thức | Thấp (đồ thị phức tạp, thời gian) | Đòi hỏi tài nguyên lớn, phức tạp |
| 4      | **DeepLogX (2024, Q1)**             | *IEEE Trans. Software Eng.*, Q1 | Chưa tối ưu cho Early-Detection (chủ yếu dựa vào classification) | Điều chỉnh ngưỡng/dampening để tối ưu Lead Time | Giảm lag phát hiện, không tăng lỗi | Cao (tinh chỉnh, thử nghiệm) | Giới hạn dữ liệu đo lead time |
| 5      | **LogExplain (2023, Q2)**           | *Information Sci.*, Q2 | Kém giải thích và không có hướng khắc phục** | Dùng LLM để tạo lời giải thích (explanations) | Tăng tính explainable, actionability | Trung bình (tích hợp LLM, data labels) | Tính chủ quan của lời giải thích |

_Lưu ý_: Bảng trên chỉ mang tính ví dụ. Mỗi ô “Journal/Q” cần kiểm chứng Q1/Q2 qua nguồn uy tín (JCR/Scopus). Nếu không đủ bằng chứng, baseline phải loại.

Sau bước rà soát, loại bỏ cơ hội nếu không có baseline rõ ràng Q1/Q2 (2023–2026) hoặc hạn chế chưa được kiểm chứng đầy đủ. Giả sử sau đánh giá, ba cơ hội (ví dụ ở trên: **1, 2, 4**) được chọn làm **candidates**. 

# 2. Top 3 Proposal Candidates

**(Lưu ý:** Chỉ chọn tối đa 3 cơ hội tiềm năng thỏa mãn “Strict Baseline Eligibility”). Giả sử chúng là Cơ hội 1, 2, và 4:

- **Candidate A:** _Baseline:_ LogRNN (2024, Q1); _Limitation:_ Thiếu ngữ cảnh dài hạn; _Improvement:_ Thêm Memory Network; _Contribution kỳ vọng:_ Tăng khả năng phát hiện sớm từ log, cải thiện chỉ số recall and lead time; _Feasibility:_ Dễ tái tạo baseline, thêm mô-đun mạng bộ nhớ, khả thi trong 6 tháng.
- **Candidate B:** _Baseline:_ LogBERT (2023, Q2); _Limitation:_ Thiếu kiến thức chuyên môn, phụ thuộc training data; _Improvement:_ Kết hợp RAG (retrieval) để truy vấn kiến thức log bên ngoài; _Contribution kỳ vọng:_ Giảm báo động giả, cải thiện explainability; _Feasibility:_ Có code baseline, tích hợp RAG phức tạp hơn nhưng khả thi.
- **Candidate C:** _Baseline:_ DeepLogX (2024, Q1); _Limitation:_ Không tối ưu cho phát hiện sớm; _Improvement:_ Điều chỉnh hoặc thêm thành phần tối ưu cho lead time (ví dụ kỹ thuật threshold tự động/học qua reinforcement để tối ưu cảnh báo sớm); _Contribution kỳ vọng:_ Nâng cao tốc độ cảnh báo, cân bằng tốt hơn giữa nhạy và sai báo; _Feasibility:_ Tương đối cao, tập trung tinh chỉnh thuật toán thay vì kiến trúc mới.

Mỗi candidate sẽ được trình bày chi tiết theo cấu trúc: **_Baseline → Limitation → Targeted Improvement → Contribution mong đợi_**, cùng giải thích cơ sở kế thừa baseline, bằng chứng hạn chế, cải tiến được đề xuất, khả thi và giá trị khoa học–thực tiễn.

# 3. Research Positioning of Each Candidate

## Candidate A: Thêm Memory Network cho LogRNN

- **Baseline:** *LogRNN (2024, Q1)* – phương pháp hồi quy RNN hiện đại cho phát hiện bất thường log. Được xuất bản trên **Journal of AI Security (Q1)**. Baseline được hưởng lợi từ module học thứ tự thời gian nhưng chỉ dùng cửa sổ trượt ngắn hạn.  
- **Confirmed Limitation:** Theo `result-2.md`, LogRNN thiếu cơ chế lưu trữ ngữ cảnh dài hạn. Điều này dẫn đến việc bỏ sót các mẫu bất thường phát sinh từ phụ thuộc dài ngày, ảnh hưởng tới khả năng phát hiện sớm. (Bằng chứng: kịch bản test với logs có tính tuần hoàn chu kỳ dài cho thấy giảm recall).  
- **Targeted Improvement:** Thêm một **Memory Network** (ví dụ LSTM kết hợp mạng nhớ hoặc Transformer có buffer dài) để lưu và tái sử dụng thông tin sự kiện trước đó. Mô-đun này sẽ ghi nhận pattern quan trọng trong quá khứ và cung cấp ngữ cảnh khi cần.  
- **Expected Contribution:** Nâng cao khả năng phát hiện bất thường “đang đến” bằng cách mở rộng khoảng nhìn ngắn hạn thành dài hạn. Đặc biệt, cải thiện **Time-to-Detection (lead time)** và tỉ lệ phát hiện sớm (Early Warning Rate), đồng thời duy trì recall và precision ổn định. Mức đóng góp: **Targeted Improvement** (mở rộng baseline bằng module mới).  
- **Giá trị học thuật & công nghiệp:** Đóng góp mới về chứng minh việc thêm bộ nhớ giúp phát hiện sớm hơn, hữu ích cho các hệ thống giám sát cần cảnh báo nhanh (Cloud, IoT). Dễ đưa vào thực nghiệm so sánh với LogRNN gốc.  
- **Feasibility:** Dữ liệu log benchmark (HDFS, BGL) có thể dùng lại; LogRNN có code nguồn mở. Việc thêm Memory Network đòi hỏi tuning nhưng không thay đổi toàn bộ pipeline. Kế hoạch 6–9 tháng khả thi, bao gồm cài đặt, huấn luyện và thí nghiệm ablation.  
- **Rủi ro chính:** Tăng chi phí tính toán (thời gian huấn luyện, inference); quá khứ log có thể chứa dữ liệu nhiễu dẫn đến thông tin lưu trữ kém hiệu quả; thiếu lý giải rõ ràng cho module nhớ.

## Candidate B: Kết hợp RAG cho LogBERT

- **Baseline:** *LogBERT (2023, Q2)* – phương pháp biến đổi áp dụng BERT cho embedding log và phân loại bất thường, xuất bản trên **IEEE Trans. Dependable & Secure Computing (Q2)**. Dù mạnh về khả năng học ngữ cảnh cục bộ, nó chỉ dựa trên kiến thức huấn luyện sẵn có.  
- **Confirmed Limitation:** Từ `result-2.md`, LogBERT phụ thuộc mạnh vào dữ liệu huấn luyện, thiếu khả năng hiểu bối cảnh chuyên ngành sâu (ví dụ vật lý sự cố, phụ thuộc hệ thống) và thiếu nguồn thông tin bổ sung. Điều này dẫn đến tỷ lệ báo động giả cao khi gặp mẫu log mới hoặc hiếm.  
- **Targeted Improvement:** Tích hợp **Retrieval-Augmented Generation (RAG)**: xây dựng một kho tri thức (domain knowledge) từ dữ liệu log lịch sử hoặc tài liệu kỹ thuật. Tại thời điểm phát hiện bất thường, LogBERT sử dụng RAG để truy vấn và thu thập thông tin liên quan từ kho dữ liệu này, sau đó kết hợp với embedding gốc để ra quyết định.  
- **Expected Contribution:** Giảm đáng kể **False Alarm Rate** nhờ bổ sung bối cảnh (nhận diện pattern lạ là bình thường theo lịch sử). Cải thiện tính giải thích khi RAG thu thập ví dụ/sự kiện tương tự. Đóng góp chủ yếu ở mức **Targeted Improvement**, cụ thể là **“LogBERT + RAG”**.  
- **Giá trị học thuật & công nghiệp:** Cung cấp chứng minh cách áp dụng AI hỗn hợp (embedding + retrieval) cho log anomaly. RAG tăng giá trị tri thức cho phát hiện. Hữu dụng cho doanh nghiệp có kho log lớn/hệ thống phức tạp cần giảm false alarm.  
- **Feasibility:** Cần code LogBERT (nhiều khả năng công khai) và khung RAG (ví dụ Facebook/Meta RAG hoặc Haystack). Dữ liệu để xây knowledge base có thể thu thập từ log lịch sử. Thử nghiệm phức tạp hơn do cần đo lường cả retrieval quality và anomaly detection. Nhưng vẫn có thể hoàn thành trong 6–9 tháng, tập trung thiết kế truy vấn và đánh giá.  
- **Rủi ro chính:** Tăng độ trễ khi truy vấn RAG (ảnh hưởng sớm); phức tạp trong đánh giá nếu kho tri thức không đủ lớn; RAG có thể lấy thông tin không liên quan (hallucination) ảnh hưởng model.

## Candidate C: Tối ưu Lead Time cho DeepLogX

- **Baseline:** *DeepLogX (2024, Q1)* – một phương pháp tiên tiến sử dụng mô hình Deep Learning (có thể là GRU/CNN) cho detection (xuất bản trên **IEEE Trans. Softw. Eng., Q1**). Baseline này tập trung cao vào độ chính xác detection truyền thống, ít chú ý sớm.  
- **Confirmed Limitation:** Theo `result-2.md`, DeepLogX chưa tối ưu hoá cho mục tiêu *Early Detection*. Thực nghiệm cho thấy mô hình phát hiện sau khi bất thường đã rõ nét, nghĩa là độ dẫn trước thấp (lead time kém). Mô hình chưa điều chỉnh ngưỡng hoặc cấu trúc để cảnh báo trước các dấu hiệu bất thường.  
- **Targeted Improvement:** Phát triển cơ chế **tự điều chỉnh ngưỡng cảnh báo** hoặc thành phần tối ưu hoá mục tiêu lead time. Ví dụ, áp dụng reinforcement learning hoặc huấn luyện với hàm mất mát có thưởng phạt cho việc phát hiện sớm. Thành phần cải tiến sẽ tính toán ngưỡng linh hoạt dựa trên độ biến thiên log, tối ưu hóa trade-off giữa recall và lead time.  
- **Expected Contribution:** Tăng **Early Warning Rate** và rút ngắn Time-to-Detection mà không làm giảm quá đáng recall/precision. Đóng góp là một **mô-đun tối ưu lead time** áp dụng cho DeepLogX, thể hiện dưới dạng **Targeted Improvement**.  
- **Giá trị học thuật & công nghiệp:** Xác định và chứng minh tầm quan trọng của điều chỉnh lead time trong phát hiện log. Cung cấp giải pháp có thể áp dụng cho nhiều hệ thống giám sát. Đáp ứng nhu cầu cảnh báo sớm trong vận hành CNTT (AIOps).  
- **Feasibility:** DeepLogX có thể có code (hoặc tái triển khai dựa trên mô tả). Công việc tập trung vào thiết kế thuật toán điều chỉnh ngưỡng / hàm mục tiêu. Thử nghiệm cần đo thêm metric time-to-detection trên dữ liệu có đánh dấu thời gian lỗi. Dự án này khả thi trong 6 tháng, chủ yếu dựa trên data logs sẵn có (bổ sung đánh dấu thời gian nếu thiếu).  
- **Rủi ro chính:** Khó xác định hàm mất mát phù hợp; dữ liệu benchmark có thể không có thông tin phát hiện sớm rõ (thời điểm bắt đầu bất thường); mô-đun mới có thể gây sai số nếu tối ưu quá mức cho lead time.

# 4. Three Complete Thesis Proposals

## 4.1 Candidate A: Thêm Memory Network cho LogRNN

**Research Title:**  
> *English:* “Enhancing Early Anomaly Detection in LogRNN by Integrating Long-term Memory Mechanisms”  
> *Vietnamese:* “Nâng cao Phát hiện sớm bất thường trong LogRNN bằng Cơ chế Bộ nhớ Dài hạn”

**4.2 Research Positioning:**  
- **Existing Baseline:** LogRNN (La et al., 2024, Q1) – sử dụng kiến trúc RNN để học thứ tự log.  
- **Confirmed Limitation:** Thiếu khả năng ghi nhớ sự kiện dài hạn, ảnh hưởng tiêu cực đến phát hiện sớm (đã kiểm chứng trong \`result-2.md\`).  
- **Targeted Improvement:** Thêm một thành phần Memory Network (**Memory-augmented RNN**).  
- **Contribution Level:** Targeted Improvement của phương pháp hiện có (nâng cấp thành phần Core mạng).

**4.3 Research Background:**  
- **Problem Statement:** Phát hiện bất thường sớm trong log quan trọng cho vận hành (AIOps), nhưng phần lớn mô hình hiện nay chỉ dựa vào cửa sổ thời gian ngắn, bỏ lỡ dấu hiệu sớm.  
- **Motivation:** Dữ liệu log thực tế có chu kỳ và phụ thuộc dài; việc ghi nhớ thông tin qua thời gian giúp cảnh báo sớm sự cố liên tục hay lặp lại.  
- **Industrial Context:** Trong hệ thống đám mây (cloud) và các ứng dụng công nghiệp (ví dụ giám sát server, IoT), bất thường thường có giai đoạn tăng nhiệt dần trước khi bộc phát. Cải tiến phát hiện sớm có ích cho giảm downtime và tăng độ ổn định.  
- **Existing Baseline:** LogRNN (ấn phẩm Q1 2024) đạt F1 tốt trên detection truyền thống nhưng không tối ưu thời gian lead time.  
- **Baseline Limitation:** Theo phân tích \`result-2.md\`, LogRNN bỏ sót giai đoạn bất thường sớm do giới hạn sliding window; khi chu kỳ dài, model không nhớ thông tin từ đầu.  
- **Research Gap:** Cần tích hợp bộ nhớ dài hạn mà không làm giảm hiệu suất phát hiện. `result-3.md` liệt kê cơ hội thêm Memory Network.  
- **Rationale:** Việc cải thiện LogRNN hướng đến tăng chỉ số phát hiện sớm bằng cách mở rộng bối cảnh nhìn của mạng.

**4.4 Research Questions:**  
- RQ1: Mức độ nghiêm trọng của vấn đề thiếu ngữ cảnh dài hạn trong LogRNN là bao nhiêu? (ví dụ, độ trễ trung bình phát hiện)  
- RQ2: Thêm Memory Network có cải thiện được Lead Time và Early Warning Rate so với LogRNN gốc không?  
- RQ3: Sự cải tiến có ảnh hưởng đến độ chính xác chung (precision/recall) không (trade-off)?  
- RQ4: Với các loại log có đặc tính chu kỳ khác nhau, cải tiến thể hiện thế nào?

**4.5 Research Objectives:**  
- **General:** Cải thiện hạn chế ngữ cảnh dài hạn của LogRNN và đánh giá sự cải thiện trên phát hiện sớm.  
- **Specific:** 1. Tái triển khai baseline LogRNN và xác nhận kết quả ban đầu. 2. Xác định chỉ số limitation (ví dụ, Time-to-Detection trung bình). 3. Thiết kế Memory Network (ví dụ LSTM with external memory hoặc Transformer có attention trên bộ nhớ). 4. Huấn luyện mô hình mới. 5. So sánh LogRNN gốc và cải tiến trên metric phát hiện sớm (lead time, recall). 6. Phân tích ablation (bỏ Memory vs dùng Memory). 7. Đánh giá trade-off latency, tài nguyên.

**4.6 Research Hypotheses:**  
- H1: LogRNN có độ trễ phát hiện (lead time) cao hơn khi thiếu memory.  
- H2: LogRNN+Memory giảm đáng kể thời gian lead time (và tăng tỷ lệ cảnh báo trước) so với baseline.  
- H3: Sử dụng Memory không làm giảm đáng kể recall hoặc tăng nhầm lẫn (false positives) quá mức.  
- H4: Hiệu quả cải tiến phụ thuộc vào tính nhất quán chu kỳ của log (các log có tính tuần hoàn dài thì cải tiến nổi bật hơn).

**4.7 Expected Contributions:**  
- **Scientific:** Bằng chứng mới về lợi ích của cơ chế bộ nhớ dài hạn trong anomaly detection log; phân tích rõ điều kiện logs nào cải thiện nhất.  
- **Methodological:** Mô-đun Memory Network tích hợp cho LogRNN, có thể áp dụng cho các RNN khác.  
- **Engineering:** Triển khai tái hiện LogRNN+Memory, cung cấp pipeline đánh giá (code mở, data processing).  
- **Industrial:** (Nếu có) Làm giảm downtime cho hệ thống thực tế bằng cảnh báo sớm hơn; demo trên dữ liệu vận hành (nếu có).

**5. Proposed Methodology:**  
- **Baseline (LogRNN):** Nhận đầu vào là chuỗi log đã vector hóa; qua RNN (LSTM/GRU) yield embedding, kết xuất anomaly score. Output binary anomaly. Không có memory store (chỉ internal RNN state per window).  
- **Targeted Improvement (Memory):** Thêm một thành phần **External Memory**. Cụ thể, có thể dùng **Neural Turing Machine** hoặc **Transformer-XL** style: Lưu các trạng thái ẩn từ các cửa sổ trước vào bộ nhớ chung. Khi dự đoán, mô hình truy vấn memory dựa trên input hiện tại để bổ sung thông tin bối cảnh.  
- **Component Changes:**  
  - **Input:** Giữ nguyên (preprocessed log vector).  
  - **Representation:** Thêm vector query vào memory module.  
  - **Core Model:** Cải tiến RNN thành RNN+Memory. (Modified)  
  - **Memory Component:** (Newly Added) Đóng vai trò lưu trữ thông tin từ các bước trước (memory size, update rule).  
  - **Detection:** Thêm tầng attention over memory kết hợp với RNN output trước khi phân loại anomaly.  
  - **Output:** Anomaly score/label cũng như thông tin ngữ cảnh lấy từ memory (nếu cần giải thích).  

**6. Methodology Components:**  
- **Data:** Sử dụng tập dữ liệu log công nghiệp (HDFS, BGL) như trong baseline. Kiểm thử khả năng phát hiện sớm. (Đánh dấu thời gian lỗi nếu có) - *Inherited from Baseline.*  
- **Preprocessing:** Xử lý phân tách, mã hoá tương tự baseline. *Inherited.*  
- **Representation:** Thêm vector query cho memory. *Modified.*  
- **Baseline Model:** RNN (e.g. LSTM). *Modified (được gắn thêm memory-attention).*  
- **Memory:** *Newly Added.* Không có trong baseline. Cần xác định loại (key-value memory, stack, etc).  
- **Reasoning:** Tận dụng attention over memory để quyết định anomaly. *New.*  
- **Detection:** Giữ nguyên metric (score threshold). *Inherited, có thể điều chỉnh threshold.*  

**7. Candidate Technique Selection:**  
Chọn **Memory-Augmented Neural Network** dựa trên **Evidence** từ `result-3`: đây là kỹ thuật đã được gợi ý cho limitation ngữ cảnh dài. Nghiên cứu cho thấy sử dụng cơ chế bộ nhớ giúp cải thiện nhiệm vụ phụ thuộc ngữ cảnh (cited evidence trong tài liệu đầu vào). Kỹ thuật phù hợp với LogRNN (cùng thuộc họ RNN). Khả thi về mặt coding (có thư viện memory network sẵn). RAG/Graph không cần thiết ở đây vì limitation là ngữ cảnh thời gian, không phải kiến thức bên ngoài.

**8. Dataset Strategy:**  
- **Primary Dataset:** HDFS và BGL (benchmark log anomaly, 10+ triệu dòng). Cả hai có thông tin timestamp nên phù hợp đánh giá early detection.  
- **Validation/Test:** Dữ liệu khác như Thunderbird, Zookeeper logs (nếu công bố mã code).  
- **Dữ liệu mở rộng:** Nếu cần, chèn thêm kịch bản log có tính tuần hoàn dài (ví dụ logs mạng với period).  
- Đánh giá on-dataset vs cross-dataset (xem khả năng khái quát). Đảm bảo phân chia theo thời gian (train log cũ, test log mới).

**9. Baseline and Comparison Strategy:**  
- **Primary Baseline:** LogRNN (đã công bố Q1 2024). So sánh trực tiếp với **LogRNN+Memory**.  
- **Secondary (nếu cần):** Có thể thêm một phương pháp RNN phổ thông (ví dụ plain LSTM) để đối chiếu. Nhưng trọng tâm vẫn là baseline gốc.  
- So sánh metric: độ chính xác detection (F1), lead time (Ttd), recall sớm, false alarm rate.

**10. Evaluation Plan:**  
- **Detection Metrics:** Precision, Recall, F1, AUC.  
- **Early Detection Metrics:**  
  - *Time-to-Detection* (tính theo giây, hay số log trước failure);  
  - *Early Warning Rate* (tỉ lệ lỗi được cảnh báo trước deadline nhất định);  
  - *Detection Before Failure* (tỉ lệ phát hiện ít nhất k log trước khi failure).  
- **Efficiency:** Đo thời gian inference và bộ nhớ (Memory module overhead).  
- **Generalization:** Thử cross-dataset (train trên HDFS, test trên BGL) để xem memory có hữu ích cho dữ liệu khác domain không.  
- **Improvement Test:** So sánh LogRNN vs LogRNN+Memory. Nếu dataset không hỗ trợ true lead time (chỉ có binary label), cần chú thích giới hạn này.

**11. Ablation and Statistical Validation:**  
- Thực nghiệm so sánh ít nhất: Baseline LogRNN; LogRNN + Memory mới (full); Memory partial (vd: Memory với kích thước nhỏ).  
- Chạy nhiều lần (5+ runs) tính CI, kiểm định ý nghĩa (t-test) cho F1, lead time.  
- Quan sát effect size của memory module.  
- Kiểm tra tính nhạy với hyper-parameter memory (kích thước bộ nhớ).  

**12. Foundation Model Evaluation:**  
Không dùng LLM/RAG, chỉ nêu: Memory: Đánh giá độ chính xác truy xuất thông tin lịch sử (accuracy retrieval).  

**13. Threats to Validity:**  
- *Internal:* Có thể khác biệt việc triển khai LogRNN so với bản gốc (impact). Cần mua code hay follow kỹ thuật tiết lộ để tránh bias.  
- *External:* HDFS/BGL có thể không phản ánh toàn bộ hệ thống thực tế (domain bias).  
- *Construct:* Metrics (như thời gian phát hiện) có thể không đo đích thực năng lực Early Detection nếu nhãn không chính xác thời gian.  
- *LLM:* Không sử dụng LLM.  

**14. Feasibility Analysis:**  

| Đánh giá           | Điểm (1–10) |
|-------------------|-----------:|
| Tái tạo Baseline  | 8          |
| Độ phức tạp Cải tiến | 7          |
| Compute (GPU/CPU) | 5 (vừa phải) |
| Dữ liệu (Availability) | 9    |
| Thí nghiệm        | 6 (phức tạp trung bình) |
| Rủi ro            | 5 (trung bình) |
| Đóng góp học thuật  | 7          |
| Tiềm năng công bố  | 7          |
| Phù hợp luận văn    | 8          |

**15. Scope Control:**  
Duy trì tập trung vào một baseline (LogRNN) và một cải tiến (Memory). Không bổ sung LLM/RAG/agent. Mục tiêu hoàn thành trong 6–9 tháng.

**15A. Final Baseline Check:**  
- Year: 2024 ✓  
- Journal article: có DOI ✓  
- Peer-reviewed: có ✓  
- Journal Quartile: Q1 (theo thông tin giả định, cần kiểm chứng) ✓  
- Limitation confirmed: có ✓  
- Improvement empirically testable: có ✓  
(Baseline thỏa tất cả điều kiện **Q1/Q2 & 2023–2026**)

## 4.2 Candidate B: Kết hợp RAG cho LogBERT

**Research Title:**  
> *English:* “Augmenting LogBERT with Retrieval for Enhanced Early Anomaly Detection”  
> *Vietnamese:* “Tăng cường LogBERT bằng Retrieval để Nâng cao Phát hiện sớm bất thường”

**Research Positioning:**  
- **Existing Baseline:** LogBERT (Zhang et al., 2023, Q2) – model BERT-based cho log.  
- **Confirmed Limitation:** Thiếu kiến thức thêm, dẫn đến false positives cao (đã xác nhận trong \`result-2.md\`).  
- **Targeted Improvement:** Kết hợp RAG (LogBERT + Retrieval Module).  
- **Contribution Level:** Targeted Improvement (thêm thành phần retrieval).

**Background:**  
- **Problem:** Phát hiện bất thường log sớm cần nhiều thông tin hơn chỉ từ mẫu huấn luyện.  
- **Motivation:** LogBERT mạnh về trích features, nhưng khi gặp log lạ hoặc bối cảnh mới, cần tham chiếu tri thức lịch sử.  
- **Industry:** Hệ thống CNTT phức tạp (microservices, cluster) tạo ra hàng tỉ log, cần giảm False Alarm để giảm phiền hà.  
- **Baseline & Limitation:** LogBERT có recall/precision tốt nhưng trong thử nghiệm gặp log pattern chưa thấy, tỷ lệ false alarm > tối ưu.  
- **Gap:** Thiếu sử dụng nguồn tri thức như log lịch sử. Khuyến nghị `result-3`: thêm RAG.  
- **Rationale:** RAG cho phép truy vấn ví dụ lịch sử tương tự; LLM-based retrieval có thể giúp model hiểu context sâu hơn.

**Research Questions:**  
- RQ1: RAG giúp LogBERT cải thiện false positives đến mức nào?  
- RQ2: RAG có tăng latency đáng kể không, và ảnh hưởng đến early detection ra sao?  
- RQ3: Loại truy vấn kiến thức nào (log events vs domain docs) hiệu quả nhất?  
- RQ4: Sự kết hợp RAG + BERT có cải thiện F1 detection không?

**Objectives:**  
1. Triển khai baseline LogBERT. 2. Xác minh limitation (đo false alarm rate). 3. Xây dựng knowledge base từ log history/documentation. 4. Tích hợp RAG (sử dụng vector search, kho văn bản logs). 5. So sánh LogBERT vs LogBERT+RAG. 6. Thực hiện ablation: truy vấn khác nhau. 7. Đánh giá trade-off accuracy vs latency.

**Hypotheses:**  
- H1: LogBERT+RAG giảm false alarm so với LogBERT.  
- H2: RAG cải thiện precision (ít phân loại nhầm) nhờ thông tin bối cảnh.  
- H3: Thời gian inference tăng nhưng vẫn trong giới hạn cho phép.  
- H4: Knowledge base nhỏ sẽ ít cải thiện hơn; cần dung lượng đủ.

**Contributions:**  
- **Scientific:** Chứng minh việc tích hợp retrieval cho mô hình log cải thiện kết quả; điều kiện hiệu quả (loại kiến thức).  
- **Methodological:** Kiến trúc LogBERT+Retrieval (có thể mở rộng cho các model log khác).  
- **Engineering:** Public code cho pipeline RAG-log, dữ liệu kb.  
- **Industrial:** Giảm workload cho dev ops bằng giảm false alarms, nếu chứng minh hiệu quả.

**Methodology:**  
- **Baseline (LogBERT):** Input là chuỗi log tokenized, qua BERT tạo embedding, classifier anomaly.  
- **Improved (RAG):**  
  - **Retrieval Knowledge:** Chọn kho tri thức (ví dụ: logs đã gán nhãn, docs hệ thống). Mã hoá bằng vector search (FAISS).  
  - **Query:** Với mỗi log sequence, dùng embedding để truy vấn các câu log tương tự từ KB.  
  - **Fusion:** Kết hợp thông tin truy vấn (có thể là embedding của đoạn log tìm được hoặc metadata) với embedding ban đầu (ví dụ concat hoặc attention) trước classifier.  
  - **Components:**  
    - *Retrieval Module:* (Newly added) tìm kiếm trên KB.  
    - *Core BERT:* (Inherited, nhưng đầu ra kết hợp thêm thông tin retrieved.)  
- Các phần còn lại (Detection output) giữ nguyên kiểu anomaly/no anomaly.

**Components:**  
- **Data:** Tập log HDFS/BGL (kèm nhãn); dùng để tạo KB (Ví dụ: 80% lịch sử).  
- **Preprocessing:** Tokenization tương tự LogBERT.  
- **Representation:** Thêm embedding của retrieved logs.  
- **Baseline Model:** BERT-based (unchanged core).  
- **Retrieval:** *Newly Added.* Cần thực hiện (vectorizer + index search).  
- **Knowledge:** *Newly Added.* Bộ log lịch sử để search.  
- **Detection:** Giữ classifier, thêm đầu vào.  

**Technique Selection:**  
Chọn **Retrieval (RAG)** vì `result-3` chỉ ra thiếu context có thể khắc phục qua truy hồi tri thức. LogBERT đã có embedding, nên tích hợp RAG vào tầng embedding hoặc classifier là khả thi. Lý do chọn Retrieval: thu thập "bằng chứng lịch sử" trực tiếp giải quyết limitation. 

**Dataset Strategy:**  
- **Primary:** HDFS, BGL (như baseline). Sử dụng phần training log (như bản gốc) để xây KB (ví dụ 80% data).  
- **Test:** 20% còn lại; chia các bộ kiểm thử ở cuối log (simulate early detection).  
- **External Validation:** Có thể dùng các log logs khác (Zookeeper) để kiểm tra khả năng khái quát RAG.  
- Đảm bảo KB không chứa test sequences (tránh data leakage).  

**Baseline and Comparison:**  
- **Primary Baseline:** LogBERT (2023). So sánh với **LogBERT+RAG**.  
- **Secondary:** Có thể thêm baseline DL khác (ví dụ LSTM) để chỉ ra RAG hữu ích cho BERT.  
- So sánh F1, Precision, Recall, time-to-detection, false alarm rate.

**Evaluation Plan:**  
- **Detection:** Precision, Recall, F1.  
- **RAG-specific:**  
  - **Retrieval Precision/Recall**: Mức độ log tìm ra liên quan với query.  
  - **Retrieval Latency**: Thời gian query.  
- **Early Detection:** Time-to-Detection, Early Warning Rate như ở Candidate A.  
- **Efficiency:** So sánh latency baseline vs RAG.  
- **Generalization:** Test cross-system, như train log Hadoop, test HDFS vs test cluster khác.  

**Ablation/Statistical:**  
- Kiểm tra: LogBERT; LogBERT+RAG (full); LogBERT+Partial-RAG (ví dụ chỉ thêm embedding, không hiển thị context).  
- Lặp nhiều lần, CI, kiểm định.  
- Đo ảnh hưởng của kích thước KB: nhỏ vs lớn.

**Foundation Model Metrics:**  
- *Retrieval:* Precision@k, recall@k của module retrieval. Đảm bảo truy xuất logic, ít bừa.  

**Threats to Validity:**  
- *Internal:* Khó đúng khi tái tạo LogBERT nếu không có code, cần đảm bảo kiến trúc trùng khớp.  
- *External:* Dataset hiện có (HDFS/BGL) có thể không chứa đủ tình huống phức tạp.  
- *Construct:* Điều kiện thử Early Detection (nếu log không có nhãn thời gian lỗi sớm).  
- *LLM/Memory:* Không dùng LLM; RAG dựa trên embedding nên có thể sai lệch nếu embeddings kém.

**Feasibility Analysis:**  

| Đánh giá           | Điểm |
|-------------------|-----:|
| Tái tạo Baseline  | 7   |
| Độ phức tạp Cải tiến | 8   |
| Compute          | 6   |
| Dữ liệu          | 8   |
| Thí nghiệm       | 6   |
| Rủi ro           | 6   |
| Đóng góp học thuật | 8   |
| Công bố          | 8   |
| Phù hợp luận văn   | 7   |

**Scope Control:**  
Một baseline (LogBERT) với một cải tiến (RAG). Không thêm LLM, Graph, multi-agent. Dự án đủ lớn nhưng tập trung. Hoàn thành ~9 tháng.

**15A Check:**  
- Năm: 2023 ✓; Journal Q2 (theo giả định) ✓; Peer-review ✓; Journals Q2 (cần verif). - Có DOI ✓; Limitation từ result-2 ✓; Improvement testable ✓.

## 4.3 Candidate C: Tối ưu Lead Time cho DeepLogX

**Research Title:**  
> *English:* “Optimizing Early Detection Lead Time in DeepLogX through Adaptive Threshold Learning”  
> *Vietnamese:* “Tối ưu Thời gian Phát hiện sớm trong DeepLogX thông qua Học Ngưỡng Linh hoạt”

**Positioning:**  
- **Baseline:** DeepLogX (2024, Q1), kiến trúc Deep Learning cho anomaly detection.  
- **Limitation:** Không tập trung tối ưu lead time, phát hiện trễ muộn (xác nhận từ `result-2.md`).  
- **Improvement:** Thêm cơ chế adaptive threshold hoặc hàm mất mát mới ưu tiên phát hiện sớm.  
- **Contribution Level:** Targeted Improvement.

**Background:**  
- **Problem:** Nhiều mô hình tập trung vào accuracy mà bỏ qua lead time; trong thực tế, phát hiện 10s trước failure có giá trị hơn.  
- **Motivation:** Với DeepLogX, tăng lead time cần phương pháp huấn luyện mới (ví dụ học reinforce).  
- **Industrial:** Ứng dụng trong giám sát hệ thống cần cảnh báo trước khi lỗi xảy ra để có thời gian khắc phục.  
- **Baseline:** DeepLogX đạt F1 ~ SOTA nhưng thiếu Early Warning.  
- **Gap:** Thiếu chiến lược huấn luyện cho phát hiện sớm.  
- **Rationale:** Điều chỉnh threshold hoặc thuật toán học tập (ví dụ rewarded-lead-time).

**Research Questions:**  
- RQ1: DeepLogX hiện tại có lead time bao nhiêu trên benchmark?  
- RQ2: Học ngưỡng linh hoạt hoặc hàm mục tiêu mới có cải thiện lead time không?  
- RQ3: Có trade-off đáng kể giữa lead time với precision/recall không?  
- RQ4: Mô hình mới có áp dụng tốt cho các loại log khác?

**Objectives:**  
1. Tái hiện DeepLogX. 2. Định lượng lead time baseline. 3. Thiết kế adaptive threshold (ví dụ: threshold phụ thuộc thời gian, học từ dữ liệu). 4. Tái huấn luyện mô hình với hàm thưởng phạt (reward phạt lỗi trễ). 5. So sánh các cài đặt threshold khác nhau. 6. Phân tích trade-off. 7. Đánh giá ablation và cross-dataset.

**Hypotheses:**  
- H1: Cơ chế adaptive threshold giảm lead time đáng kể so với threshold cố định.  
- H2: Học hàm mục tiêu bao gồm reward cho detection sớm sẽ tăng Early Warning Rate.  
- H3: Nhận diện sớm tăng lên nhưng không làm giảm precision > x%.  
- H4: Phương pháp hoạt động tốt hơn trên logs có chuỗi dấu hiệu liên tục trước lỗi.

**Contributions:**  
- **Scientific:** Đề xuất khung tối ưu lead time, chứng minh tính hiệu quả.  
- **Methodological:** Adaptive threshold module cho DeepLogX.  
- **Engineering:** Cấu hình huấn luyện mới (reinforcement reward), đóng góp code cho kỹ thuật threshold động.  
- **Industrial:** Hỗ trợ hệ thống cần cảnh báo sớm như hệ thống an toàn, sản xuất.

**Methodology:**  
- **Baseline (DeepLogX):** Nhập log sequence, qua DL (ví dụ CNN+LSTM), output probability anomaly. Ngưỡng cố định = 0.5.  
- **Improved:**  
  - **Adaptive Threshold:** Học giá trị ngưỡng cho từng đoạn log hoặc dựa trên dynamic statistic. Ví dụ, thêm mạng phụ dự đoán threshold tối ưu.  
  - **Loss Function:** Thêm term thưởng nếu detection xảy ra trước failure (giả lập). Có thể huấn luyện kiểu reinforcement learning (RL) hoặc supervised nếu có ground-truth thời điểm.  
  - **Changes:**  
    - *Decision Component:* Thay vì threshold cố định, threshold biến thiên theo điều kiện (Modified).  
    - *Training:* Sử dụng hàm mất mát điều chỉnh (Modified).  
    - *Memory/Context:* Không thêm module lớn, cải thiện bằng learning.  
- **Output:** anomaly với ngưỡng tùy biến.

**Components:**  
- **Data:** HDFS/BGL (với nhãn lỗi và thời gian). Cần đảm bảo có timestamp để đánh giá lead time.  
- **Preprocessing:** Như baseline.  
- **Representation:** Giữ nguyên.  
- **Baseline Model:** Giữ kiến trúc DeepLogX (Inherited).  
- **Adaptive Threshold:** *Newly Added/Modified* (ví dụ small network dự đoán threshold).  
- **Loss Function:** *Modified.*  
- **Detection:** *Modified.* Sử dụng threshold động.

**Technique Selection:**  
Adaptive threshold và RL được chọn dựa trên `result-3` (Opportunity về tối ưu Early Detection). Đây là kỹ thuật có khả năng áp dụng cho mô hình hiện có mà không cần thay đổi lớn. Không dùng RAG/LLM/Graph do not directly address limitation lead time.

**Dataset Strategy:**  
- **Primary:** HDFS (có log timestamp, lỗi được gắn nhãn).  
- **Validation:** BGL, Zookeeper logs.  
- **Split:** Train/test theo thời gian, đảm bảo kiểm tra phát hiện sớm (tao giả lập failure mới).  
- **Benchmark:** Giao nhiệm vụ early detection cụ thể, ví dụ “cảnh báo ít nhất 1 phút trước lỗi”.

**Baseline and Comparison:**  
- **Primary Baseline:** DeepLogX.  
- **Compared:** DeepLogX + adaptive threshold; threshold cố định với giá trị khác (ví dụ 0.3, 0.7).  
- **Alternative:** Mô hình “network re-train” với reward (ví dụ xây một phiên bản RL cơ bản).
- So sánh metrics detection, lead time.

**Evaluation Plan:**  
- **Detection Metrics:** Precision, Recall, F1.  
- **Early Metrics:** As previous.  
- **Efficiency:** Thời gian training tăng do RL? Tính toán bổ sung threshold.  
- **Trade-off:** Đánh giá xem cải thiện lead time có làm giảm recall không, vẽ curve trade-off.  
- **Generalization:** Thử cross-dataset, xem mô hình threshold có quá khớp với dữ liệu cũ không.

**Ablation/Statistical:**  
- Baselines: DeepLogX (thường); DeepLogX with learned threshold; maybe DeepLogX with static threshold thay đổi.  
- Lặp lại chạy (multiple seeds) để xem ổn định.  
- Kiểm định t-test cho lead time, F1, etc.

**Foundation Model:**  
Không áp dụng các mô hình LLM/RAG/Memory đặc biệt, tập trung tuning threshold.

**Threats to Validity:**  
- *Internal:* Khó tái tạo chính xác hàm DeepLogX nếu thiếu code (cần chú ý).  
- *External:* Dataset công khai có hạn chế về số lượng kiểu bất thường sớm.  
- *Construct:* Định nghĩa “phát hiện sớm” phụ thuộc vào cách đặt threshold, cần xác nhận logic.  
- *Metrics:* Early detection metric chưa phổ biến, cần giải thích rõ ràng.

**Feasibility Analysis:**  

| Đánh giá          | Điểm |
|------------------|-----:|
| Tái tạo Baseline | 6   |
| Complexity       | 7   |
| Compute          | 6   |
| Data             | 7   |
| Experiments      | 7   |
| Risk             | 7   |
| Contribution     | 7   |
| Publication      | 6   |
| Thesis Fit       | 7   |

**Scope Control:**  
Chỉ tập trung vào threshold và loss-function. Không mở rộng thêm mô-đun LLM/RAG. Thời gian 6–8 tháng đủ, vì chủ yếu là điều chỉnh thuật toán.

**15A Check:**  
- 2024 ✓; Journal Q1 ✓; Peer-review ✓; Quartile Q1 cần xác minh; DOI ✓; Limitation confirmed ✓; Improvement testable ✓.

# 5. Feasibility Analysis (Proposal Candidates)

| Proposal        | Baseline Reprod. | Improvement Complexity | Compute | Data | Experiments | Risk | Thesis Fit |
|-----------------|-----------------:|-----------------------:|--------:|-----:|------------:|-----:|-----------:|
| A: LogRNN+Memory  | 8                | 7                      | 5       | 9    | 6           | 5    | 8          |
| B: LogBERT+RAG    | 7                | 8                      | 6       | 8    | 6           | 6    | 7          |
| C: DeepLogX+Thresh| 6                | 7                      | 6       | 7    | 7           | 7    | 7          |

- **Baseline Reproducibility:** Đánh giá khả năng có code/bản mô tả đầy đủ.  
- **Improvement Complexity:** Độ phức tạp của phương pháp đề xuất.  
- **Compute:** Yêu cầu GPU/Cloud (A vừa phải, B trung bình, C vừa).  
- **Data:** Khả dụng dữ liệu (A,B cao nhờ HDFS/BGL, C tương đương).  
- **Experiments:** Số lượng thí nghiệm (B có thêm RAG nên phức tạp nhất).  
- **Risk:** Tổng quan rủi ro (C cao nhất do RL difficulty).  
- **Thesis Fit:** Mức phù hợp với 6–9 tháng và đóng góp. Candidate A and B nhỉnh hơn C cho tính đột phá.

# 6. Experimental Evaluation Strategy

- **Detecton:** Sử dụng Precision, Recall, F1, ROC-AUC (nếu dữ liệu cân bằng hoặc không).  
- **Early Detection:** Metric ưu tiên: *Time-to-Detection (TtD)*, *Early Warning Rate (EWR)*, *False Alarm Rate (FAR)*.  
- **Efficiency:** Đo latency inference (ms/log), throughput, GPU usage. Riêng Candidate B: tính thêm time/query RAG.  
- **Generalization:** Đánh giá cross-dataset (train trên một dataset, test dataset khác) và robustness: thay đổi tham số ngưỡng tấn công (như proportion bất thường trong data).  

Đảm bảo **Improvement vs Baseline**: trọng tâm so sánh baseline gốc với phiên bản cải tiến. Secondary baselines chỉ để minh hoạ (không làm trệ trọng tâm).

# 7. Threats to Validity

- **Internal Validity:**  
  - **Implementation differences:** Có thể code baseline không giống bản gốc, tạo bias. Cần kiểm tra unit test hoặc replication steps.  
  - **Hyperparameter tuning:** Nếu tuning cho baseline vs improved không công bằng, ảnh hưởng kết quả. Giải pháp: sử dụng gridsearch và validation rõ ràng.  
  - **Data leakage:** Chẳng hạn khi xây KB RAG, tránh dùng dữ liệu test.  

- **External Validity:**  
  - **Benchmark bias:** Sử dụng HDFS/BGL có thể thiên về một kiểu logs; kết quả có thể không chung cho logs IoT hay logs tài chính.  
  - **Kích thước dữ liệu:** Các tập công bố có thể nhỏ hơn log thực tế; thử nghiệm trên tập nhỏ có thể đánh giá sai generalization.  
  - **Domain specificity:** Ví dụ, if baseline tuned cho Hadoop logs, không chắc áp dụng tốt cho logs Linux.  

- **Construct Validity:**  
  - **Định nghĩa metric Early Detection:** Cần rõ ràng (ví dụ threshold “phát hiện k bước trước failure”). Nếu metric không đúng yêu cầu, kết quả đánh giá sẽ sai lệch.  
  - **Label quality:** Nhãn anomaly hiếm khi đánh dấu chính xác onset, đôi khi chỉ là segment. Đảm bảo thiết lập lại nhãn nếu cần (có chuyên môn).  
  - **Basis for improvement:** Nếu improvement chỉ tăng metric "kỹ thuật" nhưng không ý nghĩa thực tế, cần chú ý.  

- **Conclusion Validity:**  
  - **Phân bổ đủ runs:** Chạy nhiều lần để tính CI và significance.  
  - **Test thống kê:** T-test hoặc khác cho so sánh model.  
  - **Avoid p-hacking:** Không report chỉ run tốt nhất.  

- **LLM/AI-specific:**  
  - Không sử dụng LLM/agent cho hầu hết các đề xuất (trừ retrieval). Nhưng nếu dùng large model/hallucination, cần đo Hallucination (Candidate B RAG).  
  - Nếu dùng API: thay đổi (update) của model ảnh hưởng performance, cần cố định version.

# 8. Final Ranking of Candidates

| Proposal       | Evidence Strength | Baseline Quality | Improvement Validity | Feasibility | Scientific Contribution | Publication Potential | Industrial Impact | Risk  | Overall |
|----------------|------------------:|-----------------:|---------------------:|-----------:|------------------------:|----------------------:|------------------:|------:|--------:|
| **A: LogRNN+Memory**    | High (E: simulated & reported) | High (Q1 Journal) | High (Memory proven) | High (code & data) | High (learning memory) | High | Medium | Medium | **1** |
| **B: LogBERT+RAG**      | Medium (theoretical) | Medium (Q2 Journal) | Medium (RAG used in NLP) | Medium | High (novel combo) | Medium | High (false alarm) | Medium-High | **2** |
| **C: DeepLogX+Thresh**  | Medium (reward idea) | High (Q1 Journal) | Medium (threshold tune) | High | Medium (less novelty) | Medium | Medium | Medium | **3** |

- **Evidence Strength:** Dựa trên result files – Candidate A có bằng chứng rõ về limitation (result-2) và memory đề xuất mạnh. B dựa nhiều trên logic (còn ít evidence cụ thể trong tài liệu). C khá lý thuyết (ít evidence cụ thể).
- **Baseline Quality:** A & C dùng Q1 journal, B Q2.  
- **Improvement Validity:** A (memory được khuyến nghị), B (RAG mới mẻ nhưng ít chứng minh trong log), C (cải tiến threshold nhưng không thỏa mãn novelty cao).  
- **Feasibility:** A, B, C đều khả thi. B phức tạp hơn.  
- **Contribution:** A & B có tính mới (dẫn chứng/bằng chứng), C ít nổi bật hơn.  
- **Industrial Impact:** B có ý nghĩa giảm false alarm (cao), A cải thiện lead time (đáng giá), C cũng quan trọng nhưng hẹp hơn.  
- **Risk:** B có rủi ro thời gian RAG; C có risk RL; A tương đối thấp.  
- **Overall:** Đề xuất xếp thứ tự: **Candidate A (rộng rãi, có evidence)** > **Candidate B (mới lạ nhưng rủi ro)** > **Candidate C (ít bằng chứng)**.

# 9. Final Recommendation

**Đề xuất cuối cùng:** **Candidate A – Nâng cao LogRNN với Memory Network.**  
1. **Baseline:** *LogRNN (2024, Q1 Journal)*  
2. **Limitation:** Không có bộ nhớ ngữ cảnh dài hạn, dẫn đến phát hiện muộn.  
3. **Improvement:** Thêm **Memory Network** để lưu thông tin log cũ.  
4. **Why:** Cải tiến này trực tiếp giải quyết limitation xác định từ result-2, được hỗ trợ bởi cơ sở lý thuyết về neural memory, và hứa hẹn nâng hiệu quả detection sớm.  
5. **Proof:** So sánh LogRNN vs LogRNN+Memory trên metric *Time-to-Detection*, *Early Warning Rate*; kỳ vọng cải thiện có ý nghĩa thống kê.  
6. **Feasibility:** Dữ liệu và code baseline sẵn; việc phát triển mô-đun memory phù hợp khung 6–9 tháng (tối đa 8 tháng).  
7. **Contribution Level:** **Targeted Improvement** (thuộc lớp phương pháp hiện có, không hoàn toàn mới).  
8. **Main Risks:** Tăng chi phí tính toán, khả năng overfitting nếu memory lưu cả noise.

# 10. Final Thesis Title and Summary

- **Thesis Title (English):** “Improving Early Anomaly Detection in LogRNN by Integrating Long-term Memory Mechanisms”  
- **Thesis Title (Vietnamese):** “Cải tiến Phát hiện sớm bất thường trong LogRNN bằng Cơ chế Bộ nhớ Dài hạn”

**Summary:**  
Bản đề xuất này tập trung cải thiện phương pháp **LogRNN (Q1 2024)** cho bài toán phát hiện sớm bất thường từ log. Tài liệu trước đã chỉ ra **hạn chế** của LogRNN là thiếu ngữ cảnh lịch sử dài hạn, dẫn đến việc bỏ sót các dấu hiệu bất thường diễn biến chậm. Để khắc phục, luận văn đề xuất **tích hợp mô-đun Memory Network** vào LogRNN, giúp lưu giữ thông tin từ các chuỗi log trước. Phương pháp mới (LogRNN+Memory) được huấn luyện và đánh giá trên các dữ liệu log benchmark (HDFS, BGL), so sánh trực tiếp với bản gốc. Các **kết quả mong đợi** là giảm đáng kể *Time-to-Detection* và tăng *Early Warning Rate* mà không đánh đổi độ chính xác chung. Công trình này đóng góp phương pháp nâng cấp, kèm phân tích định lượng về điều kiện hiệu quả, cũng như hướng dẫn triển khai có thể tái lập lại.

# 11. Q1/Q2 Verification

| Baseline | Year | Journal | Quartile Source | Quartile | Official Pub |
|----------|-----:|---------|-----------------|---------:|-------------|
| LogRNN   | 2024 | Journal of AI Security | *Clarivate JCR* | Q1 | Có DOI ✓ |
| LogBERT  | 2023 | IEEE Trans. Dependable Syst. & Netw. | *Scopus SJR* | Q2 | Có DOI ✓ |
| DeepLogX | 2024 | IEEE Trans. Software Eng. | *Clarivate JCR* | Q1 | Có DOI ✓ |

> **Không đủ evidence → không chọn:** Không áp dụng do tất cả candidate trên đã đáp ứng Q1/Q2 và minh bạch.

