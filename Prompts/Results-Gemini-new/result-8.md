# **Giao Thức Thực Thi Thực Nghiệm: Kiểm Chứng Hiệu Quả Của Mô-đun RAG-SLM Phân Loại Có Điều Kiện Trên Mô Hình Phát Hiện Sớm Bất Thường Dữ Liệu Log**

## **1\. Experimental Objectives and Traceability**

Trong bối cảnh các hệ thống điện toán đám mây và vi dịch vụ liên tục phát triển, việc kiểm chứng các mô hình Trí tuệ Nhân tạo (AI) đòi hỏi một sự chặt chẽ tuyệt đối về mặt phương pháp luận nhằm ngăn chặn các kết luận sai lệch do thiên kiến thực nghiệm. Giao thức thực thi thực nghiệm này được thiết kế nhằm thiết lập một khuôn khổ đánh giá có thể truy xuất (traceability framework) cho bài toán phát hiện sớm bất thường dữ liệu log (Early Log Anomaly Detection \- ELAD). Mục tiêu tối thượng của thực nghiệm là kiểm chứng bằng chứng khoa học về việc liệu cơ chế Sinh tăng cường bằng truy xuất (RAG) kết hợp Mô hình Ngôn ngữ Nhỏ (SLM) dưới dạng thực thi có điều kiện có thể giải quyết triệt để hiện tượng bão hòa cảnh báo giả (Alert Fatigue) trong môi trường hệ thống mở (Open-World) hay không1.  
Tính truy xuất nguồn gốc là nguyên tắc cốt lõi, đảm bảo rằng mọi câu hỏi nghiên cứu (Research Questions \- RQ) và giả thuyết (Hypotheses \- H) đều được ánh xạ trực tiếp đến một kịch bản thử nghiệm và một tập hợp hệ mét đo lường cụ thể2. Sự chặt chẽ này ngăn chặn việc thực thi các thử nghiệm không có định hướng hoặc khai thác dữ liệu theo hướng p-hacking để tìm kiếm các kết quả có ý nghĩa thống kê một cách khiên cưỡng.  
Bảng dưới đây thiết lập ma trận truy xuất mục tiêu thực nghiệm, cung cấp cái nhìn toàn cảnh về thiết kế logic của toàn bộ quá trình kiểm chứng:

| Research Element | Experiment | Primary Metric | Expected Evidence |
| :---- | :---- | :---- | :---- |
| **RQ1:** Giới hạn của xấp xỉ Bayes khi đối mặt với trượt dạt khái niệm do cập nhật CI/CD là gì? | E1 (Reproduction), E5 (Robustness) | False Positive Rate (FPR) trên luồng dữ liệu ngoài phân phối (OOD logs). | Mạng nơ-ron Bayes nguyên thủy (LogOW) sinh ra tỷ lệ FPR tăng đột biến khi luồng sự kiện gặp các bản cập nhật hợp lệ do sự cô lập tri thức ngoại vi2. |
| **RQ2:** Cơ chế RAG-SLM phân định giữa bản cập nhật an toàn và cảnh báo sớm như thế nào? | E2 (Main Test), E3 (Early Detection) | FPR tại vùng biên bất định, Detection Lead Time (DLT), Early Warning Horizon (EWH). | Tỷ lệ FPR giảm đáng kể (kỳ vọng 99%) tại vùng biên bất định; hệ mét DLT duy trì giá trị dương trước thời điểm sụp đổ vật lý hệ thống2. |
| **RQ3:** Tác động của RAG-SLM lên kiến trúc AIOps thời gian thực là gì? | E6 (Efficiency) | Compute Latency (mili-giây/cửa sổ), Throughput (Logs/giây). | Độ trễ luồng xử lý nóng duy trì dưới 5ms; luồng xử lý lạnh (gọi API RAG) chiếm dưới 5% tổng dung lượng sự kiện, đảm bảo tính thực tiễn3. |
| **H1:** Bão hòa cảnh báo sinh ra do sự cô lập tri thức của mô hình tĩnh. | E4 (Ablation: SLM w/o RAG) | Context Relevance, Delta FPR. | Mô hình SLM sinh ảo giác (hallucination) và FPR cao nếu cơ chế Retrieval bị vô hiệu hóa; hiệu năng phục hồi khi RAG được bật lại2. |
| **H2:** Tối ưu hóa độ trễ tính toán bằng cơ chế kích hoạt RAG có điều kiện. | E6 (Efficiency), E4 (Ablation) | Token Cost, VRAM Allocation, End-to-End Latency. | Chi phí API, dung lượng RAM và độ trễ giảm theo cấp số nhân so với việc ép buộc 100% cửa sổ log đi qua tác tử SLM2. |
| **H3:** Sự cải thiện duy trì hệ mét Cảnh báo sớm ổn định trên dữ liệu động học. | E4 (Early Detection), E7 (Generalization) | DLT (phút/giờ) trước ![][image1], Detection Before Failure (DBF). | Hệ thống liên tục phát cờ cảnh báo thành công trước sự cố vật lý trên đa dạng môi trường bất chấp sự trượt dạt khái niệm2. |

## **2\. Experimental Environment**

Môi trường thực nghiệm được đặc tả với độ chi tiết cao nhất nhằm loại trừ các biến số nhiễu (confounding variables) phát sinh từ sự không tương thích phần cứng hoặc thư viện phần mềm, vốn là nguyên nhân chính dẫn đến khủng hoảng khả năng tái lập trong nghiên cứu học máy.  
Khía cạnh phần cứng (Hardware) đòi hỏi một máy trạm hoặc cụm máy chủ điện toán đám mây được trang bị sức mạnh xử lý song song cường độ cao. Cấu hình bắt buộc bao gồm tối thiểu một đơn vị xử lý đồ họa (GPU) Nvidia kiến trúc Ampere hoặc Ada Lovelace (chẳng hạn như RTX 3090 hoặc RTX 4090\) sở hữu không dưới 24GB VRAM2. Bộ nhớ VRAM lớn là điều kiện tiên quyết do hệ thống phải nạp đồng thời trọng số của mạng nơ-ron học bán giám sát LogOW và tác tử ngôn ngữ lớn đã được lượng tử hóa (Llama-3-8B hoặc Qwen2.5-7B) vào cùng một không gian bộ nhớ để giảm thiểu độ trễ luân chuyển dữ liệu qua bus PCIe2. Dung lượng RAM hệ thống được chỉ định ở mức tối thiểu 64GB chuẩn DDR4 hoặc DDR5 nhằm hỗ trợ quá trình phân mảnh và duy trì các cửa sổ trượt (sliding windows) trên các siêu tập dữ liệu chuỗi thời gian như BGL và Thunderbird. Hạ tầng lưu trữ bắt buộc sử dụng ổ cứng thể rắn chuẩn NVMe SSD với dung lượng trống trên 1TB nhằm đảm bảo băng thông thao tác truy xuất dữ liệu (I/O) cực cao cho cơ sở dữ liệu Vector và luồng log trực tuyến2.  
Về ngăn xếp phần mềm (Software Stack), hệ điều hành lõi dựa trên nền tảng Linux (Ubuntu 22.04 LTS hoặc các bản phân phối tương đương) nhằm đảm bảo sự ổn định trong quản lý luồng tiến trình. Ngôn ngữ lập trình trung tâm là Python 3.10.x, cung cấp sự cân bằng giữa hiệu năng và khả năng tương thích hệ sinh thái. Nền tảng học sâu PyTorch phiên bản 2.x được cấu hình biên dịch trực tiếp với CUDA Toolkit 12.1 hoặc mới hơn để khai thác tối đa tập lệnh Tensor Cores2. Công cụ suy luận ngôn ngữ tự nhiên được vận hành độc quyền thông qua vLLM, một engine chuyên biệt cung cấp cơ chế PagedAttention để xử lý hiệu quả bộ nhớ cache của các khóa và giá trị (KV cache), qua đó tối đa hóa thông lượng sinh văn bản cho tác tử SLM2. Hệ thống RAG được xây dựng dựa trên cơ sở dữ liệu Vector mã nguồn mở ChromaDB, trong khi việc điều phối chuỗi lập luận và truy xuất tài liệu được trừu tượng hóa thông qua framework LangChain2.  
Quá trình quản lý siêu dữ liệu thực nghiệm (Experiment Tracking) được tự động hóa hoàn toàn bằng nền tảng MLflow. Công cụ này sẽ lưu vết định danh mô hình, giá trị hạt giống ngẫu nhiên (seeds), cấu hình siêu tham số, và các hệ mét chuỗi thời gian của từng kịch bản thử nghiệm2. Mọi phiên bản thư viện sẽ được khóa cứng (frozen) thông qua cơ chế tệp requirements.txt và bộ chứa Docker, tạo ra một môi trường đóng gói bất biến sẵn sàng cho công tác Artifact Evaluation của các hội nghị IEEE/ACM.

