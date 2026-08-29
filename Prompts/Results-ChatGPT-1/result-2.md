# Phân tích học thuật: Chọn và Cải tiến phương pháp phát hiện bất thường log sớm (2025–2026)

## 1. Validation of Literature Mapping  
**Claim:** Các xu hướng gần đây chú trọng ứng dụng mô hình ngôn ngữ lớn (LLM) và phương pháp RAG cho phát hiện bất thường log. **Supporting Evidence:** Tài liệu tổng quan cho thấy LLM và RAG giúp tăng độ chính xác và khả năng giải thích của hệ thống phát hiện bất thường so với phương pháp truyền thống. Ví dụ, Cabello et al. nhận xét “LLM-based approaches significantly outperform traditional methods” về F1, precision và recall. **Contradicting Evidence:** Một số khảo sát cũ chỉ đề cập DL thông thường (LSTM, Autoencoder) mà chưa đề cập tới LLM. Chưa có nhiều công trình thực nghiệm so sánh toàn diện giữa LLM và các kiến trúc DL truyền thống trên tập data chuẩn. **Confidence:** Medium. **Assessment:** Xu hướng dùng LLM/RAG trong AIOps được nhắc đến nhưng bằng chứng thử nghiệm đầy đủ còn hạn chế. Có báo cáo cho thấy RAG giảm hiện tượng “hallucination” và tăng khả năng thích ứng môi trường, song cần thêm phân tích độc lập.  

**Claim:** Cấu trúc phân loại (taxonomy) các phương pháp phát hiện bất thường log bao gồm: **deep learning** (LSTM, Transformer, BERT), **học tăng cường/RAG**, **knowledge graphs**, và **agent AI**. **Supporting Evidence:** Khảo sát của Landauer et al. (2023) liệt kê nhiều kiến trúc DL (CNN, RNN, Transformer) cho anomaly detection. Ngoài ra, các công trình gần đây đề xuất RAG (ví dụ RAGLog) và KGs (OntoLogX) để bổ sung ngữ cảnh cho LLM. **Contradicting Evidence:** Chưa có sự đồng thuận rõ về phân loại – một số tác giả chủ yếu phân chia theo mô hình (học không giám sát, có giám sát, xen kẽ) mà không nhấn vào LLM/RAG. Các khung agent AI chỉ vừa mới xuất hiện (LogRESP-Agent 2025) và chưa phổ biến. **Confidence:** Low-Medium. **Assessment:** Taxonomy chưa được chuẩn hóa trong tài liệu, tuy nhiên các hạng mục LLM, RAG, KG, agent là hợp lý dựa trên xu hướng mới. Tuy nhiên, nhiều phương pháp (cụ thể dl truyền thống) chưa tích hợp cơ chế giải thích/diễn giải/phát hiện sớm, nên đánh giá sơ bộ cần đính chính khi bằng chứng chưa đầy đủ.  

**Claim:** Thời gian (timeline) nghiên cứu phát hiện bất thường log: ban đầu chủ yếu dựa trên luật cố định (trước 2010), sau đó ML/DL phát triển từ 2010–2020, và từ 2022 xu hướng LLM/RAG xuất hiện. **Supporting Evidence:** Landauer et al. (2023) đề cập thành tựu deep learning gần đây (NLP, speech) được ứng dụng cho logs từ khoảng 2018 trở đi. Patel (2026) cũng trình bày khảo sát LLM mới nhất (GPT-4, LLaMA-3) áp dụng cho 2024–2026. Báo cáo SLR 2025 xác nhận LLM/RAG là xu hướng mới giúp “boost accuracy and interpretability”. **Contradicting Evidence:** Không có. **Confidence:** High. **Assessment:** Các báo cáo khảo sát và nghiên cứu gần đây nhất nhất trí rằng các mô hình ngôn ngữ tiên tiến (GPT-4, LLaMA-3) và RAG là hướng nghiên cứu mới nổi (2024–2026). Tuy nhiên, cần lưu ý nhiều phương pháp mới (như RationAnomaly 2025) vẫn trong giai đoạn thử nghiệm không rộng.  

## 2. Cross-paper Critical Analysis

### 2.1 Foundation Models  
Mô hình ngôn ngữ lớn (LLM) như GPT-3.5, GPT-4, LLaMA-3… có khả năng “hiểu ngữ nghĩa log” nhờ được huấn luyện trên kho văn bản khổng lồ cả tổng quát và chuyên ngành. Theo Patel (2026), LLM “possess an inherent understanding of log semantics that traditional methods lack”. Tuy nhiên, hiệu suất phát hiện bất thường chủ yếu bị chi phối bởi phương pháp sử dụng (fine-tune vs prompt) và phạm vi ngữ cảnh. Trên các tập log chuẩn, mô hình tinh chỉnh (fine-tuned BERT/RoBERTa) vượt trội hơn prompt LLM (F1 ~0.96-0.99 vs 0.82-0.91). Điều này cho thấy LLM thừa sức giải thích ngữ nghĩa nhưng việc dùng trực tiếp (zero-shot) có độ chính xác thấp hơn các mô hình chuyên biệt khi có đủ nhãn huấn luyện. Như vậy, LLM có **semantic understanding** mạnh nhưng chỉ **generalize** tốt trong các bài toàn thu thập huấn luyện khổng lồ; khi áp vào log logs (thông tin kỹ thuật) có domain mismatch (trừ khi fine-tune). LLM cũng dễ **hallucinate** (tạo thông tin sai) nếu không có dữ liệu nền trợ giúp. Mức độ **contextual understanding** phụ thuộc vào chiều dài ngữ cảnh (token window); ví dụ RationAnomaly (2025) cần tóm tắt log qua bộ nhớ để tránh input quá dài.  

Về **anomaly interpretation/explanation**, LLM tiềm năng cao: chúng có thể sinh ngôn ngữ tự nhiên giải thích kết quả (Ví dụ, hệ thống LogREx tuyên bố LLM+KG cho giải thích rõ ràng). Trong khi đó, kiến trúc transformer tinh chỉnh hay các mạng RNN/Autoencoder truyền thống thường là black-box, thiếu giải thích. Công trình RationAnomaly kết hợp Chain-of-Thought (CoT) với Reinforcement Learning làm minh chứng: CoT fine-tuning giúp huấn luyện LLM sinh các bước lý luận giải thích, cải thiện độ tin cậy và giảm hallucination. Tuy nhiên, hầu hết các báo cáo (ví dụ [22]) chỉ tập trung vào F1, Precision, Recall tiêu chuẩn; các chỉ số đặc thù cho cảnh báo sớm (lead time, MTTD) thì hiếm thấy. Như Landauer et al. (2023) lưu ý, “early detection of relevant incidents” là mục tiêu, nhưng chưa công bố độ trễ phát hiện cụ thể.  

