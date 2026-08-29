# Consolidated and Prioritized Research Gaps

- **Thời gian thực và khả năng giải thích.** Khảo sát người dùng cho thấy phần lớn (84.5%) kỳ vọng hệ thống “phát hiện bất thường theo thời gian thực” và đòi hỏi công cụ có khả năng giải thích (interpretability) kèm lý do cho quyết định bất thường. Điều này phản ánh khoảng trống trong các phương pháp hiện tại vốn tập trung vào độ chính xác chung (F1, Precision, Recall) thay vì đánh giá thời gian phát hiện và khả năng giải thích.  
- **Đa dạng định dạng và tuỳ biến.** Hơn 78% người dùng cần công cụ có thể tuỳ biến để xử lý “các cấu trúc log khác nhau” đồng thời cung cấp giải thích. Nhiều kỹ thuật nghiên cứu chưa tối ưu cho việc log định dạng hỗn hợp (thiếu “cross-format”) hay đa ngôn ngữ. Ví dụ, các phương pháp hiện tại chủ yếu đào tạo trên tập Linux syslog (Cabello 2026) hoặc các bộ dữ liệu chuẩn như HDFS/BGL (LAnoBERT 2023), dẫn đến tính tổng quát kém khi chuyển đổi môi trường hoạt động hoặc ngôn ngữ log.  
- **Giới hạn ngữ cảnh dài hạn.** Các mô hình tuần tự như LSTM/Transformer vẫn gặp khó với các bất thường phân tán trên chuỗi thời gian dài (ví dụ tấn công APT nhiều giai đoạn). Cụ thể, giới hạn cửa sổ ngữ cảnh cố định (sliding window) làm mất thông tin lịch sử quan trọng. Đã có khuyến cáo rằng các chỉ số như “số log sai” dự báo chậm hơn khi cửa sổ mở rộng, đồng thời các phương pháp truyền thống (DeepLog, LogBERT) thường cần cập nhật lại khi mẫu log thay đổi.    
- **Các giới hạn của mô hình hiện đại.** Nhiều mô hình học sâu và LLM-based thiếu khả năng thích nghi với dữ liệu mới và gặp trục trặc khi tấn công tinh vi. Ví dụ, LogBERT (Cabello 2026) chỉ huấn luyện trên log bình thường nên cần thủ công điều chỉnh cửa sổ để đạt độ nhạy cao. Các phương pháp mới nhất (như LogRESP-Agent 2025) có độ chính xác cao nhưng chỉ tập trung phát hiện và giải thích, chưa hướng đến phản ứng tự động. Các mô hình cũ (CNN/LSTM) thiếu khả năng diễn giải và “không chủ động”, trong khi nhiều mô hình mới cũng mặc định giả thiết input đã được cấu trúc tốt.  

Các khoảng trống ưu tiên là khả năng giải thích và thời gian phát hiện sớm, xử lý các định dạng log hỗn hợp, và mở rộng ngữ cảnh dài hạn (ví dụ bằng cơ chế nhớ, RAG). Những gap này có sức ảnh hưởng cao bởi người dùng và có bằng chứng mạnh từ khảo sát và xu hướng tấn công hiện nay.

# Baseline-centric Root Cause Analysis

| **Baseline (Q1/Q2, 2023–26)** | **Component** | **Limitation** | **Root Cause** | **Evidence** | **Impact** |
|---|---|---|---|---|---|
| **LogRESP-Agent (Appl. Sci. 2025, Q2)** | Cơ chế thu thập/ngữ cảnh | Tập trung phát hiện & giải thích, chưa hỗ trợ tự động phản ứng hoặc định dạng log hỗn hợp | Mô hình dựa trên các công cụ tĩnh (RuleMatcher, SequenceScorer…) và vòng lặp reasoning cố định, giả định log đầu vào có cấu trúc tốt; chưa tích hợp kiến thức ngoài để thích ứng đa định dạng | Tác giả nêu rõ hạn chế không hỗ trợ phản ứng chủ động và xử lý đa định dạng | Không thể tự động hóa phòng thủ (cần can thiệp thủ công); hiệu quả giảm khi gặp log không chuẩn hóa hoặc ngoặc ngữ nghĩa khác |
| **LogBERT trong AIOps (Syst. Soft. Comput. 2026, Q2)** | Cấu hình cửa sổ/tần suất | Cần cân bằng giữa độ bao phủ ngữ cảnh và độ trễ dự đoán; cửa sổ ngắn hơn tăng phát hiện nhưng bỏ sót ngữ cảnh | Đào tạo tự giám sát trên bộ log chuẩn (Linux syslog) nên thiếu cơ chế ghi nhớ ngữ cảnh dài hạn; mục tiêu huấn luyện chỉ là mô phỏng ngôn ngữ log thông thường (BERT masked) mà không có feedback cho anomaly | Kết quả cho thấy “cửa sổ 15 giây với chồng chéo 10 giây” là trade-off tốt nhất; cửa sổ ngắn hơn cho F1 cao hơn nhưng ít ngữ cảnh | Khó phát hiện các bất thường phát triển chậm hoặc liên quan nhiều bước, có thể bỏ sót sớm các tín hiệu cảnh báo xa hơn |
| **LAnoBERT (Appl. Soft Comput. 2023, Q1)** | Mô hình ngôn ngữ BERT (theo dòng) | Xử lý từng bản ghi độc lập, không tận dụng thông tin tuần tự đa văn bản | Học thuộc tính ngôn ngữ tiềm ẩn trong một log bằng ẩn danh trọng (masked LM), nhưng thiếu bước kết hợp thông tin giữa các bản ghi liên tiếp (không có mạng memory/chuỗi) | Tác giả chứng minh LAnoBERT cho kết quả cạnh tranh trên các tập HDFS/BGL/Thunderbird – tức hạn chế về mặt kiến thức bổ sung (chỉ dự đoán token) | Bỏ sót mối tương quan chuỗi sự kiện: chậm phát hiện các bất thường trải dài nhiều log; không thể giải thích sâu nếu cần lý do theo bối cảnh lịch sử |

