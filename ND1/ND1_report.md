# Báo Cáo Phân Tích Các Bài Báo Trong Thư Mục ND1

Báo cáo này tóm tắt các bài báo dựa trên các tiêu chí: Chủ đề, Phương pháp, Điểm mạnh, Điểm yếu, Hướng phát triển và Dataset sử dụng.

### 1. `1-s2.0-S1319157823000393-main.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện bất thường tự động trong toàn bộ vòng đời DevOps nhằm ngăn chặn sớm các vấn đề trước và sau khi triển khai hệ thống (Đề xuất khung _DevOps Anomaly Detection Framework - DADF_).
- **Phương pháp (Đã làm gì):** Khung DADF bao gồm 2 thành phần:
  1. _Phát hiện bất thường trước khi sản xuất (ADBP)_: Sử dụng thuật toán Local Outlier Factor (LOF) - học máy không giám sát để phát hiện điểm dị thường.
  2. _Phát hiện bất thường sau khi triển khai (ADAS)_: Ứng dụng mô hình chuỗi thời gian đa biến (ví dụ: Prophet) để dự đoán giá trị và so sánh với giá trị thực tế thay vì dùng các quy tắc ngưỡng cố định.
- **Điểm mạnh:** Giám sát được toàn diện từ các giai đoạn phát triển, kiểm thử cho đến khi vận hành thực tế; mô hình chuỗi thời gian linh hoạt hơn so với ngưỡng cảnh báo thủ công tĩnh.
- **Điểm yếu:** Đòi hỏi phải tích hợp sâu vào quy trình CI/CD và phải xử lý khối lượng dữ liệu log rất lớn, có thể gây quá tải nếu trình phân tích log (log parser) không tối ưu.
- **Hướng phát triển:** Sử dụng các trình phân tích log tiên tiến hơn để tăng tốc độ và hiệu suất, cho phép mô hình giám sát hoạt động chính xác với khung thời gian (window size) nhỏ hơn.
- **Dataset:** Một bộ dữ liệu công nghiệp thực tế thu thập từ luồng DevOps của hệ thống.

---

### 2R. `1-s2.0-S1566253523001136-main.pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá tổng quan một cách có hệ thống (Systematic Literature Review) về ứng dụng của Trí tuệ nhân tạo (AI) trong lĩnh vực an ninh mạng, lấy khung an ninh mạng NIST làm nền tảng.
- **Phương pháp (Đã làm gì):** Khảo sát 236 bài báo và phân loại (taxonomy) các trường hợp sử dụng AI vào 5 chức năng an ninh mạng cốt lõi của NIST: Nhận dạng (Identify), Bảo vệ (Protect), Phát hiện (Detect), Phản hồi (Respond), và Phục hồi (Recover).
- **Điểm mạnh:** Cung cấp một bộ phân loại toàn diện, đa cấp độ, giúp chuẩn hóa lại bức tranh tổng thể về cách AI đang hỗ trợ an ninh mạng.
- **Điểm yếu:** Đây là một bài tổng quan tài liệu, do đó nó không đề xuất hay xây dựng một mô hình thực nghiệm nào có thể dùng ngay.
- **Hướng phát triển:** Định hướng các nghiên cứu trong tương lai cần tập trung vào những lỗ hổng chưa được giải quyết tốt bởi AI hiện tại (ví dụ: khả năng giải thích của mô hình, và phòng thủ chống lại chính AI tấn công).
- **Dataset:** Không có (Bài báo Review).

---

### 3R. `1-s2.0-S2667305325001346-main.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tổng quan về sự giao thoa giữa nền tảng vận hành AI (AIOps), phát hiện bất thường trong hệ thống nhật ký (Log Anomaly Detection) dựa trên Mô hình ngôn ngữ lớn (LLM) và tối ưu hóa qua RAG (Retrieval-Augmented Generation). Nhấn mạnh tính ứng dụng vào hệ thống hạ tầng an ninh quốc phòng - quân sự.
- **Phương pháp (Đã làm gì):** Khảo sát hệ thống (SLR) để làm rõ cách LLM kết hợp RAG được sử dụng nhằm giảm thiểu ảo giác thông tin và cải thiện khả năng chẩn đoán lỗi trong nhật ký hệ thống.
- **Điểm mạnh:** Là nghiên cứu tiên phong điều tra sự kết hợp giữa kiến trúc RAG và LLM trong bối cảnh AIOps, nêu bật sức mạnh của LLM trong việc đọc hiểu các log phi cấu trúc.
- **Điểm yếu:** Mang tính chất tổng hợp các phương pháp luận (review), chưa đi sâu vào so sánh thực nghiệm độ trễ của RAG-LLM trong môi trường thời gian thực.
- **Hướng phát triển:** Ứng dụng RAG-LLM linh hoạt hơn để phát triển các thế hệ cảnh báo lỗi thông minh và tự động khắc phục cho các hệ thống rủi ro cao.
- **Dataset:** Không có (Bài báo Review).

---

### 4. `10.51537-chaos.1348302-3355185.pdf`

- **Chủ đề (Vấn đề giải quyết):** Chuyển đổi dữ liệu nhật ký (log) đa dạng thành cấu trúc đồ thị và phát hiện bất thường sử dụng các phương pháp học sâu.
- **Phương pháp (Đã làm gì):** Sử dụng thuật toán `node2vec` (một phương pháp học bán giám sát, khám phá heuristic) để chuyển đổi các mẫu log thành vector/đồ thị. Sau đó, dữ liệu này được đưa vào mô hình học sâu `LSTM` (Long Short-Term Memory) để phân loại và phát hiện bất thường.
- **Điểm mạnh:** Node2vec cung cấp tính linh hoạt cao nhờ các tham số có thể điều chỉnh và khả năng mở rộng trong việc học đặc trưng (feature learning); LSTM giải quyết được vấn đề suy giảm đạo hàm (gradient vanishing) của RNN truyền thống và đạt độ chính xác cao.
- **Điểm yếu:** Phương pháp phụ thuộc nhiều vào chất lượng của bước trích xuất mẫu log (template extraction) ban đầu.
- **Hướng phát triển:** Tinh chỉnh các phương pháp hiện tại, khám phá thuật toán mới và tận dụng các công nghệ mới nổi để tăng cường hiệu quả và khả năng mở rộng của hệ thống.
- **Dataset:** Tập dữ liệu Hadoop HDFS thu thập từ nhiều nguồn.

---

### 5R. `21.pdf`

- **Chủ đề (Vấn đề giải quyết):** Các mối đe dọa không gian mạng do AI điều khiển (AI-Powered Cyber Threats) - Đánh giá tổng quan hệ thống. Tập trung vào cách AI được sử dụng để thực hiện các cuộc tấn công mạng phức tạp.
- **Phương pháp (Đã làm gì):** Đánh giá tổng quan hệ thống (Systematic review) tổng hợp các nghiên cứu hiện tại để xác định quy mô, quy trình phát hiện, tác động và các hệ thống giảm nhẹ liên quan đến các mối đe dọa do AI khởi xướng.
- **Điểm mạnh:** Làm nổi bật hiệu ứng kép (dualistic effect) của AI - vừa là công cụ tấn công vừa là công cụ phòng thủ; cung cấp một cái nhìn tổng quan có cấu trúc về phạm vi, cách phát hiện, tác động và xu hướng tương lai.
- **Điểm yếu:** Đây là một bài báo tổng quan (Review), không đề xuất một khung thực nghiệm hoặc thiết lập thí nghiệm mới.
- **Hướng phát triển:** Cần sự đổi mới không ngừng trong các kỹ thuật an ninh mạng để đối phó với sự phát triển của các cuộc tấn công tự động do AI hỗ trợ.
- **Dataset:** Không có (Bài báo Review).

---

### 6. `2203.08580v1.pdf`

- **Chủ đề (Vấn đề giải quyết):** Xây dựng các tập dữ liệu nhật ký (log datasets) có thể bảo trì để đánh giá các Hệ thống phát hiện xâm nhập (Intrusion Detection Systems - IDS), giải quyết vấn đề thiếu hụt dữ liệu log được gán nhãn công khai.
- **Phương pháp (Đã làm gì):** Trình bày một bộ sưu tập các tập dữ liệu log được thu thập trong một testbed (môi trường thử nghiệm) mô phỏng một doanh nghiệp nhỏ. Sử dụng máy trạng thái (state machines) để mô phỏng hành vi người dùng bình thường và tiêm các cuộc tấn công đa bước. Dùng kỹ thuật model-driven engineering để tự động sinh và gán nhãn tập dữ liệu.
- **Điểm mạnh:** Giải quyết triệt để vấn đề thiếu tập dữ liệu log gán nhãn cho đánh giá IDS; cho phép khả năng tái tạo (reproducibility), thay đổi tham số dễ dàng và cung cấp mã nguồn mở.
- **Điểm yếu:** Dữ liệu sinh ra trong môi trường mô phỏng (testbed) có thể không nắm bắt được toàn bộ sự phức tạp và tính khó đoán của các mạng lưới doanh nghiệp thực tế.
- **Hướng phát triển:** Không đề cập cụ thể trong phần Abstract, nhưng mở ra hướng cho cộng đồng sử dụng công cụ để tự tạo ra các bộ dữ liệu phong phú hơn.
- **Dataset:** Bài báo cung cấp 8 tập dữ liệu mới chứa 20 loại file log khác nhau, trong đó gán nhãn 8 file cho 10 bước tấn công.

---

### 7R. `2212.13245v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Nghiên cứu và phân tích các đặc điểm của các dự án mã nguồn mở về AIOps trên GitHub để hiểu rõ thực tiễn ứng dụng của AIOps.
- **Phương pháp (Đã làm gì):** Trích xuất một tập hợp các dự án AIOps từ GitHub, phân tích các chỉ số kho lưu trữ (ví dụ: ngôn ngữ lập trình). Tiếp theo, đánh giá định tính để hiểu dữ liệu đầu vào, kỹ thuật phân tích và mục tiêu. Cuối cùng, đánh giá chất lượng dự án (như số lượng lỗi) so với các dự án Học máy (ML) và dự án chung thông thường.
- **Điểm mạnh:** Đây là nỗ lực đầu tiên định hình và mô tả hệ sinh thái mã nguồn mở AIOps; cung cấp những hiểu biết có giá trị dựa trên các chỉ số thực tế từ GitHub.
- **Điểm yếu:** Chỉ dựa trên kho lưu trữ mã nguồn mở (GitHub), do đó có thể không phản ánh hoàn toàn thực trạng các hệ thống AIOps riêng tư, khép kín tại các tập đoàn lớn.
- **Hướng phát triển:** Giúp các nhà nghiên cứu và thực hành nhận ra các điểm yếu của dự án AIOps hiện tại (nhiều lỗi hơn các dự án ML thông thường) để có biện pháp cải thiện chất lượng phần mềm.
- **Dataset:** Tập hợp các dự án mã nguồn mở trên GitHub.

---

### 8. `2305.09678v1.pdf`

