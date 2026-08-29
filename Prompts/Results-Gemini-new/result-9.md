# **Kế Hoạch Thực Thi, Viết Luận Văn Và Gói Xuất Bản Khoa Học: Tối Ưu Hóa Phương Pháp Phát Hiện Sớm Bất Thường Dữ Liệu Log Bằng Cơ Chế Sinh Tăng Cường Truy Xuất Có Điều Kiện**

Việc xây dựng một lộ trình nghiên cứu và phát triển phần mềm trong lĩnh vực trí tuệ nhân tạo phục vụ vận hành hệ thống (AIOps) đòi hỏi một sự kết hợp khắt khe giữa kỷ luật thực nghiệm học thuật và tiêu chuẩn kỹ thuật công nghiệp. Báo cáo chiến lược này thiết lập một khuôn khổ toàn diện—bao gồm Lộ trình Triển khai (Implementation Roadmap), Kế hoạch Viết Luận văn (Thesis Writing Plan), và Gói Xuất bản (Publication Package)—nhằm định hướng cho việc thực thi một luận văn Thạc sĩ định hướng ứng dụng tiên tiến. Trọng tâm của nghiên cứu là giải quyết hiện tượng bão hòa cảnh báo giả (Alert Fatigue) sinh ra từ sự trượt dạt khái niệm (Concept Drift) trong các môi trường tích hợp và triển khai liên tục (CI/CD).  
Nghiên cứu được neo giữ vững chắc trên một phương pháp cơ sở (baseline) đã được bình duyệt và công bố chính thức: phương pháp LogOW (A Semi-Supervised Log Anomaly Detection Model in Open-World Setting), được xuất bản trên tạp chí *Journal of Systems and Software* trong giai đoạn 2024–20251. Bằng việc tôn trọng nguyên tắc bảo toàn tính toàn vẹn của mô hình cơ sở, nghiên cứu đề xuất một sự can thiệp có mục tiêu thông qua kiến trúc Sinh tăng cường bằng truy xuất và Mô hình ngôn ngữ nhỏ thực thi có điều kiện (Conditional RAG-SLM Triage). Toàn bộ bản quy hoạch dưới đây được thiết kế nhằm đảm bảo khả năng tái lập (reproducibility), tính hợp lệ của các phép đo lường động học như Thời gian Dẫn trước Cảnh báo (Detection Lead Time \- DLT), và sự sẵn sàng cho việc đệ trình kết quả lên các nền tảng xuất bản thuộc nhóm Q1/Q2.

## **1\. Lộ Trình Triển Khai Thực Nghiệm (Implementation Roadmap)**

Lộ trình triển khai được chia thành bảy giai đoạn phát triển tuyến tính. Mỗi giai đoạn đóng vai trò như một khối xây dựng độc lập nhưng có tính phụ thuộc cao, yêu cầu hệ thống phải vượt qua các rào chắn đánh giá (acceptance criteria) nghiêm ngặt trước khi chuyển sang pha tiếp theo nhằm triệt tiêu rủi ro sai lệch kỹ thuật ở các khâu cuối3.

### **Giai đoạn 1: Môi trường và Lưu trữ Cơ sở (Phase 1 — Environment and Repository)**

Giai đoạn khởi tạo tập trung vào việc thiết lập một không gian tính toán biệt lập, đảm bảo tính bất biến của các thư viện học máy và cấu trúc hóa kho lưu trữ mã nguồn để phục vụ việc đóng gói tạo tác (Artifact) sau này. Mục tiêu cốt lõi là xây dựng một hệ sinh thái phần mềm ổn định trên hạ tầng phần cứng GPU cục bộ (như Nvidia RTX 3090 hoặc 4090 với 24GB VRAM) có khả năng hỗ trợ đồng thời mạng nơ-ron học sâu (PyTorch) và công cụ suy luận ngôn ngữ (vLLM)4. Đầu vào của giai đoạn này bao gồm các thông số môi trường từ kho lưu trữ Zenodo của tác giả LogOW gốc1. Đầu ra yêu cầu một môi trường Python ảo (Conda/Virtualenv) hoàn chỉnh, tệp requirements.txt khóa chặt phiên bản, một cấu trúc thư mục dự án tuân thủ tiêu chuẩn ICSE, và hệ thống theo dõi MLflow chạy nền. Sản phẩm bàn giao là một kho lưu trữ Git đã được thiết lập với các nhánh (branches) phân định rõ ràng. Sự phụ thuộc của pha này nằm hoàn toàn vào sự tương thích hệ thống giữa CUDA 12.1+, PyTorch 2.x, vLLM 0.4.2+, và cơ sở dữ liệu vector ChromaDB5. Tiêu chí nghiệm thu quy định rằng máy trạm phải khởi chạy thành công một luồng nạp tensor cục bộ mà không gặp lỗi tràn bộ nhớ (Out-Of-Memory) hay xung đột trình điều khiển. Rủi ro chính là sự phân mảnh phiên bản thư viện có thể làm suy giảm hiệu năng của engine suy luận, đòi hỏi việc cố định môi trường thông qua container Docker ngay từ những ngày đầu.

### **Giai đoạn 2: Dữ liệu và Tái lập Cơ sở (Phase 2 — Dataset and Baseline)**

Mục đích của giai đoạn hai là chuẩn bị các siêu dữ liệu chuỗi thời gian thực và tái lập thành công hiệu năng tĩnh của phương pháp cơ sở LogOW. Đầu vào bao gồm tập dữ liệu phần cứng BGL (khoảng 708MB thô, nén 62.9MB) và tập dữ liệu mạng phân tán Thunderbird (29.6GB thô, nén 2.0GB) được cung cấp bởi Loghub8. Đầu ra của quá trình này là các tập dữ liệu đã được làm sạch, phân tích cú pháp bằng thuật toán Drain (với độ sâu cây phân tích cố định ở mức 4), và được phân mảnh nghiêm ngặt theo kỹ thuật cắt dọc trục thời gian thực (Chronological Split)3. Sản phẩm bàn giao thiết yếu là trọng số của mạng nơ-ron Bayes (BNN) đã trải qua huấn luyện và được đóng băng (frozen weights), cùng với báo cáo tái lập tỷ lệ dương tính giả (FPR). Giai đoạn này phụ thuộc hoàn toàn vào khả năng xử lý song song khối lượng dữ liệu khổng lồ của Thunderbird trong RAM hệ thống8. Tiêu chí nghiệm thu đòi hỏi việc tái tạo lại được tỷ lệ FPR trên tập dữ liệu ngoài phân phối (OOD) với sai số cho phép xấp xỉ so với công bố gốc trên *Journal of Systems and Software*. Rủi ro chí mạng ở đây là việc sử dụng vô tình các hàm xáo trộn ngẫu nhiên (Random Shuffle) của Scikit-learn, gây ra hiện tượng rò rỉ dữ liệu tương lai (Data Leakage) và làm sụp đổ hoàn toàn tính hợp lệ nội tại của thực nghiệm3.

### **Giai đoạn 3: Tích hợp Cải thiện Nhắm mục tiêu (Phase 3 — Targeted Improvement)**

Đây là giai đoạn kiến tạo lõi công nghệ mới của luận văn: xây dựng và tích hợp mô-đun "Não bộ ngoại vi" RAG-SLM tại cổng đầu ra hậu xử lý mà không xâm lấn vào kiến trúc luồng suy luận của mạng nơ-ron gốc. Đầu vào của pha này là các chuỗi sự kiện log tạo ra mức phương sai dự đoán (Entropy) vượt ngưỡng an toàn từ LogOW, kết hợp với trọng số của mô hình ngôn ngữ Llama-3-8B-Instruct đã được lượng tử hóa theo chuẩn AWQ 4-bit để tối ưu hóa bộ nhớ VRAM5. Đầu ra bao gồm một hệ thống Tìm kiếm lai (Hybrid Search) tích hợp hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty) và cơ chế rẽ nhánh luồng dữ liệu kép (Hot/Cold path)3. Bàn giao phẩm là thư mục improvement/ chứa toàn bộ mã nguồn điều phối (orchestration) và cấu trúc System Prompt ép buộc mô hình SLM xuất kết luận dưới định dạng JSON tĩnh. Sự phụ thuộc nằm ở việc hoàn tất tái lập nền tảng ở Giai đoạn 2\. Tiêu chí nghiệm thu quy định mô-đun chỉ được phép triệu gọi API vLLM khi và chỉ khi điểm bất định Bayes phá vỡ ngưỡng động, đồng thời đảm bảo SLM sinh ra kết quả phân loại nhị phân chính xác về mặt định dạng cấu trúc mà không bị ảo giác3. Rủi ro cốt lõi là hiện tượng lệch chuẩn không gian nhúng (Embedding Mismatch) khiến bộ máy tìm kiếm ngữ nghĩa không thể bắt khớp được các tham số kỹ thuật cứng như địa chỉ IP hoặc mã lỗi thập lục phân, dẫn đến việc cung cấp ngữ cảnh sai lệch cho hệ thống sinh ngôn ngữ3.

