# **Thiết kế Kế hoạch Nghiên cứu: Nâng cao Năng lực Phát hiện Sớm Bất thường trên Log qua Mạng Đồ thị Động Tăng cường MoE**

## **1\. Research Design Consistency Check**

Sự nhất quán trong thiết kế nghiên cứu là nền tảng cốt lõi để đảm bảo tính hợp lệ khoa học và khả năng tái lập của bất kỳ công trình nào trong lĩnh vực Khoa học Máy tính. Việc đối chiếu các thành phần được phê duyệt từ đề xuất nghiên cứu với diễn giải thiết kế chi tiết nhằm đảm bảo không có sự sai lệch về phạm vi, mục tiêu, và phương pháp luận so với định hướng ban đầu1. Bảng dưới đây cung cấp một ma trận kiểm tra tính nhất quán, xác nhận rằng thiết kế hiện tại tuân thủ nghiêm ngặt mô hình nâng cấp cục bộ (targeted improvement) dựa trên một phương pháp cơ sở đã được xác định.

| Element | From result-4 | Design Interpretation | Consistent? |
| :---- | :---- | :---- | :---- |
| **Baseline** | TempoLog (2025): Khung Mạng Đồ thị Động Theo thời gian thực (CTDG), xử lý cấp độ sự kiện không sử dụng cửa sổ (window-free). | Kế thừa nguyên bản cấu trúc CTDG đa tỷ lệ của TempoLog làm mốc tham chiếu nhằm tối ưu hóa độ trễ xử lý luồng sự kiện. | Yes |
| **Limitation** | Cơ chế Cập nhật Bộ nhớ (Memory Updater) sử dụng hàm gộp tuyến tính tĩnh (Static Linear Aggregation) gây xung đột đặc trưng liên miền. | Khối Message Aggregator hiện tại áp đặt trọng số cố định cho 4 đặc trưng, dẫn đến sụp đổ hiệu năng khi chuyển dịch miền dữ liệu. | Yes |
| **Targeted Improvement** | Mạng Cổng Định tuyến Đặc trưng Động (Dynamic Feature Gating) dựa trên Hỗn hợp Chuyên gia (Mixture-of-Experts \- MoE). | Thay thế hàm tuyến tính tĩnh bằng mạng MLP siêu mỏng, phân ly đặc trưng thành *Semantic Expert* và *Temporal Expert* để tự động hóa sự chú ý. | Yes |
| **RQ** | Tác động của hàm gộp tĩnh; Khả năng khôi phục F1 của Gating; Độ trễ tính toán của mạng Gating. | Đưa các câu hỏi nghiên cứu vào quy trình kiểm định định lượng, bao gồm đo lường tỷ lệ báo động giả, độ ổn định F1-score và độ trễ suy luận. | Yes |
| **Hypotheses** | Cải thiện 10% F1 trên tập dữ liệu mạng; Trọng số Temporal chiếm ưu thế; MTTD tăng không quá 5%. | Xây dựng các giả thuyết có thể kiểm định bằng toán học thống kê thông qua các bài kiểm tra chéo và phân tích cắt bỏ (Ablation). | Yes |
| **Main Metrics** | Mean Time to Detect (MTTD), Detection Lead Time, F1, PR-AUC, Latency. | Ưu tiên tuyệt đối các chỉ số cảnh báo sớm (Early Detection) thay vì chỉ lệ thuộc vào thước đo chẩn đoán hậu sự cố. | Yes |
| **Main Dataset** | BGL (Compute-bound), Spirit (Network-bound), HDFS (Sanity check). | Kiểm soát chặt chẽ rò rỉ dữ liệu bằng phương pháp phân chia Temporal Split, loại bỏ hoàn toàn việc xáo trộn ngẫu nhiên. | Yes |

Kiến trúc tổng thể của nghiên cứu bám sát triết lý nâng cấp tối giản. Thay vì tạo ra một hệ thống hoàn toàn mới mang tính chắp vá, thiết kế này cô lập một điểm nghẽn duy nhất trong phương pháp cơ sở, đề xuất một giải pháp can thiệp có cơ sở lý thuyết vững chắc, và chứng minh hiệu quả thông qua thực nghiệm đối chứng nghiêm ngặt1.

## **2\. Existing Baseline Reconstruction**

Để thực hiện bất kỳ cải tiến nào, việc tái thiết lập kiến trúc của hệ thống cơ sở là bước tiên quyết. Khung làm việc TempoLog (Beyond Window-Based Detection: A Graph-Centric Framework for Discrete Log Anomaly Detection, công bố năm 2025\) được lựa chọn nhờ khả năng phá vỡ giới hạn của các mô hình học sâu truyền thống1. Các hệ thống tiền nhiệm thường phụ thuộc vào các cửa sổ trượt tĩnh (sliding windows), gây ra "độ lệch ngữ cảnh" (context bias) và sự mơ hồ trong định vị lỗi2. Ngược lại, TempoLog thiết lập một đường ống xử lý luồng sự kiện (event-level streaming) trực tiếp, được mô tả thông qua các giai đoạn cốt lõi sau:  
Quá trình bắt đầu với luồng dữ liệu đầu vào (Input), nơi các thông điệp log thô (raw logs) được sinh ra liên tục từ các kiến trúc vi dịch vụ và hệ thống phân tán. Tại pha tiền xử lý (Preprocessing/Parsing), thuật toán Drain được ứng dụng để bóc tách các tham số động (dynamic parameters) và trích xuất các mẫu tĩnh (log templates)1. Việc sử dụng parser giúp giảm thiểu sự bùng nổ không gian trạng thái của hệ thống. Kế tiếp, ở pha biểu diễn (Representation), mỗi template mới được khởi tạo thành một vector nhúng ngữ nghĩa (semantic embedding) thông qua mô hình ngôn ngữ Sentence-BERT (SBERT). Quá trình này tạo ra một không gian vector dày đặc, mang tính chất tĩnh và được lưu trữ trong bộ đệm để truy xuất tức thời1.  
Điểm đột phá của baseline nằm ở pha xử lý chuỗi và ngữ cảnh (Sequence/Context). Thay vì nhóm dữ liệu thành các khối thời gian cố định, hệ thống xây dựng một Mạng Đồ thị Động Theo thời gian thực (Continuous-Time Dynamic Graphs \- CTDG). Mỗi log template xuất hiện được coi là một nút (node), và các tương tác tuần tự theo thời gian được biểu diễn thành các cạnh (edges)2. Mạng đa tỷ lệ (multi-scale) này cho phép hệ thống nắm bắt cả phụ thuộc cục bộ và toàn cục mà không cần định nghĩa kích thước cửa sổ.  
Cốt lõi của mô hình (Baseline Core) hoạt động dựa trên cơ chế cập nhật bộ nhớ của CTDG. Mỗi nút duy trì một vector bộ nhớ ![][image1] để lưu trữ trạng thái lịch sử3. Khi một sự kiện mới phát sinh, thông điệp từ các nút láng giềng được tập hợp lại. Tại đây, mỗi cạnh mang 4 đặc trưng tĩnh: Sự tương đồng ngữ nghĩa (![][image2]), Tần suất đồng xuất hiện (![][image3]), Khoảng thời gian trễ (![][image4]), và Mức độ nghiêm trọng của log (![][image5])1. Mô-đun Message Aggregator của TempoLog thực hiện việc gộp 4 đặc trưng này thông qua một hàm biến đổi tuyến tính tĩnh (Static Linear Aggregation) để sinh ra vector thông điệp cập nhật cho bộ nhớ1.  
Sau khi bộ nhớ được cập nhật, pha tính điểm bất thường (Anomaly Scoring) kích hoạt một mạng Multi-Layer Perceptron (MLP) đóng vai trò dự đoán liên kết (Link Prediction). Mạng này tính toán xác suất tồn tại một liên kết hợp lệ giữa hai nút tại mốc thời gian ![][image6]. Dựa trên một ngưỡng quyết định (Decision), nếu xác suất thấp, hệ thống kích hoạt tín hiệu cảnh báo cấp độ sự kiện (Output), cung cấp khả năng phát hiện tức thời mà không cần chờ đợi cửa sổ dữ liệu đóng lại2.

## **3\. Targeted Improvement Definition**

