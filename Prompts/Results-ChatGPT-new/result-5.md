# Thiết kế nghiên cứu cải thiện baseline Q1/Q2 (2023–2026) cho phát hiện sớm bất thường log  

## 1. Kiểm tra tính nhất quán thiết kế nghiên cứu  

| Element             | From result-4 (Proposal)                                  | Design Interpretation                                               | Q1/Q2 & Publication Check                                            | Consistent?      |
|---------------------|----------------------------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------|------------------|
| **Baseline**        | Được chọn là mô hình LogFiT (Almodovar et al., IEEE TNSM 2024).         | Baseline là phương pháp dự đoán token log bằng BERT được fine-tune trên dữ liệu log bình thường. | Journal: IEEE TNSM 2024 (Q1). ISSN thuộc SCIE. DOI:10.1109/TNSM.2024.3358730.| Có (Q1, chính thức). |
| **Limitation**      | “Không có sử dụng kiến thức bên ngoài; độ bao phủ kém đối với bất thường mới” (theo proposal). | Baseline chỉ học từ logs huấn luyện, không khai thác ngữ cảnh hoặc tri thức lịch sử. | –                                                                    | Có               |
| **Improvement**     | Tích hợp cơ chế truy xuất ngữ cảnh (RAG) vào pipeline.    | Thêm thành phần truy xuất dữ liệu log lịch sử liên quan để bổ sung bối cảnh cho mô hình. | –                                                                    | Có               |
| **RQ**              | RQ1/RQ2/RQ3 (proposal) liên quan đến hiệu quả của cải tiến. | Ví dụ: “Cải tiến RAG có cải thiện tỷ lệ phát hiện sớm không?”.   | –                                                                    | Có               |
| **Hypotheses**      | H1/H2/H3 (proposal) về tăng F1, lead-time sớm.            | H1: Tích hợp RAG sẽ tăng chỉ số phát hiện; H2: rút ngắn lead time; H3: chi phí chấp nhận được. | –                                                                    | Có               |
| **Main Metrics**    | Precision, Recall, F1, Lead-time (proposal)               | Các chỉ số phát hiện (Precision/Recall/F1/AUC) và đặc trưng sớm (thời gian phát hiện). | –                                                                    | Có               |
| **Main Dataset**    | Các bộ dữ liệu HDFS, BGL, Thunderbird (proposal). | Sử dụng các tập public logs (HDFS, BGL, Thunderbird) chuẩn đã dùng trong nghiên cứu anomaly detection. | –                                                                    | Có               |

## 2. Phục dựng phương pháp baseline hiện tại  

- **Input:** Dữ liệu log thô từ các hệ thống phân tán (ví dụ HDFS, BGL, Thunderbird) gồm các dòng sự kiện thời gian có thông tin message log.  
- **Tiền xử lý (Parsing):** Tách và làm sạch log sentence; nếu sử dụng parser (Drain/RL) thì chỉ để nhóm sự kiện; LogFiT *không dùng từ điển mẫu* (không gán template), mà coi từng câu log như chuỗi ký tự. Có thể vẫn phân nhóm theo ID (ví dụ HDFS theo block ID thành “đoạn log”).  
- **Biểu diễn (Representation):** Mỗi câu log được mã hóa bằng embeddings từ mô hình ngôn ngữ BERT đã được pretrained (LogFiT dùng BERT base). Cụ thể, câu log được tokenize và chuyển thành vector thông qua BERT. Nếu nhóm thành đoạn log, ta có chuỗi embedding của mỗi câu trong đoạn.  
- **Bối cảnh (Sequence/Context):** Với mỗi window/log đoạn (ví dụ 60 giây hoặc theo session), nối các sentence embedding theo thứ tự thời gian. BERT không có trạng thái ẩn thời gian, nên mỗi câu được xử lý độc lập hoặc với cơ chế attention trên chuỗi embedding đoạn. Baseline không truy xuất dữ liệu ngoài, chỉ dựa trên chuỗi hiện tại.  
- **Mô hình lõi (Core Model):** Mô hình LogFiT là một BERT fine-tuned theo nhiệm vụ Masked Language Modeling trên log bình thường. Quá trình học: cho các câu log bình thường (không có bất thường), mask một số token và huấn luyện BERT dự đoán token bị che. Kết quả là một mô hình nắm được ngữ cảnh “bình thường” của log. (Nguồn: LogFiT, IEEE TNSM 2024).  
- **Tính điểm bất thường (Anomaly Scoring):** Khi phát hiện, cho các câu log mới vào mô hình, và xem độ chính xác dự đoán token hàng đầu (top-k token prediction). LogFiT sử dụng “top-k accuracy” trên mỗi câu làm threshold: nếu độ chính xác dự đoán thấp, đánh dấu bất thường. (Dữ liệu [44†L158-L166] cho thấy F1 của baseline).  
- **Quyết định (Decision):** Nếu tỉ lệ token tiên đoán không khớp vượt ngưỡng (tức sai nhiều hơn bình thường), cửa sổ log hiện tại được coi là chứa bất thường. Ngưỡng có thể đặt dựa trên phân phối sai số của logs bình thường.  
- **Output:** Thông báo nhãn bất thường/không bất thường cho mỗi window/đoạn log. (Mục tiêu là phát cảnh báo sớm khi phát hiện bất thường mới).  