### **Giai đoạn 4: Thực nghiệm Đối chứng (Phase 4 — Controlled Experiments)**

Mục tiêu của giai đoạn bốn là thực thi các phép đo lường động học nhằm xác minh sự sụt giảm của hiện tượng Alert Fatigue và khả năng bảo toàn Thời gian Dẫn trước Cảnh báo (DLT) trong điều kiện vận hành mô phỏng3. Đầu vào của thực nghiệm là hai hệ thống chạy song song: Hệ thống A (LogOW nguyên thủy) và Hệ thống B (LogOW tích hợp cổng phân loại Conditional RAG-SLM Triage). Đầu ra là các bộ số liệu thô về DLT, FPR, Precision, và Recall được thu thập qua 10 vòng lặp độc lập, trong đó hạt giống ngẫu nhiên (random seed) được khóa cứng ở giá trị 42 nhằm bảo vệ tính tái lập3. Sản phẩm bàn giao là một kho lưu trữ cơ sở dữ liệu nội bộ MLflow chứa toàn bộ siêu dữ liệu, dấu thời gian thực thi, cấu hình YAML, và Ma trận nhầm lẫn (Confusion Matrices) của các thực nghiệm E1, E2, E4, E7. Sự phụ thuộc rõ ràng nằm ở việc hoàn thiện thành công mô-đun cải thiện ở Giai đoạn 3\. Tiêu chí nghiệm thu bắt buộc là hệ thống phải hoàn thành trọn vẹn 10 vòng lặp trên cả hai miền dữ liệu (BGL và Thunderbird) mà không vấp phải bất kỳ lỗi sụp đổ API hay tràn bộ nhớ đồ họa nào3. Rủi ro nghiêm trọng ở pha này là việc tính toán sai lệch DLT nếu các nhãn thời gian sụp đổ vật lý (Failure timestamps) bị rò rỉ vào kho tri thức Vector, cho phép mô hình nhìn trước tương lai3.

### **Giai đoạn 5: Cắt lớp, Bền vững và Hiệu năng (Phase 5 — Ablation / Robustness / Efficiency)**

Quá trình này bóc tách tính nhân-quả của từng thay đổi kiến trúc và định lượng chính xác mức tiêu hao tài nguyên phần cứng, đáp ứng đòi hỏi khắt khe của môi trường công nghiệp. Đầu vào là các kịch bản thử nghiệm đã được sửa đổi: tắt luân phiên tính năng RAG, loại bỏ đối sánh từ khóa BM25, vô hiệu hóa cổng điều kiện Entropy (Thực nghiệm E3), và kịch bản bơm nhiễu ngoài phân phối (OOD) ở mức 20% đến 40% để thử tải (Thực nghiệm E5)3. Đầu ra là bộ dữ liệu chứng minh định lượng sự cần thiết tuyệt đối của RAG để chống lại sự ảo giác của SLM, kèm theo các thông số về Thông lượng (Throughput) và Độ trễ tính toán (Compute Latency) của luồng nóng và luồng lạnh. Sản phẩm bàn giao bao gồm các tập dữ liệu hệ mét hiệu năng (E6) và biểu đồ đường cong chịu tải của hệ thống. Giai đoạn này phụ thuộc vào sự vận hành mượt mà của hạ tầng theo dõi MLflow từ Giai đoạn 4\. Tiêu chí nghiệm thu được đặt ở mức khắt khe: độ trễ của luồng nóng (chỉ chạy nơ-ron Bayes) phải duy trì dưới 5 mili-giây trên mỗi cửa sổ trượt; luồng lạnh (gọi RAG-SLM API) phải khống chế thời gian phản hồi dưới mức 1200ms và tổng lưu lượng đi vào luồng này không được vượt quá 5% khối lượng sự kiện3. Rủi ro kỹ thuật chính là nút thắt cổ chai của băng thông PCIe khi phải chuyển giao liên tục các tensor giữa RAM hệ thống và VRAM, có thể đẩy độ trễ toàn trình vượt qua ranh giới Thỏa thuận Mức Dịch vụ (SLA) thời gian thực.

### **Giai đoạn 6: Phân tích Cuối cùng (Phase 6 — Final Analysis)**

Giai đoạn phân tích đóng vai trò lượng hóa ý nghĩa thống kê của các phát hiện khoa học và nhận diện gốc rễ của những trường hợp hệ thống đưa ra dự báo sai lầm. Đầu vào là toàn bộ khối lượng siêu dữ liệu đã được đông cứng từ Giai đoạn 4 và 5\. Đầu ra yêu cầu kết quả của phép kiểm định phi tham số Wilcoxon signed-rank test và một hệ thống phân loại nguyên nhân lỗi (Error Taxonomy) minh bạch. Sản phẩm bàn giao thiết yếu là biểu đồ mật độ phân phối DLT, biểu đồ tích lũy Tỷ lệ phát hiện trước sụp đổ (DBF), cùng với báo cáo phân tích hiệu năng tĩnh và động. Sự phụ thuộc nằm ở việc kết thúc toàn bộ các kịch bản chạy máy. Tiêu chí nghiệm thu quy định sự sụt giảm của tỷ lệ FPR trên tập dữ liệu OOD phải đạt mức ý nghĩa thống kê (p \< 0.05), và mọi lập luận giải thích phải được neo chặt vào bằng chứng thực chứng từ chuỗi dữ liệu JSON xuất ra bởi SLM. Rủi ro học thuật lớn nhất tại đây là thiên kiến xác nhận (Confirmation bias), khi nhà nghiên cứu có xu hướng vô ý chọn lọc lần chạy tốt nhất (best run) để báo cáo thay vì trung bình cộng của toàn bộ phân phối.

### **Giai đoạn 7: Đóng băng Tạo tác (Phase 7 — Artifact Freeze)**

Giai đoạn cuối cùng tập trung vào việc đóng gói toàn bộ cấu hình, kết quả và mã nguồn thành một tệp tạo tác (Artifact) duy nhất có khả năng tái lập 100%, sẵn sàng vượt qua các hội đồng bình duyệt hiện vật của IEEE/ACM. Đầu vào bao gồm các tệp mã nguồn Python, cấu hình YAML, kịch bản Jupyter Notebook dùng để vẽ biểu đồ, và kết xuất dữ liệu từ MLflow. Đầu ra là một cấu trúc thư mục chuẩn hóa theo yêu cầu xuất bản, đi kèm với tệp tài liệu reproducibility.md diễn giải cặn kẽ quy trình cài đặt. Sản phẩm bàn giao là một gói nén ZIP hoặc Tarball chứa toàn bộ Artifact, sẵn sàng đưa lên các nền tảng như Zenodo hay GitHub. Phụ thuộc vào việc hoàn tất phân tích ở Giai đoạn 6\. Tiêu chí nghiệm thu là một nhà nghiên cứu độc lập (hoặc hội đồng Artifact Evaluation) có thể khởi chạy tệp runner.sh trên một môi trường GPU cấu hình tương đương và tái tạo chính xác tuyệt đối bảng số liệu đối chứng giữa Baseline và Improved model3. Rủi ro trong khâu này là việc lập trình viên để sót mã cứng (hardcode) các đường dẫn tuyệt đối hoặc phụ thuộc ẩn vào cấu hình cá nhân của hệ điều hành, làm vỡ khả năng thực thi chéo nền tảng.

## **2\. Kế Hoạch Thời Gian Phát Triển (Development Timeline)**

Tiến trình phát triển được phân bổ hợp lý trong quỹ thời gian 9 tháng, cho phép không gian dự phòng cần thiết để xử lý các sự cố phần cứng tiềm ẩn và tinh chỉnh các phân tích hồi quy, đồng thời đảm bảo sự chuyển tiếp mượt mà giữa các khối công việc.

