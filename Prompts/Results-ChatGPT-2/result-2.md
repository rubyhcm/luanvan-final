# 1. Xác thực kết quả Literature Mapping

| Claim | Bằng chứng ủng hộ | Bằng chứng trái ngược | Độ tin cậy | Đánh giá |
|---|---|---|---|---|
| **Các mô hình học sâu (LSTM, CNN)** đạt kết quả tốt trong phát hiện dị thường log. | Nghiên cứu thực nghiệm chỉ ra các mô hình học sâu (ví dụ LSTM, CNN) cho kết quả “hứa hẹn” trong phát hiện dị thường log. | Các phương pháp truyền thống (PCA, SVM, isolation forest, v.v.) vẫn có thể đáp ứng được trong một số trường hợp đơn giản. | Trung bình | Các kỹ thuật DL được áp dụng rộng rãi gần đây và thường vượt các phương pháp cổ điển, nhưng mức độ cải thiện còn phụ thuộc vào bộ dữ liệu và cấu hình cụ thể. |
| **Độ chính xác của tiền xử lý phân tích cấu trúc log (log parsing)** tỷ lệ thuận với độ chính xác phát hiện dị thường. | Giả định phổ biến: log cần được parse chính xác để phát hiện dị thường tốt. | Nghiên cứu toàn diện cho thấy *không có mối tương quan mạnh* giữa độ chính xác parsing và độ chính xác phát hiện dị thường; thay vào đó, độ **phân biệt** của kết quả parsing mới quan trọng. | Cao | Bằng chứng mạnh mẽ từ phân tích thực nghiệm cho thấy giả định này là sai. Cần điều chỉnh quan điểm: tối ưu hoá khả năng phân biệt (distinguishability) quan trọng hơn. |
| **Truy hồi kiến thức (RAG)** cải thiện kết quả phát hiện dị thường. | Ví dụ, khung LogSentry sử dụng kết hợp BERT và KNN truy hồi, báo cáo “hiệu suất cao” vượt các phương pháp nền tảng. | Mặc dù cải thiện accuracy, truy hồi có thể gây độ trễ và cần cập nhật bộ nhớ kiến thức liên tục; tính cũ/rời rạc của dữ liệu truy hồi là rủi ro tiềm ẩn. | Trung bình | Bằng chứng thực nghiệm ban đầu cho thấy lợi ích về độ chính xác, nhưng vẫn cần xem xét khả năng áp dụng trong hệ thống thực tế (độ trễ, chi phí). |
| **Mô hình Transformer (BERT)** đang trở nên phổ biến trong phân tích log. | Nhiều công trình gần đây (vd. LogSentry) dựa vào BERT để mã hóa log. | Mô hình này nặng và yêu cầu từ vựng cố định: LAnoBERT lưu ý **vấn đề từ vựng và OOV**, do logs thường có các từ/tên không xuất hiện trong tập huấn luyện. | Trung bình | Xu hướng dùng transformer rõ ràng, nhất là BERT tùy biến trên log. Tuy nhiên, các giới hạn về từ vựng và chi phí tính toán là thách thức cần vượt qua. |
| **Tập trung vào phát hiện sớm (early detection)** trong các công trình hiện tại còn yếu. | Rất ít nghiên cứu trong mapping bàn đến các chỉ số như lead-time. Hầu hết chỉ trình bày F1/precision/recall bình thường. | Không có bằng chứng trực tiếp từ mapping; chủ yếu là suy luận dựa trên thiếu hụt công bố. | Thấp | Suy luận: hầu hết phương pháp chỉ tập trung đo lường kiểu phân loại thông thường, chưa đo lường khoảng cách thời gian dẫn đến sự cố (lead time) để khẳng định tính “phát hiện sớm” thực sự. |

**Đánh giá:** Kết quả định tính của mapping (trends, taxonomy, claims) có phần đúng – như xu hướng học sâu và sự quan tâm đến các mô hình Transformer/RAG – nhưng một số giả định (ví dụ vai trò của độ chính xác parsing) đã bị bác bỏ bởi bằng chứng thực nghiệm mạnh. Cần cẩn trọng: mapping ban đầu có thể cho rằng parsing accuracy quan trọng; nhưng thực nghiệm cho thấy không phải vậy. Tương tự, cần phân biệt rõ giữa phát hiện dị thường thông thường và **phát hiện sớm**, bởi các chỉ số F1/Recall/Precision không đo được độ sớm của cảnh báo. Các đánh giá trên dẫn đến độ tin cậy cao đối với bằng chứng đã xác minh (ví dụ mô hình DL tốt) và chứng cứ phủ định (ví dụ parsing), và độ tin cậy trung bình đối với hướng mới (ví dụ RAG) hoặc thiếu bằng chứng (phát hiện sớm).

# 2. Phân tích phê phán nhiều paper

## 2.1. Mô hình cơ sở (Foundation Models)

Các mô hình ngôn ngữ lớn (LLM) hay domain-specific (như LogBERT) chưa phổ biến cho detection đơn thuần. Trong tài liệu, chỉ có các biến thể Transformer như **BERT** được áp dụng cho log (ví dụ LAnoBERT, LogSentry) thay vì GPT-3/4 nguyên gốc. Điểm mạnh của BERT là mã hoá ngữ nghĩa log tốt (đặc biệt với lớp semantic embedding); ví dụ, các DL model (LSTM/CNN) đã cho kết quả “hứa hẹn” trong phát hiện dị thường, và BERT cũng tiếp nối xu hướng này. Tuy nhiên, LAnoBERT nhấn mạnh điểm yếu: những mô hình embedding tĩnh **không xử lý được từ vựng mới (OOV)** và phụ thuộc vào kết quả parsing. Điều này cho thấy mô hình ngôn ngữ tổng quát thường cần điều chỉnh sâu (domain adaptation) để hiểu logs: ví dụ các tham số, timestamp, địa chỉ IP đặc thù. LLM lớn (ChatGPT, GPT-4) có khả năng tổng quát cao nhưng chi phí tốn kém, và chưa có công trình Q1/Q2 nào chính thức dùng LLM đầy đủ cho phát hiện sớm log. 

Về khả năng chung, các mô hình ngôn ngữ tiên tiến có ưu thế xử lý ngữ nghĩa và ngữ cảnh (contextual understanding), nhưng trong bối cảnh log anomaly detection, thành tựu cụ thể còn hạn chế. Ví dụ, việc “giải thích” (explanation) hay “lý giải gốc rễ” (root-cause) của LLM vẫn là thách thức do thiếu kiến thức chuyên ngành gắn liền với logs. Các đặc tính như **phát hiện dị thường sớm** đòi hỏi mô hình dự đoán trước thời điểm lỗi, khả năng hiện chưa được chứng minh ở quy mô LLM. Nói chung, LLM/Transformers giúp cải thiện sự nhận biết ngữ cảnh dài, nhưng phải đánh đổi với chi phí tính toán và vấn đề khuyết/vắng mặt dữ liệu chuyên biệt (domain mismatch).