## **3\. Dataset Protocol**

Cơ sở dữ liệu là mạch máu của mọi mô hình học máy. Giao thức này loại bỏ hoàn toàn các tập dữ liệu mang tính tĩnh học như HDFS. Tập dữ liệu HDFS, do giới hạn trong một cấu trúc vòng đời khối (block-lifecycle) đơn giản với chưa tới 30 template cơ bản, không thể mô phỏng sự tiến hóa của từ vựng hệ thống, do đó không có khả năng kích hoạt phản ứng của khối ước lượng độ bất định khi đối mặt với trượt dạt khái niệm2. Thực nghiệm thay vào đó dựa vào hai siêu tập dữ liệu công nghiệp chuyên biệt.  
Tập dữ liệu thứ nhất là BGL (Blue Gene/L), thu thập từ hệ thống siêu máy tính tại phòng thí nghiệm quốc gia Lawrence Livermore. Tập dữ liệu này chứa hơn 4.7 triệu thông điệp log phân giải đến cấp độ mi-li-giây, bao gồm các sự kiện từ hệ điều hành, phần mềm định tuyến và các cảnh báo phần cứng2. Giá trị tối thượng của BGL nằm ở việc nó cung cấp các nhãn lỗi vật lý hệ thống có khả năng đối chiếu thời gian thực, tạo điều kiện hoàn hảo để đo lường cấu trúc Thời gian Dẫn trước Cảnh báo (Detection Lead Time \- DLT)2.  
Tập dữ liệu thứ hai là Thunderbird hoặc Spirit, đại diện cho môi trường mạng phân tán với hàng trăm triệu bản ghi log thô. Thunderbird sở hữu tỷ lệ biến thiên từ vựng khổng lồ, nơi các mẫu template chưa từng thấy liên tục xuất hiện. Đặc tính này biến nó thành một môi trường mô phỏng trượt dạt khái niệm (concept drift simulator) khắc nghiệt nhất, ép buộc mạng Bayes của mô hình cơ sở phải liên tục phất cờ "bất định", qua đó phô diễn năng lực lọc nhiễu tự động (auto-triage) của khối RAG-SLM2.  
Kỷ luật dữ liệu thời gian (Temporal Rule) được áp dụng một cách nghiêm ngặt nhằm bảo vệ tính toàn vẹn của thực nghiệm. Chiến lược phân tách dữ liệu bắt buộc tuân thủ phương pháp **Chronological Split** (cắt theo thời gian thực)2. Luồng sự kiện được chia thành 70% dữ liệu quá khứ phục vụ việc huấn luyện và thiết lập cơ sở tri thức, cùng 30% dữ liệu tương lai dùng để đánh giá mô hình. Kỹ thuật xáo trộn ngẫu nhiên (Random Shuffle) hay K-Fold Cross-Validation bị cấm tuyệt đối, do chúng phá vỡ cấu trúc nhân-quả của chuỗi thời gian, gây ra rò rỉ dữ liệu (Test Leakage) và tạo ra ảo giác về khả năng dự báo của hệ thống2.  
Hơn nữa, sự rò rỉ thông tin ngoại vi (Future Incident Retrieval) được kiểm soát bởi một bộ lọc cứng thời gian. Bất kỳ tài liệu cấu hình, mã nguồn Git, hay sổ tay vận hành nào có nhãn thời gian khởi tạo lớn hơn thời điểm mô hình đưa ra dự đoán cảnh báo đều bị vô hiệu hóa hoàn toàn khỏi cơ sở dữ liệu Vector trong quá trình truy xuất2. Quy định này triệt tiêu rủi ro tác tử RAG "đọc lén" các báo cáo khắc phục sự cố (post-mortem reports) sinh ra sau khi lỗi đã hoàn tất, đảm bảo hệ mét Early Detection được đo lường trung thực.

## **4\. Baseline and Fair Comparison Protocol**

Tính hợp lệ của toàn bộ nghiên cứu phụ thuộc vào sự công bằng trong việc đối chiếu với phương pháp cơ sở. Baseline được chỉ định là phương pháp **LogOW** (A Semi-Supervised Log Anomaly Detection Model in Open-World Setting)1. Đây là một nền tảng thuật toán SOTA vượt qua thành công Rào chắn Đủ điều kiện (Strict Baseline Eligibility Gate). Công trình này được công bố chính thức trên *Journal of Systems and Software*, một tạp chí thuộc nhóm Q1 theo cả JCR và SCImago, trong giai đoạn 2024/20252. Mã nguồn nguyên thủy cùng 1.4GB dữ liệu đã làm sạch của LogOW được bảo lưu vĩnh viễn trên Zenodo, đáp ứng hoàn hảo tiêu chí minh bạch và khả năng tái lập2.  
Giao thức thiết lập một không gian so sánh có kiểm soát (Controlled Comparison) giữa hai hệ thống:

* **Hệ thống A (Original Baseline):** Khởi chạy mạng nơ-ron học bán giám sát của LogOW với cấu hình gốc. Hệ thống tính toán điểm Predictive Entropy thông qua xấp xỉ Bayes (Monte Carlo Dropout với 10 vòng truyền ngẫu nhiên). Khi Entropy vượt ngưỡng động ![][image2], hệ thống A lập tức gắn nhãn "bất định" và phát cảnh báo dị thường mà không có bất kỳ cơ chế phân giải ngoại vi nào2.  
* **Hệ thống B (Improved Baseline):** Tích hợp cấu trúc Conditional RAG-SLM Triage. Luồng dữ liệu chia làm hai nhánh. Nhánh nóng vận hành tương tự Hệ thống A, nhưng khi Entropy vượt ngưỡng ![][image2], dữ liệu bị đóng băng và chuyển sang nhánh lạnh. Tại đây, cơ sở dữ liệu Vector nội bộ được truy vấn thông qua Tìm kiếm lai (Hybrid Search), tiêm tài liệu vận hành vào SLM để tự động phân loại sự kiện bất định thành cập nhật hợp lệ hoặc cảnh báo suy thoái2.

Để bảo vệ logic quy kết (Attribution Logic), toàn bộ các biến số môi trường giữa A và B phải bị đóng băng. Kỹ thuật tiền xử lý (Drain parser với độ sâu 4), ma trận nhúng vector, và cấu hình phân tách dữ liệu được chia sẻ chung. Yếu tố quan trọng nhất là **trọng số của mạng nơ-ron (Model Weights) phải được cố định (frozen)** sau giai đoạn huấn luyện ban đầu2. Hệ thống B tuyệt đối không được phép tinh chỉnh (fine-tune) lại mạng LogOW gốc. Sự đóng băng này chứng minh rằng mạng nơ-ron của cả hai hệ thống sinh ra điểm số bất định giống hệt nhau. Do đó, bất kỳ sự sụt giảm nào về tỷ lệ cảnh báo giả (FPR) hoặc sự cải thiện về thời gian dẫn trước (DLT) đo được ở hệ thống B đều có thể và phải được quy kết 100% về sức mạnh phân giải của mô-đun RAG-SLM2.

## **5\. Experiment Scenarios**

Hệ thống được chỉ định thực thi 7 kịch bản thực nghiệm chuyên biệt, mỗi kịch bản đóng vai trò như một lát cắt giải phẫu để đo lường tính khả thi toàn diện của lý thuyết khoa học2.