| Giai đoạn Thực thi (Period) | Nhiệm vụ Trọng tâm (Main Tasks) | Sản phẩm Bàn giao (Deliverables) | Ràng buộc Phụ thuộc (Dependencies) | Tiêu chí Hoàn thành (Exit Criteria) |
| :---- | :---- | :---- | :---- | :---- |
| **Tháng 1** | Thiết lập môi trường học sâu; Tải và phân mảnh dữ liệu BGL/Thunderbird; Khảo sát mã nguồn gốc LogOW. | Môi trường Python/Docker; Tập dữ liệu Chronological Split3. | Hạ tầng GPU cục bộ sẵn sàng5. | Baseline khởi chạy thành công epoch đầu tiên không sinh lỗi CUDA OOM. |
| **Tháng 2** | Tái lập Baseline LogOW; Tái tạo điểm FPR trên tập OOD (Thực nghiệm E1). | Báo cáo tái lập baseline; Checkpoint trọng số BNN đóng băng. | Hoàn thành tiền xử lý dữ liệu (Drain depth=4). | Tái lập FPR sát với công bố gốc trên *Journal of Systems and Software*3. |
| **Tháng 3** | Phát triển cổng Triage Gate; Cài đặt ChromaDB; Khởi chạy vLLM với Llama-3 4-bit AWQ. | Lớp truy xuất Hybrid Search; Pipeline sinh In-context Prompt3. | Trọng số baseline đã đóng băng. | SLM sinh ra JSON hợp lệ; RAG không truy xuất tài liệu tương lai (Time-decay hoạt động). |
| **Tháng 4** | Thực thi phép đối chứng E2 (LogOW vs LogOW+RAG) và E4 (Đánh giá Cảnh báo Sớm DLT). | Bảng kết quả FPR giảm thiểu; Biểu đồ thời gian DLT3. | Hoàn thiện tích hợp RAG-SLM tại luồng lạnh. | Hoàn thành 10 lần lặp với hạt giống seed=42; DLT có giá trị dương. |
| **Tháng 5** | Tiến hành thử nghiệm cắt lớp (Ablation \- E3), Kiểm tra bền vững (E5), Đánh giá độ trễ và thông lượng (E6). | Số liệu Compute Latency; Ma trận nhầm lẫn cho SLM Hallucination3. | MLflow tracking API vận hành ổn định. | Độ trễ luồng nóng \< 5ms; Luồng RAG \< 1200ms; lưu lượng lạnh \< 5%3. |
| **Tháng 6** | Thống kê kiểm định Wilcoxon; Phân tích lỗi (Error Analysis); Hoàn thành Thực nghiệm E7 (Thunderbird). | Bảng phân tích ý nghĩa thống kê (p-value, 95% CI); Error Taxonomy. | Hoàn tất toàn bộ quy trình chạy máy. | Mọi so sánh hiệu năng được hỗ trợ bởi bằng chứng thống kê. |
| **Tháng 7** | Viết bản thảo luận văn Thạc sĩ (Từ Tổng quan tài liệu đến Phân tích kết quả). | Bản thảo luận văn đầy đủ (Full Draft) bám sát các RQ và Hypotheses. | Biểu đồ và bảng số liệu đã hoàn chỉnh. | Các chương có tính liên kết nhân-quả chặt chẽ. |
| **Tháng 8-9** | Đóng gói Artifact; Biên soạn bài báo khoa học mục tiêu Q1/Q2; Rà soát tính tái lập. | Gói Artifact nén; Bài báo định dạng IEEE/ACM; reproducibility.md. | Bản thảo luận văn được Hội đồng duyệt sơ bộ. | Kho lưu trữ Artifact độc lập có thể tái lập kết quả qua một lệnh duy nhất. |

## **3\. Quy Hoạch Tài Nguyên (Resource Planning)**

Tính khả thi của luận văn phụ thuộc lớn vào việc hoạch định các giới hạn tài nguyên tính toán. Việc triển khai các mô hình ngôn ngữ thế hệ mới cùng cơ sở dữ liệu vector đòi hỏi sự thấu hiểu sâu sắc về kiến trúc phần cứng.  
Sức mạnh phần cứng (Hardware) yêu cầu trang bị tối thiểu một Đơn vị Xử lý Đồ họa (GPU) cấp độ trung tâm dữ liệu hoặc máy trạm cao cấp, điển hình như Nvidia RTX 3090 hoặc RTX 4090 với dung lượng bộ nhớ VRAM đạt 24GB4. Lựa chọn mô hình nền tảng Llama-3-8B-Instruct khi áp dụng kỹ thuật lượng tử hóa AWQ 4-bit sẽ yêu cầu một cấu hình VRAM cơ sở (Weights footprint) khoảng 4.8GB đến 6GB5. Sự tối giản này cho phép hệ thống phân bổ phần không gian VRAM còn lại (khoảng 18GB) cho hệ thống quản lý bộ nhớ đệm dạng trang (KV Cache) của vLLM và đồ thị tính toán của mạng nơ-ron học sâu PyTorch (LogOW), giúp duy trì hiệu năng của luồng kép trên một thiết bị GPU duy nhất5. Về năng lực CPU và System RAM, bộ vi xử lý đa luồng kết hợp tối thiểu 64GB RAM chuẩn DDR4/DDR5 là yêu cầu bắt buộc để hấp thụ và tải tập dữ liệu Thunderbird thô có kích thước lên đến 29.6GB9. Việc thiếu hụt dung lượng RAM hệ thống sẽ đẩy quá trình nạp dữ liệu vào phân vùng trao đổi (swap space), làm suy sụp hoàn toàn thông lượng xử lý. Tài nguyên lưu trữ yêu cầu một ổ cứng NVMe SSD dung lượng từ 1TB trở lên nhằm triệt tiêu điểm nghẽn truy xuất khi cơ sở dữ liệu ChromaDB đọc/ghi liên tục hàng vạn bản ghi vector trong pha chạy thực nghiệm.  
Ngăn xếp phần mềm (Software) phục vụ luận văn bao gồm một loạt các công cụ mã nguồn mở được tối ưu hóa. Lớp hệ điều hành dựa trên Ubuntu 22.04 LTS kết hợp Docker CE để đảm bảo sự liền mạch về môi trường. Hệ sinh thái học sâu hoạt động trên hạt nhân PyTorch 2.x, tích hợp CUDA 12.1+ để kích hoạt tập lệnh Tensor Cores. Tác tử sinh ngôn ngữ được vận hành độc quyền qua vLLM (phiên bản 0.4.x), một engine suy luận hiệu suất cao sử dụng PagedAttention và gom nhóm liên tục (continuous batching) nhằm ép độ trễ xuống ngưỡng chấp nhận được5. Khối não bộ ngoại vi sử dụng ChromaDB cho Vector Store và LangChain để cấu trúc hóa luồng truy xuất, trong khi MLflow gánh vác toàn bộ nghiệp vụ theo dõi siêu tham số và lưu vết hệ mét thực nghiệm.  
Tài nguyên nhân lực (Human Resources) được giới hạn ở quy mô nghiên cứu hàn lâm. Một nghiên cứu viên chính (sinh viên Thạc sĩ) đóng vai trò kỹ sư AI toàn full-stack, đảm nhận việc phát triển đường ống luồng dữ liệu, lập trình tích hợp, cấu hình Prompt Engineering và thực thi phân tích thống kê. Trách nhiệm của Giáo sư Hướng dẫn là cung cấp định hướng phương pháp luận về lý thuyết bất định Bayes, phê duyệt cấu trúc chia tách thời gian thực, và đảm bảo sự vững chắc học thuật của bản thảo khoa học trước khi đệ trình lên các tạp chí Q1.  
Nút thắt cổ chai nguy hiểm nhất trong kiến trúc này nằm ở giới hạn VRAM (VRAM Bottleneck) khi luồng lạnh kích hoạt dồn dập5. Nếu mạng nơ-ron cơ sở xác định một loạt các sự kiện log đều "bất định", engine vLLM sẽ bị tràn bộ nhớ nếu không có cơ chế quản lý hàng đợi. Việc giải quyết rủi ro này phụ thuộc vào việc tinh chỉnh hệ số ngưỡng của cổng điều kiện, ép buộc giới hạn luồng RAG ở mức dưới 5% tổng lưu lượng sự kiện3. Đáng chú ý, dự án triệt tiêu hoàn toàn chi phí hàm API trả phí (API Cost) bằng cách tận dụng hoàn toàn các mô hình cục bộ mã nguồn mở, bảo vệ quyền riêng tư tuyệt đối cho hệ thống dữ liệu IT telemetry và duy trì mức chi phí duy nhất ở hao mòn phần cứng.

## **4\. Kế Hoạch Quản Trị Rủi Ro (Risk Management)**