## 3. Xác định cải tiến mục tiêu  

| Component        | Baseline (LogFiT)                   | Journal/Q1-Q2 Evidence      | Limitation                                            | Improvement (Cải tiến)                | Expected Effect                   | Evidence                                       |
|------------------|-------------------------------------|-----------------------------|-------------------------------------------------------|---------------------------------------|-----------------------------------|------------------------------------------------|
| Bối cảnh đầu vào / Representation | BERT-based masked LM (LogFiT) | IEEE TNSM 2024 (Q1) | Chỉ học từ dữ liệu huấn luyện, không có thông tin lịch sử ngoài; dễ bỏ sót bất thường mới. | Thêm truy xuất ngữ cảnh từ log lịch sử (RAG): tìm các mẫu log tương tự trong cơ sở dữ liệu trước đó và nạp vào mô hình. | Cải thiện độ chính xác phát hiện (Precision/F1 tăng) và phát hiện sớm hơn (lead time dài hơn) nhờ thêm thông tin hỗ trợ. | Dự kiến tăng recall/precision (ví dụ: các hệ thống RAG đã báo cáo cải tiến lên đến 60% trong một số ứng dụng).  |

*Chú thích:* Component ở đây là thành phần của pipeline baseline được cải tiến. Ví dụ bảng chỉ minh họa một dòng chính cho cải tiến RAG. 

## 4. Kiến trúc nghiên cứu tổng thể  

Thiết kế tổng thể giữ nguyên pipeline baseline và chèn thêm thành phần truy xuất (RAG) như cải tiến. Các thành phần chính: 
- **Inherited:** Dữ liệu log, bước parsing, biểu diễn bằng embeddings, mô hình baseline (BERT fine-tune), việc tính điểm bất thường và đánh giá dữ liệu. 
- **Modified:** Thành phần ngữ cảnh đầu vào được mở rộng bằng các bản ghi lịch sử retrieved. 
- **New:** Thành phần *Retriever/Memory* – xây dựng chỉ mục log lịch sử và module truy vấn; bộ chứa tri thức (có thể là KB hoặc index) để lưu trữ logs trước đó.  
- **Optional:** Nếu cần, có thể thêm phần giải thích/phản hồi (explainable alert) cho kết quả.  

Như vậy, pipeline kế thừa phần lớn từ Baseline (BERT, cách xử lý log), chỉ bổ sung thêm việc truy xuất thông tin từ logs lịch sử. Không thay đổi mô hình BERT gốc (mô hình lõi vẫn giữ nguyên) để đảm bảo độ so sánh công bằng; chỉ thêm bước sử dụng thông tin mới để nâng cao hiệu quả phát hiện.

## 5. Quy trình dữ liệu và pipeline thời gian  

- **Raw Logs:** Dòng log liên tục (real-time) hoặc batch từ các hệ thống giám sát (input stream). Mỗi log ghi nhận timestamp và nội dung sự kiện.  
- **Parsing:** Áp dụng công cụ parsing (ví dụ Drain) để tách lấy thành phần message (hoặc không nếu dùng raw text). Mục tiêu lọc bớt chi tiết không cần thiết, ánh xạ log vào câu thông điệp. Đầu ra là chuỗi câu log đã làm sạch. (Tương tự baseline).  
- **Windowing/Grouping:** Gom các log liên tiếp thành các cửa sổ (windows) dựa trên thời gian (ví dụ 1 phút) hoặc ID (ví dụ block ID của HDFS), tạo thành “đoạn log” liên tục. Bước này giống pipeline baseline và chuẩn bị ngữ cảnh đầu vào cho mô hình.  
- **Representation:** Mỗi câu trong cửa sổ được biểu diễn bằng vector embedding (qua BERT như baseline). Chuỗi embedding của cửa sổ này dùng làm input cho mô hình phát hiện.  
- **Cải tiến (RAG Retrieval):** Tại đây, dùng embedding hoặc câu log hiện tại làm truy vấn. Thực hiện truy xuất trên *corpus* logs lịch sử (ví dụ index cosine similarity trên embeddings lưu trữ) để lấy các đoạn log tương tự (context) đã xảy ra trước đó. Kết quả retrieval (top-K đoạn log) được gắn vào input: có thể nối vào window hiện tại hoặc đưa thêm thông tin cho mô hình. Bước này là cải tiến so với baseline.  
- **Detection:** Dùng mô hình baseline (BERT MLM) trên cả ngữ cảnh gốc và thông tin mới để tính điểm bất thường. Kết quả là score/lần cảnh báo.  
- **Early Detection Evaluation:** Tính các chỉ số phát hiện sớm (lead-time, time-to-detect, false alarms) dựa trên thời điểm cảnh báo so với thời điểm gốc của lỗi (nếu có).  
- **Alert:** Khi score vượt ngưỡng, hệ thống phát cảnh báo cảnh báo sớm bất thường. Kết quả này ghi nhận cho đánh giá.  

Pipeline cải tiến chủ yếu khác baseline ở chỗ có thêm khâu “Cải tiến” (Retrieval), còn các bước khác giữ giống để kiểm soát thử nghiệm.

## 6. Thiết kế dữ liệu theo thời gian  

