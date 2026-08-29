# 1. Validation of Literature Mapping  
Trong `result-1.md`, nhiều bài báo mới sử dụng các kỹ thuật dựa trên mô hình ngôn ngữ (Transformer/LLM) cho bài toán phát hiện bất thường log. Ví dụ, Sci. Rep. 2025 giới thiệu *LogSentry* kết hợp contrastive learning và retrieval-augmented learning, trong khi Sci. Rep. 2026 đề xuất mô hình Transformer kết hợp phân tích sentiment để phát hiện bất thường log đơn lẻ. Các báo cáo cũng nhấn mạnh xu hướng “rich semantic information” trong log và cần kết hợp kỹ thuật NLP hiện đại (BERT và biến thể). 

Tuy nhiên, một số kết luận trong mapping cần xem xét cẩn trọng. Ví dụ, LogSentry tuy có cơ chế KNN retrieval nhưng thiếu đánh giá về chi phí hoặc giới hạn bối cảnh ngữ cảnh. Nhiều mô hình chỉ tối ưu F1/precision/recall (offline) mà không xét sớm. Các khẳng định về khả năng “miễn dịch với imbalance” hay “đột biến log format” cần kiểm chứng chi tiết. Dữ liệu nguồn dùng (HDFS, BGL) là chuẩn tác giả thừa nhận, nhưng chưa đại diện đủ cho log đa dạng hay streaming. Phân tích chi tiết:  

| **Claim** | **Supporting Evidence** | **Contradicting Evidence / Nhận Xét** | **Độ tin cậy** | **Đánh giá** |
|---|---|---|---|---|
| Mô hình LogSentry (Sci Rep 2025) đạt hiệu suất cao so với các phương pháp baseline khác. | Bài báo báo cáo *F1-score cao nhất* trên tập HDFS/BGL, vượt LogFormer\(_S\), LogRobust, DeepLog,…. | Tuy nhiên, kết quả chỉ so với một số baseline chọn lọc, không có đánh giá đa dạng (ví dụ không có so sánh với Mô hình retrieval-free mới khác) và thiếu thông tin về lead-time hay tính sớm. | Trung bình | Kết quả cải thiện F1 rõ rệt, nhưng cần đánh giá thêm về chi phí tính toán, khả năng generalize, và sớm (early) chưa được xét. |
| Mô hình “sentiment-aware” Sci Rep 2026 thu được F1 cực cao (>99%) và khả năng chuyển hệ thống (out-of-domain) cũng cao. | Báo cáo F1 đạt 99.96% (tập huấn luyện ~kiểm thử cùng hệ thống) và 96.97% (out-of-domain). | Điểm **đặc biệt**: mô hình này chỉ phát hiện bất thường tại các log entry riêng biệt, không dùng bối cảnh chuỗi sự kiện. Do đó “độ sớm” kiểu phát hiện sớm chuỗi chưa được thiết kế, khó áp dụng cho kịch bản streaming. | Cao | Mô hình chứng minh khả năng phân loại từng dòng log tốt. Nhưng hạn chế rõ ràng: không xét quan hệ nhiều log, chỉ “individual log”. |
| Các phương pháp mới 2023–2026 chủ yếu dựa trên BERT/Transformer/contrastive/embedding học sâu. | Nhiều bài báo nêu rõ dùng BERT hoặc Transformer (LogSentry sử dụng BERT; mô hình sentiment dùng BERT-ITPT-FiT; LogCEM dùng RoBERTa và CNN/GRU). | Thiếu bằng chứng sử dụng các kỹ thuật phi-DL hoặc thuật toán truyền thống. Hầu hết đều là Mô hình deep learning; chưa xét các approach dựa trên KG hoặc quy tắc. | Cao | Đúng với xu hướng chung: Log hiện được xử lý như ngôn ngữ tự nhiên, tận dụng Transformer. Tuy nhiên, cần lưu ý đánh giá so sánh với phương pháp phi-NN (không thấy nhiều trong mapping). |
| *Retrieval-Augmented* (RAG) chỉ mới thử nghiệm trong một số ít công trình (ví dụ LogSentry) và chưa rõ lợi ích thực sự. | Chỉ LogSentry đề cập rõ việc sử dụng KNN retrieval trong inference; chưa thấy nhiều bài khác sử dụng semantic retrieval hoặc RAG phức tạp hơn. | Các bài khác có nhắc đến “knowledge-augmented” (tiền huấn luyện kiến thức) nhưng không hẳn retrieval trực tuyến. Sự phù hợp của RAG cho anomaly detection chưa rõ ràng trong bằng chứng hiện có. | Trung bình | Có thể khẳng định RAG đang được chú ý (LogSentry), nhưng cần kiểm chứng thêm: Liệu retrieval có giúp phát hiện sớm hay chỉ cải thiện explainability? Chưa đủ dữ liệu kết luận. |

# 2. Phân tích xuyên bài

## 2.1. Foundation Models (BERT/Transformer)  
Các bài Q1/Q2 giai đoạn 2023–2026 đều khai thác mô hình ngôn ngữ tiền huấn luyện: **BERT** (nhiều báo cáo) và các kiến trúc Transformer phái sinh. Chẳng hạn, *LogSentry* dùng **BERT-base** để mã hóa log và huấn luyện contrastive learning; mô hình “sentiment-aware” dùng BERT-ITPT-FiT; *LogCEM* tận dụng **RoBERTa** để trích xuất vector từ mỗi từ log. Các mô hình này cho phép **semantic understanding** tốt (mã hóa ngữ nghĩa câu log) và thường mạnh trong phân loại cuối cùng, thể hiện qua F1 cao. Tuy nhiên, nhược điểm phổ biến là:
- **Contextual understanding**: Hầu hết chỉ xét từng dòng hoặc cửa sổ dòng log cố định; mô hình không lưu giữ bối cảnh dài hạn hoặc chuỗi sự kiện (thời gian) để phát hiện sớm. Ví dụ, mô hình sentiment chỉ phân tích độc lập từng log entry.
- **Generalization/Domain Adaptation**: Dù sử dụng BERT, các mô hình này cần huấn luyện với dữ liệu đặc thù (log Hadoop, HPC, IoT). “Out-of-domain” trong Sentiment là thử nghiệm đặc biệt, nhưng trong thực tế, logs thay đổi liên tục (new templates). Mô hình BERT không tự động thích nghi với log format mới trừ khi fine-tuning. 
- **Anomaly Interpretation vs Detection**: Các model BERT chủ yếu tập trung phân lớp (đầu ra anomaly hay không). Một số (Sentiment, LogCEM) kết hợp giải thích (như dùng **SHAP**), nhưng bản thân Việc giải thích không giúp phát hiện sớm. 
- **Early Detection**: Rất ít nếu không nói là không có. Các mô hình sử dụng F1/recall trên dữ liệu offline, nên không chứng minh được khả năng cảnh báo “trước khi xảy ra” (chỉ classification).

Nhìn chung, Foundation Models mạnh về **semantic encoding** của log (giúp phát hiện anomalies dựa vào ngữ cảnh từ các tokens) và *xu hướng chung* trong mapping cũng đúng như vậy. Tuy nhiên, sự thiếu hụt về luồng thời gian và bộ nhớ dài hạn (như trong LSTM/Tower memory hay RAG) cho phép mô hình sử dụng thông tin lịch sử, vẫn là hạn chế.