Triển khai trí tuệ nhân tạo tạo sinh vào hệ thống vòng kín thời gian thực tiềm ẩn những điểm nứt vỡ cấu trúc. Quản trị rủi ro khoa học không chỉ vạch ra kế hoạch dự phòng mà còn quy định rõ nguyên tắc bất biến: Mọi phương án thoái lui (Fallback) chỉ được phép thu hẹp phạm vi giải quyết vấn đề trong cùng một hướng nghiên cứu, nghiêm cấm việc chuyển hướng sang một chủ đề hoàn toàn mới.

| Phân Loại (Risk Type) | Bối cảnh Rủi ro (Risk Description) | Xác suất (Prob.) | Tác động (Impact) | Chiến lược Giảm thiểu (Mitigation) | Phương án Dự phòng (Fallback) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Nghiên cứu (Research)** | **Improvement không tạo Gain:** Sự cấy ghép RAG-SLM không làm giảm thiểu tỷ lệ FPR trên tập dữ liệu ngoài phân phối hoặc khiến hệ mét DLT sụp đổ3. | Thấp | Rất Cao | Đảm bảo tính tươi mới và chất lượng của tài liệu Git commits. Khóa cứng tham số sinh ngôn ngữ (temperature=0.0) nhằm định hướng SLM suy luận tuyến tính, không bịa đặt3. | Báo cáo chân thực giới hạn của năng lực SLM. Chuyển hướng phân tích học thuật sang việc lý giải sự thất bại của LLM trong việc nắm bắt mã nguồn. |
| **Dữ liệu (Data)** | **Rò rỉ Dữ liệu Tương lai (Future Data Leakage):** Kỹ thuật xáo trộn ngẫu nhiên (Random Shuffle) vô tình được áp dụng, làm ô nhiễm tập huấn luyện, sinh ra ảo giác dự báo F1-Score3. | Trung bình | Rất Cao | Thiết lập kỷ luật phân mảnh dữ liệu bằng kỹ thuật Chronological Split (cắt dọc trục thời gian) ở cấp độ lõi của Data Loader3. | Xóa bỏ toàn bộ bộ nhớ đệm (cache). Rà soát lại log chia tập dữ liệu và thực hiện quá trình chạy lại từ điểm xuất phát (Zero). |
| **Kỹ thuật (Engineering)** | **Độ trễ Truy xuất API (Retrieval Latency):** Thời gian chờ từ vLLM phá vỡ thỏa thuận SLA dưới 1200ms của nền tảng AIOps, làm hỏng giá trị vận hành thực tiễn. | Cao | Cao | Thiết lập kiến trúc Dual-path Inference. Luồng RAG chỉ được phép đánh thức khi Entropy Bayes thực sự bứt phá qua ngưỡng động \!\[image1\]3. | Tăng hệ số nhân của ngưỡng cắt động (Triage Threshold Multiplier) để ép giảm tần suất gọi SLM, ưu tiên tốc độ hơn độ chính xác. |
| **RAG / Foundation Model** | **Ô nhiễm Ngữ cảnh (Context Pollution) & Lệch chuẩn Không gian nhúng:** Cơ sở dữ liệu Vector nạp các tài liệu đã lỗi thời hoặc không bắt khớp được mã lỗi thập lục phân/IP3. | Trung bình | Cao | Tích hợp thuật toán Tìm kiếm lai (Hybrid Search) kết hợp BM25. Bổ sung hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty)3. | Tinh giản quy trình truy xuất, chỉ sử dụng đối sánh từ khóa chính xác (Exact Keyword Match \- BM25) để tìm kiếm tĩnh trên Runbooks. |
| **RAG / Foundation Model** | **Ảo giác Mô hình (Hallucination):** Tác tử SLM đưa ra kết luận JSON sai định dạng cấu trúc hoặc hư cấu một nguyên nhân lỗi phi logic. | Trung bình | Cao | Vận dụng In-context Prompting cực kỳ nghiêm ngặt; áp đặt cấu trúc JSON schema cứng trong luồng chỉ thị của hệ thống. | Kích hoạt cơ chế "Fail-safe", tự động bỏ qua kết luận của SLM và thoái lui về quyết định cảnh báo Anomaly mặc định của baseline BNN3. |

## **5\. Kế Hoạch Viết Luận Văn (Thesis Writing Plan)**

Bản thảo luận văn Thạc sĩ sẽ được cấu trúc hóa theo một trình tự logic tuyến tính, minh bạch hóa mối quan hệ nhân-quả giữa vấn đề công nghiệp phát hiện được và giải pháp công nghệ đề xuất. Kế hoạch viết cam kết không tự ý tạo thêm khoảng trống nghiên cứu (Research Gap) mới ngoài các giới hạn đã được xác nhận của phương pháp cơ sở.  
**Chương 1 — Introduction (Giới thiệu):** Chương mở đầu đóng vai trò thiết lập khung bối cảnh. Mục tiêu là xác định rõ vấn đề bão hòa cảnh báo giả (Alert Fatigue) trong các hệ thống giám sát AIOps khi môi trường vi dịch vụ mở rộng (Concept Drift). Nội dung cốt lõi sẽ trình bày động lực nghiên cứu (Motivation) xuất phát từ sự quá tải của kỹ sư vận hành. Phạm vi nghiên cứu (Scope) được khoanh vùng nghiêm ngặt ở các dữ liệu log chuỗi thời gian. Chương này sẽ phát biểu 3 câu hỏi nghiên cứu (RQs) và tuyên bố rõ đóng góp khoa học (Contribution). Tiêu chí hoàn thành của chương là thuyết phục được người đọc hiểu rõ vì sao việc đánh giá điểm F1 tĩnh là một sai lầm, và vì sao Cảnh báo Sớm (ELAD) là một yêu cầu bắt buộc của ngành công nghiệp.  
**Chương 2 — Literature Review (Tổng quan Tài liệu):** Dựa trên kết quả từ Hệ thống Ánh xạ Tài liệu (result-1.md) và Phân tích Phê phán (result-2.md), chương này sẽ phân tích hệ thống tài liệu Q1/Q2 từ 2023 đến 2026\. Trọng tâm của chương là giới thiệu chi tiết phương pháp cơ sở LogOW1 và mổ xẻ cơ chế đo lường độ bất định thông qua xấp xỉ Bayes. Phần quan trọng nhất là cung cấp bằng chứng thực nghiệm về giới hạn đã được xác nhận (Confirmed Limitation) của LogOW: sự cô lập tri thức ngoại vi dẫn đến việc mô hình không thể phân định một bản cập nhật hệ thống hợp lệ3. Tiêu chí hoàn thành đòi hỏi một lập luận chặt chẽ về sự chuyển tiếp bắt buộc từ mô hình thế giới đóng sang thế giới mở, chứng minh rằng sự thiếu hụt bối cảnh là điểm mù hệ thống của mọi mô hình học sâu hiện đại.  
**Chương 3 — Research Methodology (Phương pháp Nghiên cứu):** Được trích xuất từ Thiết kế Nghiên cứu (result-5.md) và Giao thức Thực nghiệm (result-8.md), chương ba trình bày chi tiết phương pháp luận. Nội dung bao gồm việc phát biểu các giả thuyết nghiên cứu (Hypotheses H1-H3) và đặc tả phương pháp luận định lượng động học thông qua các hệ mét Thời gian Dẫn trước (DLT) và Chân trời Cảnh báo (EWH). Chương này cũng thiết lập và giải thích nguyên lý của giao thức phân mảnh dữ liệu Chronological Split nhằm chặn đứng hiện tượng rò rỉ dữ liệu3. Các biểu đồ dòng thời gian mô tả sự khác biệt toán học giữa \!\[![][image1]\] và \!\[![][image2]\] là yêu cầu bắt buộc để vượt qua tiêu chí nghiệm thu của chương.  
**Chương 4 — System and Software Design (Thiết kế Kiến trúc Phần mềm):** Dành riêng cho việc minh họa sự tinh xảo trong kỹ thuật phần mềm, chương bốn mô tả kiến trúc đường ống lai (Hybrid Pipeline) (result-6.md, result-7.md). Nội dung sẽ đi sâu vào cơ chế vận hành của luồng nóng (LogOW BNN) kết hợp với luồng lạnh (Conditional RAG-SLM Triage). Nó sẽ công bố các bảng tham số thiết lập môi trường ChromaDB, vLLM, cấu hình lượng tử hóa AWQ 4-bit, và các quy tắc Prompt Engineering được thiết kế để bảo vệ tính xác định của SLM3. Sơ đồ khối (Block Diagram) mô tả ranh giới hệ thống và Lưu đồ thuật toán (Flowchart) quá trình rẽ nhánh điều kiện Entropy là các thành phần minh họa không thể thiếu.  
**Chương 5 — Experiments and Results (Thực nghiệm và Kết quả):** Đây là trái tim thực chứng của luận văn, tổng hợp dữ liệu từ 7 kịch bản E1-E7. Nội dung bắt đầu bằng việc báo cáo kết quả tái lập mạng LogOW. Tiếp đó, phân tích đối chứng chính diện (Baseline vs Improved) sẽ trình bày sự sụt giảm mạnh mẽ của tỷ lệ FPR tại vùng biên, đồng thời phân tích hiệu quả cắt lớp (Ablation), khả năng bảo vệ vững chắc hệ mét DLT, và thống kê mức tiêu hao hiệu năng (Latency/Throughput). Biểu đồ mật độ phân phối DLT, Bảng so sánh FPR trên luồng OOD, Biểu đồ phân bổ VRAM, và Ma trận thống kê Wilcoxon signed-rank test (p-value, 95% CI) sẽ được trình bày trực quan thông qua các định dạng bảng chuẩn Markdown3.  
**Chương 6 — Discussion, Conclusion and Future Work (Bàn luận và Kết luận):** Chương cuối cùng tổng kết các kết quả thông qua việc trả lời trực tiếp các câu hỏi nghiên cứu (RQs). Nó sẽ phân định rõ ràng các giả thuyết được ủng hộ (Supported) hoặc bác bỏ. Hoạt động phân tích lỗi (Error Analysis) sẽ mổ xẻ nguyên nhân hiện tượng ảo giác của SLM hoặc sự chệch hướng của không gian nhúng. Chương này cũng trình bày một cách trung thực các mối đe dọa đến tính hợp lệ (Threats to Validity) và đề xuất các hướng nghiên cứu xa hơn về tối ưu hóa độ trễ API. Tiêu chí hoàn thành cốt lõi là không phóng đại mức độ đóng phá (novelty), khẳng định rõ đề tài là một "cải thiện nhắm mục tiêu" (targeted improvement) nhằm giải quyết dứt điểm điểm nghẽn Alert Fatigue.