Mặc dù kiến trúc CTDG mang lại tốc độ xử lý ưu việt, các phân tích cắt bỏ (Ablation Studies) từ báo cáo nguyên bản của TempoLog đã phơi bày một điểm nghẽn kiến trúc (bottleneck) nghiêm trọng tại mô-đun Message Aggregator1. Việc sử dụng hàm gộp tuyến tính tĩnh ngụ ý rằng hệ thống áp đặt một bộ trọng số bất biến cho các đặc trưng ![][image7], bất kể bản chất vật lý của hệ thống đang được giám sát1.

| Component | Baseline | Limitation | Improvement | Expected Effect | Evidence |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Memory Updater (Message Aggregator)** | Hàm gộp tuyến tính tĩnh cho 4 đặc trưng cạnh (![][image7]). | Cấu trúc tĩnh không thể thích ứng với sự dịch chuyển miền (Domain Shift). Nó gây nhiễu chéo khi phân phối đặc trưng thay đổi giữa các hệ thống khác biệt. | Tích hợp **Dynamic Feature Gating** dựa trên MoE. Phân ly thành *Semantic Expert* (![][image8]) và *Temporal Expert* (![][image9]), kết hợp mạng MLP định tuyến động. | Tự động hóa sự chú ý (attention weight) theo ngữ cảnh miền. Duy trì sự ổn định trên hệ thống tính toán, đồng thời khôi phục F1 trên hệ thống mạng. Tối ưu hóa tính bền bỉ (robustness) và tổng quát hóa. | Bảng Ablation của TempoLog xác nhận F1 rớt 75% trên tập Spirit khi thiếu đặc trưng ngữ nghĩa do cơ chế gộp không thể tự điều chỉnh trọng số1. |

Sự phân phối tĩnh này tạo ra hiện tượng xung đột miền (Domain Conflict). Trên hệ thống siêu máy tính (ví dụ BGL), đặc trưng ngữ nghĩa đóng vai trò sống còn. Tuy nhiên, trên hệ thống bộ định tuyến mạng (ví dụ Spirit), sự biến động của khoảng thời gian trễ mới là tín hiệu quyết định, trong khi đặc trưng ngữ nghĩa lại đóng vai trò như một tác nhân gây nhiễu1. Cải tiến nhắm mục tiêu (Targeted Improvement) sẽ thay thế hàm gộp tĩnh bằng một Mạng Cổng Định tuyến Động (Dynamic Feature Gating) dựa trên lý thuyết Hỗn hợp Chuyên gia (MoE), trao cho mô hình khả năng tự động điều chỉnh sự chú ý (attention weights) theo thời gian thực để thích ứng với mọi môi trường triển khai1.

## **4\. Research Architecture**

Kiến trúc tổng thể của nghiên cứu được xây dựng dựa trên nguyên tắc mở rộng có kiểm soát: duy trì nguyên vẹn các thành phần xử lý luồng cốt lõi của Baseline và chỉ can thiệp vào điểm nghẽn toán học đã được chứng minh. Phương pháp tiếp cận này đảm bảo khả năng quy kết nguyên nhân rõ ràng cho mọi biến động về hiệu năng.

* **Data:** **Inherited**. Kế thừa toàn bộ cấu trúc nạp dữ liệu sự kiện từ các tập dữ liệu điểm chuẩn công cộng mà không thay đổi định dạng đầu vào.  
* **Preprocessing:** **Inherited**. Thuật toán phân tích cú pháp Drain được giữ nguyên để đảm bảo tính nhất quán trong việc sinh ra các log templates1.  
* **Representation:** **Inherited**. Không gian vector nhúng được khởi tạo bằng Sentence-BERT ngoại tuyến, loại bỏ sự cần thiết phải gọi API trong quá trình xử lý thời gian thực1.  
* **Context / Graph Construction:** **Inherited**. Mạng CTDG đa tỷ lệ không cửa sổ được bảo tồn toàn diện. Việc duy trì cấu trúc này là bắt buộc để bảo vệ đặc tính độ trễ thấp của mô hình2.  
* **Foundation Model:** **Inherited**. Foundation Model (SBERT) chỉ giới hạn ở khâu khởi tạo biểu diễn tĩnh.  
* **Retrieval / Knowledge / Reasoning:** **Optional (Excluded)**. Các kỹ thuật truy xuất RAG hoặc suy luận đa bước bằng LLM bị loại bỏ hoàn toàn khỏi đường ống phát hiện chính. Bản chất của các truy vấn k-NN đồng bộ sinh ra độ trễ I/O nghiêm trọng, trực tiếp phá vỡ quỹ thời gian cảnh báo sớm (Early Warning Horizon) và làm tăng chỉ số MTTD4.  
* **Memory / Message Aggregation:** **Modified (The Intervention Point)**. Đây là khu vực chịu sự can thiệp kiến trúc duy nhất của toàn bộ nghiên cứu.  
* **Dynamic Feature Gating (MoE):** **New**. Mạng Multi-Layer Perceptron (MLP) siêu mỏng được nhúng vào mô-đun tổng hợp thông điệp. Đặc trưng được tách thành *Semantic Expert* và *Temporal Expert*. MLP tính toán hai trọng số cổng định tuyến ngay tại thời điểm diễn ra sự kiện1.  
* **Detection (Link Prediction):** **Inherited**. Hàm dự đoán liên kết và hàm suy hao Binary Cross-Entropy (BCE) được giữ nguyên1.  
* **Early Detection / Alert:** **Modified (Evaluation Protocol)**. Đầu ra cảnh báo được tích hợp vào hệ thống đo lường thời gian vật lý mới nhằm định lượng chính xác năng lực Phát hiện Sớm.

Thiết kế này làm rõ rằng luồng dữ liệu, quá trình tiền xử lý, cấu trúc đồ thị và cơ chế đánh giá tổn thất (loss mechanism) remains unchanged, trong khi phương thức tổng hợp đặc trưng và phân bổ trọng số bộ nhớ is improved1.

## **5\. Data Pipeline**

Luồng dữ liệu (Data Pipeline) được thiết kế khép kín, hoạt động theo cơ chế luồng (streaming) liên tục để mô phỏng chính xác môi trường vận hành sản xuất.  
Giai đoạn đầu tiên, **Raw Logs**, tiếp nhận các luồng văn bản thô theo thời gian thực từ các node phân tán. Dữ liệu này ngay lập tức được đẩy vào mô-đun **Parsing**, nơi thuật toán Drain tách cấu trúc thành các biến số động và mẫu tĩnh, tạo ra chuỗi định danh sự kiện (Event IDs). Mục đích của bước này là cô đọng không gian trạng thái, ngăn chặn sự phình to của đồ thị. Kế tiếp, pha **Representation** ánh xạ mỗi Event ID mới thành một vector ngữ nghĩa thông qua SBERT. Để đảm bảo độ trễ thấp, kết quả nhúng được lưu trữ trong bảng băm cục bộ (local cache), đảm bảo thời gian truy xuất là ![][image10] cho các sự kiện lặp lại1.  
Dữ liệu sau đó tiến vào khối **Window (Window-free)**. Thay vì chờ đợi một tập hợp các sự kiện để lấp đầy cửa sổ thời gian, mỗi sự kiện được đẩy trực tiếp vào quá trình cập nhật đồ thị CTDG. Mối quan hệ giữa sự kiện hiện tại và lịch sử tương tác được mã hóa thành các cạnh chứa 4 thuộc tính. Tại đây, luồng dữ liệu đi qua **Targeted Improvement (MoE Gating)**. Các đặc trưng cạnh đi vào hai luồng chuyên gia chuyên biệt. Mạng Gating quan sát bối cảnh không gian-thời gian của đồ thị, xuất ra phân phối softmax cho hai trọng số cổng. Vector thông điệp mới được tổng hợp có chọn lọc, ưu tiên tín hiệu hữu ích và triệt tiêu nhiễu1.  
Giai đoạn **Detection** nhận vector bộ nhớ đã cập nhật để so khớp với nút mục tiêu thông qua mạng MLP dự đoán liên kết. Xác suất này quyết định trạng thái của hệ thống. Cuối cùng, pha **Early Detection Evaluation / Alert** ghi nhận thời gian phát ra tín hiệu cảnh báo, đối chiếu với nhãn thời gian của lỗi hệ thống thực tế (system failure tag) để định lượng độ trễ cảnh báo, hoàn tất chu trình giám sát theo thời gian thực.

## **6\. Temporal Data Design**

