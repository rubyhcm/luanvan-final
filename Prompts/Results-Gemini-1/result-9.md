# **Kế Hoạch Triển Khai Thực Nghiệm, Cấu Trúc Luận Văn Và Gói Xuất Bản Khoa Học: Nâng Cấp Phương Pháp Phát Hiện Sớm Bất Thường Trên Log Giai Đoạn 2025–2026**

Bản báo cáo này cung cấp một bản thiết kế toàn diện, chuyên sâu và mang tính chiến lược về lộ trình triển khai, kế hoạch viết luận văn và chiến lược xuất bản khoa học dành cho nghiên cứu nâng cấp kiến trúc Mạng Đồ thị Động Theo thời gian thực (Continuous-Time Dynamic Graphs \- CTDG). Toàn bộ kế hoạch được xây dựng dựa trên nguyên lý cốt lõi: kế thừa một phương pháp cơ sở của giai đoạn 2025–2026 (cụ thể là TempoLog), cô lập một điểm nghẽn kiến trúc đã được xác nhận (cơ chế gộp tuyến tính tĩnh gây xung đột miền dữ liệu), triển khai một giải pháp nâng cấp có mục tiêu (Mạng Cổng Định tuyến Đặc trưng Động dựa trên lý thuyết Hỗn hợp Chuyên gia \- MoE), và cuối cùng là sản xuất một tập hợp các bằng chứng thực nghiệm đối chứng nghiêm ngặt1.  
Cấu trúc của bản kế hoạch tuân thủ các quy chuẩn học thuật và kỹ thuật khắt khe nhất từ các tạp chí hàng đầu của IEEE (đặc biệt là IEEE Transactions on Software Engineering) và các tiêu chuẩn đánh giá hiện vật nghiên cứu (Artifact Evaluation) của ACM/ICSE4. Mọi quyết định kỹ thuật, từ việc kiểm soát rò rỉ dữ liệu (data leakage) thông qua kỹ thuật phân chia theo dòng thời gian (Temporal Split) đến việc đo lường Thời gian Phát hiện Trung bình (MTTD), đều phục vụ trực tiếp cho việc bảo vệ tính liêm chính khoa học của luận văn và tối đa hóa khả năng được chấp nhận tại các diễn đàn học thuật chuẩn lõi Core A1.

## **1\. Implementation Roadmap**

Lộ trình triển khai (Implementation Roadmap) được thiết kế theo các ranh giới phụ thuộc (dependency) tuyến tính thực tế, đảm bảo rằng mỗi giai đoạn (phase) chỉ được kích hoạt khi các tiêu chí chấp nhận của giai đoạn tiền nhiệm đã được thỏa mãn hoàn toàn. Cấu trúc này phong tỏa rủi ro phình to phạm vi (scope creep), ngăn chặn việc phát triển thành một nền tảng thương mại, và duy trì sự tập trung tuyệt đối vào việc tối ưu hóa hiệu năng Phát hiện Sớm7.  
Lộ trình được chia thành bảy giai đoạn liên tiếp. Sự chuyển tiếp giữa các giai đoạn được kiểm soát bởi các tiêu chí đầu ra khắt khe, từ việc chuẩn bị môi trường điện toán đến việc đóng gói hiện vật nghiên cứu cuối cùng.