## **6\. Sơ Đồ Đóng Góp Luận Văn (Thesis Contribution Mapping)**

Mỗi tuyên bố về đóng góp khoa học hoặc kỹ thuật trong luận văn phải được đối chiếu trực tiếp với một quy trình thực nghiệm tạo ra bằng chứng định lượng, đảm bảo tính chặt chẽ của lập luận3.

| Đóng góp (Contribution) | Bằng chứng (Evidence) | Thực nghiệm (Experiment) | Chương Luận văn (Thesis Chapter) | Trạng thái (Status) |
| :---- | :---- | :---- | :---- | :---- |
| **Baseline reproduction** (Methodological) | Tái tạo thành công các điểm số tĩnh F1 và tỷ lệ FPR nguyên thủy của mạng học sâu LogOW trên tập dữ liệu kiểm chứng. | E1 (Reproduction) | Chapter 5 | Pending |
| **Limitation evidence** (Scientific) | Sự tăng vọt của chỉ số FPR khi mạng nơ-ron Bayes bị thử thách với luồng log chứa bản cập nhật CI/CD. | E1, E5 (Robustness) | Chapter 2, Chapter 5 | Pending |
| **Targeted improvement** (Engineering) | Xây dựng thành công kiến trúc phân giải RAG-SLM điều hướng luồng dữ liệu kép (Hot/Cold Path) tích hợp qua engine vLLM. | E2, E6 (Efficiency) | Chapter 4 | Pending |
| **Early detection gain** (Scientific/Industrial) | Chỉ số DLT duy trì mức dương vững chắc; FPR sụt giảm đáng kể (kỳ vọng 99%) tại các vùng biên phân phối thế giới mở. | E3 (Early Detection), E2 | Chapter 5 | Pending |
| **Robustness/efficiency** (Industrial) | Hệ thống bảo toàn thông lượng cao, sự kiện đi vào luồng lạnh (API RAG) bị khống chế dưới 5% tổng lưu lượng sự kiện. | E6 (Efficiency), E5 | Chapter 5 | Pending |
| **Reproducibility artifact** (Engineering) | Một kho lưu trữ nguyên vẹn chứa mã nguồn, siêu tham số YAML, và lịch sử thực thi MLflow được đóng băng vĩnh viễn. | Tích hợp Artifact | Chapter 4, Appendix | Pending |

## **7\. Kế Hoạch Xuất Bản Khoa Học (Publication Plan)**

Chiến lược xuất bản tuân thủ một nguyên tắc học thuật minh bạch: Luận văn không sử dụng danh xưng "completely new method" (phương pháp hoàn toàn mới). Bài báo khoa học sẽ tập trung vinh danh đóng góp cải thiện có mục tiêu (**Targeted RAG improvement contribution**) trên nền tảng một phương pháp cơ sở hiện hữu thuộc nhóm Q1 (**Existing Q1 baseline contribution**).  
Mặc dù phương pháp cơ sở LogOW đã được xác nhận qua tạp chí *Journal of Systems and Software* (Q1)2, đích đến của bài báo mới sẽ được đánh giá độc lập dựa trên chất lượng của khối lượng thực chứng sinh ra từ dự án. Việc sở hữu một baseline Q1 không đồng nghĩa với việc nghiễm nhiên được xuất bản ở Q1 nếu bằng chứng thực nghiệm không đủ mạnh.

| Tạp chí Đích (Target Venue) | Mức độ Phù hợp (Fit) | Bằng chứng Bắt buộc (Required Evidence) | Lợi thế Cốt lõi (Main Strength) | Rủi ro Chính (Main Risk) | Mức độ Ưu tiên (Priority) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ACM TOSEM** (Q1, SJR 1.59)13 | Rất Cao (Tập trung sâu vào phương pháp luận và kỹ thuật phần mềm). | Khung thực nghiệm ELAD động học nghiêm ngặt, kiểm định Wilcoxon, và các thử nghiệm cắt lớp (Ablation) cực sâu. | Đề cao tính chặt chẽ của Chronological Split và giải pháp cụ thể cho Concept Drift. | Yêu cầu sự đối sánh chéo đa phương pháp vô cùng khắt khe, khó thỏa mãn trong 6 tháng. | **1 (Cao)** |
| **IEEE TSE** (Q1, IF 7.09)14 | Cao (Ứng dụng Kỹ thuật Phần mềm trong môi trường thực tiễn). | Bằng chứng rõ ràng về độ trễ (Latency), chi phí Token/VRAM, và tính năng mở rộng hệ thống. | Quan tâm đặc biệt đến kiến trúc phần mềm lai (Hot/Cold Path) áp dụng trong vận hành AIOps. | Có thể bị từ chối nếu độ trễ sinh ngôn ngữ của SLM phá vỡ SLA thời gian thực của nền tảng. | **2 (Cao)** |
| **J. Systems & Software** (Q1, SJR 0.95)2 | Cao (Tạp chí gốc từng công bố Baseline LogOW). | Chứng minh được sự ưu việt trực tiếp của kiến trúc RAG so với LogOW tĩnh. | Sự quen thuộc của phản biện với baseline LogOW giúp quá trình review đi thẳng vào trọng tâm cải tiến. | Có thể bị đánh giá là một công trình kế thừa nhỏ (incremental work) nếu tỷ lệ FPR giảm không ấn tượng. | **3 (Trung bình)** |

*Chiến lược cốt lõi của bài báo:* Kế thừa LogOW \+ Chứng minh Alert Fatigue \+ Can thiệp Conditional RAG-SLM Triage \+ Cung cấp Bằng chứng DLT/FPR có kiểm soát.

## **8\. Cấu Trúc Gói Tạo Tác (Artifact Package)**