## 2.2. Truy hồi kiến thức (RAG)

Chiến lược truy hồi – như tìm kiếm láng giềng gần nhất (KNN) trong không gian embedding – được một số nghiên cứu kết hợp vào phát hiện dị thường log. Ví dụ, **LogSentry** (Scientific Reports 2025) xây dựng một “cơ sở tri thức” gồm các vector đặc trưng của log đã ghi nhãn, sau đó trong pha suy luận kết hợp đầu ra của model với kết quả truy hồi KNN. Cụ thể, đầu ra của mô hình DL và trung bình nhãn thu được từ KNN được tính trọng số để ra kết quả cuối cùng. Phương pháp này cải thiện độ chính xác phát hiện (theo báo cáo “đạt hiệu suất cao so với baseline”). 

Tuy nhiên, cần cân nhắc chất lượng & độ phù hợp của tri thức truy hồi: nếu dataset huấn luyện và thực tế có sự sai lệch (stale knowledge) thì ví dụ truy hồi có thể không liên quan. Chiến lược embedding (chẳng hạn dùng BERT) cũng phải xử lý khớp từ khóa log; nếu logs nhiều biến thể hoặc lỗi cú pháp thì embedding KNN có thể sai lệch. Về thực thi, truy hồi KNN (đặc biệt với HNSW) có độ phức tạp và độ trễ nhất định, có thể không phù hợp cho ứng dụng đòi hỏi đáp ứng thời gian thực. Nhìn chung, các bằng chứng từ LogSentry cho thấy RAG cải thiện **độ chính xác phân loại dị thường**, nhưng công năng chủ yếu hướng đến *xác định* và *lý giải* dị thường (với trọng số nhãn) hơn là thay đổi cách kiến thức được tích hợp chủ động trong quá trình huấn luyện.

## 2.3. Lập luận (Reasoning)

Các phương pháp phát hiện dị thường log hiện nay chủ yếu là giải quyết bài toán phân loại hay dự báo nhãn bất thường đơn giản, ít khi triển khai các kỹ thuật lập luận phức hợp. Ví dụ, **Chain-of-Thought (CoT)** hay tự phản chiếu chưa được ứng dụng chính thức trong các nghiên cứu phê duyệt; cũng không có chuẩn mực nào về việc sử dụng multi-step reasoning hay tích hợp công cụ cho anomaly detection trong log. Do đó, hầu hết nghiên cứu chỉ dừng ở việc tính toán điểm bất thường (anomaly score) từ đầu ra của mô hình, không chạy các bước phân tích sâu để lý giải nguyên nhân gốc. Kỹ thuật **multi-event reasoning** (so sánh nhiều log liên tiếp) đã được xem xét qua các mô hình tuần tự (RNN/GRU/Transformer) để tìm mẫu dị thường, nhưng những phương pháp này không trọng tâm vào *hợp nhất thông tin xuyên cửa sổ thời gian* hay **dự báo lỗi trước**. Các khía cạnh như tự động phát hiện nguyên nhân (root-cause analysis) hay đưa ra lời giải thích chưa được các paper 2023–2026 tập trung, nên chưa có bằng chứng thực nghiệm hỗ trợ. 

Nói chung, khả năng lập luận lồng ghép vào công cụ hiện chưa rõ rệt: hầu hết giải pháp tập trung vào nhiệm vụ phát hiện/ phân loại dị thường, trong khi tự động hóa suy luận cao cấp (multi-step reasoning hoặc lập plan) chỉ mới manh nha ở mức khái niệm trong lĩnh vực AIOps tổng quát, chưa thấy ở bài bản phân tích logs (trừ một số work-in-progress hay dự án công nghiệp chưa công bố trên tạp chí Q1/Q2).

## 2.4. AI tăng cường tri thức (Knowledge-Augmented AI)

Sử dụng đồ thị tri thức, kho dữ liệu sự cố, hoặc tài liệu miền (domain knowledge) là một hướng nghiên cứu hứa hẹn nhưng ít được nêu bật trong các paper từ mapping. Ví dụ, không có nghiên cứu Q1/Q2 2023–2026 nào xây dựng đồ thị sự cố (knowledge graph) hoặc lược đồ (ontology) cho logs. Lý thuyết thì rõ: nếu có kiến thức về hệ thống (như kiến trúc phần mềm, quan hệ nhân quả giữa event) sẽ hỗ trợ lập luận và chẩn đoán, nhưng thực tế **chưa có hệ thống tri thức hoàn chỉnh** nào được tích hợp. Chất lượng bộ tri thức là một thách thức lớn (ví dụ, dữ liệu cũ, không đầy đủ, hoặc sai lệch), và cần bảo trì liên tục để đảm bảo luôn cập nhật (log và sự cố mới liên tục xuất hiện). Do đó, hầu hết phương pháp vẫn chỉ dựa vào log thuần túy, chưa kết hợp dữ liệu ngoài (ngoại trừ trường hợp nào như LogSentry, bản thân “cơ sở tri thức” đó chỉ đơn giản là tập vector embedding). Khả năng cải tiến sớm (early-warning) từ việc tăng cường tri thức này vẫn chưa được chứng minh.

## 2.5. AI tác nhân (Agentic AI)

Việc triển khai các tác nhân tự chủ (agents, multi-agent) để điều tra logs, phối hợp truy vấn hay gọi công cụ hầu như chưa thấy trong tài liệu chính thống. Tuy nhiên, ý tưởng có thể là một “agent” (dựa trên LLM) tự động thu thập bằng chứng (ví dụ truy vấn cơ sở dữ liệu lịch sử sự cố, logs, tài liệu hướng dẫn), tích hợp kết quả và thông báo. Ưu điểm tiềm năng: có thể tự động hóa quá trình chẩn đoán từ log, tìm hiểu hệ quả, lập kế hoạch khắc phục sự cố. Nhưng rủi ro rất cao: độ trễ lớn, chi phí tính toán khổng lồ, khó tái lập, thiếu tin cậy (LLM dễ “nói hão”, không được đào tạo chuyên sâu theo miền logs), và khó đánh giá chính xác. Hiện tại chưa có bằng chứng cho thấy agentic AI đã được áp dụng thành công cho đề bài này. Kết luận: agent có thể là xu hướng tương lai (AI đa tác vụ), nhưng ở cấp độ công bố Q1/Q2 chưa ổn định; chưa có đánh giá chuyên sâu về độ trễ/cost/độ tin cậy của nó trong cảnh báo sớm.