- **Thứ tự log (Timestamp/Order):** Log được xử lý theo thứ tự thời gian. Mỗi bản ghi log gắn timestamp. Pipeline tuân thủ strict FIFO, không dùng dữ liệu tương lai cho dự đoán hiện tại (không có *future leakage*).  
- **Observation Window:** Cửa sổ quan sát (ví dụ 60s hoặc định lượng số câu) bao gồm các log đã ghi trong khoảng thời gian trước đó. Ví dụ, mỗi 30s hoặc 1 phút lấy một cửa sổ để dự đoán.  
- **Context Window:** Với mỗi khoảng thời gian quan sát, ngữ cảnh đầu vào cho mô hình là những log trong window đó. Đối với RAG, context còn bao gồm cả các log tương tự được truy xuất (từ logs trước đó, cứng tuổi hơn). Chúng ta đảm bảo chỉ truy xuất log có timestamp **nhỏ hơn** thời điểm hiện tại.  
- **Prediction Horizon:** Mục tiêu là phát hiện ngay trong thời gian thực khi lỗi sắp xảy ra. Khoảng cách (horizon) giữa dữ liệu dùng cho dự báo và thời điểm sai lệch thực sự càng nhỏ càng tốt. Thiết kế tập trung on-line, tức độ trễ gần như bằng 0.  
- **Thời điểm bất thường/lỗi:** Giả sử có nhãn sự kiện “failure” tại thời điểm T_true. Early detection là phát hiện bất thường trong khoảng T < T_true.  
- **Lead Time:** Đo khoảng thời gian giữa lần cảnh báo (T_alert) và T_true. Lead time dương nghĩa là phát hiện sớm (alert trước failure).  
- **Kiểm soát rò rỉ thông tin:** Bảo đảm rằng mọi dữ liệu từ sau T_current (đang xét) đều không được dùng. Đặc biệt với retrieval, chỉ index log **trước** thời điểm phân tích. 

Với logs lịch sử hay runbook, luôn lưu ý điều kiện thời gian: chỉ dùng kiến thức từng xảy ra trước thời điểm dự báo. Điều này đảm bảo tính thực tế và tránh đánh giá quá lạc quan.

## 7. Thiết kế kiến thức / truy xuất  

- **Nguồn tri thức (Knowledge):** Sử dụng kho logs lịch sử đã thu thập (vd. logs vận hành thực tế) làm cơ sở tri thức. Có thể mở rộng bằng tài liệu runbook, mô tả hệ thống, kiến thức chuyên gia nếu liên quan. Tuy nhiên, sơ bộ dùng logs lịch sử vì phù hợp nhất với dữ liệu đầu vào.  
- **Truy vấn (Query):** Mỗi khi một window log mới xuất hiện, ta tạo truy vấn như vector embedding của window đó hoặc embedding của câu khóa quan trọng. Ví dụ, dùng vector embedding trung bình của window, hoặc concat các embedding.  
- **Truy xuất (Retrieval):** Thực hiện tìm kiếm (ví dụ nearest neighbors) trên cơ sở dữ liệu embeddings logs lịch sử để lấy các window tương tự nhất. Lọc các window đó theo thời gian (nhỏ hơn hiện tại) và ý nghĩa (ngữ cảnh tương đồng).  
- **Kết quả (Filtering/Ranking):** Chọn Top-$K$ (vd. K=5) window tương tự có độ tương đồng cao. Xếp hạng theo cosine-similarity. Loại bỏ nếu thông tin không liên quan hoặc quá cũ (tùy thiết kế).  
- **Tích hợp (Context Injection):** Kết quả retrieve được nối vào ngữ cảnh xử lý: có thể cộng các embeddings retrieved vào input của mô hình, hoặc tổ chức như tập hợp các ví dụ hỗ trợ.  
- **Cải thiện:** Baseline thiếu kiến thức xuyên lịch sử và phán đoán theo ngữ cảnh rộng. Cải tiến đã xử lý điểm này bằng cách đưa vào thông tin từ các logs tương tự đã lưu (cụ thể hơn: log đã biết là bình thường/không bất thường trong tình huống tương ứng). Nhờ đó, mô hình có thêm bối cảnh để phân biệt “bất thường thực” so với biến thể mới chưa từng gặp.

## 8. Thiết kế mô hình nền tảng / học máy  

- **Vai trò mô hình nền tảng:** Baseline sử dụng mô hình BERT (transformer cỡ trung bình) đã được pretrained (Ví dụ BERT-base) làm thành phần chính. Mô hình này nhận đầu vào là các câu log (đã embedding) và học dự đoán token tiếp theo (masked LM) trên logs bình thường. Mô hình này không thay đổi trong thiết kế mới.  
- **Đầu vào/Đầu ra:** Baseline input: embedding của chuỗi log hiện tại; output: xác suất của token (sử dụng cho top-k accuracy). Cải tiến (retrieval) không thay đổi đầu ra là xác suất token hay điểm bất thường, chỉ bổ sung thêm đầu vào.  
- **Huấn luyện:** Sử dụng việc huấn luyện tự giám sát (self-supervised) trên các log bình thường (không có nhãn bất thường). Không có phần học mới hướng dẫn cải tiến (không fine-tune thêm BERT cho RAG). Tức, mô hình chỉ huấn luyện theo baseline ban đầu, phần RAG không yêu cầu training (chỉ lập chỉ mục và tìm kiếm).  
- **Không Fine-tune khác:** Không thêm việc fine-tune mô hình mới hoặc học chuyển giao (PEFT) vào cải tiến vì tăng độ phức tạp và cần nhiều tài nguyên. Nếu có LLM (như GPT) dùng cho reasoning, ta chỉ sử dụng inference mà không đào tạo lại (nếu cần). 