## 2.2. Retrieval / RAG  
Trong nhóm paper Q1/Q2, có **ít** công trình sử dụng rõ chiến lược Retrieval. *LogSentry* (Sci Rep 2025) là ví dụ điển hình: sử dụng KNN để lưu các feature vector log trong bộ nhớ và truy vấn tương tự. Phần còn lại (LogFiT, LogSentiment, LogCEM) không đề cập đến retrieval; chúng đều hoạt động “model-centric” trong inference. 

- **Embedding/Vector Store**: LogSentry lưu trữ các vector BERT của log và nhãn (0/1) trong một cơ sở kiến thức, rồi tính trung bình nhãn của K láng giềng để cộng với kết quả model. Không thấy đề cập tới sử dụng cơ sở dữ liệu lớn hơn hay kiến thức ngoài (semantic graph, log ontology).
- **Quality/Relevance**: KNN retrieval trong LogSentry có thể truy xuất log tương tự tốt nếu space vector đủ biệt lập, nhưng có nguy cơ **nghi vấn**: nếu log mới hoặc không giống nhóm training, KNN có thể trả nhầm nhãn (pollution). Bài báo không thảo luận hạn chế này. Latency của KNN trên nhiều bản ghi cũng có thể cao (tuy chưa đánh giá).
- **RAG Fit**: 
  - *LogSentry:* Strong Fit, vì đúng dùng retrieval cải thiện kết quả (mixture of experts). Cơ chế này hướng đến bù đắp cho độ thiếu tin cậy của model đơn thuần. Tuy nhiên, LogSentry dùng retrieval chỉ trên tập huấn luyện (feature vectors của chính dữ liệu đó), không thực sự “knowledge-enhanced” từ ngoài (ví dụ kiến thức miền hay historical anomalies).
  - *LogFiT:* Moderate Fit. Hiện chỉ fine-tune BERT trên log hiện tại, không lưu trữ hay truy vấn. RAG có thể hỗ trợ (vd. lưu trữ embedding log patterns hoặc knowledge graph cấu trúc logs) nhưng chưa được nghiên cứu trong paper.
  - *LogSentiment:* Moderate/Weak Fit. Mô hình cá nhân, nhưng có thể thêm retrieval về “sentiment log lexicon” hay templates nổi tiếng. Tuy nhiên, khả năng sử dụng RAG để cải thiện phát hiện bất thường trên cơ sở sentiment chưa rõ, vì mãng cơ chế chỉ là nội dung từ ngữ.
  - *LogCEM:* Weak Fit. Mô hình CNN/GRU kết hợp RoBERTa, không liên quan đến retrieval hay knowledge. Cải tiến RAG sẽ đòi hỏi chỉnh sửa lớn (như thay CNN bằng một retrieval module).
  
Tóm lại, retrieval có thể cải thiện **độ sáng tỏ** trong anomaly detection (thông qua giải thích, giám sát ví dụ tương tự) hơn là gia tăng tỷ lệ phát hiện sớm. Ví dụ, LogSentry kết hợp KNN giúp giảm false alarms hơn (tăng precision), chủ yếu cải thiện chẩn đoán. Đặc biệt, RAG chưa được chứng minh giúp phát hiện sớm (early detection), chủ yếu cải thiện hiệu suất classification. Chất lượng retrieval (độ tương tự của vector, bộ nhớ KNN) và vấn đề *stale knowledge* (không cập nhật log mới) cần thêm đánh giá.

## 2.3. Reasoning (CoT, Multi-step)  
Hầu hết các phương pháp trong review tập trung vào **mã hóa thống kê** và phân loại, chưa sử dụng rộng khái niệm reasoning đa bước. Không có paper nào rõ ràng triển khai Chain-of-Thought (CoT) hay tư duy chuỗi cho anomaly detection. Ví dụ, LogSentry và LogFiT dùng mô hình đơn bước (dự đoán trực tiếp anomaly hay không), Sentiment + SHAP chỉ giải thích quyết định, không “suy luận” nguyên nhân. 

- **Anomaly reasoning / Root-cause**: Hầu hết các báo cáo không đề cập tới phân tích nguyên nhân (root cause) dù nêu vai trò quan trọng. Mô hình sentiment giúp “giải thích” bằng SHAP (từ ngữ quan trọng), nhưng đó chỉ là chẩn đoán bề ngoài. 
- **Temporal/multi-event reasoning**: None. Các framework CNN/Transformer chỉ coi xét các log độc lập hoặc window nhỏ. Không có multi-step chaining (ví dụ, “xác định loạt events dẫn đến anomaly”).
- **Early warning**: Không được đánh giá dưới góc độ temporal. Hầu hết metric là F1, thiếu metric như lead-time, time-to-detect. Do đó, không thể khẳng định khả năng phát hiện sớm.
- **Explanation vs Detection**: Việc dùng SHAP (Sentiment, TGB model IIoT) hoặc attention chỉ nhằm giải thích, không trực tiếp nâng cao độ chính xác detection. RAG thường cải thiện “ngữ cảnh” hơn là reasoning.

### 2.4. Knowledge-Augmented AI  
Các bài hiện tại **hầu như không** tích hợp nguồn tri thức bên ngoài (chẳng hạn kiến thức miền, ontology log, historical incidents) để hỗ trợ phát hiện. *LogSentry* mới chỉ thu thập *feature embedding* log, không phải “kiến thức thực” (như GH&A logs, tài liệu hướng dẫn lỗi). Mô hình Sentiment hoặc CMC hoàn toàn không sử dụng knowledge graph hay external KB. 

Do đó:
- **Knowledge Graph, Ontology**: Hầu như vắng bóng trong các phương pháp Q1/Q2. Chưa thấy ví dụ nào xây dựng đồ thị sự kiện từ log để liên kết anomalies với nguyên nhân.
- **Historical logs**: Tất cả dùng datasets benchmark (HDFS, BGL, Thunderbird). Không dùng logs thực (tồn tại nhiều dạng, drift).
- **Domain knowledge**: Không rõ cập nhật domain-specific rules (vd. loại lỗi hay cấu trúc phần mềm).
- **Maintenance & Freshness**: Không có khái niệm cập nhật (model được train offline, static).
  
Tổng quát, mọi giải pháp hiện tại xem log chỉ như văn bản (text). Một hạn chế chính: thiếu exploitation của “external knowledge / mémoire” để hỗ trợ suy luận anomaly phức tạp hay biết trước hậu quả. Có thể coi đây là khe hở: ít công trình sử dụng RAG như knowledge retrieval, hay knowledge graph để tăng cường detection.  

### 2.5. Agentic AI  
Các giải pháp analyzed đều là **ô tô riêng lẻ**, không tích hợp agent hoặc hệ thống tác vụ/phối hợp phức tạp. Không có đề cập tới multi-agent, plan hay auto-diagnosis tool. Mọi thứ là neural network pipeline cố định. Việc gọi APIs hoặc agent-based exploration của logs chưa thấy trong Q1/Q2 papers này. Một số từ khoá như “RAG” gợi ý hướng agent (LLM gọi retrieval), nhưng thực tế các paper chỉ dừng ở mô hình machine learning cục bộ. Nếu có agent, có lẽ ở dạng future work (ví dụ tận dụng LLM để query tri thức log). 

Tóm lại, hầu như mọi work đều “passive”: nhận log vào, xuất nhãn anomaly/normal. Chưa có agent để điều tra log mới, truy vấn KB tự động hay thực hiện tác vụ cảnh báo/Lưu trữ. Cũng chưa thấy đánh giá latency/cost code GPT hay LLM. Vì vậy **độ phức tạp, chi phí, reproducibility** theo kiểu agent chưa có data; dường như không phải yếu tố chính ở các paper baseline.