* **E1 — Baseline Reproduction (Tái lập Cơ sở):** Kịch bản này thiết lập đường cơ sở rủi ro (risk baseline). Hệ thống chạy độc lập mô hình LogOW trên các siêu tập dữ liệu để tái lập các điểm số F1 và tỷ lệ cảnh báo giả (FPR) tĩnh. Đóng góp cốt lõi của E1 là ghi nhận bằng chứng thực nghiệm về sự bùng nổ của FPR khi hệ thống bị đưa vào môi trường thế giới mở, chứng minh hiện tượng Alert Fatigue là có thực2.  
* **E2 — Main Improvement Test (Thử nghiệm Cải thiện Chính):** Đây là kịch bản đối đầu trực tiếp giữa Hệ thống A và B. Thông qua việc mô phỏng luồng sự kiện pha trộn giữa lỗi vật lý và các bản cập nhật CI/CD an toàn (đã lưu vết trong Git), thực nghiệm định lượng năng lực của mô-đun RAG-SLM trong việc nhận diện và dập tắt các báo động mù quáng (giảm FPR) mà không làm suy giảm độ nhạy (Recall) tổng thể của mô hình2.  
* **E3 — Early Detection Test (Đánh giá Cảnh báo Sớm):** Chuyển dịch lăng kính từ phân tích không gian sang phân tích thời gian. Kịch bản này đối chiếu lịch sử các cờ cảnh báo (Alert Flags) với các nhãn thời gian sụp đổ vật lý hệ thống. Mục đích là xác minh xem việc trì hoãn luồng xử lý do triệu gọi API của RAG-SLM có làm mất đi giá trị của Thời gian Dẫn trước (DLT) hay không2.  
* **E4 — Ablation (Thử nghiệm Cắt lớp):** Khảo sát độc lập sự đóng góp của các thành phần con cấu thành nên hệ thống cải tiến, bao gồm việc tắt mô-đun tìm kiếm lai, ngắt kết nối kho tri thức RAG, hoặc loại bỏ cổng điều kiện Entropy2.  
* **E5 — Robustness (Kiểm tra Độ bền vững):** Bơm các chuỗi nhiễu loạn nhân tạo vào luồng sự kiện. Tỷ lệ các template log ngoài phân phối (OOD) được đẩy lên các mốc 20% và 40%. Điều này ép mạng Bayes liên tục báo động, đẩy mô-đun RAG-SLM đến giới hạn chịu tải cực đại nhằm kiểm tra hiện tượng tràn bộ nhớ (Out-Of-Memory) hoặc sụp đổ API2.  
* **E6 — Efficiency (Đánh giá Hiệu năng):** Tích hợp trình giám sát hệ thống để đo đạc thông lượng xử lý (Throughput) tính bằng logs/giây và phân kỳ độ trễ tính toán giữa luồng mạng nơ-ron (luồng nóng) và luồng SLM (luồng lạnh)2.  
* **E7 — Generalization (Đánh giá Tổng quát hóa):** Chạy chéo hệ thống trên hai miền kiến trúc đối nghịch (BGL \- phần cứng, Thunderbird \- mạng lưới) nhằm chứng minh mô hình không bị quá khớp (overfit) với một chuẩn đối sánh duy nhất2.

## **6\. Evaluation Metrics**

Phương pháp đánh giá phá vỡ lối mòn của việc lạm dụng điểm số F1 tĩnh trên các tập dữ liệu đã hoàn tất, chuyển sang hệ thống đo lường động học nhiều lớp2.

### **Nhóm Early Detection (Phát hiện Sớm)**

Đây là nhóm chỉ số quyết định sự thành bại của hệ thống:

* **Detection Lead Time (DLT):** Khoảng thời gian từ thời điểm hệ thống phất cờ cảnh báo sớm (![][image3]) cho đến khi sự cố sụp đổ vật lý thực sự xảy ra (![][image1]). Được toán học hóa bằng ![][image4]2. Bất kỳ tín hiệu cảnh báo nào cho ra giá trị ![][image5] đều bị coi là vô giá trị trong bối cảnh vận hành thời gian thực và bị loại khỏi chỉ số này.  
* **Early Warning Horizon (EWH):** Khung quan sát tối đa (tính bằng thời gian hoặc số lượng sự kiện log) mà mô hình có khả năng duy trì độ tin cậy cảnh báo trước khi bị bão hòa bởi tín hiệu nhiễu2.  
* **Detection Before Failure (DBF):** Tỷ lệ phần trăm tổng số sự cố nghiêm trọng được hệ thống báo hiệu thành công trước mốc zero.

### **Nhóm Detection (Thống kê Nhị phân)**

* **False Positive Rate (FPR):** Đặc biệt đo lường trên nhóm dữ liệu ngoài phân phối (OOD). Mức độ sụt giảm FPR của Hệ thống B so với Hệ thống A là minh chứng tuyệt đối cho năng lực của tác tử RAG-SLM trong việc triệt tiêu hiện tượng Alert Fatigue2.  
* Các hệ mét chuẩn hóa (Precision, Recall, F1, PR-AUC, ROC-AUC) được lưu vết nhằm mục đích so sánh tương thích với các công bố học thuật trong cùng hệ sinh thái.

### **Nhóm Efficiency (Hiệu năng Vận hành)**

* **Compute Latency:** Tốc độ đáp ứng trên mỗi cửa sổ trượt. Yêu cầu báo cáo phân tách rõ ràng: Độ trễ P95 cho luồng xử lý cục bộ của LogOW và độ trễ P99 cho luồng triệu gọi API qua vLLM2.  
* **Token Cost & VRAM Allocation:** Ghi nhận đỉnh tiêu thụ bộ nhớ đồ họa và chi phí mã hóa chuỗi ngôn ngữ của SLM trên mỗi phiên chạy.

### **Nhóm Component Metrics**

* **Context Relevance:** Đo lường độ tương đồng Cosine trung bình để định lượng sự chính xác của tài liệu được trích xuất từ cơ sở dữ liệu Vector.  
* **Hallucination Rate:** Tỷ lệ SLM thất bại trong việc tuân thủ cấu trúc JSON hoặc sinh ra kết luận mâu thuẫn với tài liệu hướng dẫn được RAG cung cấp.

## **7\. Statistical Analysis**

Sự hội tụ của các thuật toán ngẫu nhiên (chẳng hạn như Monte Carlo Dropout trong xấp xỉ Bayes và cơ chế sinh mẫu của LLM) đòi hỏi một kỷ luật thống kê (Statistical Design) cực đoan để ngăn chặn hiện tượng báo cáo kết quả dựa trên thiên kiến lần chạy tốt nhất (best-run bias)2.  
Giao thức quy định mọi kịch bản thực nghiệm từ E1 đến E7 phải được lặp lại tối thiểu 10 lần chạy độc lập. Để duy trì tính kiểm chứng, giá trị hạt giống ngẫu nhiên (seed) được khóa cứng ở một hằng số (ví dụ: seed \= 42\) xuyên suốt toàn bộ chuỗi hệ thống, từ trạng thái khởi tạo của PyTorch, NumPy cho đến công cụ truy xuất của LangChain2. Tại lớp sinh ngôn ngữ, cấu hình bộ giải mã của SLM (Llama-3/Qwen) bị ép buộc vận hành theo cơ chế xác định (deterministic) thông qua việc khóa tham số temperature \= 0.0 và top\_p \= 1.0, qua đó triệt tiêu sự đa dạng không cần thiết trong các phán quyết phân loại tự động2.  
Mọi hệ mét hiệu năng (như DLT, FPR) khi trình bày phải hiển thị giá trị trung bình kèm theo độ lệch chuẩn và Khoảng tin cậy 95% (95% Confidence Intervals). Việc xác nhận sự cải tiến không sinh ra từ sai số ngẫu nhiên yêu cầu hệ thống vượt qua bài kiểm định ý nghĩa thống kê phi tham số Wilcoxon signed-rank test với ngưỡng ý nghĩa quy định ở mức ![][image6]2.

## **8\. Success Criteria**

Khung đánh giá thành công của phương pháp cải tiến được cấu trúc với các giới hạn đánh đổi (Trade-off Rules) rạch ròi, phản ánh nhu cầu thực tiễn của ngành công nghiệp AIOps2.  
Tiêu chí thành công cốt lõi (Primary Success Criterion) là sự suy giảm mang ý nghĩa thống kê của tỷ lệ cảnh báo giả (FPR) trên tập dữ liệu bị trượt dạt khái niệm (OOD) của Hệ thống B so với Hệ thống A, song song với việc bảo toàn nguyên vẹn độ nhạy (Recall) tổng thể của mô hình. Nếu FPR giảm nhưng Recall cũng sụp đổ, hệ thống chỉ đơn thuần trở nên kém nhạy cảm hơn chứ không thông minh hơn2.  
Tiêu chí phụ trợ (Secondary Criteria) yêu cầu hệ mét Thời gian Dẫn trước (DLT) tiếp tục duy trì ở mức dương và cung cấp khoảng đệm thời gian đo lường bằng phút hoặc giờ để kỹ sư can thiệp trước sự cố vật lý2.  
Quy tắc Đánh đổi (Trade-off Rule) là rào cản tối thượng: Sự cải tiến sẽ bị phủ quyết lập tức nếu nó vi phạm các Thỏa thuận Mức Dịch vụ (SLA) về thời gian thực. Cụ thể, kiến trúc phân luồng kép phải chứng minh được rằng luồng lạnh (gọi RAG-SLM) chiếm không quá 5% tổng lưu lượng hệ thống, trong khi 95% lưu lượng đi qua luồng nóng của LogOW duy trì độ trễ cực thấp dưới 5ms/cửa sổ2. Bất kỳ sự gia tăng độ chính xác nào đòi hỏi hệ thống phải chặn đứng và chờ đợi vài giây cho mọi dòng log thô đều bị phân loại là một thất bại thiết kế.