**Ghi chú:** Thành phần học (learning) chủ yếu đã hoàn thành ở baseline. Cải tiến chính là phần kiến thức bên ngoài, không thêm bước huấn luyện lớn nào mới. 

## 9. Chiến lược suy luận  

- **Đầu vào:** Khi một cửa sổ log mới (window) được tạo, hệ thống ngay lập tức thực hiện xử lý. Suy luận online: mọi bước đều diễn ra trực tiếp khi log đến, không chờ batch offline lớn.  
- **Context/Window:** Sử dụng toàn bộ nội dung của cửa sổ cùng với kết quả truy xuất (nếu có). Sau bước parsing, tạo embedding và bổ sung ngữ cảnh từ retrieval.  
- **Truy xuất (nếu có):** Một thành phần thực hiện tìm kiếm trên log lịch sử trong thời gian thực. Có thể song song khi xử lý baseline để giảm độ trễ. Ví dụ, đồng thời với việc BERT tính toán, module retrieval truy vấn vector DB và trả về context.  
- **Suy luận (Baseline + Cải tiến):** Mô hình BERT nhận đầu vào mở rộng (câu log + ngữ cảnh) và thực hiện dự đoán. Tính score bất thường dựa trên top-k accuracy (như baseline). Nếu sử dụng GPT hoặc LLM lớn trong pipeline (optional), sẽ được gọi sau khi context đã được chuẩn bị (ví dụ hỏi LLM “Dựa trên đoạn log hiện tại và bối cảnh lịch sử, có bất thường không?”) nhưng trong thiết kế tối giản, chúng ta không cần đến.  
- **Score bất thường:** Tính chỉ số (ví dụ top-k token accuracy) cho cả đầu vào gốc. Nếu kết quả dưới ngưỡng, gắn nhãn bất thường. Có thể kết hợp điểm từ retrieved context (ví dụ đánh giá thêm: nếu logs tương tự trước đó bình thường/ngưng hoạt động thì xác suất cao có bất thường).  
- **Early Detection:** Ngay khi score vượt ngưỡng, kích hoạt cảnh báo. Đây là bước online, không chậm trễ nhiều.  
- **Độ trễ:** Tối ưu truy vấn để không gây quá tải. Ví dụ, có thể precompute index embeddings logs. BERT inference tốc độ đủ nhanh cho real-time (tùy vào năng lực phần cứng). Khâu phân tích và hỏi O(1) với retrieve, inference bằng BERT chủ yếu tốn thời gian GPU.  
- **Online vs Offline:** Training mô hình (baseline) và xây dựng index logs lịch sử được thực hiện offline. Giai đoạn phát hiện anomaly thực hiện online. Thao tác ngoại tuyến: xây dựng vector DB cho retrieval; trực tuyến: streaming inference và retrieval query.  

## 10. Thiết kế thí nghiệm  

- **E1 – Tái lập baseline:** Thực hiện thí nghiệm baseline (LogFiT) với các tham số báo cáo, trên HDFS/BGL/Thunderbird. Ghi lại chỉ số (Precision/Recall/F1) và so sánh với kết quả đăng báo. Nếu có sai lệch lớn, kiểm tra nguyên nhân (thuật toán parsing, ngưỡng, seed).  
- **E2 – Đánh giá cải tiến chính:** So sánh trực tiếp *Baseline* vs *Baseline+RAG*. Cố định mọi thứ (dữ liệu, phân chia train/test, mã nguồn) ngoài thành phần truy xuất được thêm vào. Ghi chỉ số chính (Precision, Recall, F1, AUC). Mục tiêu: kiểm định H1/H2, xem RAG có cải thiện độ chính xác.  
- **E3 – Ablation:** Phân tích tác động của thành phần cải tiến: Ví dụ, “chỉ phân tích Baseline vs Baseline với retrieval tĩnh (không update), vs Baseline với retrieval kết hợp”. Hoặc thử chỉ thêm bước lookup (“phát hiện ban đầu, rồi truy xuất chỉnh sửa”). Tương tự, có thể thử tập hồi hồi tiếp retrieval. Mục đích xác định thành phần cải tiến đóng góp thế nào.  
- **E4 – Đánh giá phát hiện sớm:** Tính và so sánh các chỉ số lead-time (detection lead time, time-to-detection) cho Baseline và Baseline+RAG. Đo tỷ lệ cảnh báo sớm (đúng phát hiện trước sự cố) và false alarm. Kiểm định xem cải tiến tăng lead time bao nhiêu giây (hoặc %cases).  
- **E5 – Robustness:** Thử các kịch bản nhiễu/phân phối khác: ví dụ thay đổi format log, thêm bớt event mới. Đánh giá xem Baseline và Cải tiến ảnh hưởng ra sao. Nếu retrieval giúp làm cho mô hình dẻo hơn (vì có ví dụ rộng hơn), thì các thử nghiệm này sẽ cho thấy sự khác biệt.  
- **E6 – Hiệu quả (Efficiency):** Đo chi phí thực thi: latency (ms), throughput (logs/s), bộ nhớ, chi phí token nếu dùng API. So sánh Baseline và Baseline+RAG, tính overhead do retrieval tạo ra. Đánh giá xem liệu độ trễ có phù hợp real-time không (VD: <200ms).  
- **E7 – Khả năng tổng quát (Generalization):** Nếu khả thi, chạy thử trên hệ thống/log khác (không phải HDFS/BGL) để xem cải tiến có cải thiện trên nhiều loại log không. Ví dụ logs Apache, hệ thống mạng, v.v. (để đánh giá hạn chế domain bias).  