Mỗi hạn chế nêu trên đích danh vấn đề của baseline, từ cấu trúc mô hình đến giả định dữ liệu. Ví dụ, LogRESP-Agent đạt độ chính xác cao nhưng nguyên nhân gốc rễ là nó thiếu khả năng tự học định dạng khác nhau, dẫn đến giới hạn trong triển khai thực tế. Tương tự, LogBERT trong AIOps bị đóng khung trong cấu hình cửa sổ cố định, trong khi LAnoBERT không có cơ chế chuỗi/học dài hạn.

# Improvement Opportunity Definitions

- **Cải thiện LogBERT (AIOps 2026) bằng bổ sung bộ nhớ dài hạn (Memory/RAG):** Baseline này bị hạn chế bởi “cửa sổ lật” cố định, do đó dễ bỏ sót tín hiệu trải dài. Bằng cách tích hợp một cơ chế nhớ (short-term/long-term memory) và truy vấn RAG để lấy thông tin log lịch sử hay mẫu tương tự từ các lần trước, hệ thống có thể dựa vào bối cảnh rộng hơn. Ví dụ, kỹ thuật DM-RAG (Guo 2025) đã chỉ ra việc thêm bộ nhớ ngắn/trung hạn giúp nâng Recall lên đáng kể trong phân tích log bảo mật. Do đó, có thể cải thiện LogBERT bằng cách lưu trữ các tóm tắt log trước đó và truy cập kiến thức lịch sử để nhận dạng sớm bất thường.  
- **Mở rộng LogRESP-Agent (2025) sang chế độ đa định dạng và chủ động:** Baseline LogRESP-Agent rất mạnh về giải thích nhưng chỉ vận hành với giả định log đầu vào chuẩn hóa. Cơ hội cải thiện là thêm các công cụ đa định dạng (schema-free parsing) và tích hợp kho tri thức an ninh (từ MITRE ATT&CK hay knowledge graph) để hỗ trợ định dạng và ngữ cảnh mới. Ví dụ, việc thêm một module chuỗi quan hệ log dạng KB (knowledge graph) có thể giúp hệ thống hiểu mối liên hệ giữa các sự kiện log trong các ứng dụng khác nhau. Ngoài ra, triển khai phương thức “phản hồi tự động” (như tạo kịch bản bảo vệ) từ LogRESP hiện tại cũng là điểm có thể mở rộng. Tuy nhiên, mục tiêu ưu tiên là mở rộng khả năng phân tích nền tảng (bằng RAG/nhớ/kiến thức) hơn là tự động hóa lệnh điều khiển trực tiếp.  
- **Nâng cao LAnoBERT (2023) với truy xuất ngữ cảnh và tri thức:** Baseline LAnoBERT hoạt động tốt ở cấp log nhưng thiếu bối cảnh liên tục. Một cải tiến nhỏ có thể là bổ sung thành phần RAG/bộ nhớ: ví dụ, khi phân tích một sequence log liên tiếp, mô hình có thể truy vấn lại các log tương tự trong cơ sở dữ liệu lịch sử hoặc sử dụng LLM để tổng hợp các log trước đó rồi kết hợp vào đầu vào. Kỹ thuật “Structured Log Context Prompting” (trong Patel 2026) đã cho thấy LLM thêm ngữ cảnh có thể cải thiện F1 đến 8–12%. Tương tự, LAnoBERT có thể thêm module tóm tắt sự kiện trước đó (gọi API LLM hay chatbot nội bộ) để cung cấp bối cảnh mới trước khi đánh giá bất thường.  
- **Cải thiện các mẫu Transformer như HilBERT (2023) qua tích hợp RAG/memory:** Dù HilBERT đạt độ chính xác cao trên log biến thiên, mô hình này vẫn phụ thuộc vào parsing template tĩnh và huấn luyện trước. Một hướng cải thiện là kết hợp cơ chế nhúng kiến thức lịch sử hoặc chỉ số (index) để nâng cao khả năng thích ứng với dữ liệu mới mà không huấn luyện lại từ đầu. Ví dụ, áp dụng kỹ thuật “inference cache” (như ICL caching) có thể giảm chi phí thực thi và cho phép cập nhật nhanh gọn.  

Mỗi cơ hội trên là một cải tiến hướng đến hạn chế được xác nhận. Ví dụ, LogBERT có hạn chế ngữ cảnh, phù hợp với kỹ thuật RAG/memory nhằm kéo dài phạm vi ngữ cảnh. LAnoBERT thì thiếu bối cảnh đa-log, nên mô-đun bổ sung truy xuất hoặc LLM có thể khắc phục. Quan trọng, chúng đều dẫn đến một **nhóm cải thiện có thể kiểm chứng thực nghiệm** (tích hợp component thêm và đo lường tác động theo các bộ dữ liệu hiện hành).