**Đánh giá:** Các Foundation Models hứa hẹn về ngữ nghĩa và giải thích, nhưng chưa thể thay thế hoàn toàn mô hình tinh chỉnh truyền thống về độ chính xác thuần túy; đồng thời chúng có nhược điểm về chi phí token, độ trễ inference và dễ bị hallucination khi không có biện pháp khắc phục. Cần phân biệt rõ giữa khả năng giải thích (explainability) – vốn được cải thiện nhờ CoT và KG – và khả năng phát hiện sớm; hiện chưa có bằng chứng rằng LLM một mình thực hiện tốt *early detection* nếu chỉ đánh giá bằng F1 thông thường.  

### 2.2 Retrieval / RAG  
Các phương pháp retrieval/RAG đóng vai trò quan trọng trong các hệ thống LLM hiện đại để cải thiện kiến thức hậu cảnh cho mô hình (giảm hallucination) và tăng hiệu suất phát hiện. NVIDIA Log Analysis Agent (2025) sử dụng cả BM25 và FAISS (embedding) để thu hồi log liên quan, kết hợp thành hybrid retrieval. Cụ thể, hệ thống này thực hiện: (1) Hybrid retrieval: BM25 bắt từ khóa, vector embedding bắt ý nghĩa; (2) Reranking để sàng lọc kết quả cho liên quan cao; (3) Grading và Generation; (4) Vòng tự sửa lỗi nếu câu truy vấn ban đầu không đủ kết quả. Điều này cải thiện khả năng nắm bắt các mẫu bất thường; hạn chế là độ trễ cao (vòng gọi LLM nhiều bước) và phức tạp.  

Nhiều nghiên cứu gần đây tích hợp RAG cho phát hiện bất thường log. Ví dụ, RAGLog (2024) tạo ngăn xếp mẫu log bình thường; khi có log mới, nó truy vấn những bản mẫu tương tự để làm ngữ cảnh cho LLM quyết định có bất thường hay không. EnrichLog (2025) lại hợp nhất “kiến thức corpus” (văn bản hướng dẫn sử dụng, định nghĩa sự cố) và “kiến thức mẫu” (ví dụ bị đánh dấu) thông qua retrieval để làm giàu đoạn log trước khi phân loại. Kết quả là EnrichLog cải thiện hiệu suất trên nhiều tập chuẩn và hiệu quả tính toán nhờ tách bước lọc nhanh các log rõ ràng bình thường rồi mới thực hiện RAG cho trường hợp còn lại. Tuy vậy, việc xây dựng và duy trì kho dữ liệu hoặc văn bản ngoại sinh vẫn là thách thức (cần cập nhật) và retrieval có thể “đưa” ngữ cảnh không liên quan (pollution) hoặc quá cũ (stale knowledge). Mặc dù [9] cho rằng LLM+RAG thích nghi tốt với môi trường thay đổi, song không nhiều kết quả thực nghiệm công khai để kiểm chứng luận điểm này.  

 *Hình 1: Minh họa khái niệm pipeline Retrieval-Augmented (mũi tên vàng – FAISS embedding, mũi tên xanh – BM25) và tích hợp vào hệ thống phân tích log.*  

**Hỏi:** Retrieval cải thiện phát hiện hay chỉ giải thích? Các công trình như [9] và [40] báo cáo cải thiện chính xác khi thêm retrieval/context so với baseline thuần LLM, nghĩa là nó giúp kết quả phát hiện tốt hơn (độ nhạy/TNR tăng). Đồng thời, thông tin thu thập qua retrieval (ví dụ tri thức về lược đồ hệ thống, ví dụ lịch sử) làm tăng khả năng giải thích (LLM đưa ra câu trả lời có lý giải). Tuy nhiên, cải thiện lớn nhất của retrieval thường là giúp giải trình (giảm hallucination) và hiệu suất ổn định hơn, chứ hiếm khi “tăng lead time”.  

### 2.3 Reasoning  
Hướng phát triển hiện nay là kết hợp Chain-of-Thought (CoT), tự phản tỉnh (self-reflection) và đa bước (multi-step) để cải thiện khả năng suy luận của LLM trong bối cảnh logs. Ví dụ, RationAnomaly (2025) minh họa lợi thế của CoT fine-tuning: mô hình được huấn luyện sinh *reasoning trace* (ngôn ngữ diễn giải từng bước) và dùng RL để tối ưu cả độ chính xác lẫn tính hợp lý逻辑 của kết quả. Nhóm tác giả đã nhận xét “LLM-based methods are often hindered by unreliability and hallucinations” và giải pháp của họ nhằm giảm thiểu điều này bằng tối ưu trực tiếp qui trình suy luận.  

Tuy nhiên, trong hầu hết các phương pháp log anomaly truyền thống (DL hay LLM-đơn thuần), việc suy diễn lỗi gốc/phát hiện nguyên nhân gốc (root-cause reasoning) ít được đề cập. Một hệ thống LLM với CoT có thể giả lập suy luận từng bước (ví dụ giám sát nếu `NullPointerException` → lỗi ứng dụng, nếu `IOException` → I/O), nhưng cần khung logic/law riêng. Agent như LogRESP-Agent (2026) còn cho thấy khả năng tự động áp dụng luật và công cụ (như RuleMatcher, ContextRetriever) để liên tục điều chỉnh giả thuyết. Điều này minh chứng khả năng đa bước và đa công cụ cho giải thích phức tạp, nhưng đi kèm độ trễ và khó tái sản xuất cao. Trong khi đó, các mô hình DL thuần túy (DeepLog, LogRobust, v.v.) đạt F1 cao nhưng diễn giải rất hạn chế.  

Về **reasoning liên tục qua thời gian (temporal reasoning)**, hầu hết phương pháp vẫn giới hạn ở trong một cửa sổ log cố định (session hoặc sliding window). Mô hình không có bộ nhớ dài hạn (ngoại trừ giải pháp tóm tắt như Egersdoerfer đề xuất) nên dễ bỏ lỡ bất thường phụ thuộc chuỗi sự kiện nhiều bước. Ví dụ, LogLLM nhận thấy “token limit” khiến LLM không thể xử lý chuỗi log dài quá. Dù vậy, LLM có thể tự suy luận một phần nếu ngữ cảnh đủ dài để thấy “điệp khúc” (pattern) nào bất thường xuất hiện. Các phương pháp đa-bước/chuyển bước (như agent đa tác nhân) có tiềm năng làm tốt hơn trong reasoning liên tục, nhưng đòi hỏi thiết kế phức tạp.  