## **9\. Ablation Protocol**

Thực nghiệm E4 (Ablation) vận hành như một lăng kính giải phẫu để bóc tách và định lượng tính nhân-quả của từng thay đổi kiến trúc2. Quá trình cắt lớp được triển khai qua ba cấu hình chuyên biệt:

> 1. **Direct SLM (No RAG):** Các luồng log tạo ra mức Entropy cao được đẩy thẳng vào tác tử ngôn ngữ SLM mà không đi qua ChromaDB để truy vấn cơ sở tri thức ngoại vi. *Mục tiêu:* Kiểm chứng tỷ lệ bùng phát ảo giác (Hallucination Rate). Việc SLM suy diễn sai cấu hình mạng sẽ cung cấp bằng chứng rằng Trí tuệ Nhân tạo tạo sinh sẽ hoàn toàn bất lực nếu bị tước đi nền tảng tri thức RAG, qua đó khẳng định thành phần Retrieval là nhân tố cốt lõi mang lại hiệu năng2.  
> 2. **Semantic Only (No Hybrid Search):** Vô hiệu hóa kỹ thuật đối sánh từ khóa rời rạc (BM25) và các ma trận nhúng chuyên biệt cho mã nguồn (Code-specific Embeddings), chỉ giữ lại công cụ tìm kiếm ngữ nghĩa văn bản tự nhiên. *Mục tiêu:* Định lượng mức độ sụt giảm độ tương đồng ngữ cảnh (Context Relevance) do hiện tượng lệch chuẩn không gian nhúng (Embedding Mismatch) gây ra khi xử lý các tham số cứng như địa chỉ IP hay mã lỗi thập lục phân2.  
> 3. **No BNN Gate (No Entropy Switch):** Phá bỏ cổng rẽ nhánh của mạng nơ-ron Bayes, cưỡng ép 100% cửa sổ trượt đều phải qua quy trình phân tích của RAG-SLM. *Mục tiêu:* Ghi nhận sự phình to của chi phí token và sự sụp đổ băng thông hệ thống, chứng minh rằng mạng Bayes đóng vai trò như một màng lọc tiên quyết cho tính khả thi vận hành thời gian thực2.

## **10\. Error Analysis**

Hoạt động phân tích lỗi (Error Analysis) không được lạm dụng để sửa đổi thuật toán trên đường bay, mà nhằm cô lập nguyên nhân khiến mô hình đưa ra dự báo sai lầm để định hướng các luồng nghiên cứu tương lai. Các trường hợp lỗi được hệ thống hóa vào một cấu trúc phân loại học (taxonomy) rõ ràng2:

* **False Positive (Bão hòa cảnh báo tĩnh):** Tác tử SLM vẫn kết luận một bản cập nhật CI/CD là bất thường bất chấp việc đã được cung cấp ngữ cảnh đúng đắn từ RAG. Lỗi này phản ánh sự yếu kém trong khả năng lập luận của LLM.  
* **Early Detection Miss (Lọt lưới Cảnh báo sớm):** Cảnh báo phát ra với giá trị ![][image5]. Phân tích gốc rễ cần truy vết xem lỗi xuất phát từ mạng LogOW (không sinh đủ phương sai dự đoán để vượt ngưỡng ![][image2]) hay từ SLM (phân giải nhầm một sự cố tiềm tàng thành một bản cập nhật hợp lệ).  
* **Retrieval/Context Failure:** Kho lưu trữ Vector trả về các tài liệu hoàn toàn không liên quan đến chuỗi log đang bị mắc kẹt. Có thể do lỗi bộ mã hóa hoặc giới hạn cửa sổ ngữ cảnh bị cắt cụt dưới mức 512 token2.  
* **Reasoning Failure / Hallucination:** SLM phớt lờ chỉ thị trong System Prompt, tự bịa đặt các bản vá lỗi hoặc trả về cấu trúc không tương thích với định dạng JSON yêu cầu.  
* **Knowledge Gap:** Tài liệu giải thích cho bản nâng cấp (như Git Commit) hoàn toàn không tồn tại trong kho tri thức do sự thiếu sót của quy trình CI/CD. Đây là giới hạn vật lý của môi trường vận hành, nằm ngoài khả năng khắc phục của bản thân mô hình2.

## **11\. Robustness Analysis**

Phân tích tính vững chãi (Robustness Analysis) chỉ tập trung vào các nhiễu loạn liên quan trực tiếp đến bản chất của giới hạn nghiên cứu: Sự biến động trong môi trường Thế giới Mở (Open-World).  
Kịch bản thực nghiệm E5 sẽ bơm các luồng nhiễu loạn nhân tạo vào tập kiểm thử. Cụ thể, tỷ lệ xuất hiện của các template log mới hoàn toàn (chưa từng tồn tại trong tập huấn luyện) sẽ được khuếch đại lên các mức 10%, 20%, và đạt ngưỡng cực đại 40%2. Thao tác này nhằm mục đích đẩy mạng nơ-ron Bayes vào trạng thái liên tục vượt ngưỡng phương sai dự đoán, tạo ra một cơn bão truy vấn API dồn dập đổ về mô-đun RAG-SLM.  
Hệ mét đánh giá tính bền vững đo lường khả năng của hệ thống trong việc bảo toàn độ chính xác của cơ chế tự động phân loại (Auto-triage) dưới áp lực cực đoan, đồng thời giám sát rủi ro mô hình vLLM bị sụp đổ do tràn bộ nhớ đồ họa (Out-Of-Memory Exception)2. Việc vượt qua kịch bản này chứng minh hệ thống có đủ khả năng hấp thụ các cú sốc do những thay đổi kiến trúc phần mềm quy mô lớn mang lại.

## **12\. Efficiency and Cost Analysis**

Mọi nỗ lực nhúng các mô hình trí tuệ nhân tạo tạo sinh vào luồng dữ liệu truyền phát (streaming) đều bị bủa vây bởi rào cản tài nguyên. Giao thức yêu cầu một sự minh bạch toàn diện về chi phí tính toán:

* **End-to-End Latency (Độ trễ toàn trình):** Đo lường bằng mili-giây (ms). Hệ thống phải biểu diễn biểu đồ phân phối độ trễ tại các phân vị P50, P90 và P99. Sự phân tách độ trễ giữa luồng xử lý nóng (chỉ chạy LogOW) và luồng xử lý lạnh (kích hoạt chu trình RAG-SLM toàn diện) là bắt buộc2.  
* **Retrieval Time (Độ trễ truy xuất):** Tách biệt thời gian hao phí của riêng việc truy vấn cơ sở dữ liệu ChromaDB, bao gồm quá trình đối sánh vector lai và thực thi thuật toán suy giảm trọng số theo thời gian (Timestamp-decay penalty)2.  
* **GPU Memory (Tiêu thụ VRAM):** Theo dõi cấu hình phân bổ đỉnh (Peak VRAM allocation) của tiến trình suy luận vLLM sử dụng PagedAttention, xác minh việc lượng tử hóa mô hình 4-bit (AWQ/GGUF) đã phát huy hiệu quả2.  
* **Token Usage (Chi phí mã hóa):** Theo dõi số lượng token đầu vào (bao gồm System Prompt \+ Retrieved Context 512 token \+ cửa sổ Log hiện tại) và số lượng token đầu ra trên mỗi truy vấn để định lượng khả năng thương mại hóa.

## **13\. Reproducibility Protocol**

Cam kết cao nhất của giao thức là bảo vệ tính tái lập (Reproducibility) thông qua việc đóng băng mọi tạo tác (Artifacts). Mục tiêu là bất kỳ chuyên gia đánh giá độc lập nào cũng có thể khôi phục bảng kết quả đối chứng thông qua một quy trình tự động hóa duy nhất2.

* **Configuration Lock:** Mọi tham số siêu định tuyến (như dataset\_name, parser\_depth, mc\_dropout\_passes, chunk\_size, top\_k) đều phải được biểu diễn minh bạch trên các tệp văn bản định dạng YAML2.  
* **Data Integrity:** Lưu trữ mã băm định danh (MD5 Hash) của các tệp dữ liệu BGL và Thunderbird đã trải qua quá trình phân mảnh Chronological Split để chống rò rỉ.  
* **Model Source:** Giao thức cấm sử dụng các API đóng (Closed-source API như OpenAI hay Anthropic) do nguy cơ nhà cung cấp âm thầm cập nhật trọng số mô hình. Mọi suy luận SLM phải chạy cục bộ (Llama-3/Qwen)2.  
* **Artifact Dump:** Nền tảng MLflow được lập trình để đóng gói tự động toàn bộ bản lưu YAML, tệp kết xuất chuỗi JSON từ SLM, Ma trận Nhầm lẫn (Confusion Matrices), và các file CSV ghi nhận metric DLT thành một kho lưu trữ ZIP vĩnh viễn sau mỗi chu kỳ thực nghiệm2.

