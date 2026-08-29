# **Đặc Tả Thiết Kế Kỹ Thuật: Tối Ưu Hóa Phương Pháp Phát Hiện Sớm Bất Thường Dữ Liệu Log Bằng Cơ Chế Phân Giải Độ Bất Định Dựa Trên Sinh Tăng Cường Bằng Truy Xuất (RAG) Có Điều Kiện**

Tài liệu này cung cấp một bản đặc tả thiết kế kỹ thuật ở cấp độ kiến trúc phần mềm theo tiêu chuẩn IEEE, phục vụ cho quá trình triển khai và kiểm chứng thực nghiệm mô hình phát hiện sớm bất thường dữ liệu log (Early Log Anomaly Detection). Toàn bộ kiến trúc được xây dựng nhằm mục đích khắc phục hiện tượng bão hòa cảnh báo giả (Alert Fatigue) trong các môi trường vận hành thế giới mở, nơi sự trượt dạt khái niệm do các bản cập nhật phần mềm liên tục làm vô hiệu hóa các mô hình học sâu tĩnh1. Phương pháp luận xoay quanh việc cấy ghép một cơ chế phân loại tự động sử dụng Mô hình Ngôn ngữ Nhỏ (Small Language Model \- SLM) kết hợp Sinh tăng cường bằng truy xuất (RAG), được kích hoạt độc quyền bởi hệ thống ước lượng độ bất định Bayes từ một phương pháp cơ sở đạt chuẩn Q1.

## **1\. Design Freeze Verification**

Bước xác minh thiết kế đóng băng (Design Freeze Verification) đóng vai trò là chốt chặn pháp lý và học thuật, đảm bảo toàn bộ nền tảng lý thuyết đã được phê duyệt sẽ được ánh xạ chính xác thành các thành phần kỹ thuật. Sự nghiêm ngặt trong khâu này ngăn chặn hiện tượng trôi dạt phạm vi nghiên cứu và bảo vệ tính hợp lệ nội tại của các so sánh đối chứng1.

| Element | From result-5.md | Technical Interpretation | Q1/Q2 / Publication Check | Changed? |
| :---- | :---- | :---- | :---- | :---- |
| **Baseline** | LogOW (A Semi-Supervised Log Anomaly Detection Model in Open-World Setting)1. | Tái sử dụng nguyên vẹn mạng nơ-ron Bayes, cơ chế cửa sổ trượt, biểu diễn vector liên tục và Monte Carlo Dropout. | Tạp chí: *Journal of Systems and Software* (Q1, SJR: 0.95, IF: 3.8). Năm: 2024/2025. Có DOI và Zenodo Repo2. | Không |
| **Limitation** | Bão hòa cảnh báo giả do cô lập tri thức khi gặp trượt dạt khái niệm1. | Mạng nơ-ron thiếu cơ chế tham chiếu đến cấu hình cập nhật hệ thống, dẫn đến việc cắm cờ bất định sai lệch cho các sự kiện hợp lệ. | Bằng chứng học thuật xác nhận hạn chế này qua thử nghiệm luồng dữ liệu ngoài phân phối (OOD) của mô hình LogOW1. | Không |
| **Targeted Improvement** | Conditional RAG-SLM Triage (Mô-đun RAG-SLM phân loại có điều kiện)1. | Thiết lập cổng quyết định hậu xử lý. Kích hoạt truy vấn RAG/SLM khi và chỉ khi Predictive Entropy vượt ngưỡng động ![][image1]. | Đảm bảo tính can thiệp tách rời (Decoupled Intervention), bảo toàn toàn bộ trọng số gốc của LogOW. | Không |
| **Input** | Dữ liệu log thô từ môi trường tích hợp liên tục (CI/CD). | Luồng chuỗi thời gian phân tán từ siêu máy tính và hệ thống đám mây quy mô lớn. | Tuân thủ nghiêm ngặt kỹ thuật phân tách theo thời gian (Chronological Split) để loại bỏ rò rỉ dữ liệu tương lai1. | Không |
| **Output** | Cảnh báo sớm (Early Alert) kèm theo lý giải nguyên nhân rễ. | Cấu trúc JSON chuẩn hóa từ SLM chứa quyết định phân loại (Auto-triage) và diễn giải ngữ cảnh hệ thống. | Phục vụ khả năng phân tích chẩn đoán cho các kỹ sư trung tâm điều hành bảo mật. | Không |
| **Main Evaluation** | Detection Lead Time (DLT), Early Warning Horizon (EWH), FPR trên tập OOD1. | Xây dựng khung đo lường động học chống rò rỉ dữ liệu tương lai; đánh giá độ trễ tính toán theo thời gian thực mô phỏng. | Bác bỏ các phương pháp đánh giá tĩnh thuần túy; tập trung vào khả năng cung cấp khoảng đệm thời gian cho vận hành1. | Không |

Quá trình đối chiếu kiến trúc xác nhận không tồn tại bất kỳ sự sai lệch nào so với tài liệu thiết kế ban đầu. Sự nhất quán này cho phép thiết lập một khung đánh giá có kiểm soát, nơi mọi cải thiện về hiệu năng đều được quy chiếu nhân-quả trực tiếp về mô-đun cải tiến.

## **2\. System Boundary**

Ranh giới hệ thống phân định rõ ràng các giới hạn kỹ thuật, đảm bảo độ phức tạp của quá trình phát triển phần mềm được kiểm soát tối đa nhằm phục vụ duy nhất một mục tiêu là chứng minh giả thuyết khoa học1.

### **In Scope**

Hệ thống bao trùm các thành phần điện toán và vi kiến trúc cần thiết để tái lập phương pháp cơ sở LogOW từ mã nguồn gốc, đồng thời triển khai mô-đun cải tiến RAG-SLM. Các thành phần trong phạm vi bao gồm bộ phân tích cú pháp biểu thức chính quy (Drain parser) để trích xuất mẫu log, môi trường lưu trữ cơ sở dữ liệu vector cục bộ (điển hình như ChromaDB) để kiến tạo không gian truy xuất ngữ nghĩa, và công cụ suy luận (inference engine) vLLM chạy trên cụm GPU Nvidia RTX 3090/4090 nhằm gia tốc quá trình sinh ngôn ngữ1. Toàn bộ các công cụ phục vụ việc thiết lập luồng dữ liệu đánh giá cắt lớp (ablation studies), đo lường thời gian dẫn trước (DLT), và đánh giá độ trễ tính toán (latency overhead) đều nằm gọn trong ranh giới thiết kế hệ thống.

### **Out of Scope**

Nhằm tránh sa đà vào hoạt động kỹ thuật phần mềm thương mại, các kiến trúc dành riêng cho nền tảng AIOps doanh nghiệp bị loại trừ hoàn toàn. Cụ thể, hệ thống sẽ không bao gồm các bảng điều khiển trực quan (Dashboards), cơ chế tự trị khắc phục sự cố vật lý (Autonomous Remediation), hoặc hạ tầng phục vụ đa khách hàng (Multi-tenant Infrastructure). Kiến trúc cân bằng tải, cơ chế dự phòng thảm họa (Disaster Recovery) và các microservices quản trị phân quyền người dùng không thuộc đối tượng của thực nghiệm này. Mục đích của ranh giới này là duy trì một phòng thí nghiệm phần mềm khép kín, tối thiểu và thuần khiết để kiểm chứng độ tin cậy của thuật toán phân giải bất định1.

## **3\. Baseline Implementation Specification**

Mô hình LogOW đóng vai trò là một tham chiếu đóng băng (frozen reference) không thể sửa đổi ở cấp độ lõi, cung cấp cơ chế nền tảng cho việc nhận diện sự trượt dạt khái niệm thông qua lý thuyết học sâu Bayes1.

| Component | Responsibility | Input | Output | Parameters | Dependency |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Log Parser** | Trích xuất các mẫu cốt lõi từ văn bản log thô chưa cấu trúc. | Raw log streaming messages. | Log templates (keys) và các tham số biến thiên. | Thuật toán Drain; Độ sâu cây tìm kiếm (depth \= 4), ngưỡng tương đồng mặc định1. | None |
| **Representation** | Ánh xạ các log templates vào không gian ngữ nghĩa liên tục. | Log templates. | Dense Vector Embeddings. | Ma trận nhúng liên tục đã học (Semantic Embeddings). | Log Parser |
| **Windowing** | Phân mảnh luồng sự kiện theo chuỗi thời gian liên tiếp. | Timestamped Vector Sequence. | Sliding Context Windows. | Kích thước cửa sổ quan sát (Window Size), Bước trượt (Step Size). | Representation |
| **Core Model (BNN)** | Xấp xỉ mạng nơ-ron Bayes để theo dõi trạng thái. | Sliding Context Windows. | Phân phối xác suất dự đoán trạng thái hệ thống. | Monte Carlo Dropout (MCD) áp dụng trên các lớp ẩn (10 vòng truyền ngẫu nhiên)1. | Windowing |
| **Anomaly Scoring** | Định lượng mức độ bất định nhận thức (Epistemic Uncertainty). | Tập hợp phân phối xác suất từ ![][image2] lần truyền. | Predictive Entropy ![][image3]. | Phương sai dự đoán tính bằng công thức Entropy thông tin toán học. | Core Model |
| **Decision Rule** | Phân lập dữ liệu nằm ngoài phân phối (Out-of-Distribution). | Predictive Entropy ![][image3]. | Nhãn nhị phân: Normal hoặc Uncertain. | Ngưỡng cắt động ![][image1]. Nếu ![][image4] cắm cờ bất định (Uncertain)1. | Anomaly Scoring |

Đặc tả triển khai này tuân thủ trọn vẹn mã nguồn lưu trữ trên Zenodo (DOI: 10.5281/zenodo.14214083), bảo toàn tính toàn vẹn của thuật toán tính toán độ bất định2. Sự thiếu hụt hoàn toàn của bất kỳ mô-đun truy xuất tri thức nào ở baseline nguyên thủy chính là khoảng trống kiến trúc mà phần thiết kế cải tiến sẽ lấp đầy.

## **4\. Targeted Improvement Specification**

Cải tiến nhắm mục tiêu (Targeted Improvement) giải quyết trực tiếp một điểm nghẽn duy nhất: Sự cô lập tri thức của các mô hình nơ-ron khi đánh giá dữ liệu mới. Cơ chế Conditional RAG-SLM Triage được thiết kế như một bộ não ngoại vi, hoạt động độc lập và chỉ được đánh thức tại các điểm giới hạn của phân phối dữ liệu1.

| Improvement Component | Input | Responsibility | Output | Baseline Relation | Hypothesis |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Conditional Triage Gate** | Predictive Entropy ![][image3] và Ngưỡng ![][image1]. | Giám sát điểm bất định để định tuyến luồng dữ liệu (Hot Path / Cold Path). | Tín hiệu điều phối luồng và khóa cửa sổ log. | Gắn trực tiếp vào đầu ra của khối Decision Rule của LogOW. | H2: Kích hoạt có điều kiện bảo vệ độ trễ hệ thống \< 5ms cho phần lớn lưu lượng1. |
| **Knowledge Retrieval** | Chuỗi log bị gắn cờ "Uncertain" (Query). | Tìm kiếm lai (Hybrid Search) các tài liệu lịch sử vận hành tương đồng. | Top-K Documents (Context). | Ngoại vi hoàn toàn. Không can thiệp vào đồ thị tính toán của BNN. | H1: RAG cung cấp tri thức hệ thống cập nhật để phá vỡ sự cô lập ngữ cảnh1. |
| **SLM Reasoning Engine** | System Prompt, Retrieved Context, Dữ liệu log vùng biên. | Thực thi In-context Learning để suy luận logic nhân quả. | JSON Object: Phân loại cuối cùng (Benign/Anomaly) và Diễn giải. | Hoạt động như một tác tử hậu xử lý nhằm tự động hóa quy trình phân tích thủ công. | H3: Cơ chế suy luận triệt tiêu 99% cảnh báo giả cho các dữ liệu chưa từng thấy1. |

Bằng việc quy định rõ ràng trách nhiệm của từng cấu phần, kiến trúc ngăn chặn sự can thiệp chéo, giúp việc quy kết nguyên nhân của sự thay đổi hiệu năng trở nên minh bạch tuyệt đối trong quá trình đánh giá.

## **5\. Overall System Architecture**