Mỗi thí nghiệm gồm các tham số cố định khác, chỉ thay đổi mục tiêu cần so sánh. Kết quả báo cáo gồm giá trị trung bình và phương sai từ nhiều lần chạy (nếu có tính ngẫu nhiên).

## 11. Chỉ số đánh giá  

- **Detection (Phát hiện):** Precision, Recall, F1-score là chỉ số chính. Ngoài ra PR-AUC (Area under PR curve) để tổng quan, ROC-AUC nếu dữ liệu cân bằng. Đánh giá dựa trên nhãn bất thường được gắn sẵn từ dataset.  
- **Early Detection (Phát hiện sớm):** Thời gian để phát hiện (time-to-detection) tính từ đầu sự cố, Lead Time (thời gian cảnh báo trước lỗi). Tỉ lệ cảnh báo sớm (Early Warning Rate): phần trăm lần phát hiện trước khi lỗi thực sự xảy ra. Tỉ lệ False Alarm (một phần của Precision/Recall). Tập trung vào khả năng phát hiện sớm nhất có thể.  
- **Hiệu quả (Efficiency):** Latency trung bình và đỉnh mỗi bản ghi (ms), thông lượng (logs/giây), chi phí tính toán (số token nếu dùng LLM, thời gian GPU). Bộ nhớ sử dụng (nếu lập index).  
- **Thành phần cụ thể:** Nếu có retrieval: độ chính xác và độ đầy đủ của truy xuất (ví dụ precision/recall đối với việc lấy context liên quan). Nếu có memory: độ chính xác truy vấn trong memory. Nếu reasoning (LLM): đánh giá tính nhất quán/phản hồi của LLM (nếu dùng).  

Các chỉ số chọn phải phục vụ RQ/Hypothesis: Ví dụ RQ1 sử dụng F1, RQ2 sử dụng Lead Time.

## 12. Thiết kế thống kê  

- **Số lần chạy lặp lại:** Mỗi thiết lập (Baseline vs Improved) chạy nhiều lần (ví dụ 5–10 lần) với seed khác nhau để thu thập phân phối kết quả.  
- **Khoảng tin cậy & Đánh giá ý nghĩa:** Tính CI95% cho mỗi chỉ số và thử nghiệm thống kê (t-test hay Wilcoxon) để so sánh hai nhóm kết quả (Baseline vs Improved). Báo cáo p-value và effect size để chắc chắn sự khác biệt có ý nghĩa.  
- **Kiểm soát ngẫu nhiên (seed):** Cố định seed cho thành phần ngẫu nhiên (nếu có, ví dụ train/test split). Báo cáo trung bình ± độ lệch chuẩn. Không chỉ lấy một kết quả tốt nhất.  
- **Nếu dùng LLM/API (stochastic):** Cố định version model, điều chỉnh temperature=0 nếu cần. Chạy nhiều inferences để xác định biến thiên.  
- **Năng lực tính toán:** Dùng cùng loại phần cứng cho cả Baseline và Improved để tránh sai lệch do khác biệt.  

Mục tiêu: kết quả tin cậy, có chứng cứ định lượng cho tuyên bố tăng hiệu quả.

## 13. Các biến kiểm soát  

| Biến               | Baseline                   | Cải tiến                     | Được kiểm soát? |
|--------------------|----------------------------|------------------------------|-----------------|
| **Dữ liệu (Dataset)**        | HDFS, BGL, Thunderbird (công khai) | Giống baseline                | Có              |
| **Phân chia (Train/Test)**   | Sử dụng split xác định           | Giống baseline                | Có              |
| **Tiền xử lý (Parsing)**     | Ví dụ dùng Drain hoặc parse tool   | Giống baseline                | Có              |
| **Biểu diễn (Embedding)**    | BERT-base chuẩn                 | Giống baseline                | Có              |
| **Mô hình (Model)**          | BERT fine-tuned (LogFiT)       | Giữ nguyên phần BERT          | Có (chỉ thêm retrieval) |
| **Thành phần RAG**   | Không có                        | Có                            | Đổi              |
| **Đánh giá (Protocol)**     | Precision/Recall/F1           | Giống baseline                | Có              |
| **Phần cứng/Soft**          | GPU/CPU giống, cùng thư viện    | Giống baseline                | Có              |

*Mục tiêu:* Giữ tất cả yếu tố cố định, chỉ thay đổi thành phần cải tiến Retrieval. Nhờ đó, mọi khác biệt kết quả có thể quy cho cải tiến RAG duy nhất.

## 14. Logic quy kết (Attribution Logic)  