# 3. Đánh giá ứng viên phương pháp (2023–2026, Q1/Q2)

*Các phương pháp được xem xét làm baseline phải đáp ứng đủ điều kiện: năm 2023–2026, journal Q1/Q2, bài chính thức, liên quan trực tiếp đến anomaly log.*

| Ứng viên      | Năm  | Tạp chí (Q1/Q2)                   | Vấn đề phù hợp         | Hiệu năng | Tính tái lập | Rõ ràng kiến trúc | Bằng chứng hạn chế    | Tiềm năng cải tiến                    | Khả năng thí nghiệm | Đánh giá baseline |
|---------------|-----:|----------------------------------|------------------------|----------|---------------|-------------------|-----------------------|------------------------------------|--------------------|-------------------|
| **LAnoBERT** | 2023 | Applied Soft Computing (Elsevier, Q1) | Phát hiện dị thường log dựa trên BERT | Cao (dựa trên báo cáo F1 tốt) | Thấp–Trung bình (code chưa công bố công khai) | Kiến trúc transformer rõ ràng (mô hình BERT + head phân loại) | Thường xuyên phải parse log; nhược điểm OOV rõ | Dễ (MDPI/Elsevier cho phép, dữ liệu HDFS phổ biến) | Trung bình (Q1, hiện đại, nhưng hạn chế OOV/parse) |
| **LogOW** | 2025 | J. Systems & Software (Elsevier, Q1) | Dị thường log bán giám sát trong thế giới mở | Chưa biết (tác giả báo SOTA) | Cao (source code công bố trên Zenodo) | Kiến trúc làm rõ (sử dụng học sâu bán giám sát) | Có khả năng mở rộng phát hiện với logs mới; hạn chế chưa rõ (mới) | Phụ thuộc vào dataset (log hub, HDFS) | Cao (Q1, code có, phù hợp real-world) |
| **MidLog** (Multi-head GRU) | 2025 | J. Systems & Software (Elsevier, Q1) | Phát hiện dị thường log tự động | Chưa biết (SOTA trên vài bộ) | Thấp (không thấy code công khai) | Cấu trúc GRU đa đầu có thể phức tạp | Có thể tăng trưởng (hơi trừu tượng), chưa biết điểm yếu cụ thể | Tương tự LogOW | Thấp–Trung bình (Q1, mới nhưng thiếu code) |
| **LogSentry** | 2025 | Scientific Reports (Nature, Q1) | Dị thường log với truy hồi ngữ nghĩa | Công bố độ chính xác cao so baseline | Trung bình (mô hình mới, code chưa rõ) | Rõ ràng (BERT + KNN retrieval) | Nâng cao qua tối ưu hóa retrieval, xử lý OOV | Hướng dẫn dataset có, nhưng KNN tốn tài nguyên | Cao (Q1, open-access, ý tưởng mới) |

**Đánh giá:** Tất cả ứng viên trên đều là bài báo Q1/Q2 chính thức (xác minh qua SCImago/JCR). *LogOW* và *MidLog* đều ở JSS (Q1); *LAnoBERT* ở Applied Soft Computing (Elsevier, Q1); *LogSentry* ở Scientific Reports (Q1). Về *Phù hợp vấn đề*, cả bốn đều trực tiếp giải quyết anomaly detection trên log, tuy nhiên không có phương pháp nào gốc chuyên về *cảnh báo sớm*. Về *hiệu năng*, các tác giả đều báo cáo tốt (nhưng chờ thẩm định độc lập). *LAnoBERT* và *LogSentry* là những đề xuất đột phá (BERT, RAG), tuy nhiên hạn chế về khả năng tái lập (thiếu công khai code). *LogOW* có ưu thế tái lập (có code) và đề cập môi trường mở (open-world), là lợi thế thực nghiệm. Điểm yếu chung: tất cả chưa xét đến drift hoặc dữ liệu streaming. Độ *khả thi* thí nghiệm cao (dữ liệu HDFS/BGL phổ biến, quy mô vừa phải). Kết luận: **LogOW** và **LAnoBERT**/ **LogSentry** là các baseline triển vọng nhất. Nếu chọn một – xu hướng cải thiện có thể ưu tiên **LAnoBERT** hoặc **LogSentry** (Q1, ý tưởng hiện đại, có bằng chứng hạn chế để cải tiến).  

# 4. Phân rã baseline

Đối với các baseline ưu tiên (ví dụ *LAnoBERT* và *LogSentry*), ta xem xét các thành phần chính sau:

| Thành phần           | Triển khai (Baseline)         | Ưu điểm                         | Nhược điểm                           | Bằng chứng                  |
|---------------------|-------------------------------|---------------------------------|--------------------------------------|-----------------------------|
| **Tiền xử lý/Parsers** | Sử dụng kỹ thuật parsing (ví dụ Drain) để chuẩn hoá logs thành template. | Chuyển logs thành các template cố định, đơn giản hoá dữ liệu đầu vào. | Sai số parsing ảnh hưởng nhỏ đến kết quả; parsing có thể bỏ sót thông tin số liệu. |  |
| **Biểu diễn (Representation)** | *LAnoBERT:* Mã hoá log bằng BERT với từ vựng cố định. *LogSentry:* Mã hoá BERT sinh đặc trưng ngữ nghĩa. | Nắm bắt ngữ nghĩa sâu (đặc biệt LAnoBERT bắt đầu từ ngữ cảnh transformer). | *LAnoBERT:* Vocab cố định, không nắm bắt được từ mới (OOV); phụ thuộc parsing. *LogSentry:* Phụ thuộc BERT, tốn tài nguyên. |  |
| **Ngữ cảnh/Trình tự**  | Xử lý theo cửa sổ thời gian hoặc chuỗi logs (ví dụ session HDFS). | Khai thác tuần tự sự kiện (RNN/GRU/Transformer). | Cần chuỗi log đủ dài; **không xử lý tốt trường hợp phát hiện từ một log đơn lẻ**. (Ví dụ, nhiều phương pháp hiện tại chỉ hoạt động với session dài) | Gián tiếp: nhiều công trình nhấn mạnh phải có cửa sổ (vd. PLELog). |
| **Truy hồi/kiến thức (Memory)** | *LogSentry:* Xây cơ sở dữ liệu vector features từ tập huấn luyện, dùng KNN lấy nhãn gần nhất. | Ghi nhớ ví dụ lịch sử, có thể tăng cường phân loại. | Tốn thời gian truy vấn KNN, khả năng tràn/bão hoà nếu feature vector trùng lặp; dựa vào dữ liệu tĩnh không tự cập nhật. |  (LogSentry) |
| **Đánh giá dị thường (Scoring)** | Cụm lớp phân loại hoặc sử dụng các chỉ số thống kê. Ví dụ *LAnoBERT* dùng đầu ra layer cuối (logits) để phân loại. | Đơn giản, dễ triển khai. | Ngưỡng (threshold) cố định có thể không thích ứng với drift; thiếu lead-time. | – |
| **Huấn luyện (Training)** | Thường là huấn luyện có giám sát (benign vs. anomalous) hoặc bán giám sát (đào tạo trên logs bình thường, đánh giá dự báo). | Có thể tận dụng nhãn đầy đủ nếu có; bán giám sát dễ triển khai khi ít nhãn. | Cần dữ liệu nhãn (anomaly) cân đối; dễ bị lệch class (imbalance) – LogSentry dùng contrastive learning để giảm imbalance. | – |
| **Inference**        | Mô hình forward qua mạng. *LogSentry* cộng thêm bước truy vấn KNN và kết hợp kết quả. | Nhanh chóng (riêng bước forward rất nhanh nếu trên GPU); *LogSentry* cải thiện accuracy nhờ truy hồi. | Có độ trễ khi lấy KNN; khả năng trôi ngữ cảnh nếu không cập nhật. |  |