Kiến trúc hệ thống tổng thể áp dụng triết lý phân luồng kép (Dual-path Inference Strategy), tạo ra một đường ống lai (Hybrid Pipeline) nhằm giải quyết bài toán nan giải về sự đánh đổi giữa tốc độ phản hồi của các thuật toán xác suất và trí thông minh lập luận của AI tạo sinh1. Hệ thống tổng thể là sự ghép nối giữa các cấu trúc **Baseline \+ Targeted Improvement**, được phân loại theo trạng thái thành phần.  
Luồng nóng (Hot Path) là xa lộ dữ liệu kế thừa nguyên trạng từ LogOW, đảm nhận trách nhiệm xử lý tốc độ cao. Dòng sự kiện thô đi qua Log Input/Parser (trạng thái: Inherited) và mô-đun Window/Representation (Inherited) để chuyển hóa không gian. Sau đó, dữ liệu được truyền vào Baseline Module (Inherited), nơi mạng nơ-ron học bán giám sát thực thi các đường truyền ngẫu nhiên (Monte Carlo Dropout) nhằm ước lượng phương sai dự đoán. Ngay tại cổng xuất, một nút rẽ nhánh điều kiện (Conditional Fork \- trạng thái: Modified) được thiết lập. Đối với hơn 95% lưu lượng dữ liệu tĩnh mang đặc trưng phân phối quen thuộc (Entropy ![][image5]), tín hiệu sẽ trực tiếp đi ra hệ thống cảnh báo mà không phải chịu bất kỳ độ trễ suy luận nào từ các mô hình ngôn ngữ lớn1.  
Luồng lạnh (Cold Path) là mạng lưới tư duy sâu, chỉ được đánh thức khi nút rẽ nhánh phát hiện sự trượt dạt khái niệm nghiêm trọng (Entropy \> ![][image1]). Khối lượng dữ liệu bị đóng băng này được điều phối vào Improvement Module (trạng thái: New). Hệ thống kích hoạt Knowledge/Retrieval/Context Module (New) để truy vấn cơ sở dữ liệu vector cục bộ. Khi tập hợp ngữ cảnh lịch sử đã sẵn sàng, Foundation Model Module (New) vận hành thông qua engine vLLM sẽ tiếp nhận chuỗi Prompt để tiến hành chẩn đoán. Hai luồng dữ liệu cuối cùng hội tụ tại khối Detection & Evaluation (New / Evaluation-only) để xác lập các hệ mét cảnh báo sớm và kết xuất siêu dữ liệu thực nghiệm1.

## **6\. Research Traceability**

Mối liên kết chặt chẽ giữa các câu hỏi nghiên cứu, giả thuyết và kiến trúc kỹ thuật được vạch ra để đảm bảo không có bất kỳ dòng mã nào được phát triển mà không phục vụ một mục đích học thuật cụ thể1.

| Research Requirement | System Component | Experiment | Metric |
| :---- | :---- | :---- | :---- |
| **RQ1:** Giới hạn của xấp xỉ Bayes khi gặp Concept Drift. | Baseline Module (BNN \+ Monte Carlo Dropout). | E1 (Reconstruction), E5 (Robustness). | FPR đo lường trên OOD logs. |
| **RQ2:** Cơ chế RAG-SLM phân định cập nhật an toàn và cảnh báo sớm. | Improvement Module (SLM Reasoning Engine). | E2 (Main Test), E3 (Ablation). | DLT, EWH, FPR tại vùng biên. |
| **RQ3:** Tác động của RAG lên kiến trúc thời gian thực. | Inference Workflow (Hot/Cold Path). | E6 (Efficiency). | Compute Latency (ms), Throughput. |
| **H1:** Bão hòa cảnh báo bắt nguồn từ sự cô lập tri thức. | Knowledge/Retrieval Module. | E3 (Ablation Config 1: SLM without RAG). | Context Relevance, độ gia tăng FPR. |
| **H2:** Tối ưu hóa độ trễ qua cổng điều kiện (Entropy Threshold). | Conditional Triage Gate. | E6 (Efficiency). | Tỷ lệ điều hướng luồng lạnh (\< 5% tổng dung lượng), Token Cost1. |
| **H3:** RAG-SLM giảm 99% cảnh báo giả vùng biên. | Foundation Model Module (JSON Triage Output). | E2 (Main Test). | Khác biệt FPR giữa Baseline và Improved. |
| **H4:** Cải thiện hệ mét DLT ổn định trên dữ liệu động. | Temporal Data Design & Evaluation Infrastructure. | E4 (Early Detection), E7 (Generalization). | DLT duy trì giá trị dương trước sụp đổ vật lý1. |

Mọi thành phần quan trọng trong kiến trúc đều sở hữu mục đích nghiên cứu minh định, và mọi giả thuyết đều được neo chặt vào các bài kiểm tra thực nghiệm có thể lượng hóa.

## **7\. Data Flow**

Luồng dữ liệu (Data Flow) mô tả quỹ đạo vật lý của thông tin, phân định sự khác biệt giữa quy trình xử lý tiền tính toán ngoại tuyến (Offline Processing), luồng suy luận trực tuyến (Online Processing) và xử lý phục vụ mục đích kiểm chứng (Evaluation-only).  
Quy trình tiền tính toán ngoại tuyến xoay quanh việc kiến tạo không gian tri thức nội bộ. Dữ liệu thô từ các hồ sơ quản trị hệ thống—bao gồm tệp cấu hình, lịch sử Git Commits và các báo cáo sự cố đã đóng—được vector hóa (Embedding) và nạp vào cơ sở dữ liệu Vector để tạo thành kho lưu trữ Knowledge Corpus. Quá trình này được thực thi trước thời điểm chạy suy luận nhằm ngăn chặn hiện tượng tắc nghẽn tài nguyên trực tuyến1.  
Luồng suy luận trực tuyến khởi đầu bằng việc luồng Raw Logs được phân tách (Chronological Split) đi vào hệ thống qua mô phỏng streaming. Dòng sự kiện đi qua Parsing Engine để sinh ra Template, được phân nhóm theo Windowing, và chuyển hóa qua lớp Representation. Inference Engine chạy mạng Bayes để tính toán Anomaly Score (Entropy). Khi thuật toán xác nhận trạng thái ![][image6], luồng tiếp tục thẳng tới Anomaly Prediction. Khi tín hiệu ![][image7] xuất hiện, luồng sự kiện chuyển hướng lập tức. Query Builder đóng gói cửa sổ log hiện tại thành truy vấn thô. Vector Database tiến hành Retrieval và Ranking/Filtering (áp dụng cơ chế Time-decay) để xuất xưởng Retrieved Context. Mô hình SLM tiếp nhận Context và tiến hành suy luận (In-context Classification) để sinh ra nhãn dự báo cuối cùng.  
Kết quả từ cả luồng tuyến tính và luồng RAG được hội tụ tại mô-đun đánh giá. Mô-đun này (Evaluation-only) so khớp dự báo với các nhãn thời gian sự cố (Failure Time) ẩn để trích xuất DLT và EWH, trước khi kết xuất dữ liệu cho hệ thống phân tích.

## **8\. Temporal Data Design**

Khung dữ liệu thời gian là cấu trúc mang tính sống còn đối với bài toán Phát hiện sớm (Early Detection). Bất kỳ sự vi phạm nào về trật tự nhân quả của sự kiện sẽ lập tức dẫn đến hiện tượng Rò rỉ Dữ liệu (Data Leakage), làm mất đi tính hợp lệ của mọi kết luận học thuật1.  
Thuật toán hoạt động trên một Cửa sổ Quan sát (Observation/Context Window) trượt dọc theo dòng thời gian của hệ thống. Trật tự của các dấu thời gian (timestamps) được bảo tồn tuyệt đối; mọi kỹ thuật xáo trộn ngẫu nhiên (Random Shuffle) thường thấy trong học máy tĩnh đều bị nghiêm cấm.  
Hệ mét thời gian được đặc tả thông qua các điểm đánh dấu mốc: Gọi ![][image8] là thời điểm hệ thống sụp đổ vật lý (Failure/Anomaly time). Gọi ![][image9] là thời điểm hệ thống đưa ra quyết định cảnh báo (Detection time). Chân trời dự báo (Prediction Horizon) và Thời gian Dẫn trước (Detection Lead Time) được toán học hóa bằng phương trình: ![][image10]1. Một hệ thống cảnh báo sớm thành công phải chứng minh được khả năng duy trì ![][image11] ổn định và có ý nghĩa thống kê. Bất kỳ cảnh báo nào có ![][image12] đều là phát hiện trễ (post-mortem) và không được tính vào hiệu năng.  
Để kiểm soát chặt chẽ quá trình RAG, nguyên tắc Sẵn sàng Tri thức theo Thời gian (Temporal Availability Control) được áp đặt. Cơ sở dữ liệu Vector lưu trữ các tài liệu (Git Commits, Runbooks) với nhãn thời gian tương ứng ![][image13]. Khi truy vấn xảy ra tại ![][image9], một bộ lọc cứng (Temporal Filter) cưỡng chế loại bỏ tất cả các tài liệu có ![][image14]1. Kỹ thuật này triệt tiêu hoàn toàn rủi ro mô hình "đọc trước" các báo cáo khắc phục sự cố (post-mortem reports) từ tương lai.

| Data Source | Timestamp | Available at Prediction Time (Talert​)? | Allowed in Prompt? |
| :---- | :---- | :---- | :---- |
| Historical Logs | ![][image15] | Yes | Yes (in Context Window) |
| Git Commits / Runbooks | ![][image16] | Yes | Yes (Retrieved by RAG) |
| Post-mortem Reports | ![][image17] | No | **Strictly Forbidden** |
| Future Incident Labels | ![][image18] | No | **Strictly Forbidden** (Eval-only) |

## **9\. Knowledge / Retrieval**

Kiến trúc Truy xuất (Retrieval) đóng vai trò là cầu nối ngôn ngữ tự nhiên giữa dữ liệu telemetry tĩnh và trí tuệ vận hành hệ thống, giúp khắc phục nhược điểm cốt lõi của các mạng nơ-ron cô lập.  
Kho tri thức (Knowledge Corpus) được tổng hợp từ lịch sử lưu vết mã nguồn (Git Commits), tệp cấu hình hệ thống, sổ tay vận hành (Runbooks), và hồ sơ giải quyết sự cố đã đóng1. Nhằm khắc phục hiện tượng Lệch chuẩn Không gian nhúng (Embedding Mismatch)—vốn xảy ra khi các bộ mã hóa văn bản tự nhiên mã hóa sai lệch các đặc trưng kỹ thuật như địa chỉ IP hay mã lỗi Hexadecimal—hệ thống triển khai kỹ thuật Tìm kiếm Lai (Hybrid Retrieval). Kỹ thuật này hợp nhất kết quả từ đối sánh từ khóa chính xác Sparse (BM25) và đối sánh ngữ nghĩa Dense Vector thông qua các bộ nhúng chuyên biệt cho mã nguồn (Code-specific Embeddings).  
Khi một truy vấn (Query) chứa chuỗi log bất định xuất hiện, hệ thống quét qua Candidate Pool. Khâu Xếp hạng và Lọc (Ranking/Filtering) đo lường độ tương đồng Cosine (Cosine Similarity), đồng thời áp dụng ngưỡng cắt (Relevance Threshold ![][image19]) để giảm nhiễu. Số lượng tài liệu trích xuất tối đa (Top-K) được cố định ở mức ![][image20] để tối ưu hóa không gian ngữ cảnh1. Đặc biệt, thuật toán tích hợp hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty) nhằm tự động hạ thấp điểm tương đồng của các tài liệu đã cũ, đảm bảo SLM luôn nhận được ngữ cảnh tươi mới nhất.

## **10\. Context Construction**

Quá trình xây dựng ngữ cảnh (Context Construction) được kỹ sư hóa cẩn trọng nhằm đóng gói dữ liệu thành một cấu trúc Prompt chặt chẽ, ngăn chặn hiện tượng quá tải thông tin dẫn đến sự sinh ảo giác của mô hình ngôn ngữ.  
Ngữ cảnh hiện tại (Current Context) bao gồm chuỗi các template log đang tạo ra mức Entropy cao. Ngữ cảnh truy xuất (Retrieved Context) bao gồm Top-3 tài liệu vận hành từ RAG. Trình tự sắp xếp (Ordering) đặt các tài liệu có độ tương đồng lớn nhất và thời gian gần nhất lên ưu tiên hàng đầu. Metadata đính kèm vào chuỗi văn bản được giới hạn nghiêm ngặt ở nhãn thời gian và phân loại tài liệu (ví dụ: \[GIT\_COMMIT\], \[RUNBOOK\]).  
Để kiểm soát giới hạn cửa sổ (Context Limit), hệ thống áp đặt mức trần 512 tokens cho mỗi giao dịch prompt1. Cơ chế ưu tiên (Prioritization) bảo vệ chuỗi Current Context không bị sửa đổi. Quá trình cắt cụt (Truncation) nếu cần thiết sẽ được thực thi bằng cách cắt bỏ các token từ phần đuôi của Retrieved Context. Thiết kế này khóa chặt không gian suy luận, giữ vững tính xác định (determinism) của thuật toán phân loại tự động.