Nếu hiệu năng cải tiến tăng, nguyên nhân chính được cho là do thành phần thêm (truy xuất ngữ cảnh). Bởi vì phần còn lại của pipeline (dữ liệu, preprocessing, mô hình, tham số) được giữ nguyên trong E2/E3. Do đó, sự khác biệt kết quả có thể quy cho RAG. Cụ thể: nếu Precision/F1 tăng, chúng ta giả thiết là do RAG cung cấp thêm mẫu chuẩn từ lịch sử giúp mô hình nhận ra bất thường tốt hơn. Nếu lead time tăng, điều này cũng rõ ràng do việc truy vấn cho phép cảnh báo từ sớm. Trong các thí nghiệm ablation (E3), loại bỏ cải tiến (retrieval) sẽ phải trả về hiệu năng baseline, củng cố giả thuyết rằng chính cải tiến mang lại lợi ích. 

Tóm lại, sự so sánh có kiểm soát giữa Baseline và Baseline+Improvement sẽ chỉ ra chênh lệch do cải tiến. Nếu cần, ta cũng tiến hành thử cắt bỏ một phần retrieval (partial RAG) để đánh giá tác động riêng của từng bước (ví dụ, chỉ sử dụng top-1 vs top-5 logs từ retrieval). Kết quả kiểm soát sẽ giúp khẳng định lý do cải tiến hiệu quả.

## 15. Các phương án thiết kế thay thế  

**A – Minimal:** Chỉ thêm bước truy xuất sau khi mô hình baseline tính điểm. Ví dụ: Baseline tính score bất thường, nếu nghi ngờ, thực hiện tìm kiếm thêm logs tương tự và điều chỉnh score. Ưu điểm: Đơn giản, tích hợp dễ dàng. Khuyết điểm: Chậm trễ thêm bước sau phát hiện.  

**B – Refined:** Kết hợp trực tiếp context của retrieval vào đầu vào BERT. Ví dụ: ghép chuỗi câu log tương tự vào window trước khi tính score. Hiệu quả hơn vì mô hình cùng lúc xem log mới và lịch sử. Phức tạp hơn, cần chỉnh sửa pipeline.  

**C – Robust:** Ngoài retrieval, xây dựng Knowledge Graph của log events hoặc dùng GPT để lý giải. Ví dụ: lược đồ tri thức thể hiện mối quan hệ giữa các sự kiện log, hoặc gọi LLM để phân tích kết hợp log hiện tại và retrieved logs. Rất mạnh nhưng phức tạp nhất, vượt quá mục tiêu “tối giản và có kiểm soát”.  

**Lựa chọn:** Chọn phương án **A – Minimal**, vì nó đơn giản nhưng đủ để kiểm định giả thuyết (có thay đổi lớn nào hay không). Nếu phương án A thành công, có thể triển khai B hoặc C sau.  

## 15A. Xác minh tính đủ điều kiện của baseline cuối cùng  

- **Baseline đúng giai đoạn (2023–2026)?** Có, LogFiT năm 2024 (thỏa).  
- **Loại công bố?** IEEE TNSM là bài báo tạp chí đã peer-review, đã xuất bản chính thức (số tháng 4/2024).  
- **Journal Q1/Q2?** IEEE TNSM thuộc hạng Q1 (Computer Science, SCIE; JIF ~5.7).  
- **Bằng chứng xếp hạng:** Clarivate JCR/Nhóm từ thông tin JIF & SCImago cho thấy Q1 (các nguồn ghi nhận TNSM Q1).  
- **DOI/Metadata:** DOI 10.1109/TNSM.2024.3358730 có trên trang chính thức.  
- **Baseline đúng đề xuất?** Có, đây là baseline đã được duyệt trong result-4.  
- **Không thay bằng paper khác:** Giữ nguyên, không thay đổi baseline do điều kiện phù hợp.  
- **Limitation/Improvement khớp đề xuất:** Có, chúng ta sử dụng limitation và improvement đã xác định trong proposal (đã minh họa ở trên).  

**Kết luận:** Baseline thỏa mãn tất cả điều kiện Q1/Q2, 2023–2026, peer-review, có DOI. Thiết kế nghiên cứu tiếp tục hợp lệ.

## 16. Lựa chọn thiết kế nghiên cứu cuối cùng  

| Design Choice    | Selected Option                        | Reason                                                                    |
|------------------|----------------------------------------|---------------------------------------------------------------------------|
| **Baseline**     | LogFiT (IEEE TNSM, 2024)              | Tạp chí Q1 gần đây, phù hợp chủ đề. Đã được phê duyệt trong proposal.       |
| **Main Improvement** | Truy xuất ngữ cảnh (RAG)         | Giải quyết trực tiếp hạn chế về kiến thức/ngữ cảnh lịch sử của Baseline.   |
| **Data**         | HDFS, BGL, Thunderbird (LogHub)       | Dữ liệu công khai tiêu chuẩn, dùng trong baseline và nhiều nghiên cứu. |
| **Learning**     | Self-supervised MLM (BERT fine-tune)  | Áp dụng như baseline (không thêm học mới lớn).                             |
| **Inference**    | Online: BERT + retrieval             | Giữ pipeline online; thêm truy vấn context trước khi đánh giá.             |
| **Evaluation**   | Precision/Recall/F1; Time-to-detect; Overhead | Đánh giá toàn diện cả chất lượng phát hiện và chi phí thực thi.           |