**Đánh giá:** LLM với CoT và agentic AI cho ra khả năng reasoning vượt trội, tạo ra chuỗi lý giải rõ ràng (cải thiện explainability). Điều này quan trọng cho *giải trình anomalous events* nhưng chưa chứng minh trực tiếp cải thiện *phát hiện sớm*. Ngoài ra, mô hình phức tạp, ít rõ ràng trong cấu trúc, khiến khó đánh giá tác động độc lập. Công trình RationAnomaly tuy công bố SOTA nhưng chưa có bên thứ ba đánh giá. Trừ khi có dữ liệu phân hạng lỗi (expert labels) để huấn luyện reasoning, khả năng phát hiện của agentic AI dựa vào chất lượng công cụ tích hợp (rule, KGs) sẽ quyết định.  

### 2.4 Knowledge-Augmented AI  
Áp dụng tri thức bên ngoài (knowledge graphs, ontology, documentation, báo cáo sự cố, lịch sử logs) nhằm làm giàu ngữ cảnh phát hiện bất thường. OntoLogX (2026) là ví dụ gần nhất: nó sử dụng LLM cộng ontology để chuyển logs thô thành graph dữ liệu vi phạm, gắn với MITRE ATT&CK. Kết quả khẳng định việc xây KG giúp thu thập thông tin từ nhiều logs khác nhau và liên kết với chiến thuật tấn công, dẫn đến thông tin hành động có giá trị cho CTI. Điều này cho thấy **structured knowledge** (domain ontology, KG) có thể giúp hệ thống định nghĩa ranh giới bất thường (chẳng hạn, “Error 500” liên hệ tới khía cạnh tuyến bài toán web) và đưa ra giải thích.  

Tuy nhiên, tri thức này đòi hỏi duy trì (cập nhật ontology, doc), chất lượng định nghĩa (chính xác, nhất quán). Chẳng hạn, OntoLogX cần đảm bảo KG “syntactically and semantically valid” qua nhiều bước chỉnh sửa. Nếu kiến thức lỗi thời hoặc không phù hợp, LLM vẫn có thể bị nhiễu (pollution). Ngoài ra, phần lớn phương pháp hiện tại (EnrichLog, OntoLogX) tập trung vào xây knowledge cho mục đích giám sát/phân loại, chưa khai thác đầy đủ cho *phát hiện sớm* (không thấy metric lead-time hay dự báo).  

**Đánh giá:** Tri thức bên ngoài (KG, tài liệu, báo cáo) giúp cải thiện khả năng phân loại logs nhờ ngữ cảnh, đặc biệt tăng tính minh bạch/giải thích. Bằng chứng từ OntoLogX cho thấy KGs rất hữu ích để “extract actionable CTI”. Tuy nhiên, việc tích hợp chúng có tính đắt đỏ (cần công cụ xây, bảo trì) và chưa có đánh giá trực tiếp về lợi ích cho *early anomaly detection*.  

### 2.5 Agentic AI  
Multi-agent, LLM-điều phối (có planning, gọi tool, tự động hóa điều tra) là lĩnh vực mới cho log analysis. Ví dụ, **NVIDIA log analysis agent** (2025) triển khai ba “agent” lần lượt thực hiện: kiểm tra tính liên quan, tái viết truy vấn, và tạo phản hồi, cùng với bộ điều khiển RAG trung tâm. Mỗi agent đóng vai trò riêng (kiểm tra sự khớp, sửa prompt, tạo câu trả lời). Họ sử dụng NeMo Embedding và Llama-3.3 để tính toán semantic retrieval, đồng thời tự động lặp lại truy vấn khi cần (self-correction loop). Hình 2 (Nvidia) minh họa kiến trúc đa tác nhân cho thấy khả năng phân tách nhiệm vụ, tái sử dụng mô hình embed/LLM nhiều lần với mục đích khác nhau.  

Tương tự, LogRESP-Agent (2026) của Ravichandran sử dụng khung LangChain: một agent LLM “planner” phối hợp các công cụ chuyên biệt (RuleMatcher, ContextRetriever, TTPMapper) theo quy trình TAO (Thought–Action–Observation) để suy luận đa bước về sự cố. Họ nhấn mạnh kết quả không chỉ là nhãn bất thường mà còn kèm *Reasoning Trace* và *Mapped Threat Context* (đưa ra liên hệ MITRE), giúp nhân viên tin tưởng kết quả.  

Tuy nhiên, các hệ thống này rất phức tạp: yêu cầu hạ tầng mạnh (đa mô hình, kết nối API), khó tái lập. Độ trễ lớn do phải gọi nhiều mô-đun liên tiếp. Khả năng lặp lại kết quả thấp (cần seed, context giống). Bù lại, chúng có thể thực hiện phân tích “autonomous”, khảo sát logs, truy vấn cơ sở tri thức, và tự cập nhật giả thuyết. Đây là lợi thế cho các quy trình điều tra tấn công phức tạp hơn là đẩy front-end anomaly detection nhanh.  

**Đánh giá:** Agentic AI mang lại khả năng *investigation* sâu, hội tụ dữ liệu và suy luận dựa trên nhiều công cụ – điều mà các mô hình DL/LLM đơn thuần không có. Người đánh giá các tác phẩm này ca ngợi tính lý giải và hệ thống hóa việc truy vấn. Tuy nhiên, chúng chỉ phù hợp cho bài toán điều tra/phân tích sự cố (incident response) hơn là *phát hiện sớm* theo thời gian thực, bởi chi phí tính toán và độ trễ. Ngoài ra, kết quả là dự đoán cuối cùng (bất thường hay không) thường kèm theo phần giải thích — có thể dùng để đánh giá hiệu quả, nhưng không đủ chứng minh so sánh độ chính xác với mô hình truyền thống do đánh giá phức tạp hơn (bạn cần đánh giá cả reasoning).  