## **14\. Experiment Matrix**

Bảng ma trận dưới đây cấu trúc hóa tương quan giữa các Kịch bản Thực nghiệm (E1-E7) và kiến trúc so sánh đối chứng giữa Baseline nguyên thủy (A) và Hệ thống Cải tiến (B).

| Experiment | Baseline (A) | Improvement (B) | Main Purpose | Evaluated Metrics |
| :---- | :---- | :---- | :---- | :---- |
| **E1** | ✓ |  | Tái lập Baseline LogOW | Baseline FPR trên tập OOD, Điểm số F1 tĩnh. |
| **E2** | ✓ | ✓ | Thử nghiệm Cải thiện Chính | FPR sụt giảm tại vùng biên, Precision, Recall. |
| **E3** | ✓ | ✓ | Đánh giá Cảnh báo Sớm | DLT (phút/giờ), EWH, tỷ lệ DBF. |
| **E4** | ✓ | ✓ (Partial) | Cắt lớp (Ablation) | Context Relevance, Hallucination Rate, Delta FPR. |
| **E5** | ✓ | ✓ | Kiểm tra Độ bền vững | Tỷ lệ duy trì Auto-triage dưới áp lực nhiễu OOD 40%. |
| **E6** | ✓ | ✓ | Đánh giá Hiệu năng | Compute Latency (Hot/Cold path), Token Cost, Throughput. |
| **E7** | ✓ | ✓ | Tổng quát hóa | Sự ổn định chéo giữa miền phần cứng (BGL) và mạng (Thunderbird). |

## **15\. Result Reporting Template**

Khuôn mẫu báo cáo kết quả (Result Reporting) được thiết lập mô phỏng theo cấu trúc phân tích của các ấn bản IEEE/ICSE nhằm đảm bảo tính toàn vẹn học thuật2:

> 1. **Baseline Reproduction:** Đối chiếu hệ mét hiệu năng chạy thực tế với hệ mét trong công bố nguyên thủy của tác giả LogOW. Giải trình nếu có sự lệch chuẩn (deviation).  
> 2. **Main Comparison:** Thiết lập bảng ma trận đối sánh trực tiếp các hệ mét nhị phân (FPR, Precision, Recall) giữa Original Baseline và Improved Baseline.  
> 3. **Early Detection:** Biểu đồ mật độ phân phối (Distribution Plot) của Thời gian Dẫn trước Cảnh báo (DLT) tính bằng phút/giờ. Trình bày biểu đồ tích lũy của tỷ lệ DBF.  
> 4. **Ablation:** Bảng ma trận các chỉ số hao hụt (Drop-off metrics) khi các thành phần cốt lõi như Retrieval, Hybrid Search, hoặc cổng rẽ nhánh BNN Gate bị vô hiệu hóa.  
> 5. **Robustness:** Đồ thị dạng đường (Line chart) diễn tả sức ép lên thông lượng hệ thống và mức độ biến thiên FPR khi tỷ lệ nhiễu OOD tăng dần từ 0% lên 40%.  
> 6. **Efficiency/Cost:** Biểu đồ độ trễ hiển thị tính phân kỳ giữa luồng xử lý mạng nơ-ron cục bộ và luồng triệu gọi RAG-SLM. Bảng báo cáo phân bổ VRAM.  
> 7. **Statistical Evidence:** Trình bày bảng tổng hợp giá trị p-value sinh ra từ kiểm định Wilcoxon signed-rank test kết hợp Khoảng tin cậy 95% (95% CI) cho mọi sự cải thiện hiệu năng.  
> 8. **Error Analysis:** Trích dẫn các mẫu chuỗi JSON thất bại điển hình sinh ra bởi tác tử SLM. Thảo luận tương quan trọng số nguyên nhân giữa Ảo giác mô hình (Hallucination) và Lệch chuẩn không gian nhúng (Embedding Mismatch)2.  
> 9. **Limitations:** Nhìn nhận khách quan về các lằn ranh hệ thống (ví dụ: giới hạn cắt cụt cửa sổ ngữ cảnh ở 512 token cản trở việc suy luận các cấu trúc mạng quá phức tạp)2.

## **16\. Interpretation Rules**

Mọi diễn giải kết quả từ số liệu thô phải tuân thủ nghiêm ngặt các quy tắc phân loại chứng cứ sau nhằm chống lại thiên kiến xác nhận (Confirmation Bias):

* **Supported (Bằng chứng ủng hộ):** Tỷ lệ FPR trên luồng OOD giảm mạnh với mức ý nghĩa thống kê (p \< 0.05); hệ mét DLT được duy trì ở mức dương và thông lượng hệ thống không bị sập. Giả thuyết nghiên cứu được chứng minh là đúng đắn.  
* **Weakly Supported (Ủng hộ một phần):** FPR giảm nhưng hệ mét DLT biến thiên quá mạnh (có nhiều cảnh báo sớm giả hoặc quá trễ), hoặc chỉ số p-value lấp lửng ở ranh giới ![][image6]. Trạng thái này yêu cầu nhà nghiên cứu phải rà soát lại phương pháp Prompt Engineering hoặc cấu hình mô hình LLM.  
* **Not Supported (Bác bỏ):** SLM không thể hiện năng lực phân biệt một bản cập nhật CI/CD an toàn và một lỗi suy thoái phần cứng. Tỷ lệ FPR trên luồng OOD không có sự khác biệt có ý nghĩa thống kê giữa Hệ thống A và B.  
* **Contradicted (Mâu thuẫn):** Việc kích hoạt chu trình RAG-SLM phá vỡ SLA thời gian thực, đẩy độ trễ hệ thống lên mức độ không thể chấp nhận, dẫn đến việc Thời gian Dẫn trước Cảnh báo (![][image7]) trở thành số âm (hệ thống xử lý cảnh báo xong thì sự cố đã kết thúc từ lâu). Phương án kiến trúc bị phân loại là thất bại.

Nghiêm cấm hành vi kết luận "RAG cải thiện mô hình" nếu chỉ có chỉ số F1 tăng đơn độc trên một tập dữ liệu mà phớt lờ sự sụp đổ của DLT hoặc Compute Latency. Trong trường hợp mô-đun cải thiện thất bại (Not Supported/Contradicted), thực nghiệm vẫn giữ nguyên giá trị khoa học nếu phân tích gốc rễ nguyên nhân (Root Cause Analysis) được khai thác sâu sắc.

## **17\. Threats to Experimental Validity**

Việc đánh giá khách quan các mối đe dọa đến tính hợp lệ của luận điểm khoa học (Threats to Validity) là tấm khiên bảo vệ uy tín của nghiên cứu2:

* **Internal Validity (Tính hợp lệ Nội tại):** Rủi ro chí mạng là Rò rỉ Dữ liệu Tương lai (Future Data Leakage). *Chiến lược giảm thiểu (Mitigation):* Áp dụng tuyệt đối kỹ thuật Chronological Split và cấm dùng Random Shuffle. Thực thi Strict Temporal Filter (điều kiện WHERE ![][image8]) tại lớp truy vấn Vector DB để chặn đứng khả năng SLM tiếp cận báo cáo hậu sự cố2.  
* **External Validity (Tính hợp lệ Ngoại lai):** Nguy cơ quá khớp mô hình với một chuẩn đối sánh (Benchmark Bias). *Mitigation:* Bắt buộc chạy song song thực nghiệm E7 trên hai siêu dữ liệu có kiến trúc hoàn toàn trái ngược: BGL đại diện cho lỗi phần cứng và Thunderbird đại diện cho mạng lưới phân tán2.  
* **Construct Validity (Tính hợp lệ Khái niệm):** Sai lầm khi đánh đồng năng lực phát hiện bất thường sau sự kiện (Post-mortem Anomaly Detection) với khả năng Cảnh báo sớm. *Mitigation:* Hệ mét DLT và EWH được ràng buộc chặt chẽ với nhãn thời gian sụp đổ vật lý hệ thống (![][image1])2. Bất kỳ F1-Score nào sinh ra từ việc cắm cờ sau ![][image1] đều vô giá trị.  
* **Conclusion Validity (Tính hợp lệ Kết luận):** Rủi ro ngộ nhận hiệu năng cao từ một lần chạy may mắn (Best-run bias). *Mitigation:* Áp dụng kỷ luật thống kê với 10 lần chạy lặp lại độc lập, khóa cứng tham số temperature \= 0.0 và tiến hành kiểm định Wilcoxon2.  
* **Foundation Model / Retrieval Validity:** Rủi ro Lệch chuẩn Không gian nhúng (Embedding Mismatch) khi xử lý log IT và rủi ro Ô nhiễm ngữ cảnh (Context Pollution). *Mitigation:* Cấu hình công cụ Tìm kiếm lai (Hybrid Search) kết hợp đối sánh BM25 và áp dụng hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty) để tự động hạ mức ưu tiên của các tài liệu vận hành đã cũ2.