Nhằm đảm bảo sự tuân thủ các tiêu chuẩn đánh giá Artifact của ICSE, cấu trúc thư mục của dự án được thiết kế chuẩn hóa và bắt buộc phải công khai trên nền tảng lưu trữ vĩnh viễn (ngoại trừ các siêu dữ liệu bị ràng buộc bởi thỏa thuận NDA của doanh nghiệp).  
artifact/ ├── README.md \# Tài liệu hướng dẫn khởi chạy toàn tập hệ thống ├── configs/ \# Tệp YAML: baseline.yaml, model.yaml, retrieval.yaml ├── data\_reference/ \# Script tải BGL/Thunderbird và module Chronological Split ├── baseline/ \# Mã nguồn đóng băng của LogOW (Inherited Code) ├── improvement/ \# Mã nguồn cổng Triage Gate và RAG-SLM adapter ├── prompts/ \# Tệp lưu trữ In-context learning schema cho Llama-3/Qwen ├── scripts/ \# Bash scripts tự động hóa runner: run\_e1.sh, run\_e2.sh... ├── experiments/ \# Cơ sở dữ liệu nội bộ của MLflow (Tracking) ├── results/ \# Các tệp CSV thô chứa nhãn thời gian T\_alert và T\_failure ├── figures/ \# Biểu đồ DLT, ROC-AUC xuất tự động từ Jupyter ├── logs/ \# JSON outputs từ hệ thống sinh ngôn ngữ tự nhiên ├── tests/ \# Unit tests cho Drain Parser và Cosine Similarity ├── docs/ \# Tài liệu thiết kế kiến trúc phần mềm └── reproducibility.md \# Danh sách kiểm tra môi trường và thông số phần cứng Artifact này phải có khả năng hỗ trợ nhà nghiên cứu tái lập chính xác mô hình LogOW tĩnh, quy trình tích hợp mô-đun RAG, và tạo ra chuỗi kết quả đánh giá cho các kịch bản thực nghiệm đối chứng, cắt lớp, và tổng hợp số liệu. Yêu cầu kiểm tra bao gồm việc khóa cứng phiên bản hệ điều hành, cấu trúc phân chia dữ liệu, và siêu tham số mạng. Mục đích là đáp ứng trọn vẹn tiêu chuẩn "reproduced" và "documented" của hội đồng đánh giá phần mềm.

## **9\. Danh Sách Kiểm Tra Khả Năng Tái Lập (Reproducibility Checklist)**

Một công bố khoa học hướng tới mục tiêu Q1/Q2 yêu cầu sự minh bạch tuyệt đối về cấu hình môi trường thực thi. Các yếu tố sau phải được khóa cứng và kiểm chứng.

* **Dataset Versioning:** Sử dụng mã băm (MD5 Hash) cho tệp nén BGL (62.9MB) và Thunderbird (29.6GB) từ kho Loghub8.  
* **Data Split Protocol:** Đảm bảo 100% việc tuân thủ Chronological Split (cắt dọc trục thời gian, cấm hoàn toàn Random Shuffle) để ngăn chặn rò rỉ dữ liệu3.  
* **Baseline Code/Version:** Ghi nhận chính xác thẻ cam kết (commit tag) của LogOW trên kho Zenodo (DOI: 10.5281/zenodo.14214083)1.  
* **Model Versioning:** Cố định siêu dữ liệu của SLM chạy cục bộ (ví dụ: Meta-Llama-3-8B-Instruct-AWQ-4bit thông qua engine vLLM)5.  
* **Retrieval Settings:** Lưu vết kích thước phân mảnh (chunk\_size=512), số tài liệu truy xuất (top\_k=3), và áp đặt hàm suy giảm theo thời gian (Timestamp-decay penalty)3.  
* **Random Seed:** Tham số khởi tạo ngẫu nhiên bị khóa chặt (seed=42) cho toàn bộ môi trường PyTorch, NumPy, và quá trình lấy mẫu LLM.  
* **LLM Determinism:** Khóa cứng nhiệt độ sinh ngôn ngữ (temperature=0.0, top\_p=1.0) nhằm triệt tiêu sự thay đổi kết quả3.  
* **Environment Dependencies:** Sử dụng tệp requirements.txt và Dockerfile để khóa chặt phiên bản của PyTorch, CUDA, vLLM, và ChromaDB.

## **10\. Danh Sách Kiểm Tra Hoàn Thành Thực Nghiệm (Experiment Completion Checklist)**

Mọi kịch bản thử nghiệm đã được phê duyệt tại tài liệu thiết kế giao thức thực nghiệm bắt buộc phải được hoàn thành qua 10 vòng lặp độc lập để triệt tiêu sai số ngẫu nhiên.

* **E1 (Baseline Reproduction):** Đã chạy thành công LogOW tĩnh, tái lập F1-Score và ghi nhận tình trạng FPR cao đột biến do Concept Drift.  
* **E2 (Main Comparison):** Đã đối chiếu hiệu năng LogOW với LogOW+RAG, xác nhận FPR giảm mạnh tại vùng biên mà không làm sụp đổ chỉ số Recall tổng thể.  
* **E3 (Ablation):** Đã hoàn tất các phép thử cắt lớp: (a) SLM không RAG (chứng minh Hallucination), (b) Không sử dụng Hybrid Search (chứng minh Embedding Mismatch), (c) Hủy bỏ cổng Entropy (chứng minh rào cản độ trễ).  
* **E4 (Early Detection):** Đã trích xuất và xuất xưởng biểu đồ phân phối Thời gian Dẫn trước (DLT) có giá trị dương ổn định.  
* **E5 (Robustness):** Đã ép hệ thống vận hành dưới áp lực 40% dữ liệu OOD nhân tạo, kiểm tra khả năng sống sót qua rủi ro CUDA OOM.  
* **E6 (Efficiency):** Đã xuất báo cáo độ trễ (Latency) cho luồng nóng (\< 5ms) và luồng lạnh (\< 1200ms)3.  
* **E7 (Generalization):** Đã thực thi đối chiếu chéo thành công trên hai miền đối nghịch: BGL (Phần cứng) và Thunderbird (Mạng phân tán).  
* **Statistical Tests:** Đã chạy kiểm định phi tham số Wilcoxon signed-rank test (với mức ý nghĩa p \< 0.05) cho sự cải thiện DLT và FPR.

## **11\. Danh Sách Kiểm Tra Sự Sẵn Sàng Của Luận Văn (Thesis Readiness Checklist)**

* **Research Questions Answered:** 3 Câu hỏi Nghiên cứu (RQs) đã được giải đáp một cách hệ thống bằng các bằng chứng thực chứng.  
* **Objectives Met:** "Não bộ ngoại vi" RAG-SLM được cấy ghép thành công, hoạt động như một tiện ích mở rộng mà không xâm lấn không gian biểu diễn của mạng gốc.  
* **Hypotheses Tested:** Các giả thuyết H1, H2, H3 đã được phân loại rõ ràng và minh bạch thành *Supported* hoặc *Not Supported*.  
* **Limitation Confirmed:** Chương 2 của luận văn đã trình bày bằng chứng thuyết phục về hiện tượng Alert Fatigue của nền tảng LogOW.  
* **Targeted Improvement Evaluated:** Chương 5 lượng hóa chi tiết mức độ giảm nhiễu cảnh báo đạt được thông qua can thiệp RAG-SLM.  
* **Contribution Clearly Stated:** Loại bỏ các thuật ngữ tiếp thị cường điệu ("completely new method"), xác nhận định vị chuyên môn ở mức độ Nâng cấp/Mở rộng.  
* **Threats to Validity Addressed:** Trình bày minh bạch rủi ro rò rỉ dữ liệu tương lai và hiện tượng ảo giác sinh văn bản của AI.  
* **Reproducibility Adequate:** Mã nguồn, tệp cấu hình YAML, và danh sách tham số phần cứng được đính kèm chi tiết ở Phần Phụ lục.

## **12\. Danh Sách Kiểm Tra Sẵn Sàng Xuất Bản (Publication Readiness Checklist)**

Chất lượng của một bài báo mục tiêu Q1/Q2 yêu cầu sự tách bạch dứt khoát giữa những lỗi chí mạng cần phải khắc phục ngay lập tức (Blocking Issues) và các điểm cải thiện thứ cấp (Non-blocking Improvements).

### **Blocking Issues (Lỗi Chí Mạng Bắt Buộc Sửa Khắc Phục)**

* Sự cố không sử dụng Chronological Split (Vẫn để lọt hàm Random Shuffle gây Data Leakage). \-\> *Bắt buộc sửa chữa.*  
* Bằng chứng hiệu năng chỉ đo lường dựa trên F1-Score tĩnh, không chứng minh được năng lực về Thời gian Dẫn trước (DLT). \-\> *Bắt buộc khắc phục.*  
* Hiện tượng Ảo giác (Hallucination) của SLM tự ý thay đổi cảnh báo an toàn thành sụp đổ mà không có cơ chế Fallback (Thoái lui) bảo vệ an toàn. \-\> *Bắt buộc can thiệp.*  
* Luồng gọi API vLLM chiếm hơn 15% dung lượng phân tích hệ thống, phá vỡ hoàn toàn SLA độ trễ thời gian thực. \-\> *Bắt buộc xử lý thông qua việc cấu hình nâng ngưỡng cắt động Entropy*3.

