# Bản đồ tài liệu (2023–2026, chỉ Q1/Q2)  
Nhiều hướng nghiên cứu hiện tại trong **phát hiện bất thường log** tận dụng các mô hình học sâu và NLP tiên tiến. Các phương pháp nổi bật bao gồm các mô hình *Transformer/BERT* (ví dụ LogFiT, CLDTLog, LogEDL) và các kỹ thuật *contrastive/self-supervised* (CLDTLog, LogEncoder, v.v.). Gần đây xuất hiện xu hướng sử dụng **retrieval-augmentation** (LogSentry kết hợp BERT với KNN retrieval), **foundation models** (LogFiT fine-tune BERT) và **kiến thức đa miền/đa mô thức** (CoLog sử dụng nhiều modal log cùng lúc). Ví dụ, Catalán et al. (2026) đề xuất transformer tăng khả năng diễn giải và xử lý logs “không cần parser”. Ngoài ra, các khảo sát gần đây (được giới thiệu trên Springer Nature và Elsevier) tổng hợp các phương pháp log anomaly cũ (DeepLog, LogRobust, LogBERT, LogContrast, AugLog, v.v.) đồng thời chỉ ra thách thức về **đa dạng định dạng logs** và **imbalance giữa dữ liệu bình thường và bất thường**. 

Xu hướng 2023–2026 cho thấy ưu thế của các mô hình ngôn ngữ lớn và Transformer trong phân tích log. Nhiều bài báo Q1/Q2 tập trung vào tận dụng BERT hoặc tương đương để trích xuất ngữ nghĩa (LogFiT, CLDTLog, LogEDL) hoặc học biểu diễn tương phản (contrastive learning) để tăng khả năng khái quát (CLDTLog, LogSentry). Một số công trình mới tích hợp **multi-modal** (CoLog) hoặc **giải thích được** (Catalán et al. 2026) vào phát hiện bất thường. Xu hướng chung là ưu tiên tính mở rộng, khả năng giải thích và khả năng vận hành quy mô lớn (thông lượng cao). Tuy nhiên, hầu hết các phương pháp chỉ báo cáo F1/Precision/Recall, chưa đánh giá đầy đủ khả năng *phát hiện sớm* (lead time hay detection delay).  

## Phân loại phương pháp  
Có thể phân nhóm các phương pháp theo hướng sau:
- **Machine Learning kinh điển**: PCA, SVM, Isolation Forest… (xem nền tảng cung cấp ngoại lệ cơ bản).  
- **Học sâu truyền thống (RNN/CNN/Autoencoder)**: Ví dụ DeepLog, LogAnomaly, các mạng LSTM/CNN dùng để học tuần tự log.  
- **Transformer/BERT**: LogFiT, LogBERT (ICML/TCS 2021), LogFormer, LogRobust. Các phương pháp này không dùng vocabulary đếm mà sử dụng mô hình ngôn ngữ mãn quyền để học ngữ nghĩa log.  
- **Mô hình lớn (Foundation Models/LLM)**: Sử dụng ngôn ngữ lớn, thường fine-tune cho log, ví dụ mô hình BERT-ITPT của Catalán et al. 2026.  
- **Contrastive/Self-supervised**: CLDTLog, AugLog, LogContrast, LogEncoder… – kết hợp học biểu diễn so sánh (triplet loss, focal loss, v.v.) để tăng khả năng phân biệt.  
- **Retrieval-Augmented (RAG)**: LogSentry (BERT + KNN retrieval) hay các đề xuất nghiên cứu LLM + truy vấn (LogRAG, RAGLog). Ý tưởng dùng bộ nhớ/VBert để hỗ trợ model chính.  
- **Đồ thị/ngữ nghĩa (Graph/KG)**: Một số công trình sơ khai dùng GNN cho log (Log2Graph kiểu BERT-GNN, hoặc kiến thức chuyên ngành chưa thấy Q1).  
- **Hệ thống tác nhân (Agent)**: Chưa thấy Q1/Q2 ứng dụng rõ ràng, chủ yếu xuất hiện trên workshop.  
- **Bộ nhớ/Ngữ cảnh mở rộng**: Các mô hình Transformer kéo dài ngữ cảnh, lưu trữ trạng thái qua session, phần lớn chưa áp dụng trong Q1/Q2 logs.  
- **Hỗn hợp (Hybrid)**: Kết hợp nhiều thành phần trên, ví dụ CoLog (đa modal) hay LogEDL (BERT + đầu mạng evidential).