Vấn đề kiểm soát và thiết kế dữ liệu thời gian (Temporal Data Design) quyết định tính liêm chính của toàn bộ thiết kế thực nghiệm. Trong các hệ thống chuỗi thời gian, bất kỳ sự rò rỉ dữ liệu (future leakage) nào cũng sẽ làm mất hiệu lực của kết luận khoa học, tạo ra ảo tưởng về hiệu năng1.  
Dữ liệu đầu vào phải duy trì thuộc tính **timestamp/order** tuyệt đối. Mọi sự kiện được xử lý theo trình tự thời gian vật lý với độ phân giải mili-giây. Thiết kế **observation window** tuân thủ nguyên tắc window-free; luồng quan sát là liên tục và không bị cắt khúc nhân tạo. Việc xác định bối cảnh (**context window**) không dựa trên giới hạn thời gian tĩnh, mà được định hình động thông qua số lượng bước nhảy láng giềng (neighborhood hops) bên trong CTDG, cho phép mô hình thu thập thông tin từ các sự kiện có tương quan nhân quả bất kể khoảng cách thời gian2. Pha dự đoán (**prediction horizon**) diễn ra tức thời tại mốc thời gian ![][image6] của sự kiện đang xét.  
Biện pháp bảo vệ tối quan trọng là việc thiết lập kỹ thuật phân chia dữ liệu **Temporal Split 60:40** (Chronological Split). Tập dữ liệu được sắp xếp nghiêm ngặt theo dòng thời gian. Khối 60% dữ liệu phát sinh đầu tiên được sử dụng độc quyền cho quá trình huấn luyện, trong khi khối 40% xuất hiện sau đó chỉ dành cho kiểm thử1. Việc sử dụng thuật toán xáo trộn ngẫu nhiên (Random Shuffle) bị nghiêm cấm, nhằm đảm bảo mô hình không bao giờ có thể "nhìn trộm" các hành vi của tương lai để nội suy quy luật của quá khứ1. Mạng Gating MLP chỉ được quyền truy cập vào cấu trúc đồ thị và tri thức tích lũy tính đến mốc thời gian ![][image11].

## **7\. Knowledge / Retrieval Design**

Dựa trên quá trình phân tích phê phán tài liệu học thuật giai đoạn 2025-2026, các cơ chế Trí tuệ Nhân tạo Tăng cường Tri thức (Knowledge-Augmented AI) hoặc Truy xuất RAG bị loại trừ hoàn toàn khỏi thiết kế kiến trúc4. Mặc dù các kỹ thuật này mang lại khả năng giải thích (explainability) xuất sắc bằng cách truy xuất tài liệu thiết kế hoặc báo cáo sự cố lịch sử, chúng vấp phải rào cản vật lý về độ trễ.  
Việc thực hiện các phép tìm kiếm lân cận gần nhất (k-NN search) trong cơ sở dữ liệu vector khổng lồ đối với hàng vạn thông điệp log mỗi giây sinh ra nút thắt cổ chai I/O nghiêm trọng. Sự chậm trễ đồng bộ này trực tiếp bóp nghẹt thông lượng xử lý luồng (streaming throughput) và phá vỡ tiêu chí "Phát hiện Sớm" (Early Detection). Mô hình cơ sở TempoLog được thiết kế để xử lý sự kiện trong vòng vi giây2, do đó, việc ép buộc ghép nối Retrieval sẽ phá hủy ưu thế lớn nhất của Baseline. Trong phạm vi đề tài này, nếu RAG được triển khai, nó chỉ đóng vai trò là một quy trình hậu kiểm (post-mortem) phi đồng bộ, nằm ngoài đường ống giám sát thời gian thực.

## **8\. Foundation Model / Learning Design**

Việc lạm dụng Mô hình Ngôn ngữ Lớn (LLMs) trong vòng lặp suy luận luồng tạo ra chi phí tính toán (compute cost) và độ trễ sinh token (token generation latency) không thể chấp nhận được đối với các hệ thống AIOps tuyến đầu4. Do đó, vai trò của Foundation Model được tinh giản tối đa.  
Hệ thống sử dụng mô hình Sentence-BERT (SBERT) độc quyền cho tác vụ tiền xử lý ngoại tuyến (offline preprocessing) nhằm khởi tạo không gian vector ngữ nghĩa cho các log templates1. Trong quá trình suy luận trực tuyến, mô hình không thực hiện bất kỳ lệnh gọi API hoặc lan truyền xuôi (forward pass) nào đối với mạng Transformer khổng lồ; mọi truy xuất đều thông qua bảng băm lưu trữ trước. Không áp dụng các kỹ thuật fine-tuning hay PEFT lên SBERT để giữ cho đường ống gọn nhẹ.  
Quá trình học tập (Learning) hoàn toàn tập trung vào Mạng Gating MLP và khối Multi-Layer Perceptron dự đoán liên kết. Chúng được huấn luyện end-to-end thông qua kỹ thuật truyền ngược (backpropagation) sử dụng hàm suy hao Binary Cross-Entropy (BCE) Loss dựa trên tín hiệu giám sát từ chuỗi sự kiện tiếp theo1. Việc cô lập quá trình học tập vào mô-đun định tuyến đảm bảo cải tiến nhắm mục tiêu (targeted improvement) thực sự là tác nhân mang lại sự thay đổi hiệu năng.

## **9\. Inference Strategy**

Chiến lược suy luận (Inference Strategy) được phân tách rạch ròi giữa các tiến trình có thể tính toán trước và các bước nhạy cảm với độ trễ để bảo vệ thông lượng của hệ thống1.

* **Offline / Precomputed Steps:** Bao gồm việc học quy luật phân tích cú pháp (parser trees) của thuật toán Drain và việc ánh xạ các mẫu log tĩnh thành vector nhúng ngữ nghĩa thông qua SBERT. Các hoạt động này được thực hiện trong quá trình khởi tạo hoặc cập nhật nền.  
* **Online / Latency-Sensitive Steps:** Khi một thông điệp log thô mới được tiếp nhận, hệ thống nhận diện Event ID trong thời gian ![][image10]. Sự kiện này được chèn vào đồ thị CTDG, khởi tạo cạnh kết nối với các nút lịch sử. Bốn đặc trưng cạnh tĩnh được trích xuất tức thời. Tại đây, mạng Gating MLP kích hoạt. Do cấu trúc siêu mỏng (thin architecture), mạng tính toán hai trọng số cổng ![][image12] (cho Semantic Expert) và ![][image13] (cho Temporal Expert) với độ phức tạp ![][image10]1. Vector bộ nhớ của nút được cập nhật, và mạng dự đoán liên kết tính toán điểm số bất thường (anomaly score).  
* **Alert Generation:** Nếu điểm số vượt quá ngưỡng cho phép, tín hiệu cảnh báo được phát ra. Toàn bộ chu kỳ suy luận này được ràng buộc phải hoàn thành trong khoảng thời gian tính bằng vi giây (microseconds), đảm bảo khả năng đáp ứng cho các hệ thống có lưu lượng cao.

## **10\. Experimental Design**

Kế hoạch thực nghiệm được cấu trúc thành 7 pha độc lập, nhằm cung cấp bằng chứng định lượng vững chắc bảo vệ các giả thuyết nghiên cứu.

* **E1 — Baseline Reproduction:** Tái tạo nguyên bản mô hình TempoLog gốc (với hàm gộp tĩnh) trên các tập dữ liệu điểm chuẩn HDFS, BGL, và Spirit, sử dụng cấu trúc Temporal Split. Quá trình này thiết lập mốc tham chiếu và xác nhận lại sự sụt giảm F1-score (khoảng 75% trên tập Spirit) khi phân phối đặc trưng thay đổi, chứng minh tồn tại của điểm nghẽn1.  
* **E2 — Main Improvement Test:** Thực hiện so sánh đối sánh trực tiếp (head-to-head) giữa TempoLog gốc và kiến trúc TempoLog-MoE trên các tập dữ liệu chéo miền. Đây là thử nghiệm nòng cốt để kiểm chứng RQ2, đo lường sự khôi phục và duy trì F1-score khi chuyển đổi giữa hệ thống thiên về ngữ nghĩa (BGL) và hệ thống thiên về thời gian (Spirit)1.  
* **E3 — Ablation Study (Phân tích Cắt bỏ):** Nhằm phục vụ mục tiêu quy kết nguyên nhân (attribution), thử nghiệm này sẽ ép buộc các trọng số định tuyến động (![][image14]) trong TempoLog-MoE trở thành hằng số tĩnh (ví dụ: 0.5/0.5). Nếu hiệu năng mô hình biến động và sụt giảm trở lại mức của Baseline, điều này cung cấp bằng chứng toán học rằng mạng Gating động chính là tác nhân duy nhất tạo ra sự vượt trội1.  
* **E4 — Early Detection:** Đánh giá năng lực thời gian vật lý. Đo lường Thời gian Phát hiện Trung bình (MTTD) và Thời gian Cảnh báo Trước (Detection Lead Time). Cải tiến MoE không được phép làm tăng MTTD vượt quá ngưỡng 5% so với bản gốc1.  
* **E5 — Robustness:** Kiểm tra độ bền bỉ bằng cách chèn thêm các mẫu log rác (garbage templates) mô phỏng sự cố của bộ phân tích cú pháp (parser failure). Quan sát cách Semantic Expert tự động bị giảm trọng số để bảo vệ hệ thống khỏi các báo động giả.  
* **E6 — Efficiency:** Đo lường chi phí vật lý của cải tiến. Báo cáo độ trễ suy luận trung bình (inference latency) trên mỗi thông điệp log tính bằng vi giây và tổng thông lượng (throughput)1.  
* **E7 — Generalization:** Đánh giá năng lực tổng quát hóa Zero-shot bằng cách huấn luyện mô hình trên HDFS và suy luận trực tiếp trên BGL mà không cần tinh chỉnh lại, kiểm tra khả năng tự thích ứng của mạng định tuyến.