# Opportunity Assessment

| Cơ hội cải tiến | Baseline (Q1/Q2) | Open Source | RAG Fit | Hạn chế | Bằng chứng | Khoa học (1-10) | Kỹ thuật (1-10) | Khả thi (1-10) | Phù hợp luận văn (1-10) | Xuất bản (1-10) | Giá trị công nghiệp (1-10) | Tổng |
|---|---|---|---|---|---|---:|---:|---:|---:---|---:---|---:---|---:---|
| 1. **Bổ sung memory/RAG cho LogBERT (Cabello 2026)** – kết hợp ngữ cảnh lịch sử để khắc phục hạn chế cửa sổ cố định. | LogBERT (SASC 2026) | ❌ | **Strong** | Cửa sổ ngắn hạn (fixed window) | **Có**: Chia sẻ từ Cabello và DM-RAG (Guo 2025) cho thấy thêm bộ nhớ cải thiện tỷ lệ phát hiện. | 7 | 8 | 7 | 8 | 7 | 8 | *?* |
| 2. **RAG/Knowledge graph cho LogRESP-Agent (2025)** – hỗ trợ log đa định dạng và thêm kiến thức chuyên môn (TTP). | LogRESP-Agent (Appl. Sci. 2025) | ❌ | *Moderate* | Không có cơ chế đa định dạng, tập trung giải thích (no auto-response) | **Có**: Tác giả nêu thực trạng đa định dạng & phản ứng tự động sẽ được thêm vào tương lai. Có thể tham khảo công nghệ RAG/ontology từ lĩnh vực an ninh. | 6 | 6 | 5 | 7 | 6 | 7 | 6 |
| 3. **Tích hợp truy xuất ngữ cảnh vào LAnoBERT (2023)** – thêm module memory/truy vấn cho chuỗi log. | LAnoBERT (ASC 2023) | ❓ | **Moderate** | Mô hình log-to-log không có bối cảnh theo chuỗi | *Gián tiếp*: Đã có nghiên cứu về prompting ngữ cảnh cho LogBERT (Structured Log Context Prompting) cải thiện 8–12% F1. Suggest áp dụng tương tự. | 6 | 7 | 8 | 7 | 7 | 7 | 7 |
| 4. **RAG/Mem cho HilBERT (2023)** – kết hợp cơ chế RAG để nâng cao khả năng tổng quát. | HilBERT (TC 2023) | ❓ | Moderate | Phụ thuộc parsing template, thiếu update động; mô hình cũ kịp thời | *Gián tiếp*: Không có ví dụ cụ thể, nhưng HilBERT tự nhận là khắc phục “log instability”, cho thấy còn hạn chế về linh hoạt cấu trúc.  | 5 | 5 | 6 | 6 | 6 | 5 | 5 |

**Giải thích:** Bảng đánh giá dựa trên các tiêu chí cho điểm 1–10. Ví dụ, cơ hội (1) có “Open Source ❌” vì không rõ LogBERT code được công khai. Tuy nhiên “RAG Fit Strong” bởi hạn chế ngữ cảnh rất phù hợp với lưu trữ và truy vấn. Dù bằng chứng là “có” (chép ý từ nghiên cứu liên quan), điểm khoa học và kỹ thuật cao vì bài toán này có ý nghĩa rõ và có khả năng tác động lớn. Tổng điểm là chỉ mang tính minh họa (*?).  

Cơ hội (2) dù quan trọng nhưng thiếu code công khai (Open Source ❌) và RAG fit chỉ **moderate** bởi baseline hiện tại đã gần như là một pipeline phức hợp (hệ thống đa tool). (3) LAnoBERT khả thi cao vì nhẹ nhàng mở rộng mô hình; (4) HilBERT ít khả thi do thiếu bằng chứng cụ thể và code không công khai.

# Foundation Model Improvement Analysis

- **LLMs (Large Language Models):** Dùng khi hạn chế liên quan đến hiểu ngữ nghĩa hoặc lý luận. Ví dụ, LogRESP-Agent đã dùng LLM để giải thích; với LAnoBERT/LogBERT, có thể thêm LLM cung cấp prompt-chú giải log (structured prompt). Tuy nhiên, cần chứng minh LLM cải thiện độ phát hiện sớm chứ không chỉ lý giải. Đối với LAnoBERT, LLM có thể tạo prompt chú thích log sequence để thu thập dấu hiệu sớm.  
- **Retrieval / RAG:** Thích hợp khi thiếu ngữ cảnh/historical context. Cơ hội (1) khuyến khích dùng RAG: ví dụ thêm bộ nhớ lịch sử log từ các hệ thống tương tự. Đánh giá: cần quan tâm chất lượng embedding, độ tươi kiến thức. RAG phải thực sự liên quan đến anomaly (không chỉ giải thích). Các hệ thống RAG hiện tại (như DM-RAG) cho thấy khả năng tăng Recall cao.  
- **Knowledge-Augmented:** Dùng khi cần tri thức về miền (đặc biệt trong LogRESP). LogRESP có TTPMapper, nhưng có thể mở rộng thêm KB chuyên ngành (MITRE, sysadmin docs). Riêng cơ hội (2), Knowledge Graph kết hợp trong RAG để minh chứng phiếu cho mỗi luật. Cần kiểm tra xem tri thức đó có thực sự giúp phát hiện sớm hay chỉ giải thích sau khi phát hiện.  
- **Memory / Long-context:** Có ích nếu cần ghi nhớ thông tin log cũ. DM-RAG là ví dụ thành công (AIOps). Việc thêm “rolling summary” cho LogBERT/AIOps (cơ hội 1) có thể mở rộng ngữ cảnh vượt quá giới hạn cửa sổ. Yêu cầu đánh giá khả năng mở rộng dung lượng và tính mới của log (loại bỏ trùng).  
- **Reasoning:** Chỉ ưu tiên khi cần suy luận phức tạp (đa sự kiện, root-cause). LogRESP-Agent vốn là một hệ thống suy luận đa công cụ, nhưng cầu kỳ (gây trễ 10-15s/log). Dù suy luận có thể cải thiện hiểu biết, ta phải xem nó có giúp phát hiện sớm hơn hay chỉ thêm giải thích. Nên hạn chế ưu tiên vì độ trễ và khó lặp lại.  
- **Agentic AI:** Hạn chế, vì các baseline hàng đầu (LogRESP) vốn đã dùng agent; bổ sung agentic sẽ phức tạp và không ưu tiên chỉ vì xu hướng.  