# 3. Đánh giá Ứng viên Baseline Q1/Q2 (2023–2026)  

Dưới đây là các ứng viên thỏa mãn điều kiện (Journal Q1/Q2, 2023–2026, peer-review, chính thức) mà có liên quan trực tiếp đến anomal detection trong log:

| **Candidate (Phương pháp)** | **Year** | **Journal** | **Q1/Q2 (Nguồn)** | **Official Pub** | **OpenSource** | **Repo Quality** | **RAG Fit** | **Problem Fit** | **Performance** | **Reproducibility** | **Architecture Clarity** | **Limitation Evidence** | **Improvement Potential** | **Feasibility** | **Baseline Suitability** |
|---|:---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **LogSentry** (Contrastive+RAG) | 2025 | Scientific Reports | Q1 | ✔ Yes (DOI) | – (no repo found) | N/A | **Strong** (có retrieval KNN) | High (direct log anomaly) | High (F1 cao) | Medium/Low (k cần code) | Medium (đề rõ BERT+KNN) | Imbalance, KNN latency (paper ghi *imbalance remains*) | High (có thể cải thiện retrieval bằng KG/GPT, giảm false positives) | Medium (BERT fine-tune + KNN khả thi) | **Good** (đã dùng RAG, có evidence F1 cải thiện) |
| **Sentiment-Aware Transformer** | 2026 | Scientific Reports | Q1 | ✔ Yes | – | N/A | **Moderate** (có thể bổ sung retrieval sentiment lexicon) | Medium (log-level, hạn chế chuỗi) | Very High (F1~99.96% in-domain) | Low (không công bố code) | High (kiến trúc rõ: BERT-ITPT-FiT + SHAP) | Chỉ nhìn log đơn lẻ | Moderate (thêm context retrieval hoặc dùng GRU on log sequence) | Medium | Good (hiệu suất cao, Q1, interpretable) |
| **LogFiT (BERT fine-tune)** | 2024 | IEEE TNSM | Q1 | ✔ Yes (DOI) | – | N/A | **Moderate** (có thể kết hợp retrieval logs) | High (chính xác log anomaly) | *Not publicly reported* (likely competitive) | Low | Medium (Dựa BERT, pipeline rõ ràng) | Dựa log patterns, cần fine-tune mới, thiếu knowledge external | High (có thể thêm vector store), but unverified | Medium | Moderate (Q1, nhưng info công bố ít) |
| **LogCEM (CNN+RoBERTa+GRU)** | 2024 | Computers, Materials & Continua | Q2 | ✔ Yes (DOI) | – | N/A | **Weak** (không đề retrieval) | Medium (tập trung DNN, chưa thử domain khác) | High (báo cáo outperform baseline) | Low | High (mô tả hybrid CNN+GRU) | Phụ thuộc RNN, domain-general không rõ | Moderate (có thể thay RNN bằng attention, thêm RAG) | Medium | Acceptable (Q2, kiến trúc thú vị, nhưng RAG kém) |

**Ghi chú:**  
- *RAG Fit:* Phân loại tiềm năng RAG cải thiện hạn chế.  
- *OpenSource/Repo:* Tìm kiếm công khai không thấy mã nguồn chính thức cho các phương pháp trên. Điều này kéo xuống khả năng tái lập.  
- *Limitation Evidence:* Từ nội dung và đánh giá paper (xem phân tích).  
- *Improvement Potential:* Đề xuất sơ bộ (thí dụ: thêm retrieval, memory, domain adaptation).  

Dựa trên bảng, **LogSentry (Sci Rep 2025)** và **Sentiment-Aware (Sci Rep 2026)** nổi bật với F1 rất cao và kiến trúc hiện đại (BERT/Transformer). Cả hai đều Q1 và chính thức. *LogSentry* tích hợp retrieval, thuận lợi cho RAG, trong khi *Sentiment* đạt F1 rất tốt nhưng thiếu bối cảnh. *LogFiT* (TNSM 2024) đủ điều kiện Q1 nhưng thông tin hạn chế. *LogCEM* Q2 là lựa chọn khả thi nữa. 

# 4. Phân tích Thành phần Baseline  
Bảng dưới đây so sánh chi tiết các bước chính của mỗi baseline đã chọn (LogSentry, Sentiment, LogFiT, LogCEM), xác định điểm mạnh/yếu và bằng chứng (trích từ bài):

| **Component** | **LogSentry (Sci Rep 2025)** | **Sentiment Model (Sci Rep 2026)** | **LogFiT (TNSM 2024)** | **LogCEM (CMC 2024)** |
|---|---|---|---|---|
| **Parsing/Preprocessing** | Log parsed thành các *log-key sequence* (cấu trúc cặp key-value) | *Parser-free*: không parse, dùng trực tiếp bản ghi log raw | Thường cần log parser (template extraction) để tạo đầu vào cho BERT | Yêu cầu parse theo template rồi tách ra message để embedding (RoBERTa dùng text) |
| **Representation (Embedding)** | Dùng **BERT-base** mã hóa key-value pairs (phù hợp chuỗi ngữ nghĩa) | Dùng **BERT-ITPT-FiT** để embedding câu log, do logs có tính “ngôn ngữ tự nhiên” (đã pre-train NLP) | Dùng BERT (fine-tune) cho chuỗi log. Có thể embedding log template n-gram | Dùng **RoBERTa** trích vector từ từng từ trong template. Kết hợp SIF và MSCNN/ECA để tạo vector sequence |
| **Sequence/Context** | Xem xét sequences log theo **cửa sổ thời gian cố định**; dùng RNN (nếu có) hoặc chỉ xem riêng từng sequence | *Không có* chuỗi: phân tích từng log độc lập (phù hợp realtime) | Xem theo window, BERT xử lý tuần tự từng entry, chưa rõ mechanism sequence | RNN (Mogrifier GRU) nhận chuỗi log vector (sau CNN), ưu điểm bắt pattern local + global nhưng giới hạn độ dài |
| **Retrieval/Knowledge** | **Yes (KNN)**: Lưu feature vector và nhãn của logs huấn luyện, truy vấn KNN trong inference. *Không dùng external KB.* | **No**: Chỉ dựa trên model. Không có cơ chế truy vấn văn bản hoặc mẫu logs tương tự. | **No**: Model thuần focus prediction, không memory. | **No**: Không sử dụng retrieval, chỉ xử lý diễn dịch nội tại. |
| **Memory/Reasoning** | *Không thiết lập bộ nhớ dài hạn* hay reasoning multistep; chỉ dùng weighting mixture (model + retrieval). | Không có: quyết định từng log; Lặp lại BERT và giải thích bằng SHAP. | Không có memory. Quyết định trực tiếp từ fine-tuned BERT. | Không có. Kết quả trực tiếp từ MLP trên GRU, không tracking state ngoài. |
| **Anomaly Scoring** | Dự báo nhãn (0/1) từ mô hình BERT + *weighted* kết quả KNN (mixture of experts). Kết hợp: Score = α·BERT + β·(điểm KNN). | Dự báo anomaly/normal (binary) với threshold (Softmax). Model mở RNN output hoặc dùng threshold softmax. | Dự đoán nhãn từ BERT fine-tune classification (sigmoid/softmax). | Dự đoán anomaly dựa classifier trên output của hybrid CNN+GRU. |
| **Threshold/Decision** | Ngưỡng mặc định >0.5 hoặc weight α,β (mixture) mặc định. (Không có điều chỉnh RAG-specific) | Ngưỡng 0.5 (nhị phân). Không tune hoặc adaptive threshold đề cập. | Tương tự: threshold cố định, chỉ dựa xác suất model. | Tương tự: xác suất đầu ra. |
| **Training/Fine-tuning** | BERT pre-train sau đó fine-tune với contrastive learning (tách similar/dissimilar pairs) và supervised classification. Dữ liệu huấn luyện chuẩn (HDFS, BGL). | Mô hình BERT pre-train + Fine-tune sentiment classification (điều chỉnh với label anomaly). Có thêm giai đoạn in-task pre-training. | BERT pre-train + fine-tune binary classification. Cần nhiều data cân bằng (thường sử dụng oversampling). | Huấn luyện riêng từng module (RoBERTa+SIF tính vector, huấn luyện CNN+GRU cuối cùng với crossentropy). Hướng đến general classification. |
| **Inference** | Cho logs mới: trích feature (BERT), áp dụng KNN với KB, tính weighted sum. Must compute vector + truy vấn KNN (có thể chậm). | Cho log mới: lấy embedding BERT, classification, sau đó tính SHAP sub-token, map sang word scores. Chậm do SHAP nhưng offline interpret. | Cho log mới: BERT inference và dự đoán. Relatively nhanh trừ chi phí BERT. | Cho log mới: RoBERTa embedding + chạy qua CNN+GRU. Tương đối chậm do RNN tính tuần tự. |
| **Feedback/Update** | Không đề cập (offline). Nếu có log mới thì cần retrain/gia huấn luyện. | Không (offline); không có cập nhật online. | Không (offline). | Không (offline). |