## **11\. Evaluation Metrics**

Việc lựa chọn hệ đo lường phải phản ánh sự khác biệt giữa chẩn đoán chệch hướng và phát hiện sớm.

### **11.1 Detection (Độ chính xác Nhị phân)**

* **F1-Score (Macro & Micro):** Chỉ số chính để đánh giá sự cân bằng giữa Precision và Recall. Mục tiêu tối thượng là khôi phục toàn bộ phần F1-score (lên tới 75%) đã bị đánh mất trên tập Spirit do nhiễu miền1.  
* **PR-AUC:** Đo lường hiệu năng trên dữ liệu mất cân bằng (imbalanced data), vốn là đặc trưng cố hữu của các luồng sự kiện viễn trắc.  
* **False Alarm Rate (FAR):** Tỷ lệ báo động giả (False Positives), đóng vai trò quan trọng trong việc trả lời RQ1 về tác động của hàm gộp tĩnh1.

### **11.2 Early Detection (Tiêu chuẩn Thời gian thực)**

* **Mean Time to Detect (MTTD):** Độ trễ vật lý, tính từ mốc thời gian sự kiện bất thường đầu tiên xuất hiện (root cause onset) đến khi thuật toán phất cờ cảnh báo1.  
* **Detection Lead Time (Early Warning Horizon):** Khoảng thời gian từ khi hệ thống AI phát tín hiệu cảnh báo đến khi ghi nhận trạng thái sập dịch vụ thực tế (System Failure Tag). Đây là quỹ thời gian vàng để đội ngũ vận hành can thiệp1.

### **11.3 Efficiency (Hiệu năng Vật lý)**

* **Inference Latency:** Đo lường chi phí thời gian cho mỗi pha dự đoán tính bằng vi giây (microseconds)1.  
* **Throughput:** Định lượng khả năng đáp ứng lưu lượng cao thông qua tổng số thông điệp log xử lý mỗi giây1.

## **12\. Statistical Design**

Nhằm đảm bảo kết quả không phát sinh từ sự may mắn hay phương sai (variance) trong quá trình khởi tạo trọng số ngẫu nhiên của mạng nơ-ron (Gating MLP và Link Predictor), thiết kế thống kê sau được áp dụng1:

* **Repeated Runs:** Các thực nghiệm lõi (E1-E3) bắt buộc phải được lặp lại 5 lần (5 independent runs) với các seed ngẫu nhiên khác nhau.  
* **Reporting:** Kết quả đánh giá sẽ được báo cáo dưới định dạng khoảng tin cậy (Confidence Intervals) hoặc Giá trị Trung bình ![][image15] Độ lệch Chuẩn (Mean ![][image15] Std).  
* **Significance Tests:** Sử dụng kiểm định Paired Student's t-test (![][image16]) để khẳng định sự gia tăng F1-score của kiến trúc MoE so với Baseline mang ý nghĩa thống kê vững chắc.

## **13\. Controlled Variables**

Để chứng minh nguyên nhân dẫn đến hiệu năng tăng lên hoàn toàn thuộc về khối Dynamic Feature Gating, tất cả các thành phần môi trường và kiến trúc khác được đóng băng (controlled) nghiêm ngặt1. Bảng dưới đây hệ thống hóa các biến kiểm soát:

| Factor | Baseline (TempoLog) | Improved (TempoLog-MoE) | Controlled? |
| :---- | :---- | :---- | :---- |
| **Dataset & Split** | BGL, Spirit (Temporal Split) | BGL, Spirit (Temporal Split) | **Yes** \[cite: 1\] |
| **Log Parser** | Drain (Fixed parameters) | Drain (Fixed parameters) | **Yes** |
| **Initial Embedding** | Sentence-BERT (SBERT) | Sentence-BERT (SBERT) | **Yes** \[cite: 1\] |
| **Graph Structure** | Hops, node initialization | Hops, node initialization | **Yes** |
| **Loss Function** | Binary Cross-Entropy (BCE) | Binary Cross-Entropy (BCE) | **Yes** \[cite: 1\] |
| **Memory Updater** | Static Linear Aggregation | **Dynamic Feature Gating** | **NO (Independent Variable)** |
| **Evaluation Hardware** | Nvidia vGPU tiêu chuẩn | Nvidia vGPU tiêu chuẩn | **Yes** |

## **14\. Attribution Logic**

Thiết kế kiến trúc và kiểm soát biến số tạo ra một chuỗi suy luận nhân quả (causal attribution logic) mạnh mẽ. Nếu kiến trúc TempoLog-MoE duy trì được F1-score ở mức cao trên hệ thống BGL (nơi đặc trưng ngữ nghĩa mang tính quyết định) và đồng thời khôi phục mạnh mẽ F1-score trên hệ thống Spirit (nơi đặc trưng ngữ nghĩa gây nhiễu và đặc trưng thời gian chi phối)1, trong khi mọi điều kiện khác (parser, CTDG structure, BCE loss) được giữ cố định, thì sự gia tăng này **chỉ có thể** xuất phát từ khả năng của mạng Gating trong việc học cách điều hướng luồng thông tin. Sự linh hoạt trong việc triệt tiêu trọng số của Semantic Expert (![][image2]) và tăng cường trọng số của Temporal Expert (![][image4]) chính là nguồn gốc của hiệu năng. Thực nghiệm E3 (Ablation) sẽ cung cấp mảnh ghép cuối cùng bằng cách vô hiệu hóa cơ chế Gating động và quan sát mô hình sụp đổ trở lại trạng thái tĩnh, xác nhận hoàn toàn giả thuyết1.

## **15\. Design Alternatives**

Thay vì đề xuất các framework phân mảnh, thiết kế xem xét 3 biến thể nội tại của cùng một định hướng nâng cấp để đảm bảo tính tối giản:

* **A — Minimal (Simple Attention):** Áp dụng cơ chế tự chú ý (Self-attention) đơn giản trên 4 đặc trưng tĩnh mà không phân ly thành các chuyên gia. Phương án này dễ hội tụ nhưng không giải quyết triệt để sự xung đột miền do không gian biểu diễn vẫn bị trộn lẫn.  
* **B — Refined (Decoupled MoE Gating \- Selected):** Phân tách rạch ròi luồng thông tin thành *Semantic Expert* (![][image8]) và *Temporal Expert* (![][image9]). Sử dụng một mạng MLP định tuyến tính toán 2 trọng số ![][image14] ngay tại mốc thời gian thực1. Đây là kiến trúc minh bạch, đơn giản và phản ánh đúng bản chất vật lý của hệ thống.  
* **C — Robust (MoE \+ Domain Adaptation Loss):** Bổ sung thêm hàm suy hao (loss function) chuyên biệt để ép buộc các chuyên gia phân ly cực đoan hơn. Tuy nhiên, phương án này bị loại bỏ do làm tăng độ phức tạp của quy trình huấn luyện và đi chệch nguyên tắc "nâng cấp tối giản có ý nghĩa" (minimal meaningful improvement).

## **16\. Final Research Design Selection**

Dựa trên phân tích tính khả thi và giới hạn vật lý của bài toán Phát hiện Sớm, phương án B được lựa chọn làm thiết kế chính thức. Bảng dưới đây tóm tắt các quyết định lõi:

| Design Choice | Selected Option | Reason |
| :---- | :---- | :---- |
| **Baseline** | TempoLog (2025) CTDG | Cấu trúc window-free tối ưu hóa chỉ số MTTD, cung cấp nền tảng xử lý luồng tốt nhất hiện nay1. |
| **Main Improvement** | MoE Dynamic Feature Gating | Khắc phục điểm yếu chí mạng (Domain Conflict) bằng một mạng MLP mỏng, bảo toàn độ trễ vi giây1. |
| **Data** | BGL, Spirit, HDFS | Đại diện xuất sắc cho các miền lỗi hoàn toàn khác biệt (compute-bound vs network-bound)1. |
| **Learning** | BCE Loss End-to-End | Giữ nguyên từ Baseline để chứng minh sự đột phá đến từ cấu trúc định tuyến, không phải do kỹ thuật tối ưu1. |
| **Inference** | Microsecond Online Streaming | Tính toán các trọng số MoE ![][image14] tức thời tại mốc sự kiện đơn lẻ1. |
| **Evaluation** | Temporal Split \+ MTTD | Ngăn chặn tuyệt đối Data Leakage và định lượng khả năng cảnh báo sớm một cách thực tế1. |

## **17\. Research Traceability Matrix**

Ma trận truy xuất đảm bảo mọi câu hỏi nghiên cứu và giả thuyết đều có phương thức đo lường và hệ thống thực nghiệm đối ứng tường minh.

| Research Element | Design Element | Experiment | Metric | Evidence of Success |
| :---- | :---- | :---- | :---- | :---- |
| **RQ1 (Tác động hàm tĩnh)** | Static Linear Aggregation | E1 (Reproduction) | False Alarm Rate (FAR), F1 | Quan sát thấy F1 sụt giảm mạnh và FAR tăng vọt trên tập Spirit so với BGL khi chạy trên nền hàm tĩnh1. |
| **RQ2 (Sự khôi phục F1)** | MoE Dynamic Gating | E2 (Main Test) | F1-Score | TempoLog-MoE duy trì F1 ở mức cao và ổn định xuyên suốt cả hệ thống BGL và Spirit. |
| **RQ3 (Độ trễ Gating)** | Mạng MLP siêu mỏng | E6 (Efficiency) | Latency (microsec) | Overhead độ trễ tính toán không đáng kể, duy trì trọn vẹn thông lượng luồng của CTDG1. |
| **H1 (Cải thiện 10% Spirit)** | Temporal Expert Routing | E2 (Main Test) | F1, PR-AUC | Mức tăng trưởng F1 trên tập Spirit của TempoLog-MoE vượt Baseline tĩnh ít nhất 10%1. |
| **H2 (Trọng số chiếm ưu thế)** | Softmax ![][image17] | E2, E3 (Ablation) | ![][image13] value log | Trong quá trình suy luận trên Spirit, mạng Gating tự động gán trọng số ![][image18]1. |
| **H3 (MTTD tăng \< 5%)** | **![][image10]** MLP complexity | E4 (Early Detection) | MTTD (ms) | Sự chênh lệch về MTTD giữa mô hình cải tiến và Baseline tĩnh không vượt quá 5%1. |

## **18\. Threats to Validity**

Thiết kế nghiên cứu cần đối diện với các rủi ro học thuật tiềm ẩn nhằm củng cố độ tin cậy của kết luận.

* **Internal Validity:** Nguy cơ lớn nhất là rò rỉ dữ liệu (Data Leakage) đã được phong tỏa hoàn toàn thông qua giao thức phân chia Temporal Split 60:40 thay cho việc xáo trộn ngẫu nhiên1. Tuy nhiên, thiên kiến tinh chỉnh (Tuning Bias) có thể phát sinh nếu mạng Gating được tối ưu siêu tham số quá mức. Để kiểm soát, cùng một learning rate và bộ tối ưu (optimizer) sẽ được áp dụng cho cả mô hình cơ sở và cải tiến.  
* **External Validity:** Hiện tượng thiên kiến điểm chuẩn (Benchmark Bias) thường xảy ra khi sử dụng các tập dữ liệu quá dễ đoán như HDFS. Bằng cách thiết lập tập Spirit (nơi có độ nhiễu mạng lưới rất cao) làm đấu trường chính, nghiên cứu chủ động thử thách tính bền bỉ (robustness) của mô hình trước biến thiên liên miền1.  
* **Construct Validity:** Việc sử dụng F1-score đơn thuần để đánh giá các hệ thống thời gian thực có thể dẫn đến sai lệch cấu trúc (Metric Mismatch). Việc tích hợp hệ đo lường MTTD và Detection Lead Time trực tiếp giải quyết lỗ hổng này1. Thêm vào đó, giả định rằng bộ phân tích cú pháp (Drain) hoạt động hoàn hảo là không thực tế. Sự xuất hiện của các "template rác" sinh ra nhiễu cấu trúc; nhưng với thiết kế MoE, Semantic Expert có nhiệm vụ học cách triệt tiêu trọng số khi phát hiện nhiễu này, bảo vệ CTDG khỏi sự phân mảnh.  
* **Conclusion Validity:** Sự biến thiên của các trọng số động học (Gating weights) ở những chu kỳ đầu huấn luyện có thể cao. Để đảm bảo kết luận thống kê vững chắc, đường cong hàm suy hao (BCE Loss curve) sẽ được giám sát chặt chẽ sự hội tụ, kết hợp với các bài kiểm tra ý nghĩa thống kê (t-test) từ 5 lần chạy độc lập1.

## **19\. Risk and Mitigation**

Để đảm bảo khả năng hoàn thành dự án trong 6-9 tháng, các rủi ro kỹ thuật và phương án dự phòng được hệ thống hóa.

| Risk | Probability | Impact | Mitigation | Fallback |
| :---- | :---- | :---- | :---- | :---- |
| **Mạng Gating MLP không hội tụ** | Thấp | Cao | Sử dụng kiến trúc mỏng (1-2 layers), tích hợp chuẩn hóa LayerNorm trước khi áp dụng Softmax. | Chuyển đổi sang sử dụng cơ chế gộp Self-attention đơn giản (Design Alternative A). |
| **Overhead độ trễ (Latency) vượt ngưỡng 5%** | Trung bình | Cao | Tối ưu hóa phép nhân ma trận của Gating; giới hạn nghiêm ngặt số chiều (hidden size) của mạng nơ-ron1. | Triển khai cơ chế tiền tính toán (pre-compute) cho các cụm đặc trưng thường xuyên xuất hiện. |
| **Baseline TempoLog không đạt F1 như báo cáo gốc** | Trung bình | Trung bình | Bám sát mã nguồn và cấu hình tham số từ tác giả hoặc tái tạo theo mô tả giấy chặt chẽ nhất. | Đánh giá dựa trên *Relative Gain* (Tăng trưởng tương đối) giữa mô hình tĩnh và động thay vì so sánh số tuyệt đối. |
| **Drain Parser sụp đổ tạo quá nhiều Log OOV** | Cao | Trung bình | Giữ nguyên cài đặt Drain tiêu chuẩn, dựa vào tính linh hoạt của Semantic Expert để tự động đánh giá thấp các đặc trưng nhiễu1. | (Không khuyến nghị đổi Parser để giữ nguyên control variable, nhưng có thể chấp nhận nhiễu như một tính năng của Robustness Test). |

## **20\. Expected Contributions**

Nghiên cứu dự kiến tạo ra những đóng góp đột phá ở ba cấp độ:

* **Scientific Contribution (Đóng góp Khoa học):** Cung cấp hệ thống bằng chứng thực nghiệm rõ ràng về cách thức các kỹ thuật Hỗn hợp Chuyên gia (MoE) có thể giải quyết bài toán dịch chuyển miền (Domain Shift) bên trong các kiến trúc Mạng Đồ thị Động (CTDG) mà không phá vỡ tính chất thời gian thực1.  
* **Methodological Contribution (Đóng góp Phương pháp luận):** Chuẩn hóa một giao thức đánh giá Phát hiện Sớm (Early Detection Evaluation Protocol) liêm chính, sử dụng Temporal Split và hệ đo lường vật lý (MTTD), kiên quyết từ bỏ việc lạm dụng Random Split gây rò rỉ dữ liệu1.  
* **Engineering Contribution (Đóng góp Kỹ thuật):** Thiết lập một kiến trúc mã nguồn mở gọn nhẹ, xử lý luồng sự kiện ở mức vi giây (microsecond throughput), sẵn sàng triển khai trên các hệ thống giám sát AIOps quy mô lớn mà không đòi hỏi tài nguyên API đắt đỏ của các Mô hình Ngôn ngữ Lớn1.