**Nhận xét:** Cốt lõi của *LAnoBERT* là sử dụng BERT/Masked LM để học biểu diễn ngữ nghĩa log, song đang bị hạn chế bởi bộ từ vựng tĩnh và phụ thuộc parsing. *LogSentry* kết hợp Hệ thống truy hồi song lại đối mặt với chi phí truy vấn cao và tính cũ của bộ dữ liệu học (tri thức). Những điểm nghẽn này chính là các cơ hội cải tiến: cải thiện tầng biểu diễn để xử lý OOV và token động, hoặc tối ưu cơ chế truy vấn/kiến thức để giảm độ trễ.

# 5. Giả định chung

Các nghiên cứu thường mặc định (implicit assumption) trong baseline bao gồm: 
- **Logs đã được parse/chuyển cấu trúc:** Hầu hết phương pháp giả sử log đầu vào đã được phân tích cấu trúc (như template) và mã hoá thích hợp (thông qua các công cụ như Drain). Giả định này phù hợp trong thí nghiệm (dễ dàng áp dụng log parser), nhưng trong môi trường thực, lỗi parser có thể liên tục xảy ra.
- **Tập cố định, offline:** Dữ liệu huấn luyện và đánh giá là bất biến (offline, train/test tĩnh) và tương tự nhau. Do đó, không xem xét drift (thay đổi luồng logs theo thời gian) hay streaming (cảnh báo liên tục). Điều này làm đơn giản hoá thí nghiệm nhưng hạn chế thực tế, vì logs vận hành thường biến đổi theo thời gian.
- **Không dùng kiến thức ngoài:** Hầu hết phương pháp chỉ dùng dữ liệu log hiện có, không truy vấn thêm nguồn kiến thức bên ngoài (như tài liệu kỹ thuật, lịch sử sự cố). 
- **Ngưỡng cố định:** Ngưỡng phát hiện dị thường thường cố định sau huấn luyện, không thay đổi theo ngữ cảnh. Giả định này đơn giản nhưng có thể kém linh hoạt khi phân phối log thay đổi.
- **Ngữ cảnh đủ dài:** Giả định có đủ ngữ cảnh (chuỗi logs) để mô hình học. Đánh giá cao thành phần sequence, nhưng không xét trường hợp ngữ cảnh ngắn hay log đơn lẻ.
- **Nhãn lỗi ổn định:** Giả định rằng lớp “normal” và “anomaly” tương đối ổn định (không thay đổi mục tiêu).
  
**Đánh giá:** Những giả định trên hợp lý cho phòng thí nghiệm, nhưng tác động đến tính ứng dụng thực tế. Ví dụ, **drift dữ liệu** hay **streaming online** thường xảy ra trong môi trường thực AIOps và nếu không xử lý sẽ giảm hiệu năng. Giả định logs đã parse và ngữ cảnh đủ dài có thể không đúng trong thực tế (log rác, log chưa parser tốt). Những yếu tố này có thể là hạn chế chính nếu muốn áp dụng. 

# 6. Hạn chế chung

Các hạn chế quan trọng tìm thấy gồm:

- **Mô hình nền tảng (Foundation Model):**  
  - *OOV/hallucination:* Như LAnoBERT nhận định, mô hình dùng từ vựng cố định dễ bỏ sót từ lạ (common log identifiers). Nếu dùng GPT-like, hallucination có thể xảy ra (tạo thông tin sai khi giải thích logs).  
  - *Chi phí tính toán:* Mô hình Transformer/BERT/ngôn ngữ lớn tiêu tốn nhiều tài nguyên (GPU, inference time), làm giảm khả năng triển khai thời gian thực.  
  - *Lỗi logic (prompt sensitivity):* Nếu dùng prompt cho LLM, kết quả có thể rất nhạy với câu lệnh đầu vào, khiến khó điều chỉnh cho detection chuẩn.  

- **Truy hồi (Retrieval):**  
  - *Truy vấn không chính xác:* Kết quả KNN phụ thuộc embedding; nếu embedding không tốt (OOV, domain mismatch), truy hồi đem lại thông tin kém liên quan.  
  - *Tri thức lỗi thời:* Đóng gói log training vào KB có thể lỗi thời nếu log format thay đổi; cần cập nhật thường xuyên.  
  - *Ngữ cảnh nhiễu:* Nếu lấy quá nhiều log không liên quan làm ngữ cảnh, có thể làm loãng tín hiệu bất thường chính.  
  - *Chi phí cao:* KNN trên nhiều vector có thể đắt ở quy mô lớn, gây độ trễ cao; khả năng mở rộng không tốt.  

- **Tri thức bên ngoài:**  
  - *Không đầy đủ/hay lỗi:* Các tài liệu/hồ sơ sự cố có thể lỗi thời, rời rạc, không đủ liên kết với log hiện thời.  
  - *Khó align:* Kết hợp kiến thức có cấu trúc (ví dụ ontology) với dữ liệu log thô phức tạp, cần xử lý nền tảng riêng.  

- **Bối cảnh/temporal:**  
  - *Cửa sổ ngắn:* Nếu mô hình chỉ xem trong cửa sổ ngắn (vd. vài chục log), sẽ bỏ sót trường hợp cần xem xa hơn (cross-window dependency).  
  - *Gián đoạn/ngắt:* Dữ liệu streaming thường bị cắt gọn (truncated); model huấn luyện offline không học nối tiếp liên tục.  
  - *Drift:* Các baseline thường không kiểm soát tình trạng drift concept (phân phối log thay đổi qua thời gian), nên dễ mất chính xác sau một thời gian.  