**Đánh giá:**  
- *LogSentry* kết hợp Contrastive Learning và KNN-Retrieval mang lại F1 cao. Điểm mạnh là hỗ trợ nhãn từ cây tri thức chứa embedding (improve recall/precision). Nhược điểm: yêu cầu lưu trữ toàn bộ vector logs, tính toán KNN trên tập huấn luyện lớn có thể kém hiệu quả. Bên cạnh đó, kỹ thuật contrastive cải thiện representation, nhưng không giải quyết được *anomaly imbalanced*. Bộ mix (BERT+KNN) là đóng góp chính.  
- *Sentiment* tập trung phân tích nội dung log tại dòng, với cơ chế explainability nhờ SHAP. Mô hình linh hoạt với định dạng log khác nhau (parser-free). Tuy nhiên, nó **bỏ qua thông tin chuỗi**. Do đó, bất thường phụ thuộc thứ tự các log (collective anomalies) sẽ bị bỏ lỡ. Mô hình dễ hiểu và có hiệu suất rất cao trên tập đơn lẻ nhưng hạn chế khi xử lý luồng log liên tục.  
- *LogFiT* (mô hình BERT) phần lớn như mô hình phân loại nhị phân, thiếu cả retrieval lẫn reasoning. Nó có thể mạnh về semantic của log nếu fine-tuned đủ, nhưng độ rõ ràng kiến trúc ít hơn (không public code) và thiếu evidence so sánh chi tiết, điểm hạn chế cũng khó xác định.  
- *LogCEM* (CNN + RoBERTa + GRU) là mô hình hybrid phức hợp, khai thác cả đặc tính cục bộ (CNN) và ngữ cảnh (GRU). Điều này có thể tăng độ chính xác (theo báo cáo), nhưng cũng rất nặng nề tính toán. Mô hình đã chứng minh vượt các phương pháp trước, song nhược điểm: sức mạnh RNN giới hạn bối cảnh, cần training nhiều, và thiếu cơ chế knowledge ngoài.

# 5. Giả định Chung của Các Paper  
Phần lớn phương pháp trong mapping đều dựa trên những giả định tiêu chuẩn sau:

- **Logs đã được parse**: Hầu hết giả định log đã được chuyển thành dạng template/text mạch lạc. Ví dụ, các mô hình như *LogCEM* sử dụng tokenization (GloVe/RoBERTa) cho từng từ trong template. Hiếm có mô hình học trực tiếp raw logs mà không parsing (Sentiment).

- **Dataset cố định, offline**: Sử dụng các benchmark chuẩn (HDFS, BGL, Thunderbird, Spirit). Quy trình huấn luyện/offline, không tính drift hay streaming. Hậu quả: mô hình đánh giá được qua F1, não lệ thuộc giả định train/test cùng phân phối.

- **Anomalies hiếm (imbalanced)**: Mặc dù chưa áp dụng kỹ thuật cân bằng (LogSentry giải quyết một phần bằng contrastive learning), hầu hết giả định số điểm bất thường ít hơn rất nhiều so với bình thường (như thực tế các tập HDFS/BGL).

- **Không có external knowledge/retrieval/memory**: Hầu hết giả định chỉ dựa vào tập dữ liệu hiện tại. Ngoại trừ LogSentry dùng nội dung từ chính train set làm “knowledge store” (KNN), hiếm khi sử dụng tài liệu, log lịch sử ngoài.

- **Context cố định/quãng ngắn**: Giả định các cột window log đủ chứa thông tin anomaly. Ví dụ, LogSentry xem logs theo time windows nhất định; Sentiment coi riêng từng log.

- **Nhãn ổn định**: Giả định dữ liệu huấn luyện có nhãn chuẩn xác và phù hợp, không xem xét drift nhãn hoặc yêu cầu online updating.

Những giả định này giúp thiết kế mô hình nhưng cũng là **hạn chế** trong thực tế: sản xuất logs thường streaming, có concept drift, dữ liệu đa dạng, yêu cầu phát hiện sớm và thích ứng liên tục.  

# 6. Hạn chế Chung (Có chứng cứ)  
Từ các baseline và xu hướng chung, có thể phân nhóm hạn chế:

- **Foundation Model**: 
  - *Hallucination/Domain mismatch:* BERT/Transformer tiền huấn luyện dựa trên văn bản tự nhiên, đôi khi *không học* được hết pattern kỹ thuật trong logs (dấu, số, cấu trúc cụ thể). Ví dụ Sentiment dùng BERT mà không parse, có thể **mất thông tin nhãn quan trọng**. Khả năng hallucinant (sai lệch ngữ nghĩa khi gặp log lạ) không được kiểm chứng.
  - *Prompt sensitivity:* Nếu áp dụng LLM (chuẩn future work), khả năng phụ thuộc prompt/tuning chưa rõ.
  - *Token limit:* Các mô hình Transformer tiêu chuẩn có giới hạn 512 tokens. Nếu log entry dài, có thể bị cắt/truncate, mất context. (Không có paper đề cập nhưng đây là giới hạn chung của BERT).
  - *Inference cost/Latency:* Tất cả dùng large models (BERT/RoBERTa) đều có chi phí tính toán cao, latency không tối ưu cho realtime. Không paper nào đề cập giải quyết vấn đề này.
  - *Stable reasoning:* Mô hình đầu ra có xu hướng thay đổi khi huấn luyện với dữ liệu khác; thiếu cơ chế đảm bảo kết quả ổn định với dữ liệu log mới.