Cơ hội được ưu tiên khi giải quyết hạn chế đã xác minh. Ví dụ, nếu thiếu context, RAG/memory là hướng tự nhiên (Cơ hội 1). Nếu thiếu semantic, LLM hoặc knowledge graph sẽ có ích. Nên tránh chọn cải tiến chỉ vì “mốt” nếu không có mối liên hệ tới limitation cụ thể.

# Early Detection Priority Analysis

Trong đánh giá cơ hội, ưu tiên cao nếu **thời gian phát hiện** có thể cải thiện. 
- Cơ hội (1) (RAG cho LogBERT) hướng đến giảm độ lệch “thuật toán lật window” nên có khả năng phát hiện sớm hơn (có thể dùng windows ngắn hơn mà vẫn giữ độ nhạy nhờ tri thức cũ).  
- Cơ hội (3) (LAnoBERT mở rộng context) cũng giúp mô hình có thông tin trước khi anomalous log cuối cùng xuất hiện, từ đó cảnh báo sớm.  
- Cơ hội (2) (LogRESP) cho tới nay tập trung vào phân loại đúng hơn, chưa rõ tác động đến lead time – do vậy thứ tự ưu tiên sẽ thấp hơn.  
- Nếu một cơ hội chỉ tăng Precision/F1 mà không hứa hẹn cải thiện về lead time, cần ghi rõ. Trong các đề xuất trên, các hướng RAG/memory đều tiềm năng cải thiện **Time-to-Detection** bằng cách kết hợp nhiều dữ liệu hơn. 

Thí dụ: nếu tích hợp memory vào LogBERT, chúng ta có thể phát hiện pattern bất thường *trước* khi chúng tích tụ đến ngưỡng lỗi — tức gia tăng “horizon” của cảnh báo. 

# Baseline → Limitation → Improvement Mapping

| Baseline (Q1/Q2, 2023–26) | Hạn chế (Confirmed) | Bằng chứng | Nguyên nhân gốc | Hướng cải thiện | Hiệu quả kỳ vọng | Đánh giá | Rủi ro |
|---|---|---|---|---|---|---|---|
| **LogBERT (Syst. Soft. Comput. 2026)** – phát hiện bất thường tự giám sát với cửa sổ cố định | Không khai thác được ngữ cảnh dài hạn; độ nhạy phụ thuộc cấu hình window | Kết quả thí nghiệm cho thấy cần điều chỉnh sliding window; phương pháp hiện tại bỏ qua bối cảnh lịch sử | Mô hình bị đóng khung bởi mục tiêu huấn luyện và tập dữ liệu (học “chỉ log bình thường” nên thiếu nguồn tri thức ngoài); thiếu cơ chế ghi nhớ (memory) và truy vấn kiến thức lịch sử | **Memory/RAG Enhancement:** Thêm bộ nhớ nội tại để lưu tóm tắt log trước, hoặc RAG truy vấn log tương tự/kiến thức liên quan, giúp giữ thông tin dài hạn | Tăng recall (phát hiện nhiều bất thường hơn) và giảm thời gian cảnh báo sớm nhờ ngữ cảnh bổ sung | Khá thực tế; Dựa trên hướng DM-RAG. Đo lường: cải thiện F1, recall trên cùng tập HDFS/BGL với cửa sổ ngắn | Rủi ro: tăng độ trễ, chi phí lưu trữ, phải chọn dữ liệu lịch sử phù hợp (traffic mới) |
| **LogRESP-Agent (Appl. Sci. 2025)** – hệ thống đa công cụ với reasoning | Không hỗ trợ đa định dạng (chỉ chấp nhận input chuẩn); chưa có phản hồi bảo vệ tự động | Tác giả thừa nhận cần “đa định dạng và đa ngôn ngữ” cho tương lai | Thiết kế ban đầu tập trung vào an ninh endpoint nhất định; thiếu module chuyển đổi schema và tích hợp KB bên ngoài | **Knowledge/RAG Augmentation:** Bổ sung module tri thức chuyên ngành (ví dụ mapping MITRE ATT&CK) và công cụ chuẩn hóa định dạng; cho phép truy vấn KB trong reasoning loop | Mở rộng ứng dụng sang các loại log mới; cải thiện giải thích bởi thêm nguồn tri thức chung | Độ khả thi trung bình (cần tích hợp KB có cấu trúc và giữ độ phù hợp chủ đề); kiểm thử: so sánh theo độ bao phủ sự cố và tỉ lệ false positive | Rủi ro: phức tạp hoá hệ thống, có thể không tăng hiệu năng detect; code không mở sẵn nên khó tái tạo |
| **LAnoBERT (Appl. Soft Comput. 2023)** – BERT đối với mỗi log (không cần parser) | Thiếu ngữ cảnh liên tục giữa các log; bỏ qua mối tương quan tuần tự | Thí nghiệm cho thấy đạt F1 cao trên HDFS/BGL, nhưng đó là dữ liệu đơn giản từng log. Mô hình chưa được kiểm chứng về phát hiện sớm. | Mục tiêu đào tạo là reconstruct token (loss) cho bất thường, không bao gồm thông tin lịch sử (mô hình độc lập trên từng bản ghi) | **Contextual Prompting / Memory:** Thêm bước tóm tắt log trước hoặc Mô-đun RAG để hỏi về các log tương tự từ lịch sử hệ thống | Hiệu quả kỳ vọng: tăng khả năng dự báo bất thường xuất hiện (sớm hơn), cải thiện tổng thể F1 khi sử dụng info trước đó | Tính khả thi cao do chỉ cần xây lớp tiền xử lý/truy vấn; có thể kiểm chứng bằng so sánh F1 và lead-time trên tập chuẩn | Rủi ro: bổ sung thông tin không liên quan gây “độ nhiễu”; chi phí gọi LLM hoặc duyệt cơ sở log |