- **Dữ liệu/Bộ test:**  
  - *Thiên lệch và giả lập:* Bộ dữ liệu phổ biến (HDFS, BGL, ThunderBird) bị hạn chế: thường là logs được tổng hợp theo workflow, thiên vị hệ thống Hadoop hoặc máy lớn. Anomalies có thể được tiêm thủ công với giả định (chưa phản ánh mọi tình huống thực).  
  - *Thiếu đa dạng:* Hầu hết chỉ dùng 2–3 bộ dữ liệu, chưa đủ đại diện cho các domain khác (edge computing, logs mạng, IoT).  
  - *Không phân biệt type:* Bài toán đôi khi chỉ đưa anomaly đơn lẻ (point anomaly), chưa xét collective/trend anomaly.  
  - *Dữ liệu cân bằng:* Anomaly rất ít (imbalance), tạo thách thức trong huấn luyện nhưng hầu như chưa được xử lý triệt để (chỉ LogSentry chú ý đến imbalance).  

- **Đánh giá:**  
  - *Offline-only:* Đa số thí nghiệm chỉ kiểm tra trên tập tĩnh offline; không có môi trường giả lập streaming hoặc deployment thực tế.  
  - *Thiếu metric sớm:* Hầu như chỉ dùng Precision/Recall/F1, không đo “time to detect” hay “lead time”. Nhiều nghiên cứu tự nhận là sớm nhưng không cung cấp metric tương ứng.  
  - *Thiếu so sánh công bằng:* Các paper thường dùng bộ test riêng (như HDFS-người tạo) và đánh giá lẫn lộn, thiếu giao thức đánh giá chuẩn, gây khó khăn so sánh.  

Tóm lại, các hạn chế cốt lõi được xác nhận bằng chứng mạnh là: sự phụ thuộc nặng nề vào parsing và từ vựng tĩnh (cần cải thiện); và thiếu các metric/chương trình huấn luyện thực tế cho cảnh báo sớm. Ngoài ra, các vấn đề như chi phí truy hồi cao, drift, thiếu benchmark thực tế vẫn cần khắc phục trong tương lai.

# 7. Phân tích về phát hiện sớm trong log

**Phân biệt các khái niệm:**  
- **Phát hiện dị thường (Anomaly Detection):** Xác định điểm bất thường dựa trên log quan sát. Đầu ra thường là nhãn bất thường/không bất thường.  
- **Phân loại (Classification):** Đối xử tương tự (có nhãn) nhưng không quan tâm đến thời gian xuất hiện.  
- **Chẩn đoán (Diagnosis):** Tập trung vào xác định nguyên nhân gốc rễ của anomaly, không chỉ phát hiện nó.  
- **Dự đoán lỗi (Failure Prediction):** Dự báo sự cố trước khi xảy ra (dựa trên log và các tín hiệu), chú trọng về mặt thời gian.  
- **Cảnh báo sớm (Early Warning/Early Anomaly Detection):** Phát hiện anomaly trước khi chúng tác động (ví dụ trước thời gian lỗi thực tế), hoặc càng sớm càng tốt. Được đánh giá bằng các chỉ số như **Lead Time** (khoảng thời gian giữa cảnh báo và lỗi), **Time-to-Detect**, **Detection Before Failure**.  

**Các phép đo liên quan:**  
- *Detection Lead Time:* Thời gian cảnh báo trước thời điểm lỗi.  
- *Time-to-Detect (TTD):* Thời gian kể từ khi sự cố diễn ra đến khi phát hiện (đối với cảnh báo đang trì hoãn).  
- *Mean Time to Detect (MTTD):* Trung bình TTD qua nhiều sự kiện.  
- *Early Warning Horizon:* Thời gian trước lỗi mà mô hình có thể cảnh báo (càng lớn càng tốt).  
- *Detection Before Failure:* Tỷ lệ phát hiện anomaly trước khi thất bại xảy ra.  

**Nhận xét:** Hầu hết các báo cáo trong result-1 (và các phương pháp baseline) chỉ cung cấp precision/recall/F1/accuracy thông thường. Theo hướng dẫn, ta không được coi đó là minh chứng của “phát hiện sớm”. Nếu một phương pháp tuyên bố phát hiện sớm mà không nêu lead time hay horizon rõ ràng, thì tuyên bố đó không có bằng chứng đủ. Ví dụ, *LogSentry* và *LAnoBERT* báo cáo F1 cao trên benchmark, nhưng không đánh giá mức độ sớm của cảnh báo. Nói cách khác, mọi phân tích cụ thể về thời gian phát hiện (để chứng minh thực sự “early”) đều bị bỏ ngỏ. Đây là lỗ hổng chung: thiếu các phép đo chuyên biệt về độ sớm, làm cho các khẳng định “sớm” chỉ dựa trên metrics phân loại cơ bản là **không đủ**.

# 8. Xác thực bằng chứng (Evidence Validation)

| Khẳng định (Claim) | Loại bằng chứng | Bài báo hỗ trợ | Bằng chứng trái ngược | Độ tin cậy |
|---|---|---|---|---|
| **Độ chính xác parsing cao không nhất thiết cải thiện detection** | Bằng chứng thực nghiệm (Experimenal) | Khan et al. 2024 (Emp. SE) | – | Cao (giá trị thực nghiệm) |
| **Phương pháp học sâu (DL) vượt trội so với truyền thống** | Phân tích chéo (Cross-paper) | Khan et al. 2024; Nhiều paper DL khác (LogBERT, LogAnomaly) | – | Trung bình (nhiều ví dụ) |
| **Phương pháp dựa trên chuỗi (sequence) bỏ sót anomaly đơn lẻ** | Luận giải tác giả (Inference) | – | Ví dụ đề cập của các tác giả LAnoBERT nêu: baseline cần nhiều log entry (không mở được) | Thấp (thiếu bằng chứng công bố) |
| **Mô hình embedding tĩnh gặp giới hạn (OOV, phụ thuộc parsing)** | Bằng chứng tác giả (Author inference) | LAnoBERT (ASoC 2023) | – | Cao (trích tác giả) |
| **Truy hồi KNN tăng độ chính xác** | Bằng chứng tác giả (Author/Experimental) | LogSentry (SciRep 2025) | – | Trung bình (một paper) |
| **Hệ thống benchmarks hiện chưa đo lường phát hiện sớm** | Mô hình luận lý (Model inference) | – | – | Thấp (dựa trên đánh giá vắng bằng chứng cụ thể) |