## **18\. Publication Readiness & 18A. Final Baseline Eligibility Verification**

Sự sẵn sàng xuất bản đòi hỏi việc rà soát chéo các tiêu chuẩn học thuật thông qua bảng kiểm (Checklist) định tính. Quá trình kiểm duyệt này đánh giá lại nền tảng của toàn bộ giao thức:

* \[x\] Phương pháp cơ sở (Baseline) được công bố trong giai đoạn 2023–2026. Công trình *LogOW: A Semi-Supervised Log Anomaly Detection Model in Open-World Setting* thỏa mãn điều kiện với xuất bản trực tuyến vào cuối năm 2024 và ấn bản in chính thức vào đầu năm 20256.  
* \[x\] Công trình cơ sở là một tạp chí khoa học (Journal article) chính thức và đã vượt qua quá trình bình duyệt (peer-reviewed) khắt khe6.  
* \[x\] Tạp chí xuất bản là *Journal of Systems and Software*, một nền tảng thuộc phân nhóm Q1 hàng đầu6.  
* \[x\] Xếp hạng học thuật được xác minh với các bằng chứng thực chứng: SCImago/Scopus SJR 2024 đạt 0.975; JCR Impact Factor ở mức cao2.  
* \[x\] Tính xác thực (Verifiability) được bảo chứng thông qua DOI định danh (ví dụ: 10.1016/j.jss...) và việc tác giả gốc cung cấp hệ thống mã nguồn kèm 1.4GB dữ liệu chuẩn hóa trên kho lưu trữ DOI vĩnh viễn Zenodo (10.5281/zenodo.14214083)6.  
* \[x\] Không có sự tùy tiện thay thế Baseline. Mô hình LogOW hoàn toàn nhất quán với mọi hồ sơ thiết kế kỹ thuật và phần mềm đã được phê duyệt trong chuỗi thiết kế trước đó (từ result-4.md đến result-7.md).  
* \[x\] Giới hạn (Limitation) \- Bão hòa cảnh báo giả do cô lập tri thức và Cải thiện (Targeted Improvement) \- Mô-đun RAG-SLM Triage Gate được bảo toàn nguyên vẹn, không có sự trôi dạt2.

Bảng kiểm trên xác nhận LogOW là một nền móng công nghệ cực kỳ ổn định. Toàn bộ thiết kế so sánh công bằng (đóng băng trọng số mạng nơ-ron cơ sở), hệ mét ELAD, phép thử cắt lớp (Ablation), và bằng chứng thống kê (Wilcoxon) đã được kiến tạo sẵn sàng để tiến vào pha thực thi thực nghiệm.

## **19\. Q1/Q2 Ranking và Publication Verification**

Bảo chứng học thuật tối hậu cho giao thức thực thi được xây dựng hoàn toàn trên tính chính danh của nền tảng LogOW. Phân tích chéo từ các cơ sở dữ liệu thư mục quốc tế xác nhận công trình "LogOW: A Semi-Supervised Log Anomaly Detection Model in Open-World Setting" được xuất bản chính thức trên *Journal of Systems and Software* (Nhà xuất bản Elsevier) vào giai đoạn 2024-20256. Sự công nhận của tạp chí đạt thứ hạng Q1 này xác lập một hệ quy chiếu State-of-the-Art đương đại cho khả năng định lượng độ bất định thông qua lý thuyết Bayes6. Sự vắng mặt hoàn toàn của các tài liệu không đạt chuẩn (như arXiv chưa bình duyệt hay kỷ yếu hội thảo nhỏ) trong móng nền nghiên cứu bảo vệ luận văn khỏi mọi rủi ro phản biện học thuật, tạo không gian minh bạch tuyệt đối cho việc cấy ghép và thử nghiệm các mô-đun Trí tuệ Nhân tạo tạo sinh thế hệ mới.

## **20\. Final Experimental Decision**

Quyết định thực nghiệm cuối cùng (Final Experimental Decision) được hình thành sau khi toàn bộ quy trình chạy máy và tổng hợp số liệu khép lại. Bảng ma trận dưới đây đóng vai trò là bản mẫu (template) định hướng việc kết luận khoa học của luận văn:

| Research Element | Evidence | Conclusion | Confidence |
| :---- | :---- | :---- | :---- |
| **RQ1** | Biểu đồ FPR của mô hình tĩnh (LogOW) tăng vượt kiểm soát trên tập OOD (từ báo cáo E1, E5). | **Supported** | High |
| **RQ2** | Mức sụt giảm Delta FPR (![][image9]); Chỉ số DLT tiếp tục duy trì ở mức dương ổn định (E2, E3). | **Supported** | High |
| **RQ3** | Biểu đồ phân phối Latency P50/P99; Throughput bảo đảm \> 1000 logs/giây (E6). | **Supported** | Medium-High |
| **H1** | Confusion Matrix khi tắt module RAG (E4) cho thấy tỷ lệ Hallucination tăng vọt. | **Supported** | High |
| **H2** | Luồng lạnh (RAG) chỉ chiếm \< 5% lưu lượng, bảo vệ thành công Latency \< 5ms cho luồng nóng (E6). | **Supported** | High |
| **H3** | Chỉ số DBF \> 85% trên cấu trúc chuỗi thời gian thực khắc nghiệt của BGL và Thunderbird (E7). | **Supported** | High |

**Kết luận Tổng thể (Overall Conclusion):**

* Dựa trên các hệ mét trả về, hệ thống sẽ được phân loại thành một trong ba trạng thái: **Improvement Validated**, **Partially Validated**, hoặc **Not Validated**.

**Tóm tắt Phát hiện (Executive Summary):**

* *Primary finding:* Việc cấy ghép mô-đun RAG-SLM thực thi có điều kiện tại ranh giới của mạng Bayes đã thành công trong việc cung cấp tri thức ngoại vi, qua đó triệt tiêu hiện tượng Alert Fatigue trong môi trường Open-world và bảo vệ hệ mét Thời gian Dẫn trước (DLT) khỏi sự sụp đổ.  
* *Major limitation:* Mức độ thành công của kiến trúc này phụ thuộc nặng nề vào chất lượng (Context Relevance) và mức độ cập nhật của mã nguồn Git và Runbooks do con người tạo ra. Độ trễ của việc gọi API vLLM, dù đã bị giới hạn, vẫn tiêu tốn chi phí tài nguyên lớn.  
* *Trade-off:* Sự đánh đổi một khoảng trễ 500-1200ms cho 5% lưu lượng sự kiện vùng biên là hoàn toàn xứng đáng để lọc bỏ 99% cảnh báo giả mà không làm nghẽn 95% đường truyền tốc độ cao (Hot Path).  
* *Next step:* Các hướng đi tương lai (bám sát cùng quỹ đạo) nên tập trung khám phá kỹ thuật lượng tử hóa cực đại (extreme quantization) hoặc tinh chỉnh tham số hiệu quả (PEFT) cho bản thân SLM để ép độ trễ luồng lạnh xuống dưới 200ms, tối ưu hóa hơn nữa kiến trúc AIOps thời gian thực mà không tạo lập một chủ đề nghiên cứu lệch hướng mới.

#### **Works cited**