## 3. 2025–2026 Baseline Candidate Assessment  
| Candidate            | Year | Problem Fit        | Performance (F1 etc.) | Reproducibility    | Architecture Clarity | Limitation Evidence         | Improvement Potential                | Experimental Feasibility | Baseline Suitability |
|----------------------|:----:|--------------------|----------------------|--------------------|---------------------|-----------------------------|---------------------------------------|-------------------------|----------------------|
| **RationAnomaly**    | 2025 | Phát hiện và giải thích bất thường log | *F1 cao* (SOTA theo báo cáo) | Code mở (GitHub), nhưng RL phức tạp | Mô hình LLM+CoT+RL nhiều thành phần | Hallucination (LLM); cần dữ liệu expert lớn | Kết hợp RAG để giảm hallucination; cải thiện speed (2-step); củng cố dataset | Cần GPU, RL tốn k. Code sẵn giúp thử nghiệm | Cao (đã có code & data) |
| **LLM-Enhanced (Patel)** | 2026 | Đánh giá so sánh LLM vs truyền thống | FT BERT: F1~0.96–0.99; GPT prompt: ~0.82–0.91 | Code là benchmark, dữ liệu công khai (LogHub) | Kiến trúc rõ (parser+ML, FT, prompt) | Prompt LLM kém chính xác nhất (dữ liệu ít) | Áp dụng context prompting cải thiện zero-shot; thêm kiến thức bằng RAG | Các tập HDFS/BGL etc có sẵn; dễ tái tạo | Trung bình (target kỹ năng benchmark) |
| **EnrichLog**       | 2025 | Entry-based anomaly detection với tri thức tăng cường | Tăng F1 so với baseline trên 4 dataset | Training-free (workflow); code không rõ | Mô hình hai giai đoạn (lọc nhanh + RAG) | Phụ thuộc documentation, cần parsing chính xác | Bổ sung KG hoặc self-learning cho knowledge; giảm latency hơn nữa | Triển khai bằng pipeline LLM/RAG, có thể phức tạp | Trung bình (yêu cầu xử lý văn bản và KG) |

**Chọn rút gọn:** RationAnomaly, LLM-Enhanced, EnrichLog. Các ứng viên này đại diện cho các hướng tiếp cận khác nhau (CoT+RL, benchmark LLM, knowledge augmentation). Mỗi ứng viên ủng hộ một khía cạnh (sự tiên tiến, khả năng so sánh, sử dụng tri thức).  

## 4. Baseline Decomposition  
Đối với mỗi baseline, xác định thành phần chính:  
- **RationAnomaly (LLM+CoT+RL):**  
  - *Preprocessing:* Phân đoạn log, chuyển thành văn bản đầu vào LLM.  
  - *Representation:* Sử dụng embedding nội tại LLM (GPT-based) cho log raw.  
  - *Context/Sequence:* Áp dụng prompt nội dung log, thêm hướng dẫn CoT.  
  - *Knowledge/Retrieval:* Ít dùng external (chủ yếu nội tại câu lệnh).  
  - *Memory/Reasoning:* Sử dụng CoT để ghi nhật ký reasoning; RL training tối ưu logic.  
  - *Anomaly Scoring:* Mô hình ra nhãn (bình thường/bất thường) với điểm tin cậy.  
  - *Threshold:* Sử dụng ngưỡng 0.5 trên softmax hoặc quyết định logic.  
  - *Training:* 2 giai đoạn: CoT fine-tune (supervised) rồi Reinforcement Learning tuning.  
  - *Inference:* Gọi LLM theo chuỗi step-by-step đã huấn luyện.  
  - *Feedback:* Không cập nhật thời gian chạy (phiên bản cố định).  
  - *Strength:* Khả năng giải thích (CoT); độ chính xác cao theo báo cáo.  
  - *Weakness:* Tính phức tạp (RL đòi hỏi huấn luyện đặc biệt, nhiều siêu tham số); đòi hỏi tập chuyên gia chất lượng.  
  - *Evidence:* Kết quả F1 và explainability (hàm thưởng logic) được trình bày.  
- **LLM-Enhanced (Benchmark):**  
  - *Preprocessing:* Drain/Spell parser để chuyển logs thành templates/token hoặc sử dụng trực tiếp text logs cho LLM.  
  - *Representation:* Dùng embedding BERT (fine-tune) hoặc cú pháp prompt cho GPT.  
  - *Context/Sequence:* Đối với fine-tune, sử dụng template + label; đối với prompt, cung cấp ví dụ (few-shot) hoặc prompt câu hỏi.  
  - *Knowledge/Retrieval:* Không có (phần lớn phương pháp đánh giá thô).  
  - *Memory/Reasoning:* Lưu mô hình được huấn luyện; không cơ chế reasoning multi-step.  
  - *Scoring:* Thuật toán phân loại nhị phân (softmax).  
  - *Threshold:* Mặc định 0.5 cho nhãn bất thường.  
  - *Training:* Fine-tune BERT/Transformer (supervised); prompt không huấn luyện (zero-shot).  
  - *Inference:* Chạy mô hình đã huấn luyện hoặc gọi API LLM (không cần tài nguyên retrain).  
  - *Feedback:* Không cập nhật trực tuyến.  
  - *Strength:* Khả năng so sánh công bằng, code open-source; F1 rất cao với fine-tune (0.99).  
  - *Weakness:* Phụ thuộc vào tập huấn luyện, không giải thích; prompt LLM zero-shot kém chính xác, đắt (GPT API) nếu thiếu label.  
  - *Evidence:* Nghiên cứu của Patel công khai số liệu hiệu năng, benchmark tiêu chuẩn.  
- **EnrichLog (Knowledge-Augmented):**  
  - *Preprocessing:* Parse log thành văn bản gốc.  
  - *Representation:* Kết hợp raw text + context enrichment (thêm ví dụ anomalous/normal bằng prompt).  
  - *Context/Sequence:* Quy trình hai bước: lọc log bình thường qua prompt nhẹ, sau đó áp dụng prompt + retrieval nếu nghi ngờ anomalous.  
  - *Knowledge/Retrieval:* Tích hợp “kiến thức tập hợp” (tóm tắt toàn bộ doc, định nghĩa sự cố) và “kiến thức mẫu” (lịch sử ví dụ) thông qua vector retrieval và LLM.  
  - *Memory/Reasoning:* Dữ liệu tri thức được mã hóa thành embedding; LLM tập trung phần cần thiết cho mỗi log.  
  - *Scoring:* Dự đoán nhãn bất thường hay không (binary classifier do prompt LLM thực hiện).  
  - *Threshold:* Bước đầu tiên lọc dùng ngưỡng confidence; bước RAG dùng câu trả lời LLM.  
  - *Training:* Không yêu cầu training mô hình (training-free framework).  
  - *Inference:* Gọi LLM với prompt chứa doc summary + ví dụ + log hiện tại.  
  - *Feedback:* Không tự cập nhật.  
  - *Strength:* Tận dụng kiến thức bên ngoài (tài liệu, ví dụ) để xử lý trường hợp log cùng template nhưng khác ngữ nghĩa. Hiệu suất cải thiện đáng kể trên nhiều tập (theo báo cáo).  
  - *Weakness:* Yêu cầu xây dựng các tài liệu hướng dẫn/sự cố đầy đủ, và tốn chi phí tính toán nhiều do hai bước gọi LLM.  
  - *Evidence:* Kết quả thử nghiệm cho thấy nhất quán tăng hiệu quả phát hiện qua baseline trên 4 tập logs.  