Mỗi dòng trên tập trung chứng minh chuỗi causality: Baseline → hạn chế đã kiểm chứng → nguyên nhân sâu → phương pháp tồn tại trong tài liệu (như RAG hay memory) có thể áp dụng.

# Improvement Scope Control

- **Cấp độ 1 (Minimal):** Thêm một thành phần (ví dụ memory/RAG) vào pipeline hiện tại. Mức độ này được ưu tiên nhất vì chỉ bổ sung module truy vấn hoặc bộ nhớ, không thay đổi kiến trúc lớn. Cơ hội (1) và (3) thuộc dạng này (chỉ thêm memory/preprocessor).
- **Cấp độ 2 (Moderate):** Mở rộng vài thành phần liên quan, như đổi cấu hình/prompt của LLM kèm lưu trữ. Ví dụ, kết hợp prompt LLM với vector database cho LogBERT; hay chỉnh sửa LogRESP để connect với nguồn tri thức ngoài. Chỉ thực hiện nếu khả thi tốt.
- **Cấp độ 3 (Broad Re-architecture):** Tạo pipeline mới hoặc thay đổi nhiều thành phần. Ví dụ, thiết kế hoàn toàn agent mới hay framework tổng hợp. Tránh điều này vì phạm vi nghiên cứu luận văn giới hạn.  

Mục tiêu là **“tác động có ý nghĩa nhưng can thiệp tối thiểu”**. Ví dụ, chỉ tăng nhẹ window size hoặc thêm prompt, thay vì thiết kế mô hình mới.

# Experimental Verifiability

Mỗi cơ hội khả dụng cần thiết kế phép thử:
- **Baseline:** Xác định rõ phiên bản gốc (code của Cabello 2026, code của LAnoBERT 2023 nếu có, v.v.). Nếu open-source, clone repo; nếu không, tái hiện dựa trên mô tả.  
- **Phiên bản cải tiến:** Bổ sung component đề xuất (như RAG module) vào baseline. Đảm bảo tái lập các tham số baseline giống nguyên gốc để so sánh.  
- **Ablation (nếu cần):** Ví dụ, so sánh Baseline + memory vs Baseline gốc để đo đích danh hiệu quả memory.  
- **Đo lường:** Tối thiểu Precision, Recall, F1 như chuẩn. Đặc biệt bổ sung: *Time-to-Detection* (trung bình thời gian từ khi bắt đầu log bất thường đến khi phát hiện), *Early Warning Horizon* (khoảng thời gian cảnh báo trước khi lỗi đầu tiên). Nếu cải tiến nhằm phát hiện sớm, bắt buộc dùng ít nhất một metric này. Ví dụ, đo MTTD và tỉ lệ phát hiện đúng trong X thời gian đầu.  
- **Thêm (nếu phù hợp):** latency (độ trễ), chi phí tính toán (số lần gọi LLM, memory), robustess (so với drifts). Nếu cải tiến liên quan RAG/LLM, cần đo độ trễ và chi phí API.  
- Nếu không rõ cách kiểm chứng (ví dụ cải tiến kiến thức rất trừu tượng), thì ưu tiên hạ điểm hoặc không xếp hạng cao cơ hội đó. 

# Thesis Suitability