- **Retrieval**: 
  - *Chất lượng retrieval:* LogSentry dùng KNN dựa trên embedding. Nếu embedding không tách bạch tốt, retrieval đưa nhầm nhãn, gây false positives. 
  - *Embedding mismatch:* Lỗi khi embedding của log mới lệch so với tập train (domain shift), KNN đánh giá sai.
  - *Stale knowledge:* Nếu tập train chưa cover trường hợp lạ, KNN bộ nhớ không hữu ích. Model không cập nhật online.
  - *Irrelevant context (context pollution):* Nếu KNN lấy log không liên quan (embedding mơ hồ), làm nhiễu kết quả.
  - *Latency/Scalability:* KNN trên hàng chục ngàn vector, đặc biệt với BERT, rất tốn thời gian. Không thấy đánh giá.

- **Kiến thức (Knowledge)**: 
  - *Thiếu/Kém hiện đại:* Không tận dụng logs lịch sử, incident reports, tài liệu kỹ thuật, v.v. Giả sử một anomaly lặp lại nhiều lần, mô hình không nhớ/truy xuất kinh nghiệm cũ.
  - *Outdated:** Data huấn luyện chỉ tại một thời điểm; không có cập nhật tự động khi system log format mới xuất hiện.
  - *Misaligned/noisy:* Nếu dùng thêm knowledge (chưa thấy trong các paper), việc alignment log với knowledge graph phức tạp, lỗi có thể nhiễu detection.

- **Temporal/Context**: 
  - *Ngắn hạn:* Hầu hết window log rất ngắn (vd. LogSentry, 200 dòng ~ X giây). Anomaly kiểu diễn tiến dài có thể bị bỏ sót.
  - *Cross-window dependency:* Khi anomaly liên quan giữa nhiều window (trượt), hầu hết mô hình không nắm bắt được.
  - *Truncation:* Log dài bị cắt. (Chưa thấy minh chứng cụ thể, nhưng là giới hạn của tokenizer).
  - *Concept drift:* Không giải quyết adaptation khi cấu trúc logs thay đổi theo thời gian.

- **Dataset/Evaluation**:
  - *Benchmarks cũ, thiếu streaming:* HDFS/BGL/Thunderbird tập tĩnh, offline labeling. Không có đánh giá streaming hoặc time-to-detection. 
  - *Bias:* HDFS, BGL chỉ vài domain (Hadoop, HPC). 
  - *Synthetic anomalies:* Một số bất thường là injection thủ công (HDFS). Có thể không phản ánh đủ kịch bản thực.
  - *Production gap:* Không test logs thực từ hệ thống phức tạp (chưa thấy paper triển khai thực tế).
  - *Imbalance cao:* Mặc dù LogSentry đề cập imbalance, hầu hết bench có ~1-5% anomalies. Các mô hình thường phải tùy chỉnh để không bỏ quên anomalies.
  - *Offline-only metrics:* Thiếu các metric sớm như lead-time. Ai chỉ đánh F1 thì không chứng minh “early detection”.

Mọi hạn chế quan trọng trên đều có cơ sở từ đặc điểm của các phương pháp hiện tại (hoặc từ khái niệm chung). Ví dụ, LogSentiment chỉ phân tích dòng đơn (thiếu context, chỉ có threshold detection), LogSentry nhận biết imbalance nhưng “vẫn chưa giải quyết”. Các mô hình không đề cập early-warning, do đó “early detection” không thực sự được chứng minh. 

# 7. Phân tích Đặc thù Early Detection  
**Phân biệt mục tiêu:** *Anomaly detection* thông thường (phát hiện bất thường khi nó đã xảy ra); *Early anomaly detection* (còn gọi early warning) đòi hỏi phát hiện trước khi vấn đề hoàn thiện. Các baseline hiện không rõ yêu cầu sớm.  
- **Phương pháp**: Tất cả phương pháp trên tập trung classification (anomaly/normal) hoặc chẩn đoán (sentiment, giải thích từ ngữ). Không có phương pháp nào báo cáo metric sớm (lead time, time-to-detect).  
- **Các phép đo phù hợp Early Detection**: Detect Lead Time, Time-to-Detect, Mean Time to Detect, Early Warning Horizon… Hầu hết các báo cáo Q1/Q2 chỉ dùng Precision/Recall/F1. Chẳng hạn, LogSentry chỉ báo F1 trên HDFS/BGL, không đo thời gian phát hiện.  
- **Kết luận Early?** Không có bằng chứng trực tiếp. Việc dùng F1 cao không đồng nghĩa model “phát hiện sớm”. Vì vậy, bất kỳ tuyên bố nào rằng những phương pháp này là *“early detection”* đều không được chứng minh. 

# 8. Xác thực Bằng chứng  
Một số khẳng định tiềm năng và loại bằng chứng liên quan:

| **Claim** | **Bằng chứng** | **Paper hỗ trợ** | **Trái ngược** | **Độ tin cậy** |
|---|---|---|---|---|
| BERT-based models (LogSentry, Sentiment) đạt F1 rất cao. | Đã trích dẫn F1 lên đến 99.96% (in-domain) cho Sentiment; LogSentry F1 cao hơn phương pháp trước. |  | Không tìm thấy báo cáo F1 thấp cho cùng bộ dữ liệu; tuy nhiên, không có so sánh với mọi phương pháp dẫn đầu (e.g., LogRobust chỉ show precision). | Cao |
| Retrieval (KNN) giúp cải thiện precision. | LogSentry báo rằng model + KNN weighted giảm false positives: “LogSentry đạt precision cao hơn except LogRobust”. |  | Không thấy thử nghiệm thay KNN khỏi pipeline. Nhưng LogSentry có hai bản: pre-train vs pre-train+retrieval; phiên bản đầy đủ (with KNN) cho recall và precision tốt hơn. | Trung bình |
| Sentiment model giải thích được quyết định nhờ SHAP. | Bài đưa ra mapping từ subword SHAP đến word-level tại phần explainability. Kết quả rất trực quan (ví dụ negative words → anomaly). |  | Chưa có đối chứng, nhưng giải thích SHAP có nhược: có thể nhiễu nếu log chứa từ chung (ví dụ “error” bình thường trong báo cáo). | Trung bình |
| Hybrid CNN+GRU trong LogCEM tăng khả năng bắt pattern (outperform baseline). | Kết quả thí nghiệm chứng minh LogCEM “outperforms current mainstream methods”. |  | Không có đánh giá cụ thể về mỗi thành phần CNN/GRU; nên khó khẳng định phần nào hiệu quả thật. | Trung bình |

Độ tin cậy phản ánh sự chắc chắn (dựa vào số liệu công bố hay thí nghiệm cụ thể). Các kết luận dựa trên báo cáo nội dung paper là độ tin cậy cao nếu đã có dữ liệu trực tiếp (F1, bảng so sánh). Bất kỳ inference nào thiếu dữ liệu (ví dụ, cải thiện early detection) thì tin cậy thấp và chỉ để gợi ý thảo luận.

# 9. Mapping: Baseline → Limitation → Cơ hội cải tiến  