## Phương pháp tiêu biểu Q1/Q2 (2023–2026)  
Một số công trình tiêu biểu công bố chính thức:
- **Skopik et al. (IEEE TDSC 2023)** – “Behavior-Based Anomaly Detection…” sử dụng biểu diễn thống kê chuỗi sự kiện của hệ thống kiểm soát ra vào. *Thứ hạng:* TDSC thường Q1. Xử lý logs vật lý, mô hình dựa trên baseline thống kê.  
- **Tian et al. (Sensors 2023)** – *CLDTLog* sử dụng BERT fine-tune kết hợp *contrastive learning* và bài toán hai mục tiêu để phát hiện anomaly. Thuật toán không cần parse logs, đạt F1~0.9999 trên BGL và 0.997 trên HDFS. (*Sensors* SCImago Q2).  
- **Almodovar et al. (IEEE TNSM 2024)** – *LogFiT* dùng BERT tự huấn luyện (masked sentence prediction) mà không cần nhãn, đánh giá bằng top-k accuracy. LogFiT vượt các baseline trên HDFS, BGL, Thunderbird với F1 cao hơn đáng kể. (TNSM Q1).  
- **Duan et al. (Appl. Sci. 2024)** – *LogEDL* (Applied Sciences, Q2) thay thế hàm mất mát Softmax bằng hàm mất mát evidential để định lượng độ tin cậy. LogEDL đạt SOTA, ví dụ F1=97.91% trên Thunderbird, bỏ xa các mô hình khác.  
- **Li et al. (Sci Rep 2025)** – *LogSentry* kết hợp BERT pre-train (contrastive learning) và KNN retrieval. Nghiên cứu này công bố trên *Scientific Reports* (Q1), mô tả khung huấn luyện-tổng hợp log và rút trích tương tự, đạt hiệu năng cao trên HDFS/BGL.  
- **Nasirzadeh et al. (Sci Rep 2025)** – *CoLog* dùng “collaborative transformers” xử lý logs đa-modal (nhiều nguồn log) trong các hệ thống lớn. CoLog đạt ~99.6% F1 trên 7 bộ dữ liệu, tập trung phát hiện anomalies theo điểm và tập hợp. (Sci Reports Q1).  
- **Catalán et al. (Sci Rep 2026)** – mô hình Transformer “sentiment-aware” giải thích được kết hợp SHAP. Đạt F1 ~99.96% (trong domain) và 96.97% (out-of-domain) trên các datasets.  

## Đề cử baseline (tuân thủ tiêu chí nghiêm ngặt)  
Xét tiêu chí (*2023–2026*, Q1/Q2, bài báo chính thức):
- **LogFiT (Almodovar et al., IEEE TNSM 2024)** – Q1 (IEEE TNSM), tự huấn luyện BERT, không cần nhãn, hiệu năng cao. Là mô hình mới (2024), kiến trúc rõ ràng, không phụ thuộc ngưỡng cứng ngoài top-k.  
- **LogSentry (Li et al., Sci Rep 2025)** – Q1 (Scientific Reports), Kết hợp BERT + retrieval, khắc phục imbalance, hiệu năng cao trên HDFS/BGL. Khai thác retrieval để cải thiện, thích hợp cho detection, minh bạch.  
- **CLDTLog (Tian et al., Sensors 2023)** – Q2, kết quả cực cao trên HDFS/BGL. Đơn giản (một số giới hạn training cần labelled hoặc không, nhưng thực nghiệm chỉ dùng data labels), hiệu năng mạnh.  
- **LogEDL (Duan et al., Appl Sci 2024)** – Q2, tự huấn luyện với hàm loss evidential, SOTA trên nhiều dataset. Nhược: tính toán nặng (FLOPs cao).  
- **CoLog (Nasirzadeh et al., Sci Rep 2025)** – Q1, đa-modal, chưa có mã nguồn bên ngoài (mã đã public trên GitHub), đạt kết quả cao. Tuy nhiên phương pháp mới (rare in log community).  