**Lý do chọn phương án tối giản:** Bảo toàn mô hình và dữ liệu đã có, chỉ thêm retrieval để kiểm chứng tác dụng. Thiết kế này đủ minh chứng hypothesis, đồng thời khả thi trong 6–9 tháng.

## 17. Ma trận truy xuất nghiên cứu (Traceability Matrix)  

| Research Element | Design Element           | Experiment(s) | Metric                        | Evidence of Success                        |
|------------------|--------------------------|---------------|-------------------------------|--------------------------------------------|
| **RQ1:** Hiệu quả phát hiện | So sánh Baseline vs Baseline+RAG | E2           | Precision/Recall/F1/AUC       | F1 và precision cải thiện đáng kể           |
| **RQ2:** Phát hiện sớm    | So sánh hai hệ thống & đo lead time | E2, E4     | Time-to-detect, Lead Time, EAR (Early Warning Rate) | Thời gian phát hiện sớm hơn, lead-time tăng |
| **RQ3:** Chi phí & phổ quát | So sánh hiệu năng và trên domain khác | E6, E7     | Latency, Throughput, Accuracy cross-dataset | Overhead chấp nhận được; hiệu năng giữ ổn định  |
| **H1:** F1 tăng            | Baseline vs Baseline+RAG        | E2           | F1, Precision/Recall          | Hệ thống cải tiến có F1 cao hơn thống kê     |
| **H2:** Cảnh báo sớm       | Baseline vs Baseline+RAG        | E4           | Lead Time                     | Lead Time dài hơn (cảnh báo trước nhiều hơn)|
| **H3:** Overhead nhỏ       | Baseline vs Baseline+RAG        | E6           | Latency, Throughput           | Độ trễ tăng không đáng kể; thông lượng đủ cao |

Mỗi RQ/Hypothesis sẽ gán thí nghiệm tương ứng để kiểm chứng, với chỉ số đo lường rõ ràng và tiêu chí thành công cụ thể như trên.

## 18. Các mối đe dọa đến tính đúng đắn (Threats to Validity)  

- **Nội bộ (Internal):** Mismatch trong triển khai baseline (ví dụ cài lại BERT khác tham số). Thiết lập ngưỡng quyết định có thể ảnh hưởng so sánh. Bên cạnh đó, tuning tham số có thể vô tình ưu đãi bên cải tiến. Kiểm soát bằng cách dùng đúng mã nguồn tham khảo và giữ các tham số giống nhau.  
- **Ngoại lệ (External):** Dataset HDFS/BGL có thể không phản ánh mọi loại hệ thống. Kết quả có thể không tổng quát cho mọi bài toán log anomaly khác (benchmark bias). Tính khả dụng dữ liệu thực tế giới hạn (log có nhãn).  
- **Tổ hợp (Construct):** Metric F1/lead-time có thể không hoàn toàn phản ánh khả năng cảnh báo thực tế. Nhãn bất thường trong tập dữ liệu có thể không khớp chính xác thời điểm lỗi hệ thống, làm sai lệch đánh giá early detection.  
- **Mô hình nền tảng (Foundation Model):** Nếu dùng LLM ngoài (không có ở thiết kế chính), có thể gặp vấn đề drift của model, không tái lập được. Cũng có thể nhạy với prompt nhưng nếu ta không dùng GPT trong thiết kế cuối thì tránh được.  
- **Truy xuất (Retrieval):** Nguy cơ rò rỉ thông tin nếu vô tình truy xuất log từ tương lai (đã kiểm soát temporal ở trên). Thông tin cũ có thể lỗi thời (ví dụ kiến thức vận hành thay đổi). Dữ liệu retrieved có thể không liên quan (retrieval bias).  
- **Kết luận:** Số lần chạy ít, phạm vi datasets giới hạn. Variance kết quả có thể cao (nếu sampling ngẫu nhiên). Kết quả cải thiện có thể chỉ đặc hiệu với tập HDFS/BGL, cần cảnh báo hạn chế phạm vi.  

Nhìn chung, cần cẩn thận khi diễn giải kết quả, đảm bảo mọi thay đổi đều đến từ cải tiến đã chỉ định.

## 19. Rủi ro và biện pháp giảm thiểu  

| Risk (Rủi ro)                                 | Probability (Xác suất) | Impact (Tác động) | Mitigation (Giảm thiểu)                                              | Fallback                       |
|-----------------------------------------------|------------------------|-------------------|----------------------------------------------------------------------|--------------------------------|
| **R1:** Không tái lập được kết quả baseline   | Medium                 | High              | Kiểm thử lặp lại với các tham số như bài báo. Sử dụng code gốc nếu có. | Giảm scope (so sánh tương đối thay vì tuyệt đối). |
| **R2:** Cải tiến không cho hiệu quả vượt trội   | Medium                 | Medium            | Nếu không hiệu quả, thử các cấu hình khác của retrieval (K, filtering). | Dùng lại baseline (nhận ra giới hạn nghiên cứu). |
| **R3:** Kết quả chỉ áp dụng với HDFS/BGL      | Medium                 | Medium            | Thử nghiệm trên thêm dataset/log khác trong khả năng.               | Chỉ tuyên bố giới hạn ứng dụng. |
| **R4:** Chi phí tính toán quá cao (latency, memory) | Low/Medium          | High              | Tối ưu code/truy vấn; dùng indexing hiệu quả. Giới hạn K retrieval.  | Giảm độ phức tạp retrieval, ví dụ K nhỏ hơn. |
| **R5:** Truy xuất thông tin không ổn định       | Medium                 | Medium            | Tinh chỉnh thuật toán retrieval, test robust (E5).                   | Loại bỏ retrieval hoặc cải tiến thuần túy nội tại mô hình. |
| **R6:** Thiếu dữ liệu/bất thường làm benchmark | Low/Medium             | Medium            | Dữ liệu nhân tạo, tổng hợp thêm logs lỗi nếu cần.                    | Hạn chế thí nghiệm đơn, tập trung phân tích chi tiết trên ít data. |