**Xác định cốt lõi, nút thắt:**  
- RationAnomaly: CoT+RL là cốt lõi, nhưng bottleneck là chi phí huấn luyện và hội tụ RL, cũng như giới hạn ngữ cảnh token. Có thể cải thiện bằng retrieval (giúp LLM không phải nhớ mọi thông tin) hoặc bằng phân tích chuỗi dài hơn (memory).  
- LLM-Enhanced: Cốt lõi là fine-tuned Transformer. Hạn chế ở prompt LLM (trừ khi dùng thêm context). Cải tiến có thể là thêm RAG hoặc CoT để prompt hiệu quả hơn, hoặc tối ưu prompt engineering.  
- EnrichLog: Cốt lõi là bổ sung kiến thức. Hạn chế: phụ thuộc thiết lập knowledge. Cải tiến: thêm KG hoặc điều chỉnh lựa chọn kiến thức động (dynamic retrieval), tối ưu prompt để giảm độ dài.  

## 5. Common Assumptions  
- **Log đã được parse (Drain/Spell)**: Hầu hết phương pháp DL và LLM đều giả định logs đã được tiền xử lý thành templates hoặc token; ví dụ trong LLM-Enhanced, Drain tách các log thành templates. Giả định này hợp lý vì parsing giúp tiêu chuẩn hóa, nhưng gây mất mát ngữ nghĩa (thông tin cụ thể bị loại bớt). Nó cũng làm lệ thuộc vào hiệu năng parser. Trong thực tế, logs có định dạng thay đổi thường xuyên, nên assumption này có thể là một hạn chế (cần kiểm định parser phù hợp). *Confidence:* High (dựa trên thực tế hầu hết công trình đều dùng parsing).  
- **Tập benchmarks cố định (HDFS, BGL, Thunderbird, Spirit)**: Gần như mọi nghiên cứu dùng các tập này để đánh giá, mặc dù logs thực tế đa dạng hơn. Giả định này giúp so sánh nhưng gây bias (overfit máy học vào đặc điểm benchmark). *Confidence:* High.  
- **Inference offline (không streaming)**: Các thí nghiệm thường tải sẵn logs và chạy batch, không giả lập stream thực. Điều này hợp lý cho đánh giá F1, nhưng không phản ánh hạn chế latency/online. *Confidence:* High (các đánh giá thực nghiệm chỉ dùng tập logs có sẵn).  
- **Không dùng tri thức bên ngoài**: Phần lớn hệ thống chuẩn chỉ dùng log nội tại và mô hình DL, không gọi kiến thức bên ngoài (trừ EnrichLog, OntoLogX). *Confidence:* Medium (đa số, trừ một vài SLR mới).  
- **Ngữ cảnh đủ (window ngắn)**: Giả định window log đưa vào đủ chứ không cần lịch sử dài. Nhiều thử nghiệm đặt window nhỏ (ví dụ HDFS fix-size). *Confidence:* Medium (thường mọi người dùng session/window như trong [26†L339-L347]).  
- **Labels ổn định**: Giả định rằng phân phối nhãn (bình thường/bất thường) không thay đổi giữa train/test, không có concept drift. *Confidence:* Medium (không có đánh giá drift trong hầu hết papers).  

Những assumption này giúp đơn giản hoá thiết kế, nhưng giới hạn tính ứng dụng thật. Ví dụ, giả sử log ổn định là không hợp lý trong môi trường thực, dễ gây giảm hiệu suất khi phần mềm cập nhật liên tục.  

## 6. Common Limitations  
- **Foundation Models:**  
  - *Hallucination:* LLM thường sinh thông tin sai nếu không có kiến thức chính xác. Cần RAG hay fine-tune để giảm.  
  - *Prompt sensitivity:* Kết quả phụ thuộc nhiều vào cách thiết kế prompt; thiếu robust khi prompt thay đổi.  
  - *Chi phí token/latency:* Các model lớn (GPT-4) rất tốn thời gian, tiền (API), nhất là khi phân tích logs dài. Ví dụ Gupta et al. (2025) phải tối ưu chạy trên CPU để rút ngắn thời gian.  
  - *Bối cảnh ngắn:* LLM có giới hạn số token, nên logs dài (>1000 dòng) phải tóm tắt hay cắt bỏ. Như [26] nêu, quá nhiều mẫu log một lúc vượt quá giới hạn token.  
  - *Domain mismatch:* Các LLM huấn luyện trên văn bản tổng quát (tiếng Anh) hoặc code; logs hệ thống có cấu trúc riêng, nên LLM không tối ưu nếu không fine-tune domain.  
- **Retrieval:**  
  - *Poor retrieval:* Kết quả thu hồi không đảm bảo liên quan hoàn toàn; có thể quăng vào dữ liệu rác (nếu embedding không tốt).  
  - *Embedding mismatch:* Nếu logs quá chuyên môn (code, config) so với embedding chung, có thể “không tìm được” đoạn tương tự.  
  - *Thông tin lỗi thời:* Dữ liệu lưu trữ (kiến thức) có thể cũ, không phản ánh cập nhật mới của hệ thống.  
  - *Context pollution:* Dữ liệu thu hồi vô tình làm mô hình “chú ý nhầm” phần không cần thiết.  
  - *Latency/Scalability:* Hệ RAG đôi khi phải tính toán embedding và truy vấn cơ sở dữ liệu vector lớn, tốn thời gian hơn inference thuần túy (như [36] cho thấy kết hợp BM25 và FAISS để cân bằng).  
- **Knowledge:**  
  - *Incomplete/Noisy:* Ontology hoặc documentation thường thiếu cập nhật, có thể sai hoặc không đầy đủ.  
  - *Alignment:* Để LLM hiểu ontologies cần format nhất quán; lỗi chuyển đổi làm model nhầm ý.  
  - *Maintenance:* Cập nhật KG, tài liệu đòi hỏi công tác liên tục (công việc thủ công).  
  - *Limited utility:* Tri thức chỉ giúp khi có sự kiện mới khớp thông tin; không đóng góp khi pattern bất thường hoàn toàn mới.  