## **11\. Foundation Model / Training**

Mô hình nền tảng (Foundation Model) hoạt động với tư cách là Tác tử Phân loại (Triage Agent) chuyên biệt, giải quyết các sự kiện vùng biên (edge cases) mà mạng nơ-ron không thể tự tin kết luận. Lựa chọn kiến trúc hướng tới các Mô hình Ngôn ngữ Nhỏ (SLMs) sở hữu dưới 10 tỷ tham số, cụ thể là Llama-3-8B-Instruct hoặc Qwen2.5-7B. Các mô hình này thể hiện năng lực lập luận xuất sắc trong khi vẫn vận hành mượt mà trên phần cứng GPU cục bộ1.  
Giao diện mô hình (Model Interface) được triển khai qua engine suy luận vLLM để tối ưu hóa băng thông. Đầu vào (Input) của mô hình là System Prompt chứa khối In-context rules; Đầu ra (Output) bị ép buộc (constrained) thành một chuỗi JSON duy nhất chứa nhãn phân loại tự động và lý do giải thích. Cấu hình suy luận (Inference Config) khóa cứng tính ngẫu nhiên thông qua các tham số: temperature \= 0.0, top\_p \= 1.0, và seed \= 421.  
**Nguyên tắc Đóng băng Học máy (Training Rules):** Thiết kế loại bỏ hoàn toàn quá trình Tinh chỉnh (Fine-tuning) đối với SLM nhằm tránh chi phí huấn luyện lại mỗi khi hệ thống có bản cập nhật CI/CD mới. SLM sử dụng trọng số gốc kết hợp lượng tử hóa 4-bit (4-bit GGUF/AWQ). Đồng thời, trọng số của mạng nơ-ron cơ sở (LogOW) sau giai đoạn huấn luyện ban đầu trên tập dữ liệu cũng bị đóng băng hoàn toàn. Việc sử dụng chung một checkpoint của LogOW cho cả Baseline và Improved System đảm bảo sự thay đổi hiệu năng được cô lập thuần túy về phía mô-đun RAG-SLM Triage.

## **12\. Inference Workflow**

Luồng suy luận (Inference Workflow) là một tiến trình vận hành thời gian thực, phân định rõ ràng các bước dựa trên mức độ nhạy cảm với độ trễ (Latency-sensitive).

> 1. **Log Arrival (Online):** Sự kiện thô tiến vào hệ thống qua dòng truyền phát liên tục.  
> 2. **Preprocessing (Online / Latency-sensitive):** Bộ phân tích Drain (cấu hình depth=4) trích xuất log template tức thời1.  
> 3. **Windowing (Online):** Hệ thống cập nhật cửa sổ trượt quan sát (Sliding window) cho luồng log.  
> 4. **Representation (Online / Precomputed lookups):** Ánh xạ log template thành Dense Vectors dựa trên ma trận nhúng.  
> 5. **Core Model Inference (Online / Latency-sensitive):** BNN chạy ![][image21] lần truyền Monte Carlo Dropout để sinh ra phân phối xác suất dự báo trạng thái.  
> 6. **Anomaly Scoring (Online):** Định lượng phương sai dự đoán thành giá trị Predictive Entropy ![][image3].  
> 7. **Decision Gate (Online):**  
   * Nếu ![][image6]: Kết luận trực tiếp (Normal/Anomaly) thông qua log likelihood ![][image22] Luân chuyển tới Bước 10 (Độ trễ luồng nóng \< 5ms)1.  
   * Nếu ![][image7]: Tạm dừng luồng xử lý của cửa sổ hiện tại và chuyển hướng qua Cold Path.  
> 8. **Retrieval/Context (Online / Delay-tolerant):** Truy vấn cơ sở dữ liệu Vector lấy Top-3 tài liệu, áp dụng màng lọc Temporal filter, thực thi Time-decay, và xây dựng Prompt (giới hạn 512 tokens).  
> 9. **SLM Triage (Online / Delay-tolerant):** Gọi API cục bộ tới vLLM, mô hình sinh JSON phân loại quyết định "Benign Update" hoặc "Early Anomaly" (Độ trễ tích lũy 500-1200ms)1.  
> 10. **Early Detection Output/Alert:** Hệ thống tổng hợp kết luận cuối cùng, kích hoạt cờ cảnh báo kèm diễn giải, và ghi nhận nhãn thời gian về Evaluation module.

## **13\. Anomaly / Early Detection Interface**

Giao diện giữa Phát hiện Bất thường và Cảnh báo Sớm (Anomaly/Early Detection Interface) phân tách minh bạch hai khái niệm toán học: Điểm số bất thường và Quy tắc cảnh báo sớm.  
Điểm bất thường (Anomaly Score) được đo lường bằng Predictive Entropy. Phạm vi (Range) là số thực không âm. Diễn giải (Interpretation): Giá trị càng cao phản ánh sự bất định nhận thức (Epistemic Uncertainty) càng lớn của mạng Bayes, đặc trưng cho Concept Drift hoặc các biến động cấu trúc hệ thống. Quy tắc quyết định (Decision Rule) sử dụng một ngưỡng hiệu chỉnh động (Adaptive Threshold ![][image1]). Mức ![][image1] này được cấu hình tự động thông qua việc phân tích phân phối Entropy của tập dữ liệu kiểm chứng (Validation set), nhằm khoanh vùng khoảng tin cậy của mô hình1.  
Cảnh báo sớm (Early Detection) không đồng nhất với một mức Anomaly Score cao. Khái niệm "sớm" (Early) được đo lường qua sự phát sinh tín hiệu cảnh báo vật lý (![][image9]) xảy ra trước sự kiện sụp đổ (![][image8]) một khoảng thời gian ý nghĩa. Bất kỳ cảnh báo nào có ![][image12] đều là kết quả của phân tích lỗi sau sự kiện (post-mortem anomaly detection) và bị loại bỏ khỏi tính toán Early Warning Horizon.

## **14\. Configuration**

Toàn bộ cấu hình hệ thống (Configuration) được định dạng theo cấu trúc YAML nhằm bảo vệ tính nguyên vẹn và khả năng tự động hóa của thực nghiệm1:

* dataset.yaml:  
  * dataset\_name (string): bgl hoặc thunderbird (Chống benchmark overfitting).  
  * split\_method (string): chronological (Tránh rò rỉ dữ liệu).  
  * train\_ratio (float): 0.7 (Tỷ lệ huấn luyện/kiểm thử).  
* baseline.yaml:  
  * parser\_depth (int): 4 (Chiều sâu cây Drain parser).  
  * mc\_dropout\_passes (int): 10 (Số vòng truyền ngẫu nhiên sinh phân phối Bayes).  
* improvement.yaml:  
  * triage\_threshold\_multiplier (float): 1.5 (Hệ số nhân độ lệch chuẩn Entropy tạo ngưỡng ![][image1]).  
* model.yaml:  
  * llm\_model (string): llama-3-8b-instruct.  
  * quantization (string): 4-bit-awq (Giảm VRAM footprint).  
  * temperature (float): 0.0 (Buộc LLM sinh đầu ra xác định).  
  * seed (int): 42\.  
* retrieval.yaml:  
  * chunk\_size (int): 512\.  
  * top\_k (int): 3\.  
  * similarity\_threshold (float): 0.75 (Ngưỡng loại bỏ tài liệu nhiễu).  
* evaluation.yaml:  
  * target\_metrics (list): \[DLT, EWH, FPR, F1, Latency\].

## **15\. Experiment Management**

Nền tảng quản lý thực nghiệm (Experiment Management) ứng dụng MLflow chạy trên môi trường cục bộ để lưu vết mọi siêu dữ liệu1. Mỗi lần chạy (Run) phải thu thập đầy đủ:

* run\_id: Định danh duy nhất theo UUID.  
* seed: Cố định giá trị 42 cho toàn bộ thí nghiệm để đảm bảo tính tái lập.  
* dataset\_version: Hash MD5 của tập BGL/Thunderbird đã phân tách theo thời gian.  
* baseline\_version: Ghi nhận commit hash từ Zenodo source code (14214083).  
* config\_snapshot: Dữ liệu YAML được dump nguyên vẹn thành metadata của MLflow.  
* artifacts: Bản ghi log JSON từ SLM, Ma trận nhầm lẫn (Confusion Matrix), và các tệp báo cáo DLT.  
* metrics: Dữ liệu chuỗi thời gian của FPR và độ trễ tính toán. Hệ thống không sử dụng W\&B hay DVC để giới hạn độ phức tạp quản trị.

## **16\. Controlled Comparison**

Việc thiết kế một không gian so sánh có kiểm soát (Controlled Comparison) là cốt lõi để loại trừ các biến nhập nhằng (confounding variables) làm sai lệch kết quả. Thực nghiệm bắt buộc tiến hành đối chứng cấu trúc A/B:**A — Original Q1/Q2 Baseline (LogOW tĩnh)B — Baseline \+ Targeted Improvement (LogOW \+ Conditional RAG-SLM Triage)**

| Factor | Baseline (A) | Improved (B) | Controlled? |
| :---- | :---- | :---- | :---- |
| **Dataset & Split** | BGL/Thunderbird (Chronological) | BGL/Thunderbird (Chronological) | **Yes** |
| **Preprocessing** | Drain (Depth=4) | Drain (Depth=4) | **Yes** |
| **Model Weights** | Frozen Base Weights | Frozen Base Weights | **Yes** |
| **MC Dropout Config** | 10 passes | 10 passes | **Yes** |
| **Threshold** | **![][image1]** adaptive | ![][image1] adaptive | **Yes** |
| **Improvement** | None | RAG-SLM Validation Gate | **No** (Independent Variable) |
| **Evaluation** | DLT, FPR, Latency | DLT, FPR, Latency | **Yes** |

Sự đóng băng toàn bộ cấu trúc nền tảng khẳng định rằng mọi sự gia tăng về độ chính xác hay bảo vệ DLT đo lường được ở hệ thống B đều có thể quy kết 100% về sức mạnh phân giải của mô-đun RAG-SLM, bảo vệ tính hợp lệ nội tại (Internal Validity) một cách tuyệt đối1.

## **17\. Ablation**

Thử nghiệm cắt lớp (Ablation Studies) được thiết kế qua 3 kịch bản nhằm định lượng độ quan trọng của các thành phần con cấu thành nên mô-đun cải thiện (Experiment E3)1:

* **Remove Retrieval (Direct SLM):** Luồng log bất định được nạp thẳng vào SLM mà không thông qua truy vấn RAG. Mục tiêu: Quan sát tỷ lệ sinh ảo giác (hallucination) để chứng minh rằng Trí tuệ Nhân tạo tạo sinh sẽ hoàn toàn thất bại nếu bị tước đoạt tri thức ngoại vi, qua đó xác nhận RAG là điều kiện tiên quyết.  
* **Remove Hybrid Search (Semantic Only):** Vô hiệu hóa đối sánh BM25 và Code-specific embeddings, chỉ dùng mã hóa ngôn ngữ tự nhiên thông thường. Mục tiêu: Phân tích sự sụt giảm hiệu năng khi hệ thống mắc phải hiện tượng lệch chuẩn không gian nhúng đối với các tham số Hex và IP.  
* **Remove Conditional Gate (No Entropy Switch):** Ép buộc 100% cửa sổ log chạy qua RAG-SLM thay vì sử dụng mạng Bayes chặn lọc. Mục tiêu: Ghi nhận sự sụp đổ về băng thông và sự phình to của độ trễ tính toán, chứng minh cổng điều kiện Entropy là một thiết kế bắt buộc cho tính khả thi thời gian thực.

## **18\. Evaluation Infrastructure**

Cơ sở hạ tầng đánh giá được cấu trúc để phục vụ chuyên biệt hệ thống ELAD, loại bỏ các chuẩn đo lường tĩnh không phản ánh được năng lực phát hiện sớm1.