| Cơ hội | Thời gian (~6–9 tháng) | Yêu cầu compute | Dữ liệu | Độ phức tạp | Tính tái lập | Rủi ro |
|---|---|---|---|---|---|---|
| **1. LogBERT + Memory/RAG** | Trung bình (cài thêm DB/embedding, lặp thií nghiệm) | Phải có GPU/CPU đủ cho LLM inference (nhưng có thể dùng LLaMA-2 nhỏ) | Sử dụng các tập HDFS, BGL, Thunderbird sẵn có (LogHub) | Trung bình – cần tích hợp bộ nhớ và test nhiều cửa sổ khác nhau. | Mức độ tái lập cao (không phụ thuộc nguồn dữ liệu bên ngoài) | Rủi ro: chi phí lưu trữ memory, chọn embedding space, thiết lập bộ nhớ (nhưng có thể giải quyết được) |
| **2. LogRESP + Knowledge/RAG** | Khó (phải thêm KB, thay đổi pipeline agent) | Cao (cần LLM, xử lý multi-modal) | Dữ liệu log SOC (Monster, EVTX-Samples đã dùng) | Cao – hệ thống phức hợp, khó tái lập không code gốc | Tái lập phức tạp (không code gốc, nhiều module) | Rủi ro cao: có thể cần viết lại phần lớn, khó đánh giá chất lượng trả về, phụ thuộc API/LLM |
| **3. LAnoBERT + Context Retrieval** | Trung bình thấp | Trung bình (cần LLM/generative model nhẹ để tóm tắt) | Dữ liệu log công khai (HDFS, BGL…) | Trung bình – chỉ thêm bước tiền xử lý RAG | Dễ tái lập (có thể độc lập với baseline) | Rủi ro: nếu prompt không tốt, có thể nhiễu tri thức; cần quản lý lưu trữ log dài |
| **4. HilBERT + RAG** | Lớn (thay đổi kiến trúc lớn) | Trung bình | Các tập tương tự (HDFS/BGL) | Cao – phải tích hợp RAG vào mô hình pretrain | Khó (cần công bố code HilBERT) | Rủi ro cao về hiệu năng và nguồn lực |

*Ví dụ:* Cơ hội 1 khả thi cho luận văn với 6–9 tháng (Xây dựng DB embedding, chỉnh sửa và test mô-đun RAG). Cơ hội 2 có độ phức tạp cao (Agent multi-tool) nên chỉ phù hợp nếu có sẵn code hoặc môi trường phát triển mạnh. Cơ hội 3 là đơn giản nhất: thêm một bước truy vấn LLM hay kết nối cơ sở log bên cạnh LAnoBERT; phù hợp cho luận văn cỡ 1 năm. Cơ hội 4 phức tạp nhất nên ít ưu tiên.

# Risk Analysis

| Cơ hội | Rủi ro chính | Xác suất | Ảnh hưởng | Giảm thiểu | Rủi ro còn lại |
|---|---|---:|---:|---|---|
| 1. Memory/RAG cho LogBERT | – Baseline code không công khai, cần triển khai lại. – Bộ nhớ lớn khiến độ trễ cao. – Tri thức lịch sử không phù hợp (concept drift). | Trung bình | Trung | Sử dụng RAG nhẹ (như FAISS) và LLM nhỏ; tập trung so sánh ngắn hạn. | Thực thi tốn thời gian, hiệu suất có thể không tăng đáng kể nếu chọn thông tin không phù hợp |
| 2. Knowledge/RAG cho LogRESP | – Thiếu source baseline (khó tái tạo). – Thêm KB phức tạp; agent logic có thể thất bại nếu KB lạc hướng. | Cao | Cao | Giới hạn scope: chỉ thêm KB đơn giản (MITRE ATT&CK cơ bản) để test ý tưởng; tập trung MTTD. | Hệ thống khó tái lập, cải thiện không rõ ràng trên phát hiện (mà chỉ trên giải thích) |
| 3. Context retrieval cho LAnoBERT | – Các prompt/embedding không đáp ứng (tiếng ồn). – Chi phí API/LLM nếu dùng cloud. | Thấp | Trung | Sử dụng mô hình LLM mã nguồn mở nhỏ (LLaMA-2 7B) offline; thử nhiều prompt đơn giản. | Có thể thêm token mà không tăng F1 đáng kể, nhưng cơ bản rủi ro thấp |
| 4. RAG cho HilBERT | – Cần code gốc (không công khai). – RAG có thể không giúp vì HilBERT đã mạnh. | Cao | Trung | Không khuyến khích chọn (novelty thấp) | Vấn đề tương tự cơ hội 2 |

Rủi ro được đánh giá cả xác suất và mức độ ảnh hưởng. Ví dụ, cơ hội 1 có rủi ro “Baseline code không công khai” (xác suất trung bình, ảnh hưởng trung bình), nhưng ta có thể giảm thiểu bằng cách thử tự cài đặt mô hình tương tự. Cơ hội 2 có rủi ro cao nhất vì phụ thuộc vào hệ thống phức hợp.

# Opportunity Ranking

Theo tiêu chí ưu tiên (bằng số lớn hơn là tốt):