## **21\. Reproducibility**

Tính tái lập là tiêu chuẩn tối cao để đảm bảo giá trị của công trình khoa học. Toàn bộ thiết kế thực nghiệm sẽ được đóng gói và ghi chép minh bạch. Các tài nguyên sau sẽ được báo cáo chi tiết:

* Mô hình khởi tạo SBERT (tên phiên bản cụ thể và thư viện framework)1.  
* Phiên bản của thuật toán Drain parser cùng các tham số biểu thức chính quy (Regex parameters) tùy chỉnh.  
* Danh sách chính xác 5 seed ngẫu nhiên được sử dụng cho quá trình phân tách Temporal Split và khởi tạo trọng số MLP.  
* Cấu hình kỹ thuật mạng Gating: số lớp (layers), hàm kích hoạt (activation functions), và tỷ lệ Dropout.  
* Giao thức phần cứng: Cấu hình vGPU/RAM sử dụng để tính toán đo lường độ trễ (Inference Latency).  
* Mọi thông số siêu tham số (Learning rate, Batch size, Epochs, BCE weights) của cả mô hình Baseline và Improved Model. Mục tiêu là đảm bảo bất kỳ nhóm nghiên cứu độc lập nào cũng có thể tái hiện chính xác sự vượt trội của cấu trúc Gating động so với cấu trúc tuyến tính tĩnh.

## **22\. Final Checklist**

* \[x\] Một baseline 2025–2026 rõ ràng (TempoLog CTDG).  
* \[x\] Một confirmed limitation (Static Linear Aggregation gây Domain Conflict).  
* \[x\] Một main targeted improvement (MoE Dynamic Feature Gating).  
* \[x\] Baseline reproduction/reference (E1).  
* \[x\] Baseline vs Improved (E2).  
* \[x\] Ablation phù hợp (E3).  
* \[x\] Early Detection metrics (MTTD, Detection Lead Time).  
* \[x\] Controlled variables (Bảng Mục 13).  
* \[x\] Statistical validation khi cần (5 runs, t-test).  
* \[x\] Risk mitigation (Bảng Mục 19).  
* \[x\] Không tạo research topic mới (Trung thành với đề xuất đã duyệt).  
* \[x\] Không thêm technology chỉ vì trend (Đã loại bỏ RAG/LLM do latency bottleneck).  
* \[x\] Khả thi 6–9 tháng (Thiết kế MLP can thiệp cục bộ rất tinh gọn).

#### **Works cited**