| **Baseline** | **Hạn chế đã xác nhận** | **Bằng chứng** | **Technique hiện tại / Related** | **Cơ hội cải tiến** | **Expected Effect** | **Risk** | **Độ tin cậy** |
|---|---|---|---|---|---|---|---|
| **LogSentry (Sci Rep 2025)** | Giới hạn bối cảnh: chỉ window ngắn, không dùng kiến thức ngoài | Paper thừa nhận *“issues: variability of logs, imbalance”* nhưng không giải quyết drift/mới format. Hơn nữa, KNN retrieval chỉ trong bộ dữ liệu huấn luyện, không dynamic. | Sử dụng Contrastive BERT + KNN (retrieval). | - Thêm *external knowledge*: dùng RAG với mô hình LLM (ví dụ: chuỗi log như prompt hỏi mô tả lỗi), hoặc dùng knowledge graph logs để cung cấp ngữ cảnh. - Hoặc sử dụng mô hình nhánh “mixture of experts” thông minh hơn (ví dụ, một transformer dài hơn nạp cả log cũ). | Giúp phát hiện anomalies cần hiểu rộng hơn (qua gợi ý logs trước đó hay thông tin hệ thống). Có thể tăng recall với lead-time (phát hiện qua dấu hiệu sớm trong ngữ cảnh nhiều logs) và giải thích tốt hơn. | Complexity (cần xây KB, fine-tune lại), latency cao. Lại cần dữ liệu tri thức chuyên ngành. | Trung bình |
| **Sentiment Model (Sci Rep 2026)** | Chỉ xử lý log đơn lẻ; không bắt được pattern liên tiếp. Không có memory/history. | Mô hình chỉ đánh giá từng sự kiện riêng rẽ, không có cơ chế xem trước hay sau. Bản thân paper thừa nhận “individual log detection” phù hợp realtime nhưng nhấn thiếu dependence trên chuỗi. | Đã dùng BERT-ITPT-FiT + SHAP, không liên kết chuỗi. | - Mở rộng khả năng cắm thêm RNN hoặc Transformer layers để xử lý chuỗi (phiên bản “sentiment sequence”). - Hoặc dùng RAG: khi một log được phân loại, truy vấn similarity với logs lịch sử để tăng/giảm độ tin cậy. | Bổ sung context để bắt anomalies diễn tiến (cải thiện detection của anomaly dạng collective). RAG có thể hỗ trợ giải thích: “log này có sentiment giống với log từng bị phát hiện trước kia”. | Mô hình phức tạp hơn, dễ gây overfitting chuỗi logs, latency tăng. | Trung bình |
| **LogFiT (TNSM 2024)** | Không có retrieval/ kiến thức; phụ thuộc training set. Có thể thiếu khả năng generalize chuỗi/format mới. | Không có phân tích chi tiết, nhưng theo logic, fine-tune BERT chỉ mạnh với patterns quen thuộc. Chưa đề cập đến external data. | BERT fine-tune classification. | - Thêm module lưu trữ: *vector store* của logs (theo kiểu RAG) để khi gặp log mới, so sánh với lịch sử. - Hoặc áp dụng RAG: Hỏi BERT một câu hỏi contextual (ví dụ “Đây có phải phân đoạn bất thường?”) sử dụng prompt dựa trên logs tương tự từ KB. | Cải thiện phát hiện cho logs lạ bằng truy cập kiến thức history. Giảm false negative khi gặp pattern hơi khác. | Phức tạp triển khai RAG, cần prompt/tuning. | Thấp (chưa rõ minh chứng) |
| **LogCEM (CMC 2024)** | Quá nặng, chỉ dùng model cố định. Thiếu retrieval/domain adaptation. | Bài báo không đề cập hạn chế rõ, nhưng cấu trúc có thể overfit quan sát hiện tại. | CNN + GRU xử lý chuỗi local. | - Thay GRU bằng mô hình Transformer dài (cho context lớn hơn). - Hoặc kết hợp RAG: Nếu log lạ, truy vấn cơ sở template logs để hỗ trợ quyết định. | Xử lý dữ liệu dài tốt hơn, phát hiện sớm tốt hơn nếu dùng Transformer (long-range). RAG có thể thêm ngữ nghĩa ngoại lai. | Thử biến kiến trúc cốt lõi, mất đơn giản. | Trung bình |

**Đánh giá sơ bộ:** Hầu hết cơ hội tập trung vào **bổ sung RAG/kiến thức** cho baseline hiện tại, đặc biệt LogSentry và LogFiT để khắc phục thiếu context. Các cải tiến đều có thể tăng khả năng phát hiện (nhất là recall, khả năng xử lý logs mới) và giải thích. Tuy nhiên, chúng làm tăng độ phức tạp, latency và yêu cầu thêm dữ liệu tri thức.

# 10. Xếp hạng Hướng Cải thiện  
Đánh giá các hướng cải tiến tiềm năng, dựa trên các hạn chế có chứng cứ:

| **Improvement** | **Evidence** | **Impact** | **Novelty** | **Feasibility** | **Evaluation Ease** | **Complexity** | **Risk** | **Overall** |
|---|---|---|---|---|---|---|---|---|
| **Thêm RAG (Knowledge Retrieval) cho LogSentry** (kết hợp external KB/log memory) | Hạn chế: không có external context, KNN chỉ trong dữ liệu huấn luyện. RAG có thể trực tiếp giải quyết thiếu context. | Cao: Có thể tăng recall (bắt anomalies dựa trên ngữ cảnh rộng hơn) và độ tin cậy (dựa trên logs lịch sử). | Cao-medium: Ý tưởng kết hợp LLM+retrieval vào log anomaly chưa nhiều; là hướng mới. | Medium: Cần xây KB, fine-tune LLM hoặc query kiểu vector search. Kĩ thuật có sẵn (hay dùng ElasticSearch, FAISS). | Medium: Dễ kiểm thử trên cùng tập (so sánh F1). Tuy nhiên cần tạo KB (logs lịch sử). | Tăng lớn: Xây dựng KB, cài vector store, kết hợp LLM prompt. | Medium-high (phức tạp, latency, tính khả thi depends on KB) | **High** (có bằng chứng cần, tác động rõ) |
| **Mở rộng Sentiment model thành sequence model hoặc RAG** | Hạn chế: chỉ xét log đơn, thiếu thông tin liền kề. | Trung bình: Bổ sung RNN/Transformer hoặc sử dụng retrieval có thể bắt anomalies cần bối cảnh, nhưng Sentiment vốn đặt biệt về từng log, cải tiến có thể không tăng F1 nhiều trên nghiệm thu ban đầu (đã rất cao). | Medium: Kết hợp sentiment analysis với RAG ít thấy, cũng mới mẻ. | Medium: Thêm RNN transformer không khó, nhưng tích hợp LLM+retrieval đòi hỏi datasets phù hợp. | Medium: Có thể đo bằng độ tăng precision/recall trên dataset có anomalies liên kết. | Cao: Thêm RNN/LLM, tinh chỉnh, nhiều tham số. | Medium | **Medium** (tác động rõ hạn chế, nhưng hiệu quả thực tế chưa rõ) |
| **Memory replay for LogFiT** (lưu embedding logs, hoặc cập nhật incremental learning) | Hạn chế: thiếu memory, domain shift. | Trung bình: Ghi nhớ logs cũ, cập nhật incremental giúp bền vững khi log thay đổi, nhưng cần thiết tập anomaly thật. | Thấp-medium: Ý tưởng tương tự replay hay fine-tune incremental đang được dùng trong ML, không hoàn toàn mới. | Medium-high: Cần kỹ thuật continual learning trên BERT hoặc vector store + monitoring. | Low-medium: Phát triển và đánh giá đòi hỏi pipeline phức, ít công cụ sẵn. | Cao: Continual learning phức tạp, dễ quên. | Low-medium | Low (không cụ thể đủ evidence) |
| **Transformer dài (Longformer) thay GRU cho LogCEM** | Hạn chế: GRU giới hạn context, truncation. | Cao: Long context có thể bắt pattern dài, giúp early detection. | Medium: Longformer trong anomaly mới, nhưng ý tưởng đã có trong NLP rộng. | Medium: Thay nhân GRU bằng Longformer dễ về mặt code, nhưng cần nhiều dữ liệu. | Medium: So sánh F1/lead-time trước/sau dễ đo. | Cao: Training transformer lớn phức tạp, cần GPU lớn. | Medium | Medium |
| **Graph Neural Network on logs** (bao gồm knowledge graph) | Hạn chế: thiếu knowledge context, không dùng cấu trúc. | Cao: Có thể nắm mối quan hệ giữa sự kiện (log templates) để phát hiện bất thường phức tạp. | Cao: Kết hợp log anomaly + GNN là tương đối mới. | Low: Cần xây cấu trúc log graph/hierarchy và dataset có annotated graph. | Low: Rất khó thu thập data, đánh giá phức tạp. | Rất cao: Khó dựng graph logs thực; overhead thời gian cao. | Low | Low-medium |