- **Temporal/Context:**  
  - *Short context:* Xử lý theo window ngắn bỏ lỡ thông tin log liên kết xa.  
  - *Cross-window dependency:* Các bất thường lan man qua nhiều session không được phát hiện (hầu hết nghiên cứu chỉ xem xét từng session độc lập).  
  - *Concept drift:* Hệ thống giả định môi trường không đổi; logs thay đổi theo thời gian không được xử lý (lack online learning).  
- **Dataset:**  
  - *Benchmarks bias:* HDFS/BGL có tỷ lệ anomaly cố định, thường tạo ra bằng cách phóng to hoặc phá hủy block—không phản ánh lỗi an ninh/tấn công thực.  
  - *Imbalance:* Bất thường quá hiếm (1–7% logs) khiến mô hình dễ bị lệch sang dự đoán “bình thường” cho an toàn.  
  - *Limited domains:* Ít tập dữ liệu (chủ yếu datacenter cũ) nên các phát hiện có thể không áp dụng sang các ứng dụng mới (container, mobile, IoT).  
  - *Data leakage:* Nguy cơ train/test không phân tách đúng thể hiện (session-based splits).  
- **Evaluation:**  
  - *Offline-only:* Thiếu đánh giá thời gian thực.  
  - *Thiếu metrics stream/early-warning:* Hầu hết chỉ báo F1, thiếu lead-time, MT-Detect.  
  - *F1-centric:* Đôi khi phụ thuộc F1 dễ “lừa” (ví dụ threshold được chọn tối ưu), không đánh giá sớm hay chi phí cảnh báo giả.  
  - *No lead-time analysis:* Không đo thời gian cảnh báo trước sự cố.  

Tất cả các giới hạn trên đều xuất hiện trong các báo cáo hiện tại. Ví dụ, Landauer et al. (2023) chỉ đề cập tới các vấn đề mở (lack real-time processing, concept drift, explainability). Các công trình LLM mới thừa nhận vấn đề hallucination và tính không ổn định, nhưng chưa có giải pháp hoàn thiện.

## 7. Early Log Anomaly Detection Analysis  
Các phương pháp thường không phân biệt rõ *classical anomaly detection* (phát hiện khi anomaly đã xảy ra) và *early warning* (cảnh báo trước khi xảy ra thất bại). Mục tiêu “sớm” (early detection) hàm ý cần metrics như: **Detection Lead Time** (thời gian cảnh báo trước sự cố), **Time-to-Detection**, **MTTD** v.v. Hiện nay các báo cáo chủ yếu dùng **Precision/Recall/F1/Accuracy** (ví dụ [22], [28]), tức chỉ đánh giá phân loại, nên không chứng minh được khả năng cảnh báo sớm. Landauer et al. (2023) nhấn mạnh “cần hành động kịp thời để tránh cascading effects”, nhưng không cung cấp metric cụ thể. Rất ít tác phẩm báo cáo thời gian phát hiện tính bằng giây/phút. Nếu không có lead-time, chúng ta chỉ biết mô hình đánh dấu đúng sai, nhưng không biết nó giật điện báo trước bao lâu. Vì vậy, không thể đánh giá một paper thực sự “early” chỉ từ F1; cần đề xuất đo đạc mới (ví dụ average lead-time cho các anomaly được báo trước) khi đánh giá cải tiến.  

**Early warning vs. Failure prediction:** Một số nghiên cứu đề cập “predict failure” hơn là anomaly detection (như Sentinel logs forecasting). Cần chú ý: *fault prediction* hướng đến trước event cụ thể (machine failure), còn *anomaly detection* phát hiện mẫu bất thường trong log, có thể không dẫn tới hỏng. *Early anomaly detection* gộp cả hai: dự báo mẫu log lỗi trước khi nó xảy ra. Hầu hết công trình chỉ làm *anomaly detection* thông thường.  

## 8. Evidence Validation  
| Claim | Evidence Type | Supporting Paper(s) | Contradicting Evidence | Confidence |  
|---|---|---|---|---|  
| LLM-based methods cải thiện độ chính xác: RAG+LLM có độ F1 cao hơn phương pháp truyền thống. | Experimental (bài báo) | De la Cruz Cabello et al. (2025) báo cáo LLM-RAG “significantly outperform traditional”; Patel (2026) thấy prompt LLM F1 0.82–0.91 (hấp dẫn). | Hiện chưa thấy đối chứng lớn; một vài câu như [26] chỉ nêu khó khăn không rõ thí nghiệm cụ thể. | Medium |  
| CoT fine-tuning giúp giải thích: Chain-of-Thought tạo ra lý giải từng bước, giảm hallucination. | Author inference (RationAnomaly) | RationAnomaly (2025) chứng minh mô hình huấn luyện CoT + RL “effectively mitigating hallucinations” và có *transparent step-by-step outputs*. | Cần độc lập kiểm chứng (không có rep khác) | Low-Medium |  
| Retrieval giảm hallucination: RAG giúp grounding LLM, giảm thông tin sai lệch. | External evidence | AWS blog (2025) chỉ rõ RAG *“helps reduce generation of false or misleading information (hallucinations)”*. | RAG cũng vẫn có lỗi (không loại bỏ hoàn toàn hallucination). | High |  
| Biased benchmark: HDFS/BGL thiếu thực tế. | Survey | Khảo sát [44] nói cần stream, concept drift; bench HDFS/BGL không phản ánh môi trường thay đổi. | | High |  