*Đánh giá:* Ta chỉ đưa vào các khẳng định có bằng chứng cụ thể. Ví dụ, [76] trực tiếp chứng minh parsing accuracy không ảnh hưởng đến detection (độ tin cậy cao vì số liệu thực nghiệm rõ ràng). Bằng chứng về DL mạnh hơn truyền thống khá phổ biến, nên tin cậy trung bình. Bằng chứng về OOV/parsing là trích từ bài LAnoBERT (do tác giả nêu), độ tin cậy cao vì cùng tác giả. Giả thuyết về phát hiện sớm được đánh giá là không có đủ bằng chứng cụ thể (độ tin cậy thấp). Không cố kết luận vượt mức bằng chứng này.

# 9. Bản đồ Baseline → Hạn chế → Cải tiến

| Baseline    | Hạn chế được xác nhận | Bằng chứng | Kỹ thuật hiện có / Nghiên cứu liên quan | Cơ hội cải tiến | Ảnh hưởng kỳ vọng | Rủi ro | Độ tin cậy |
|------------|-----------------------|-----------|-------------------------------------------|------------------|-------------------|-------|------------|
| **LAnoBERT (ASC 2023)** | Phụ thuộc vocab cố định, không xử lý từ mới (OOV); Cần log parsing chính xác | Bài viết nêu rõ hai hạn chế trên | Phương pháp token hoá động (subword, BPE) hoặc embedding tự động (like FastText) để giảm OOV | Cải tiến: áp dụng token hoá subword hoặc training từ mới trực tuyến; tích hợp RAG để bổ sung thông tin từ ngoài (tri thức logs) | Tăng khả năng xử lý logs lạ, cải thiện recall cho trường hợp log format mới | Tăng độ phức tạp huấn luyện, có thể tăng FPR nếu tokenizer không tốt | Cao (nhờ bằng chứng rõ ràng) |
| **LogSentry (SciRep 2025)** | Mô hình nặng (BERT+KNN), tính toán truy vấn cao; dựa vào dữ liệu cũ trong KB | Báo cáo của tác giả chỉ ra KNN cần nhiều index và tính năng | Kỹ thuật giảm chi phí: Approximate NN, chuẩn hoá embedding để tăng độ tương tác | Cải tiến: tối ưu hóa cấu trúc lưu trữ vector (HNSW tuning); cập nhật KB liên tục (streaming logs); sử dụng chỉ điểm phụ (proxy) | Giảm độ trễ phản hồi, cập nhật model phù hợp logs mới | Nếu áp dụng gần real-time, có thể tăng sai lệch do tri thức lỗi thời | Trung bình (phát hiện ngoài bài) |
| **Các phương pháp dựa trên chuỗi (ví dụ sliding window)** | Không phát hiện được anomaly từ một sự kiện đơn lẻ (single point) | Gián tiếp từ các nhận xét trong mapping (phần multi-event) | Phương pháp phát hiện anomaly tại mức sự kiện hoặc bổ sung context qua memory mạng | Cải tiến: học biểu diễn event (embedding) kết hợp với ngữ cảnh hệ thống; hoặc sử dụng mạng attention để tập trung sự kiện quan trọng | Cải thiện khả năng phát hiện các sự kiện đặc biệt không nằm trong mẫu lớn | Có thể tăng FPR nếu không có bối cảnh đầy đủ | Trung bình (kinh nghiệm chung) |

*Mỗi hàng chỉ nêu hạn chế có bằng chứng đủ mạnh.* Ví dụ, LAnoBERT có bằng chứng trực tiếp về OOV và parsing, do đó cải thiện hướng vào xử lý từ mới/token động. LogSentry nặng và KB tĩnh, cần cải tiến phương thức lưu trữ/cập nhật. Hướng cải tiến tiềm năng gồm: phân đoạn subword, thu thập tri thức mới, tối ưu hóa truy vấn, mở rộng mô hình vào streaming logs, v.v.

# 10. Xếp hạng các ứng viên cải tiến

Đánh giá các ý tưởng cải tiến dựa trên: bằng chứng ủng hộ, tác động, tính mới, tính khả thi, độ phức tạp, rủi ro.

| Ứng viên cải tiến                                | Bằng chứng           | Tác động | Mức mới lạ | Tính khả thi | Dễ đánh giá | Độ phức tạp | Rủi ro | Tổng quan |
|---------------------------------------------|---------------------|----------|------------|--------------|-------------|------------|-------|-----------|
| **Tích hợp truy hồi (RAG) vào baseline**       | Có: LogSentry chứng minh cải thiện hiệu năng | Cao (cải thiện accuracy) | Trung bình (RAG đang phổ biến) | Trung bình (cần hệ thống truy vấn) | Khó (cần kiểm tra độ trễ và độ chính xác) | Cao (tích hợp KB, tuning) | Trung bình (chi phí, stale) | Ưu tiên (bằng chứng thực nghiệm mạnh) |
| **Embedding động (subword/BPE) cho logs**      | Có: LAnoBERT nêu OOV làm yếu điểm | Trung bình (cải thiện recall với logs mới) | Trung bình | Cao (có nhiều thư viện BPE) | Trung bình (benchmark F1) | Trung bình (cần train lại ngôn ngữ) | Thấp (phổ biến, chi phí training) | Cao (đã có bài nêu, cải thiện rõ rệt) |
| **Mở rộng bối cảnh dài (transformer memory)**    | Ít (công bố giới hạn) | Trung bình (phát hiện mẫu xa) | Cao (research mới) | Thấp (đòi hỏi tài nguyên lớn) | Khó | Cao | Trung bình (khó training dài) | Thấp (bằng chứng yếu) |
| **Xử lý drift (continual learning)**           | Ít rõ ràng (phần lớn giả định tĩnh) | Cao (cần thiết cho môi trường thực) | Trung bình | Trung bình (vẫn nghiên cứu) | Trung bình | Cao | Cao (quên lãng cat) | Thấp–Trung bình |
| **Đồ thị tri thức (Knowledge Graph)**         | Ít (còn sơ khai) | Trung bình | Cao | Thấp | Khó | Rất cao | Rất cao (cần tích hợp phức tạp) | Thấp |

**Ưu tiên:** 1) *Tích hợp truy hồi (RAG)*: có bằng chứng [78] cho thấy hiệu quả cải thiện. 2) *Embedding động (subword)*: có bằng chứng nhu cầu từ LAnoBERT, dễ triển khai. Các ý tưởng khác (context dài, drift, knowledge graph) chưa có bằng chứng rõ, nên xếp sau vì khó khăn và rủi ro cao.

# 11. Gap nghiên cứu dựa trên bằng chứng

Các gap nghiên cứu ưu tiên chính:

- **Gap 1: Từ vựng tĩnh và parsing trong LogBERT (LAnoBERT)**  
  - **Baseline:** LAnoBERT (Applied Soft Computing 2023).  
  - **Bằng chứng:** Tác giả nêu rõ: vocab cố định gây **OOV**; embeddings phụ thuộc kết quả parsing.  
  - **Nguyên nhân:** Logs liên tục xuất hiện các từ/tên mới (dịch vụ, port, ID) không có trong tập huấn luyện; parsing không hoàn hảo.  
  - **Ảnh hưởng:** Phương pháp dễ bỏ sót các anomalies chứa từ mới hoặc phân loại nhầm nếu parsing sai template; giảm hiệu năng trong môi trường thực.  
  - **Công trình liên quan:** Một số nghiên cứu trong xử lý ngôn ngữ (NLP) đã dùng subword (BPE) để giảm OOV, hoặc cải tiến parsing. Chưa có công trình cụ thể áp dụng cho anomaly log.  
  - **Giải pháp hiện có:** Thí nghiệm *Log2Graphs* (SSRN 2023) đề xuất embedding dựa trên đồ thị template nhưng chưa peer-review.  
  - **Cơ hội cải tiến:** Nghiên cứu embedding theo subword/code (ví dụ Byte Pair Encoding), hoặc LLM lĩnh vực logs (Log-oriented GPT), kết hợp RAG để bổ sung thông tin từ logs tương tự.  
  - **Độ tin cậy:** Cao (dựa trên phát hiện rõ ràng của LAnoBERT).  

- **Gap 2: Hạn chế phụ thuộc chuỗi dài (session) khi phát hiện cục bộ**  
  - **Baseline:** Phần lớn phương pháp hiện tại (bao gồm LAnoBERT, LogSentry) cần ít nhất một window log để phát hiện.  
  - **Bằng chứng:** Mặc dù chưa có bài báo cụ thể Q1/Q2 giải quyết, mapping cho thấy các phương pháp dựa trên sequence mong đợi mẫu tuần tự và bỏ sót sự kiện đơn lẻ.  
  - **Nguyên nhân:** Mô hình học theo thứ tự (GRU, Transformer) giả định nhiều log liên quan để xác định abnormal.  
  - **Ảnh hưởng:** Các trường hợp anomalous chỉ thể hiện trong một log (độc lập) không được phát hiện, dẫn đến trễ trong cảnh báo.  
  - **Công trình liên quan:** Một số phương pháp trong anomaly detection (ngoài log) áp dụng kỹ thuật điểm (point-based), chưa thấy phổ biến cho log.  
  - **Giải pháp hiện có:** Linear/one-class SVM trên các feature cá nhân, hoặc các kỹ thuật event-based.  
  - **Cơ hội cải tiến:** Phát triển mô hình kết hợp cả mức phiên (session) và mức sự kiện, ví dụ dùng attention để cân bằng thông tin, hoặc thêm module đánh giá từng log riêng.  
  - **Độ tin cậy:** Trung bình (nhận thấy chung, nhưng thiếu bài cụ thể).  

- **Gap 3: Đánh giá cảnh báo sớm chưa được giải quyết**  
  - **Baseline:** Hầu hết phương pháp không đo lường lead-time.  
  - **Bằng chứng:** Thiếu hẳn metric “time-to-detect” trong các bài của mapping; các tác giả chỉ báo cáo precision/recall.  
  - **Nguyên nhân:** Thiếu chuẩn chung trong cộng đồng về metric cảnh báo sớm; tập benchmark không định nghĩa rõ ràng mục tiêu sớm.  
  - **Ảnh hưởng:** Dù mô hình có phát hiện được anomaly, nhưng không biết nó phát hiện trước hay sau khi lỗi xảy ra; điều này làm giảm giá trị cảnh báo sớm.  
  - **Công trình liên quan:** Có một số nghiên cứu về anomaly detection thời gian (thí dụ IoT, logs dành riêng từ góc độ “early warning”), nhưng chưa phổ biến trong nhóm papers log truyền thống.  
  - **Giải pháp hiện có:** Hướng đi nghiên cứu như ADELE (cập nhật qua Google Scholar) giải quyết mục tiêu cảnh báo sớm trong hệ thống lưu trữ (chưa Q1).  
  - **Cơ hội cải tiến:** Xây dựng giao thức thử nghiệm và metric cụ thể (detection lead time) cho anomaly log, đồng thời cải tiến mô hình để tối ưu metric này.  
  - **Độ tin cậy:** Thấp (chưa có số liệu từ mapping, là kết luận dựa vào thiếu hụt).  

# 12. Định vị nghiên cứu (Research Positioning)

- **Level 1 – Tái hiện lại:** Chỉ tái hiện hoàn toàn một baseline (re-implementation) không đủ.  
- **Level 2 – Cải tiến có định hướng:** Ưu tiên, tập trung cải thiện những nút thắt có bằng chứng. Ví dụ, bổ sung component truy hồi cho LAnoBERT hoặc thêm cơ chế cập nhật từ vựng động. Đây là hướng được đề xuất.  
- **Level 3 – Mở rộng lớn hơn:** Thay đổi nhiều thành phần (ví dụ kết hợp đồng thời RAG, graph, multi-agent) chỉ nên xem xét nếu có lí do thuyết phục. Mục tiêu là cải tiến, không phải tạo hoàn toàn kiến trúc mới mà thiếu căn cứ.  

Chúng ta ưu tiên hướng **Mức 2 (Targeted Improvement)**: tập trung vào cải tiến các thành phần đắt giá đã xác định (embedding động, RAG, temporal context…) dựa trên bằng chứng. Ví dụ, có thể bắt đầu từ *LAnoBERT* hoặc *LogSentry*, thêm một tính năng mới hoặc module mà không tái thiết kế hoàn toàn.

# 13. Benchmark và tính thực tiễn

**Dữ liệu phổ biến:**  
- **HDFS (Hadoop):** Dữ liệu logs từ hệ thống Hadoop. Lớn, hợp mô hình pipeline, nhiều tham số. Tuy nhiên, SynHDFS được tổng hợp nhân tạo cho nghiên cứu (vd. LogBERT). Khó chuyển sang các logs khác biệt.  
- **BGL (Blue Gene/L):** Logs siêu máy tính, dạng syslog. Ít formats, anomaly rất hiếm. Chủ yếu kiểm thử thuật toán trên hệ thống cũ.  
- **Thunderbird:** Logs Hadoop (IBM), có cấu trúc tương tự HDFS nhưng với scenario khác (benchmark).  
- **OpenStack, Spirit:** Lần đầu xuất hiện gần đây; logs đa dạng (cloud) nhưng ít được dùng trên Q1 papers 2023–2026 do muộn.  
- **Sotels (bọn mapping có thể đề cập):** Một số dataset nhỏ chuyên ngành (máy bay, v.v.) có thể được chia sẻ.  