Ưu tiên cải tiến **RAG cho LogSentry** là cao nhất (bằng chứng hạn chế rõ, tác động lớn, khả thi trong scope luận văn). Hướng **sentence model → sequence/RAG** cho Sentiment ở mức trung bình (có evidence, nhưng khó đảm bảo nâng cao đáng kể). Các hướng khác có evidence thấp hoặc rủi ro cao. 

# 11. Cơ hội Nghiên cứu (Evidence-based Gaps)  

Dựa trên phân tích trên, các gap có thể:

| **Gap** | **Baseline** | **Evidence** | **Nguyên nhân** | **Ảnh hưởng** | **Related Work** | **Partial Solutions** | **Improvement Opp.** | **Tin cậy** |
|---|---|---|---|---|---|---|---|---|
| **1. Thiếu ngữ cảnh dài hạn (temporal)** | LogSentry, LogSentiment, LogCEM | Mọi mô hình đều giới hạn cửa sổ/độ dài ngắn. | Thiết kế model chỉ xử lý chuỗi nhỏ (RNN hay độc lập). | Giảm khả năng phát hiện anomalies phụ thuộc sequence; không thể cảnh báo sớm. | Time-series anomaly models (CNN, LSTM) chưa áp dụng cho log riêng. | Một số công trình log anomaly dùng RNN nhưng không đối thủ Q1 mới. | **Thử Transformer dài hoặc RAG về logs history**. | Cao |
| **2. Không dùng kiến thức ngoài (knowledge)** | LogSentry | LogSentry chỉ dùng feature KNN từ tập huấn luyện, không tham chiếu external. Sentiment, LogCEM tương tự. | Tập data hạn chế, thiếu KB. | Model dễ bị thua khi gặp logs mới, mất khả năng explain. | Các công trình AI-Augmented (RAG trong tổng quan LLM) hứa hẹn. | RAG thuần. | **Tích hợp RAG/KG**: RAG chatbot cho log; Graph logs. | Cao |
| **3. Không đánh giá Early Detection** | Tất cả | Không thấy metric sớm nào. | Dữ liệu offline, thiếu benchmark sớm. | Thiếu chứng cứ, model có thể “bị động” chỉ phát hiện khi anomaly đã xảy ra. | Work IoT anomaly detection có lead-time metric. | Thường xử lý sao? | **Xây benchmark/metrics**: lấy logs có sự kiện biết trước, tính time-to-detect. | Trung bình |
| **4. Tính tái lập hạn chế (reproducibility)** | Tất cả Q1/Q2 | Không có source code chính thức; khó tái tạo. | Nhu cầu công bố, nhưng nhiều tác giả không cung cấp code. | Gây khó khăn xác nhận kết quả, phát triển tiếp. | MITAC (model zoo), OpenAI code share... | Tăng độ minh bạch. | **Yêu cầu open source**: Nghiên cứu khả năng tái lập như yêu cầu. | Cao |
| **5. Adaptation với drift** | LogFiT | Chưa thấy đề cập incremental learning hoặc domain adaptation. | Hạn chế train/test ổn định, logs thay đổi. | Model nhanh lỗi thời, hiệu suất giảm khi chuyển domain. | Transfer learning (LogFormer ACE 2025) [arXiv]. | Domain adaptation chung. | **Continual Learning/RAG**: Thêm cơ chế học liên tục, hoặc RAG truy vấn log mới. | Thấp |

Các gap trên được ưu tiên dựa trên bằng chứng: Gap 1 & 2 rất rõ (dựa vào cấu trúc mô hình, dữ liệu). Gap 3 là thiếu của toàn ngành, cần tự tạo benchmark. Gap 4,5 chủ yếu lưu ý reproducibility/adaptability.

# 12. Định vị Nghiên cứu  
- **Reimplementation:** Không cần (đã có mã, chỉ cần phân tích).  
- **Cải tiến Đặc thù (Targeted Improvement):** Ưu tiên. Ví dụ: “bổ sung RAG” cho baseline *LogSentry* hoặc *Sentiment*. Làm rõ cách RAG khắc phục limitation và thực nghiệm chứng minh hiệu quả.  
- **Mở rộng Rộng (Broader Extension):** Thay đổi quá nhiều (thêm multi-agent, kiến trúc hoàn toàn mới) không phù hợp scope thạc sĩ.  

Chú ý sử dụng các thuật ngữ “improve/augment”, tránh tạo method hoàn toàn mới. Hướng nghiên cứu nên kế thừa baseline hiện có và tập trung giải quyết bottleneck đã chứng minh.

# 13. Ma trận Khả năng (Traditional vs Transformer/LLM/RAG)  

| **Capability** | Traditional DL (CNN/RNN) | Transformer (BERT) | Domain LLM | RAG | Agentic AI |
|---|---|---|---|---|---|
| **Semantic Understanding** | Trung bình (khó khai thác meaning log templates) | Tốt (BERT học embedding ngữ nghĩa) | Rất tốt (LLM hiểu văn bản) | Kém/Tùy retrieval (cần content) | N/A |
| **Anomaly Detection** | Tốt trong pattern nhất định (PCA, CNN chặn ngắn) | Rất tốt (theo nhiều báo cáo SOTA) | Có thể, nếu được fine-tune | Cải thiện recall (dựa memory) | N/A |
| **Early Detection** | Yếu (offline) | Yếu (hầu hết offline) | Yếu (chưa nghiên cứu) | Giúp về recall nhưng chưa đo sớm | Có thể (agent có thể proactive) |
| **Generalization** | Trung bình (phải train lại domain mới) | Tốt (transfer learning) | Xuất sắc (pretrained rộng) | Tốt nếu có KB phong phú | Có (tự học) |
| **Explainability** | Thấp (đen-box) | Thấp (phải thêm SHAP hoặc attention) | Thấp | Trung bình (có thể giải thích via retrieved docs) | Cao (giải thích qua reasoning steps) |
| **Retrieval** | Không có | Không (trừ embed-based search) | Không (thường) | Rất tốt (mã hóa retrieval) | Có thể (multi-tool agents) |
| **Reasoning** | Rất yếu (không chain-of-thought) | Rất yếu (deterministic model) | Tốt (LLM chuỗi suy luận) | RAG có thể hỗ trợ reasoning bằng external text | Có (multi-step planning) |
| **Temporal/Context** | Thấp (giới hạn window RNN) | Tốt (self-attention wide) | Tốt nếu prompt lịch sử | Tốt (context từ docs) | Tốt (giả sử agent ghi nhớ) |
| **Scalability** | Khó (CNN/RNN nặng, không xén context) | Khó (Transformer chậm, tốn bộ nhớ) | Rất khó (LLM yêu cầu lớn) | Khó (vector store lớn, retrieval) | Rất khó (nhiều components) |
| **Industrial Readiness** | Cao (dễ kiểm soát, hiện hữu) | Trung bình (phải thiết lập Pipeline ML) | Thấp (mới, rủi ro) | Thấp (hiếm hệ thống ứng dụng RAG) | Thấp (chưa có triển khai thực tế lớn) |