### **Non-blocking Improvements (Điểm Cải Thiện Có Thể Gác Lại)**

* Việc thiết kế và tích hợp giao diện Dashboard UI quản lý cảnh báo (Không mang lại giá trị cốt lõi cho một nghiên cứu học thuật).  
* Đề xuất triển khai thuật toán lượng tử hóa cực đại siêu nhẹ để đưa mô hình Llama-3 xuống dưới mức 3-bit (Đây là một chủ đề phức tạp, phù hợp cho các nghiên cứu tương lai).  
* Áp dụng cơ chế truy xuất đồ thị đa chiều (GraphRAG) thay vì VectorRAG thông thường (Khối lượng công việc này vượt quá giới hạn khả thi của một luận văn 6-9 tháng).

## **13\. Kế Hoạch Đánh Giá Vòng Đời Cuối (Final 6–9 Month Plan)**

Bảng phân kỳ ra quyết định bảo vệ hệ thống khỏi việc sa lầy vào các nút thắt kỹ thuật không mang lại giá trị cốt lõi cho câu hỏi nghiên cứu.

| Khung Thời gian (Period) | Mục tiêu Cốt lõi (Primary Goal) | Sản phẩm Bàn giao (Key Deliverable) | Cổng Quyết định (Decision Gate) |
| :---- | :---- | :---- | :---- |
| **M1** | Baseline setup | Môi trường Python/Docker; Dữ liệu BGL/Thunderbird sẵn sàng để nạp. | **Go/No-Go**: LogOW khởi chạy thành công được epoch huấn luyện đầu tiên. |
| **M2** | Baseline validation | Báo cáo chi tiết tái lập hệ mét FPR của thuật toán LogOW gốc. | **Go/No-Go**: FPR đạt mức tương đồng chấp nhận được so với bài báo *Journal of Systems and Software*. |
| **M3-M4** | Improvement | Hệ thống lai ChromaDB \+ vLLM (Llama-3 AWQ 4-bit) tích hợp mượt mà cổng Triage Gate. | **Go/No-Go**: Tốc độ xử lý của luồng nóng không bị đình trệ do sự can thiệp của luồng lạnh. |
| **M5** | Main experiments | Hoàn thành thực nghiệm E2, E4, E7; xuất bản thành công file log JSON từ tác tử SLM. | **Go/No-Go**: Chỉ số DLT duy trì mức dương vững chắc trên tập dữ liệu chuỗi thời gian động. |
| **M6** | Ablation/robustness | Hoàn thiện Bảng dữ liệu Ablation (E3) và đánh giá Efficiency (E6). | **Go/No-Go**: Độ trễ API của tác tử RAG-SLM nằm trong ranh giới chịu đựng (\< 1200ms)3. |
| **M7** | Final analysis | MLflow metrics frozen; quá trình kiểm định Wilcoxon signed-rank hoàn tất. | **Go/No-Go**: Sự cải thiện FPR và DLT đạt mức có ý nghĩa thống kê (p \< 0.05). |
| **M8** | Thesis writing | Bản thảo Full Draft luận văn Thạc sĩ hoàn chỉnh. | **Review**: Hội đồng học thuật duyệt bố cục và logic nhân-quả của các chương. |
| **M9** | Finalization/publication | Bản bảo vệ luận văn \+ Gói Artifact ZIP \+ Bản thảo bài báo (IEEE TSE/TOSEM). | **Submit**: Đệ trình bài báo và mở public repository trên GitHub/Zenodo. |

## **14\. Xác Minh Xếp Hạng Q1/Q2 Và Công Bố Của Phương Pháp Cơ Sở (Final Baseline Eligibility Verification)**

Sự vững chắc của nền tảng lý thuyết là điểm tựa cho toàn bộ uy tín của dự án luận văn. Các bước xác minh cuối cùng khẳng định rằng phương pháp cơ sở hoàn toàn hợp lệ đối với rào chắn kiểm định khắt khe nhất:

* **Tên bài báo cơ sở:** *LogOW: A Semi-Supervised Log Anomaly Detection Model in Open-World Setting*1.  
* **Tạp chí Công bố (Journal):** *Journal of Systems and Software* (Nhà xuất bản Elsevier)2.  
* **Năm Xuất bản (Year):** Xuất bản trực tuyến vào năm 2024, và ấn bản in chính thức Volume 222 vào năm 2025\. Thời điểm này nằm trọn vẹn trong biên độ bắt buộc **2023–2026**2.  
* **Xếp hạng & Điểm số (Ranking Source & Quartile):** Nguồn SCImago/Scopus SJR năm 2024 ghi nhận mức 0.975 (Đạt **Q1**); JCR Impact Factor duy trì ở mức 3.8 đến 5.882.  
* **Trạng thái Xuất bản (Official Publication Status):** Bài báo đã qua quá trình bình duyệt chuyên sâu (peer-reviewed) và được công bố chính thức, bác bỏ việc sử dụng các bản nháp arXiv.  
* **Tính Xác thực (DOI & Verifiability):** Có siêu dữ liệu DOI định danh bài báo (10.1016/j.jss...). Cung cấp một kho lưu trữ mã nguồn mở vĩnh viễn trên Zenodo kèm theo 1.4GB dữ liệu chuẩn hóa (DOI: 10.5281/zenodo.14214083)1.

**Kết luận Kiểm định:** Phương pháp cơ sở LogOW hoàn toàn vượt qua ngưỡng Kiểm định Bắt buộc (Strict Baseline Eligibility Gate). Kế hoạch xuất bản và thiết kế thực nghiệm không vi phạm bất kỳ rào cản nào về tính chính danh học thuật và hoàn toàn hợp lệ để làm nền tảng cho sự cải tiến RAG.

## **15\. Quyết Định Cuối Cùng (Final Decision)**

Kế hoạch thực thi dự án chính thức được phê duyệt và "chốt sổ" với cấu trúc thứ tự ưu tiên cùng các rào chắn an toàn kỹ thuật như sau:

### **Trình tự Thực thi Luận văn (Thesis Execution Priority)**

> 1. Tái lập và đóng băng trọng số của mô hình Baseline LogOW (BNN).  
> 2. Xây dựng và tích hợp mô-đun Targeted Improvement (Conditional RAG-SLM Triage thông qua sự kết hợp của ChromaDB và vLLM).  
> 3. Chạy các Main controlled experiment (Tập trung đối chứng sự sụt giảm FPR tại vùng biên trượt dạt khái niệm).  
> 4. Tính toán hệ mét Early Detection evaluation (Bóc tách toán học chỉ số DLT và EWH dựa trên nguyên tắc Chronological Split).  
> 5. Thực hiện Supporting experiments (Thực thi các phép cắt lớp Ablation, đánh giá nghiêm ngặt độ trễ Latency và Thông lượng hệ thống).  
> 6. Hoàn tất Final analysis (Chạy kiểm định thống kê Wilcoxon, xây dựng Error Taxonomy cho SLM).  
> 7. Thesis writing (Soạn thảo văn bản học thuật minh bạch hóa chuỗi nhân-quả).  
> 8. Đóng gói Artifact và nộp bản thảo bài báo mục tiêu (IEEE TSE/TOSEM/JSS).

### **Tiêu chuẩn Quyết định Go/No-Go (Go/No-Go Criteria)**

* **Baseline:** Phải tái lập được chỉ số FPR tĩnh trong biên độ sai số tương đối cho phép so với công bố lưu trữ trên Zenodo.  
* **Improvement:** Luồng xử lý RAG-SLM bắt buộc phải khả thi và tương thích với GPU cục bộ RTX 3090/4090 24GB VRAM (ứng dụng mô hình Llama-3-8B AWQ 4-bit để giữ mức tiêu hao dưới 6GB VRAM)5.  
* **Experiment:** Thời gian dẫn trước cảnh báo (DLT) bắt buộc phải đạt giá trị dương (Positive) trên siêu dữ liệu động BGL/Thunderbird; Mọi cảnh báo có DLT âm sẽ bị coi là phát hiện hậu sự cố và đánh giá là thất bại thực nghiệm3.  
* **Compute/Time:** Độ trễ luồng xử lý RAG-SLM (luồng lạnh) không được vượt quá 1200ms và tổng lưu lượng truy cập luồng này không được chiếm quá 5% tổng lưu lượng sự kiện của toàn hệ thống3.  
* **Artifact:** Tập lệnh tự động hóa (Runner scripts) phải khởi chạy thành công trơn tru trên một máy ảo độc lập chỉ bằng một dòng lệnh duy nhất.