> 1. result-4.md  
> 2. arXiv:2501.12166v1 \[cs.SE\] 21 Jan 2025, [https://arxiv.org/pdf/2501.12166](https://arxiv.org/pdf/2501.12166)  
> 3. Beyond Window-Based Detection: A Graph-Centric Framework for Discrete Log Anomaly Detection \- arXiv, [https://arxiv.org/html/2501.12166v1](https://arxiv.org/html/2501.12166v1)  
> 4. result-3.md  
> 5. result-1.md  
> 6. result-2.md

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAaCAYAAAA0R0VGAAAB2ElEQVR4Xu2WzStEURjGXxQLEUqhZMpHWSgLsrGwECV7VuIPkCKFnbCgbOylCAsbe7IUVspGWVr4WihZSL7e5557Z8483a8xBov51VNznuc995x7zrn3jkie/0MLGz7UqgrZzDWfbISQSW3W3Kmq2QyhWPXBZi4YUd2zaYFVWmFTOVatsvnTYPAaNl0KxOTtHChFkuPtrZPwASYkPEfWy2YQY6odVTcHAWyqXtlU+lQDYs4iJjDotplL1RmbfuAiCff3rGouFQXyrtpmU5lUTYu5JgZHGzfOYIywlXU4Up1YbXRYttpBoG6BTRfvvLVxYDEsMSb3JKZoQ1VPmcepqpw89PFbETAu0QN3SXSNtIop8vSYHjsssSGmdpRNlweJHrhTomuSNKluJH4H1M2z6YJsn01iSCLGQvjs43k0iDmT65bngbotNiV13jrcdqVqMRUnmZEYk0Nnj0PVntW+UlWJeTIZvHZe2FRKJX3QoE/VheqcTRu8BNEZF4Om0mMHPAx4spiEBN85bhLZLQcWyPvZzJSgCQBe+bh4W58VPWK2tkxVkR454BN1zWYMDlRrbH4HnKtdNi3exEw+Lviz6XeGc0YmW/SrEwM4Q81s+tCoKmEzT56/5guVj2elNBsMJwAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAaCAYAAABctMd+AAAA5klEQVR4Xu2TOwoCMRCGB6ysPICdYGljpV7BQvAENva23sFasPYMFuItLBVr8YHaWPn8hwTMzgby2ErIBx+7zJ+ZZANLlIigCkdwBmtGvWO8BzOHH7iFXViHU7iHbZ1FwY1vWJEBGJPK1zLw4UnuU3Hel0UXN1KNZRkIXJvnaJBq2sjAQvDwF6km2z0XhgcHn8iXIsMXsmBSIjX4IAML5gEmsCdqVnxO3oIDWSR3H+1ILeKvsMH1oyxqnMMZXsQ/kdygCU+iZuI1nFnR74ru+jnMrMjjPTyG/xu+hFd4hhf4yMaJRAhfjT84R2qNZTkAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAaCAYAAABctMd+AAABC0lEQVR4XmNgGAVkAGkgLgDimUCshCRuhcQmGSwG4v9AfBuIvYFYFYinAfFzILaEypEFQBr/ATE/ugQQVDJA5C+hSxAD/jAQdhVIPghdkBD4wADRyIkugQYIWY4BdBkgmm6hS2ABJBv+lwGiCVs4UwxABpPsImIBuYY/YoDoW4EuAQPMDBAFL9ElsABkB3xFYoPyw2MkPgogxuUWQJyAxAep94Cy8WasuwwQSZAvsAGQ+Ct0QSRQyoDHcBAASYIyEboFRkD8Gk0MHYD0aqILooPdDIggAoUpiE5FUYEJLgKxDrogNcACIBaHsouRxCkGmUCcxwCJ5HQg/oEiSyGABR8Mv0WVHgWjgBQAAM9vPz7suG3kAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAaCAYAAABctMd+AAABFElEQVR4XmNgGAVkAGkgLgDimUCshCRuhcQmGSwG4v9AfBuIvYFYFYinAfFzILaEypEFQBr/ATE/ugQQVDJA5C+hSxAD/jAQdhVIPghdkBD4wADRyIkugQYIWY4BdBkgmm6hS2ABJBv+lwGiCVs4UwxABpPsImIBuYbfBOL3QLwCXQIGmBkgBr9El8ACkB3wE4jdoewbQHwZSQ4FEONyCyBOQOJvAeJwKPs1A8QHWMFdBojhIF9gAyDxV+iCSACkVwBdEBmAFIAyEboFRgwQl2EDYUC8AIhnoIljBbsZEEH0FUqnoqjADiYD8W90QUoAKChhvvRkIBxnJAGQYeJQdieUTzUQxwApLpYC8Xc0uVEwCkgEADzuP0bOT6TmAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAaCAYAAABctMd+AAAA/klEQVR4XmNgGAVkAGkgLgDimUCshCRuhcQmGSwG4v9AfBuIvYFYFYinAfFzILaEypEFQBr/ATE/ugQQVDJA5C+hSxAD/jAQdhVIPghdkBD4wADRyIkugQYIWY4BdBkgmm6hS2ABJBv+lwGiCVs4UwxABpPsImIBpYa/RheAAWYGiMEv0SWwAGwOCGXALg4HxLjcAogT0AWBoIOBgN67DBAFIF9gAyDxV+iCQPAUSuM1HARACkCZCN0CIwbsYeoBxFxQNkHDQWA3AyKIvkLpVBQVCAAqa2CAKMOJBSZAvA8JgwwH0TLIiqgFqOpyGJBkgJRJb6C0Gqr0KBgFxAIAwmM8IkY6PU8AAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAcCAYAAACtQ6WLAAAAe0lEQVR4XmNgGOTAEYht0QVh4D8Qr0UXhAGQZAG6IAjoM0AkmZAFbYDYC4h3QyV9oXwwKALiEqjEWygfhFEASDIXXRAEdBkgkozoEiCwhgEiiRW8ZsAjCZLYhMTfhsQGS1pA2RlIbDAASYK8UwfEK5AlYADkeQl0wREPAGL/GMEfWDMiAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAAAXCAYAAAAIqmGLAAADyElEQVR4Xu2ZWchOQRjHH/saKYkshZQlS1L2Wxdc2F0gSyKSJSSyJUVJuSBLrpAlcSXZ4kpKKWtk/biy74Ssz9+c+d75/t+858z3nvNacn717zvv88zMc87Mc2bmzCeSk5OTk6O0VS1U7VR1cuyDnOty0Ee1XrVZ1cCxr3Ouy8Ew1TbVIrLPoN9Z0lA1SbVLNdyx11G1cn5XY6/qh+qOaoSqi5ibf6QaGPnKQYWYto+qhqgGq26qNqoOqi4XimZGS9VXMXERp6dqnOq7qrPqrWpUZensQAzE/KiaqeqomhfZMECxfQwnbrA5O5TlYvxX2ZESvLFoF4Pk47kY/xh2pGSFmHZ3sCMCvtjOKpEHYtrFm8s0lYS4NqPiyLqzGolp8zY7HJDdSfdVU/B2oM3Z7HA4ItnHPSemzWbscIDf+yK8FuNEp8WR9U3HZo1DSJlQuoppL2n6XKC6wsYUYG1H3InsIF6pRrPRZmpcNluy7KzDYtqbzA4Pl9iQAkzniFuLHQSm95FsTEFoQn5mA/gmprJvHSonoTedJd3ExHzPjjJzQEzckneof6KzsHNCTKyDvxO7c93AjjJj+7gxO0JJM0jH2BDIEjEx97AjAewEP4mpW8r3yzsxdd3vvhAmiEmou6ru5AshTR9X7smfsMODG2STmPm61MBrxNSdww4Pp5zrLc51aH2XkB0sGCuFj3Z8cOIb0YL6SesZEzpI19hgCWlggGoaGyW5XjGQyah7iB3EcVXt6LqDVI13kn6HsFtMnaS3AZsLl5fOdU1jArtZSeI+Gyz3xDSAt8oH7E/ZGBEXeKmqLhsdkpKjn8SvHZi6LpINGb6SbC7wI6b3OyQCi3x7NkZsVZ1go9JaNZWNDlPExB3PDocPbBCzw6wEDWAq4IHqq3pGNpdinTxfjA8dWQwcyaDMdXYoy1T72OiAMz1f7Bdi7EiQYuA8EmXWskM5L/6TAIDzRCRrC3ZIIeG4/1ywnqEMPnlcMJ3ieKgJ2TGDzCKbnJZCMIwq/uJcKQ5fR1kqJHn3Vl/MxxvasVPCG1UPt5AHlPOtC73FDNRDdhC9pPqzXlDVcwsVAWVxCOyCI6YbqulkZxZLIa5NqO1VShQI2ScEETdIIMlfChhUC7LTB9ayrMAmAge8FjwTEprBKXZ/NqbgbKTUxA0CpiQcwWcJTsWRrdBc8XcWfO3YmIIzYg55LXhm379rbrHhT4OdFTIaN4+dz5eq7l/gJCNLsD7aqcIKx/vMYzZkAJ5zv5gpajX5wFDVKjb+C+DY/X+hDRtycnL+Jn4C7rb3/e2MrEIAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAaCAYAAAAT6cSuAAAB9klEQVR4Xu2Xu0scURSHD0YMAcHGRqw0WIkiYuHrP0ghWKewsbARixC0shAURLAQRLFThBDSBREjWGmtiCAoYUuJbxErn7/jmWXvHu/euTOzExDmg48dzu/OOfPYWUeijIx3Rz0cgYuw0ah3G9tp0AYn4Sz8aNQnjO3YrMBneAy/wCY4D09gV5ClQY6k92/YC3vgIZyGP+BeYWk8uPkTrNEBGCPJ93WQEP6GcF8+ORvnJHm/DqLwQOF3JfEQxSeSnkc6MGih8ONyck3SgIe5SDTEAvfz6emzxkr+yriuXp7YQyz8Iun3VQcWdnXBl0eSIbbnLE1871oi/ssQxWeSmfycp0qSk1vTBU++kcxc1kEEQo/5A8mifzqwYDabgX2qFoVxkn2HdGDhjy6Q/M3zmu1z5zrhgC5S+H6l4Dce3venDhTrsELVWmEdec7+S7KQ76INrp/qYoBrwHdYqYsGYRe1A07pIskJM659i+CF/HDrE2yHZ6pmUmrAMEl2qwODWpI1BzoAo3BVF8GOsV1qtpVNKlzNu+BzsGjFW1wDchT+a1gFr0j68Gsff97AZnNRQENgHtfsshA2ICyPwhzcCtwm6c3bqeE6eP53ZUkXy4T3D0ocNki+TvzGfgnvi+NX+M0nDRZIZl+Q+5lOlWpdyMjIyHiXvADmOnxr5aKQ5gAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAaCAYAAAAT6cSuAAACMklEQVR4Xu2XPWjWUBSGD61aBMFFdHBr6yC1IMWh/nQvupWODl1EXGzBH+qkICi4uAniIkqhFLeCgnZy0skfBLFSCjoUq1JbUUTU+r6exJ6c3ib5ki9KIQ88fDfn3J/k5t4kn0hNzbpjJxyB12G7iR8w5SrYCy/Bq7DNxC+acmFuw2X4Gh6Bu+A1OAf3R7kqmBXtexIeggfhS3gFjsOnK1WLwc5/wa0+Ac6J5p/7REm4QtgvLy7EB9H8gE80wg/JviulB3FsFu1z2icM3ZJ9Xql8Eu2Ag6VRapAA7C9Pn3nqBIlnJm32YgoPEuCOaH9HfSLAEx/Iy0/RQUL7rEry3rVS/JNBHB2iY3KfV0rRi3sj2o6P6UY5Ldr2lk9ksB1+hUvwjMutolV0kHc+EcBOwBdT5vvwrTnOw3nR/k74RID7pszXFM+ZsP2gyQXJc+d64ZA5Zv3+qFzkxc4vHraZ8AnHPdhijufhxqjM9sMmF2RGtGI8Ix7G2elacHmELu4s3OCDhqxJ3Qcv+2BEp+jSzAUH4eb2F9gD37uYh213u9jJKP7ZxS3bROu88AkwCsd8MOICfAgPu3gqD2RlNrmn+HssUWM1z+AeH4yYleyn4Sa4IDoW9xN/F2GXrbQGrMt3ZSXchDui8ikTt6Qtu0bhP4RX5vixNLf/v/Apx6U3BI/Db4mswpO54YMl6JPkxXyX5JO0acTLN/ZjMv0Hfvk0m7twCj4S3RL/jS0+UFNTU7Mu+Q1FVoWY9IP92QAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAXCAYAAABnGz2mAAABuklEQVR4Xu2VzSpFURTHl28GxIAywMAziEzkIzyAYiA3A2WuJI+glGTgHTyCCRPJSEx0lQEywIBSyOda7b2v7X/3vmtfrhj41b/O+e21zl33dM4+RP/8PsMoFFo55Sg1OjjrnDVOA6yFmOUsoEzgDUWMFTLFU/a8nXPJechV5NPGuUDp0UjxAao5ryh95JZK8zYuWJ4pfgHpqwXXzDm1ay4xdjjLKB3SeILSY4BMzSD4Xs4jOEQbrIIi6+cUWfBwd3QD/BPpz5Y2mCDrQ77os3LLlwGayNTdgBdXBw5JGeyIs+cL+cfShM8IMkmmbt9z9dZppAy2SFCT0iRkydTJtuDot04j5TcmyKtpsSdakxCqmw64EKFepJu8Gvc23OeWw4yRqcOtJGO9RspgXQQ1KU2xmh4KeyTW7zNOUHOLAnCbZBUu0MebqpEymGw5eTUiDlAyV2Te2kJIr3xWCpEy2CF9fuNzXJNp3iXzzMmxPJAaUjeH0iJ7nnxDz2zkGPdBh1xnBOV3mOfcoSySMtLv6JeQi1aiLIJNzirKUjDKOUaZiHyDX1CWkiXODMoEfnQoRwaFQienBuWf5R1Vdn+F4xa9TgAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAAA1klEQVR4Xu2TPQoCQQyFo4gWXsNWLLT0BIJewloQ8RgexcrW1srKO6iwglr6U+kLMwtjEMkimyoffDCTvIXHskvkOM4/nOTgFze4lcOS2cFXohoOT+XQiBUVKNuhEK7KhRGqsn04gGsK4WG8W6MqO4NzCsFLvLPWqMrmcHAih4aoy7YpBCty8YU67Cntxmc0qMsuSRkETThSyt+/FnVZDl3l0JhCZfkny9kkZysKlW3F8zNdGMIviHs05EKyoBB8wJrYlc0dZvAA9/AIz3CchhzHcRzngzcjETkwh7m/rQAAAABJRU5ErkJggg==>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAaCAYAAABYQRdDAAAA0UlEQVR4XmNgGAWjYGgCVyDeAMR56BLkABMg/g/EDlB+FZQPA9OQ2EQBXQaIAUJo4iCx1VD2X2QJYgBI8wt0QSD4xwCRMwfiaDQ5vMCBAaLRHU0cBB4xQOSQg4EoAPIeLk3XGCBykugShEADA25DLzLgllvMAEklv9AlYACkURVN7B4Qr4XKgUAfkpwmEC+CskHhjhWAYh0Uu7Dwm4Ekdx8qFo8kpgYVA+kRQRKnCHABMS8Q9zDgDh6SgBsDqpc/IbEpAh+AeB8QH0KXGAUjHQAAIJUvQF5JpHcAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAXCAYAAADtNKTnAAAAvElEQVR4XmNgGAWjgDzgCsQbgDgPXYIYYALE/4HYAcqvgvJhYBoSGyvQZYBoEEITB4mthrL/IktgAyDFL9AFgeAfA0TOHIij0eRQgAMDRKE7mjgIPGKAyCF7CwZQxEDOxaYIBK4xQOQk0SUY0PQ0oAsggYsMmHIwl2G4EMRRRRYAgntAvBYqBwJ9SHLngNgfiQ8GoFgBhT7M9BlIcvehYvFIYuiuIwtQbIgTEF+HskGuJBv8AuLz6ILDBAAAW60vgovDjAgAAAAASUVORK5CYII=>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAXCAYAAABwOa1vAAABmklEQVR4Xu2UzytEURTHv36lRPm5sGBHUdgo29ngX1ASxU7ZKllM1rLEmh0pVnaaZDU7GyVF2VAUsZNf5zj3vjlzZm7MvFHU+9S3zv1+3zv3vXfvu0BCQkJCwl9jlLRPWrDBLzFB2iPNGP9bhkkfpJQbL7mxZ13VlWAK0n/QjQ9Ir7kYJ6ouYAByc6vx2dt19ZsOYjIL6V1tfPbmXX2uAwtfeGtN4h2SjZAmTRYH7rljTYh/T1okdZms3hcpyIXjUZTjGpLprRGXNKRfo/EZP9eDDaCegZc89EBnkKzTBjG4Q3g+/8B2q7RAVvuLNMINThHOtiGnyYsNiDlShzUdGYR7FltN7+VlXPT4geMSctz4i9ZU1kfacnX05o4hFJ/Y0wbJ6pRXQ3omHbuM0acS//D8lSP4dGDTT7SpsivnTSuv13l8T7vyPVnI0ofoR/5XW1YZ71/2/HHHhF7+xzSQmkirCDfTZ2ocmlG4iiUxhvwGT6rWXFijTFZIG64+1EEpPJKOIHuuGDekKmuWSS3ko2SMX1G6rZHwX/gEoPJmm+MVlpYAAAAASUVORK5CYII=>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAZCAYAAAA4/K6pAAAAQ0lEQVR4XmNgGAX4ACMQh6ILkgI4gbgEXZAUwAPEpeiCpABehiFlwH8SsSxEG35AkguwgZFmAHooE8LSEG2jYBRAAAAOPx2FGF9UOAAAAABJRU5ErkJggg==>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEoAAAAaCAYAAAAQXsqGAAACl0lEQVR4Xu2YTYhOURjHH8bHWJh8lSKKjZWVRpqVJCyQLFjIhgXZWVgQq9koO2ayYMFOkZBC7BAp8hWi1MxiVvL9MRPh+c85xzzv/57zvvde6W1yfvXvvc//ee655557zj13RiSTyWQydTik+qj6qtpJuVacVP1SDaoWUg68V/WqFqgmqVao7jdUjBOeqa6b+Knqtomb8VO1xsQYsHUmDh5rb0NFm1nJRoQucR1n4M1gk8As4XPXRzzE+1WnVbso11auqt6qZnMiwkMp3hiAhyXVDNRgNjLwscwCP8xxJZaojsvYE1umuqDq/lNRncmqF6rXqqmUa0ZYCkzKtyB/g01x/lETfzfHpZmgeqxaJa7BAdVmn0ODp/xxWWaq3qjuiGu7KqkBSfkW5C+xKc6/YuIRVb/qg+qMz/eYfJSzqomqDeJOWGxyh71XhkWqYdV5TlQkNSApP4B7QD52ffivTIzddK2Jl4urmWW8Agf9710pduRcxGOwTLHT9HGiJqkBSfkW5PHKYODfZJNADQawJSh8HvFadQ5bMWoOcKImqWumfAvy19gU558wMd6fTJn2R0HR1og3RF6KMLOOcaIinyTe4diDZFCT2vXCvW338b6x9CilBirMCss273WS3wp8CX8Rt2zrsEWKfQHw8DAsPIsxSHxueP8Edvh4vvEAvJfkFcAOhUJ8nIHwYkSn6zJd3Gy8xYkS4Nq7TXzEe5Z33ttjPLyM+eFihvKfJ9zW5YgXJYzmE3/8WTWvoaI+HaoH4tqfQrkU08T1457qkbjdlD81lor7RmNWizv3orjBxCRg5oirwecBfr9Jsf0oKMZS+9f8zQxtOxul5LT738G/HMJan0u5jAFrGrveJim5TjOZTCaTGZf8BqtNtgh8KhRfAAAAAElFTkSuQmCC>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAXCAYAAABXlyyHAAABM0lEQVR4XmNgGAWjYBSMglEwCvjRBYY76ADiP0Csjy4xGIArEG8A4jx0CSqAMiD+D8S+6BIDAUwYII5xgPKroHwYmIbEphTEMEDMzkaXoBfQZYA4QAhNHCS2Gsr+iyxBJeDMALEDlOTpCkCWvkAXBIJ/DBA5cyCORpOjJtAB4t9APAtdghbAgQHiKXc0cRB4xACRQ07aMIBNjFwgAcSfgHgbugQtACjJ4nL8NQaInCS6BANuPaQALQZIzM5Dl6AlaGDA7fiLDJhysBjHFfPEACcGiN4mdAl6AZDlqmhi94B4LVQOBPqQ5M4BsT8Sn1gAK53T0CXoDUClM6gUhsXaDCS5+1CxeCQxUmMWVKeD9HihSwwVQKqH9dAFhhIA5b/rUDYo9kcE+AXE59EFR8EoGAV0BwDMN0FD87rMJwAAAABJRU5ErkJggg==>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAXCAYAAAC74kmRAAABg0lEQVR4Xu2WL0gEQRTGP1GTYLAdBouCcNgE27EIIlgEwaLBbLEZtGgXjP5pdhFEo2YxKRYtomASNN1hEf+9x9uR8dOFW91dPW9+8MHt73E7NzNv5xYIBAKBQCBPapIllsKrpMLyvzIEm/AE+QXJk6Sb/K8yItmVzHEhA2ZhC9FPfltyJ2knXyiDsB8XxdeL8bVjzfv8UzZhj0YH+QvJMblCGIBNtou8Ot0d5dkvZMSR5JycLkpVsk4+V3SityyFF1hNn+FpqmVFG2zsLfK9sLHzGvedCDbQKHnlBlbzHwXHV+47tMDGOSSvB6N23Tz5zNEWT5qMtqfWSlxA8nfSsAc7/LQLHK2wjtj3XK4sI3kyZ/hccx2R1Bn1oAes7i7//R1ILmFdUSg6kT5yV5KduKaserUTybh3XS9jsPtF5FckD5JO8oWhp7/uiNvVDa92HbsZz6Xd+R7YgcrvFlOwe5XJ/3nSLMA9Pi6oQ+8xybIRGIa9sCjaHU3Jo+SUZSAQaDjeAMl6VHdP6e3MAAAAAElFTkSuQmCC>