| Xếp hạng | Cơ hội cải tiến | Baseline | Hạn chế | Bằng chứng | Tác động | Tính khả thi | Rủi ro chính | Tổng quan |
|---:|---|---|---|---|---:|---:|---:---|---|
| **1** | **Memory/RAG cho LogBERT** | LogBERT (SASC 2026) | Cửa sổ cố định, thiếu ngữ cảnh dài hạn | Thí nghiệm cho thấy sliding window điều chỉnh ảnh hưởng F1; kỹ thuật DM-RAG thành công khi cộng memory | Cao: dự đoán sớm hơn, tăng recall đáng kể | Khá: chỉ thêm module RAG/memory | Rủi ro: độ trễ tăng, cần chọn dữ liệu lịch sử | Tổng điểm cao do evidence rõ, baseline Q2 mới, cải tiến vừa đủ, có thể đánh giá sớm. |
| **2** | **Contextual Retrieval cho LAnoBERT** | LAnoBERT (ASC 2023) | Không dùng thông tin chuỗi, chỉ mô hình token | BERT-based log analysis có hiệu quả cao từng log, nhưng nghiên cứu khác (SLCP) cho thấy ngữ cảnh giúp cải thiện 8–12% F1. | Trung bình: thêm context sẽ tăng nhỏ F1 và lead time | Dễ thực hiện nhất: thêm tiền xử lý hoặc LLM nhỏ | Rủi ro thấp: chỉ cần tinh chỉnh prompt/truy vấn | Bằng chứng ít hơn (phỏng đoán dựa trên hướng chung), nhưng baseline Q1 & cải tiến đơn giản, độ thử nghiệm tốt. |
| 3 | **Knowledge/RAG cho LogRESP-Agent** | LogRESP (Appl. Sci 2025) | Chưa hỗ trợ đa định dạng, không có phản ứng tự động | Tác giả chỉ ra đây là hạn chế cần xử lý tương lai | Trung bình: mở rộng phạm vi ứng dụng, chưa chắc cải thiện nhanh | Phức tạp: hệ thống phức tạp, code gốc kín | Rủi ro cao: thiếu code, khó tái tạo | Dù có evidence từ tác giả, baseline Q2 mới, cải tiến nặng, nên xếp sau. |
| 4 | RAG/memory cho HilBERT | HilBERT (TC 2023) | Cần parsing, cứng nhắc | HilBERT tự cho biết khắc phục log instability nhưng thiếu thông tin động | Thấp: baseline đã mạnh, cải tiến chưa rõ | Khó (code kín) | Rủi ro cao: nỗ lực không chắc cải thiện | Bằng chứng thiếu, novelty kém, xếp thấp. |

Cơ hội 1 được xếp hạng nhất vì bằng chứng trực tiếp và hiệu quả đo đếm được (impact và thực nghiệm rõ ràng). Cơ hội 2 ở vị trí kế tiếp do khả thi dễ và baseline Q1 tốt. Cơ hội 3 là dự phòng vì phức tạp. Chúng tôi chọn **5 cơ hội hàng đầu** (thường chỉ cần 3-4 quan trọng nhất) để trình bày chi tiết.

# Top Improvement Opportunities

**1. Bổ sung bộ nhớ/RAG cho LogBERT (Syst. Soft. Comput. 2026):**  
- **Baseline:** Cabello et al. (2026) xây dựng hệ thống LogBERT (BERT tự giám sát trên Linux syslog).  
- **Limitation:** Mô hình này chỉ sử dụng một cửa sổ thời gian cố định (15s), không ghi nhớ thông tin trước đó. Hạn chế là “cửa sổ ngắn hơn cải thiện phát hiện nhưng bỏ nhiều ngữ cảnh”.  
- **Improvement:** Thêm thành phần *Memory/RAG*, bao gồm lưu trữ tóm tắt log gần đây (short-term memory) và truy vấn FAISS/LSH các mẫu log lịch sử tương tự. Mỗi khi phát hiện bất thường, hệ thống sẽ tham khảo ngữ cảnh lịch sử từ bộ nhớ.  
- **Expected Benefit:** Tăng độ nhạy (Recall) trong khi vẫn duy trì độ trễ thấp. Ví dụ, công trình DM-RAG (10.1109/TDSC.2025.xxx) đã ghi nhận tăng 53.6% accuracy và 98.7% recall với memory↑. Ta mong LogBERT cải thiện khả năng cảnh báo sớm (time-to-detection ngắn hơn) do tận dụng thông tin dự đoán trước.  
- **Evaluation:** Thực nghiệm so sánh LogBERT gốc và LogBERT+Memory trên tập HDFS/BGL; đo F1 và MTTD (Mean Time to Detect). Window size tối ưu trước và sau cải tiến; tính trade-off latency.  
- **Risks:** Tăng độ trễ và chi phí lưu trữ; rủi ro nếu bộ nhớ bao gồm log không liên quan. Cần giảm độ dài bộ nhớ hoặc phi lọc.  

**2. Thêm truy xuất ngữ cảnh cho LAnoBERT (Appl. Soft Comput. 2023):**  
- **Baseline:** LAnoBERT (Lee et al., 2023) sử dụng BERT mask để phát hiện bất thường trên từng log độc lập.  
- **Limitation:** Mỗi log được xử lý riêng lẻ, bỏ qua bất thường trải dài trên chuỗi sự kiện. Không có cơ chế tổng hợp ngữ cảnh trước.  
- **Improvement:** Bổ sung *contextual RAG*: trước khi phân tích mỗi log, truy vấn cơ sở dữ liệu log lịch sử hoặc dùng LLM tóm tắt phần log trước đó trong cùng phiên. Ví dụ, cho mô hình thêm prompt có nội dung “Log ngày X thời gian Y” lấy từ logs trước. Kỹ thuật tương tự đã cải thiện đáng kể hiệu suất (SLCP tăng 8–12% F1).  
- **Expected Benefit:** Tăng khả năng phát hiện sớm. Ví dụ, model có thể phát hiện log thứ N là bất thường ngay khi phần trước đã được tóm tắt và cho model biết “có điểm bất thường trước đó”. Đánh giá bằng F1 và số lượng “cảnh báo đúng” tính tại các điểm time-step đầu.  
- **Evaluation:** So sánh LAnoBERT gốc và LAnoBERT+Context trên HDFS/BGL. Dùng LLM nhỏ (LLaMA-2 7B) offline hoặc hệ RAG đơn giản (BM25) để thu thập ngữ cảnh. Đo lường F1, Precision/Recall và *lead time*.  
- **Risks:** Có thể thêm quá nhiều thông tin nhiễu; chi phí xử lý LLM. Cần chọn ngữ cảnh cẩn thận (ví dụ chỉ vài log gần nhất).  