Bảng trên chỉ mang tính tham khảo. Ví dụ, semantic understanding của RAG/LLM cao, nhưng cần dữ liệu phù hợp. Agentic AI chưa xuất hiện trong paper nên để **N/A**.

# 14. Benchmarks và Tính Thực Tiễn  
Phổ biến nhất: **HDFS (Hadoop)**, **BGL (BlueGene/L)**, **Thunderbird (HPC)**. Đã có Spirit (Máy tính Google, có sẵn data). Tất cả các dữ liệu này:
- **Quy mô**: Trung bình (HDFS: ~11M dòng, BGL: ~4M). Lớn so với labs, nhỏ vs. data thực tế. 
- **Loại anomaly**: HDFS chủ yếu point anomaly (điểm lẻ do lỗi). BGL cũng phần lớn point anomalies. Thiếu anomalies logic phức tạp (ví dụ drift).
- **Mất cân bằng**: Tỷ lệ anomaly rất nhỏ (HDFS ~2%, BGL ~1%), như thực tế logs.
- **Tính thời gian**: Dữ liệu có timestamp nhưng phần lớn đánh giá offline (bỏ qua lead time). 
- **Thực thế**: HDFS/BGL là logs phần cứng, trong khi ứng dụng công nghiệp rộng hơn có logs system, cloud, thiết bị IoT, microservices. Sự đa dạng thiếu trong benchmarks.
- **Lọc truất**: Một số logs đã được parse (N-gram) cho thuận tiện.
  
Kết luận: Các benchmark này phù hợp cho test anomaly detection cổ điển (mức độ, recall, precision). Tuy nhiên, thiếu realism về streaming, real-time và cross-domain. Cần xem xét bổ sung dataset mới hoặc metrics “early detection” để đánh giá cải tiến.

# 15. Tổng hợp

- **Best Baseline Candidate:** *LogSentry* (Scientific Reports 2025). Lý do: Q1, chính thức, kết hợp Contrastive+BERT với retrieval, báo cáo F1 cao, có sẵn DOI, có khả năng mở rộng RAG. Ngoài ra *Sentiment-aware Transformer* (Sci Rep 2026) là đối thủ mạnh (F1 ~99.96%, Q1) nhưng hạn chế về ngữ cảnh nên khó cải tiến early detection.  
- **Why This Baseline:** LogSentry đã giải quyết một số hạn chế (như imbalance) và dùng retrieval, nên phù hợp để bổ sung thêm RAG. Mô hình rõ ràng (BERT+KNN) giúp xác định bottleneck (lookup KNN, imbalance) và được minh chứng hiệu quả qua experiment.  
- **Confirmed Limitation:** Phát hiện rằng LogSentry vẫn thiếu **context/knowledge bên ngoài**; nó dựa trên feature space của tập huấn luyện (KNN), không có tri thức domain mở rộng. Ngoài ra, khả năng xử lý log với cấu trúc mới hoặc anomalies chuỗi dài còn hạn chế (hạn chế ngữ cảnh). Các hạn chế này được hỗ trợ bởi phân tích hiệu suất và thiết kế method.  
- **Improvement Opportunity:** Bổ sung RAG – cài một hệ thống *retrieval-augmented* thực thụ: Ví dụ, xây một vector store chứa **kiến thức logs lịch sử/dokument domain** và sử dụng LLM để truy xuất context cho log mới. Cụ thể, có thể huấn luyện một LLM (hoặc dùng GPT) fine-tune cho log domain để trả lời câu hỏi (Q&A) về log history liên quan. Điều này trực tiếp giải quyết **thiếu context/knowledge** và có khả năng nâng cao detection (đặc biệt anomalies phức tạp) và early warning.  
- **Supporting Evidence:** Hạn chế RAG đã được nhắc trong paper (thiếu context beyond KNN), và RAG đã chứng minh thành công trong các lĩnh vực tương tự (nlp classification). Mặc dù chưa có thử nghiệm, nhưng logic cho thấy việc “kết hợp thêm tri thức ngoài” có thể bổ sung cho decision của model. Ngoài ra, LogSentry có cải thiện nhờ retrieval đơn giản (KNN), gợi ý RAG thế hệ mới có thể tiếp tục xu hướng này.  
- **Expected Contribution Level:** Tiến hành một bổ sung có mục tiêu (level 2). Cụ thể, phát triển một module retrieval-augmented cho LogSentry – tức không thay đổi kiến trúc gốc mà mở rộng nó. Điều này tạo ra sự mới mẻ vừa phải (không kiến trúc hoàn toàn mới) và có thể công bố.  
- **Experimental Feasibility:** Trung bình: Cần xây dựng KB logs (dùng các tập hiện có và có thể thêm logs tổng hợp) và tích hợp hệ thống RAG. Cần compute resource cho LLM inference và lưu trữ vectors. Có thể test bằng các tập dữ liệu chuẩn (HDFS, BGL) để đánh giá cải thiện F1, precision, recall, và thêm lead-time metric. Nếu code LogSentry chưa public, cần implement lại baseline (time-consuming nhưng khả thi trong phạm vi luận văn). Tóm lại, **khả thi** nhưng có thách thức (khó ở việc cấu hình retrieval).  

**Key Findings:** Trong các bài báo Q1/Q2 giai đoạn 2023–2026, có xu hướng mạnh sử dụng Transformer/BERT cho anomaly detection trên log. Tuy nhiên, chúng thường giới hạn ngữ cảnh (window nhỏ, thiếu thông tin lịch sử) và chỉ dùng evaluation offline (F1). Các gap quan trọng bao gồm: (*1*) **Thiếu contextual/knowledge** (hầu hết không dùng RAG/knowledge graph), (*2*) **Thiếu đánh giá early detection**, và (*3*) **Tái lập hạn chế** (thiếu code). *LogSentry (Sci Rep 2025)* được chọn làm baseline tốt nhất (F1 cao, dùng retrieval) để tập trung cải tiến: hướng nghiên cứu là **bổ sung Retrieval-Augmented (RAG)**, dựa trên evidence limitation. Hướng này nhiều bằng chứng cho thấy khả năng tăng recall/explainability, và đạt yêu cầu (*evidence mạnh + limitation rõ + improvement hợp lý*). Quá trình thực nghiệm có thể tiến hành trong quy mô luận văn (xây KB, đo F1 và lead-time). Mức đóng góp được kỳ vọng là cải thiện rõ rệt khả năng phát hiện (sớm) với model đã được chứng minh trước đó. 

**Kết luận:** Baseline đề xuất là *LogSentry* (Scientific Reports 2025), và cải tiến hướng RAG (thêm external knowledge/retrieval cho anomaly detection). Bằng chứng từ các paper cho thấy cần giải quyết limitation về context/knowledge, và RAG là kỹ thuật phù hợp để bổ sung. Đây cũng là hướng có tiềm năng thực nghiệm trong thời gian luận văn, đồng thời đóng góp mới cho lĩnh vực Log Anomaly Detection. Trọng tâm là: **LogSentry (Q1, peer-reviewed 2025) → Confirmed Limitation (thiếu context/knowledge) → Improvement (RAG augmentation) → Expected impact (tăng recall/explainability, hỗ trợ early detection)**.