### **Chiến lược Thoái lui (Fallback Strategy)**

Trong điều kiện thực tế nếu độ trễ truy xuất API của vLLM vi phạm thỏa thuận SLA thời gian thực, hệ thống **tuyệt đối không được phép chuyển hướng sang một đề tài khác (ví dụ: chuyển sang nghiên cứu Computer Vision)**. Thay vào đó, hệ thống sẽ thực hiện quá trình giảm phạm vi (Scope Reduction) nhưng vẫn đi đúng định hướng nghiên cứu:

* Tiến hành nâng hệ số nhân của ngưỡng cắt động (Triage Threshold Multiplier) của mạng nơ-ron Bayes để ép giảm tối đa tần suất gọi SLM, qua đó hy sinh một phần nhỏ độ nhạy (Recall) để cứu vãn tính năng thời gian thực của kiến trúc phần mềm.  
* Nếu hiện tượng Lệch chuẩn không gian nhúng (Embedding Mismatch) làm RAG thất bại trong việc đọc thông số mã Hex/IP, lập tức thoái lui về cơ chế truy xuất tĩnh thuần túy bằng đối sánh từ khóa chính xác (Exact BM25) thay vì tiếp tục sử dụng hệ thống Tìm kiếm lai (Hybrid Search)3.

Bản quy hoạch tổng thể này chính thức niêm phong mọi kiến trúc kỹ thuật và phương pháp luận. Không có phương pháp mới, công nghệ mới, hay lý thuyết râu ria nào được phép bổ sung. Dự án chuyển sang giai đoạn kỹ thuật phần mềm (Implementation Phase) với nhiệm vụ duy nhất: **Cung cấp bằng chứng thực chứng không thể bác bỏ về việc tri thức ngoại vi có khả năng giải quyết bài toán bão hòa cảnh báo trong môi trường mở.**

#### **Works cited**

> 1. LogOW: A Semi-Supervised Log Anomaly Detection Model in Open, [https://zenodo.org/records/14214083](https://zenodo.org/records/14214083)  
> 2. Journal of Systems and Software \- Impact Factor (IF), Overall, [https://www.resurchify.com/impact/details/19309](https://www.resurchify.com/impact/details/19309)  
> 3. result-8.md  
> 4. Hosting LLMs — From Fundamentals to Scaled Production (with, [https://medium.com/@xiaxiami/hosting-llms-from-fundamentals-to-scaled-production-with-hands-on-tutorial-6598d16810e0](https://medium.com/@xiaxiami/hosting-llms-from-fundamentals-to-scaled-production-with-hands-on-tutorial-6598d16810e0)  
> 5. LLMs, RAG, Agents & System Design \- AI Engineering Handbook, [https://handbook.exemplar.dev/ai\_engineer/dev\_tools/local\_llms](https://handbook.exemplar.dev/ai_engineer/dev_tools/local_llms)  
> 6. LogOW: A Semi-Supervised Log Anomaly Detection Model in Open, [https://explore.openaire.eu/search/result?pid=10.5281/zenodo.14214083](https://explore.openaire.eu/search/result?pid=10.5281/zenodo.14214083)  
> 7. How to Deploy vLLM in Production: OpenAI-Compatible API, Tensor, [https://www.codersarts.com/post/how-to-deploy-vllm-in-production-openai-compatible-api-tensor-parallelism-on-2-gpus-and-docker](https://www.codersarts.com/post/how-to-deploy-vllm-in-production-openai-compatible-api-tensor-parallelism-on-2-gpus-and-docker)  
> 8. Loghub: A Large Collection of System Log Datasets for AI-driven, [https://zenodo.org/records/3227177](https://zenodo.org/records/3227177)  
> 9. GitHub \- logpai/loghub: A large collection of system log datasets for, [https://github.com/logpai/loghub](https://github.com/logpai/loghub)  
> 10. result-1.md  
> 11. Deploy LLaMA 3 in India: Complete Guide with Indian GPU Pricing, [https://zenocloud.io/blog/deploy-llama-india-gpu/](https://zenocloud.io/blog/deploy-llama-india-gpu/)  
> 12. How to Optimize LLM Inference on Runpod Serverless, [https://www.runpod.io/articles/guides/optimize-llm-inference-on-runpod-serverless](https://www.runpod.io/articles/guides/optimize-llm-inference-on-runpod-serverless)  
> 13. ACM Transactions on Software Engineering and Methodology, [https://www.resurchify.com/impact/details/18121](https://www.resurchify.com/impact/details/18121)  
> 14. IEEE Transactions on Software Engineering \- Impact Factor (IF, [https://www.resurchify.com/impact/details/18711](https://www.resurchify.com/impact/details/18711)  
> 15. The roles of artificial intelligence and generative applications in, [https://www.emerald.com/ijmpb/article/doi/10.1108/IJMPB-09-2025-0356/1383537/The-roles-of-artificial-intelligence-and](https://www.emerald.com/ijmpb/article/doi/10.1108/IJMPB-09-2025-0356/1383537/The-roles-of-artificial-intelligence-and)  
> 16. SOFTWARE Metrics based on Scopus® data as of March 2025 Title Is, [https://kniznica.umb.sk/app/cmsSiteBoxAttachment.php?ID=6408\&cmsDataID=0](https://kniznica.umb.sk/app/cmsSiteBoxAttachment.php?ID=6408&cmsDataID=0)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAaCAYAAADMp76xAAABmklEQVR4Xu2WzytEURTHjx8hK9nYWSsbtv4ByUJZICEla8rChrUdW/EHoOzERlmSkoTdULKwUJL8SH5/T+fe5nTm1sybV28m3U99e+987513zzv3zJ0hikT+BzvQbwJVHE5iKODZ5DoCXua0klRYU0uS2JnxmVtrZM0uVGO8WZKEB4zfAC0bL3NmrAEeKbz1LVCbNauBUP9WLXUkyZ7YgWplniThfjtQAmtUgZ15pvIX7YOurZmQL5KTq2TS9O8xNGHNhCRam4+tYv3LRyCfIlskx96IGgstdgVtQk8u7oL2oGmSFzx3/j3lixV6TpB1ksmTxtfoh/H29ajYLqTjJXflxLqhHxfrOXzGr6g4yCD0RlK1Byfu4w8qTGCBpGIePd4L5VS8Db1DB9Ar1KnGuOL85bZ8U8L+LQYnOG5izxE0pmIuwpSKNfy5emtSYYFSsw+1u/tV6BAadrFf7MJdN6A5d8+MqvtQYvwC3r/UA2ngHxXeNm6fZuiT5OxlFkmqzH+cPDckLXEHNTqvCTr1EwwvlH/hSCQSKYM/3JRrd53NpBYAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAACI0lEQVR4Xu2XTUgVURTHj4WuWlQGuRFbiW0iXLSJaCUiLhQFDUQUolWgrqpVQQtx4cfSRS0UBNcRWohIqAsXYopEGzEI0YX2AVFaKfr/c+7g9TjvOcLzY4b5wQ/uOXfezNy599yZJ5KSkpIE3sLdYxh7OIiGkJwdXFlILnZcFZ1hnwuiA5s3efLVJuLGCMwzuQ7RAdeYfAHsNbnY0W4T4IeEL93L8LpNJoGw+k0sF0UHO2s7MhD7GX8qOuBq2xHCOLwL/9qOLLBcArrlHKykXxL9JnhcESyxHVmwe0bUa50YUev3ikQ7LhtVcNkmTxO+dqLUb/BQwh4OHwSX7QSsFf1YIS/gJ3jTxWQGNnvxOtz24i5427UX4H/R872Bn4ODQCPcgO9huZc/kleiA2g1+TA+wnqT4/vcfwBs57t2C+yBffvdB459EpLz27fgT9gGH4gOngzAIdcm3FeyUgf/iM7KNyfr+J8cnj0f9tkPFl7stRfb3x8VXzI5229jwtw70dLwB55zMl282LVviD7IAC71HS+uhEteTAbhS9fm7r/i9ZFM1zxx7NIN+O2152An7HfxB9gEn7t4TLR0plxMFuF912Z9P4bDLn4kOpMWex+s9ZzDGhq1SXBN9J3MDaQQfocPXd890U0rGFAJ/CI60wH86NkU/YPClbIGK1zfNCx1bR+edwuuim6MOYc3MCn6/k08z0T/MvpLN/HcsYmUlJQzYw+kT4h5P1lWDAAAAABJRU5ErkJggg==>