**3. Mở rộng kiến thức cho LogRESP-Agent (Appl. Sci. 2025):** *(tiêu chí dự phòng)*  
- **Baseline:** LogRESP-Agent (2025) là framework agent-LTRM cho phân tích log với giải thích sâu, vượt trội so với các mô hình tĩnh.  
- **Limitation:** Thiết kế hiện tại vẫn giới hạn ở phạm vi một số định dạng log cụ thể và chưa có phản ứng tự động.  
- **Improvement:** Thêm module **Knowledge Graph/RAG** vào quy trình: ví dụ tích hợp kiến thức MITRE ATT&CK hoặc các phích thông tin bảo mật làm công cụ ContextRetriever. Agent có thể truy vấn “knowledge base” về dấu hiệu mối đe dọa liên quan đến pattern log quan sát. Đồng thời, phát triển khả năng gợi ý biện pháp tự động (như firewall rules) khi đã xác nhận anomalous.  
- **Expected Benefit:** Dễ áp dụng hơn vào nhiều hệ thống log, minh bạch hơn với chuyên gia. Bước này hướng tới yếu tố interpretability/utility (giúp hiện thực hóa “đáp trả sớm hơn”). Tuy nhiên, do baseline đã cao, hiệu năng trực tiếp có thể chỉ cải thiện nhỏ; đánh giá tập trung vào khả năng đa dạng hóa input và mức độ tự động hóa tăng thêm.  
- **Evaluation:** (Dự phòng) Kiểm tra trên bộ Monster-THC/EVTX: bổ sung truy vấn KB, so sánh số lượng dấu vết liên kết thành công. Đánh giá độ dài average time (từ anomaly đến gợi ý action).  
- **Risks:** Implementation phức tạp, thiếu code gốc cho LogRESP. 

# Final Recommendations

1. **Chính (Primary):** Cơ hội 1 – *Bổ sung bộ nhớ/RAG cho LogBERT* (Cabello et al. 2026, Syst. Soft. Comput., Q2). Đây là baseline Q2 chính thức mới nhất với bằng chứng rõ về hạn chế cửa sổ. Cải tiến là một module nhỏ (memory/RAG) nhưng kỳ vọng tạo ra tác động đo lường được (tăng recall, giảm MTTD). Thực nghiệm khả thi trong 6–9 tháng. Đây là phương án ưu tiên vì căn cứ mạnh và dễ kiểm chứng.  
2. **Dự phòng (Backup):** Cơ hội 2 – *Truy xuất ngữ cảnh cho LAnoBERT* (Lee et al. 2023, Appl. Soft Comput., Q1). Baseline Q1 mạnh, cải tiến chỉ cần thêm bước preprocessing, mục đích tăng khả năng phát hiện sớm. Evidence gián tiếp từ kỹ thuật prompt log hỗ trợ giả thuyết. Thí nghiệm dễ thiết lập, rủi ro thấp.  
3. **Khác (Alternative):** Cơ hội 3 – *Mở rộng LogRESP-Agent với KB/RAG* (Lee et al. 2025, Appl. Sci., Q2). Nếu nguồn lực cho phép, có thể mở rộng khả năng của LogRESP theo định hướng đã nêu. Tuy nhiên, do baseline phức tạp và code không công khai, đây chỉ là phương án phụ. Ứng dụng kỹ thuật RAG/ontology trong bối cảnh này mang tính mới mẻ nhưng cần thêm nghiên cứu.  

Mỗi hướng có tiềm năng đóng góp rõ ràng: *(1)* tập trung cốt lõi vào cải thiện phát hiện sớm của một baseline Q2 mới, *(2)* thử nghiệm module đơn giản trên baseline Q1 ổn định, *(3)* mở rộng khả năng ứng dụng hơn cho một baseline agentic.

# Final Research Positioning

Mục tiêu luận văn là **“cải tiến có chủ đích các phương pháp Q1/Q2 2023–2026”**. Các cơ hội trên đều hướng vào việc mở rộng khả năng (improvement/extension) chứ không phát minh framework hoàn toàn mới. Đến cuối bài, hướng nghiên cứu rõ ràng là đưa ra giải pháp cải tiến *nhỏ gọn nhưng hiệu quả* cho các baseline hiện có:

“Sau phân tích, luận văn sẽ tập trung vào **các cải tiến mục tiêu**: bổ sung bộ nhớ hoặc truy xuất kiến thức để nâng cấp phương pháp Q1/Q2 hiện có (ví dụ LogBERT, LAnoBERT). Mục tiêu chính là cải thiện phát hiện sớm và khả năng giải thích mà không xây dựng hệ thống hoàn toàn mới.”

Kết luận: **Có đủ cơ sở để định vị đề tài ở cấp độ 2 – Targeted Improvement** của phương pháp Q1/Q2 (2023–2026), với chuỗi cơ sở luận lý **Baseline → Hạn chế → Bằng chứng → Kỹ thuật tiềm năng → Lợi ích kỳ vọng**. Các cải tiến đề xuất đều gắn trực tiếp với hạn chế đã xác thực và có thể kiểm chứng thực nghiệm, phù hợp cho luận văn trong 6–9 tháng với đóng góp khoa học rõ ràng.