## 9. Baseline → Limitation → Improvement Mapping  
| Baseline | Confirmed Limitation | Evidence | Existing Technique / Related | Improvement Opportunity | Expected Effect | Risk | Confidence |  
|---|---|---|---|---|---|---|---|  
| **RationAnomaly** | *Hallucination và tính không ổn định của LLM* | RationAnomaly tự trích dẫn hallucinations; AWS nêu RAG giảm hallucination. | Kỹ thuật RAG tổng quát; CoT fine-tuning. | Thêm Retrieval (RAG) để cung cấp log mẫu/bối cảnh, giảm thông tin sai lệch | Độ chính xác tăng; lý giải hợp lý hơn | Cần xây kho log mẫu; overhead thêm latency | Medium |  
| **LLM-Enhanced (Patel)** | *Phụ thuộc labels cho fine-tune; prompt LLM kém chính xác* | Kết quả prompt F1 chỉ 0.82–0.91, kém fine-tune. | Few-shot prompting improvements (SLCP). | Kết hợp CoT hoặc multi-step reasoning; sử dụng kiến thức ngoài (RAG/KG) trong prompt | Tăng F1 của prompt LLM (tiệm cận fine-tune), khả năng không cần nhãn | Tăng chi phí tính toán; phức tạp hóa workflow | Medium |  
| **EnrichLog** | *Phụ thuộc nhiều vào tài liệu hướng dẫn/bảo trì tri thức* | Đặt assumption tài liệu sẵn có. | Ontology/KG giúp cố định tri thức. | Kết hợp KG (OntoLogX) để có quy tắc/sự kiện rõ ràng hơn; học tự động từ logs mới | Giảm nhu cầu manual; bổ sung thông tin, giải thích rõ hơn | Tốn công tích hợp KG; mức độ cải tiến khó định lượng | Low-Medium |  
| **Tất cả** | *Không đánh giá sớm (no lead-time metric)* | Phần lớn papers không có; Landauer đề cập mục tiêu sớm. | Sử dụng metric như MTTD, nhãn thời gian (thời điểm failure) | Thiết kế thí nghiệm streaming, thêm cơ chế dự báo sự cố (forecast) | Đánh giá thực tiễn hơn, phản ảnh đúng “sớm” | Cần dữ liệu gắn time-stamp chuẩn; phức tạp hóa thí nghiệm | Medium |  

**Lưu ý:** Các limitation chỉ đưa ra khi có bằng chứng xác thực từ tài liệu (experimental hoặc kiến nghị từ tác giả). Hướng cải tiến đề xuất dựa trên kỹ thuật hiện có (RAG, KG, CoT, memory) và inference từ vấn đề.  

## 10. Improvement Candidate Ranking  
| Improvement Candidate              | Evidence       | Impact            | Novelty       | Feasibility  | Eval Ease    | Complexity | Risk      | Overall  |  
|---|---:|---:|---:|---:|---:|---:|---:|---:|  
| *Kết hợp RAG cho LLM baseline*            | Medium         | High              | Medium        | High         | High         | Medium     | Low       | **High** |  
| *Chain-of-Thought Fine-Tuning*           | Medium         | Medium-High       | Medium-High   | Medium       | Medium       | High       | Medium    | **High** |  
| *Knowledge Graph/Domain KG*              | Medium         | Medium            | Medium        | Medium       | Medium       | High       | Medium    | Medium   |  
| *Temporal Context Handling* (memory, drift) | Low            | Medium-High       | High          | Low          | Low          | High       | High      | Medium   |  
| *Prompt Engineering / SLCP*              | Medium         | Medium            | Medium        | High         | High         | Low        | Low       | Medium   |  
| *Multi-agent System*                     | Low            | High (interpret.) | High          | Low          | Low          | High       | High      | Low      |  

- **Ưu tiên:** Kết hợp RAG (retrieval) và Chain-of-Thought Fine-Tuning. Cả hai có bằng chứng rõ rệt về tác dụng (LLM-RAG tăng accuracy; CoT giảm hallucination), tác động cao (giúp cả detection và explain), và khả năng thực nghiệm khả thi (cả hai không yêu cầu dữ liệu label mới). Novelty ở mức trung bình vì đã có trước, nhưng trong ngữ cảnh logs tương đối mới.  
- Tiếp đến là **Prompt engineering**/tiếp tục SLCP (dựa trên Patel) – hiệu quả vừa phải nhưng dễ thực hiện.  
- **Knowledge Graph** cung cấp kiểm giải thích/kiến thức, nhưng phức tạp và cần xây dựng ontology.  
- **Xử lý temporal/drift** quan trọng nhưng chưa đủ evidence, khó thực hiện trong quy mô luận văn.  
- **Multi-agent** có tác động lớn về lý giải nhưng quá phức tạp, chi phí cao, ít khả thi.

## 11. Evidence-based Research Gap Candidates  
- **Thiếu tính thích ứng với concept drift:** Các baseline (ví dụ RationAnomaly, LLM-Enhanced) giả định phân phối ổn định. *Bằng chứng:* Khảo sát [44] chỉ ra các hệ DL phần lớn không xử lý log stream động. *Impact:* Mô hình có thể “học lệch” sau khi môi trường thay đổi. *Gap:* “Nghiên cứu thiếu cơ chế học tiếp” (incremental learning). *Existing:* Một số đề xuất log stream parsing (Spell [44†L1-L4]) nhưng không tích hợp LLM. *Opportunity:* Kết hợp continual learning (finetune hàng ngày). *Confidence:* Medium.  
- **Ít đánh giá lead-time/detect time:** Không có phương pháp nào đánh giá metric cảnh báo sớm. *Gap:* Thiếu pipeline cho early anomaly detection. *Evidence:* Phần lớn so sánh dùng F1 (ví dụ [22], [28]); [44] đề cập real-time processing cần thiết. *Opportunity:* Thiết kế thí nghiệm đặt mục tiêu phát hiện sớm (ví dụ bổ sung nhãn failure). *Confidence:* High.  
- **Thiếu giải thích hệ thống:* Nhiều baseline không hỗ trợ lý giải cho cảnh báo. *Evidence:* Hầu hết công bố chỉ F1, không trình bày gì. *Opportunity:* Kết hợp CoT hoặc KG để cung cấp nhãn và giải thích. *Confidence:* Medium.  

## 12. Benchmark and Practical Relevance  
Các tập dữ liệu phổ biến là **HDFS, BGL, Thunderbird, Spirit**. Tóm lại:  
- *HDFS:* logs hệ thống Hadoop, ~11M dòng, anomalies tạo ra bằng missing blocks. Dữ liệu thưa (2.4% anomaly). Thích hợp kiểm thử LSTM / seq2seq nhưng phát sinh *gian lận* (anomaly không là lỗi thực tế). *Production realism:* Thấp (phân phối lỗi nhân tạo).  
- *BGL:* logs siêu máy tính Blue Gene, ~4M dòng, ~7.4% anomalies. Nhiều log chiến thuật: sẹo ngẫu nhiên, ~thực tế hơn. Song domain (siêu máy tính) hẹp.  
- *Thunderbird/Spirit:* logs của các tác vụ (211M và 272M dòng) với lớp nhãn lỗi (bổ sung thủ công). Riêng *Spirit* là hội tụ tuyệt đối (lỗi dịch vụ) – thích hợp đánh giá phân loại. Tuy nhiên, tính chất không phải anomaly “tấn công”, ít phù hợp cho mục tiêu phát hiện sớm hệ thống.  
- *Vấn đề:* Cả bốn đều offline; giả lập theo session hoặc fixed window. Không có chỉ số lead-time. *Mismatch environment:* Thiết kế ban đầu cho fault detection, không phải security; logs cũ (2007–2015). *New trends:* Ít sử dụng log microservice, container, mobile, IoT; chưa phản ánh quy mô log streaming hiện đại.  