* **Early Detection Metrics (Hệ mét Ưu tiên):** Thời gian Dẫn trước Cảnh báo (Detection Lead Time \- DLT) tính bằng phút/giờ trước sự kiện sụp đổ; Chân trời Cảnh báo Sớm (Early Warning Horizon \- EWH); Tỷ lệ Phát hiện Trước Sụp đổ (Detection Before Failure \- DBF).  
* **Detection Metrics:** Tỷ lệ Cảnh báo Giả (False Positive Rate \- FPR) được đo lường chuyên biệt trên nhóm log chưa từng thấy (OOD) nhằm định lượng hiệu năng triệt tiêu Alert Fatigue. Các chỉ số Precision, Recall, F1-Score, PR-AUC, ROC-AUC được trích xuất song song làm tham chiếu.  
* **Efficiency Metrics (Hiệu năng):** Độ trễ luồng nóng (\< 5ms) và luồng lạnh (500-1200ms) tính trên mỗi cửa sổ log. Chi phí Token Cost, tiêu thụ Memory (VRAM), và thông lượng hệ thống (Throughput)1.  
* **Generalization:** Đánh giá chéo (cross-dataset) khả năng chống Benchmark Overfitting thông qua kết quả độc lập trên BGL (môi trường phần cứng) và Thunderbird (môi trường mạng phân tán). Tập dữ liệu HDFS bị loại bỏ hoàn toàn do cấu trúc tĩnh đơn giản của nó không phù hợp để kiểm chứng hiện tượng Concept Drift1.

## **19\. Statistical / Reproducibility**

Bản chất ngẫu nhiên của thuật toán Monte Carlo Dropout và mô hình sinh ngôn ngữ tự nhiên đòi hỏi một kỷ luật thống kê (Statistical Design) khắt khe1:

* **Number of runs:** Mọi cấu hình thực nghiệm (E1-E7) phải được chạy lặp lại độc lập 10 lần.  
* **Seeds:** Giá trị seed \= 42 được áp đặt trên toàn bộ hệ thống PyTorch, NumPy và bộ sinh số của vLLM. Tham số lấy mẫu của SLM bị khóa cứng ở temperature \= 0.0 để bảo đảm đầu ra xác định (deterministic).  
* **Statistical Tests:** Báo cáo các chỉ số trung bình (Mean) kèm độ lệch chuẩn (Variance) và khoảng tin cậy 95% (Confidence Intervals). Để đánh giá sự cải thiện về DLT và FPR có ý nghĩa thống kê, kiểm định phi tham số Wilcoxon signed-rank test sẽ được áp dụng với mức ý nghĩa ![][image23].

## **20\. Deployment Scope**

Phạm vi triển khai (Deployment Scope) tuân thủ tính khả thi của một luận văn Thạc sĩ, nghiêm cấm sự lan man sang các mô hình thương mại không cần thiết:

* **Required (Bắt buộc):** Một khung kiểm thử Python mã nguồn mở, cài đặt trên máy trạm GPU cục bộ (Nvidia RTX 3090/4090 24GB VRAM). Toàn bộ pipeline từ phân tích cú pháp đến đánh giá DLT chạy qua các tệp script .py và Jupyter Notebook để xuất biểu đồ phân tích.  
* **Optional (Tùy chọn):** Một nguyên mẫu (Prototype) đóng gói qua Docker Compose bao gồm 3 container (LogOW inference, vLLM engine, ChromaDB vector store) kết nối qua FastAPI để chứng minh tính tách rời của kiến trúc trong mô phỏng truyền phát luồng dữ liệu (streaming mock).  
* **Out of Scope (Ngoài phạm vi):** Không triển khai lên môi trường Kubernetes thương mại, không phát triển Dashboard UI web, không xây dựng hạ tầng bảo mật dữ liệu đa khách hàng (multi-tenant security) hay cơ chế khắc phục lỗi hệ thống tự động (autonomous remediation).

## **21\. Non-functional Requirements**

Các yêu cầu phi chức năng (NFRs) tập trung bảo vệ giá trị nghiên cứu thay vì thương mại hóa:

* **Latency (Độ trễ):** NFR sống còn của hệ thống. Cấu trúc thực thi có điều kiện phải bảo vệ độ trễ luồng nóng (Hot path) ở mức ![][image24]ms cho 95% lưu lượng, và khống chế độ trễ luồng lạnh (Cold path) trong biên độ 500ms \- 1200ms để thỏa mãn SLAs thời gian thực của AIOps1.  
* **Reproducibility (Tính tái lập):** 100% kết quả từ tập dữ liệu công khai (BGL, Thunderbird) phải có khả năng tái tạo bởi nhà nghiên cứu độc lập thông qua tệp requirements.txt và config.yaml.  
* **Explainability (Tính diễn giải):** Cấu trúc JSON trả về từ SLM phải chứa lập luận tự nhiên minh bạch, hỗ trợ kỹ sư SOC hiểu rõ bối cảnh sự cố thay vì chỉ cấp một điểm số bất thường dạng "hộp đen".  
* **Cost & Scalability:** Việc thiết kế hệ thống tách rời và loại bỏ hoàn toàn quá trình Fine-tuning SLM giúp tiết kiệm hàng ngàn giờ huấn luyện GPU, tối ưu hóa chi phí và đảm bảo tính nhân rộng trên phần cứng phổ thông.

## **22\. Technical Risks**

Bản đồ quản trị rủi ro (Risk Mitigation) được thiết lập để dự phòng các sự cố kỹ thuật có thể đe dọa đến tính hợp lệ của luận văn1.

| Risk | Probability | Impact | Mitigation | Fallback |
| :---- | :---- | :---- | :---- | :---- |
| **Baseline Reproduction Failure:** Không lặp lại được các chỉ số FPR gốc của LogOW do xung đột thư viện phần mềm. | Low | High | Sử dụng nguyên vẹn mã nguồn từ Zenodo (DOI 10.5281/zenodo.14214083), cài đặt môi trường ảo tuân thủ thông số của tác giả2. | Tập trung đánh giá độ sụt giảm FPR tương đối (Delta) thay vì giá trị tuyệt đối. |
| **SLM Hallucination:** Tác tử AI sinh ra kết luận sai lệch, tự bịa đặt sự kiện và bỏ sót cảnh báo sớm. | Medium | High | Kỹ thuật Prompt Engineering định dạng JSON cứng; áp đặt Context-bound strictness; khóa temperature \= 0.01. | Tạm ngưng sinh ngôn ngữ, chuyển sang mô hình Rule-based parser tĩnh quét từ khóa từ tài liệu RAG. |
| **Retrieval Latency:** Độ trễ từ việc gọi API RAG-SLM phá vỡ hoàn toàn SLA thời gian thực. | High | Very High | Thiết kế Conditional Triage (Chỉ chạy RAG khi Entropy \> ![][image1]), giữ 95% traffic ở luồng nóng1. | Tăng hệ số nhân của ngưỡng ![][image1] để giảm thiểu tối đa số cuộc gọi API luồng lạnh. |
| **Context Pollution:** Cơ sở dữ liệu Vector truy xuất nhầm các tài liệu vận hành đã lỗi thời. | Medium | High | Áp dụng hàm Timestamp-decay penalty cho Vector. Cưỡng chế Strict Temporal Filter (![][image16])1. | Xóa toàn bộ bộ nhớ Vector và nạp thủ công tài liệu theo từng khoảng thời gian test. |
| **Embedding Mismatch:** Kỹ thuật Semantic search không thể hiểu cấu trúc IP hoặc mã Hex trong log. | Medium | High | Áp dụng Hybrid Search kết hợp đối sánh BM25 và Code-specific embeddings1. | Rút gọn quy trình chỉ dùng Exact Keyword Match (BM25). |

## **23\. Artifact & Reproducibility**

Để bảo vệ quyền được kiểm chứng khoa học, hệ thống tạo tác (Artifacts) sẽ được đóng gói toàn vẹn:

* data/: Script tải dữ liệu thô và cấu hình phân chia Chronological Split (BGL, Thunderbird).  
* configs/: Toàn bộ các tệp .yaml mô tả cấu hình Baseline, Improvement, SLM, và Retrieval.  
* models/: Checkpoint đã huấn luyện và đóng băng của mạng nơ-ron LogOW gốc.  
* prompts/: Template của In-context learning sử dụng cho SLM.  
* experiments/: Cơ sở dữ liệu MLflow tracking chứa metadata của 10 lần chạy lặp lại, Confusion Matrices, JSON logs từ SLM.  
* environment/: Tệp Dockerfile và requirements.txt. Mục tiêu tối thượng là: **bất kỳ nhà nghiên cứu nào cũng có thể tải artifact, nhập lệnh thực thi duy nhất và tái lập chính xác bảng so sánh giữa Baseline và Improved model**1.

## **24\. Research Execution Roadmap**

Lộ trình triển khai bám sát quỹ thời gian 6-9 tháng của một dự án Thạc sĩ, chia thành các chặng nước rút (Sprints):

* **Sprint 1 — Environment \+ Baseline:** Thiết lập môi trường Python/GPU, tải dữ liệu BGL/Thunderbird, phân chia Chronological Split, thực thi thành công Baseline LogOW.  
* **Sprint 2 — Baseline Validation:** Đánh giá các hệ mét tĩnh của LogOW, trích xuất chuỗi Entropy chứng minh điểm nghẽn Alert Fatigue (Thực nghiệm E1).  
* **Sprint 3 — Targeted Improvement:** Triển khai cơ sở dữ liệu Vector cục bộ, cấu hình Hybrid Search, cài đặt Llama-3/Qwen qua engine vLLM, thiết kế cổng Conditional Gate.  
* **Sprint 4 — Main Experiments:** Thực thi phép đối chứng trực tiếp LogOW vs LogOW+RAG (E2), thu thập log JSON và kết quả phân loại vùng biên OOD.  
* **Sprint 5 — Ablation/Robustness:** Đóng/Mở các cấu hình cắt lớp (E3), thử nghiệm với mức độ nhiễu OOD 20-40% (E5) để kiểm tra giới hạn chịu tải của hệ thống.  
* **Sprint 6 — Early Detection/Efficiency:** Chuyển đổi nhãn sự kiện sang khung thời gian thực. Đối chiếu nhãn ![][image8] để tính toán hệ mét DLT, EWH (E4). Ghi nhận Latency/Throughput (E6, E7).  
* **Sprint 7 — Final Evaluation/Artifact Freeze:** Tổng hợp dữ liệu từ 10 lần chạy ngẫu nhiên, thực hiện kiểm định Wilcoxon signed-rank, đóng gói Artifacts và hoàn thiện văn bản đặc tả nghiên cứu.

## **25\. Acceptance Criteria**

Tiêu chuẩn nghiệm thu được thiết lập minh bạch để xác thực sự hoàn thành của từng chặng nghiên cứu:

* **Baseline:** Chạy độc lập mà không báo lỗi. Các chỉ số tham chiếu (FPR trên tập tĩnh) phải được tái lập với sai số (tolerance) không quá ![][image25] so với công bố của tác giả.  
* **Improvement:** Luồng RAG-SLM tự động gọi API và sinh JSON đúng định dạng. Cổng Entropy điều hướng chính xác luồng dữ liệu (chỉ gửi các mẫu ![][image7] sang SLM) mà không làm sụp đổ luồng nơ-ron gốc. Giao diện giao tiếp giữa PyTorch và vLLM hoạt động mượt mà.  
* **Main Experiment:** Giao thức Chronological Split áp dụng chung cho cả Baseline và Improved. Bảng dữ liệu DLT và FPR thu thập đầy đủ qua 10 vòng lặp hoàn chỉnh.  
* **Reproducibility:** Môi trường ảo (Docker/Pip) chạy trên máy trạm GPU mới tái tạo lại toàn bộ bảng so sánh (Baseline vs Improved) bằng một dòng lệnh cấu hình duy nhất.

## **25A. Final Baseline Eligibility Verification**

Trước khi khóa sổ tài liệu kỹ thuật, cổng kiểm tra rào chắn cuối cùng (Final Baseline Eligibility Verification) xác nhận tính hợp lệ tuyệt đối của phương pháp cơ sở **LogOW**:

* \[x\] **Publication year:** Available online cuối 2024, xuất bản chính thức Volume 222 đầu năm 2025\. Nằm trọn vẹn trong giai đoạn 2023–2026.  
* \[x\] **Publication type:** Tạp chí khoa học (Journal article) chính thức.  
* \[x\] **Peer-reviewed:** Đã vượt qua quá trình bình duyệt học thuật.  
* \[x\] **Journal ranking:** Tạp chí *Journal of Systems and Software* thuộc phân nhóm Q1.  
* \[x\] **Ranking evidence:** Xác minh minh bạch qua SCImago/Scopus SJR 2024: 0.975; JCR Impact Factor 3.8/5.883.  
* \[x\] **Verifiability:** Công bố đi kèm DOI (10.1016/j.jss...). Hệ thống mã nguồn và 1.4GB dữ liệu thực nghiệm được lưu trữ vĩnh viễn trên Zenodo (DOI: 10.5281/zenodo.14214083)2.  
* \[x\] **Consistency:** Phương pháp cơ sở phản ánh đúng 100% nội dung đã được phê duyệt trong hồ sơ Design Freeze.  
* \[x\] **Limitation/Improvement:** Khoảng trống cô lập tri thức và giải pháp RAG hoàn toàn tuân thủ luồng đề xuất, không có sự vay mượn.