**Đặc điểm cần lưu ý:**  
- **Quy mô:** Nhiều benchmarks còn nhỏ (~10k–100k logs), phù hợp demo. Để đánh giá context dài, kích thước được mở rộng (ví dụ SynHDFS có 6000 sessions).  
- **Loại anomaly:** Hầu hết là point anomalies hoặc collective anomalies đơn giản (vd. mất kết nối, buffer overflow). Thiếu các anomaly kiểu trôi dạt (drift) hoặc tấn công có cấu trúc phức tạp.  
- **Cân bằng:** Tỉ lệ anomaly rất thấp (1–5%), gây mất cân bằng; nhiều phương pháp ít tính đến điều này (LogSentry là ngoại lệ).  
- **Tính thời gian:** Các dataset nói trên không cung cấp metric thời gian thực (trừ time-stamp). Thường tổ chức theo session, không đo lead-time.  
- **Thực tế sản xuất:** Do tập dữ liệu thường nhân tạo hoặc cũ, gap so với logs thực (đa dạng định dạng, volume cao, drift) là đáng kể.  
- **Chéo miền:** Các tập hiện chỉ đại diện hạn chế cho hạ tầng cụ thể (Hadoop, IBM). Không có bộ tổng hợp cho IoT hay logs hệ điều hành hiện đại (trừ các dự án mới).  
- **Rò rỉ thông tin:** Một số bộ cho phép đọc trước event tần số cao hoặc lai ghi nhãn (một chuỗi test bao gồm anomaly từ nhóm train cũ), cần cảnh giác khi so sánh.  

Tóm lại, các benchmark hiện tại có giá trị để so sánh học-thuật cơ bản, nhưng hạn chế tính đa dạng và temporal. Chúng phục vụ cho **phát hiện** dị thường nhưng chưa thực sự phù hợp để đánh giá **cảnh báo sớm** (vì thiếu metric thời gian) và **độ phức tạp thực tế** (domain/thông tin lẫn lộn).

# 14. Tổng hợp cuối

1. **Baseline được chọn:** *LAnoBERT (Applied Soft Computing 2023)* được đề xuất là baseline tốt nhất. Lý do: tạp chí Q1, vấn đề phù hợp (anomaly detection với Transformer), có ý tưởng rõ ràng và có bằng chứng hạn chế về nhược điểm (OOV, parsing). *LogSentry (Sci Rep 2025)* là lựa chọn thay thế tiềm năng do phương pháp RAG hiện đại, nhưng LAnoBERT có ưu thế nghiên cứu rõ ràng về hạn chế cần cải tiến.  

2. **Lý do chọn baseline:** LAnoBERT vừa mới và mạnh (F1 cao), nhưng tác giả đã chỉ ra rõ ràng **hai hạn chế then chốt** (còn thiếu xử lý từ mới và phụ thuộc parsing). Điều này tạo cơ hội nghiên cứu rõ ràng: tập trung khắc phục những điểm yếu đã xác định, thay vì tạo lại toàn bộ phương pháp. 

3. **Hạn chế được xác nhận:** *Mô hình từ vựng cố định khiến OOV, và việc phụ thuộc vào kết quả log parsing*. Cả hai đều được LAnoBERT tự nêu ra. Hạn chế này làm giảm khả năng phát hiện các log chứa ký hiệu mới hoặc dữ liệu không theo format cũ.  

4. **Cơ hội cải tiến:** Phát triển một phương pháp mã hoá linh động hơn: ví dụ ứng dụng **token hoá subword** (như BPE/WordPiece) cho log để giảm OOV, hoặc kết hợp các kiến thức ngoại vi (RAG) để bổ sung thông tin khi gặp log mới. Cụ thể, một ý tưởng là “Dynamic LogBERT” dùng BPE cho tất cả logs hoặc sử dụng một tập dữ liệu log mở rộng để fine-tune trước khi huấn luyện anomaly. Hoặc kết hợp hệ thống truy hồi/KNN tương tự *LogSentry* để xử lý log lạ.  

5. **Bằng chứng hỗ trợ:** LAnoBERT chỉ ra yếu điểm OOV và parsing. Các nghiên cứu (như LogSentry) hỗ trợ cải tiến truy hồi. Đặc biệt, Khan et al. 2024 đã xác nhận việc phụ thuộc parsing không tăng accuracy, là lý do thiết yếu chuyển đổi hướng nghiên cứu (tập trung vào embedding thay vì tối ưu parsing).  

6. **Mức đóng góp dự kiến:** Tập trung cải tiến (Level 2) – bổ sung module hoặc cải biến thành phần (embedding/RAG) trong khung LAnoBERT hiện có. Ví dụ có thể giữ kiến trúc BERT chính và thay đổi cách tokenizer hoặc thêm khối retrieval. Đóng góp sẽ là làm đầy khoảng trống được xác định bởi các tác giả trước (như LAnoBERT đề nghị “kiểm tra các biến thể của BERT embedding” trong tương lai).  

7. **Khả năng thực nghiệm:** Rất khả thi. Dữ liệu HDFS/BGL phổ biến dùng cho LAnoBERT đã có sẵn để tái tạo và so sánh. Việc triển khai cải tiến như token hoá subword hay tích hợp KNN đều khả thi với Python/ML libraries (HuggingFace, FAISS). Thử nghiệm có thể được thực hiện bằng benchmark SynHDFS-6k như LAnoBERT đã làm. Cần lưu ý: nếu muốn chứng minh “sớm hơn” thì bổ sung đánh giá lead-time (giả lập lỗi có time-stamp) là cần thiết, dù các bài gốc không làm. 

**Kết luận:** Baseline LAnoBERT (2023, Q1) là ứng viên tốt nhất vì nó vừa mạnh và công khai hạn chế chính. **Hạn chế đã xác nhận** là phụ thuộc vocab cố định và parsing. **Cơ hội cải tiến** là đưa embedding của log thành động (subword, RAG) để xử lý ký hiệu mới. Đề tài luận văn sẽ tập trung vào **cải thiện nhược điểm đã xác nhận này** (ví dụ bằng phương pháp RAG token nhỏ hơn hoặc BPE), đồng thời đánh giá với tiêu chí cảnh báo sớm (lead-time) để hoàn thiện. Bằng chứng thực nghiệm đã có chỉ rõ cần làm, nên khả năng đóng góp học thuật là rõ ràng, đồng thời có thể thực hiện được trong khuôn khổ luận văn.  