Các ứng viên này đáp ứng tiêu chí *tuổi tác (2023–2026), công bố chính thức, tạp chí Q1/Q2, phù hợp bài toán log anomaly*.  Trong số này, **LogFiT** và **LogSentry** là tân nhất (2024, 2025) và thuộc Q1. CLDTLog, LogEDL cũng mạnh nhưng thuộc Q2. CoLog có novel về modal nhưng tập trung point anomaly, chưa rõ hướng cải tiến cụ thể.  

## Phân tích baseline (LogFiT làm ví dụ)  
- **Đầu vào/biểu diễn:** Nhóm hàng log (mỗi *log paragraph*) được gộp theo ID (như HDFS). Không dùng log parser, trực tiếp lấy câu log.  
- **Cơ chế phát hiện:** Mô hình BERT tiền huấn luyện được fine-tune tự giám sát bằng *masked sentence prediction* trên logs bình thường (chỉ xuất hiện ‘sentence’ (paragraph) hợp lệ). Khi dự đoán token với độ chính xác *top-k*, nếu dưới ngưỡng quyết định thì xem là bất thường. Tức LogFiT đánh dấu anomaly dựa trên độ *độ tin/top-k accuracy*.  
- **Retrieval/Knowledge:** Không dùng cơ chế truy vấn hay kiến thức ngoài; chỉ dựa trên mô hình ngôn ngữ.  
- **Lý luận/bộ nhớ:** Mô hình hoàn toàn dựa trên attention, không lưu giữ trạng thái ngoài các embedding. Dữ liệu ngữ cảnh giới hạn trong mỗi paragraph (có thể chiều dài ~512 tokens).  
- **Tiền xử lý:** Có thể tiền xử lý đơn giản (gộp logs, token hóa); mô hình chủ yếu tận dụng encoder BERT chuẩn.  
- **Workflow inference:** Với logs mới, chia thành paragraphs, đưa qua BERT để sinh token score. Dựa trên tỉ lệ đúng top-k để gán nhãn. Do *self-supervised*, không cần nhãn huấn luyện.  

Tổng quan: LogFiT **tập trung vào học biểu diễn ngôn ngữ của log bình thường** mà không cần nhãn. Khả năng tái triển khai cao nhờ sử dụng mô hình và pipeline có sẵn (Hugging Face). Kết quả thử nghiệm cho thấy vượt trội so với các baseline khác trên nhiều bộ dữ liệu tiêu chuẩn.  

## Bằng chứng giới hạn của baseline  
Từ phân tích trên và theo báo cáo các tác giả:
- **Yêu cầu tính toán:** LogFiT nặng vì dùng BERT. Tài liệu ghi nhận hiệu năng suy giảm do throughput chưa tối ưu; tác giả đề xuất cần *giảm dung lượng mô hình/giảm kích thước* trong tương lai.  
- **Ngưỡng quyết định:** Sử dụng top-k accuracy làm ngưỡng có thể không ổn định trong trường hợp **drift** logs hoặc môi trường thay đổi (tài liệu không thảo luận chi tiết, nhưng đây là điểm yếu chung của phương pháp threshold).  
- **Đặc thù logs:** LogFiT chưa thiết kế đặc biệt để xử lý logs mới lạ (không có trong training); tác giả chỉ ra nó có thể chuyển thành classifier nếu cần. Hiện tại chỉ xử lý logs đơn lẻ mà chưa tận dụng kiến thức bên ngoài hoặc lịch sử dài hạn.  
- **Đánh giá muộn:** Giống nhiều công trình khác, LogFiT chưa đo các metric sớm (lead time); chỉ báo cáo F1/Precision/Recall truyền thống. Do đó, khả năng *phát hiện sớm* thiếu kiểm chứng.  
Các bằng chứng cụ thể từ bài viết thể hiện hạn chế về tốc độ (throughput) và khả năng triển khai thời gian thực.