## **26\. Final Technical Design Freeze**

Bản đặc tả kỹ thuật này chốt lại **01 Technical Design duy nhất**, không tồn tại phương án phân nhánh:

* **Baseline:** LogOW (Semi-Supervised BNN, Zenodo Repo 14214083).  
* **Main Improvement:** Conditional RAG-SLM Triage Gate.  
* **Unchanged Components:** Cây phân tích Drain Parser, Semantic Embedding, BNN weights, thông số MCDropout.  
* **New/Modified Components:** Cổng điều hướng Entropy (Modified), Vector DB & Hybrid Search (New), Prompt Engine & SLM Inference cục bộ (New).  
* **Core Experiment:** Baseline tĩnh (LogOW) đối chứng trực tiếp với Improved System (LogOW \+ RAG).  
* **Primary Success Criterion:** Việc tích hợp RAG-SLM triệt tiêu FPR trên nhóm dữ liệu OOD (giải quyết Alert Fatigue).  
* **Secondary Criteria:** Duy trì DLT ở mức dương (Early Detection), bảo vệ độ trễ hệ thống tổng thể thông qua luồng kép (Efficiency), và tính bền vững trên cả hai tập BGL/Thunderbird (Generalization).

## **27\. Q1/Q2 Ranking and Publication Verification**

Cổng kiểm định xếp hạng khoa học bảo vệ tính chính danh của nền tảng nghiên cứu. Phương pháp cơ sở LogOW đã vượt qua mọi tiêu chí khắt khe1:

* **Journal:** *Journal of Systems and Software* (Nhà xuất bản Elsevier)1.  
* **Year:** 2024/2025. Nằm vững trong chu kỳ quy định 2023-2026.  
* **Ranking Source & Quartile:** Xếp hạng **Q1**. Các chỉ số xác minh bao gồm SCImago SJR 2024: 0.975, h-index: 141; JCR Impact Factor: 3.8 / 5.883.  
* **Official Publication Status:** Đã bình duyệt và xuất bản chính thức.  
* **DOI / Metadata:** DOI bài báo 10.1016/j.jss.... Mã nguồn lưu trữ với DOI vĩnh viễn: 10.5281/zenodo.142140832. Nền tảng này cung cấp một cơ sở lý luận và pháp lý không thể phản bác cho việc cấy ghép các thuật toán trí tuệ nhân tạo thế hệ mới.

## **28\. Final Traceability Matrix**

Bảng đối chiếu tổng kết thiết lập một đường ống logic kiên cố từ lý thuyết khoa học đến từng đơn vị mã nguồn, khẳng định 100% tính khả thi kỹ thuật của toàn bộ quá trình phát triển hệ thống1.

| Research Question / Hypothesis | Technical Component | Experiment | Metric | Acceptance Criterion |
| :---- | :---- | :---- | :---- | :---- |
| **RQ1:** Giới hạn của LogOW khi đối mặt Concept Drift do cập nhật CI/CD. | Baseline BNN & Thresholding Gate. | E1, E5 (Baseline Validate & Robustness). | FPR trên luồng OOD Logs. | FPR của hệ thống LogOW tăng đột biến khi luồng log gặp bản cập nhật hợp lệ. |
| **RQ2:** Khả năng phân định cảnh báo của kiến trúc RAG-SLM. | Improvement Module (SLM Triage & Prompt Engine). | E2, E3 (Main Test & Ablation). | DLT, EWH, FPR tại vùng biên. | FPR giảm 99% tại vùng biên bất định; DLT duy trì giá trị dương đáng kể. |
| **RQ3:** Tác động của tác tử RAG lên kiến trúc thời gian thực. | Dual-path Inference Workflow (Hot/Cold Path). | E6 (Efficiency). | Latency (ms), Thông lượng (Throughput). | Độ trễ luồng nóng \< 5ms; Luồng lạnh (gọi API RAG) chiếm \< 5% tổng dung lượng sự kiện. |
| **H1:** Bão hòa cảnh báo sinh ra do sự cô lập tri thức. | Retrieval Module (Cơ sở dữ liệu Vector cục bộ). | E3 (Ablation: Direct SLM vs RAG Semantic). | Context Relevance, FPR. | LLM sinh ảo giác (FPR cao) nếu vô hiệu hóa Retrieval; phục hồi hiệu năng ngay khi RAG bật. |
| **H2:** Tối ưu hóa độ trễ tính toán bằng kích hoạt có điều kiện. | Conditional Triage Gate (Dựa trên ngưỡng Entropy ![][image1]). | E6 (Efficiency). | Token Cost, VRAM Memory, Latency. | Chi phí API và RAM giảm theo cấp số nhân so với việc ép buộc 100% log chạy qua SLM. |
| **H3/H4:** Cải thiện hệ mét Cảnh báo sớm ổn định. | Temporal Data Design / Evaluation Module. | E4, E7 (Early Detection & Generalization). | DLT (tính bằng phút/giờ). | Hệ thống liên tục phát cờ cảnh báo thành công trước ![][image8] trên cả hai môi trường BGL và Thunderbird. |

#### **Works cited**