## 13. Research Positioning  
- **Level 1 (Reimplementation):** Chỉ tái hiện baseline công bố (không đủ mới).  
- **Level 2 (Targeted Improvement):** Cải tiến cụ thể cho nút cổ chai đã xác nhận. *Ưu tiên:* Kết hợp RAG vào RationAnomaly hoặc LLM-Enhanced; thêm CoT hoặc LLM-based summarization để cải thiện detection/early.  
- **Level 3 (Broader Extension):** Thay đổi nhiều thành phần (ví dụ tạo hệ thống đa tác nhân mới) chỉ xem xét nếu có cơ sở vững. *Không ưu tiên:* Việc “phát minh” hệ thống hoàn toàn mới (vd agent thuần, novel arch.) ít có bằng chứng mạnh.  

## 14. Comparative Capability Matrix (tổng hợp)  
| Capability               | Traditional DL | Transformer Fine-Tune | LLM (Prompt) | RAG-augmented LLM | Agentic AI       |  
|--------------------------|:--------------:|:---------------------:|:------------:|:-----------------:|:----------------:|  
| **Semantic Understanding**    | Thấp (template)   | Trung bình      | Cao (bán tự do) | Rất cao (có KG)  | Rất cao (multi-modal) |  
| **Anomaly Detection (F1)**    | Cao (như DeepLog, ~.95)  | Rất cao (~.96-.99) | Trung (0.8–0.9) | Cao (≥fine-tune) | Cao (theo tuyên bố)  |  
| **Early Detection** (lead time)  | Thấp  | Thấp  | Thấp  | Thấp  | Có thể (có planning) |  
| **Generalization** (adapter)   | Kém (dữ liệu mới)   | Tốt khi có labels | Tốt (zero-shot) | Rất tốt (dự phòng KB) | Tùy kiến thức agent (nhiều) |  
| **Explainability**           | Thấp (blackbox) | Thấp–Trung bình | Trung (via reasoning) | Trung–Cao (với context) | Rất cao (trace) |  
| **Retrieval Capability**      | Không có   | Không có  | Không có  | Có (BM25+embeddings) | Có (multiple queries) |  
| **Reasoning (multi-step)**    | Không  | Không  | Có hạn (prompt) | Có (dựa KG) | Rất cao (planning) |  
| **Temporal/Context Handling** | Bị giới hạn | Window nhỏ | Window nhỏ (token) | Cải thiện đôi chút (RAG có bối cảnh) | Có thể lưu state qua RL |  
| **Scalability** (tốc độ)        | Tốt (GPU) | Tốt (GPU) | Kém (API) | Kém (đồng thời MB25+emb) | Kém (đa tác nhân) |  
| **Industrial Readiness**     | Đã dùng nhiều | Đã dùng nhiều | Mới xuất hiện | Mới xuất hiện | Chưa sẵn sàng |  

*Nguồn/tham khảo:* Kết quả trên chủ yếu inference từ các báo cáo.  

## 15. Recommended Baseline  
**Phương pháp Baseline tốt nhất:** Theo đánh giá trên, phương án phối hợp LLM và RAG trên nền tảng fine-tuned Transformer được xác nhận có hiệu năng cao (ví dụ LLM-Enhanced của Patel 2026) là lựa chọn baseline. Tuy RationAnomaly tuyên bố F1 tốt nhưng có quá nhiều yếu tố phức tạp; trong khi EnrichLog chú trọng knowledge nhưng thiếu thông tin thực nghiệm đầy đủ. Do đó, **Dịch vụ LogRAG (LLM + Retrieval)** hoặc **hệ thống Transformers tinh chỉnh tiêu chuẩn** (như pipeline có parser + BERT + ML) sẽ là baseline thực tế.  

**Lý do chọn:** Độ sát đề bài cao (thực hiện anomaly detection cho logs hiện đại), đã được cộng đồng chấp nhận (benchmark công khai), độ chính xác cao, và có code/dữ liệu tái tạo. Cả LLM-Enhanced và RAGLog đều có thông tin và một phần code tham khảo (LogRAG có code trên GitHub). **Hạn chế cần cải tiến:** Các phương pháp này vẫn thiếu tích hợp context (RAG) và lý giải (CoT).  

## 16. Most Defensible Improvement Direction  
**Định hướng cải tiến:** Ưu tiên phát triển “LLM + Retrieval + Temporal Memory” kết hợp prompt engineering. Cụ thể: sử dụng một LLM lớn làm mô hình chính, bổ sung một kho dữ liệu log bình thường (retrieval) và cơ chế tóm tắt log dài (memory). Ví dụ: nhúng RAG vào pipeline baseline để LLM truy vấn mẫu logs tương tự, đồng thời áp dụng CoT fine-tuning để nâng cao khả năng giải thích. Các công nghệ này đã có bằng chứng hỗ trợ (RAG giảm hallucination, CoT cải thiện độ tin cậy). Cần thiết kế thử nghiệm cho trường hợp cảnh báo sớm (ví dụ simulasi streams) và đánh giá metric lead-time.  

**Đóng góp dự kiến:** Cải thiện trải nghiệm thực nghiệm và interpretability so với baseline. Dự kiến đóng góp khoa học ở mức **mô đun hóa pipeline** (augmentation của phương pháp có sẵn bằng retrieval/CoT) hơn là mô hình hoàn toàn mới. 

**Thực nghiệm:** Có thể xây dựng trên code LLM-Enhanced hoặc LogRAG sẵn, thêm thành phần retrieval (vector DB). Kiểm thử trên HDFS/BGL để đối chiếu với baseline. Bằng chứng mạnh (scientific) dựa vào F1 và lead-time, có thể đánh giá so sánh trực quan lý giải nếu áp CoT. 

**Kết luận:** Đề xuất xoay quanh cải tiến có căn cứ thực nghiệm cao: **kết hợp RAG và reasoning**. Đây không đơn thuần là mở rộng lý thuyết, mà dựa trên bằng chứng từ các khảo sát và thực nghiệm gần đây. Hướng đi này hứa hẹn tăng độ nhạy (với logs mới) và khả năng giải thích, đồng thời vẫn có thể thực nghiệm trong phạm vi luận văn. 