- **Chủ đề (Vấn đề giải quyết):** Đề xuất một tập dữ liệu phát hiện xâm nhập mới, thực tế và đáng tin cậy mang tên "ICS-Flow" dùng cho việc đánh giá các Hệ thống Phát hiện Xâm nhập (IDS) trong môi trường Hệ thống Điều khiển Công nghiệp (ICS).
- **Phương pháp (Đã làm gì):** Sử dụng framework ICSSIM để tạo một môi trường thử nghiệm ICS ảo. Triển khai 4 loại tấn công mạng: Reconnaissance, DDoS, MitM (False data injection), và Replay. Phát triển công cụ ICSFlowGenerator mã nguồn mở để trích xuất đặc trưng luồng mạng từ các gói tin thô.
- **Điểm mạnh:** Tập dữ liệu hoàn toàn không bị ẩn danh (un-anonymized), bao gồm đa dạng các đặc trưng luồng mạng, chứa cả các bản chụp trạng thái của hệ thống, log tấn công. Các bất thường được sinh ra từ các cuộc tấn công mạng thực tế chứ không phải do sinh bất thường tổng hợp (synthetic).
- **Điểm yếu:** Tập dữ liệu vẫn được tạo ra từ môi trường mô phỏng (ảo hóa) thay vì một hệ thống công nghiệp thực tế đang hoạt động.
- **Hướng phát triển:** Dùng làm benchmark (tiêu chuẩn) để huấn luyện và phát triển các thuật toán ML phát hiện xâm nhập mạnh mẽ hơn cho ICS.
- **Dataset:** Đề xuất tập dữ liệu mới công khai `ICS-Flow` (https://www.kaggle.com/datasets/alirezadehlaghi/icssim).

---

### 11-Compare. `2406.07467v4.pdf`

- **Chủ đề (Vấn đề giải quyết):** Giải quyết thách thức Phát hiện bất thường trên dữ liệu Log không ổn định (ULAD - Unstable Logs Anomaly Detection) trong điều kiện thiếu hụt dữ liệu gán nhãn, một kịch bản thực tế hơn so với giả định log ổn định.
- **Phương pháp (Đã làm gì):** Đề xuất "FlexLog", một cách tiếp cận lai (hybrid) kết hợp các mô hình học máy truyền thống (Decision Tree, KNN, Feedforward Neural Network) với một Mô hình Ngôn ngữ Lớn (Mistral) thông qua phương pháp học kết hợp (ensemble learning). Tích hợp thêm bộ nhớ đệm (cache) và sinh văn bản tăng cường truy xuất (RAG) để nâng cao tính hiệu quả.
- **Điểm mạnh:** Vượt trội so với các mô hình cơ sở (baselines) về điểm F1 dù sử dụng lượng dữ liệu gán nhãn ít hơn đáng kể; giữ được thời gian suy luận dưới 1 giây cho mỗi chuỗi log; giải quyết được các vấn đề thực tế như log thay đổi (unstable) và rò rỉ dữ liệu (data leakage).
- **Điểm yếu:** Thời gian suy luận (dưới 1 giây) có thể vẫn chưa đủ nhanh đối với các hệ thống yêu cầu độ trễ cực thấp (ultra-low latency-sensitive systems).
- **Hướng phát triển:** Tối ưu hóa sâu hơn các mô hình LLM cục bộ (local LLM) để tiếp tục giảm thiểu độ trễ suy luận, mở rộng nghiên cứu sang các cấu trúc log phức tạp hơn.
- **Dataset:** Sử dụng 4 tập dữ liệu dành riêng cho ULAD: ADFA-U, LOGEVOL-U, SynHDFS-U, và SYNEVOL-U.

---

### 12R. `2409.20503v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tìm hiểu xem loại thông tin nào (ngữ nghĩa, tuần tự, thời gian, hay sự xuất hiện của sự kiện) đóng góp lớn nhất vào quá trình phát hiện bất thường dựa trên nhật ký (log-based anomaly detection).
- **Phương pháp (Đã làm gì):** Đề xuất một mô hình học sâu có khả năng tùy chỉnh dựa trên kiến trúc Transformer, cho phép cấu hình và thu thập riêng biệt thông tin ngữ nghĩa (semantic), tuần tự (sequential) và thời gian (temporal). Huấn luyện và đánh giá mô hình bằng các chuỗi log có độ dài khác nhau thay vì dùng khung thời gian/độ dài cố định.
- **Điểm mạnh:** Cách tiếp cận cho phép cô lập và đánh giá chính xác tác động của từng loại đặc trưng log. Khắc phục được hạn chế phải dùng chuỗi log có độ dài cố định. Đạt hiệu suất cạnh tranh và ổn định.
- **Điểm yếu:** Kết quả cho thấy các tập dữ liệu công khai hiện tại quá đơn giản (phần lớn chỉ cần dựa vào tần suất xuất hiện sự kiện là đủ để phát hiện), làm giảm ý nghĩa thực sự của thông tin tuần tự và thời gian trên các bộ dữ liệu này.
- **Hướng phát triển:** Nhấn mạnh sự cần thiết phải xây dựng các bộ dữ liệu benchmark mới, phức tạp hơn, chứa nhiều loại bất thường thực tế để đánh giá đúng sức mạnh của các mô hình học sâu.
- **Dataset:** Các bộ dữ liệu log công khai (như HDFS).

---

### 13-Compare. `2504.02994v1.pdf`

- **Chủ đề (Vấn đề giải quyết):** Cải thiện khả năng phát hiện bất thường dựa trên nhật ký (log-based anomaly detection) thông qua việc sử dụng các bộ lọc thích ứng được học tự động (Learned Adaptive Filter).
- **Phương pháp (Đã làm gì):** Thay vì dùng các quy tắc/bộ lọc ngưỡng cố định truyền thống, nghiên cứu sử dụng Học tăng cường sâu (Deep Reinforcement Learning - DRL) để xây dựng một bộ lọc thích ứng. Tác nhân DRL sẽ tương tác và tự động thiết lập các ngưỡng bất thường khác nhau tùy theo từng chuỗi log cụ thể. Thử nghiệm áp dụng bộ lọc này lên trên hai mô hình học không giám sát tiên tiến là DeepLog và LogAnomaly.
- **Điểm mạnh:** Vượt qua hạn chế của bộ lọc ngưỡng tĩnh, tự động thích ứng với tính chất thay đổi linh hoạt của các chuỗi log khác nhau, mang lại hiệu suất phát hiện cao hơn.
- **Điểm yếu:** Mô hình DRL đưa vào hệ thống sự phức tạp đáng kể trong quá trình huấn luyện và yêu cầu thời gian hội tụ, có thể khó tinh chỉnh (tune) trong thực tế sản xuất.
- **Hướng phát triển:** Nghiên cứu tối ưu hóa phần thưởng (reward function) và tăng tốc hội tụ cho DRL trong môi trường AIOps thực tế.
- **Dataset:** HDFS và BGL.

---

### 14R. `2510.01409v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Trích xuất Thông tin Tình báo Mối đe dọa Mạng (Cyber Threat Intelligence - CTI) có thể hành động từ các nhật ký hệ thống chưa cấu trúc và hỗn tạp bằng cách sử dụng các Mô hình Ngôn ngữ Lớn (LLMs).
- **Phương pháp (Đã làm gì):** Giới thiệu "OntoLogX", một tác nhân AI tự trị (autonomous AI agent) dùng LLM để biến đổi log thô thành các Đồ thị Tri thức (Knowledge Graphs - KGs) dựa trên một bản thể luận (ontology) không gian mạng. Kết hợp Retrieval Augmented Generation (RAG) và các bước sửa lỗi lặp lại. Cuối cùng, tổng hợp các KG này để dự đoán chiến thuật tấn công MITRE ATT&CK.
- **Điểm mạnh:** Tự động hóa việc cấu trúc hóa dữ liệu log nhiễu thành đồ thị tri thức có khả năng tương tác, giảm thiểu hoàn toàn sự can thiệp của con người; liên kết được bằng chứng mức thấp với mục tiêu tấn công mức cao.
- **Điểm yếu:** Quá trình phụ thuộc vào hiệu năng của LLM và pipeline RAG, có rủi ro về ảo giác (hallucination) nếu các bước sửa lỗi không thành công.
- **Hướng phát triển:** Tối ưu hiệu năng của agent, triển khai phân tích thời gian thực với độ trễ thấp trên hệ thống phòng thủ.
- **Dataset:** Một tập dữ liệu honeypot công khai và một tập dữ liệu honeypot thực tế mới thu thập.

---

### 16R. `3501297.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tổng quan về các kỹ thuật Phát hiện Bất thường và Phân tích Nguyên nhân gốc rễ (Root Cause Analysis - RCA) trong các ứng dụng đám mây đa dịch vụ (Multi-service/Microservices).
- **Phương pháp (Đã làm gì):** Cung cấp một cái nhìn tổng quan có cấu trúc và phân tích định tính về các kỹ thuật hiện có dùng để phát hiện bất thường và tìm ra nguyên nhân lỗi trong các ứng dụng đa dịch vụ hiện đại. Phân biệt rõ các khái niệm về bất thường, lỗi, và gỡ lỗi (debugging).
- **Điểm mạnh:** Một bài tổng quan (survey) toàn diện nhắm mục tiêu cụ thể vào các kiến trúc cloud-native, microservices; làm rõ được luồng quy trình từ phát hiện bất thường đến phân tích nguyên nhân.
- **Điểm yếu:** Không đề xuất một mô hình/khung thực nghiệm mới mà chỉ tổng hợp các nghiên cứu đã có.
- **Hướng phát triển:** Thảo luận về các thách thức mở như làm thế nào để kết hợp chặt chẽ hơn giữa bước "phát hiện" và bước "tìm nguyên nhân" thành một pipeline hoàn chỉnh, liền mạch.
- **Dataset:** Không có (Bài báo Review).

---

### 19R. `A_Multi-Agent_System_for_Cybersecurity_Threat_Detection_and_Correlation_Using_Large_Language_Models.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện và tương quan (correlation) các mối đe dọa an ninh mạng phức tạp trên nhiều hướng tấn công (multi-vector) sử dụng Hệ thống Đa Tác nhân (Multi-Agent System) và LLM.
- **Phương pháp (Đã làm gì):** Xây dựng một hệ thống gồm ba tác nhân chuyên biệt hoạt động độc lập (xác thực email, phân tích log, và rà quét IP). Một hệ thống gợi ý theo ngữ cảnh (contextual recommendation system) thu thập đầu ra từ ba tác nhân này để phân tích tương quan và phát hiện các mẫu tấn công lén lút nhiều lớp. Tích hợp LLM để phân tích ngữ nghĩa và đưa ra chuỗi suy luận (chain-of-thought).
- **Điểm mạnh:** Độ chính xác phát hiện lên tới 93,6% và giảm 41,3% tỷ lệ dương tính giả (False Positive Rate) so với các phương pháp cũ; khả năng diễn giải tự động (Explainable AI) giúp giảm đáng kể thời gian đánh giá (triage) của nhà phân tích.
- **Điểm yếu:** Chi phí gọi API LLM cao và có khả năng phát sinh độ trễ khi phân tích dữ liệu thực tế tốc độ cao (real-time high-speed data).
- **Hướng phát triển:** Tối ưu hóa LLM cục bộ để thay thế API thương mại nhằm tăng tính bảo mật dữ liệu và giảm độ trễ; mở rộng thêm các domain phân tích khác (ví dụ: endpoint telemetry).
- **Dataset:** CIC-IDS 2017, SpamAssassin, và hệ thống mạng giả lập (custom simulated network environments).

---

### 20-Compare. `A_Multi-source_Log_Hidden_Anomaly_Detection_Method.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện các bất thường ẩn (hidden anomalies) từ dữ liệu nhật ký đa nguồn, giải quyết vấn đề các hành vi bất thường thường nảy sinh từ các thao tác đồng thời (concurrent) của người dùng thay vì chỉ là sự kiện đơn lẻ.
- **Phương pháp (Đã làm gì):** Đề xuất mô hình TE-LSTM, kết hợp bộ mã hóa Transformer (Transformer Encoder) và mạng LSTM. Mô hình cải tiến bộ mã hóa Transformer bằng cách loại bỏ mã hóa vị trí (positional encoding) và thêm cơ chế che giấu (masking mechanism), giúp nắm bắt hiệu quả đặc trưng ngữ nghĩa và tương quan chuỗi thời gian của log đa nguồn.
- **Điểm mạnh:** Khắc phục được nhược điểm của phân tích log một chiều (one-dimensional) truyền thống, nhận diện chính xác các sự kiện bất thường ẩn mình trong các hoạt động đồng thời phức tạp của hệ thống đa nguồn.
- **Điểm yếu:** Thay đổi kiến trúc chuẩn của Transformer (bỏ positional encoding) có thể làm giảm khả năng bắt chuỗi dài nếu LSTM không bù đắp kịp thời, gây khó khăn khi scale với chuỗi log quá dài.
- **Hướng phát triển:** Mở rộng nghiên cứu để ứng dụng vào phát hiện các mối đe dọa nội bộ (insider threats) phức tạp trong mạng doanh nghiệp với quy mô lớn hơn.
- **Dataset:** Không nêu rõ trong phần abstract/introduction (thường là các tập dữ liệu hành vi người dùng/log doanh nghiệp).

---

### 22-Compare. `AnomalyDetection.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tự động hóa quá trình phát hiện bất thường trong dữ liệu nhật ký (logs) của nền tảng quản lý đám mây OpenStack.
- **Phương pháp (Đã làm gì):** Tác giả tạo ra một tập dữ liệu gồm 25.000 log bằng cách tiêm (injecting) ba loại bất thường vào hệ thống OpenStack (thành phần Nova). Phân tích cú pháp log (parsing) bằng thuật toán IPLOM. Sau đó, áp dụng thuật toán Phân tích Thành phần Chính Mạnh mẽ (Robusted Principal Component Analysis - RPCA) để phân tách log thành ma trận rank-thấp (bình thường) và ma trận thưa (bất thường). Để dùng offline/online nhanh hơn, mô hình chiếu các điểm dữ liệu mới lên không gian cột của ma trận rank-thấp mà không cần phân tách lại.
- **Điểm mạnh:** Cải thiện điểm F1 thêm 9% so với nghiên cứu trước đó, đồng thời giảm thời gian chạy đáng kể do không phải phân tích lại toàn bộ ma trận khi có dữ liệu mới. Đóng góp một tập dữ liệu mở hữu ích cho cộng đồng.
- **Điểm yếu:** Tập dữ liệu là dữ liệu nhân tạo (được tiêm lỗi) thay vì dữ liệu lỗi thực tế trong môi trường production, có thể không phản ánh hết mọi góc cạnh của sự cố thật.
- **Hướng phát triển:** Mở rộng và kiểm chứng thuật toán trên các tập dữ liệu OpenStack có quy mô khổng lồ và độ phức tạp cao hơn trong môi trường đám mây thương mại.
- **Dataset:** Tập dữ liệu tự tạo gồm 25.000 logs của OpenStack (Nova) có dán nhãn bất thường.

---

### 23. `Anomaly_Detection_and_Root_Cause_Analysis_in_Cloud.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện sự cố và phân tích nguyên nhân gốc rễ (Root Cause Analysis - RCA) trong môi trường ứng dụng gốc đám mây (Cloud-native applications) và kiến trúc vi dịch vụ (Microservices).
- **Phương pháp (Đã làm gì):** Đề xuất một hệ thống phát hiện nguyên nhân gốc rễ động sử dụng các kỹ thuật Học máy không giám sát. Sử dụng mạng Bayesian (Bayesian networks) để thực hiện các suy luận xác suất, kết hợp với các khái niệm về đánh giá ngữ cảnh bằng LLMs nhằm đưa ra các cảnh báo có thể hành động (actionable) thay vì các báo cáo quá phức tạp và khó hiểu.
- **Điểm mạnh:** Giải quyết thực tiễn vấn đề "báo cáo quá dài và phức tạp" trong các công cụ RCA truyền thống, đưa ra các chẩn đoán ngắn gọn, rõ ràng, giúp kỹ sư dễ dàng thực hiện thao tác khắc phục.
- **Điểm yếu:** Mô hình xác suất như mạng Bayesian thường gặp khó khăn về khả năng mở rộng (scale) và cần cập nhật liên tục khi áp dụng vào các vi dịch vụ thay đổi (deploy) hàng chục/trăm lần mỗi ngày.
- **Hướng phát triển:** Cải thiện khả năng diễn giải bằng LLMs để xử lý chi phí tính toán và giảm thiểu thiên kiến (bias) hay "ảo giác" (hallucination) trong việc chẩn đoán log.
- **Dataset:** Không nêu đích danh bộ dữ liệu công khai (áp dụng trên log/metric của môi trường đám mây chung).

---

### 24. `Aya H. Salem - Advancing cybersecurity a comprehensive review of AI-driven detection techniques [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá toàn diện các kỹ thuật phát hiện dựa trên AI (Machine Learning, Deep Learning và các thuật toán Metaheuristic) trong việc nâng cao an ninh mạng.
- **Phương pháp (Đã làm gì):** Khảo sát hơn 60 nghiên cứu gần đây (đến năm 2024) về hiệu quả của các công cụ AI trong việc phát hiện nhiều loại mối đe dọa (malware, xâm nhập mạng, spam...). Đưa ra một framework chuẩn để đánh giá ưu/nhược điểm của các phương pháp AI và Metaheuristic hiện tại.
- **Điểm mạnh:** Rất cập nhật (năm 2024); không chỉ dừng ở ML/DL truyền thống mà còn phân tích sâu các thuật toán tối ưu hóa siêu heuristic (Metaheuristic algorithms) kết hợp với AI.
- **Điểm yếu:** Chỉ là một bài tổng quan văn bản (Survey/Review), không đề xuất hệ thống thực nghiệm hay mô hình mới nào để giải quyết một bài toán cụ thể.
- **Hướng phát triển:** Khuyến khích xây dựng các giải pháp thông minh và linh hoạt hơn, có khả năng học và cập nhật liên tục (continuous learning) để đối phó với những chiêu thức ngày càng tinh vi của tin tặc.
- **Dataset:** Không có (Bài báo Review).

---

### 25. `Crispin Almodovar - LogFiT Log Anomaly Detection Using Fine-Tuned Language Models [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện bất thường trong log bằng cách sử dụng các Mô hình Ngôn ngữ đã được tinh chỉnh (Fine-Tuned Language Models - LogFiT), loại bỏ bước phân tích cú pháp (log parsing) trung gian.
- **Phương pháp (Đã làm gì):** Đề xuất LogFiT, một phương pháp học không giám sát dựa trên tái thiết (reconstruction-based) sử dụng các mô hình họ BERT (RoBERTa và Longformer). Mô hình hoạt động trực tiếp trên log thô bằng cách sử dụng kho từ vựng sub-word rộng lớn của mô hình ngôn ngữ được huấn luyện trước. Sử dụng độ chính xác dự đoán top-k làm ngưỡng xác định bất thường.
- **Điểm mạnh:** Loại bỏ được điểm yếu chí mạng của bước log parsing truyền thống (mất thông tin ngữ nghĩa và không linh hoạt với cấu trúc log mới). Bền vững trước những thay đổi dần dần về mặt từ vựng (lexical content) của hệ thống.
- **Điểm yếu:** Vẫn là phương pháp không giám sát dựa trên giả định zero-positive (chỉ dùng dữ liệu log bình thường để huấn luyện), do đó nếu dữ liệu huấn luyện chứa lẫn bất thường, mô hình sẽ bị sai lệch.
- **Hướng phát triển:** Tích hợp LogFiT vào các công cụ xử lý ngôn ngữ tự nhiên (NLP) hiện có và hệ sinh thái quan sát hệ thống (observability ecosystem) rộng lớn hơn.
- **Dataset:** Các tập dữ liệu chuẩn về phát hiện bất thường log (BGL, HDFS, Thunderbird, v.v.).

---

### 26. `Egil Karlsen - Benchmarking Large Language Models for Log Analysis, Security, and Interpretation [2023].pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá tiêu chuẩn (Benchmarking) sức mạnh của các Mô hình Ngôn ngữ Lớn (LLMs) trong việc phân tích, bảo mật và diễn giải nhật ký sự kiện (log).
- **Phương pháp (Đã làm gì):** Triển khai một pipeline thử nghiệm (LLM4Sec) để benchmark 60 mô hình LLM đã được tinh chỉnh (fine-tuned) với các kiến trúc khác nhau (BERT, RoBERTa, DistilRoBERTa, GPT-2, GPT-Neo). Thử nghiệm khả năng thích ứng miền (domain adaptation) qua phương pháp phân loại chuỗi (sequence classification).
- **Điểm mạnh:** Cung cấp cái nhìn đối sánh toàn diện giữa nhiều kiến trúc LLM trên đa dạng bộ dữ liệu. Đạt hiệu suất cực cao (Mô hình DistilRoBERTa tinh chỉnh đạt F1-Score trung bình 0,998 vượt trội so với state-of-the-art hiện tại).
- **Điểm yếu:** Việc tinh chỉnh 60 mô hình là rất tốn kém tài nguyên tính toán. Phương pháp tiếp cận phân loại chuỗi thường yêu cầu dữ liệu có gán nhãn (có giám sát), điều rất khan hiếm trong môi trường log thực tế.
- **Hướng phát triển:** Áp dụng LLM cho việc trích xuất đặc trưng (feature extraction) động trên dữ liệu chưa biết cấu trúc thay cho các parser dựa trên regex tĩnh (như DRAIN).
- **Dataset:** Sử dụng 6 tập dữ liệu từ các nguồn ứng dụng web và nhật ký hệ thống.

---

### 27. `Enerst Edozie - Artificial intelligence advances in anomaly detection for telecom networks [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá các tiến bộ của Trí tuệ Nhân tạo trong việc phát hiện bất thường cho các mạng viễn thông (telecom networks).
- **Phương pháp (Đã làm gì):** Bài báo là một đánh giá quan trọng (critical review) về vai trò của AI (đặc biệt là học sâu) trong các hệ thống phát hiện bất thường viễn thông hiện đại. Khám phá các công nghệ tiên tiến như Mạng Sinh Đối kháng (GANs) và Học Tăng cường (RL) trong bối cảnh các mạng phức tạp (5G/6G, Edge computing, IoT).
- **Điểm mạnh:** Nghiên cứu rất mới (năm 2025), bắt kịp các xu hướng công nghệ mạng hiện đại như 5G/6G và tác động của chúng lên bài toán phát hiện bất thường ở hệ thống viễn thông.
- **Điểm yếu:** Là một bài Review đánh giá, không đề xuất hay thiết kế một mô hình thuật toán cụ thể nào với tập dữ liệu riêng.
- **Hướng phát triển:** Khuyến nghị áp dụng các mô hình kết hợp (hybrid models), cải thiện tiền xử lý dữ liệu nâng cao và phát triển các hệ thống tự thích ứng (self-adaptive systems) để tăng tính mạnh mẽ cho mạng viễn thông.
- **Dataset:** Không có (Bài báo Review).

---

### 28. `Felipe Urrutia - Who's the Best Detective Large Language Models vs. Traditional Machine Learning in Detecting Incoherent Fourt.pdf`

- **Chủ đề (Vấn đề giải quyết):** So sánh sức mạnh của các Mô hình Ngôn ngữ Lớn (LLMs) với các phương pháp Học máy truyền thống (ML) trong việc tự động phát hiện các câu trả lời Toán học thiếu mạch lạc (incoherent) của học sinh lớp 4.
- **Phương pháp (Đã làm gì):** Phân tích câu trả lời của học sinh bằng 3 mô hình LLM: GPT-3, BLOOM, và YOU (thử nghiệm với 0, 1, 2, 3 và 4-shot prompt) và so sánh với các bộ phân loại ML truyền thống.
- **Điểm mạnh:** Thử nghiệm trên dữ liệu thực tế đầy tính thách thức, bao gồm những câu trả lời sai chính tả đặc trưng của trẻ em và các cấu trúc câu hỏi lồng ghép đệ quy (recursive questions).
- **Điểm yếu:** Đáng chú ý là kết quả cho thấy các mô hình LLM (kể cả ChatGPT) hiện tại hoạt động **tệ hơn** các mô hình ML truyền thống trong nhiệm vụ cụ thể này, nguyên nhân chính là do chúng xử lý kém với các lỗi chính tả tự nhiên của trẻ em.
- **Hướng phát triển:** Cần tinh chỉnh (fine-tune) LLMs chuyên biệt cho văn phong và lỗi chính tả của trẻ em hoặc kết hợp LLMs với một module tiền xử lý lỗi chính tả mạnh mẽ trước khi đánh giá tính mạch lạc.
- **Dataset:** Tập dữ liệu các câu trả lời tự luận (open-ended) của học sinh lớp 4 cho các bài toán.

---

### 29. `FrameworkforautomaticdetectionofanomaliesinDevOps-KSUPaper.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tự động phát hiện bất thường trong suốt vòng đời của DevOps, giải quyết vấn đề khối lượng log sinh ra khổng lồ từ các công cụ CI/CD khiến việc kiểm tra thủ công trở nên bất khả thi.
- **Phương pháp (Đã làm gì):** Đề xuất Khung Phát hiện Bất thường DevOps (DADF) gồm 2 thành phần chính:
  1. ADBP (Phát hiện trước khi lên Production) dùng thuật toán Local Outlier Factor (LOF) trên dữ liệu mã nguồn, build, test.
  2. ADAS (Phát hiện sau Staging) dùng Vector Auto-Regression (VAR) trên các log và số liệu giám sát (CPU/Memory) sau khi triển khai.
- **Điểm mạnh:** Hệ thống giám sát toàn diện cả hai vòng đời trước và sau khi triển khai phần mềm (Continuous Integration & Continuous Deployment). Hiệu năng cao với độ chính xác đạt 96% ở pha trước triển khai trên 2 dự án công nghiệp thực tế.
- **Điểm yếu:** Sự thành công của framework phụ thuộc nặng nề vào chất lượng và định dạng log chuẩn hóa từ chuỗi công cụ (toolchain) của các tổ chức khác nhau, vốn rất dị biệt.
- **Hướng phát triển:** Tích hợp trực tiếp DADF vào các pipeline CI/CD phổ biến (như Jenkins, GitLab CI) dưới dạng plugin để tự động chặn các bản phát hành (releases) lỗi.
- **Dataset:** Dữ liệu thu thập từ quy trình CI/CD của 2 dự án công nghiệp thực tế.

---

### 30. `Guembe Blessing - The Emerging Threat of Ai-driven Cyber Attacks A Review [2022].pdf`

- **Chủ đề (Vấn đề giải quyết):** Nghiên cứu và cảnh báo về mối đe dọa đang trỗi dậy của các Cuộc tấn công không gian mạng do AI điều khiển (AI-driven Cyberattacks / Offensive AI).
- **Phương pháp (Đã làm gì):** Đánh giá hệ thống 46 bài báo chất lượng (chọn lọc từ 936 bài) tập trung vào việc tội phạm mạng sử dụng AI trong các giai đoạn khác nhau của chuỗi tiêu diệt (cybersecurity kill chain).
- **Điểm mạnh:** Chỉ ra các con số phân tích rất cụ thể: 56% kỹ thuật AI của hacker được dùng ở giai đoạn truy cập và thâm nhập (access & penetration), 12% ở khai thác và C&C, 11% ở trinh sát (reconnaissance). Khẳng định rõ ràng sự lỗi thời của các hệ thống phòng thủ truyền thống trước AI tấn công.
- **Điểm yếu:** Là một nghiên cứu tổng quan (Review), không xây dựng thuật toán hay mô hình phòng thủ cụ thể nào để đối trọng lại "Offensive AI".
- **Hướng phát triển:** Đề xuất các tổ chức cấp thiết phải đầu tư vào "Defensive AI" để có thể chống lại "Offensive AI", vì tốc độ và logic ra quyết định của phần mềm độc hại dùng AI đã vượt quá khả năng xử lý của con người.
- **Dataset:** Không có (Bài báo Review).

---

### 31. `Gökçe Karacayılmaz - A novel approach detection for IIoT attacks via artificial intelligence [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện và ngăn chặn các cuộc tấn công mạng nhằm vào thiết bị Internet vạn vật công nghiệp (IIoT) kết nối với Hệ thống Điều khiển Công nghiệp (ICS) và bộ điều khiển lập trình (PLC).
- **Phương pháp (Đã làm gì):** Đề xuất một hệ thống chuyên gia (expert system) kết hợp giám sát liên tục và phát hiện tấn công bằng phương pháp tiếp cận lai (hybrid approach), kết hợp giữa hệ luật (rule-based reasoning) và các kỹ thuật học máy. Khảo sát 3 loại tấn công chính: Man-in-the-Middle (MitM), DDoS, và Start-Stop. Đưa ra các đặc trưng mới như tỷ lệ "dup and retransmission" để phát hiện MitM tốt hơn.
- **Điểm mạnh:** Thử nghiệm trên môi trường phần cứng thực tế (real-world testbed) mô phỏng quá trình công nghiệp điều khiển bằng PLC (giao thức Modbus, MQTT) thay vì chỉ chạy trên bộ dữ liệu mạng mô phỏng. Đạt độ chính xác cao và tỷ lệ dương tính giả thấp.
- **Điểm yếu:** Thành phần dựa trên hệ luật (rule-based) đòi hỏi phải cập nhật luật thủ công, gây khó khăn trong việc mở rộng hoặc thích ứng tự động với các cuộc tấn công Zero-day hoàn toàn mới.
- **Hướng phát triển:** Tích hợp thêm học tăng cường (reinforcement learning) vào hệ thống chuyên gia để có khả năng tự động cập nhật luật phát hiện từ môi trường thực.
- **Dataset:** Dữ liệu thu thập từ testbed phần cứng thực tế mô phỏng môi trường ICS/IIoT.

---

### 32. `Haoqi Huang - Deep Learning Advancements in Anomaly Detection A Comprehensive Survey [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Cung cấp một bản đánh giá toàn diện về các tiến bộ của Học sâu (Deep Learning) trong lĩnh vực phát hiện bất thường (Anomaly Detection - AD) trong dữ liệu IoT và các lĩnh vực khác.
- **Phương pháp (Đã làm gì):** Bài báo là một nghiên cứu khảo sát (survey). Hệ thống hóa các phương pháp AD thành 3 loại: có giám sát, bán giám sát và không giám sát. So sánh chi tiết sự khác biệt, ưu/nhược điểm giữa các mô hình học máy truyền thống (PCA, Clustering) với các Mạng thần kinh sâu (DNNs).
- **Điểm mạnh:** Rất cập nhật (năm 2025), bao quát toàn bộ các nền tảng kỹ thuật hiện đại. Làm rõ lý do vì sao hầu hết các nghiên cứu AD hiện nay đều chuyển hướng sang không giám sát (do sự mất cân bằng dữ liệu và chi phí gán nhãn lớn).
- **Điểm yếu:** Chỉ là một bài khảo sát tổng hợp, không đề xuất kiến trúc mạng mới hay công bố một bộ dữ liệu mới nào.
- **Hướng phát triển:** Bài báo gợi ý các hướng nghiên cứu trong tương lai: áp dụng học sâu vào AD cho luồng dữ liệu thời gian thực và xử lý bài toán "đại dịch" nhiễu dữ liệu trong không gian IoT nhiều chiều.
- **Dataset:** Không có (Bài báo Review).

---

### 33. `Josue Genaro Almaraz-Rivera - An Anomaly-based Detection System for Monitoring Kubernetes Infrastructures [2023].pdf`

- **Chủ đề (Vấn đề giải quyết):** Giám sát và phát hiện bất thường cho các cấu trúc hạ tầng Kubernetes bằng hệ thống phát hiện dựa trên Phân loại một lớp (One-Class Classification - OCC).
- **Phương pháp (Đã làm gì):** Triển khai một quy trình làm việc (workflow) gốc đám mây (cloud-native) sử dụng MLOps (Kubeflow để điều phối AI, Prometheus để thu thập số liệu). Sử dụng các thuật toán One-class SVM, Isolation Forest (Học máy) và Autoencoders (Học sâu). Mô hình được huấn luyện offline bằng dataset LATAM-DDoS-IoT và thử nghiệm online với dữ liệu cục bộ từ hạ tầng Kubernetes tại chỗ (on-premise).
- **Điểm mạnh:** Giải quyết triệt để bài toán mất cân bằng dữ liệu bằng phương pháp OCC. Đề xuất quy trình MLOps hoàn chỉnh từ khâu thu thập metric đến việc huấn luyện/triển khai cho các kỹ sư đám mây.
- **Điểm yếu:** Chủ yếu đánh giá dựa trên các tấn công mạng truyền thống (như DDoS từ tập dữ liệu LATAM), có thể cần hiệu chỉnh thêm để nhận diện các bất thường đặc thù của Kubernetes (lỗi pod crash, rò rỉ bộ nhớ ở mức ứng dụng).
- **Hướng phát triển:** Áp dụng hệ thống OCC mở rộng cho các bài toán bảo mật đa nền tảng và tối ưu pipeline MLOps để giảm độ trễ khi suy luận mô hình trên Kubernetes.
- **Dataset:** Tập dữ liệu LATAM-DDoS-IoT và dữ liệu thực tế thu thập từ hạ tầng K8s cục bộ.

---

### 34. `L. Ofusori - Artificial Intelligence in Cybersecurity A Comprehensive Review and Future Direction [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Tầm quan trọng của Trí tuệ Nhân tạo (AI) trong An ninh mạng: Đánh giá toàn diện và Định hướng tương lai.
- **Phương pháp (Đã làm gì):** Đánh giá tài liệu có hệ thống (Systematic Literature Review - SLR) tuân theo hướng dẫn PRISMA. Trích xuất và phân tích 939 bài báo nghiên cứu chuyên sâu (được chọn lọc từ 14.509 bài trên Scopus và Web of Science) để hiểu cách các kỹ thuật AI/ML được áp dụng cho việc phát hiện bất thường, xác định mối đe dọa, phân tích dự đoán và phản hồi sự cố tự động.
- **Điểm mạnh:** Nghiên cứu có quy mô cực kỳ đồ sộ và bài bản (sử dụng chuẩn PRISMA), phác họa một bức tranh toàn cảnh về hiệu quả, thách thức và xu hướng mới nổi trong việc sử dụng AI để tự động hóa an ninh mạng.
- **Điểm yếu:** Chỉ là bài Review, không cung cấp mô hình AI thực tế nào có thể triển khai ngay hay đóng góp một bộ dữ liệu an ninh mạng mới.
- **Hướng phát triển:** Tập trung giải quyết các thách thức về việc AI bị tấn công ngược (Adversarial AI) và nhu cầu cấp thiết về dữ liệu huấn luyện an ninh mạng chất lượng cao, đa dạng hơn.
- **Dataset:** Không có (Bài báo Review).

---

### 35. `Lin Yang - Try with Simpler - An Evaluation of Improved Principal Component Analysis in Log-based Anomaly Detection [2023].pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá hiệu quả của phương pháp Phân tích Thành phần Chính (PCA) được cải tiến trong việc phát hiện bất thường dựa trên Log, đi ngược lại xu hướng lạm dụng Deep Learning (DL) phức tạp.
- **Phương pháp (Đã làm gì):** Theo đuổi triết lý "Thử với cách đơn giản hơn" (Try-with-simpler). Nhóm tác giả tối ưu hóa kỹ thuật PCA không giám sát truyền thống bằng cách kết hợp nó với kỹ thuật biểu diễn log dựa trên ngữ nghĩa siêu nhẹ (lightweight semantic-based log representation), gọi là SemPCA. Đánh giá SemPCA với 4 mô hình DL và 2 mô hình truyền thống.
- **Điểm mạnh:** SemPCA đạt hiệu quả ngang ngửa với các mô hình DL có giám sát/bán giám sát tiên tiến nhất, nhưng lại ổn định hơn nhiều khi thiếu dữ liệu huấn luyện, không phụ thuộc vào nhãn dữ liệu (data labels) và tiết kiệm tài nguyên/thời gian tính toán vượt trội.
- **Điểm yếu:** Bản chất PCA vẫn là một mô hình tuyến tính (linear model), do đó có thể sẽ gặp khó khăn đối với các hệ thống có mối quan hệ thời gian (temporal relationships) phi tuyến tính cực kỳ phức tạp mà các mô hình LSTM hay Transformer có thể học được.
- **Hướng phát triển:** Áp dụng SemPCA làm mô hình nền tảng siêu nhẹ cho các hệ thống giám sát thời gian thực cần tốc độ phản hồi tính bằng mili-giây.
- **Dataset:** Các tập dữ liệu log công khai và tập dữ liệu log công nghiệp thực tế.

---

### 36. `Lingzhe Zhang - A Survey of AIOps in the Era of Large Language Models [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá tổng quan về AIOps (Trí tuệ nhân tạo cho Vận hành CNTT) trong kỷ nguyên của các Mô hình Ngôn ngữ Lớn (LLMs).
- **Phương pháp (Đã làm gì):** Khảo sát 183 bài báo nghiên cứu (từ 2020 đến 2024) về LLM4AIOps. Phân tích cách LLMs giải quyết các nhược điểm của ML/DL truyền thống trong AIOps như: loại bỏ bước trích xuất đặc trưng thủ công (feature engineering), tăng cường khả năng tổng quát hóa chéo nền tảng (cross-platform generality) và linh hoạt chéo tác vụ (cross-task flexibility).
- **Điểm mạnh:** Chỉ ra sự thay đổi mô hình (paradigm shift) rõ ràng từ ML/DL truyền thống (vốn chỉ làm tốt một tác vụ cụ thể và dễ bị "thiu" dữ liệu) sang LLMs (có thể đọc trực tiếp log thô và xử lý nhiều tác vụ RCA cùng lúc). Rất cập nhật (năm 2025).
- **Điểm yếu:** Vẫn mang tính chất tổng hợp (Survey), không đề xuất một prompt chuẩn hay mô hình LLM tinh chỉnh cụ thể nào để người dùng có thể tải về chạy ngay.
- **Hướng phát triển:** Khám phá các phương pháp đánh giá (evaluation methodologies) mới được thiết kế riêng cho các hệ thống AIOps tích hợp LLM để đo lường độ ảo giác (hallucination) khi phân tích log.
- **Dataset:** Không có (Bài báo Review).

---

### 37. `Lipeng Ma - AdaptiveLog An Adaptive Log Analysis Framework with the Collaboration of Large and Small Language Model [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Giải quyết sự đánh đổi giữa hiệu suất (của LLMs) và chi phí/độ trễ (của các SLMs - mô hình ngôn ngữ nhỏ) trong bài toán phân tích log tự động.
- **Phương pháp (Đã làm gì):** Đề xuất framework AdaptiveLog, phối hợp giữa một LLM (như ChatGPT) và một SLM (như BERT). Những log đơn giản sẽ được giao cho SLM xử lý. LLM chỉ được gọi khi SLM có độ không chắc chắn (uncertainty) cao đối với các log phức tạp. Ngoài ra, sử dụng chiến lược prompt mới bằng cách truy xuất các ca lỗi tương tự trong quá khứ làm ngữ cảnh tham chiếu cho LLM.
- **Điểm mạnh:** Giải pháp cực kỳ tối ưu về mặt chi phí và hiệu năng. Giữ được độ chính xác ngang ngửa (state-of-the-art) với việc dùng LLM cho toàn bộ dữ liệu, nhưng lại tiết kiệm chi phí suy luận (inference cost) khổng lồ nhờ bộ lọc của SLM.
- **Điểm yếu:** Cấu trúc hệ thống phức tạp, phải duy trì, huấn luyện và triển khai song song cả hai loại mô hình (LLM và SLM) cùng với cơ sở dữ liệu vector để truy xuất ngữ cảnh.
- **Hướng phát triển:** Tích hợp các mô hình mã nguồn mở cỡ vừa (như Llama 3 8B) thay thế cho LLM thương mại để tối ưu chi phí hoàn toàn và đảm bảo tính riêng tư của log doanh nghiệp.
- **Dataset:** Các tập dữ liệu phân tích log chuẩn (BGL, HDFS, v.v.).

---

### 38. `Reinforcement_Learning-Based_Generative_Security_Framework_for_Host_Intrusion_Detection.pdf`

- **Chủ đề (Vấn đề giải quyết):** Xây dựng một Hệ thống Phát hiện Xâm nhập Máy chủ (HIDS) tự động sinh các tập luật phòng thủ chống lại các cuộc tấn công thay đổi liên tục.
- **Phương pháp (Đã làm gì):** Sử dụng Xử lý Ngôn ngữ Tự nhiên (NLP - cụ thể là TextRank) để trích xuất các từ khóa đặc trưng từ chuỗi log system call bất thường. Sau đó, kết hợp Học tăng cường (Reinforcement Learning - thuật toán Actor-Critic) với mô hình Seq2Seq đã được huấn luyện trước để tự động sinh ra các tập luật (rule set) phát hiện tối ưu cho từng loại tấn công.
- **Điểm mạnh:** Giải quyết được điểm yếu chí mạng của HIDS truyền thống là phụ thuộc vào chuyên gia bảo mật để viết luật thủ công. Tự động hóa quá trình sinh luật phòng thủ (generative security) với độ chính xác trung bình lên tới 96,5%.
- **Điểm yếu:** Quá trình huấn luyện bằng Học tăng cường và suy luận Seq2Seq tiêu tốn nhiều năng lực tính toán, có thể không phản ứng đủ nhanh (thời gian thực) đối với các cuộc tấn công có tốc độ lây lan cực nhanh so với hệ thống chặn bằng chữ ký (signature-based) tĩnh.
- **Hướng phát triển:** Tối ưu hóa hàm phần thưởng (reward function) trong RL để tạo ra các tập luật không chỉ chính xác mà còn phải ngắn gọn, ít tốn kém khi thực thi trên máy chủ.
- **Dataset:** Tập dữ liệu log system call (ADFA-LD, LID-DS 2021).

---

### 39. `SXAD_Shapely_eXplainable_AI-Based_Anomaly_Detection_Using_Log_Data.pdf`

- **Chủ đề (Vấn đề giải quyết):** Giải quyết vấn đề "hộp đen" (black-box) của các mô hình Học máy trong phát hiện bất thường log, nhằm tăng tính minh bạch, khả năng giải thích và độ tin cậy.
- **Phương pháp (Đã làm gì):** Đề xuất mô hình SXAD (Shapely eXplainable AI-Based Anomaly Detection). Tích hợp các kỹ thuật AI có thể giải thích được (XAI), cụ thể là giá trị SHAP (Shapley Additive exPlanations) với phương pháp Kernel Explainer vào các mô hình học máy để chỉ ra đích xác các sự kiện/tính năng (features) nào trong log HDFS gây ra dự đoán lỗi hệ thống.
- **Điểm mạnh:** Chuyển đổi các mô hình Học máy từ "hộp đen" sang "hộp trắng". Giúp các quản trị viên hệ thống (human-in-the-loop) hiểu rõ tại sao AI lại cảnh báo lỗi, đáp ứng hoàn hảo các nguyên tắc minh bạch của Công nghiệp 5.0 (Industry 5.0).
- **Điểm yếu:** Việc tính toán giá trị SHAP (đặc biệt là Kernel Explainer) tốn rất nhiều tài nguyên và thời gian tính toán, có thể gây thắt cổ chai (bottleneck) nếu áp dụng trực tiếp cho việc giám sát log theo thời gian thực ở quy mô dữ liệu lớn.
- **Hướng phát triển:** Nghiên cứu các phương pháp ước lượng SHAP xấp xỉ nhanh hơn (như TreeSHAP nếu dùng mô hình cây) để đảm bảo khả năng giải thích theo thời gian thực (real-time explainability).
- **Dataset:** Tập dữ liệu hệ thống chuẩn (HDFS logs).

---

### 40. `SXAD_Shapely_eXplainable_AI-based_Anomaly_Detectio.pdf`

- **Lưu ý:** Bài báo này là phiên bản trùng lặp (duplicate) hoặc được xuất bản lại của bài số 39 (`SXAD_Shapely_eXplainable_AI-Based_Anomaly_Detection_Using_Log_Data.pdf`). Nội dung phân tích tương tự bài 39.

---

### 41. `Shan Ali - A comprehensive study of machine learning techniques for log-based anomaly detection [2023].pdf`

- **Chủ đề (Vấn đề giải quyết):** Nghiên cứu thực nghiệm toàn diện so sánh các kỹ thuật Học máy (ML) truyền thống và Học sâu (DL) trong việc phát hiện bất thường từ log, nhằm phá bỏ định kiến cho rằng DL luôn tốt hơn ML truyền thống.
- **Phương pháp (Đã làm gì):** Đánh giá một loạt các kỹ thuật ML có giám sát, bán giám sát, truyền thống và học sâu dựa trên 4 tiêu chí: độ chính xác, thời gian thực thi (huấn luyện/dự đoán), và độ nhạy cảm đối với việc tinh chỉnh siêu tham số (hyperparameter tuning).
- **Điểm mạnh:** Cung cấp bằng chứng thực nghiệm mạnh mẽ cho thấy các kỹ thuật ML truyền thống (có giám sát) đạt độ chính xác và tốc độ ngang ngửa Học sâu trên hầu hết các bộ dữ liệu chuẩn, nhưng lại **ít nhạy cảm hơn rất nhiều** với các cấu hình siêu tham số (tức là bền vững và dễ triển khai thực tế hơn).
- **Điểm yếu:** Chỉ là một bài nghiên cứu đánh giá (benchmark), không đề xuất phương pháp hay kiến trúc mô hình mới nào. Kết quả cũng chỉ ra các kỹ thuật bán giám sát hoạt động kém hơn đáng kể.
- **Hướng phát triển:** Tập trung phát triển các mô hình ML truyền thống được tối ưu hóa cho tốc độ và độ ổn định thay vì tốn kém tài nguyên để chạy các mô hình Học sâu phức tạp trong môi trường giám sát log.
- **Dataset:** Các bộ dữ liệu log tiêu chuẩn (benchmark datasets).

---

### 42. `Song Chen - BERT-Log Anomaly Detection for System Logs Based on Pre-trained Language Model [2022].pdf`

- **Chủ đề (Vấn đề giải quyết):** Ứng dụng Mô hình Ngôn ngữ được Huấn luyện trước (Pre-trained Language Model) để phát hiện bất thường từ nhật ký hệ thống, khắc phục nhược điểm của Word2Vec (bỏ qua thứ tự từ) và LSTM (hạn chế biểu diễn ngữ nghĩa sâu).
- **Phương pháp (Đã làm gì):** Đề xuất mô hình BERT-Log. Coi chuỗi log như chuỗi ngôn ngữ tự nhiên, sử dụng mô hình ngôn ngữ BERT để học biểu diễn ngữ nghĩa, sau đó dùng một mạng nơ-ron kết nối đầy đủ (FCNN) để tinh chỉnh (fine-tune) và phân loại. Đề xuất một bộ trích xuất đặc trưng log mới sử dụng cửa sổ trượt (sliding window) kết hợp với node ID.
- **Điểm mạnh:** Tận dụng được sức mạnh của cơ chế Attention trong BERT, nắm bắt toàn bộ thông tin ngữ nghĩa bao gồm cả ngữ cảnh và vị trí của từ. Đạt hiệu suất cực cao (F1-score 99,3% trên HDFS và 99,4% trên BGL, vượt qua LogRobust tới 19%).
- **Điểm yếu:** Mô hình BERT rất nặng và tốn kém tài nguyên tính toán (GPU/TPU) để huấn luyện cũng như suy luận (inference) so với các phương pháp ML truyền thống hoặc các mô hình mạng nơ-ron nhỏ hơn.
- **Hướng phát triển:** Cắt tỉa (pruning) hoặc chưng cất (distillation) mô hình BERT để làm nhẹ BERT-Log, giúp mô hình có thể chạy giám sát thời gian thực trên các máy chủ có cấu hình thấp.
- **Dataset:** HDFS dataset, BGL dataset.

---

### 43. `Suhail Adel Alansary - Emerging AI threats in cybercrime a review of zero-day attacks via machine, deep, and federated learnin.pdf`

- **Chủ đề (Vấn đề giải quyết):** Đánh giá tổng quan về các mối đe dọa AI mới nổi trong tội phạm mạng và các chiến lược phòng thủ chống lại các cuộc tấn công Zero-day bằng Học máy (ML), Học sâu (DL) và Học liên kết (Federated Learning - FL).
- **Phương pháp (Đã làm gì):** Nghiên cứu tổng quan (Review). Phân tích cách AI được sử dụng không chỉ để phòng thủ (phát hiện bất thường và dự đoán lỗ hổng theo thời gian thực) mà còn cách tin tặc lợi dụng AI để khai thác các lỗ hổng chưa được biết đến (zero-day). Làm nổi bật tiềm năng của Học liên kết (FL) trong việc chia sẻ trí thông minh mối đe dọa (threat intelligence) mà không làm lộ dữ liệu nhạy cảm.
- **Điểm mạnh:** Giải quyết đúng trọng tâm vào các cuộc tấn công Zero-day mà các hệ thống IDS truyền thống (dựa trên chữ ký) hoàn toàn bó tay. Nhấn mạnh tầm quan trọng của việc duy trì quyền riêng tư thông qua Học liên kết. Bài viết rất mới (năm 2025).
- **Điểm yếu:** Chỉ là nghiên cứu tổng hợp, không đề xuất một kiến trúc mã nguồn mở cụ thể. Nhấn mạnh thách thức cố hữu của ML là xử lý dữ liệu mất cân bằng (imbalanced data) và chi phí tính toán cao.
- **Hướng phát triển:** Tích hợp AI tạo sinh (Generative AI) và Học liên kết để chủ động dự đoán và vá các lỗ hổng phần mềm từ trước khi tin tặc kịp phát hiện.
- **Dataset:** Không có (Bài báo Review).

---

### 44. `System Logs Anomaly Detection. Are we on the right path .pdf`

- **Chủ đề (Vấn đề giải quyết):** Đặt câu hỏi về tính thực tiễn của các phương pháp phát hiện bất thường hiện tại, đặc biệt là giới hạn của các phương pháp Học sâu bán giám sát (semi-supervised DL) đòi hỏi lượng dữ liệu "chuẩn bình thường" khổng lồ.
- **Phương pháp (Đã làm gì):** Đề xuất một phương pháp hoàn toàn không giám sát (fully unsupervised heuristics) thay thế cho giai đoạn giám sát của các phương pháp bán giám sát. Sử dụng phương pháp khủy tay (elbow method), khoảng tứ phân vị (IQR) và Thuật toán tôi luyện mô phỏng (Simulated Annealing). Đồng thời, đề xuất một bộ benchmark mới, thực tế hơn (tách dữ liệu theo thời gian thực tế thay vì chia ngẫu nhiên).
- **Điểm mạnh:** Chỉ ra một "lỗ hổng" lớn trong nghiên cứu học thuật hiện tại: giả định rằng dữ liệu huấn luyện luôn "sạch" và dán nhãn hoàn hảo là phi thực tế trong hệ sinh thái quy mô lớn. Phương pháp đề xuất cực kỳ thực tiễn và dễ triển khai trên dữ liệu thực.
- **Điểm yếu:** Việc tinh chỉnh các cấu hình heuristic (như elbow method hay Simulated Annealing) vẫn cần sự can thiệp thủ công từ kỹ sư để đạt độ chính xác tối ưu cho các môi trường log khác nhau.
- **Hướng phát triển:** Kết hợp các phương pháp heuristic không giám sát với các hệ thống AI phân tích tự động để loại bỏ hoàn toàn sự phụ thuộc vào nhãn dữ liệu.
- **Dataset:** Các bộ dữ liệu log tiêu chuẩn nhưng được đánh giá trên phương pháp chia tách (split) mới.

---

### 45. `Vignes V M - AI-driven cybersecurity framework for anomaly detection in power systems [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện sự cố/xâm nhập mạng (anomalies) cho các hệ thống điện lưới thông minh (smart grid) - môi trường hệ thống không gian mạng vật lý (Cyber-Physical Systems - CPS).
- **Phương pháp (Đã làm gì):** Đề xuất một framework an ninh mạng điều khiển bằng AI. Dung hợp (fusion) dữ liệu đa nguồn từ cả không gian mạng (lưu lượng mạng mạng, cảnh báo Snort) lẫn dữ liệu vật lý (số đo cấp giao thức DNP3). Sử dụng Học sâu (LSTM, GRU) để nắm bắt chuỗi thời gian, kết hợp với AI giải thích được (SHAP) và kỹ thuật huấn luyện đối nghịch (adversarial training - FGSM) để chống lại các nỗ lực né tránh.
- **Điểm mạnh:** Khung bảo mật toàn diện cho môi trường IoT/Smart Grid. Không chỉ phát hiện chính xác lỗi mà còn giải thích được nguyên nhân (thông qua SHAP) và có khả năng triển khai thực tế trên các thiết bị Edge (như Xilinx PYNQ-Z2) nhờ mô hình Random Forest hạng nhẹ.
- **Điểm yếu:** Khung giải pháp được tối ưu hóa quá chuyên biệt cho kiến trúc lưới điện và giao thức DNP3, sẽ cần phải thiết kế lại đáng kể nếu muốn áp dụng cho các hệ thống CNTT doanh nghiệp hoặc đám mây thông thường.
- **Hướng phát triển:** Mở rộng framework để hỗ trợ thêm các giao thức công nghiệp khác như IEC 61850 và Modbus trong các nhà máy thông minh.
- **Dataset:** Cyber-Physical Dataset for MiTM Attacks in Power Systems (Đại học Texas A&M).

---

### 46. `Xuefeng Chen - Large Models for Machine Monitoring and Fault Diagnostics Opportunities, Challenges and Future Direction [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Khám phá cơ hội, thách thức và định hướng tương lai của các Mô hình Lớn (Large Models - đặc biệt là LLMs) trong việc giám sát máy móc và chẩn đoán lỗi (PHM - Prognostics and Health Management).
- **Phương pháp (Đã làm gì):** Đánh giá các phương pháp dựa trên Mô hình lớn như: Học trong ngữ cảnh (In-Context Learning - ICL), Tinh chỉnh (fine-tuning), Tạo văn bản tăng cường truy xuất (RAG), và học đa phương thức (multimodal). Đề xuất một lộ trình 3 giai đoạn cho PHM dựa trên LLM: tăng cường tri thức (knowledge-enhanced), hướng tác vụ (task-driven), và tự học (self-learning).
- **Điểm mạnh:** Đưa ra một lộ trình cực kỳ chi tiết và cập nhật (năm 2025) để ứng dụng LLMs vào công nghiệp nặng/bảo trì thông minh. Trình bày rõ cách Prompt Engineering và RAG có thể biến LLM thành một chuyên gia chẩn đoán có khả năng giải thích lỗi bằng ngôn ngữ tự nhiên.
- **Điểm yếu:** Là một bài báo định hướng (roadmap/review), chưa có mô hình LLM từ đầu nào được huấn luyện dành riêng cho mảng này. Hiện tượng "ảo giác" (hallucination) của LLMs khi không có ràng buộc vật lý chặt chẽ vẫn là rào cản lớn.
- **Hướng phát triển:** Tích hợp các kiến thức nền tảng về vật lý công nghiệp vào LLM và tối ưu hóa các mô hình lớn để chạy được trên các thiết bị Edge tại nhà máy.
- **Dataset:** Không có (Bài báo Review/Roadmap).

---

### 47. `Xuhan Zhu - CoLA Model Collaboration for Log-based Anomaly Detection [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Tối ưu hóa sự đánh đổi giữa hiệu năng xử lý (của mô hình nhỏ) và độ chính xác/khả năng giải thích (của LLM) trong phát hiện bất thường từ luồng log liên tục thay đổi.
- **Phương pháp (Đã làm gì):** Đề xuất kiến trúc CoLA (Collaborative Log Anomaly detection framework). Kết hợp một Mô hình Phát hiện Nhỏ (SDM) sử dụng cấu trúc Mixture-of-Experts (LogMoE) để lọc tốc độ cao các log nghi ngờ, và một LLM (LAD-LLM) đóng vai trò chuyên gia để thẩm định, đưa ra lời giải thích. Đặc biệt, kết quả từ LLM được dùng để liên tục tinh chỉnh (refine) SDM thông qua kỹ thuật học nhãn nhiễu (noisy label learning) mà không cần con người can thiệp.
- **Điểm mạnh:** Giải quyết triệt để nút thắt hiệu suất của LLM trong thời gian thực. Tạo ra một vòng lặp học tập liên tục (continuous learning loop) hoàn toàn tự động, giúp mô hình nhỏ luôn thích ứng được với sự thay đổi của log (evolving log streams).
- **Điểm yếu:** Kiến trúc hệ thống kép phức tạp. Cần cơ chế điều phối và kỹ thuật xử lý nhãn nhiễu tinh vi để đảm bảo mô hình nhỏ (SDM) không bị học sai nếu LLM vô tình đưa ra đánh giá ảo giác.
- **Hướng phát triển:** Mở rộng cơ chế cộng tác này ra các hệ thống phát hiện xâm nhập đa luồng (như network traffic kết hợp system log) thay vì chỉ phân tích log đơn thuần.
- **Dataset:** Các luồng dữ liệu log thay đổi liên tục trong thực tế (Evolving log streams).

---

### 48. `Y. Al-Khassawneh - A Review of Artificial Intelligence in Security and Privacy Research Advances, Applications, Opportunities,.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tổng quan về Trí tuệ Nhân tạo trong An ninh và Quyền riêng tư: Các phương pháp tấn công vào hệ thống AI (Adversarial AI) và biện pháp phòng thủ.
- **Phương pháp (Đã làm gì):** Bài báo tập hợp và tóm tắt các cuộc tấn công đối kháng (adversarial attacks) nhắm vào các ứng dụng AI như: Tấn công đầu độc (Poisoning attacks - chèn dữ liệu độc hại vào tập huấn luyện) và Tấn công lẩn tránh (Evasion attacks - tinh chỉnh dữ liệu đầu vào để đánh lừa mô hình trong quá trình dự đoán). Đồng thời điều tra các biện pháp phòng thủ tương ứng.
- **Điểm mạnh:** Cung cấp góc nhìn hai chiều quan trọng: AI không chỉ là công cụ bảo mật, mà chính AI cũng là một mục tiêu mong manh cần được bảo vệ. Cung cấp một cách tiếp cận có hệ thống để thiết lập các chiến lược phòng thủ cho ML/DL.
- **Điểm yếu:** Là một bài đánh giá tổng quan (Review) khá cơ bản (xuất bản 2023), thiếu các bằng chứng thực nghiệm và không công bố framework/mô hình phòng thủ cụ thể.
- **Hướng phát triển:** Cần nghiên cứu sâu hơn vào các thuật toán phòng thủ mạnh mẽ (Robust ML) có thể chịu đựng được các cuộc tấn công đối kháng mà không làm suy giảm độ chính xác của dự đoán thông thường.
- **Dataset:** Không có (Bài báo Review).

---

### 49. `Yihan Zhou - Leveraging Large Language Models and BERT for Log Parsing and Anomaly Detection [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Cải thiện quá trình phân tích cú pháp log (log parsing) và phát hiện bất thường bằng cách tận dụng sức mạnh của Mô hình Ngôn ngữ Lớn (LLMs) kết hợp với BERT.
- **Phương pháp (Đã làm gì):** Thay thế các công cụ phân tích log truyền thống (như Drain, Spell) bằng LLM (ChatGPT) thông qua zero-shot và few-shot learning để trích xuất các template log chính xác, lọc bỏ nhiễu. Sử dụng TF-IDF để trích xuất đặc trưng và đưa vào mô hình ngôn ngữ BERT (với cơ chế self-attention) để phát hiện các log bất thường dựa trên ngữ cảnh.
- **Điểm mạnh:** Vượt qua điểm yếu chí mạng của các công cụ phân tích log truyền thống là không thể xử lý các mẫu log chưa từng thấy (unseen logs) hoặc cấu trúc phức tạp. Kết hợp được khả năng đọc hiểu ngữ nghĩa vượt trội của ChatGPT và khả năng phân tích chuỗi của BERT.
- **Điểm yếu:** Phụ thuộc vào ChatGPT để phân tích log là một quy trình cực kỳ đắt đỏ và chậm chạp nếu áp dụng cho hệ thống phân tán quy mô lớn sinh ra hàng triệu dòng log mỗi phút.
- **Hướng phát triển:** Nghiên cứu cách chưng cất (distill) khả năng phân tích log của ChatGPT sang một mô hình nhẹ hơn chạy offline để giải quyết bài toán chi phí/thời gian.
- **Dataset:** HDFS và BGL (các tập dữ liệu log tiêu chuẩn).

---

### 50. `Yiheng Zhang - LogiCode An LLM-Driven Framework for Logical Anomaly Detection [2024].pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện các bất thường về mặt logic (Logical Anomaly) trong công nghiệp (ví dụ: các linh kiện hoàn toàn bình thường nhưng bị lắp sai thứ tự, sai cấu hình) thay vì chỉ phát hiện các bất thường về cấu trúc vật lý (móp, xước).
- **Phương pháp (Đã làm gì):** Đề xuất kiến trúc LogiCode điều khiển bởi LLM. Thay vì trả về "điểm số bất thường" (anomaly score) mù mờ, LogiCode trích xuất các quy tắc logic từ trạng thái bình thường (kết hợp kiến thức chuyên gia), sau đó LLM tự động dịch các quy tắc này thành mã nguồn Python thực thi được. Mã Python này sẽ dùng để kiểm tra tính nhất quán logic của dữ liệu mới.
- **Điểm mạnh:** Một bước đột phá trong việc tạo ra tính minh bạch (interpretability). Thay vì là một "hộp đen", LogiCode biến các quy tắc giám sát thành code Python rõ ràng và có thể giải thích đích xác nguyên nhân gây lỗi bằng ngôn ngữ tự nhiên, bắt chước tư duy con người.
- **Điểm yếu:** Yêu cầu phải xác định trước và trích xuất các quy tắc logic bằng kiến thức chuyên gia ở giai đoạn đầu. Phụ thuộc lớn vào khả năng sinh code (code generation) không có lỗi cú pháp của LLM.
- **Hướng phát triển:** Cải thiện LLM để tự động khám phá và trích xuất các quy tắc logic phức tạp từ dữ liệu thô mà không cần chuyên gia mồi (prompt) trước.
- **Dataset:** MVTec LOCO AD và bộ dữ liệu mới đề xuất LOCO-Annotations.

---

### 51. `Yongqian Sun - Accurate and Interpretable Log-Based Fault Diagnosis Using Large Language Models [2025].pdf`

- **Chủ đề (Vấn đề giải quyết):** Chẩn đoán lỗi chính xác và có khả năng giải thích dựa trên Log bằng cách sử dụng Mô hình Ngôn ngữ Lớn (LLMs), khắc phục giới hạn cửa sổ ngữ cảnh (context-length) của LLM.
- **Phương pháp (Đã làm gì):** Đề xuất framework LogInsight. Thực hiện tinh chỉnh (fine-tune) một LLM mã nguồn mở cỡ vừa bằng kiến thức chuyên ngành. Để giải quyết việc LLM không thể đọc hết một file log quá dài, nhóm nghiên cứu thiết kế mô đun Tóm tắt Log Hướng Lỗi (FOLS - Fault-Oriented Log Summary) để trích xuất các thông tin cốt lõi nhất từ chuỗi log trước khi nạp vào LLM.
- **Điểm mạnh:** Giải quyết được bài toán hóc búa nhất khi dùng LLM phân tích log là giới hạn độ dài ngữ cảnh (context window) mà không cần phải can thiệp sâu để mở rộng cửa sổ ngữ cảnh của LLM. Hệ thống không chỉ phân loại lỗi (triage) mà còn cung cấp lời giải thích minh bạch cho các kỹ sư O&M. Vượt qua các baseline tiên tiến nhất (SOTA).
- **Điểm yếu:** Việc fine-tune một LLM mã nguồn mở cỡ vừa và chạy một mô-đun tóm tắt FOLS trước đó vẫn đòi hỏi tài nguyên tính toán (GPU) rất lớn so với các giải pháp máy học truyền thống.
- **Hướng phát triển:** Tối ưu hóa mô đun FOLS để nó hoạt động nhanh hơn với độ trễ siêu thấp, phục vụ cho chẩn đoán sự cố theo thời gian thực (real-time fault diagnosis).
- **Dataset:** Hai bộ dữ liệu công khai và một bộ dữ liệu từ môi trường sản xuất thực tế.

---

### 52. `applsci-13-04495-v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phân tích tính khả thi và tiện ích của việc sử dụng Học liên kết (Federated Learning - FL) trong việc phát hiện bất thường dữ liệu log.
- **Phương pháp (Đã làm gì):** So sánh các mô hình Học sâu tập trung truyền thống (CNN1D, LSTM) với kiến trúc Học liên kết (sử dụng FedAVG). Đặc biệt, đề xuất một mô hình lai (hybrid CNN1D-LSTM model) được huấn luyện trong môi trường phân tán.
- **Điểm mạnh:** Giải quyết triệt để rủi ro rò rỉ dữ liệu nhạy cảm của người dùng (như tài khoản, mật khẩu có thể bị ghi lại trong log). Trong Học liên kết, dữ liệu log thô không bao giờ rời khỏi máy chủ cục bộ, chỉ có trọng số mô hình (model weights) được truyền về máy chủ trung tâm. Mô hình lai cũng cho hiệu suất tốt hơn so với mô hình đơn lẻ.
- **Điểm yếu:** Học liên kết sinh ra chi phí truyền tải mạng (communication overhead) lớn và có thể bị giảm độ chính xác nếu phân phối log giữa các máy chủ cục bộ quá khác biệt (non-IID).
- **Hướng phát triển:** Nghiên cứu kỹ thuật giảm thiểu dung lượng truyền tải trọng số (model compression) để áp dụng mượt mà trên môi trường mạng băng thông thấp.
- **Dataset:** Tập dữ liệu log hệ thống (thử nghiệm trên các cấu hình máy chủ phân tán).

---

### 53. `applsci-13-07297-v3.pdf`

- **Chủ đề (Vấn đề giải quyết):** ADAL-NN: Phát hiện và Định vị (Localization) bất thường bằng cách sử dụng Học quan hệ sâu (Deep Relational Learning) trong hệ thống phân tán.
- **Phương pháp (Đã làm gì):** Sử dụng các định danh (Identifiers - IDs) để nhóm các dòng log bị xáo trộn (interleaved logs). Xây dựng Đồ thị Quan hệ ID (ID relation graphs) giữa các thành phần phân tán. Đề xuất một bộ phân tích log tự động (parameter-free online log parser) và sử dụng mô hình Bi-LSTM với cơ chế Attention để tìm các điểm bất thường ở cấp độ phiên bản (instance-granularity).
- **Điểm mạnh:** Không chỉ phát hiện CÓ bất thường hay không, mà còn định vị chính xác thành phần/hệ thống con (subsystem) nào gây ra lỗi. Xử lý xuất sắc các luồng log bị xáo trộn từ các tiến trình chạy song song.
- **Điểm yếu:** Việc xây dựng đồ thị quan hệ phụ thuộc nhiều vào việc các hệ thống phân tán (microservices) phải có chung chuẩn ghi log chứa ID (ví dụ: Trace ID). Điều này có thể không khả thi trên các hệ thống cũ (legacy systems).
- **Hướng phát triển:** Kết hợp phân tích mã nguồn phân tán để tự động nối ghép các chuỗi sự kiện không có ID chuẩn.
- **Dataset:** Các tập dữ liệu thực tế (real-world datasets) và tập dữ liệu tổng hợp (synthetic datasets).

---

### 54. `applsci-14-10217.pdf`

- **Chủ đề (Vấn đề giải quyết):** Tự động hóa hoạt động phản ứng với các mối đe dọa tấn công (Hacking) bằng công nghệ Tự động hóa Quy trình Bằng Robot (RPA) dựa trên AI.
- **Phương pháp (Đã làm gì):** Đề xuất một hệ thống AI-RPA được thiết kế đặc biệt cho các tổ chức chính phủ/công cộng. RPA tự động hóa việc thu thập, phân tích, chuẩn hóa định dạng và phân phối các log đe dọa từ nhiều nguồn khác nhau. Hệ thống thay thế sự can thiệp của con người để loại bỏ các cảnh báo giả (false positive) và tạo nền tảng tập trung (centralized) cho các mô hình AI trong tương lai.
- **Điểm mạnh:** Một giải pháp cực kỳ thực tế và tiết kiệm chi phí cho các tổ chức nhà nước. Công nghệ RPA cho phép triển khai tự động hóa trực tiếp trên lớp giao diện/hệ thống cũ mà không cần phải đập bỏ hay thay đổi kiến trúc cơ sở dữ liệu hiện hành.
- **Điểm yếu:** Bản chất của RPA là tự động hóa các quy trình thủ công mang tính lặp lại. "Sự thông minh" phụ thuộc vào việc tích hợp AI sau đó, RPA tự nó không "dự đoán" được tấn công chưa biết.
- **Hướng phát triển:** Tích hợp trực tiếp các mô hình LLM vào quy trình của RPA để tự động viết báo cáo tình báo mối đe dọa thay vì chỉ chuyển tiếp log.
- **Dataset:** Log đe dọa thu thập từ các hệ thống cơ quan, tổ chức thực tế.

---

### 55. `applsci-15-07237-v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Khắc phục những hạn chế của các mô hình học máy thụ động trong phân tích log (thiếu khả năng giải thích, kém thích ứng) bằng cách sử dụng Tác nhân AI (AI Agent) để tự động hóa việc phát hiện và điều tra nguyên nhân.
- **Phương pháp (Đã làm gì):** Đề xuất LogRESP-Agent, một framework AI dạng mô-đun xoay quanh một LLM Agent có khả năng lập luận. Hệ thống kết hợp: (1) Phát hiện bất thường bằng LLM có giải nghĩa ngữ nghĩa, (2) Suy luận mối đe dọa theo ngữ cảnh thông qua RAG (Retrieval-Augmented Generation), và (3) Khả năng điều tra đệ quy (recursive) gồm nhiều bước phân tích sâu vào các log hỗn hợp.
- **Điểm mạnh:** Vượt ra khỏi khuôn khổ "nhận diện thụ động" (passive detection) truyền thống để hướng tới một Tác nhân (Agent) chủ động điều tra, tự động sinh kế hoạch, và giải thích chi tiết chuỗi sự kiện tấn công (TTP). Đạt độ chính xác cực cao (99.97% trên tập Monster-THC).
- **Điểm yếu:** Một AI Agent hoạt động đệ quy và liên tục gọi API của các LLM lớn/RAG để điều tra log sẽ tiêu tốn tài nguyên khổng lồ và có thể gặp khó khăn về tốc độ phản hồi (latency) đối với các hệ thống yêu cầu real-time nghiêm ngặt.
- **Hướng phát triển:** Tối ưu hóa chuỗi suy luận (prompt routing) của Agent để giảm thiểu số bước gọi LLM không cần thiết nhằm tối ưu hóa chi phí và tốc độ.
- **Dataset:** Tập dữ liệu Monster-THC và tập EVTX-ATTACK-SAMPLES.

---

### 56. `fphy-12-1401857.pdf`

- **Chủ đề (Vấn đề giải quyết):** Nâng cao độ chính xác và tính mạnh mẽ (robustness) của việc phát hiện bất thường từ log thông qua phân tích đa giai đoạn.
- **Phương pháp (Đã làm gì):** Đề xuất LogMS, một phương pháp đa giai đoạn. Giai đoạn 1 sử dụng mạng MSIF-LSTM kết hợp nhiều nguồn thông tin (ngữ nghĩa, tuần tự, định lượng) sau khi log được parse bằng Drain và mã hóa bằng TF-IDF. Giai đoạn 2 (chỉ kích hoạt nếu giai đoạn 1 không tìm thấy lỗi) sử dụng mạng PLE-GRU kết hợp ước lượng nhãn xác suất (tạo dữ liệu pseudo-labeled từ các log bình thường).
- **Điểm mạnh:** Hiệu quả về mặt tính toán vì Giai đoạn 2 chỉ kích hoạt như một bộ lọc sâu khi Giai đoạn 1 chưa phát hiện lỗi. Tận dụng tối đa nhiều góc nhìn thông tin và các nhãn log "bình thường" vốn rất dễ thu thập trong thực tế.
- **Điểm yếu:** Cấu trúc phân đoạn đa tầng có thể làm tích lũy độ trễ. Quá trình parse vẫn phụ thuộc vào thuật toán Drain truyền thống, có thể gặp khó khăn với các mẫu log hoàn toàn mới (unseen patterns).
- **Hướng phát triển:** Kết hợp các kỹ thuật trích xuất ngữ nghĩa nâng cao (như LLMs hoặc BERT) thay thế cho TF-IDF để cải thiện sức mạnh của Giai đoạn 1.
- **Dataset:** Các tập dữ liệu HDFS và BGL.

---

### 57. `s10462-025-11167-0.pdf`

- **Chủ đề (Vấn đề giải quyết):** Thiếu một cái nhìn toàn cảnh và dữ liệu trắc lượng thư mục (bibliometric) về tình hình nghiên cứu các mô hình phát hiện tấn công mạng bằng Trí tuệ Nhân tạo.
- **Phương pháp (Đã làm gì):** Phân tích trắc lượng thư mục (Bibliometric analysis) trên cơ sở dữ liệu Scopus với hơn 2,338 bài báo từ năm 2014 đến 2024. Sử dụng công cụ thống kê R và Biblioshiny để đánh giá các tác giả, quốc gia, xu hướng hợp tác, và các từ khóa chính.
- **Điểm mạnh:** Cung cấp bức tranh toàn cảnh cực kỳ giá trị về xu hướng nghiên cứu toàn cầu. Chỉ ra rằng ML và DL là công cụ phổ biến nhất hiện nay, Mỹ, Trung Quốc và Ấn Độ là các quốc gia dẫn đầu về nghiên cứu này. Giúp định hướng cho các nhà nghiên cứu tương lai.
- **Điểm yếu:** Đây là một bài báo phân tích dữ liệu thống kê khoa học (Review/Bibliometric), không phải là một bài báo kỹ thuật đề xuất một mô hình/kiến trúc mới.
- **Hướng phát triển:** Sử dụng các kết quả từ bài báo này để định vị và lập kế hoạch cho các hướng nghiên cứu sâu hơn về Explainable AI (XAI) và bảo mật dữ liệu IoT - những vùng đang được quan tâm nhiều nhất.
- **Dataset:** Siêu dữ liệu từ cơ sở dữ liệu Scopus (2,338 bài báo).

---

### 58. `s11280-023-01174-y.pdf`

- **Chủ đề (Vấn đề giải quyết):** Giải quyết bài toán thiếu dữ liệu log bất thường được gán nhãn trong thực tế bằng mô hình học bán giám sát (semi-supervised learning).
- **Phương pháp (Đã làm gì):** Đề xuất SSDLog, một mô hình nhánh kép bán giám sát (semi-supervised dual branch model). Bao gồm một mô hình "giáo viên" (teacher) với nhiễu tăng cường nhẹ (weak augmented) và một mô hình "học sinh" (student) với nhiễu tăng cường mạnh (strong augmented). Áp dụng chiến lược sàng lọc nhãn linh hoạt dựa trên độ tin cậy và tính ổn định của các nhãn giả (pseudo-labels).
- **Điểm mạnh:** Giải quyết triệt để sự thiếu hụt dữ liệu gán nhãn. Chỉ với 30% dữ liệu huấn luyện được gán nhãn, mô hình có thể đạt được độ chính xác tương đương với các mô hình học giám sát hoàn toàn (fully supervised), rất phù hợp với môi trường thực tế khó thu thập log lỗi.
- **Điểm yếu:** Huấn luyện nhánh kép với gán nhãn giả (pseudo-labeling) tiêu tốn nhiều năng lực tính toán hơn so với mạng nhánh đơn truyền thống. Hiệu quả phụ thuộc vào tính liên tục của không gian đặc trưng khi thêm nhiễu Gauss.
- **Hướng phát triển:** Nghiên cứu các phương pháp tăng cường dữ liệu (data augmentation) tinh vi hơn ngoài nhiễu Gauss, được thiết kế đặc thù cho ngôn ngữ tự nhiên của log.
- **Dataset:** Tập dữ liệu HDFS và tập ứng dụng Hadoop.

---

### 59. `s13677-025-00765-6.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện các cuộc tấn công tiêm nhiễm (injection attacks) và giám sát bất thường trong các ứng dụng web trên nền tảng đám mây, chú trọng đến bảo mật quyền riêng tư.
- **Phương pháp (Đã làm gì):** Đề xuất Trình phân tích Log Bán giám sát (SSLA). Hệ thống sử dụng mô hình Mạng chập Đồ thị (Graph Convolutional Network - GCN) huấn luyện trên cả dữ liệu có nhãn và không nhãn. Đặc biệt, hệ thống tích hợp cơ chế Quyền riêng tư vi phân (Differential Privacy) trong quá trình xây dựng đồ thị để bảo vệ dữ liệu nhạy cảm.
- **Điểm mạnh:** Sự kết hợp độc đáo giữa GCN và Differential Privacy. Không chỉ phát hiện tấn công (SQLi, XSS) với độ chính xác cao mà còn đảm bảo các log chứa thông tin người dùng được bảo vệ nghiêm ngặt. Hệ thống còn được thiết kế tối ưu hóa QoS (độ trễ thấp, băng thông cao).
- **Điểm yếu:** Differential Privacy luôn mang lại sự đánh đổi (trade-off) giữa quyền riêng tư và độ chính xác (nhiễu vi phân làm giảm nhẹ sức mạnh dự đoán). Việc huấn luyện GCN trên đồ thị quy mô lớn rất phức tạp.
- **Hướng phát triển:** Nghiên cứu cơ chế cân bằng động (dynamic balancing) giữa mức độ bảo vệ quyền riêng tư và độ nhạy trong phát hiện tấn công theo thời gian thực.
- **Dataset:** Log của HDFS và BGL.

---

### 60. `s13677-025-00789-y.pdf`

- **Chủ đề (Vấn đề giải quyết):** Cách mạng hóa các hoạt động an ninh mạng bằng mô hình học sâu tích hợp: vừa giám sát log thời gian thực, vừa phân tích pháp y (forensic analysis) truy xuất dòng thời gian tấn công.
- **Phương pháp (Đã làm gì):** Đề xuất một framework học sâu lai (hybrid deep learning) kết hợp kiến trúc LSTM (xử lý tuần tự) và Transformer (xử lý ngữ cảnh). Tích hợp "Công cụ tương quan pháp y" (forensic correlation engine) để tự động xâu chuỗi log từ nhiều nguồn (Hệ thống, Mạng, Ứng dụng) và xây dựng lại dòng thời gian tấn công (attack timeline).
- **Điểm mạnh:** Giải pháp toàn diện không chỉ dừng lại ở việc báo động (alert), mà còn cung cấp khả năng điều tra pháp y tự động. Khắc phục được nhược điểm thiếu ngữ cảnh của LSTM và tận dụng được khả năng chú ý (attention) của Transformer. Độ chính xác lên đến 98.2%.
- **Điểm yếu:** Việc kết hợp cả hai kiến trúc nặng (LSTM + Transformer) và xử lý log chéo từ nhiều nguồn (Network, App, System) đòi hỏi năng lực phần cứng máy chủ cực mạnh để đáp ứng yêu cầu giám sát thời gian thực.
- **Hướng phát triển:** Tối ưu hóa kiến trúc lai bằng cách sử dụng các phiên bản nhẹ hơn (như DistilBERT hoặc Fast-LSTM) để giảm áp lực phần cứng cho các hệ thống nhỏ hơn.
- **Dataset:** HDFS, CICIDS, và UNSW-NB15.

---

### 61. `s41598-023-35198-1.pdf`

- **Chủ đề (Vấn đề giải quyết):** Dự báo trước (predictive forecasting) các cuộc tấn công mạng dài hạn bằng cách sử dụng các nguồn dữ liệu lớn (big data) và Kỹ thuật Học máy, thay vì chỉ phát hiện (detection) thụ động.
- **Phương pháp (Đã làm gì):** Thu thập và trích xuất các đặc trưng không đồng nhất từ các nguồn dữ liệu lớn phi cấu trúc như: dữ liệu sự cố toàn cầu (Hackmageddon), cơ sở dữ liệu học thuật (Elsevier/Scopus API), và tín hiệu mạng xã hội (Twitter). Đưa các dữ liệu này vào mô hình Học máy để dự báo xu hướng tấn công không gian mạng lên đến 3 năm trong tương lai.
- **Điểm mạnh:** Chuyển dịch tư duy từ phòng thủ phản ứng (reactive) sang phòng thủ chủ động (proactive). Phân tích trên quy mô vĩ mô (với 9 triệu tweet, 15,000 sự cố, 36 quốc gia) giúp các tổ chức an ninh mạng có đủ thời gian chuẩn bị ngân sách và chiến lược phòng thủ dài hạn.
- **Điểm yếu:** Dự báo mang tính vĩ mô (macro-trend) nên khó có thể cung cấp các thông tin hành động chi tiết ở mức độ vi mô (như IP nào sẽ tấn công vào server nào ngày mai). Dự báo không thay thế được các công cụ bảo mật thời gian thực tại các thiết bị đầu cuối.
- **Hướng phát triển:** Kết hợp các dự báo vĩ mô với các dữ liệu mối đe dọa vi mô (Threat Intelligence Feeds) để tạo ra các cảnh báo có tính "hành động" cao hơn cho từng hệ thống cụ thể.
- **Dataset:** Dữ liệu sự cố Hackmageddon, Elsevier API (Scopus), Twitter (Social media signals).

---

### 62. `s41598-025-27693-4_reference.pdf`

- **Chủ đề (Vấn đề giải quyết):** Thiếu một khuôn khổ thống nhất để phát hiện đồng thời cả bất thường điểm (point anomaly - sự kiện đơn lẻ) và bất thường tập hợp (collective anomaly - chuỗi sự kiện) trong log hệ điều hành có nhiều thể thức (multimodal).
- **Phương pháp (Đã làm gì):** Đề xuất kiến trúc CoLog, một khuôn khổ đa phương thức sử dụng "Collaborative Transformers" và cơ chế chú ý "Multi-head impressed attention". CoLog học các tương tác chéo giữa nhiều loại dữ liệu (modalities) khác nhau được ghi trong log hệ điều hành. Kết hợp thêm một lớp thích ứng phương thức (modality adaptation layer) để xử lý tính không đồng nhất của dữ liệu.
- **Điểm mạnh:** Giải quyết được hạn chế lớn của các phương pháp đơn phương thức (unimodal) là bỏ qua thông tin nền tảng, và các phương pháp đa phương thức trước đây không nắm bắt được sự tương tác chéo. Đạt độ chính xác trung bình (Precision) cực cao 99.63% trên 7 tập dữ liệu chuẩn. Hệ thống bao phủ được nhiều loại tấn công/bất thường khác nhau.
- **Điểm yếu:** Cơ chế chú ý đa đầu (multi-head attention) tính toán chéo qua lại giữa nhiều tập phương thức (modalities) sẽ gây tiêu hao bộ nhớ và yêu cầu tính toán lớn trong quá trình huấn luyện và suy luận thực tế.
- **Hướng phát triển:** Nghiên cứu kỹ thuật tinh gọn mô hình (model pruning) hoặc thưa thớt hóa ma trận chú ý (sparse attention) để tăng tốc độ phân tích trên các log hệ điều hành sinh ra liên tục.
- **Dataset:** 7 tập dữ liệu benchmark phổ biến cho phát hiện bất thường dựa trên log.

---

### 63. `s41598-026-40763-5_reference.pdf`

- **Chủ đề (Vấn đề giải quyết):** Xây dựng hệ thống phát hiện xâm nhập theo hành vi thời gian thực giải quyết cùng lúc 4 thách thức: bảo vệ quyền riêng tư, phân phối phi tập trung, mất cân bằng lớp dữ liệu, và khả năng giải thích (explainability).
- **Phương pháp (Đã làm gì):** Đề xuất framework FIDMF tích hợp hàng loạt công nghệ lõi: Học liên kết (Federated Learning) để bảo vệ quyền riêng tư; mạng Attention-LSTM để dò mẫu thời gian; Mạng đối nghịch sinh (GAN) kết hợp SMOTE để nhân bản và cân bằng các mẫu tấn công hiếm gặp. Đặc biệt, dùng LLMs mã nguồn mở để: (1) làm giàu đặc trưng ngữ cảnh, (2) hướng dẫn GAN sinh dữ liệu ngữ nghĩa, và (3) XAI (Trí tuệ nhân tạo có thể giải thích).
- **Điểm mạnh:** Một giải pháp "All-in-One" cực kỳ đồ sộ giải quyết hầu như mọi nhược điểm của IDS hiện đại. Điểm F1 cho các lớp tấn công thiểu số (minority attack class) đạt tới 99.70% trên tập NSL-KDD, chứng tỏ năng lực vượt trội trong việc phát hiện các cuộc tấn công tinh vi hiếm gặp nhờ sự trợ giúp của LLM và GAN.
- **Điểm yếu:** Kiến trúc quá phức tạp và nặng nề (nhúng cùng lúc FL, Attention-LSTM, GAN và LLM) khiến việc triển khai trong môi trường sản xuất thực tế trên các thiết bị Edge (có năng lực tính toán hạn chế) là gần như bất khả thi.
- **Hướng phát triển:** Trích xuất và phân tách thành các module vi dịch vụ (micro-services) hoặc nén mô hình (Knowledge Distillation) để phân bổ gánh nặng tính toán phù hợp trên môi trường đám mây và biên (Edge-Cloud computing).
- **Dataset:** NSL-KDD, CIC-IDS2017, và UNSW-NB15.

---

### 64. `s42400-024-00240-w.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện mối đe dọa trên máy chủ (Host threat detection), đặc biệt là các cuộc tấn công có chủ đích APT (Advanced Persistent Threat), giải quyết bài toán bùng nổ bộ nhớ và thời gian tính toán khi dùng đồ thị nguồn gốc (Provenance Graph).
- **Phương pháp (Đã làm gì):** Đề xuất phương pháp ProcSAGE. Thay vì dùng toàn bộ log hệ thống (system audit logs) đồ sộ để xây đồ thị, ProcSAGE chỉ tập trung trích xuất đặc trưng các hoạt động của tiến trình/luồng (processes/threads) và các node lân cận trong đồ thị.
- **Điểm mạnh:** Giải quyết triệt để nút thắt cổ chai về hiệu suất của các thuật toán đồ thị. Giảm 69% thời gian tính toán và 78% dung lượng bộ nhớ so với việc sử dụng toàn bộ log hệ thống, đồng thời vẫn giữ được độ chính xác tương đương. Không phụ thuộc vào luật (rule-based) nên có thể phát hiện tấn công zero-day.
- **Điểm yếu:** Bằng cách lược bỏ bớt các log hệ thống mức thấp để thu gọn đồ thị, mô hình có nguy cơ bỏ sót các dấu vết tấn công cực kỳ tinh vi nằm ngoài phạm vi hoạt động của tiến trình chính.
- **Hướng phát triển:** Nghiên cứu cơ chế "phóng to/thu nhỏ" (zoom-in/zoom-out) đồ thị động: bình thường chạy đồ thị rút gọn, khi có dấu hiệu nghi ngờ sẽ truy xuất đồ thị chi tiết.
- **Dataset:** Tập dữ liệu StreamSpot.

---

### 65. `s43681-024-00427-4.pdf`

- **Chủ đề (Vấn đề giải quyết):** Cung cấp một đánh giá toàn diện về sự năng động của AI Tấn công (Offensive AI) và AI Đối kháng (Adversarial AI) trong an ninh mạng từ góc độ phi kỹ thuật và chiến lược.
- **Phương pháp (Đã làm gì):** Thực hiện Tổng quan Tài liệu Hệ thống (Systematic Literature Review - SLR). Xây dựng một khung phân loại (taxonomy) rõ ràng phân biệt giữa AI Phòng thủ, AI Tấn công (dùng AI để tấn công hệ thống), và AI Đối kháng (tấn công trực tiếp vào mô hình AI). Phân tích động cơ của tội phạm mạng và tác động xã hội.
- **Điểm mạnh:** Cung cấp góc nhìn chiến lược, nhân văn và quản lý (holistic) rất cần thiết, thu hẹp khoảng cách giữa công nghệ và con người (technology-humanity chasm). Cung cấp khung AICD giúp các nhà lập chính sách và quản trị viên hiểu rõ mối đe dọa.
- **Điểm yếu:** Là một bài báo lý thuyết (Literature review), không đề xuất bất kỳ thuật toán phát hiện bất thường hay mô hình học máy kỹ thuật mới nào.
- **Hướng phát triển:** Chuyển hóa khung lý thuyết AICD thành các bộ quy tắc (policy/rules) cụ thể có thể tích hợp vào các hệ thống phát hiện xâm nhập hiện hành.
- **Dataset:** Không có (Bài báo Review).

---

### 66. `sensors-24-02636-v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Thiếu hụt tập dữ liệu log tường lửa (firewall logs) có chứa các cuộc tấn công thực tế để huấn luyện mô hình học máy.
- **Phương pháp (Đã làm gì):** Trình bày một phương pháp tổng hợp (Synthesis) khối lượng nhẹ để tự tạo ra (inject) các cuộc tấn công nhân tạo vào trong log tường lửa mạng điều khiển công nghiệp (ICS) mà không cần xây dựng testbed đắt tiền. Sau đó, so sánh các phương pháp học có giám sát và không giám sát trên tập log đã bị tiêm nhiễm này.
- **Điểm mạnh:** Cung cấp một phương pháp tiết kiệm chi phí để giải quyết vấn đề "đói dữ liệu" (data starvation) trong học máy. Kết quả chứng minh các bất thường nhân tạo "trộn" rất tự nhiên vào log thật (các mô hình không giám sát khó phát hiện được), nhưng mô hình có giám sát lại nhận diện rất tốt.
- **Điểm yếu:** Việc tấn công nhân tạo (artificially generated attacks) có thể không mô phỏng được hoàn hảo các chuỗi tấn công APT phức tạp trong thực tế, dẫn đến nguy cơ mô hình có giám sát bị "học vẹt" (overfitting) các đặc điểm tổng hợp thay vì dấu hiệu tấn công thật.
- **Hướng phát triển:** Kết hợp dữ liệu tấn công tổng hợp này với các kỹ thuật Học chuyển giao (Transfer Learning) để cải thiện hiệu suất nhận diện tấn công zero-day thực tế.
- **Dataset:** Log tường lửa từ một mạng điều khiển công nghiệp lớn (kèm dữ liệu tấn công được tổng hợp nhân tạo).

---

### 67. `sensors-24-07949.pdf`

- **Chủ đề (Vấn đề giải quyết):** Phát hiện bất thường trong các hệ thống phân tán phức tạp (như đám mây/microservices), nơi các sự kiện log tương tác không đồng bộ và có sự phụ thuộc sâu sắc cả về mặt thời gian lẫn logic nhân quả.
- **Phương pháp (Đã làm gì):** Đề xuất Mạng chú ý logic thời gian (Temporal Logical Attention Network - TLAN). Cơ chế này mô hình hóa rõ ràng cả "mẫu chuỗi thời gian" (temporal patterns) và "sự phụ thuộc logic" (logical dependencies) giữa các thành phần phân tán. Khung cũng sử dụng mô-đun trích xuất đặc trưng đa tỷ lệ (multi-scale) và chiến lược ngưỡng thích ứng (adaptive threshold) dựa trên tải của hệ thống.
- **Điểm mạnh:** Giải quyết triệt để điểm yếu của các mô hình học sâu truyền thống (như LSTM hay Transformer cơ bản) vốn chỉ coi log là chuỗi dữ liệu chuỗi thời gian đơn giản mà bỏ qua tính cấu trúc/logic hệ thống. Giảm tỷ lệ báo động giả (false alarms) 15.3% và cải thiện 9.4% F1-score so với các mô hình tốt nhất hiện tại.
- **Điểm yếu:** Đòi hỏi phải giám sát tải hệ thống liên tục để điều chỉnh ngưỡng thích ứng (adaptive threshold), điều này có thể tạo thêm gánh nặng cho hệ thống ở thời gian thực. Được đánh giá chủ yếu trên dữ liệu tổng hợp (synthetic).
- **Hướng phát triển:** Thử nghiệm mô hình trên các tập dữ liệu log phân tán trong môi trường sản xuất thực tế với độ nhiễu cao để kiểm chứng độ bền vững (robustness).
- **Dataset:** Tập dữ liệu tổng hợp quy mô lớn về log hệ thống phân tán (Large-scale synthetic distributed system log dataset).

---

### 68. `sensors-25-00190-v2.pdf`

- **Chủ đề (Vấn đề giải quyết):** Cung cấp một cái nhìn toàn cảnh, phân loại và hệ thống hóa các kỹ thuật học sâu (Deep Learning) mới nhất dùng để phát hiện bất thường trong Chuỗi thời gian đa biến (Multivariate Time Series - MTSAD).
- **Phương pháp (Đã làm gì):** Bài báo là một bài Tổng quan (Review/Survey). Các tác giả đã đề xuất một khung phân loại (taxonomy) phân chia các chiến lược phát hiện bất thường dựa trên mô hình học máy (Transformers, GNN, VAEs, GANs, Diffusion models) và kiến trúc mạng nơ-ron. Cũng tổng hợp các tập dữ liệu công khai và các thách thức đang bỏ ngỏ.
- **Điểm mạnh:** Cung cấp nền tảng kiến thức bài bản và hệ thống cho bất kỳ ai muốn nghiên cứu sâu về lĩnh vực MTSAD. So sánh rõ ràng ưu/nhược điểm của từng nhánh thuật toán học sâu, từ đó giúp tiết kiệm thời gian nghiên cứu nền tảng.
- **Điểm yếu:** Đây là một bài báo lý thuyết mang tính chất tổng hợp (survey paper), không đề xuất phương pháp hay kiến trúc mã nguồn kỹ thuật mới nào.
- **Hướng phát triển:** Dựa trên các thách thức mở được nêu (như thiếu dữ liệu gán nhãn thực tế hay chi phí huấn luyện cao), các nhà nghiên cứu có thể tập trung vào học chuyển giao (Transfer Learning) hoặc Few-shot learning cho MTSAD.
- **Dataset:** Tổng hợp từ nhiều tập dữ liệu công cộng khác nhau thuộc lĩnh vực MTSAD.

---

### 69. `zde27.pdf`

- **Chủ đề (Vấn đề giải quyết):** Giải quyết vấn đề "lựa chọn thuật toán" (algorithm selection problem) bằng cách đánh giá toàn diện sự hiệu quả, độ mạnh và năng lực tính toán của hàng chục thuật toán phát hiện bất thường chuỗi thời gian hiện có.
- **Phương pháp (Đã làm gì):** Thu thập, cài đặt lại và đánh giá một cách có hệ thống 71 thuật toán phát hiện bất thường tốt nhất (state-of-the-art) trên một quy mô khổng lồ gồm 976 tập dữ liệu chuỗi thời gian (cả đơn biến và đa biến).
- **Điểm mạnh:** Là một nghiên cứu chuẩn đối sánh (benchmark study) mang tính bước ngoặt, đồ sộ chưa từng có về quy mô. Cung cấp cái nhìn trung lập và thực nghiệm về ưu/nhược điểm thực sự của các thuật toán trong thực tế (hiệu quả, hiệu suất, tính mạnh mẽ), vượt ra khỏi những kết quả lý thuyết thường được báo cáo trong các bài báo đơn lẻ.
- **Điểm yếu:** Dù đánh giá quy mô lớn, báo cáo vẫn tập trung vào các mô hình trước khi kỷ nguyên của các Mô hình Ngôn ngữ Lớn (LLMs) áp dụng cho dữ liệu chuỗi thời gian trở nên bùng nổ, do đó có thể thiếu vắng một số mô hình GenAI mới nhất.
- **Hướng phát triển:** Tích hợp bộ quy chuẩn benchmark này vào một nền tảng mã nguồn mở (như thư viện Python) để tự động hóa việc đánh giá các mô hình chuỗi thời gian tương lai.
- **Dataset:** 976 tập dữ liệu chuỗi thời gian (time series datasets).

---