> 1.   
> 2. LogOW: A Semi-Supervised Log Anomaly Detection Model in Open, [https://zenodo.org/records/14214083](https://zenodo.org/records/14214083)  
> 3. Journal Of Systems And Software impact factor, indexing, ranking, [https://journalsearches.com/journal.php?title=journal%20of%20systems%20and%20software](https://journalsearches.com/journal.php?title=journal+of+systems+and+software)  
> 4. Journal of Systems and Software \- Impact Factor (IF), Overall, [https://www.resurchify.com/impact/details/19309](https://www.resurchify.com/impact/details/19309)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAjklEQVR4XmNgGFQgAYj/A/F+IPZDlUKAUCAOgrLfMEA0YAVTgNgWXRAbUGHAYwo6ACk8jy6IDWxkgCh2QZeAARsGiAJ9KI3VCQoMqBIwUzEASLADiW8NFZNAEmPQhgoiAxksYgyTsAiWYRFjKMUi+BiIl6OJgQFIIQeULQzlYwVMQPyCAaLgLZrcKBgIAACpGiD9CHWs0wAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAWCAYAAAAmaHdCAAAAwElEQVR4XmNgGAWEwDwg/gzE/6F4AYosBPxlQMiDsDOqNAIgK8IG9gGxCrogMmAE4u1AvJ4BYkgQqjQY4DIcDvKB2ATKxuWaP+gC6OAtEvsDA8QQPiQxNSDuROJjBcg2g/wN4t9EElsGxDxIfAwACo/NaGLoXsLmPRSwAYiZ0cRAXgFpfAflH0GSwwpw2QJzTQ4DnnQBA1/RBaDAjwHTW1gByIZmdEEkgNeQDAaIC2CKrqNKw8FsIN6PLjgKBjsAAEBxMUYUf8QDAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAaCAYAAAD1wA/qAAACSElEQVR4Xu2XT0hVQRTGT39MMtFVoO1CtFULEUmCyIUQKdSuxK2LFi0EBRE3grppIULQKrBaiTuhXS3aCRlE0KbAZYga/aFaKOSf8zFnfOedO3Pv876nLbo/+PCe75uZ++44M/c9ooL/h1bWaWsekVqMURXNrC/WzMm+NSphgfWLXGevTclOsbZM9p3VL7km180jnGPtWbNS/AcN8YZc1mQDYY01as0qWWHNWTMLzDw+6HsbCGkPCdKyvJyhHOM+JNfpjg0EZDvWFJ6w/lizRuC+fdZMA3si9vQ3yGXTNhCQzVpTaGG9IHcQaC6pa8z8kqo1n1ir1kzDL527rAFym/m26K1k5w9bl4Os3ZpMD7k1fpOSk4R6WK5fSt1dig+ZpGTfVND4M2vMaFyytMGQnbUmlfo8U9egU2rsSw/qLlV7Bin93mX4/RE6UgGy2P4AsRv1yl8/SZ5l8TQbpvZco2TbKF8p3vg6uWzGBopYX4DliPyq8lDj3aSJjYHlFssSoGGs8WtyWYMNFMixYUNgj9ixUY8YD/cJcZ+S/YP4szrv+wMgb7Om8I6S/VF3qPoRq1HVmglK9g8yT67hPRtQaVlkDYR8ypoC3va6/yupsS8BNjy+FcT4yPpgTc0i6zfrB+sb6ydrV7IL5F5w8JChzTa5oznEc3JtYzyl0oQMsS6y/kqtD4EQaHPLmscFHjzrv5YH/7XpRFlnPbBmleAAeGzN46aOajt7+GHll/qJc5my13yl/LOH8Fyh8q8eecBRXm/NgoKCo3MAz0eURLL5licAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAAAXCAYAAAD9VOo7AAACpklEQVR4Xu2ZS+hNURTGl3ceMSLMJIwMJJHyGCh5xAyZGlAGipJMFCYGUspIeYxkpow8ykyhpEwoAwPJI48wQF7ra639v9t3z77n3HNvnNPdv1r97/q+vc/77LX3+YtkMpn/wzyN8Sz2yTC2kVFmabxgsSa/WRglLmh8ErsIIV67N07jDXnvNTa7HzPMizhZ4xeLo0a44EXcEfNmsuE80zjI4oDc1TjN4qiANwEX/CEbTq+bBXp5dZkg/W13AQttZr/YyW9jw4H3jUXnnMYXFocE9ruBxQT7xNpvZaONoGaknsY1Yt5xNhx4J1l05mpcFiv4MfOj33gTrkZ5zBON+yyWsFPsmPCQtZYwJG3X2CJWtDd53HNv6ljrv4G3iEVllVgNWCfdNxv5Hv993fMVHXuMo9LdtyprxfqeYqMN4MCfahyiOOxer4sCbyKL0ulzMfoNlnmOuhVAvjzKA7uk976rsETju8YVNppKqB9FU1kAL1U/QOqCrfe/4WYHrrkW84rywErpbluXORofNW6w0TTeSvqkV4t5J9iISPUFGObgL4005FjbxKS2gWEs5fULjuW5xmPSGwdOOHXSt8S8aWxEwEdhLgI1hLeN/ABp2E8RoUAPwmyNDxq32WgiYa5fd/0B4C9k0Xkg3f2RL45yFN0ZUR5zRLr7VwX7QO3ALK81nBE74R1sSGe4Kbsg8I+x6GD1Hve/6XmYkqKwY5WfAsPLIxZLCLOr1FS8kWDG8VnsVX4nVux+ujddbKEHDR7afBWbEhdxSaxtivPSubG7xYaQH57Hxb4ItNnIYgIcH9pjgTjS4AaWvUV1CJ9zqoL1U8Z5qbGXxQFBoT/LYqYak6S/p7kM/IMqDKGZmuBra1lNqEq+GUMCnyniTyJ1wBR6CouZzD/jD5G2piUjIqfwAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAaCAYAAADWm14/AAABGUlEQVR4XmNgGAUjBLwG4g9A3AHEPGhyJANGdAEC4D+U9oGyryPJkQQcGSAGtKBLEAAwB5ANYhkghuSgSxAJQHqT0QWJAZUMEM1B6BIkApDlIHM40SVwgSlA/A+ILdAlyAQsDBAHEIyK9UD8A4iV0CUoANeAeDMQdzFAHFCDKo0AuQwQBVboEhSA50A8F4kPMv8ZEh8rKGGAKAxGlyARwOIdGRAVDTAQxQBRnI0uQSQA6b2NRewemhhBYMcA0diGLkEAgPSkYxFLRRMjGqgA8U8gnoMugQOALPNG4sNyAsVAEIj3owtiAauA+AES/zEQpyHx6QJgWQ+EI9HkBh+QZoDEGTGYWiUkChABYnMisSZUzygYBaOAKgAAeXs8Qq6YJ8EAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFcAAAAaCAYAAADCDsDeAAADIklEQVR4Xu2YSchPURjGX3PmUsaVISxkIRkiw0KZih2SHbGwUL6SKAoLFlJKGcqwkp0hFAs7hUimKAtKMmQIZcj0Ps453z3fc++59/z/9/bx+e6vnr7/+z733HPvuWf8RGpqatoyXNWVkw1SxT3+OwaqnnGySX5x4h9gt5jnOqOaTV6Qo6oPYgo6vbReF9Ur8t6qFlnfp8oG6an6ycm/yAHVBDEj6rs08a6u8bK4IsYbwIblsWojJ0tyVbWXkyW5pHqv6sZGAfck/O6FoIei8W6xYclreJDnNQsaoIr7dlfdVz1V9SYvljWqL5yMZb2YF1nChgXeV05aMGQ+cbIiUO88TkaCNQDT2w0xnacseJZDnIwBDxHqJbPEeDvYsMDbxUnLMNUJMS/qM8L7jR56yot9Hqquc7KAkarPqrOULwsWa7zrEDaKcMN+qWqxmAVrodU164WGFLyxnFSmi5kz50j6wyFebX+fs/GUxG5li6TLhpgqZhE8yEZJ1qq+qYZK0k4NgQKPVC2kTdbLuyE8zGuMK3PM+w0m2dgfqogne7FjheTX7fNRzIeqEnQ0v37slGKf5w9uvs3aXgF4ofkWhCqba/+6D+c4bXM+Lyh2TJP0tXn0Vz1X3ZRqDiKoe4EXb7W5aF5LuMAMMd5ONjxCZQGmEvgTvRxi7J19QvfAVBHy8sA8fkf1RMLTWRGu0/msysjlgotDBS6L8fqw4QE/tG/EnMv3RryBcqgni+WSLt8oF8XsbRtdiPBxuO4LGbkgbi/Z7P4WwB/DSQu2QVwe8Tgv3qPq58U+myVdvlkOi1mYRrMR4Lyk60a8jnJB9okpsIwNSYY0V8DA385JC05tfnmckBBjyAEsajjdhbirus3JkmyTuNNWX2n77DMlf+1p5aSY1fWd6o2YYfPDergpDgXIwcM1OJ1gm5bFcTHXhjgiyUdaqRosyfncX+iywDXzOdmODBLTTniOB+S1C/yFq8IdyTs92P5Ez0WRYJHbz8kcsCeNVYeih1Tby7BHddNULNgTx6rDMUqK59BYGm3YTsF4Kf8fKGzrenGypqampqaG+Q3Ncc60nTTu8gAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFcAAAAaCAYAAADCDsDeAAADE0lEQVR4Xu2YS6hNURjHP+88otT1mkkYyECSG3kMlGfMkMwIZaAo3RgoDBhIKQMpj5HMSJRHmSmUhEQZGEgeeYQB8vr+rbXOWee/99p77X13rq71q697vv9/PfZZZ6/XFUkkEp1M1BjIYkWaaKPfMUbjBYs1+c3CP8AhMc91UWMheUFOaXwSU9HFa+sN0HhD3nuNFdb3aXJAhmr8YrEPOa4xQ8yM+iE1vqsbvDxuivFGs2F5prGTxV5yS+MIi33EIwl/91LwhmLw7rFhKRp4UOTVZZBUa3cyCw2yWeMri7FsF/NFVrNhgfeNRQumzBcWGwL9LmExwDYx5Vex0RBo+wSLMWCNDb0lC8R4+9mwwDvIomWCxlkxm53PJO8z3tDzXu7zROMOiyWsE/NMeGGaBJs12h3HRhlu2q/RWClmw1pu47b1hrdKdwJvKotKt5g1c5Fkfzjkm+znSzaf07Zb7JFs3Viwo6PuYTYqskXju8Z4aY9TJVDhqcYuit3WK2oQ3mAWpV3ntPcZzLI51nkH8tle7lgvxX3HMF3M4JxjIwK8aH7/OClVeh633uYdrwC80HoLQp0ttn/dD+e4YDWfV5Q75kq2bF0wnT9qXGWjAPS9zMv3Wi2atxKuME+Md4ANj1BdgKUE/kxPQ46zs0+oDSwVIa8qeJbnGg9JD+FeOp+NOVohKByqcF2MN4IND/jYlPLAmsttI99BGvrJw21OvaFL44PGDTZKeCDZvq/kaEHcWbLu+RbAn8Ki5a5k6yOf5uXYcEZ5uU+PZOvHgj6w1uK0UofLku0b+VbSghwVU2EtG9Ke0twBA38fixbc2vz612zujknY1HC7C4EpfJ/FEtwpIXQ8jGWkdD77fCnee1pg5/wsZrq8E7PQ/7QeGsWlABo8lMHtBMe0PM6IKRvipLR/pA1ipqm7n/sbXR4os5TFAHg+lMdloinGihkntPuYvL8C/8JN4a7kseDY1C95KRXWokiwyR1j8X9kiFR7y8rAv/bcMpUQ81+psjU0ljSwOeCq6V9r64Bj3TAWE4lEIpFg/gAx08kR+bt9CgAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAaCAYAAAAXHBSTAAAB0UlEQVR4Xu2WOyxEURCGxyMSoUCIR4FSo1AhotUoxCMSFNQUKEQpEjWJRkKnUhOVQkMioVDpkHgUEu9nIl4zmTnZ2cm9d7E2dpPzJX92/plz9p7Ze869C+DxeFLBGurzB8oIaKG9ATnbQF1ALi0pAb5Tmmzgxe+bPHFiE+nIOirL5MaAm+ow+TzUrMmlJaM2gdxA8DYrQpXbZKYQdJ4ymhzghvZswVBrE+nMJHBT7bYg1KNWUMeocVPTHKJmJF6Gf77zDxC9gKiaZhrVoPx356WEROcpqhbFb+clDT2yo86Ta5g0Bzz+CfgJ+oKqknGNMmZbPOGaqpDYeZpPcZN4it+Bt6/+IU5RU5IrVvmELAFPGjJ5jb4QPd7PJXYvbEc/BDdF1BhPW941RbjagnzuQOz8FqLeJA6lC/UM/G66EtFFXiH+wg6bK0Atoo5Mjb43rKlK4+8huCntz4DvFsnWk0Z/4QTwghy61gnhTZUa/4hqVt4umnyZyf0p+oIUD0pcLb5PfDeEN5VvPMWtxmuGUavKH6g4aWibXgJv1TZULuoOtYUaAf4DvInqkTHXqHnghwHNo7GODeB5uxDbui2oW4gdAc0A6gN1AXx+PR6PxxPHF53sjmk1HmNgAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAaCAYAAADBuc72AAABf0lEQVR4Xu2WvS8EYRDGx0c0motGohClTq2/RhRCkKhIlArX4G/QqIiEyt8gao2PSBQ6FREiCvEdJER4JjMTr7k3y+3F3on9JU9u7pm73efenX1viXJy/gbr0HsFqhl88tGI50N1R7zMaCNZ0ZBGkkAHzmdOvZEVG1CD80okQQec3wItOC8zpr0Bbih+iQtQuzdrSWw+644mkpD7vlFvzJEE7feNBHqgS2jbN36TB0p32UcofdA9b/yEtPM5SOmDVnw+3n6S5pP7jyQ7xTPUEfR80EVoDTqDhtTjY79BR1qbZ7pQ71tWSb4w4XyDt6Zzre1PwQiD9kHXQS/8nNXLES8R/rVPJHvnlYrn9IXiB2iFVqBjKg+6ozWv4r2+smJBQ2JeVcyQBDB80F2tD6GloBcSC2Xe7Be3CviA41p36vsxfc8PNXb38qrzLBqTQZ0UNO3NWEYzdAdtQVMkDy2b0DDJ6PBc2uXvgl5JVrdXvVv6HK2QeegEKjo/Jyfn3/IB9FBv2i3YmawAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMsAAAAaCAYAAAAZmai5AAAFPElEQVR4Xu2aR6gkVRSGf3N2TBsRAwqKMAOKioHRjYKKARHRhSAPlRnGjGmhuDCM2RExbAxvVHQhqIg5PlERRBRRDJhmYUCdccyK2fNz7vGdPtatrp7X06/Kvh/8dNU591bXPXVj3QIKhUKhUCgUCi3kV9EG0VgoFHq5QPS36LPoqIDpmurPlOf/wLr4b/nqdJBmGztiHOr0UsrTKXwBWClyrAFNs42zrZlsbzkbuVf0SLB1GZbnlWB7CFr2rYKdNsZq3NhZ9Dt6Zyi7Q+Nxo7ORZaJzg631nCW6VHQRtFAf97p7WCLaI9jOhOY7KtgPE50YbF2GZYxYBxOpso0Dr4s2DLYHofHYItivEe0YbK3HP1h7+Gs5m6eqEqxEtZ0NcNNo7CjriCajEVruqqlmVTzGgb+iAfkO5cVoaDsnQVu4cSW0YG87m4ejRSQXjKq0XWXXaMD09IKjbeSMaBgT5kUD8h3KomhoO1WVPFf5q+AIxLSvRccY8DC07JtFR+FfOGVnjK6Ljq5xrOjmaIQuxFjAuJit4jxo2sOjY5a5VXR3RneKloruEN2e0q7KKNikU9k6GsaMR6ExmhMdXaPuQTepCOR75NO9gLxvUO7C8K41LHg/f0Sjg/6d0m8OvgD5Nh0fI/pNtHjaPRK2FO3ZULukPE1pWo88rXvWh0B72ByT0Bt+JjoC/YJR5xuUYV5rpuwNvR+/3vPw5cbl6Xg97wjMRe8UhSP9qBvL9qIjG2r/lKcp/TqUHDN51qdGw0xpcjP9GgLfENH/anQ46vIPyiDXukR09QA6QrM15gno/eSmFzeIzo7GBjDfqBvL6mIf1HcodQzyrD3nY8iNZT/R/dFYwQPQm86lvRDqr1uv+EJzsfcedNTitQ1uYp0i+lo039m5qcdPcG6Dvr9f1QCuDuo6kgWY9luar6AP8YP0a8Tr+MbifbY2ZCP1vstEX4oOTvaboDOGT0RHJ9ts8TT0HnMdymnQUZXP98Pg8zFZGzo6nQOtI+RJaJrjRc+JnhdNJVuM6YzwF2yqKji/po87+Dksr+38G8y7XTr+ydl9Gh77KUzuPkaN/+wlRxwh/FQk5vPnMZ/3sbJYYyH0HSg6VLRt+l0Z/LNJvxixklsjZ+d5sfPFemD7fldAX8iQp6B7NZuIJpJtCkMcWVhBrRCD6HpmFt4U/Qh9KCvSLys7K0PVdz5WaO7n8Jg9HvUztAcmbGzXit5JaUhsXCSejxqW8Tto78ayc2H+C3Qjjg/MEys94UhcNUL6c+aztQ7xPk7rYmPxMK584WIxjv5RwP2UHzBdP76BPmvaOQpGDhA9Bq1DfDtp+Hv39eYL0efJzlhYHTKmMMTGMmqs0Me5Y8++6N31tTQbu2MjnrcZX+k3h977+uk8liM2FvaehvfxOypOP4x4nXdRvRXQVtj5cI1B2FlOOl9sLFWwsUwEG0crfn5FuNzoFLHQNmXj9Go3aE9rQeJQyzS2N8Fj/51RLmhthHtVVumXoPd7OyvHXuGc3CK6yp1730eiZ915jMdG6N0p52jeZvz9vwFda9mU3PuWQd8+GvelX66J4reH90C/cSQctTqDTVk4DBM2lPehi3wuRI1PRS9De9WlKQ3hwo5DOoPCSsQAxgrSRthQOA2h+PKC8PMhfpX9uGihaHmyW4z4IsPn42dH5GTo4pdT1Alo+RkPTv+Yj9OcE1JasgP0PznKcNRuM6dDGzena2zonGGwA2WDoY2xMfgSgNNexoFwhLVYxZcDfJli6QqFQqFQKBQKhUKhUCgUCoVCX/4B6Q26UjfNbdQAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF4AAAAaCAYAAAA+G+sUAAAC2ElEQVR4Xu2Yu69NQRTGl3eIKDSIhD9AhERFdAoEiYpG4xGFhkZDREEh8YrgaiQXBRWVDo2IBKEgREgUHh3iLd7WZ2bFOt+dffbse457LuaXfLkz31ozd++ZvWfPHJFCoVDoOZ9U49ks/Fm2qX6onnEgAfJy9S22+ZfYr/qseqFaSLHG+MEaSzHPCAk50503Mnp3nAdOq86T97fzWrXb1T+q9rh6I7aodql2SBjAR63hFg6o5pG3WUK7leQvU60jb6jAkjmazQ5ZJOE+PZMTXja+oT31o5znSf2Tl5L2MZmT2BxCzqheqaZyYJBgeUndJ7w1bNaxXrXX1fHaoKO7zvPgKWZssphUbi84ovqqmsuBhuAev7Apwb/NZh2pAasayBR4M5B7kwPDENtArOBAJmj7hk0JPtb6bFapjrKpHJbQ2TUOJNgqIXc5B4YxayVc8yYO1IA2WFaZJg/qL9ol53aGJ6Aq77JUx5pySrrXl7FUQp/bOVABcvHNYOB/Z7OKJaqTbDr6JXR4kQNE3QS1izWlm32BORLOGcc4UAH+Pw6ZDPyHbFaRcxN1gzpGQvwGBxzt2jelW30tltDXTg7UUDUe8LImb4HqLJsJzknotCoXryji7dZ3f6HY/9+X8DahbwM7Bay3fBLEYQ1P2HHVLUnfdBNsbd/AgUz6ZOA12IESD2EtNnNNlML2tTi5VmFt7QINtJ0Ry++d73NQHkf1wWAPCJbXTkE/s1z9uqR3OgPAzfKg5uggGkvYr76T8HV/Hv9i4LBPvhJzPDZYOC+g/CTqg2pjjGHi9qnuxRzAEwW4XgdO2biu2RzogJkSruOS6rHk/bbVE2ywVruyZ7607ggsZ6IrG1xvByZzCpv/E36wULZlCUsITpJYu/ujZ4exabGO8oRYtnohA/yShw8mlhWAQX8g4QOLY7zxVHVVdUh1IuYA/Mj1VnVBfn/YyuAXCoVCoVAo9Iyfh2vkL56DrlIAAAAASUVORK5CYII=>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF4AAAAaCAYAAAA+G+sUAAAC5klEQVR4Xu2YS8hOQRjHH/dIwu5LkbKzURYu2dko38IKxYqysKEkRVYslHt8bNSHhViwslDYIIVYkEuUhcvGLff77fmbM3ne/zvnnJn383XeNL/69838n+fMmTNn3jkzn0gmk8k0zhfVaDYzg8tG1S/VUw4EQF6sfhTXdDND2Khhp+qr6qVqHsWSsYM1kmIWdBI5k4w3tPBuGQ8cU50mr5uYoHquusCBCt6otpr6J9U2U09irWqLarO4AXzYGm5hl2omeWvEXbeI/IWqFeR1A9NUn1UnOFDDfHHPaZkY8KKxF/pZP8x4ltBNXknYx8scx2aDYFlAP3dzIBIsL6HnhLeczTpWqrabOn42aOi28SyYxYx/WUwotwmWiuvfeg4kgja+sSnOv8lmHaEBKxvIEPhlIPc6B7qAdeL6towDHYK23rIpzsdaH81iVR+byj5xjV3hQADMIuT2cqBhesT1awMHBgDaw7LKpEzUP1QlxzaGGVCWh91CWSyVo9JZW7NVP1V7ONABuP9rNsX5uEcUC1RH2DT0i2vwHAeIuhdUFUtlIG1NFbccHOdAArg/DpkM/AdslhHzEHWDOkJc/BoHDFXXp/Iv2hqveqa6yIEIysYD3kE2Q8xVnWQzwClxjZblbhIXr1rfbUex/78n7teEtj3YKayW9pMgDmuYYYdUNyT80J0yXNzO7a6Ub52ZA9LeB3+gxCSsxb+5FIXw+1qcXMvw1/oOenDt5KL8wfg2B+VRVB8MzrBRAfow3dSvSnin0wYelgc1Rv7Qgf3qe3Ff9xfFXwzcd9WlIsfiBwvnBZQfF/qoWlXE8OJ2qO4UOYBfFOB6E0wR14/zqkcS97+tRvCDtcSULXOkdUfgc8aasofrmQrsYKHslyUsITPErd39hecPY9iDA5THFGVfTwEn51j9V+A/efhgYlkBGPT74j6w+32S8kR1WbVXdbjIAfgAvlOdlb8ftpTBn5WgTCaTyWQymUwtvwGrZeo8bncF4QAAAABJRU5ErkJggg==>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAaCAYAAAA9rOU8AAABWklEQVR4Xu2UTStFURSGXx8ZGMmAsZmJqfwHoiTjEzIldWNgZEjxA/ArMJWSga8YiKGPMjCQouRjwLvu2sfZZznFZe/u5Dz11N7v6p69OnvdA5SU/I0N+lGDUZEDRgsye3B3QRaUduib8WmEHnpqcuHGBiHZog0mm4Y2M2TyFrpssqBM2YA8oPg62minDWNTNC91oQnayJEt1INZaDP9tmDooXf0wBZC8oTfX9EgIjdTy7wMIGIz8tf9aV4q9Jzu0EXkm+lz+wV64uXCM12il7TD1ApZhTaTmDxFrkUeljKBrJlW5N9oL9136xfojAnyXbPfry+GoV3Lt+XeKXPzhu/XJfmct0+QNbNG97JSlfT39jlBeKfz3j6hh269Ts+yUpWozYzQW2+/gmw2mpE/dIzuuvUjHfdqm976X8gAX0GvcwbawLGrddFXek0nXZayDf3NhclLSkqC8wnQ8Fxe5N3tXAAAAABJRU5ErkJggg==>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGgAAAAaCAYAAABb9hlrAAADPUlEQVR4Xu2YWahNURjH/8YHMmTMm6FEMr2g5EGkDFHIi3Kv8cEDUqJ4EHmhyIsHQzx5ksiQFClJphDxaIpSZpnH73+/tdrrfHefffc+9zrnXK1f/btr/7+z9/3WXmt/a+8FRCKRSCRSW06J/hRQe6UrmvclS9P1tNrDZBaleHYwRqR4/5K9oh+icTZQIUdF14x3Etqnfsan18F4NaEP9AkK6QhN8I7xyVNrVIFN0Hzm2kBB0iZX2kQkaV5NOIPmM2UdNMF5xmeJ2G28atIAzWu1DeSgi+iwNaHX+2VN1NEArbWG8BbpCfYWDbRmDZgBzW+HDWQw0hrCeOh10ibdGmvUE+Ue+3pjjOinaL8N5MS/HHHitRs6QZO+aQN1ykxovvYlJw/tZSKWsBGa9GwbMIwWvRRdt4EqsQya50obKADP5xNYhOOo8aB+RP4E+FZV7QHaDM1vlg0UZCL0OrtsIAd574+lu2iUNYtS5LGfg+oN0D7obB9rAxVyDtrPXjaQg7z3x3IWrRwg/6Wdtf5sED0QXRLtROkATXLH20S3A598hs7WR6IBJpbFMdEH0SAbaCUtTcQjovWiE9C+hoTn9Re9EW0V3XPeN+hvuD7edbEvzmvp/2ZyAHpyo/E9LGm8wZ4VSAaoG0r/8QQkX+1foWsW4XeX/b4qx1XodduacMunHC+QfFK8Ek0NYuF5YZv5Lnbt76Lt0N2Xyc7jbws/QfOhs5vfPq+duA7xH9gO0OdXvacRyQAdFF1JQk348+11agVL5HtoH3nT30Fn9m9Rj+B3ngWii9DtpiWB7/szzLWfOfEecjuJcFIOd21PRQNUBCa6JThuFN1w7UOi+0moiXoboCIw52muzZLfYGKET1i5vnGABhuPE8GvoZWsfS2yUPQ8ON6DZK3pjNJk+Rp82bW5hiwPYqeDdhYsK3zdzyPuKbYVvHlhX1hhlkLLMwljnLR9g2O/DUV/aOAT3rsp0LJtt9faDL4kPIaWCS6iTPaWiw2BLpBPRKuc52Gp4DkPjZ8Fd7H5OpxHaSWqNbBkf4J+6/VEUgZZ5lke+ddzAVrizrtjDij7ypLHyuLhjgVjdkc9EolEIpFIJPJf8RdxNOL38spyMgAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQAAAAaCAYAAAApOXvdAAAChklEQVR4Xu2YywtNURTGP5QB8iohA0ZigJHyKPImRUkmUkbIBBlIlH9AEiZSBspcHilhYCSRR2Eqr5J3Xnlbn7V35/gcN+fh3Iv9q6+777fvOXedddZeZ98LJBKJRKIuJ0xfS6htnuDnGDqp6zCIVQWeBjehwGsDfufUAu+LeOtMr8RrneHwCs3TFx7wNfHJXTVqME+NApaZtoo3BR7fXvEHmo6I1zqnTH3E2wwPeLn4/U17xKvCTvj55+tEAc/VMI7Bjx8mPm8Qb0BX2aQG/CKKlvZQ00g1S3DY9Mk0SSc6sEENFLcjwvNqcfQEvwq4KmfgvW20TlSEsX1Ws1fpBw/4sk6UhOe5YboP721NwYcT49utE73KNnjAS3XiNxkATyIfaExq05yGxzdEJzqwA37MAp1oAy7NOsudu4YX8Av/E1RtRzdRPaGP1ShD1YCVWKlX4duwpmBsfLCV5TqqJXQwaiSU26Im+mceJvOK6R48yXWYic79cwy8Ereb3sGvJ6IJZTy74Ofj9mt6GJ8zXTK9N80JXtT670eW4BD8wLXiN8Vx00tU33rdgsc3TvzIYtPZMJ4MT0okn9CLpi1hPAhZxc9AtjoPhNfZKFmhK0xv4XvPp0Hsox/QzNIvYr/po2miThSwz/QGWXzPTK/hx7MKlVGmo6YH+DF+JnRhGNNnO2KVUvFz00wPwzhSOqHdZI0aNTkJr2LCytOELgpj+iNycxEm9I54s5D9WtOfuv88TNTYMF4Z3h8M75noJWG8Ed5+IvEmsEfrfxXjkbWO8/mJ/wEud148H4JzTY/g7YV7YrYKVlpM6mr4v1X8DB+cTGZsK2yBeS6YbqPZ3UoikUgkEom/im9nLbHB980FeQAAAABJRU5ErkJggg==>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFwAAAAXCAYAAACGcCj3AAABzElEQVR4Xu2XTStEYRTHj9eFhUSxlIVSskX5CEQkK4sJsSR5W1hZEj4AtsoaW5QsvMVClI2XohQpSl4K/+Pc233muDVzmWnm3p5f/eo+599Mz5yZOfe5RBaLxWIJO6vwK4CWf8JN7PKp6ebW+NQsASkl+YWb5JI09ljVmWtdyBJqdSFbWYc5qjZE0vA2VS+Ec6qWSQrgCTx3rkPBoC6AR/IfHSWwQhczQBm8h9s6CCt+8zsbqIZvcEUHYSaPpNkHOsggTSR7mtdBFBgn+XDNOlDUwTu4p4MU0kGylzEdRIlnSn6ctFJ6Gz5AspduHUSJIPO7hdLbcJd2kj2N6CDs8LEv0fwehadwC05TfMMbnfUUPDLqzAucgRewXGXJ0gA/4awOwsoCScNjqu7CI4Qb5tJHXsOLKP6fUQ93netXkpnP8Llfn++DUknyBS7rIAzwjYk3z2fvB0ee4+/0e7RwfcJYx8hr+CLc8aIf3Nfr90kVxfAWbuogKnzASWMdg/vO9RLJU59Juhvuwk/KfHSMHJ3wxljzudid1fkU39ge8p4En2Cvka0Z15YE8E3zkmT0DJM0+dDJqkieBK9gv1Nz2SB5zZmqWywWi+VvfANP/W5MPVdAlwAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHMAAAAaCAYAAACEuGN0AAADjklEQVR4Xu2ZR4hUQRCGfzOYEVG8mA6iB3MET6IIBhQDXncxgmBAEAU9iGIGRUQFAx4ET15M4MUAYlZUMBxNiAhmMcf6rW6mp/bN483uzuyM9Ac/vK6a19M11V3d7w0QiUQikUikGE6K/hShaqU16saSpgl6W3XBgc9JsNnE9U+wlZJdoh+iIdZRT46KrhnbcWhMXY2dtmbGVvF0ga7MkObQYO4YO3lqDWVgNXQ806yjSJImYtKkJUm2iuc06s7A5dBgphs7y9QOYysnNdBxLbaODLQSHbZGaH+/rBFVmsxl1iC8RXIwnUXdrbEJmAgd30brSGGANQhDof0kTdCl1lCtFCo9lcYg0U/RfuvIiD/4cZL+l7SABnjTOiqUSdDx2gNcFrJM2o7WUE2sggY4xToMA0UvRdeto0zMhY5zgXUUAe/nyi7Ed1E7pCecJ3zfx2zoPcWU/5LyEemDD+HpstzJXAMd32TrKJLR0H62W4djvOiyu24fOgxMNg+Rnj2ooGRmKT2eqShfMvdCV8Bg66gnZ6BxdrIOxwzRCWvMAJ+NKyKZ/g1J2n65UvRAdEG0DfnJHOPa60W3Azv5DF0Fj0TdjC+NY6IPoh7W0UDSJm0/5Pz+MzdES0SXkH/gsv2EyQx9I931V9f+5trc8++K1jl7jeis6CL0d6w3B6BfUGvsHpZVJsMzH7lktkV+UKOQe9vCALjHEpYk+/xaiCvQfhub8LVeIbgymTgPJ6OH97UxbY9dmaFvOHLJJNxfN0D33bHQx77w82njS2QmdKB8tnztxH2TX2Q7o51vYzy1yCXzIPKDJ/5+209TwTL9HhrjK9E70RfRb1GH4HPEJpMsgu6jjKdnYLfJ3BS0Q98w5CeT16wCniPQFfvMiS8zQn+jwveka4N2LbT8kEOieznXPyotmcXAZPoDEAkTyOtexudhMjcH7dA3AposD5PZO2jvE90P2iWFR+/nQXsncntjS+QPnI8OrPuEe968wHcquE5jHPQRKYv4jrkxmSW66q65vdjy1wd6fvBtDw9qW4N26OOEDx+FuDj6Bm0Sfp5vrXhaLhkM4DG0VK2Afvkt52OAnHlPRAudzXMOes9DY0+D/5bwESKLbJlsCJy0ftvxZfG86AX08MfDDMsz4dbDkv1JtFv0xmmL8/PswPv4GzEe/l5MIrc29s/vYZI9jIP3s8qFCyASiUQikUgkEvmP+QsMAwKnZ9ykkAAAAABJRU5ErkJggg==>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF8AAAAaCAYAAADR2YAqAAACjUlEQVR4Xu2YO2hUQRSGf5+NhW9sRSyCIpJCjIqVWCkKFmm1EisfWKQLNiIaEdEQFN/aCYoiwSJY2IqFWgiKJGogpPAFvvDt+T1z2bNn7727G931bnY++NmZf/buPXPu7JnZBSKRSCTSbtwS/apDzeYVKmPIU0vBgLtTPD+RjhSvGfCeq1K8n87bKXrvvEIzD7ryLVOhk3vgfPLSGw1mi2i/81ZC4zvu/Fmiy84rNIOiKc7bC53cVufPFB1zXqN56w3hBjS+uc7fAH1YLcMeb0AnnFZe5ogWebPB7PIG0ksiWYHKhdRyZE2uKDC2H96cDEyDTu6+H6iRKzm6JLooOi86JzojWvrnqtrhxsv4jvoBx0JvtAI90Mlt8gMF4TY0vtl+IMAytQ/6zeh0YxaelOaH9nUU5JvOo1ohAsmgWklMxmaUuZUMuX7eZzaNapOrxpE6tVwvqxnG9t2bhonGPtHr/hk8Sv5NvW8065Bf75OFQ/GYvF50U3RY9Nq8LyldG42XJP9UaJ80fjK2JrTviO6JvgR/OnRB8PeIvU9dcAPkh+9wflF4DI1vsfMtdgUfEPWG9m7R3dIQniI9+eQCSskndmyt6feHV/Z5UCGHoHmsiW2iT9CzPZ8axbr/FeU3/V+cEH1EKb43og+ib6LP5n0JPuZl0A2V1w0b/xGyk38a2cnvEo2ZPuH4aNA4KsfbBpsoJuNaaG8WjZixh8hOPlf0gOn75D83feIfeNtiE8F28ouXCX0hehL6eSv/IMpLhx3jvuP/3+JDXW36V027bWC55N/P76CHB264PM8z6Uug5XU7dNWzhLGULTDX2X9En0E35j5o8ikmPil//CzLWeh9uS9FIpFIJBKJRPAb0F/KC8c13gkAAAAASUVORK5CYII=>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAAB40lEQVR4Xu2WzytFQRTHD0UUkhI7JRbEyo+lIns7PzYiG2XByk5ZsLKyFSl/BEp2bLCgxIqnZGGlKOT3+Tb3au55c+bd917ZmE99e833nHvuzL3z5lyiQCDwn1lgPbKeWVMiprHKyrBmWeOsMdYoayRSzBtrjtXAqmQNsm6s+J9xwdqzxuesQ2uscc369ihG+lC/FXfSK40iqaHkpGLg1UpTgJwBVgerldUcCW+wQuQtstYp+aa9lJN57QeskmSoIE5JXygm5uNLGswKZW99V/3UlLLOyPxHsO8LRW6zGM33Uce6kiblX0dlh8xB0igDKdAWpPk+tHz4OAPuWNvRGAdTwWyyPlidMuBBW5Dma0ySOZxcoE6TNZ6PvKJZJlOoTwYcaAvSfA3kTkjTA/L3pZkvM2QKoa/lQluQ5rtoIZNbJQMRZdKg/OpnsUTmYhz5aXki9w3hXUpTYY3cNcAGmViP8OG9Cy8nKIaL2mQgBcPkniS8LmuMvoid4gJtxlUDbLE+KdkKq8nk4wGlYpf1wKqXgTzBTaetMXqhnHi81dqFD3zbEG3wRXgZ0vN/wZM5IdOv7K+PYkAfxo2PyPTmV8r+GBliHQsvBm/MN/FuMvH76Pc2GXaDT0A5iUAgEAgEAn5+ACVPhErrp0PeAAAAAElFTkSuQmCC>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAaCAYAAAANIPQdAAABgklEQVR4Xu2WTStFURSGXxSlJGVIKCZmMvEfZCg/QTHwF3QzYmCgTIh8ZKpMzAwNKBSlDEykfITykYmvtVt7s87qnHPPSZ17Buupt+5+373vXfuuu/e5gGEYZWaJ9Ez6FrqLzABeReY0HI0LYwH8+Z+kOZVlImwgjgrpWJsF807qFuO0emOpAy+40AFxShrRZsE0gut7Ed6298aFl8okeMGY8OpJX6Rm4dUSV9+BGO96L3MDbhFt/QDpWozLSO6fq1yw6F/v/8WlYwdcY6sO0nALTsAd7ffjXN+SoIW0kaB10hpplbRCWgbf7lkZAt+w56Qj8FnNRDiPH8Lb9N6U8MrGHrjGdh3EcY/4rv2nm0UwiBw1Jk18APs9OqhCE2k2p6oxAa7FHQVJUu0RGsCTDnVA9IGzJx3UgLCZaeH1Cj+VefCkUR14wpu06aBg3N1wo7wzcG1dyv9lC/x/9dHrDfzgD3SAO+ielVfguZcirwUz4E2FO8TV2xmZYRiGYRiGEfgBXu1ze8x+SwwAAAAASUVORK5CYII=>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEMAAAAaCAYAAADsS+FMAAABwElEQVR4Xu2XPS9EQRSGXx+NRJQaDSEaCQqdQsEv8C9E4R+oNKgkVL5JFCIhUUh8FSpKHY1GRIP4jgjhHOeyc485u3c3saOYJ3mzd94zc3f23LMzc4FIJBIpnTnSA+kj0UIqKrwjF2f1psNlpZr0qk2HFtIRZJ67KpYZ98f62Id8UShOUHiOPUjHOlU7ExWkLdI6ZHB/OvxF0Tf9I+5hz4X9AeVxFR0qLy9DpK7k2sr8mzYCYSWjHuLzp8t24mfm2rm+hQyuc7xW0qjTDomVjGH4/Xn4fRO3M68L3D51vBVSrdMOiZWMDfj9Kfh9L7xebCpP/1Uy34xoJy0bWiItQp4W72IzpGkZlhkrGQfw+xMQv0EHfLjrhevxDcaTdr6trNxYyeDq9fmTEJ+35ILcaCPhuzraSCMqFhIrGdaaMQu/78XquAOJnZFqVCwfTaSxIlUMVjK6IX7JuwmXzp42EyqRq47/hJUMhn19RnqEXf0/VJGuIEdXi2fSizYDw3OyksFV4J6HeHPgvo2O94tV0h3kfMHnCn738NFBGtRmIPj96ZJ0nugC8sSb3U7EMemJtAZJRF86HIlEIpFIJBIpO58xAIkO0kx1xAAAAABJRU5ErkJggg==>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAYAAAAVibZIAAAAU0lEQVR4XmNgGAWjYFCAvegC1AD/0AWoAWyAuAxdkBrgHBCbowsiAxMy8S0g3sdAZfAXiBnRBSkB/9EFKAUTgJgdXZBS8BtdgBrAAF1gFIwCGgIAYTgLotElupAAAAAASUVORK5CYII=>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEoAAAAaCAYAAAAQXsqGAAACl0lEQVR4Xu2YTYhOURjHH8bHWJh8lSKKjZWVRpqVJCyQLFjIhgXZWVgQq9koO2ayYMFOkZBC7BAp8hWi1MxiVvL9MRPh+c85xzzv/57zvvde6W1yfvXvvc//ee655557zj13RiSTyWQydTik+qj6qtpJuVacVP1SDaoWUg68V/WqFqgmqVao7jdUjBOeqa6b+Knqtomb8VO1xsQYsHUmDh5rb0NFm1nJRoQucR1n4M1gk8As4XPXRzzE+1WnVbso11auqt6qZnMiwkMp3hiAhyXVDNRgNjLwscwCP8xxJZaojsvYE1umuqDq/lNRncmqF6rXqqmUa0ZYCkzKtyB/g01x/lETfzfHpZmgeqxaJa7BAdVmn0ODp/xxWWaq3qjuiGu7KqkBSfkW5C+xKc6/YuIRVb/qg+qMz/eYfJSzqomqDeJOWGxyh71XhkWqYdV5TlQkNSApP4B7QD52ffivTIzddK2Jl4urmWW8Agf9710pduRcxGOwTLHT9HGiJqkBSfkW5PHKYODfZJNADQawJSh8HvFadQ5bMWoOcKImqWumfAvy19gU558wMd6fTJn2R0HR1og3RF6KMLOOcaIinyTe4diDZFCT2vXCvW338b6x9CilBirMCss273WS3wp8CX8Rt2zrsEWKfQHw8DAsPIsxSHxueP8Edvh4vvEAvJfkFcAOhUJ8nIHwYkSn6zJd3Gy8xYkS4Nq7TXzEe5Z33ttjPLyM+eFihvKfJ9zW5YgXJYzmE3/8WTWvoaI+HaoH4tqfQrkU08T1457qkbjdlD81lor7RmNWizv3orjBxCRg5oirwecBfr9Jsf0oKMZS+9f8zQxtOxul5LT738G/HMJan0u5jAFrGrveJim5TjOZTCaTGZf8BqtNtgh8KhRfAAAAAElFTkSuQmCC>

[image24]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAZCAYAAABQDyyRAAABFUlEQVR4Xu2SP0tCURjGTyaoEEkELuru92gJWp0C2/oYzX0Dib6FDk6O6iBBUwlihEJDS+UQCgX1vJwr3PNw//8ZhPODH3Kf5+B9z6tKWSz58QU78ARWYRt+Gidy5s/DhnEiIRcc+CAvvIVdeEZdIu7hD2xx4YMMkAlDuIY1LkJINUARPsMlrFAXFRlgDp/gBP4q/b2BHMN3+AAL1MVFBii5ngdO5kkdfsM+Fxki/x0Z4IYLQUpZ0R0XKTikZ9moDDCj3GC3iR4XMVko/bKyKztyspEr80UOv8EpPKAuCiulL+LmXOkBLikPRNb4CF+VeZswmvCFsi3cUBYL+Vk+4CkXPlwpfWPZpHyOzTo51xxYLJa95h9ItzcL5Hvk5wAAAABJRU5ErkJggg==>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAZCAYAAACo79dmAAABtklEQVR4Xu2VzSsFURjGX0IpComEpY2UnWRjhWRtodiwsFMKpeyU/8DGTllgp6Ts2ClsWCg7WSukJJ/P07nHfec1986Zq5DmV7/mnGfObd45H3NFMv4HI7DKhoZ+G/wG73AQnsMVc8+zBE9sGEIZHLVhDLdwGbbDCtgLTyMjRM7guuqzcLoGB+CMykqiGs7ZMAb/EO1sZITLuAU8D6rdnLtuwC6Vp6IGztswBhayKG7mps09D8fovXig2qRBSlx+T62EFftigxhYrN5Sr6pNSl5+T2ixzzaIYQdeqP6Vam/LN5bfE1rsE1yFd3BT3Cz1RUY4buChuPs8vKQJHn+OCMQekCR58j33cEj1e8SN4T5MQi9/ubjP2nWunYrQmY2DRfAlisGt0an6/A0PtW+nIrTYShtIfgUK0QKPVH9KouPHYbfqJxJS7IS4h9hxScXae/smq4MLqp9ISLGT4h7SanJmlybz7MEOk21JtNh6SX52hJBiiZ2l3ZjM0yZf/xDIsER/wxUruA38soWqZ7Ixl/HTxeuj5D9NlkIvQd7ETRApNu5HGBN3sIrBPwua+tOVkZGR8Uf5AM5VdJgAQ7DwAAAAAElFTkSuQmCC>