## Cơ hội cải tiến (theo giới hạn xác thực được)  
- **Tối ưu hóa mô hình (nén/giảm tính toán):** Để khắc phục throughput thấp, có thể áp dụng các kỹ thuật tiết kiệm tham số cho Transformer. Ví dụ, phương pháp *LoRA* (tăng cường ma trận hạ bậc) hoặc *quantization* (giảm độ chính xác số học) có thể giảm đáng kể FLOPs mà không giảm nhiều hiệu năng. Đây là cách cải tiến trực tiếp nhằm giảm độ trễ inference. Rủi ro: nếu nén quá mức, khả năng phát hiện anomaly có thể giảm nhẹ.  
- **Tăng khả năng giải thích:** Hiện LogFiT là “hộp đen” (chỉ ra “không đúng top-k”). Có thể cải tiến bằng cách tích hợp giải thích (như sử dụng SHAP hoặc attention trọng số) để xác định cụm từ quan trọng. Catalán et al. 2026 cung cấp ví dụ về việc kết hợp transformer với SHAP nhằm làm sáng tỏ quyết định bất thường.  
- **Mở rộng ngữ cảnh:** LogFiT chỉ xem từng paragraph. Cải tiến có thể thêm bộ nhớ ngoài để liên kết các logs theo thời gian dài, hoặc sử dụng kỹ thuật **continual learning** để thích ứng logs mới. Ví dụ, lưu trữ embedding logs mới được gắn anomaly để fine-tune dần. Tuy chưa có bằng chứng trực tiếp, đây là xu hướng đang nghiên cứu trong log mining.  
- **Kết hợp đa dữ liệu:** Theo LogSentry, một giới hạn chung là chỉ dùng logs đơn. Có thể bổ sung **dữ liệu đa-modal** (metrics, traces) để tăng tính bao phủ. Ví dụ, CoLog tích hợp nhiều nguồn log; cải tiến tương tự có thể kết hợp logs với metrics. Tuy nhiên, bước này phức tạp và cần tập dữ liệu đặc thù.  

Trong đó, **LoRA/quantization** là hướng *có cơ sở học thuật và dễ kiểm chứng* (bằng thực nghiệm đo throughput vs accuracy). Các hướng như giải thích, bộ nhớ hay đa-modal mạnh về ý tưởng nhưng đòi hỏi tài nguyên thêm. Cơ hội cải thiện được ưu tiên là tăng hiệu năng tính toán cho LogFiT (theo tác giả gợi ý) nhằm tăng cường khả năng vận hành thực tế.

## Kế hoạch đánh giá so sánh  
- **Baseline:** Chọn LogFiT (TNSM 2024, Q1) – công bố chính thức, tự giám sát, hiệu năng cao trên nhiều tập log chuẩn. So sánh với các phương pháp tương đương (ví dụ DeepLog, LogBERT, LogAnomaly) để đảm bảo độ chính xác của re-implementation.  
- **Bản cải tiến:** LogFiT được áp dụng *kỹ thuật nén mô hình* (ví dụ LoRA hay quantization). Thử nghiệm với cùng tập dữ liệu (HDFS, BGL, Thunderbird). Thực nghiệm thêm về tốc độ (inference throughput, latency) bên cạnh F1, Precision, Recall.  
- **Ablation (nếu có thể):** So sánh LogFiT gốc vs LogFiT+LoRA vs LogFiT+quantization để chứng minh ảnh hưởng.  
- **Metrics**: Ngoài F1, Precision, Recall, sẽ bổ sung đo **inference latency** (thời gian dự đoán mẫu log) và **tốc độ xử lý** (messages per second) để đánh giá cải thiện hiệu năng. Nếu muốn hướng về sớm: đo độ trễ trung bình *Time-to-Detect* (nhưng hầu hết chỉ đánh dấu mẫu, nên giả định phát hiện tại thời điểm xử lý).  
- **Cơ sở dữ liệu:** Sử dụng các benchmark thông dụng (HDFS, BGL, Thunderbird). Đảm bảo tái tạo kết quả của LogFiT ban đầu để minh bạch.  

Kế hoạch này cho phép kiểm chứng rõ ràng: LogFiT cơ sở vs LogFiT (nén) cải tiến, đo **độ chính xác** và **tốc độ**. Đóng góp nằm ở việc tối ưu hóa thuật toán hiện có thay vì đề xuất hoàn toàn mới, phù hợp định vị “mở rộng/cải tiến” theo yêu cầu.