*Biện pháp dự phòng (Fallback):* Trong trường hợp rủi ro xảy ra, ưu tiên giảm phạm vi nghiên cứu (ví dụ chỉ tập trung vào từng component nhỏ của cải tiến) hoặc dùng biến thể đơn giản hơn của cải tiến để đảm bảo có kết quả có thể phân tích được.  

## 20. Đóng góp nghiên cứu kỳ vọng  

- **Khoa học:** Cung cấp bằng chứng thực nghiệm về hiệu quả của việc kết hợp RAG trong phát hiện bất thường log sớm. Chứng minh giới hạn của phương pháp hiện tại và hiệu ứng của retrieval trên chất lượng phát hiện.  
- **Phương pháp:** Phát triển một cách tiếp cận có kiểm soát (controlled enhancement) cho vấn đề log anomaly: giữ baseline nhưng thêm thành phần knowledge, từ đó làm rõ mối quan hệ nhân quả. Đóng góp khung đánh giá đồng nhất cho phát hiện sớm.  
- **Kỹ thuật (Engineering):** Xây dựng pipeline rõ ràng, có thể tái lập, kết hợp mô hình ML và hệ thống thông tin retrieval. Công bố code và hướng dẫn tái lập (nếu khả thi) để hỗ trợ cộng đồng.  
- **Công nghiệp:** Nếu thành công, cải tiến này giúp tăng khả năng cảnh báo sớm trong giám sát hệ thống, giảm thiểu downtime và thiệt hại. Cung cấp hướng dẫn thiết kế hệ thống log-analytics trong môi trường thực tế với kiến thức lịch sử.  

## 21. Khả năng tái lập (Reproducibility)  

- **Baseline:** Sử dụng mô hình BERT-base (thuật toán như LogFiT) với weights công khai. Cố gắng sử dụng cùng phiên bản BERT và tokenizer như trong paper. Ghi rõ commit hoặc phiên bản của mô hình (ví dụ HuggingFace `bert-base-cased`).  
- **Data:** Chỉ định rõ phiên bản tập dữ liệu: HDFS log của Yahoo (2010), BGL của BlueGene/L (2009) và Thunderbird (Hadoop) có nguồn gốc, bao gồm preprocessing script (drain, mẫu). Ghi rõ seed nếu chia train/test ngẫu nhiên.  
- **Preprocessing:** Cung cấp mã hoặc tham chiếu thuật toán parse (ví dụ Drain v1.0) cùng cấu hình (depth, param).  
- **Mô hình:** Luôn sử dụng cùng kiến trúc BERT; fix seed của torch/NumPy khi train. Không sampling. Huấn luyện MLM với learning rate, batch size và epochs được thống kê rõ.  
- **Retrieval:** Ghi phiên bản thư viện (faiss, annoy) và cách tạo index log (embedding model dùng, metric). Chỉ số K chọn (ví dụ K=5).  
- **Inference:** Ghi pipeline đầy đủ từng bước (trước/trong/sau retrieval) để có thể tái hiện.  
- **Hardware/Software:** Ghi cụ thể GPU/CPU, thư viện PyTorch/TensorFlow, phiên bản Python. Seed random.  
- **Đánh giá:** Đảm bảo dùng cùng splits, cùng code đo metric.  

Mục tiêu là bất kỳ ai có code và mô hình tương đương đều có thể chạy lại được Baseline và Baseline+Retrieval để tái lập kết quả.

## 22. Danh sách kiểm tra cuối cùng  

- [x] Đã chọn một baseline rõ ràng (Q1/Q2, 2023–2026).  
- [x] Đã chỉ ra hạn chế đã xác nhận của baseline.  
- [x] Đã xác định một cải tiến mục tiêu duy nhất.  
- [x] Có kế hoạch tái lập baseline (Baseline reproduction).  
- [x] Có thử nghiệm so sánh Baseline vs Improved.  
- [x] Có kế hoạch ablation phù hợp.  
- [x] Đã bao gồm metric phát hiện sớm (lead-time, early warning).  
- [x] Giữ kiểm soát biến cố (chỉ thay đổi cải tiến).  
- [x] Thiết kế thống kê (chạy nhiều lần, test ý nghĩa).  
- [x] Đã liệt kê rủi ro & biện pháp giảm thiểu.  
- [x] Không tạo gap/đề tài mới ngoài proposal.  
- [x] Không thêm công nghệ dư thừa ngoài scope trend (chỉ thêm retrieval như đã phê duyệt).  
- [x] Kế hoạch khả thi trong 6–9 tháng (ở mức tinh giản).