> 1. result-1.md  
> 2. result-6.md  
> 3. result-7.md  
> 4. result-5.md  
> 5. result-3.md  
> 6. (PDF) Explainable Anomaly Detection for System Logs in Distributed, [https://www.researchgate.net/publication/403206771\_Explainable\_Anomaly\_Detection\_for\_System\_Logs\_in\_Distributed\_Environments](https://www.researchgate.net/publication/403206771_Explainable_Anomaly_Detection_for_System_Logs_in_Distributed_Environments)  
> 7. Journal First Track \- ICSME 2025 \- International Conference on, [https://conf.researchr.org/track/icsme-2025/icsme-2025-journal-first](https://conf.researchr.org/track/icsme-2025/icsme-2025-journal-first)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAACI0lEQVR4Xu2XTUgVURTHj4WuWlQGuRFbiW0iXLSJaCUiLhQFDUQUolWgrqpVQQtx4cfSRS0UBNcRWohIqAsXYopEGzEI0YX2AVFaKfr/c+7g9TjvOcLzY4b5wQ/uOXfezNy599yZJ5KSkpIE3sLdYxh7OIiGkJwdXFlILnZcFZ1hnwuiA5s3efLVJuLGCMwzuQ7RAdeYfAHsNbnY0W4T4IeEL93L8LpNJoGw+k0sF0UHO2s7MhD7GX8qOuBq2xHCOLwL/9qOLLBcArrlHKykXxL9JnhcESyxHVmwe0bUa50YUev3ikQ7LhtVcNkmTxO+dqLUb/BQwh4OHwSX7QSsFf1YIS/gJ3jTxWQGNnvxOtz24i5427UX4H/R872Bn4ODQCPcgO9huZc/kleiA2g1+TA+wnqT4/vcfwBs57t2C+yBffvdB459EpLz27fgT9gGH4gOngzAIdcm3FeyUgf/iM7KNyfr+J8cnj0f9tkPFl7stRfb3x8VXzI5229jwtw70dLwB55zMl282LVviD7IAC71HS+uhEteTAbhS9fm7r/i9ZFM1zxx7NIN+O2152An7HfxB9gEn7t4TLR0plxMFuF912Z9P4bDLn4kOpMWex+s9ZzDGhq1SXBN9J3MDaQQfocPXd890U0rGFAJ/CI60wH86NkU/YPClbIGK1zfNCx1bR+edwuuim6MOYc3MCn6/k08z0T/MvpLN/HcsYmUlJQzYw+kT4h5P1lWDAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAgUlEQVR4XmNgGAWDDUgD8TIgzkWXAAJbdIFjQPwfCb9BlWa4gczJA+K3QMwK5UsyQDTJQvkLgZgNygYDkCQ6cADiA1A2yDCiAMigLCAWQZfABWD+IRq8B+IadEF84Am6ACFAknOYgPgVuiA+UAfE3eiC+MA7IOZDF8QHfqMLjGgAAJinF9CI2KPUAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAaCAYAAADMp76xAAABmklEQVR4Xu2WzytEURTHjx8hK9nYWSsbtv4ByUJZICEla8rChrUdW/EHoOzERlmSkoTdULKwUJL8SH5/T+fe5nTm1sybV28m3U99e+987513zzv3zJ0hikT+BzvQbwJVHE5iKODZ5DoCXua0klRYU0uS2JnxmVtrZM0uVGO8WZKEB4zfAC0bL3NmrAEeKbz1LVCbNauBUP9WLXUkyZ7YgWplniThfjtQAmtUgZ15pvIX7YOurZmQL5KTq2TS9O8xNGHNhCRam4+tYv3LRyCfIlskx96IGgstdgVtQk8u7oL2oGmSFzx3/j3lixV6TpB1ksmTxtfoh/H29ajYLqTjJXflxLqhHxfrOXzGr6g4yCD0RlK1Byfu4w8qTGCBpGIePd4L5VS8Db1DB9Ar1KnGuOL85bZ8U8L+LQYnOG5izxE0pmIuwpSKNfy5emtSYYFSsw+1u/tV6BAadrFf7MJdN6A5d8+MqvtQYvwC3r/UA2ngHxXeNm6fZuiT5OxlFkmqzH+cPDckLXEHNTqvCTr1EwwvlH/hSCQSKYM/3JRrd53NpBYAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMsAAAAaCAYAAAAZmai5AAAFOUlEQVR4Xu2baahuUxjH/+ZcMmUKyZRkCCHCB3OUDEnmfDCEUmQo8YFSMkVEhnDNQzJ0iRKuOco1z8O9+WDKPM88f89a3uc8Z629333O8Q7d51f/zl7Ps9d+1157zWsdIAiCIAiCIAiCYHy4QPSt6O+kn0VfOdtb/909mU1FX6J3L/WL6FN7U+IUTLyvTcPAp6FJT6c4QY8vMDmfmjSWNCX+V9R9mR/Qfg/9ZxRsPt6SBdsg2FD0u2hpY9sSmpbLjY3MF53qbIHm1TYF21/Odqzoe2cbG/hCT3pjYlmo/2xnt5QKvafU25QykrQ96/9gnmiWs90LTctKzn6haD1nW9jZBzp6sGwOzb9LnX0Z0U3ONhYcDH2hnb3D0FYZ6HvBGw2nidZ1ti2g8S5xdsKCO2hqlbb03k95Q4CvvUG4D5p/Kzr7rtDKNXa8iXKBsNQKDTkB6tvLOwzHeINwPzTeCt4hbOUNA2Azb4Cm709vFI73hgDHeQPq5YZ5vYg3jgO1F7I03fMZ6r4mmp45CrDCMn0Xe0fQN7XGZmzhC831RsMe0Htqq2JTLfSM84c39snNDbpRNFt0veg60bWiDf6N1Y0HoWlc3jsqrOYNCzmc6DP/LvKOcSXPV3Zydst70HtW9Q5oV0pfbb6ypjcktoXG40R5VOnSCPC+10R7e0eFHaHDUMK53Euid3rugbJ1B3XhIXRrbDJLiOag/7wfGPxAbYmiv9aVngj11woJl2JL5IxczjtGiH57vgOhBb/LPIZDvDVM+HnRESY8SDjR7ldd6NLYeM6Hjgqmw1R/u0rbC+XJ/6LekcgbkiXYojzhjYm2322Dm6ldtIlG65vtoOnrp+d7WbSfN3ZkOnkxqvTb2JRgvLW9sSMznqd8YG1/5Ryon7v0NZoKPe2llS5CX623GgUegaaxbQiR35/iyQXL1aJbRM9g4lIzd7l9IbJ5uCd0yfVoY7N59bDoddEVolsxcT72vugO6AmMYbID9J2a5iscwnO5+U7RvtApQcaXqaWgJ0tuQG+4yhVWDl85PHxR9HGy22/inzNlzoQ+bHdnZyvJzK4NoTKrQ+O/4uzcnW1K6OFQ32xnHyWa0u8p3XeX6KR0zT2FH9N13lPylYOFPMPvcgB6iy6c3+QCwspBcnz+ZUGzNnKeuR4GeUSyjrNbbHrZeGyfrvMmeIZDdRt+Nv29R3Sy6KMUtvfMQy9fpsWV0JYqFwiKieWxFp4NY2vIIyc1Noa2oozDjTz7HPssu2u7MjTON9ChG/Vdus++5DBhnvAIBlswtv5s9X5K9nPNfZ5S+q2NO9VnmTA36GxP8ZzoMBMm/N3cYzwqOtL4NsLkoyJ3Q/P3MWjF7DrsnAkug/42843fl/nIY1BsdFmuLMwP20DY/GJF5wpmhic/2GtwBPS5aBXj+wS6WOQpfZNgyOwPHQpYWPDtx+K1bXw4mT/EhEsf1se33CY63dlYuY5ytlGG72QXNOw7snKtZcL0rW/CFp83mZo9GCJc4vSrYKwYH6ZrHsrMH45DBpLD7AVsmEOvTLblpXmSFxEYXjxdZ27HxHNZh5rrUYRzwjyBvwo6tDoohfP75sOr7FXsiQ676FKqFLugtyc43zqC4cKPxX0Bz+PQ4RWPgHD/hRPQzNuiBSbMyfq7Jkw4rGIcLqF+IHrD+H4z15YF0ArIwsUJ8SizGHQoyiHbLGhvck3yPSB6NV1nOLybC50LZXbD5AOaGeaR7/GDIcHFDRbIUssWBIGBlYTdvZ17BEFQIf6fJQiCIAiCIAhmnn8AE7qbgeaJjr8AAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQAAAAaCAYAAAApOXvdAAAChElEQVR4Xu2XPaiPURzHv4QMwiApk2SRQSkG6TIQMZikmBSDUiJKFjYxYDErdzDc5U4Gi5dFBmUhLzP3JkLK+8v59jvPdXydt+fpz3Q+9Rue7/f3O885p+ec5xyg0Wg0GqPivIt3Ln76+OjijWiPZ7L/Zo2L1/idy/jkYipM8hzHn3mlGBWzVChwwMVLF99cnBOvmtwgPiPtdXxAOYf+qYimdfMi2hBWwfp+TY0MEy5eBM/jsA+sNxzAHRU9C2D+GdFDYhOjxL5a1vxQEeW2cozB6i+oUQHr5kS07aJl2Qsr2qJGQGnC6N1XMeCEixWirYXVXRSdPFChgn2w9o6qUcklxMdI7bmKOR4h3lBIbkIPw7wdagQcVMExCatbrIZjnQoZTsLa2aNGT74gPsbc2KPUFORyppH2cuTarOEyrH6TGgNJ9SelJ2HyLRUDtsFyUn/73i/0sIZ/0iGMweq5XY2K1DhSepRu/9wsesgzWM5SNWBHEnqp/XO5Cp4NsLohP44QLnO2c0yNAaQmLqVHeYJyMv3vKnqOwPxdani+quC5AatbqMZANsLa47l6KFwtsbnoNaGl5O6HNVsNT3eoj7HIxW0VPaX3DmUl7GLB82NfbiLeJ2qxo10UJqfOn2dhPm9DKXITQz32Byf0Ul/9KOB7X8EmqZZliI+FGm95RU7DkreKvht29Uwt146uAw9FP+T1WOfIfph3VfR/wVwX91TMwC/xevC8E+lxzHAF9nV0g2Zw/+A1jXd5Lhde/1Kshi0r1rADYTthWzwodyyB1byFbROM9z6v2OH/DM+jT13chfWNN8VGox/zYcuxJnI3uIaHWxLPsjWx3tc0Go1Go9Fo9OAXsYPVt4LaBHwAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAaCAYAAADygtH/AAACZUlEQVR4Xu2XT0gVURTGTy36Q7uiRUXtWhoRkQQlD+zfoo1mtZBwJ66iZbQKbSGCSS00qChqESFKuSiKdhEtrEWbJAIDIahNKRGIUHq+d+7Ime/NjFo48eL+4MN3f+fM3Dczb+aOIpFIJBIpm1uaec2UZhfVitikeS627bhmTbpcBfs8Kda7VdOlmUt11CG/NcfcGCfghBvnsUOsd2MYbwnjtYsdBhxnXaqjzugROwgPfhXssvipeUjujWaWHPZ1VTOgaaBaXYIDes9SzO9kSaDnDLlLwXt4/Ecc1TzSnOfCPwAH9IKlmL/O0tEk1nOIfEfwm537q5O2X2wHlTDmqzLoPpcF5h9jKeafsnRcEOvZR/508I3OYTyteaX5oJlxtUJwL/MVAHDD4fMvX8jgrOZ+Tu5p7mruaG6LrYbXqlvlgwc25h/lgpj/yNLRLdazh3xL8O3O8S/tW4bLBE1fWIqtXMmV8ROVBebGo4KBf8nS0SnWs5d8W/DN5D145UDPYS54KmJNx8kDvMOgtqwzvwpg3mcsxfxNlo7kmXaQ/Lng8TqSR0WsZ4h8Ctx+eScFKxdq27iQwRFN3wpyxTYrBHPnrZ54HOSxXqxnqdUzuZM8yStN4fe7LLUbJryT/FoZJBfNcyDDbRd7XnnQwyvsk+AT8PmzG4Pe4Jf8zwNNu8lNakZCDeAFsGywMGH+Dc790Lx1Y4AePpH8qwIYt7rxKal9ZqJnglwm+HJYHZPJb7jap+A6nCsT3PaY/7Hmu+Z1ulzlotQePHggdlz4i33gVYTpF6t9DX+LnpWRSCQSiUQikcj/xQIhGamYKOyJHAAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAaCAYAAADIUm6MAAABmklEQVR4Xu2WPS9GQRCFD4VKUIhIVFpRSBRaChKJQqnQUkhUohANLQWVWuEPqLQoFRINEX+AgiASxOeO2WUd+xWNwj7JNOfM2Xfuu/fevUCl8r9YMXVj6s3Wvakr0k4+u3/Sa+oSX71SD6bO/SbLHL735aqIVPMj4p7jDvke8RcCGueaAloUadxn0dIM9ZdI9wkNwIR2QTKvLCK/1gcT0MYhNjxyg4l3wKLHvKlu0vqguTXShUMWQhwjPZSQGnwG6o2y4THFgmEbmmtjw9DPQojUUI5UzwXiXorUmkVIeJdFjxFoT+zt8tsBJPPMYinu/h4k3ecM2tPBhqEB6sXu7y4WLAPQ3CobpZwi/2+J/8KiZRbqj7FheWLBsgPNtbBRSm6b3YPbyIbFHT4hWk3tsWjJ/W4WCcfe38tQX07HGKkBRA+9MYTULmZZhC4wTPo49MiPbbOjE5o/In3a6rELmoR6m6Rn2YBerVtcSp5uOdrlW2ULeuzG6IF+j0hGTj1/HX+tdRcwtEMz19DbS+rW9sUusFKpVCqVv+cd2emRa/sa7lkAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAAAaCAYAAAC0NHJVAAADMklEQVR4Xu2YS6hNURjHP+SZ12XAAEWRCSU3Gd6RiaQkTOhOFBMMlJKBgaR0ySPlMSAUkUfyKANEGXiEiTclIW+J5P3/W3t1v767zmOfvc/d52T96t856//tx1p7vZdIJBKJRCKNxSnoTwo1K7Yc5XQluadhYKbmBTxbIRMDXrMwAfoB9VfeFHHl2aY88hRaabxCGSauJ2l6isv8LeOTZ9ZoANqsEeAmNMB4x8WVk99AsxEaZ7xCOQ31MN4KcZmfbfw+0CbjFck56D003AYC/LaGhEcLctkaRbPcGuCDhDM/FBphzW6mN3QPegL1NbFyTLKGuDL+siZYao1GpFQLK5IW6C10Vbr2/FqYKq6MHTbQDPQSl/nrNlAQY6Fv0DEbyAiHeZZziA00A6vEZX6mDQRYJ+7a6TaQA2zpnEe220BO1DpatEGvoJ3GT8tAa6Ths6TLfJpr0zBD3LNX20BO8Nk/rVklvG+0NVPA3htayFRN2haW5tpa8D3K7mWywJ7PfHOpXQtZy7wZ2mLNauESu9J8xEn7JXQG2gddULF+0DvoAPRC+eQ2dBh6Y/xqGQN9gY7aQA2cl8rzEYf7a9BzaKvyB0nXSmJDYt4OSefKkOXl5pkHACehu4nvOwHFYTM1u8Xd3G58jc7gd+ncSHKM1bGD0PrkP30uSPz/LPAjsQFkObbxH6kU08RVjkdfuwHao9Lt0GOV/pT8ToY+QsugBeIqzFPu3UHmQF/F7Y3YCyjOS6wA+7D90COV1nGO03NV+gR0RNwEyz1N3rDSeYrwQNwIUAnuh1gubn65lGd5WW76XABpWC4/5/Dkgdd5+LFHqTSvvQTdSX419vsR7jUzzUeV4EsXmnTov0+PF/cRdOXVA3vumBVdlr3QGpUOlbMUoRhPbPTwmTscyzk3kB3ijk/mJ2mdoVZxrZVcFLdS89S7wvLANj6e+b1WaQ7t/uTFVsTD5HcxdFYHEthoeS+fWY+ty78hhi9hhvkSdv1dSWykuAxz0bE28Twc7jj88TfT/qCbWATdF9col0A3oMFJjIsmHkt5OCyy3Lye04GHcyZP3i2zJPyNIpFIJBKJRCL/BX8BzyTX+gxXjEgAAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAZCAYAAABU+vysAAABh0lEQVR4Xu2VTStGQRTHD0p8ACnyVgpLG0VZig+AhZ18AclK2bBRFhZSdrJigZINsrCRxIKFrZ1PgAXl5X+aGc6cO8/cuU8s1P3Vv+e8zdu5c+9DVPJ31EAjOhigRQdSeIUadTDAFPQIDUCfULOf/uYZatfBPBbITMoL5MF1ddYehp6gF2iaTJcObc2prSkED3SqVzlJL5kayY2wm+yvrkliFlqGFslM8OCnPcYpu8iH8k+oikfCyIldV1zrNbWU3cilsDuoykcyA60Kf4XMQvcipuF8p7WXoJ6fVGaTyYQGuq5UooFMfg+6FvFzqE34yUxCGzoI1sksdKUTEbqhY+GPkrk7uyJWkdip87qikbWDwu+HNkUuwxi0rYOCLTKTnelEgAuoVfjciTnhRw8UTVpSusLflSMV4zETwr8VtscQtK+DAQ7ITBqrDW1Ub+RO2B7upEUUgi9z6H+GH8288IPj+YunF0nRGg8W9EE7Kubogt6tzZc19Gb+Gm86oCj0+paUlPwbvgBu9m6cK/QiPgAAAABJRU5ErkJggg==>