## Kết luận chính  
- **Baseline tốt nhất:** **LogFiT (TNSM 2024, Q1)** được đề xuất. Đây là phương pháp gần đây, được peer-review, phù hợp với việc phát hiện anomaly dựa trên log và có kiến trúc rõ ràng (BERT tự giám sát). Nó vượt các baseline trước đó về F1 và dùng ít phụ thuộc nhãn.  
- **Tại sao:** So với CLDTLog hay LogEDL (dù chính xác cao) và LogSentry (mới nhưng chưa nhiều chứng thực ngoài bài), LogFiT có lợi thế Q1, khả năng tái hiện bằng mô hình BERT phổ biến, và chưa có phương pháp nào áp dụng kỹ thuật nén trên nó.  
- **Hạn chế xác nhận:** *Thông lượng tính toán thấp* (thời gian inference dài) đã được tác giả chỉ ra và muốn cải thiện qua LoRA/quantization. Đây là hạn chế được chứng minh qua bảng hiệu năng và FLOPs cao (LogFiT ~628M flops).  
- **Cơ hội cải tiến:** Tập trung vào *nén mô hình và tăng tốc inference*. Bằng chứng hỗ trợ gồm gợi ý từ tác giả áp dụng LoRA/quant và nhu cầu in phép nhanh. Các kỹ thuật như LoRA đã thành công trong các ứng dụng LLM khác để giảm tham số mà giữ hiệu năng gần như không đổi.  
- **Thư viện hỗ trợ:** Catalán et al. (2026) chứng minh transformer log có thể tích hợp giải thích (SHAP); các bài tổng quan gần đây cũng nhắc đến độ trễ phát hiện là tiêu chí cần chú ý (nhưng thiếu trong bài cũ). Điều này chỉ ra việc thêm đánh giá độ trễ và làm rõ quyết định là ý tưởng khả thi, nhưng chưa có công trình Q1 nào hoàn chỉnh thực hiện.  
- **Định vị đóng góp:** Công trình này sẽ được định vị là *“cải tiến (improvement) của LogFiT – một phương pháp Q1 mới”*. Không phải tạo mô hình mới, mà giữ lõi là BERT + self-supervised, chỉ thêm khâu nén/định lượng để giải quyết điểm yếu.  
- **Khả thi thực nghiệm:** Việc áp dụng LoRA/quantization cho một mô hình BERT fine-tune là khả thi trong khuôn khổ luận văn. Cả công cụ và mã nền (BERT/Torch) đều có sẵn. Dự kiến dễ triển khai, và kết quả (độ chính xác gần tương đương, thời gian inference nhanh hơn) có thể đo lường trực tiếp, thuyết phục.  

## Tóm tắt chính  
1. Phương pháp căn bản đề xuất: **LogFiT** (TNSM 2024, Q1), sử dụng BERT tự giám sát để phát hiện anomaly log.  
2. Hạn chế xác nhận: hiệu năng tính toán thấp (throughput chưa tốt) do mô hình lớn.  
3. Cơ hội cải thiện: áp dụng *LoRA hoặc quantization* để giảm tham số và tăng tốc độ inference.  
4. Thư viện hỗ trợ: đã có nghiên cứu thẩm định transformer cho logs (Catalán et al. 2026) và các kỹ thuật nén mô hình trong NLP.  
5. Đóng góp kỳ vọng: “mở rộng/phát triển” phương pháp LogFiT (Q1 2024) thông qua tối ưu hóa inference, phù hợp với tiêu chí cải tiến mục tiêu của đề tài.  
6. Khả thi: xác suất cao để triển khai trong luận văn và thí nghiệm so sánh (đo latency và F1) với sự thay đổi rõ rệt về tốc độ mà vẫn giữ độ chính xác.

**Nguồn tham khảo:** Các trích dẫn trên đều từ bài báo Q1/Q2 giai đoạn 2023–2026 về anomaly detection trên log (như LogFiT, CLDTLog, LogEDL, LogSentry, CoLog, Catalán et al. 2026). Tình trạng xếp hạng được xác minh theo JCR/Scopus (LogFiT – IEEE TNSM Q1; LogSentry/CoLog – Scientific Reports Q1; CLDTLog/LogEDL – Q2). Các báo trích dẫn thể hiện bằng `` tương ứng từ bài đã mở.