| Giai đoạn (Phase) | Mục tiêu (Objective) | Đầu vào (Inputs) | Đầu ra và Giao phẩm (Outputs & Deliverables) | Phụ thuộc (Dependencies) | Tiêu chí Chấp nhận (Acceptance Criteria) | Rủi ro Tiềm ẩn (Risks) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Phase 1: Environment and Repository** | Thiết lập môi trường phần mềm cô lập, đóng băng các thư viện phụ thuộc và chuẩn hóa cấu trúc lưu trữ mã nguồn để đạt chuẩn "Artifacts Reusable" của ACM4. | Yêu cầu hệ thống từ Đặc tả Thiết kế Kỹ thuật (TDS) và Đặc tả Thiết kế Phần mềm (SDS)9. | Môi trường Docker hoàn chỉnh; cấu trúc repository phân tách thư mục src/, configs/, data/, và artifacts/; tệp requirements.txt7. | Cấu hình phần cứng vGPU tiêu chuẩn (Nvidia Ampere/Hopper). | Môi trường được cài đặt thành công trên một máy trạm sạch (clean machine) trong dưới 30 phút không phát sinh lỗi4. | Xung đột phiên bản CUDA với PyTorch; kiểm soát bằng cách khóa cứng phiên bản hệ điều hành gốc9. |
| **Phase 2: Dataset and Baseline** | Tiền xử lý dữ liệu log thô và tái tạo lại hiện tượng sụt giảm F1-score của mô hình TempoLog tĩnh trên hệ thống mạng lưới (Spirit)3. | Các tập dữ liệu BGL, Spirit, HDFS; thuật toán Drain; mô hình Sentence-BERT ngoại tuyến. | Các tệp pickle chứa log templates và tensor ngữ nghĩa; mô hình baseline có thể suy luận luồng; kết quả thực nghiệm E12. | Hoàn tất Phase 1; cung cấp đủ dung lượng lưu trữ cục bộ cho các bộ đệm bảng băm (hash caches). | Giao thức Temporal Split 60:40 được thực thi nghiêm ngặt; cấm xáo trộn ngẫu nhiên; Baseline tái hiện sự sụp đổ F1-score3. | Rò rỉ dữ liệu tương lai (Future leakage); bị vô hiệu hóa bởi các lệnh kiểm tra (assertions) tự động chặn sự chồng chéo thời gian10. |
| **Phase 3: Targeted Improvement** | Lập trình và tích hợp Mạng Cổng Định tuyến Đặc trưng Động (Dynamic Feature Gating) dựa trên MoE vào lõi cập nhật bộ nhớ9. | Kiến trúc đồ thị CTDG từ Phase 2; siêu tham số cấu hình từ improvement.yaml7. | Mô-đun moe\_aggregator.py hoàn chỉnh bao gồm SemanticExpert, TemporalExpert và mạng MLP siêu mỏng định tuyến7. | Baseline (Phase 2\) phải hoạt động trơn tru để chia sẻ chung thuật toán đồ thị và hàm suy hao BCE Loss9. | Mạng nơ-ron lan truyền xuôi và ngược thành công không gặp lỗi hình dạng tensor (shape mismatch); đầu ra Softmax luôn bằng 110. | Mạng MLP định tuyến không hội tụ hoặc gradient nổ; áp dụng chuẩn hóa LayerNorm trước Softmax để ổn định9. |
| **Phase 4: Controlled Experiments** | Thực thi các kịch bản đối sánh 1:1, đánh giá năng lực khôi phục độ chính xác và tốc độ phản ứng thời gian thực3. | Mô hình Baseline, Mô hình Cải tiến, và tệp cấu hình experiment.yaml chứa 5 hạt giống ngẫu nhiên (seeds) cố định7. | Kết quả định lượng của E2 và E3: F1-score, PR-AUC, FAR, MTTD và Detection Lead Time7. | Việc đóng băng toàn bộ các biến kiểm soát (Optimizer, Learning Rate, Graph Hops) giữa hai mô hình9. | TempoLog-MoE khôi phục thành công F1-score trên tập Spirit; mức tăng trưởng MTTD không vượt quá 5% so với cơ sở3. | Trôi dạt khái niệm (Concept Drift) khiến F1-score biến thiên mạnh; kiểm soát bằng các chỉ số khoảng tin cậy3. |
| **Phase 5: Ablation, Robustness, and Efficiency** | Khởi chạy kịch bản E4, E5, E6 để chứng minh nguồn gốc hiệu năng và tính khả thi trong môi trường sản xuất7. | Mô hình TempoLog-MoE và luồng dữ liệu bị chèn 5% log rác (OOV logs)3. | Lịch sử biến thiên trọng số cổng; chỉ số thông lượng (Throughput) và độ trễ suy luận vi giây (Inference Latency)7. | Sự hoàn thiện của hệ thống giám sát thời gian ở cấp độ vi kiến trúc phần cứng3. | Khóa cứng trọng số Gating khiến F1-score sụp đổ; độ trễ suy luận duy trì ở mức vi giây; mô hình chặn được báo động giả do nhiễu OOV3. | Bộ đếm thời gian hiệu năng cao bị nhiễu do tiến trình ngầm; yêu cầu cô lập tài nguyên CPU/vGPU khi đo lường độ trễ10. |
| **Phase 6: Final Analysis** | Tổng hợp dữ liệu thô, áp dụng các phương pháp kiểm định thống kê và phân tích lỗi (Error Analysis) định tính7. | Dữ liệu đầu ra từ Phase 4 và Phase 5\. | Chỉ số kích thước hiệu ứng (Cohen's d), kết quả Paired Student's t-test, và báo cáo ma trận nhầm lẫn7. | Sự hội tụ thành công của toàn bộ 5 vòng chạy thực nghiệm trên các tập dữ liệu. | Mức ý nghĩa thống kê (p-value) đạt chuẩn \< 0.05, khẳng định sự cải tiến không xuất phát từ phương sai ngẫu nhiên7. | Kích thước hiệu ứng không đủ lớn; giải quyết bằng cách phân tích sâu vào các kịch bản vi mô để tìm kiếm giá trị3. |
| **Phase 7: Artifact Freeze** | Đóng băng thư mục artifacts/, cấu hình hệ thống, mã nguồn và tài liệu thành một khối dữ liệu duy nhất hỗ trợ tái lập 100%7. | Toàn bộ repository hiện hành. | Một gói hiện vật đi kèm README.md chi tiết, sẵn sàng cấp mã DOI lưu trữ vĩnh viễn (Zenodo/Software Heritage)8. | Toàn bộ 6 Phase trước đó phải hoàn tất mà không để lại bất kỳ lỗi chưa xử lý nào. | Gói hiện vật cung cấp tập lệnh cho phép người bình duyệt tái tạo kết quả bằng một lệnh CLI duy nhất (run.py \--mode)8. | Việc lộ lọt khóa bảo mật (API keys); rủi ro đã bị loại trừ do cấm hoàn toàn sử dụng LLMs trực tuyến9. |

## **2\. Development Timeline**

Kế hoạch phát triển được quy hoạch trong quỹ thời gian 9 tháng, phân bổ theo từng nhóm tác vụ có sự phụ thuộc tuyến tính chặt chẽ. Nguyên tắc định tuyến thời gian (routing principle) quy định: Việc tái tạo Baseline bắt buộc phải hoàn tất trước khi triển khai Improvement; và toàn bộ các thử nghiệm phải đóng băng trước khi tiến hành phân tích và viết báo cáo. Bất kỳ sự xáo trộn nào trong tiến trình này đều có thể dẫn đến việc kết quả thực nghiệm bị nhiễm bẩn (contamination).

| Chu kỳ (Period) | Tác vụ Chính (Main Tasks) | Giao phẩm (Deliverables) | Sự Phụ thuộc (Dependencies) | Tiêu chí Hoàn thành (Exit Criteria) |
| :---- | :---- | :---- | :---- | :---- |
| **M1 (Tháng 1\)** | Thiết lập cấu trúc thư mục, nạp dữ liệu BGL/Spirit, lập trình bộ phân tích cú pháp Drain và bộ chia tách Temporal Splitter. | Kho mã nguồn sạch (src/data\_pipeline), môi trường Docker hoàn chỉnh. | Không có. | Cấu trúc dữ liệu được chuẩn hóa, hệ thống báo lỗi ngay lập tức nếu xuất hiện rò rỉ thời gian (future leakage)7. |
| **M2 (Tháng 2\)** | Tái tạo mạng CTDG nguyên bản, tích hợp Static Linear Aggregator, chạy thực nghiệm E1. | Lõi mô hình Baseline (src/baseline), báo cáo tham chiếu sự sụp đổ F1-score trên Spirit. | Hoàn tất M1. | Baseline chạy thành công trên 5 seeds, kết quả phản ánh đúng hiện tượng sụp đổ F1-score được xác nhận từ văn bản gốc7. |
| **M3 (Tháng 3\)** | Lập trình Mạng Cổng Định tuyến Đặc trưng Động (MoE Dynamic Gating) và tích hợp các nhánh chuyên gia. | Mô-đun cải tiến (src/improvement/moe\_aggregator.py). | Hoàn tất M2. | Mạng nơ-ron lan truyền xuôi và ngược ổn định, hàm Loss BCE hội tụ, không xảy ra hiện tượng nổ gradient (NaN)7. |
| **M4 (Tháng 4\)** | Khởi chạy thực nghiệm lõi E2 và E3. Đo lường sự khôi phục F1-score và các chỉ số thời gian vật lý. | Bộ kết quả định lượng của Main Test và Early Detection Test. | Hoàn tất M3. | MTTD và Detection Lead Time được ghi nhận chính xác ở độ phân giải mili-giây cho toàn bộ luồng sự kiện7. |
| **M5 (Tháng 5\)** | Tiến hành các thực nghiệm phân tích sâu E4 (Ablation), E5 (Robustness), E6 (Efficiency), và E7 (Generalization). | Bộ kết quả Ablation, hồ sơ tiêu thụ tài nguyên phần cứng (Latency, Throughput). | Hoàn tất M4. | Quá trình khóa cứng trọng số Gating khiến F1-score sụp đổ trở lại mức baseline, chứng minh giả thuyết H23. |
| **M6 (Tháng 6\)** | Kiểm định thống kê, tính toán kích thước hiệu ứng, phân tích lỗi định tính (Error Analysis). | Các biểu đồ phân phối trọng số, đồ thị hộp MTTD, kết quả Paired t-test. | Hoàn tất M5. | Phân tích quy kết nguyên nhân hoàn chỉnh, xác nhận p-value \< 0.05, loại bỏ hoàn toàn yếu tố phương sai ngẫu nhiên3. |
| **M7–M8 (Tháng 7-8)** | Biên soạn bản nháp luận văn Thạc sĩ theo cấu trúc 6 chương và soạn thảo bài báo khoa học. | Bản thảo luận văn đầy đủ (Full draft); bản thảo bài báo (Manuscript) định dạng IEEE hai cột13. | Hoàn tất M6. | Luận văn đạt cấu trúc logic vững chắc, liên kết chặt chẽ giữa thiết kế kiến trúc, bằng chứng thực nghiệm và giải đáp RQ7. |
| **M9 (Tháng 9\)** | Đóng gói Artifact, rà soát mã nguồn, nộp bài báo khoa học, và chuẩn bị bảo vệ. | DOI từ kho lưu trữ vĩnh viễn (Zenodo/Software Heritage), hồ sơ nộp bài hoàn chỉnh. | Hoàn tất M7-M8. | Đáp ứng toàn bộ checklist của IEEE Transactions và tiêu chí đánh giá hiện vật ICSE Artifact Evaluation4. |

## **3\. Resource Planning**

Sự phân bổ tài nguyên kỹ thuật được tính toán nhằm hỗ trợ quá trình huấn luyện mạng đồ thị CTDG và đáp ứng tốc độ suy luận luồng ở mức vi giây. Việc quy hoạch rõ ràng giúp ngăn ngừa tình trạng lãng phí đầu tư vào các cụm tính toán khổng lồ không cần thiết, phản ánh tính chất tinh gọn của cải tiến được đề xuất.

### **Hardware**

Môi trường huấn luyện và suy luận yêu cầu phần cứng chuyên dụng để xử lý phép nhân ma trận cục bộ của các nút đồ thị và cập nhật liên tục bộ nhớ mạng nơ-ron3. Tuy kiến trúc Gating MLP là siêu mỏng (O(1)), nhưng đồ thị động lại có dấu chân bộ nhớ (memory footprint) lớn khi luồng sự kiện kéo dài.

* **GPU**: Yêu cầu tối thiểu một thẻ tăng tốc đồ họa (vGPU) kiến trúc Nvidia Ampere hoặc Hopper (ví dụ: RTX 3090, A10G, hoặc A100) với tối thiểu 24GB VRAM. Bộ nhớ VRAM lớn là bắt buộc để duy trì bộ đệm vector nhúng (SBERT embeddings) và trạng thái các nút láng giềng trên đồ thị trong quá trình duyệt qua các lô dữ liệu (batch processing)3.  
* **CPU & RAM**: Bộ vi xử lý tối thiểu 16 nhân logic kết hợp cùng 64GB RAM. Cấu hình này đảm bảo không xảy ra hiện tượng tràn bộ nhớ (Out-Of-Memory) khi tải vào các tập dữ liệu log viễn trắc (HDFS, BGL, Spirit) chứa hàng triệu thông điệp sự kiện.  
* **Storage**: Ổ cứng SSD chuẩn NVMe với dung lượng từ 500GB đến 1TB. Ổ cứng tốc độ cao là thiết yếu để giảm thiểu nút thắt I/O khi lưu trữ dữ liệu log thô chưa nén, cơ sở dữ liệu bảng băm chứa biểu diễn ngữ nghĩa, và thư mục artifacts/ chứa các tệp trọng số mô hình PyTorch (.pt) từ nhiều vòng chạy khác nhau.  
* **Expected Compute Bottleneck**: Nút thắt cổ chai điện toán sẽ không nằm ở mô hình mạng nơ-ron do cấu trúc MoE Gating chỉ gồm 1-2 lớp ẩn siêu mỏng. Thay vào đó, nút thắt tiềm tàng duy nhất xuất hiện tại quá trình lập chỉ mục cấu trúc đồ thị CTDG (neighborhood hop traversal) khi số lượng sự kiện liên kết chéo tăng đột biến7.

### **Software**

Khung công nghệ giới hạn khắt khe trong các thư viện thực sự cần thiết, cấm sử dụng các phần mềm sinh ra độ trễ truy xuất mạng (network latency)9.

* **Core Framework**: Thư viện PyTorch (phiên bản \>= 2.0) tương thích CUDA, đóng vai trò xây dựng kiến trúc đồ thị, mạng Gating, quy trình lan truyền xuôi/ngược và xử lý hàm suy hao BCE Loss học từ đầu đến cuối (end-to-end)10.  
* **NLP & Parsing**: Thư viện sentence-transformers được sử dụng để chạy SBERT ngoại tuyến. Mã nguồn biểu thức chính quy (Regex) của thuật toán Drain parser phục vụ việc trích xuất template tĩnh7.  
* **Data Processing & Evaluation**: Các thư viện khoa học dữ liệu nền tảng bao gồm scikit-learn (tính toán F1-score, độ chính xác, thu hồi và PR-AUC), SciPy (thực hiện kiểm định Paired t-test), cùng pandas và numpy để thao tác dữ liệu dạng bảng3.  
* **Containerization**: Docker được sử dụng độc quyền để đóng gói môi trường phần mềm thành một bản phân phối chuẩn mực, thỏa mãn yêu cầu "Artifacts Reusable" của ACM/ICSE4.

### **Human Resources & Financial Costs**

Đội ngũ nhân sự được tối ưu hóa cho mô hình nghiên cứu phòng thí nghiệm đơn lẻ:

* **Researcher (Principal AI Engineer)**: Trực tiếp chịu trách nhiệm lập trình bộ chia Temporal Split, thiết kế mô-đun MoE Gating, điều phối toàn bộ 7 kịch bản thực nghiệm, xử lý số liệu thống kê và biên soạn bản thảo luận văn/bài báo.  
* **Supervisor (Thesis Advisor)**: Giám sát quá trình thiết kế thực nghiệm, định hướng chiến lược đóng góp học thuật, rà soát tính liêm chính thống kê của các bằng chứng (Cohen's d, p-value), và duyệt thiết kế kiến trúc3.  
* **Domain Expert**: Một chuyên gia vận hành mạng lưới (Network Operator) tham gia vào giai đoạn Phân tích Lỗi (Error Analysis). Chuyên gia này hỗ trợ đánh giá định tính xem các cảnh báo giả (False Positives) trên tập dữ liệu bộ định tuyến Spirit có thực sự là lỗi mô hình hay phản ánh đúng các diễn biến bất thường tinh vi về viễn trắc mạng3.

**Đánh giá Chi phí**: Đặc biệt quan trọng, hệ thống này **không phát sinh chi phí API hay chi phí trả cho mỗi token (model cost)**. Quyết định loại bỏ hoàn toàn các khung RAG trực tuyến hay LLMs sinh tạo (như GPT-4) khỏi thiết kế kiến trúc trực tuyến giúp tiết kiệm ngân sách nghiên cứu và bảo vệ luận điểm về độ trễ vi giây9. Trọng tâm chi phí duy nhất là tiền điện và khấu hao phần cứng cho khoảng 50-100 giờ thực thi 5 vòng lặp thực nghiệm chéo (repeated runs) cục bộ.

## **4\. Risk Management**

Quá trình nâng cấp kiến trúc học sâu phân tích chuỗi thời gian đối mặt với hàng loạt các rủi ro từ logic thuật toán đến độ ổn định phần cứng. Khung quản trị rủi ro này thiết lập các phương án dự phòng (fallback) tuân thủ nguyên tắc tuyệt đối: chỉ thu hẹp phạm vi trong cùng một định hướng cải tiến (khắc phục bộ gộp tĩnh) thay vì rẽ nhánh sang chủ đề hoàn toàn mới3.

| Hạng mục Rủi ro (Risk Category) | Xác suất (Probability) | Mức độ Ảnh hưởng (Impact) | Biện pháp Giảm thiểu (Mitigation) | Phương án Dự phòng (Fallback) |
| :---- | :---- | :---- | :---- | :---- |
| **Research**: Mạng Cổng Định tuyến không tạo ra mức khôi phục F1-score (không tạo gain) hoặc kết quả tái tạo Baseline bị lệch chuẩn so với tài liệu gốc. | Trung bình | Cao | Đảm bảo mã nguồn bám sát tài liệu TempoLog gốc. Việc đánh giá được điều chỉnh để dựa trên độ tăng trưởng tương đối (Relative Gain) giữa baseline và improved model thay vì áp đặt số đo F1 tuyệt đối9. | Áp dụng cấu trúc tự chú ý đơn giản (Simple Self-Attention) trực tiếp lên 4 đặc trưng tĩnh mà không cần phân ly thành nhánh chuyên gia (Experts), giảm độ phức tạp kỳ vọng. |
| **Data**: Rò rỉ dữ liệu (Future leakage) tạo ảo tưởng hiệu năng; hiện tượng mất cân bằng nhãn trầm trọng làm sai lệch các báo cáo F1. | Thấp | Rất Cao | Khóa cứng thuật toán xáo trộn (Random Shuffle); thi hành nghiêm ngặt cơ chế phân chia Temporal Split 60:403. Áp dụng thêm PR-AUC làm thước đo hỗ trợ và giám sát FAR7. | Trích xuất các tập con (subsets) nhỏ hơn với khoảng cách phân phối hẹp hơn để đánh giá khả năng của mô hình trong một không gian miền bị thu hẹp. |
| **Engineering**: Mạng Gating MLP không hội tụ, hàm loss nổ (NaN); độ trễ suy luận (latency) tăng vọt làm nghẽn luồng sự kiện viễn trắc. | Trung bình | Cao | Tích hợp kỹ thuật chuẩn hóa LayerNorm chuyên biệt trước khi kích hoạt hàm Softmax10. Cố định mạng MLP ở kích thước siêu mỏng (1-2 layers, hidden size thấp) để bảo vệ thông lượng9. | Loại bỏ bớt số lượng tham số ẩn của Gating Network; áp dụng kỹ thuật tiền tính toán (pre-compute) cục bộ cho các cạnh đồ thị thường xuyên lặp lại. |
| **Foundation Model/Parser**: Bùng nổ số lượng log rác (OOV logs) do bộ phân tích cú pháp tĩnh Drain sụp đổ khi hệ thống nâng cấp mã nguồn, sinh ra các vector SBERT nhiễu. | Cao | Trung bình | Giữ nguyên cấu hình Drain; tận dụng bản chất của *Semantic Expert* để tự học cách đánh giá thấp (down-weight) các nút ngữ nghĩa rác, bảo vệ CTDG khỏi ô nhiễm không gian3. | Chấp nhận sự hiện diện của log rác như một bài kiểm tra sức bền (Robustness test) chuẩn mực thay vì tìm cách tinh chỉnh bộ Parser vốn là biến kiểm soát3. |

(Lưu ý: Rủi ro về ảo giác LLM (hallucinations), độ trễ API hay chất lượng truy xuất vector k-NN đã bị triệt tiêu từ trong trứng nước, do toàn bộ các công nghệ sinh tạo và RAG này bị cấm sử dụng trong vòng lặp luồng trực tuyến9).

## **5\. Thesis Writing Plan**

Luận văn Thạc sĩ sẽ được cấu trúc theo 6 chương tiêu chuẩn. Cách tiếp cận của luận văn mô phỏng một chuỗi lập luận logic từ việc chỉ trích hệ hình (paradigm) cũ, thiết kế mô hình giải quyết, đến việc bảo vệ phương pháp luận mới bằng chứng cứ thực nghiệm vững chắc được thu thập từ lộ trình trên.

### **Chapter 1 — Introduction**

* **Objective**: Xác định ranh giới định nghĩa giữa việc chẩn đoán hậu sự cố (post-mortem diagnosis) và nhu cầu cấp bách của việc Cảnh báo Sớm (Early Detection) trong các nền tảng đám mây quy mô lớn.  
* **Expected Content**: Tuyên bố vấn đề về độ trễ cảnh báo; động lực thúc đẩy việc loại bỏ khái niệm "cửa sổ trượt"; phạm vi giới hạn của nghiên cứu (tập trung vào kiến trúc CTDG); phát biểu rõ ràng các câu hỏi nghiên cứu (RQ1, RQ2, RQ3).  
* **Required Figures/Tables**: Sơ đồ so sánh thời gian phản hồi giữa mô hình Batch/Window và mô hình Streaming/Window-free.  
* **Completion Criteria**: Người đọc nhận diện rõ ràng đóng góp kiến trúc của tác giả là một "nâng cấp cục bộ nhắm mục tiêu" (targeted architectural extension) thay vì hiểu lầm đây là một framework hoàn toàn mới3.

### **Chapter 2 — Literature Review**

* **Objective**: Lập bản đồ văn bản khoa học (Systematic Literature Mapping) giai đoạn 2025–2026 và tiến hành phân tích phê phán (critical analysis) để biện minh cho việc lựa chọn Baseline.  
* **Expected Content**: Đánh giá sự thất bại của Deep Learning dựa trên cửa sổ (gây độ lệch ngữ cảnh) và các hệ thống LLM trực tuyến (gây tắc nghẽn thông lượng vi mô)3. Trình bày chi tiết Mạng Đồ thị Động TempoLog (2025) và cô lập điểm nghẽn kiến trúc có bằng chứng (Confirmed Limitation): cơ chế gộp tuyến tính tĩnh gây xung đột miền dữ liệu (Domain Conflict).  
* **Required Figures/Tables**: Ma trận năng lực so sánh CTDG với Transformer, LLM, và Agentic AI. Bảng bằng chứng cắt bỏ (ablation evidence) từ tài liệu TempoLog gốc.  
* **Completion Criteria**: Xác lập được một khoảng trống nghiên cứu (Research Gap) xuất phát trực tiếp từ các dữ liệu thực nghiệm đã công bố, không tạo lập khoảng trống dựa trên trí tưởng tượng.

### **Chapter 3 — Research Methodology**

* **Objective**: Cung cấp bức tranh toàn cảnh về phương pháp đo lường, quy trình thiết kế luồng dữ liệu thời gian và hệ thống các giả thuyết nghiên cứu.  
* **Expected Content**: Đặc tả thiết kế Temporal Split 60:40 để chống rò rỉ dữ liệu (future data leakage)7. Định nghĩa công thức toán học khắt khe để tính toán Thời gian Phát hiện Trung bình (MTTD) và Detection Lead Time7. Phát biểu các giả thuyết H1, H2, H3 về sự khôi phục F1-score và động lực học thời gian cổng định tuyến7.  
* **Required Figures/Tables**: Biểu đồ phân chia tập dữ liệu theo dòng thời gian (Chronological data splitting timeline).  
* **Completion Criteria**: Toàn bộ hệ đo lường vật lý và thống kê (bao gồm Paired t-test, Kích thước hiệu ứng Cohen's d, sử dụng 5 seeds) được mô tả chi tiết, thể hiện sự liêm chính của thực nghiệm7.

### **Chapter 4 — System and Software Design**

* **Objective**: Phẫu thuật kiến trúc mạng nơ-ron cải tiến và trình bày chi tiết bản thiết kế mã nguồn hệ thống phần mềm thực thi.  
* **Expected Content**: Phân rã luồng dữ liệu của Baseline. Đi sâu vào phương trình toán học của Mạng Cổng Định tuyến Đặc trưng Động (MoE Dynamic Gating). Minh họa luồng dữ liệu phân ly thành SemanticExpert và TemporalExpert do một mạng MLP siêu mỏng điều hướng bằng hàm phân phối Softmax9. Cấu trúc thư mục phần mềm (configs/, src/baseline/, v.v.)7.  
* **Required Figures/Tables**: Sơ đồ kiến trúc phần mềm, sơ đồ luồng dữ liệu của khối CTDG Window-free, thuật toán tính toán trọng số Gating.  
* **Completion Criteria**: Minh bạch hóa vị trí can thiệp duy nhất của dự án (khối MessageAggregator), chứng minh tính hợp lý của việc đóng băng các thành phần ngoại vi để bảo toàn thông lượng và kiểm soát biến số.

### **Chapter 5 — Experiments and Results**

* **Objective**: Trình bày hệ thống bằng chứng định lượng thu thập được từ 7 kịch bản thực nghiệm (E1-E7) một cách tuần tự và khách quan.  
* **Expected Content**: Dữ liệu tái tạo lỗi Baseline (E1). Báo cáo sự khôi phục F1-score chéo miền trên tập Spirit so sánh với BGL (E2). Khẳng định ngưỡng tăng trưởng MTTD không vượt 5% (E3/E6). Quan trọng nhất, phân tích biểu đồ cắt bỏ (Ablation \- E4) xác nhận kiến trúc sụp đổ khi khóa cứng mạng Gating3. Kết thúc bằng phân tích lỗi (Error Analysis) định tính.  
* **Required Figures/Tables**: Bảng ma trận so sánh F1/PR-AUC/FAR, Box plots thể hiện mức độ phân tán của MTTD, biểu đồ đường (Line graphs) ghi nhận lịch sử thay đổi của trọng số định tuyến theo luồng thời gian7.  
* **Completion Criteria**: Mọi giả thuyết (H1, H2, H3) đều có kết luận thống kê rõ ràng (Supported/Not Supported) với mức p-value \< 0.05 đi kèm7.

### **Chapter 6 — Discussion, Conclusion and Future Work**

* **Objective**: Tổng hợp các đóng góp khoa học, cung cấp diễn giải sâu sắc về ý nghĩa của các phát hiện và đánh giá giới hạn hiện tại của thuật toán.  
* **Expected Content**: Giải đáp triệt để RQ1, RQ2, RQ3. Phân biệt rõ sự cải tiến về F1-score đến từ yếu tố "định tuyến linh hoạt" của Gating thay vì "năng lực mô hình đơn thuần". Trình bày trung thực các hạn chế, ví dụ như mạng Gating mất thời gian hội tụ lại khi Concept Drift xảy ra đột ngột.  
* **Required Figures/Tables**: Bảng tóm tắt việc giải quyết các RQ.  
* **Completion Criteria**: Luận văn kết thúc với một diễn ngôn khoa học khách quan, không phóng đại tính mới (novelty) và bảo vệ vững chắc giá trị thực tiễn trong công nghiệp AIOps.

## **6\. Thesis Contribution Mapping**

Bảng ánh xạ đóng góp (Contribution Mapping) định hình tính liên kết nhân quả giữa các nỗ lực kỹ thuật, bằng chứng thu được và các chương của luận văn, bảo vệ lập luận của toàn bộ dự án một cách chặt chẽ. Nó phân định rạch ròi các dạng đóng góp: khoa học, phương pháp luận, và kỹ thuật.

| Hạng mục Đóng góp (Contribution) | Phân loại (Type) | Bằng chứng (Evidence) | Thực nghiệm (Experiment) | Chương Luận văn (Thesis Chapter) | Trạng thái (Status) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Baseline reproduction** | Phương pháp luận (Methodological) | Báo cáo F1-score sụt giảm và FAR tăng vọt trên tập dữ liệu Spirit do sử dụng cơ chế gộp tĩnh. | E1 | Chapter 2, Chapter 5 | Chưa thực thi (To be executed) |
| **Limitation evidence** | Khoa học (Scientific) | Dữ liệu chứng minh sự dị thể (heterogeneity) của miền mạng lưới đã phá vỡ giả định trọng số đặc trưng bất biến của thuật toán SOTA 2025\. | E1, E4 | Chapter 2, Chapter 6 | Chưa thực thi |
| **Targeted improvement** | Kỹ thuật (Engineering) | Bảng số liệu khẳng định mô hình khôi phục \>10% F1-score trên tập Spirit; Gating tự động ưu tiên gán trọng số lớn cho Temporal Expert7. | E2, E4 | Chapter 4, Chapter 5 | Chưa thực thi |
| **Early detection gain** | Khoa học (Scientific) | Hệ đo lường vật lý xác nhận MTTD tăng \<5%; bảo tồn thành công tính chất window-free và Detection Lead Time7. | E3 | Chapter 3, Chapter 5 | Chưa thực thi |
| **Robustness/efficiency** | Kỹ thuật (Engineering) | Báo cáo Inference Latency ở mức vi giây (\!\[microsec\]); Semantic Expert tự động giảm trọng số phân phối khi bị tiêm 5% log rác (OOV noise). | E5, E6 | Chapter 5 | Chưa thực thi |
| **Reproducibility artifact** | Phương pháp luận (Methodological) | Kho mã nguồn mã hóa cứng 5 seeds, giao thức Temporal Split 60:40, và các tệp cấu hình YAML bất biến7. | N/A | Chapter 3, Appendix | Chưa thực thi |

## **7\. Publication Plan**

Chiến lược xuất bản khoa học ưu tiên việc phổ biến các bằng chứng thực nghiệm đối chứng minh bạch, thẳng thắn bác bỏ xu hướng công bố các "phương pháp hoàn toàn mới" thiếu cơ sở phân tích cắt bỏ (ablation) rõ ràng. Bài báo sẽ được định hình như một công trình phân tích nâng cấp kiến trúc nhắm mục tiêu (targeted architectural enhancement) với trọng tâm là tối ưu hóa độ trễ thời gian thực.

| Diễn đàn (Venue) | Mức độ Phù hợp (Fit) | Bằng chứng Bắt buộc (Required Evidence) | Điểm mạnh cốt lõi (Main Strength) | Rủi ro chính (Main Risk) | Độ Ưu tiên (Priority) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **IEEE Transactions on Software Engineering (TSE)** | Cực Cao | Bằng chứng vững chắc về tính liêm chính thống kê (Paired t-test, Cohen's d); áp dụng giao thức Temporal Split; phân tích MTTD vật lý rõ ràng5. | Khung phân tích lỗi và đánh giá hệ thống kỹ thuật phần mềm sâu sắc, có uy tín tối thượng trong ngành. | Yêu cầu mức độ diễn giải toán học cao; quy trình phản biện đôi (double-blind) cực kỳ khắt khe16. | \#1 |
| **ICSE (Int. Conference on Software Engineering)** | Cao | Đánh giá hiện vật (Artifact Badging) hoàn hảo; chứng minh khả năng tái lập 100% bằng container/Docker với thời gian setup \<30 phút4. | Sự giao thoa mạnh mẽ giữa MLOps và giám sát viễn trắc; khả năng đạt các huy hiệu "Functional" và "Reusable"8. | Tỷ lệ chấp nhận bài thấp; giới hạn số trang có thể làm giảm không gian phân tích sâu về Ablation. | \#2 |
| **ACM TOSEM** | Khá | Phương pháp luận thực nghiệm mạnh; công bố minh bạch về giới hạn kiến trúc và mã nguồn lưu trữ vĩnh viễn (Zenodo)8. | Sự chấp nhận đối với các báo cáo mở rộng và tập trung vào quy trình kỹ thuật bền vững. | Quá trình bình duyệt có thể kéo dài vượt quá quỹ thời gian 9 tháng của dự án. | \#3 |

**Chiến lược Viết Bài báo (Manuscript Strategy)**:  
Cấu trúc bài báo sẽ mô phỏng mạch tư duy logic: *Sự phá sản của các bộ gộp đặc trưng tĩnh trong mạng CTDG → Đề xuất Khung định tuyến MoE siêu mỏng → Minh chứng khôi phục F1-score chéo miền → Đảm bảo giới hạn độ trễ vi giây*.  
Đặc biệt tuân thủ các chỉ dẫn xuất bản của IEEE Transactions:

* Giữ độ dài bài báo ở mức tối ưu (dưới 20 trang theo định dạng IEEE hai cột đơn dòng)13.  
* Minh bạch hóa mọi công cụ AI sinh văn bản (AI-generated text) được sử dụng trong quá trình biên tập tại phần Lời cảm ơn (Acknowledgements)13.  
* Đính kèm hệ thống siêu dữ liệu (Supplementary Material) đầy đủ và cập nhật mã định danh ORCID của tất cả tác giả13.  
* Tuyệt đối không sử dụng các cụm từ cường điệu như "completely new method", thay vào đó nhấn mạnh đây là "an empirical evaluation and architectural extension of graph-based log anomaly detection" nhằm phản ánh chính xác bản chất đóng góp của nghiên cứu.

## **8\. Artifact Package**

Gói hiện vật (Artifact Package) được cấu trúc chặt chẽ để vượt qua quy trình bình duyệt của track Artifact Evaluation thuộc các hội nghị như ICSE hoặc quy chuẩn của ACM. Mục tiêu là đạt được các huy hiệu (badges) danh giá: "Artifacts Evaluated \- Functional", "Artifacts Evaluated \- Reusable", và "Artifacts Available"4.  
Cấu trúc thư mục tối thiểu được thiết kế để phân rã chức năng rõ ràng, hỗ trợ quá trình kiểm tra tự động:  
artifact/ ├── README.md \# Hướng dẫn chi tiết cài đặt môi trường (\<30 phút) và thực thi CLI4 ├── requirements.txt \# Phiên bản khóa cứng của PyTorch, scikit-learn, v.v.7 ├── Dockerfile \# Cấu hình Container đóng gói môi trường nguyên bản (Vanilla Environment) ├── configs/ \# Thư mục chứa tham số cấu hình YAML7 │ ├── dataset.yaml \# Tham số Drain parser, temporal\_split\_ratio=0.6 │ ├── model.yaml \# Kích thước ẩn (hidden\_dim), neighborhood\_hops │ ├── improvement.yaml \# Cấu trúc mạng MLP MoE siêu mỏng (layers, dropout) │ └── experiment.yaml \# 5 seeds cố định \[42, 1024...\], learning rate, batch size7 ├── data\_reference/ \# Hướng dẫn và script tự động tải các tập BGL, Spirit, HDFS ├── src/ \# Lõi mã nguồn phân rã thành các namespace module7 │ ├── data\_pipeline/ \# dataset\_loader.py (xử lý Temporal Split và nạp dữ liệu) │ ├── baseline/ \# Kiến trúc StaticLinearAggregator gốc │ ├── improvement/ \# Kiến trúc MoEDynamicAggregator (Semantic & Temporal Experts) │ ├── detection/ \# Mạng MLP Link Predictor và Binary Cross-Entropy Loss │ └── evaluation/ \# Tính toán MTTD, Lead Time, F1-score, Latency ├── scripts/ \# Các tập lệnh điều phối thực nghiệm tự động │ └── run.py \# Entry point hỗ trợ cờ \--mode \[baseline|improved|ablation\]7 ├── experiments/ \# Môi trường lưu trữ trạng thái chạy hiện hành ├── tests/ \# Bộ Unit Tests (vd: test\_no\_future\_leakage, test\_moe\_gating)10 ├── docs/ \# Tài liệu thiết kế bổ sung │ └── CITATION.cff \# Định dạng trích dẫn chuẩn hóa8 └── artifacts/ \# Thư mục tự động sinh ra metadata.json, model\_best.pt, metrics.csv  
**Tính toàn vẹn của Hiện vật**: Artifact không được phép chia sẻ các khóa API bí mật (do thiết kế đã cấm sử dụng LLM/RAG trực tuyến). Dữ liệu mồi (sample datasets) định dạng .tar.gz được bao gồm để hỗ trợ vòng chạy giả lập đầu cuối nhanh (end-to-end quick-start), giúp người bình duyệt xác minh mã nguồn hoạt động mà không cần tải hàng chục GB dữ liệu4. Việc lưu trữ vĩnh viễn (Long-term archival) sẽ được thực hiện trên Zenodo hoặc Software Heritage để cấp phát mã DOI duy nhất, đáp ứng tiêu chuẩn khắt khe của nhãn "Available"8.

## **9\. Reproducibility Checklist**

Bộ kiểm tra khả năng tái lập (Reproducibility Checklist) hoạt động như bức tường lửa cuối cùng trước khi chia sẻ kết quả với cộng đồng học thuật. Nếu bất kỳ mục nào không đạt, công trình không đủ điều kiện xuất bản.

* \[ \] **Data Integrity (Tính toàn vẹn Dữ liệu)**: Giao thức chia tách theo thời gian (Temporal Split 60:40) được sử dụng tuyệt đối; không tồn tại mã lệnh gọi random\_shuffle lên dữ liệu chuỗi thời gian nhằm ngăn chặn rò rỉ dữ liệu (data leakage)7.  
* \[ \] **Seed Control (Kiểm soát Hạt giống)**: Danh sách 5 hạt giống ngẫu nhiên (seeds) được mã hóa cứng trong experiment.yaml; các kết quả báo cáo sử dụng cấu trúc Khoảng tin cậy (Confidence Intervals) hoặc Mean ± Std7.  
* \[ \] **Environment Isolation (Cô lập Môi trường)**: Tập lệnh Dockerfile có thể dựng thành công môi trường trong thời gian dưới 30 phút trên một máy trạm phần cứng tiêu chuẩn mà không lỗi thư viện4.  
* \[ \] **Metric Transparency (Minh bạch Hệ đo lường)**: Hàm tính toán Thời gian Phát hiện Trung bình (MTTD) và Detection Lead Time được tài liệu hóa rõ ràng trong src/evaluation/, xử lý chuẩn xác độ phân giải mili-giây7.  
* \[ \] **Baseline Code (Mã nguồn Cơ sở)**: Phương pháp CTDG nguyên bản của TempoLog được tái hiện trung thực bằng PyTorch, sử dụng cùng bộ tiền xử lý và bảng băm SBERT để đảm bảo tính công bằng trong so sánh2.  
* \[ \] **Execution Simplicity (Tính đơn giản Thực thi)**: Một lệnh CLI duy nhất (python run.py \--mode \[baseline | improved | ablation\]) có thể khởi chạy toàn bộ luồng pipeline từ khâu tải dữ liệu đến khâu xuất file đánh giá CSV10.

## **10\. Experiment Completion Checklist**

Bộ kiểm tra tính toàn vẹn của các luồng thực nghiệm đảm bảo mọi khía cạnh của chuỗi quy kết nguyên nhân là không thể bác bỏ.

* \[ \] **E1 (Reproduction)**: Thu thập bằng chứng định lượng về việc Baseline tĩnh bị sụp đổ F1-score trên cụm mạng Spirit so với BGL3.  
* \[ \] **E2 (Main Test)**: Bảng dữ liệu xác nhận kiến trúc TempoLog-MoE khôi phục thành công F1-score với mức độ chênh lệch cải thiện tương đối \>10% so với Baseline tĩnh trên tập dữ liệu mạng7.  
* \[ \] **E3 (Early Detection)**: Hồ sơ đo lường vật lý xác nhận chỉ số MTTD tăng không quá 5% (phản ánh latency overhead vi mô), bảo vệ giá trị cảnh báo sớm cốt lõi của CTDG3.  
* \[ \] **E4 (Ablation)**: Dữ liệu đồ thị chứng minh hiệu năng F1-score sụt giảm nghiêm trọng khi Gating bị khóa cứng thành hằng số tĩnh; lịch sử hàm Softmax lưu lại xác nhận sự chiếm ưu thế của Temporal Expert trên tập Spirit3.  
* \[ \] **E5 (Robustness)**: Mô hình sống sót thành công sau đợt tiêm 5% log rác (OOV logs), Gating tự động triệt tiêu trọng số nhánh ngữ nghĩa để phòng thủ báo động giả.  
* \[ \] **E6 (Efficiency)**: Báo cáo Latency và Throughput thực thi trên môi trường vGPU khẳng định mạng MLP siêu mỏng không gây nghẽn cổ chai I/O hay điện toán3.  
* \[ \] **E7 (Generalization)**: Đánh giá thành công khả năng chuyển giao Zero-shot domain từ tập HDFS sang tập BGL.

## **11\. Thesis Readiness Checklist**

Căn cứ nghiệm thu nội dung luận văn trước khi chuyển sang giai đoạn bình duyệt nội bộ bởi giáo sư hướng dẫn.

* \[ \] **Scope Alignment (Đồng bộ Phạm vi)**: Lời nói đầu và kết luận khẳng định rõ dự án là một sự "cải tiến nhắm mục tiêu", không chứa các luận điểm phóng đại về một công nghệ "vạn năng".  
* \[ \] **Literature Critique (Phản biện Tài liệu)**: Chương 2 phản biện sâu sắc giới hạn vật lý của LLM và RAG trực tuyến, cũng như sự mù lòa của các mô hình học sâu dựa trên cửa sổ trượt tĩnh.  
* \[ \] **Methodological Rigor (Sự chặt chẽ Phương pháp luận)**: Chương 3 trình bày chi tiết về lỗ hổng rò rỉ dữ liệu (Data Leakage) và cách Temporal Split phong tỏa rủi ro này7.  
* \[ \] **Architectural Clarity (Độ trong suốt Kiến trúc)**: Cung cấp công thức toán học và sơ đồ định tuyến Softmax phân ly SemanticExpert và TemporalExpert10.  
* \[ \] **Statistical Significance (Ý nghĩa Thống kê)**: Chương 5 báo cáo kết quả kiểm định Paired Student's t-test với p-value \< 0.05 và kích thước hiệu ứng (Cohen's d) chứng minh giá trị thực tiễn của cải tiến7.  
* \[ \] **Threats to Validity (Rủi ro Tính hợp lệ)**: Khai báo minh bạch các rủi ro Nội tại, Ngoại cảnh và Cấu trúc, bao gồm giới hạn của bộ phân tích cú pháp tĩnh Drain3. Các câu hỏi RQ1-RQ3 và giả thuyết H1-H3 đều được trả lời đầy đủ7.

## **12\. Publication Readiness Checklist**

Bộ quy chuẩn kiểm tra tính sẵn sàng nộp bài báo khoa học dựa trên tiêu chuẩn biên tập của IEEE Transactions và ICSE13.

### **Blocking Issues (Vấn đề gây từ chối lập tức)**

* \[ \] Thiếu kiểm định thống kê hoặc dựa trên duy nhất một tập dữ liệu "dễ đoán" (như HDFS).  
* \[ \] Vi phạm nguyên tắc thời gian bằng việc áp dụng xáo trộn ngẫu nhiên (Random Shuffle) lên dữ liệu viễn trắc mạng.  
* \[ \] Không công bố mã nguồn hoặc không đính kèm tệp cấu hình cho phép người bình duyệt chạy thử8.  
* \[ \] Sử dụng công cụ AI sinh văn bản (AI-generated text) trong quá trình viết bài báo mà không khai báo minh bạch trong phần Lời cảm ơn (Acknowledgements) theo quy định của IEEE13.  
* \[ \] Bài báo vượt quá 20 trang hoặc vi phạm quy định ẩn danh (double-blind review) do để lộ thông tin tác giả/phòng lab13.

### **Non-blocking Improvements (Khuyến nghị gia tăng giá trị)**

* \[ \] Tích hợp tệp CITATION.cff và xin cấp mã DOI vĩnh viễn từ Zenodo hoặc Software Heritage để đạt nhãn "Available"8.  
* \[ \] Mở rộng biểu đồ minh họa sự thay đổi của trọng số định tuyến động (gating weights) theo trục thời gian thực.  
* \[ \] So sánh kích thước tham số lưu trữ (parameter count) giữa mô hình tĩnh và mô hình động trên GPU VRAM.

## **13\. Final 6–9 Month Plan**

Bản thiết kế điều phối quỹ thời gian tổng thể 9 tháng, đính kèm các trạm ra quyết định (Decision Gates) để kiểm soát rủi ro đi chệch hướng và dừng dự án đúng lúc nếu phương pháp luận thất bại.

| Chu kỳ (Period) | Mục tiêu Chính (Primary Goal) | Giao phẩm Cốt lõi (Key Deliverable) | Cổng Quyết định (Decision Gate) |
| :---- | :---- | :---- | :---- |
| **M1** | Baseline setup | Cấu trúc Artifact repo, bộ chia Temporal Split, và thuật toán Drain parser. | **Go/No-Go**: Dữ liệu không bị rò rỉ (no future leakage); Parser tạo template ổn định. |
| **M2** | Baseline validation | Mạng CTDG chạy ổn định; Báo cáo sụp đổ F1-score trên tập Spirit được ghi nhận. | **Go/No-Go**: Tái tạo thành công hiện tượng Domain Conflict từ tài liệu gốc. |
| **M3** | Improvement | Mô-đun MoE Dynamic Gating hoàn thiện (chứa 2 nhánh chuyên gia: Ngữ nghĩa & Thời gian). | **Go/No-Go**: Mạng nơ-ron lan truyền gradient mượt mà; hàm loss hội tụ, không bị nổ (NaN). |
| **M4** | Main experiments | Bảng dữ liệu F1-score, PR-AUC và MTTD sau 5 lần chạy chéo miền (E2, E3). | **Go/No-Go**: F1 tăng trưởng \>10% trên Spirit; MTTD tăng \<5%. |
| **M5** | Ablation/robustness | Báo cáo cấu trúc Ablation (E4) và đánh giá chi phí hiệu năng Latency (E6). | **Go/No-Go**: Thực nghiệm Ablation chứng minh Gating là tác nhân duy nhất tạo ra hiệu năng. |
| **M6** | Final analysis | Kết quả thống kê (t-test, Cohen's d), ma trận nhầm lẫn, thư mục Artifact đóng băng. | **Go/No-Go**: Dữ liệu hội tụ, p-value \< 0.05. Đạt mức ý nghĩa thống kê. |
| **M7–M8** | Thesis writing | Bản thảo Full draft (6 chương) và bài báo khoa học định dạng IEEE hai cột. | **Review**: Hội đồng/Giáo sư thông qua lập luận, không bị bác bỏ vì lỗi phương pháp luận. |
| **M9** | Finalization/publication | Nộp bài lên IEEE TSE/ICSE, cập nhật mã DOI Zenodo, bảo vệ luận văn. | **Submit**: Gói Artifact sẵn sàng. |

*(Lưu ý: Nếu quỹ thời gian thực tế của cá nhân/tổ chức rút ngắn còn 6 tháng, các giai đoạn M2-M3 và M4-M5 sẽ được hợp nhất chạy song song thông qua việc phân chia các tác vụ tiền xử lý và lập trình mạng MLP cho các thành viên trong nhóm).*

## **14\. Final Decision**

Phần này chốt lại các mệnh lệnh thực thi ưu tiên nhằm duy trì khả năng hoàn thành dự án ngay cả khi đối mặt với các rủi ro kỹ thuật bất khả kháng. Sự thành công của dự án luận văn không phụ thuộc vào việc tạo ra một công nghệ khổng lồ, mà phụ thuộc vào việc bảo vệ thành công một cải tiến nhỏ bằng hệ thống bằng chứng khổng lồ.

### **Thesis Execution Priority**

Thứ tự thực thi phản ánh tầm quan trọng sống còn của từng thành phần đối với sự thành công của công trình:

> 1. **Phòng thủ Dữ liệu**: Thiết lập bộ chia Temporal Split 60:40 và khóa ngẫu nhiên (Seeds) để bảo vệ tính liêm chính7.  
> 2. **Baseline Reproduction**: Khởi chạy TempoLog nguyên bản, chứng minh thuật toán mắc lỗi (F1 sụp đổ) khi thay đổi miền hệ thống (E1)3.  
> 3. **Targeted Improvement**: Phát triển mạng MLP Gating siêu mỏng để dung hợp đặc trưng9.  
> 4. **Early Detection Metrics**: Tính toán MTTD vật lý và Detection Lead Time ở độ phân giải mili-giây (E3)7.  
> 5. **Ablation Study**: Khóa tĩnh trọng số Gating để chứng minh nguồn gốc hiệu năng hoàn toàn thuộc về định tuyến động (E4)3.  
> 6. **Final Analysis & Writing**: Biên soạn 6 chương luận văn và bài báo IEEE TSE.  
> 7. **Artifact/Publication**: Đóng gói môi trường lên Zenodo đạt chuẩn "Reusable" của ICSE8.

### **Go/No-Go Criteria**

Để tiến tới bảo vệ luận văn và xuất bản, công trình phải thỏa mãn đồng thời các điều kiện sinh tử sau:

* Baseline được tái tạo thành công, thể hiện rõ giới hạn của cơ chế gộp tĩnh.  
* Giao thức Temporal Split chia tách thành công mà không báo lỗi tràn dữ liệu thời gian (future overlap).  
* Improvement (Mạng Gating MLP siêu mỏng) hội tụ, khôi phục thành công F1-score trên tập Spirit, và **không làm nghẽn luồng xử lý** (MTTD tăng \< 5%)7.  
* Phân tích Ablation chỉ ra sự sụp đổ của hệ thống khi Gating bị vô hiệu hóa.  
* Gói phần mềm artifact có thể được chạy mượt mà trên môi trường sạch với một lệnh CLI (cấu hình YAML) duy nhất.

### **Fallback Scoping (Điều khoản Kế hoạch Dự phòng)**

Trong trường hợp cổng Gating hai chuyên gia gặp khó khăn nghiêm trọng trong việc hội tụ gradient hoặc gây lãng phí bộ nhớ GPU dẫn đến vi phạm giới hạn độ trễ, **nghiêm cấm** việc chuyển đổi toàn bộ đề tài sang các phương pháp sử dụng LLM hoặc GraphRAG trực tuyến, bởi điều đó sẽ phá vỡ triết lý cốt lõi "Early Detection" và "Window-free CTDG" đã thiết lập từ đầu.  
Thay vào đó, chiến lược thu hẹp (fallback) bắt buộc sẽ là: Rút gọn kiến trúc MoE phức tạp thành một cơ chế **Tự chú ý Đơn giản (Simple Self-Attention)** đánh trọng số trực tiếp lên 4 đặc trưng tĩnh của cạnh mà không cần phân ly thành SemanticExpert và TemporalExpert. Phương án này giữ nguyên mục tiêu giải quyết hạn chế của "cơ chế gộp tĩnh", bảo toàn hướng nghiên cứu cốt lõi và các kịch bản thực nghiệm E1-E7, đảm bảo dự án hạ cánh an toàn với một mức độ đóng góp khoa học và kỹ thuật vừa đủ để hoàn thành luận văn.

#### **Works cited**

> 1. result-1.md  
> 2. result-5.md  
> 3. result-8.md  
> 4. ICSA 2026 \- Artifacts Evaluation \- conf.researchr.org, [https://conf.researchr.org/track/icsa-2026/icsaartifacts+evaluation+track2026](https://conf.researchr.org/track/icsa-2026/icsaartifacts+evaluation+track2026)  
> 5. Reproducibility Checklist for Software Engineering Experiments \- CMS | Blog, [https://cms.crosslinkstudies.com/reproducibility-checklist-for-software-engineering-experiments/](https://cms.crosslinkstudies.com/reproducibility-checklist-for-software-engineering-experiments/)  
> 6. Large Language Models for Software Engineering: A Reproducibility Crisis \- arXiv, [https://arxiv.org/html/2512.00651v1](https://arxiv.org/html/2512.00651v1)  
> 7.   
> 8. ICSE 2026 \- Artifact Evaluation \- conf.researchr.org, [https://conf.researchr.org/track/icse-2026/icse-2026-artifact-evaluation](https://conf.researchr.org/track/icse-2026/icse-2026-artifact-evaluation)  
> 9. result-6.md  
> 10. result-7.md  
> 11. The State of Open Science in Software Engineering Research: A Case Study of ICSE Artifacts \- arXiv, [https://arxiv.org/html/2601.02066v5](https://arxiv.org/html/2601.02066v5)  
> 12. result-4.md  
> 13. Submission Guidelines for Authors \- IEEE Access, [https://ieeeaccess.ieee.org/authors/submission-guidelines/](https://ieeeaccess.ieee.org/authors/submission-guidelines/)  
> 14. Prepare your submission \- IEEE Antennas and Propagation Society, [https://ieeeaps.org/ieee-tap/for-authors/how-to-prepare-your-submission](https://ieeeaps.org/ieee-tap/for-authors/how-to-prepare-your-submission)  
> 15. (PDF) SEGRESS: Software Engineering Guidelines for REporting Secondary Studies, [https://www.researchgate.net/publication/360506974\_SEGRESS\_Software\_Engineering\_Guidelines\_for\_REporting\_Secondary\_Studies](https://www.researchgate.net/publication/360506974_SEGRESS_Software_Engineering_Guidelines_for_REporting_Secondary_Studies)  
> 16. GUIDELINES FOR AUTHORS \- IEEE Technology and Engineering Management Society, [https://www.ieee-tems.org/guidelines-for-authors/](https://www.ieee-tems.org/guidelines-for-authors/)