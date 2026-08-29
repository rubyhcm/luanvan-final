# **Thiết Kế Nghiên Cứu: Tối Ưu Hóa Phương Pháp Phát Hiện Sớm Bất Thường Dữ Liệu Log Bằng Cơ Chế Phân Giải Độ Bất Định Dựa Trên Sinh Tăng Cường Truy Xuất (RAG)**

## **1\. Research Design Consistency Check**

Thiết kế nghiên cứu này được xây dựng dựa trên nguyên tắc kiểm soát thực nghiệm khắt khe, nhằm đảm bảo sự nhất quán tuyệt đối giữa các phát hiện từ quá trình rà soát tài liệu, các giới hạn đã được xác nhận của phương pháp cơ sở, và hướng cải tiến có mục tiêu được đề xuất. Mục tiêu tối thượng của quá trình này là kiến tạo một khung đánh giá minh bạch, tuân thủ tiêu chuẩn của các tạp chí và hội nghị khoa học hàng đầu (Q1/Q2), đồng thời duy trì sự trung thành với hồ sơ đề xuất (Proposal) đã được phê duyệt. Sự nhất quán này không chỉ bảo vệ giá trị học thuật của nghiên cứu mà còn đảm bảo tính khả thi khi triển khai trong thực tiễn công nghiệp.  
Việc đánh giá tính nhất quán được hệ thống hóa thông qua một ma trận đối chiếu, trong đó mỗi thành phần của thiết kế đều được kiểm định chéo với các bằng chứng xuất bản chính thức trong giai đoạn 2023–2026. Phương pháp cơ sở được lựa chọn là mô hình LogOW (A Semi-Supervised Log Anomaly Detection Model in Open-World Setting), một công trình đã qua bình duyệt khắt khe và công bố trên tạp chí *Journal of Systems and Software*1. Sự lựa chọn này hoàn toàn đáp ứng rào chắn kiểm định chất lượng nghiêm ngặt.

| Thành phần thiết kế | Ghi nhận từ hồ sơ đề xuất (result-4) | Diễn giải thiết kế kiến trúc | Kiểm định xuất bản Q1/Q2 (2023-2026) | Trạng thái |
| :---- | :---- | :---- | :---- | :---- |
| **Baseline (Mô hình cơ sở)** | Kế thừa LogOW, một mô hình học bán giám sát cho môi trường thế giới mở1. | Tái sử dụng nguyên vẹn mạng nơ-ron Bayes và hệ thống biểu diễn không gian vector của LogOW. | Tạp chí: *Journal of Systems and Software*. SCImago SJR 2024: 0.975 (Q1). Năm: 2024/2025. Có DOI và mã nguồn Zenodo2. | Nhất quán |
| **Confirmed Limitation** | Bão hòa cảnh báo giả (Alert Fatigue) do sự cô lập tri thức khi đối mặt với trượt dạt khái niệm3. | Cơ chế ước lượng độ bất định hoạt động chính xác về mặt toán học nhưng thiếu ngữ cảnh ngoại vi để phân giải ranh giới giữa cập nhật hợp lệ và lỗi6. | Các nghiên cứu từ 2024-2026 xác nhận giới hạn về bão hòa cảnh báo của mô hình tĩnh khi thiếu bối cảnh cấu hình8. | Nhất quán |
| **Targeted Improvement** | Mô-đun RAG-SLM phân loại có điều kiện (Conditional RAG-SLM Triage)3. | Thiết lập cổng quyết định hậu xử lý. RAG/SLM chỉ được triệu gọi khi mức Entropy của mạng nơ-ron vượt ngưỡng động3. | Tuân thủ nguyên tắc can thiệp tách rời (decoupled intervention), không xâm lấn vào luồng suy luận gốc của mạng học sâu3. | Nhất quán |
| **Research Questions** | Đánh giá năng lực giải quyết cảnh báo giả và bảo toàn thời gian dẫn trước của RAG-SLM3. | Lượng hóa sự cải thiện của tỷ lệ dương tính giả (FPR) trên dữ liệu chưa từng thấy và sự ổn định của DLT3. | Trục nghiên cứu cốt lõi được giữ nguyên, tập trung vào khả năng chẩn đoán sớm trong môi trường CI/CD. | Nhất quán |
| **Hypotheses** | Giảm thiểu 99% cảnh báo giả vùng biên; duy trì độ trễ thấp cho 95% dữ liệu tĩnh3. | 95% sự kiện log được xử lý qua luồng nóng (hot path) nơ-ron, 5% qua luồng lạnh (cold path) SLM10. | Thiết kế thực nghiệm sẽ đo lường nghiêm ngặt độ trễ cấp mili-giây để kiểm chứng giả thuyết hệ thống. | Nhất quán |
| **Main Metrics** | Thời gian dẫn trước (DLT), Chân trời cảnh báo (EWH), FPR, F1-Score, Độ trễ3. | Xây dựng khung đo lường động học chuyên biệt cho bài toán Early Log Anomaly Detection (ELAD)6. | Chỉ số DLT khắc phục triệt để lỗ hổng của các phương pháp đánh giá tĩnh (như F1 thuần túy) trên dữ liệu đã hoàn tất6. | Nhất quán |
| **Main Dataset** | BGL và Thunderbird/Spirit, áp dụng kỹ thuật chia cắt theo thời gian (Chronological Split)3. | Bác bỏ hoàn toàn tập dữ liệu tĩnh HDFS. Sử dụng chuỗi thời gian thực để mô phỏng trượt dạt khái niệm5. | Chronological split được chứng minh là phương pháp duy nhất chống lại sự rò rỉ dữ liệu tương lai (Data Leakage)15. | Nhất quán |

Sự đối chiếu chi tiết trong ma trận trên khẳng định thiết kế nghiên cứu không tự ý mở rộng phạm vi hay phát minh ra các rào cản không tồn tại. Mọi quyết định kiến trúc đều dựa trên nền tảng của một baseline Q1 duy nhất, hướng tới một điểm nghẽn đã được xác nhận, và sử dụng một kỹ thuật can thiệp duy nhất có khả năng định lượng rõ ràng.

## **2\. Existing Baseline Reconstruction**

Quá trình tái lập phương pháp cơ sở LogOW đòi hỏi sự bóc tách chi tiết luồng xử lý dữ liệu nguyên thủy, nhằm thiết lập một hệ quy chiếu (reference target) chuẩn xác. Việc mô tả cấu trúc của LogOW được thực hiện độc lập, hoàn toàn không pha trộn các cải tiến RAG được đề xuất sau này, để đảm bảo tính minh bạch trong việc đánh giá sự đóng góp của thành phần mới. Kiến trúc của LogOW tuân theo một chuỗi vận hành tuần tự từ khi tiếp nhận dữ liệu thô cho đến khi đưa ra quyết định phân loại sự kiện.  
Luồng dữ liệu đầu vào (Input) của hệ thống bao gồm các chuỗi log thô được sinh ra liên tục từ các hệ thống vi dịch vụ hoặc cụm máy chủ điện toán đám mây. Do bản chất của môi trường tích hợp và triển khai liên tục (CI/CD), luồng dữ liệu này chứa đựng sự pha trộn phức tạp giữa các thông điệp hệ thống tĩnh và các tham số biến động như địa chỉ IP, định danh người dùng, và mã tiến trình1. Bước tiếp theo là Tiền xử lý và Phân tích cú pháp (Preprocessing/Parsing), nơi hệ thống áp dụng các bộ phân tích cú pháp tự động (thường là Drain hoặc Spell) để trích xuất cấu trúc cốt lõi của thông điệp, loại bỏ các biến số nhiễu và định hình các mẫu log (Log Templates hoặc Log Keys). Quá trình này giúp chuẩn hóa ngôn ngữ máy thành một tập hợp từ vựng có thể tính toán được6.  
Sau khi dữ liệu được phân tích cú pháp, khối Biểu diễn ngữ nghĩa (Representation) chuyển hóa các mẫu log này thành một không gian vector liên tục (continuous semantic embeddings). Khác với các phương pháp lập chỉ mục tần suất (như TF-IDF) vốn phá hủy trật tự thời gian, LogOW duy trì cấu trúc không gian của các sự kiện để bảo tồn khoảng cách ngữ nghĩa giữa các mẫu log tương đồng, cho phép mô hình nhận diện sự thay đổi trạng thái dù cấu trúc câu có sự xê dịch nhẹ1. Tiếp đó, khối Mô hình hóa Chuỗi (Sequence/Context Modeling) áp dụng cơ chế cửa sổ trượt (Sliding Windows) trên dòng thời gian. Mỗi cửa sổ trượt chứa một chuỗi các sự kiện đã được mã hóa vector, cung cấp bối cảnh cục bộ cho mạng nơ-ron học bán giám sát dự đoán trạng thái tiếp theo của hệ thống3.  
Trái tim của phương pháp cơ sở nằm ở mô hình cốt lõi với khả năng Định lượng Độ bất định (Uncertainty Estimation). Để xử lý sự trượt dạt khái niệm trong môi trường thế giới mở, mạng nơ-ron của LogOW được tích hợp cơ chế Monte Carlo Dropout (MCD) nhằm xấp xỉ suy luận của mạng nơ-ron Bayes (Bayesian Neural Networks). Thông qua việc duy trì Dropout trong cả quá trình huấn luyện và suy luận, mô hình thực hiện nhiều đường truyền ngẫu nhiên (stochastic forward passes) cho cùng một đầu vào, tạo ra một phân phối xấp xỉ của các dự đoán thay vì một giá trị xác định duy nhất19. Cơ chế này cho phép tính toán phương sai dự đoán hay Entropy (Predictive Entropy). Sự bất định này, chủ yếu là bất định nhận thức (Epistemic Uncertainty), phản ánh mức độ thiếu tự tin của mô hình khi đối mặt với dữ liệu ngoài phân phối (Out-of-Distribution \- OOD) chưa từng xuất hiện trong tập huấn luyện7.  
Dựa trên giá trị Entropy thu được, khâu Quyết định (Decision) của hệ thống áp dụng một ngưỡng động ![][image1]. Khi giá trị Predictive Entropy của một chuỗi sự kiện vượt qua ngưỡng ![][image1], hệ thống đưa ra phán quyết rằng đây là một sự dịch chuyển thế giới mở (Open-world shift). Đầu ra (Output) của mô hình tại thời điểm này không chỉ là nhãn nhị phân bình thường/bất thường cứng nhắc, mà bao gồm một cờ "Bất định" (Uncertainty Flag), đánh dấu chuỗi sự kiện này cần sự can thiệp và phân tích thủ công từ phía các chuyên gia vận hành hệ thống3. Phương pháp cơ sở này hoàn toàn không sở hữu bất kỳ mô-đun Truy xuất, Tri thức, hay Suy luận ngôn ngữ tự nhiên nào (Retrieval/Knowledge/Reasoning/Memory). Sự cô lập khép kín trong không gian telemetry tĩnh chính là đặc tính vận hành cốt lõi của LogOW.

## **3\. Targeted Improvement Definition**

Thông qua việc giải phẫu cấu trúc của mô hình LogOW, giới hạn cốt lõi đã được định vị rõ ràng tại khâu đưa ra quyết định hậu xử lý. Dù cấu trúc toán học Bayes phân lập rất xuất sắc các mẫu dữ liệu OOD, sự thiếu hụt tri thức ngoại vi khiến mô hình không thể hoàn thành chu trình tự động hóa, tạo ra điểm nghẽn nghiêm trọng về mặt vận hành.

| Thành phần hệ thống | Cấu trúc Baseline (LogOW) | Bằng chứng học thuật (Q1/Q2) | Giới hạn đã được xác nhận (Limitation) | Cải tiến nhắm mục tiêu (Targeted Improvement) | Hiệu ứng kỳ vọng (Expected Effect) | Cơ sở bằng chứng (Evidence Base) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Quy trình Hậu xử lý (Decision Output)** | Gắn cờ "Bất định" và phó mặc cho chuyên gia phân tích thủ công3. | *Journal of Systems and Software*, Q1 (SJR 0.975), 2024/20252. | **Bão hòa cảnh báo và Cô lập tri thức:** Mô hình sinh ra cảnh báo giả khổng lồ khi hệ thống nâng cấp do thiếu bối cảnh cấu hình5. | **Conditional RAG-SLM Triage:** Kích hoạt mô-đun truy xuất RAG và LLM nhỏ để tự động phân loại khi Entropy vượt ngưỡng3. | Giảm mạnh tỷ lệ dương tính giả (FPR) đối với dữ liệu vùng biên, tối ưu hóa thời gian dẫn trước (DLT)3. | Năng lực giảm cảnh báo giả của RAGLog trong hệ thống chẩn đoán8. |

Cơ chế nhận thức (Conceptual Mechanism) của sự cải tiến này được thiết lập dựa trên một chuỗi nhân quả chặt chẽ. Khi mô hình LogOW vấp phải hiện tượng trượt dạt khái niệm do một bản cập nhật CI/CD, mạng nơ-ron Bayes đẩy mức Predictive Entropy lên cao, đánh dấu sự bất định của hệ thống (Baseline limitation). Hệ thống lập tức nhận diện sự thiếu hụt ngữ cảnh về các thay đổi cấu trúc gần đây (Missing Context). Một truy vấn tự động được sinh ra dựa trên chuỗi log đang bị mắc kẹt (Query) và đưa vào Cơ sở dữ liệu Vector chuyên dụng, nơi lưu trữ lịch sử mã nguồn, Git Commits, và Sổ tay vận hành (Retrieval Corpus). Kiến trúc RAG tiến hành truy xuất các tài liệu liên quan nhất (Retrieval) và tiêm chúng vào vùng ngữ cảnh của một Mô hình Ngôn ngữ Nhỏ (Context Injection). Cuối cùng, SLM tự động suy luận và phân loại chuỗi log là "Bản cập nhật hợp lệ" hay "Suy thoái hệ thống thực sự", qua đó khôi phục luồng tự động hóa và triệt tiêu đến 99% các báo động mù quáng (Detection Effect)3.

## **4\. Overall Research Architecture**

Kiến trúc nghiên cứu tổng thể được thiết kế nhằm hiện thực hóa nguyên lý nâng cấp tăng cường có mục tiêu, trong đó sự toàn vẹn của mô hình cơ sở được bảo vệ tuyệt đối. Hệ thống áp dụng cấu trúc **Baseline \+ Targeted Improvement**, phân tách rõ ràng các thành phần được kế thừa và các mô-đun được cấy ghép mới. Việc bảo vệ sự tách biệt này nhằm đảm bảo mọi sự gia tăng về hiệu năng phát hiện sớm đều có thể được quy kết trực tiếp cho cơ chế RAG-SLM.  
Dữ liệu đầu vào (Data) kế thừa trọn vẹn đặc tính của các luồng log chuỗi thời gian từ các kiến trúc vi dịch vụ phân tán, đóng vai trò là mạch máu cung cấp thông tin cho toàn bộ quy trình. Thành phần Tiền xử lý (Preprocessing) và Biểu diễn ngữ nghĩa (Representation) cũng được **Inherited** (kế thừa) không thay đổi, sử dụng các bộ phân tích cú pháp tĩnh và không gian vector học sâu nhằm duy trì sự ổn định của cấu trúc dữ liệu đầu vào. Trái tim phân tích dữ liệu telemetry thô, Mô hình Cơ sở (Baseline Model), bao gồm mạng nơ-ron học bán giám sát và cơ chế Monte Carlo Dropout, được **Inherited** hoàn toàn, tiếp tục thực thi nhiệm vụ theo dõi xác suất chuyển tiếp trạng thái.  
Thành phần Phát hiện (Detection) được **Modified** (sửa đổi) nhẹ nhàng bằng việc mở thêm một ngã rẽ logic (Decision Fork) tại cổng kiểm tra giá trị Entropy, không làm thay đổi cách thức tính toán toán học bên trong. Toàn bộ các mô-đun liên quan đến xử lý ngôn ngữ và tri thức ngoại vi đều là thành phần **New** (mới). Tri thức (Knowledge) được định hình qua kho dữ liệu tài liệu thiết kế, lịch sử Git Commits và Runbooks. Cơ chế Truy xuất (Retrieval) sử dụng hệ thống cơ sở dữ liệu Vector áp dụng kỹ thuật tìm kiếm lai (Hybrid Search) kết hợp từ khóa chính xác và đối sánh ngữ nghĩa. Ngữ cảnh (Context) được cấu trúc qua hệ thống Prompt Engineering nhằm khóa chặt không gian suy luận. Mô hình Nền tảng (Foundation Model) sử dụng một Mô hình Ngôn ngữ Nhỏ (SLM), điển hình như Llama-3-8B-Instruct, chạy cục bộ. Khả năng Suy luận (Reasoning) được thể hiện qua quá trình tự động phân loại (Auto-Triage) của SLM đối với các sự kiện bất định. Cuối cùng, hệ mét Phát hiện Sớm (Early Detection) được **New** thiết lập để liên tục đánh giá khoảng đệm thời gian cảnh báo, cùng với tính năng Báo cáo/Giải thích (Alert/Explanation) là một thành phần **Optional** (tùy chọn) cung cấp tóm tắt gốc rễ sự cố do SLM sinh ra. Sự thiết kế rạch ròi này giải quyết triệt để yêu cầu: *phần mô hình hóa toán học của Baseline được giữ nguyên*, và *phần phân giải logic ở vùng biên phân phối dữ liệu được cải thiện*.

## **5\. Data Pipeline**

Thiết kế luồng dữ liệu (Data Pipeline) vạch ra hành trình biến đổi của thông tin, từ các luồng sự kiện phân tán cho đến khi một quyết định cảnh báo sớm được ban hành. Mỗi giai đoạn trong đường ống này phục vụ một mục đích chuyên biệt và có mối liên kết hữu cơ với mô hình cơ sở.  
Giai đoạn đầu tiên, **Raw Logs ![][image2] Chronological Split ![][image2] Parsing ![][image2] Windowing**, nhận đầu vào là các tập dữ liệu hệ thống thô. Dữ liệu được chia tách nghiêm ngặt theo dòng thời gian thực để loại bỏ rò rỉ dữ liệu (data leakage)5, sau đó đi qua bộ phân tích cú pháp để trích xuất các template cốt lõi. Đầu ra của giai đoạn này là các chuỗi cửa sổ thời gian cố định, duy trì nguyên vẹn trật tự nhân-quả. Giai đoạn này hoàn toàn kế thừa từ baseline, với mục đích chuẩn hóa ngôn ngữ máy.  
Giai đoạn tiếp theo, **Continuous Representation ![][image2] LogOW BNN Inference**, chuyển hóa các chuỗi template thành ma trận nhúng vector và đẩy vào mạng nơ-ron học bán giám sát. Mô hình thực hiện các đường truyền ngẫu nhiên (stochastic forward passes) để tính toán phương sai dự đoán (Entropy). Đầu ra là một điểm số bất định cho mỗi cửa sổ trượt. Mục đích của khâu này là khoanh vùng các mẫu dữ liệu OOD (Out-of-Distribution) mang tính rủi ro6.  
Điểm can thiệp cấu trúc xuất hiện tại giai đoạn **Conditional Switch ![][image2] Targeted Improvement (RAG-SLM Triage)**. Hệ thống liên tục giám sát điểm Entropy. Nếu giá trị nằm trong ngưỡng an toàn, chuỗi sự kiện được phân loại ngay lập tức và tiếp tục vòng lặp (Hot Path). Ngược lại, nếu điểm Entropy vượt ngưỡng, chuỗi log bị đóng băng và chuyển hướng sang luồng lạnh (Cold Path). Tại đây, chuỗi log bất định đóng vai trò là truy vấn, kích hoạt hệ thống RAG truy xuất tài liệu nội bộ và tiêm vào SLM. SLM sinh ra phân loại cuối cùng dưới dạng JSON có cấu trúc. Mục đích của giai đoạn này là bù đắp sự thiếu hụt ngữ cảnh ngoại vi nhằm triệt tiêu báo động giả5.  
Giai đoạn cuối cùng, **Detection ![][image2] Early Detection Evaluation ![][image2] Alert**, tổng hợp kết quả phân loại từ cả hai luồng xử lý. Nếu một sự kiện suy thoái thực sự được xác nhận, hệ thống phất cờ cảnh báo cùng với bản giải thích nguyên nhân gốc rễ, đồng thời ghi nhận nhãn thời gian để phục vụ cho việc tính toán hệ mét thời gian dẫn trước (Detection Lead Time) phục vụ công tác đánh giá.

## **6\. Temporal Data Design**

Do bản chất của bài toán hướng tới mục tiêu Phát hiện Sớm Bất Thường Dữ Liệu Log (Early Log Anomaly Detection \- ELAD), việc thiết lập một kỷ luật dữ liệu thời gian (Temporal Data Design) vững chắc là yếu tố sống còn. Sự vi phạm kỷ luật này sẽ dẫn đến hiện tượng rò rỉ dữ liệu tương lai, làm sụp đổ hoàn toàn tính hợp lệ của các kết luận nghiên cứu.  
Trật tự nhân-quả của các sự kiện (Timestamp/Order) được bảo tồn ở mức độ tuyệt đối. Mọi kỹ thuật tiền xử lý có tính chất xáo trộn ngẫu nhiên (Random Shuffle) thường thấy trong phân loại hình ảnh đều bị nghiêm cấm, bởi chúng cho phép mô hình học được các trạng thái tương lai để dự đoán hiện tại14. Khung quan sát của mô hình được giới hạn trong một Cửa sổ Quan sát (Observation Window) có kích thước cố định, trượt dọc theo dòng thời gian của hệ thống. Khối lượng dữ liệu bên trong cửa sổ này tạo thành bối cảnh phân tích cục bộ (Context Window) để mạng nơ-ron đánh giá sự chuyển tiếp trạng thái.  
Đối với việc đo lường năng lực cảnh báo, khái niệm Chân trời Dự báo (Prediction Horizon) và Thời gian Dẫn trước (Lead Time) được đặc tả rõ ràng bằng toán học. Gọi ![][image3] là nhãn thời gian ghi nhận sự cố sụp đổ hệ thống (Failure onset), được trích xuất từ báo cáo lỗi vật lý23. Gọi ![][image4] là nhãn thời gian mà kiến trúc kết hợp LogOW-RAG phát lệnh cảnh báo sớm dựa trên các triệu chứng suy thoái tĩnh lặng. Thời gian dẫn trước cảnh báo (Detection Lead Time \- DLT) được xác định bằng công thức ![][image5]6. Một hệ thống cảnh báo sớm thành công phải duy trì được ![][image6] ở mức có ý nghĩa thực tiễn, tạo ra không gian thời gian đủ lớn cho kỹ sư can thiệp.  
Đặc biệt, để kiểm soát chặt chẽ sự rò rỉ thông tin trong mô-đun sinh tăng cường truy xuất, nguyên tắc Sẵn sàng Tri thức theo Thời gian (Temporal Availability Control) được áp dụng. Toàn bộ kho lưu trữ Git Commits và Runbooks đều được gắn nhãn thời gian (![][image7]). Khi hệ thống phát lệnh truy vấn RAG tại thời điểm ![][image4], bộ lọc thời gian sẽ tự động loại bỏ mọi tài liệu có ![][image8]. Kỹ thuật này triệt tiêu hoàn toàn rủi ro mô hình sử dụng các báo cáo gỡ lỗi sự cố (post-mortem reports) được viết sau khi hệ thống đã sập để "dự báo" lại chính sự cố đó, đảm bảo tính trung thực của mọi chỉ số đo lường.

## **7\. Knowledge / Retrieval Design**

Kiến trúc Sinh tăng cường bằng truy xuất (RAG) được thiết kế đặc thù để đối phó với hiện tượng trượt dạt khái niệm, cung cấp chiếc cầu nối ngôn ngữ tự nhiên giữa dữ liệu telemetry thô và trí tuệ vận hành hệ thống.  
Kho tri thức (Knowledge Corpus) được xây dựng dựa trên sự tổng hợp của các tệp cấu hình môi trường, lịch sử lưu vết mã nguồn (Git Commits), sổ tay kỹ thuật (System Runbooks), và hồ sơ các sự cố đã được giải quyết trong quá khứ3. Việc tạo lập truy vấn (Query Formulation) diễn ra tự động khi mạng Bayes của LogOW phát tín hiệu phương sai dự đoán vượt ngưỡng. Hệ thống sẽ nối tiếp (concatenate) các mẫu log trong cửa sổ trượt đang bị đóng băng thành một chuỗi truy vấn đặc tả trạng thái bất định của hệ thống3.  
Để giải quyết bài toán Lệch chuẩn Không gian nhúng (Embedding Mismatch) vốn thường xảy ra khi áp dụng các bộ mã hóa văn bản tự nhiên chung chung cho dữ liệu kỹ thuật, cơ chế Truy xuất (Retrieval) ứng dụng kỹ thuật tìm kiếm lai (Hybrid Search). Kỹ thuật này kết hợp đối sánh từ khóa chính xác BM25 (để bảo toàn các giá trị định danh như IP, mã lỗi Hexadecimal) với các bộ mã hóa ngữ nghĩa chuyên biệt cho mã nguồn (Code-specific Dense Embeddings)5. Quá trình Xếp hạng và Lọc (Ranking/Filtering) đánh giá độ tương đồng Cosine của các tài liệu truy xuất được, đồng thời áp dụng hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty) nhằm tự động hạ cấp mức độ ưu tiên của các tài liệu đã quá cũ (stale knowledge), đảm bảo SLM luôn nhận được ngữ cảnh vận hành tươi mới nhất3.  
Kích thước ngữ cảnh (Context Size) được giới hạn ở mức 3 đến 5 tài liệu liên quan nhất. Việc kiểm soát chặt chẽ luồng thông tin này ngăn chặn hiện tượng quá tải ngữ cảnh (Lost-in-the-middle) khiến LLM bỏ sót các chỉ dẫn quan trọng24. Bằng việc tiêm chính xác bối cảnh lịch sử của một đợt nâng cấp mã nguồn hoặc một quy trình cấu hình hợp lệ vào prompt của SLM ngay tại thời điểm độ bất định bùng phát, kiến trúc RAG đã trực tiếp vá lại lỗ hổng "cô lập tri thức" của baseline LogOW.

## **8\. Foundation Model / Learning Design**

Mô hình nền tảng (Foundation Model) được cấy ghép vào hệ thống không đóng vai trò như một cỗ máy phân tích dữ liệu toàn năng quét qua hàng triệu dòng log thô, mà hoạt động như một Tác tử Phân loại (Triage Agent) cấp cao, chuyên biệt xử lý các điểm nghẽn logic vùng biên5.  
Lựa chọn mô hình hướng tới các Mô hình Ngôn ngữ Nhỏ (Small Language Models \- SLM) với quy mô dưới 10 tỷ tham số, cụ thể là Llama-3-8B-Instruct hoặc Qwen2.5-7B, áp dụng kỹ thuật lượng tử hóa 4-bit (4-bit quantization) để tối ưu hóa chi phí bộ nhớ VRAM25. Các mô hình này thể hiện năng lực lập luận và tóm tắt vượt trội trong khi vẫn duy trì được khả năng vận hành mượt mà trên phần cứng GPU cục bộ phổ thông (như RTX 3090/4090)25.  
Định hướng thiết kế học máy (Learning Design) loại bỏ hoàn toàn quá trình Tinh chỉnh (Fine-tuning) đối với SLM3. Việc phải liên tục tinh chỉnh lại trọng số của LLM mỗi khi hệ thống có một bản cập nhật CI/CD mới không chỉ gây lãng phí tài nguyên khổng lồ mà còn phá vỡ tính tổng quát hóa của toàn bộ kiến trúc giám sát. Thay vào đó, hệ thống khai thác sức mạnh của Học trong ngữ cảnh (In-context Learning) thông qua cấu trúc Prompt Engineering khắt khe. Đầu vào (Input) của SLM bao gồm các Chỉ thị hệ thống (System Instructions) buộc mô hình phải suy luận giới hạn, kết hợp với Tài liệu truy xuất được từ RAG, và Cửa sổ log bất định. Đầu ra (Output) được định dạng cứng dưới dạng JSON chứa hai trường: quyết định phân loại (Benign Update hoặc Early Anomaly) và lý do giải thích ngắn gọn8. Thiết kế này khẳng định thành phần LLM chỉ là công cụ thực thi logic dựa trên cơ chế truy xuất có điều kiện, giữ cho độ phức tạp nghiên cứu nằm trong biên độ khả thi.

## **9\. Inference Strategy**

Chiến lược Suy luận (Inference Strategy) được kiến trúc hóa theo mô hình phân luồng kép (Dual-path Inference), nhằm giải quyết bài toán nan giải về sự đánh đổi giữa trí thông minh của AI tạo sinh và độ trễ khắt khe của các hệ thống thời gian thực (real-time SLAs)10.  
Toàn bộ quá trình quét luồng log thời gian thực được thực hiện thông qua **Luồng Nóng (Hot Path)**. Mỗi cửa sổ log (Context Window) trượt qua hệ thống đều được nạp thẳng vào mạng nơ-ron học bán giám sát LogOW để tiến hành xấp xỉ Bayes thông qua Monte Carlo Dropout. Nhờ sự tối ưu hóa của kiến trúc mạng nhẹ, độ trễ tính toán cho mỗi cửa sổ trượt ở luồng này duy trì dưới mức 5 mili-giây (\< 5ms)10. Nếu phương sai dự đoán (Predictive Entropy) nằm dưới ngưỡng an toàn ![][image1], hệ thống đưa ra quyết định cảnh báo hoặc bỏ qua ngay lập tức, hoàn tất chu trình ở tốc độ cực cao.  
**Luồng Lạnh (Cold Path)** chỉ được kích hoạt đối với các sự kiện vùng biên. Khi một luồng log chứa các từ vựng mới sinh ra mức Entropy ![][image9], nó bị tạm giữ và đẩy sang luồng lạnh. Tại đây, mô-đun RAG-SLM bắt đầu thực thi truy vấn cơ sở dữ liệu Vector và tiến hành sinh văn bản tự động phân loại (Auto-triage). Do phải đi qua engine vLLM và các giao thức mạng, luồng lạnh tiêu tốn khoảng 500ms đến 1200ms cho mỗi cửa sổ log.  
Sức mạnh của chiến lược phân luồng này nằm ở hiệu quả phân bổ tài nguyên. Do sự trượt dạt khái niệm OOD chỉ xảy ra ở mức xấp xỉ 5% tổng dung lượng dữ liệu, 95% sự kiện hệ thống vẫn được xử lý ở tốc độ dưới 5ms5. Độ trễ trung bình của toàn hệ thống (P99 Latency) được bảo vệ vững chắc, thỏa mãn hoàn toàn các yêu cầu vận hành trực tuyến (online) của nền tảng AIOps công nghiệp, trong khi vẫn sở hữu khả năng giải quyết các sự cố mù mờ (latency-tolerant steps) phức tạp nhất.

## **10\. Experimental Design**

Thiết kế thực nghiệm (Experimental Design) được xây dựng theo một lộ trình đối chứng và cắt lớp nghiêm ngặt, bao gồm 7 kịch bản thử nghiệm (E1 \- E7) nhằm định lượng và bảo vệ tính nhân quả của mọi phát hiện khoa học.  
**E1 — Baseline Reproduction (Tái lập Mô hình Cơ sở):** Thực nghiệm khởi đầu bằng việc tái lập nguyên vẹn mô hình LogOW dựa trên mã nguồn mở từ Zenodo17. Mục tiêu là xác nhận năng lực đo lường độ bất định thông qua xấp xỉ Bayes và phô bày rõ ràng điểm nghẽn: sự bùng nổ của tỷ lệ cảnh báo giả (Alert Fatigue) khi đưa luồng dữ liệu trượt phân phối vào môi trường Open-world. Kết quả tái lập (Reproduced result) về các chỉ số F1 tĩnh và False Positive Rate (FPR) trên tập OOD logs sẽ được báo cáo và đối chiếu sự sai lệch (deviation) so với công bố gốc1.  
**E2 — Main Improvement Test (Thử nghiệm Cải tiến Cốt lõi):** Đây là cuộc đối đầu trực tiếp giữa **Original Baseline (LogOW)** và **Improved Baseline (LogOW \+ Conditional RAG-SLM Triage)**. Kịch bản mô phỏng sự xuất hiện của các đoạn mã lỗi mới xen lẫn các bản cập nhật cấu hình hợp lệ (đã được lưu trữ trong Git). Thực nghiệm sẽ chứng minh khả năng của mô hình đề xuất trong việc phân loại chính xác các tín hiệu bất định, từ đó duy trì giá trị Thời gian Dẫn trước (DLT) dương mà không làm bùng nổ FPR5.  
**E3 — Ablation (Thử nghiệm Cắt lớp):** Các cấu hình cắt lớp được thiết lập để cô lập sự đóng góp của từng thành phần:

* *Config 1 (LogOW \+ Direct SLM, không có RAG):* Quan sát hiện tượng ảo giác (hallucination) của SLM khi bị tước đoạt tri thức ngoại vi, chứng minh RAG là bắt buộc5.  
* *Config 2 (LogOW \+ RAG Semantic Only):* Loại bỏ bộ mã hóa Code-specific và BM25 để phân tích tác động tiêu cực của hiện tượng lệch chuẩn không gian nhúng5.  
* *Config 3 (Loại bỏ cổng điều kiện Entropy):* Ép toàn bộ 100% cửa sổ log chạy qua SLM nhằm chứng minh sự sụp đổ về độ trễ tính toán của hệ thống nếu không có mạng Bayes chặn lọc5.

**E4 — Early Detection (Đánh giá Cảnh báo Sớm):** Thực nghiệm chuyên biệt đánh giá Thời gian Dẫn trước Cảnh báo (Detection Lead Time \- DLT). Hệ thống sẽ liên tục đối chiếu các cảnh báo sinh ra với nhãn thời gian xảy ra lỗi vật lý ![][image3] để lượng hóa khoảng thời gian đệm Early Warning Horizon (EWH) cung cấp cho người vận hành6.  
**E5 — Robustness (Kiểm tra Độ bền vững):** Mô hình sẽ bị thử thách với các tập dữ liệu bị nhiễu loạn nhân tạo, nơi tỷ lệ các template log mới hoàn toàn (chưa từng thấy trong tập huấn luyện) được đẩy lên mức 20% và 40%. Mục tiêu là ép mạng Bayes liên tục vượt ngưỡng Entropy để đo lường giới hạn chịu tải của mô-đun RAG-SLM.  
**E6 — Efficiency (Đánh giá Hiệu năng):** Đo lường cụ thể thông lượng hệ thống (Throughput \- Logs/giây) và độ trễ tính toán (Compute Latency \- ms/cửa sổ). Sự chênh lệch chi phí giữa luồng nóng (mạng nơ-ron cục bộ) và luồng lạnh (truy xuất RAG và gọi SLM API qua vLLM) sẽ được phân tích chi tiết3.  
**E7 — Generalization (Đánh giá Tổng quát hóa):** Để chống lại rủi ro phụ thuộc vào một loại hệ thống (Benchmark overfitting), mô hình được chạy chéo (cross-dataset) trên hai miền hoàn toàn khác biệt: tập dữ liệu BGL (đại diện cho siêu máy tính/phần cứng) và tập dữ liệu Thunderbird (đại diện cho môi trường mạng phân tán quy mô lớn)5.

## **11\. Evaluation Metrics**

Do bản chất bài toán là phát hiện sớm sự suy thoái, hệ mét đánh giá được chia làm ba nhóm phân cấp rõ rệt, khắc phục triệt để lỗ hổng của các phương pháp đánh giá tĩnh truyền thống3:  
**Nhóm Cốt lõi (Early Detection Metrics):**

* **Detection Lead Time (DLT):** Khoảng thời gian từ lúc phất cờ cảnh báo sớm đến khi sự cố sụp đổ xảy ra (![][image5]), đo bằng phút hoặc giờ.  
* **Early Warning Horizon (EWH):** Khung thời gian tối đa mà mô hình có thể duy trì độ tin cậy cảnh báo trước khi bị nhiễu loạn tín hiệu bão hòa.  
* **Detection Before Failure Rate (DBF):** Tỷ lệ phần trăm các lỗi vật lý được hệ thống cảnh báo thành công trước thời điểm zero.

**Nhóm Cơ sở (Detection Metrics):**

* **False Positive Rate (FPR):** Đây là chỉ số sống còn để định lượng sự bão hòa cảnh báo (Alert fatigue). Việc FPR sụt giảm trên nhóm log ngoài phân phối (OOD) là minh chứng trực tiếp cho sự thành công của cơ chế RAG-SLM.  
* **Precision, Recall, F1-Score, PR-AUC, ROC-AUC:** Được báo cáo đầy đủ để duy trì tính tương thích và khả năng so sánh với các tài liệu học thuật đã công bố.

**Nhóm Vận hành và Hiệu năng (Efficiency & Component-specific):**

* **Compute Latency:** Đo bằng mili-giây (ms) trên mỗi cửa sổ log để đánh giá tính khả thi thời gian thực.  
* **Token Cost / Memory:** Khối lượng VRAM và GPU sử dụng khi vận hành SLM cục bộ.  
* **Context Relevance:** Đo lường độ chính xác (Precision/Recall) của tài liệu RAG được truy xuất (Top-K) so với nguyên nhân lỗi thực sự3.

## **12\. Statistical Design**

Đặc thù của thiết kế tích hợp các cơ chế ngẫu nhiên (như Monte Carlo Dropout trong mạng Bayes và cơ chế lấy mẫu của LLM) đòi hỏi một kỷ luật thống kê (Statistical Design) cực kỳ nghiêm ngặt nhằm tránh việc báo cáo các kết quả ảo tưởng từ một lần chạy may mắn (best run bias)3.  
Tất cả các thử nghiệm (E1 \- E7) đều được tiến hành lặp lại (Repeated runs) 10 lần độc lập. Trong quá trình vận hành mạng Bayes, các hạt giống ngẫu nhiên (seeds) cho bộ khởi tạo Dropout được cố định cẩn thận. Đối với SLM, cấu hình siêu tham số được khóa cứng với temperature \= 0.0 và top\_p \= 1.0 để áp đặt tính xác định (determinism) tối đa cho đầu ra phân loại tự động, triệt tiêu sự bay bổng ngôn ngữ không cần thiết.  
Khi báo cáo kết quả, mọi giá trị trung bình sẽ đi kèm với độ lệch chuẩn (variance) và khoảng tin cậy 95% (Confidence Intervals). Để khẳng định sự cải thiện của DLT và sự sụt giảm của FPR không phải do sai số ngẫu nhiên, các kiểm định ý nghĩa thống kê (Significance Tests), điển hình là kiểm định phi tham số Wilcoxon signed-rank, sẽ được thực hiện (với ngưỡng ![][image10])3.

## **13\. Controlled Variables**

Sự bảo vệ tính hợp lệ của mọi kết luận nhân-quả trong luận văn phụ thuộc hoàn toàn vào bảng Biến số Kiểm soát (Controlled Variables) dưới đây1. Bằng cách khóa chặt các biến thể ở mô hình gốc, sự cải thiện hiệu năng sẽ được quy chiếu trực tiếp về yếu tố biến thiên duy nhất.

| Yếu tố (Factor) | Baseline (LogOW) | Improved (LogOW \+ RAG) | Tình trạng Kiểm soát |
| :---- | :---- | :---- | :---- |
| **Dataset & Data Split** | Chronological Split | Chronological Split | **Cố định 100%** |
| **Log Parsing Method** | Dynamic Parser gốc | Dynamic Parser gốc | **Cố định 100%** |
| **Representation Matrix** | Không gian nhúng mặc định | Không gian nhúng mặc định | **Cố định 100%** |
| **Core Model Weights** | Trọng số sau huấn luyện | Trọng số sau huấn luyện | **Cố định 100% (Đóng băng)** |
| **MC Dropout Config** | Số vòng truyền ngẫu nhiên không đổi | Số vòng truyền ngẫu nhiên không đổi | **Cố định 100%** |
| **Uncertainty Threshold** | Ngưỡng ![][image1] tối ưu của baseline | Ngưỡng ![][image1] tối ưu của baseline | **Cố định 100%** |
| **RAG/SLM Validation** | Không tồn tại | Kích hoạt | **Biến Độc Lập Duy Nhất** |

## **14\. Attribution Logic**

Thiết kế cấu trúc thực nghiệm đã kiến tạo nên một logic quy kết (Attribution Logic) không thể bác bỏ. Bảng Biến số Kiểm soát chứng minh rằng: toàn bộ hệ thống dữ liệu, bộ phân tích cú pháp, ma trận biểu diễn, trọng số mạng nơ-ron, và ngưỡng quyết định Entropy đều bị **đóng băng hoàn toàn** giữa System 1 (Base) và System 2 (Improved).  
Hệ quả toán học của việc đóng băng này là mạng nơ-ron cốt lõi sẽ sinh ra những kết quả bất định (Uncertainties) hoàn toàn giống hệt nhau ở cả hai hệ thống trong mọi khung thời gian thử nghiệm. Mạng nơ-ron không hề "học" thêm bất kỳ điều gì mới. Do đó, nếu thực nghiệm ghi nhận tỷ lệ cảnh báo giả (FPR) sụt giảm đột ngột và Thời gian Dẫn trước (DLT) được duy trì tích cực ở System 2, **toàn bộ (100%) sự gia tăng hiệu năng này có thể và phải được quy kết trực tiếp cho năng lực phân giải của mô-đun RAG-SLM**3. Hiện tượng nhập nhằng (confounding variables) do sự thay đổi trọng số phân loại nội tại đã bị triệt tiêu hoàn toàn.

## **15\. Design Alternatives**

Việc theo đuổi "sự cải thiện nhỏ nhất mang lại ý nghĩa lớn nhất" (smallest meaningful improvement) đòi hỏi việc sàng lọc các biến thể thiết kế thay thế (Design Alternatives) trên cùng một hướng tiếp cận, tránh việc lan man tạo ra các kiến trúc hoàn toàn khác biệt.

* **Biến thể A — Minimal (Chỉ LLM trực tiếp, không RAG):** Biến thể này cho phép luồng log bất định được nạp thẳng vào SLM để đánh giá mà không cần truy vấn tài liệu ngoại vi. Biến thể này bị loại bỏ vì thực nghiệm sơ bộ cho thấy SLM sẽ gặp ảo giác (hallucination) nghiêm trọng do không có dữ liệu đối chiếu về lịch sử thay đổi cấu hình cục bộ5.  
* **Biến thể B — Refined (Baseline \+ RAG-SLM Triage có điều kiện):** Đây là thiết kế kiến trúc được đề xuất, sử dụng SLM kết nối cơ sở dữ liệu Vector và kích hoạt chặt chẽ dựa trên ngưỡng Entropy của BNN. Lựa chọn này khắc phục hoàn hảo sự cách ly ngữ cảnh, dập tắt cảnh báo giả trong khi vẫn duy trì chuẩn độ trễ SLA của hệ thống AIOps3.  
* **Biến thể C — Robust (Improvement \+ Memory-Augmented Networks):** Biến thể này cố gắng bổ sung thêm một mạng nơ-ron tăng cường bộ nhớ để lưu vết các chu kỳ của log bất định. Dù mạnh mẽ về mặt lý thuyết, phương án này bị loại bỏ do sự chồng chéo phương pháp luận, làm tăng tính phức tạp của việc huấn luyện lên gấp nhiều lần và tạo ra rủi ro khó hội tụ trong quỹ thời gian eo hẹp của luận văn5.

**Kết luận chọn lựa:** Phương án **B (Refined)** được chốt làm thiết kế chính thức vì tính tinh gọn, khả thi cao và sức mạnh vừa đủ để kiểm chứng các giả thuyết đã đề ra.

## **15A. Final Baseline Eligibility Verification**

Trước khi bước vào giai đoạn chốt phương án, một cuộc kiểm tra rào chắn bắt buộc lần cuối (Final Baseline Eligibility Verification) đã được tiến hành để xác nhận tính hợp lệ tuyệt đối của phương pháp cơ sở **LogOW**:

* \[x\] **Publication year:** 2024 (Available online), Volume 222 xuất bản 2025\. Nằm gọn trong giai đoạn 2023–2026.  
* \[x\] **Publication type:** Journal article chính thức.  
* \[x\] **Peer-reviewed:** Đã qua quá trình bình duyệt học thuật.  
* \[x\] **Journal ranking:** *Journal of Systems and Software* thuộc phân nhóm Q1 hàng đầu.  
* \[x\] **Ranking evidence:** Được xác minh qua SCImago/Scopus SJR 2024: 0.975 và JCR2.  
* \[x\] **Verifiability:** Công bố đi kèm DOI (10.1016/j.jss...) minh bạch. Hệ thống mã nguồn và 1.4GB dữ liệu thực nghiệm được lưu trữ vĩnh viễn trên Zenodo (DOI: 10.5281/zenodo.14214083) cho phép tái lập trọn vẹn17.  
* \[x\] **Consistency:** Phương pháp cơ sở phản ánh đúng 100% nội dung đã được phê duyệt trong hồ sơ result-4.md. Mối quan hệ giữa Limitation và Improvement không có sự vay mượn từ các công trình ngoài lề.

Cổng kiểm định xác nhận: **Baseline hợp lệ toàn diện**. Thiết kế nghiên cứu tiếp tục chuyển sang giai đoạn lựa chọn cuối cùng.

## **16\. Final Research Design Selection**

Một (01) Thiết kế Nghiên cứu tối ưu nhất được chốt lại, đáp ứng đầy đủ sự cân bằng giữa tính đột phá khoa học và giới hạn khả thi thực tiễn của một chương trình Thạc sĩ (6-9 tháng).

| Lựa chọn Thiết kế (Design Choice) | Phương án Chốt (Selected Option) | Lý do Biện luận (Reason) |
| :---- | :---- | :---- |
| **Baseline** | LogOW (Q1, 2024/25)3. | Nắm giữ thuật toán SOTA về ước lượng độ bất định Bayes trong môi trường trượt dạt khái niệm; mã nguồn mở, kiến trúc rõ ràng, minh bạch5. |
| **Main Improvement** | Tích hợp "Não bộ ngoại vi" RAG-SLM Triage thực thi có điều kiện. | Phân giải ranh giới ngữ nghĩa của sự "bất định" bằng tri thức vận hành thực tế mà không xâm lấn tốc độ của mạng học sâu gốc3. |
| **Data** | Siêu dữ liệu BGL, Thunderbird. Áp dụng Chronological Split. | Chứa đựng chuỗi thời gian thực, bác bỏ HDFS tĩnh, triệt tiêu rủi ro rò rỉ dữ liệu tương lai5. |
| **Learning** | LogOW weights Frozen. SLM sử dụng In-context learning. | Không Fine-tuning SLM. Việc đóng băng trọng số đảm bảo quy kết nhân-quả chính xác, tối ưu thời gian triển khai 6-9 tháng3. |
| **Inference** | Luồng kép: Hot Path (NN \< 5ms) \+ Cold Path (RAG \~500ms). | Tối ưu hóa độ trễ tính toán, hoàn toàn thỏa mãn các chỉ tiêu SLA công nghiệp cho nền tảng AIOps10. |
| **Evaluation** | Hệ mét DLT, EWH, DBF và FPR trên tập OOD. | Đánh giá trực tiếp và duy nhất năng lực "Phát hiện Sớm" trước khi sụp đổ vật lý, loại bỏ các chuẩn tĩnh sai lệch3. |

## **17\. Research Traceability Matrix**

Ma trận Truy xuất Nghiên cứu (Traceability Matrix) liên kết chặt chẽ mọi thiết kế thành phần với các câu hỏi và giả thuyết khoa học ban đầu, đảm bảo rằng không có bất kỳ một cấu trúc nào được xây dựng mà không có mục đích đo lường3.

| Yếu tố Nghiên cứu (Research Element) | Thành phần Thiết kế (Design Element) | Bài kiểm tra Thực nghiệm (Experiment) | Hệ mét (Metric) | Bằng chứng Thành công (Evidence of Success) |
| :---- | :---- | :---- | :---- | :---- |
| **RQ1:** Giới hạn của xấp xỉ Bayes (LogOW) trước bản cập nhật phần mềm (Concept Drift)? | Khối BNN (Monte Carlo Dropout) và ngưỡng Entropy. | E1 (Reproduction) & E5 (Robustness). | FPR trên luồng OOD logs. | FPR của LogOW gốc tăng vọt khi đối mặt với log cập nhật hợp lệ. |
| **RQ2:** RAG-SLM phân định cập nhật an toàn và cảnh báo sớm thế nào? | Cổng RAG-SLM Triage ở khâu hậu xử lý, kết hợp In-context prompting. | E2 (Main Test) & E3 (Ablation). | FPR và DLT. | FPR giảm 99% tại vùng biên bất định; DLT tiếp tục duy trì giá trị dương. |
| **RQ3:** Ảnh hưởng của RAG-SLM lên kiến trúc thời gian thực? | Dual-path Inference (Hot Path / Cold Path). | E6 (Efficiency). | Latency (ms/window), Throughput. | Độ trễ luồng nóng \< 5ms; tỷ lệ điều hướng qua luồng lạnh \< 5% tổng dung lượng. |
| **H1:** Bão hòa cảnh báo bắt nguồn từ sự cô lập tri thức. | Đối chứng Baseline vs RAG-SLM vs Direct SLM. | E3 (Ablation 1 & 2). | Context Relevance, FPR. | FPR giữ mức cao ở mô hình gốc và sụt giảm mạnh khi có sự can thiệp của tri thức ngoại vi (RAG). |
| **H2:** Tối ưu độ trễ bằng kích hoạt RAG có điều kiện (Entropy threshold). | Decision Fork / Ngưỡng cắt động ![][image1]. | E6 (Efficiency). | Chi phí API, RAM, Token Cost. | Mức độ tiêu thụ tài nguyên và thời gian giảm theo cấp số nhân so với việc quét SLM toàn bộ. |
| **H3:** Sự cải thiện ổn định của DLT trên dữ liệu động học. | Dữ liệu Chronological Split (BGL, Thunderbird). | E4 (Early Detection). | DLT, EWH, DBF. | Mô hình vượt qua màn sương mù của trượt dạt khái niệm và sinh cảnh báo trước ![][image3] một cách ổn định. |

## **18\. Threats to Validity**

Một thiết kế nghiên cứu nghiêm túc phải dũng cảm đối mặt và kiểm soát các mối đe dọa đến tính hợp lệ (Threats to Validity) từ nhiều khía cạnh cấu trúc khác nhau5.  
**1\. Internal Validity (Tính hợp lệ Nội tại):**

* **Data Leakage (Rò rỉ tương lai):** Đây là rủi ro hủy diệt nhất đối với các bài toán phân tích chuỗi thời gian. Bất kỳ sự rò rỉ nào từ dữ liệu tương lai vào quá trình huấn luyện đều làm sụp đổ giá trị của thời gian dẫn trước (DLT). Việc cấm tuyệt đối kỹ thuật Random Shuffle và áp dụng quy chuẩn **Chronological Split** là tấm khiên thép chặn đứng rủi ro này5.  
* **Tuning Bias (Thiên lệch tinh chỉnh):** Nguy cơ so sánh bất bình đẳng. Khắc phục bằng cách đóng băng toàn bộ trọng số (frozen weights) của mô hình baseline trong mọi phép đối chứng.

**2\. External Validity (Tính hợp lệ Ngoại lai):**

* **Benchmark Bias:** Quá phụ thuộc vào HDFS, một tập dữ liệu tĩnh nghèo nàn, làm sai lệch kết quả tổng quát hóa. Việc chuyển dịch sang các siêu tập dữ liệu có tính chất trượt dạt khái niệm thực tế như BGL và Thunderbird kiểm soát triệt để mối đe dọa này5.

**3\. Construct Validity (Tính hợp lệ của Khái niệm):**

* **Metric Mismatch:** Việc sử dụng F1-score tĩnh để suy ra năng lực "Phát hiện sớm" là phi logic. Rủi ro này bị bác bỏ nhờ hệ mét DLT và EWH dựa trên nhãn thời gian sụp đổ vật lý6.

**4\. Conclusion Validity (Tính hợp lệ của Kết luận):**

* **High Variance (Phương sai cao):** Cả xấp xỉ Bayes (MC Dropout) và sinh ngôn ngữ tự nhiên (SLM) đều chứa đựng tính ngẫu nhiên. Nguy cơ chọn một lần chạy may mắn (best run) để báo cáo. Sự chặt chẽ thống kê thông qua 10 lần chạy độc lập và kiểm định Wilcoxon signed-rank triệt tiêu sai số này3.

**5\. Foundation Model & Retrieval Validity:**

* **Hallucination & Stale Knowledge:** SLM có thể bịa đặt kết quả (ảo giác) do thiếu kiểm soát. Kho truy xuất có thể trả về các tài liệu thiết kế đã lỗi thời hoặc chứa mã rò rỉ tương lai. Khắc phục bằng Prompt In-context cực kỳ nghiêm ngặt với temperature \= 0.0 và áp dụng hàm suy giảm theo thời gian (Timestamp-decay) cho kho Vector3.

## **19\. Risk and Mitigation**

Kế hoạch quản trị rủi ro được lập bản đồ chi tiết để đảm bảo luận văn không rơi vào trạng thái bế tắc khi đối mặt với các khó khăn kỹ thuật5.

| Rủi ro Cốt lõi (Risk) | Xác suất | Tác động | Chiến lược Giảm thiểu (Mitigation) | Phương án Dự phòng (Fallback) |
| :---- | :---- | :---- | :---- | :---- |
| **Baseline không tái lập được hiệu năng nguyên thủy** | Thấp | Rất Cao | Tận dụng triệt để Repository mở trên Zenodo của tác giả LogOW, đi kèm 1.4GB dữ liệu đã làm sạch và tham số chuẩn17. | Bỏ qua việc săn đuổi điểm SOTA, chỉ tập trung chứng minh FPR giảm khi đối mặt luồng OOD logs. |
| **Lệch chuẩn Không gian nhúng (Embedding Mismatch)** | Trung bình | Cao | Dữ liệu log chứa mã Hex và IP khiến Semantic Search trả về sai lệch. Chuyển sang tìm kiếm lai (Hybrid Search) kết hợp BM25 và Code-specific Embeddings8. | Thu hẹp phạm vi truy xuất, chỉ sử dụng đối sánh từ khóa chính xác (Exact Keyword Match). |
| **Độ trễ API (Retrieval Latency) phá vỡ thời gian thực** | Cao | Rất Cao | Kiến trúc Dual-path (Hot/Cold Path). Ngưỡng Entropy ![][image1] đảm bảo chỉ \< 5% lượng dữ liệu OOD phải gọi API RAG10. | Nâng cao điểm cắt ngưỡng ![][image1] để giảm thiểu tối đa số lượng cuộc gọi sang LLM. |
| **SLM sinh ảo giác trong quyết định Triage** | Trung bình | Cao | Kỹ thuật Prompt Engineering định dạng JSON cứng; hạ tham số nhiễu LLM (temperature \= 0.0)5. | Tạm ngưng sinh ngôn ngữ, chuyển sang Rule-based parser quét từ khóa trên tài liệu RAG lấy được. |

## **20\. Expected Contributions**

Luận văn kiến tạo các đóng góp đa chiều, từ nền tảng lý thuyết đến khả năng ứng dụng thực chiến trong môi trường điện toán đám mây.  
**Về mặt Khoa học (Scientific):** Thiết lập và chứng minh lý thuyết quan trọng: Tích hợp Tri thức Ngoại vi (External Knowledge) thông qua việc phân giải Bất định Nhận thức (Epistemic Uncertainty) của xấp xỉ Bayes là chìa khóa giải quyết dứt điểm hiện tượng bão hòa cảnh báo (Alert Fatigue) do trượt dạt khái niệm (Concept Drift) ở các mô hình học sâu tĩnh.  
**Về mặt Phương pháp luận (Methodological):** Đề xuất kiến trúc Hybrid Pipeline thực thi có điều kiện. Việc phân lập hoàn hảo giữa luồng nóng (mạng nơ-ron học sâu tốc độ cao) và luồng lạnh (tác tử SLM phân giải ranh giới bất định) đã tạo ra một mô hình chuẩn mực giải quyết sự đánh đổi giữa trí thông minh của AI tạo sinh và độ trễ mili-giây10.  
**Về Kỹ thuật & Công nghệ (Engineering):** Chuẩn hóa Khung đánh giá Thực nghiệm Động học (Dynamic Evaluation Framework) cho hệ thống Early Log Anomaly Detection. Chấm dứt sự phụ thuộc vào F1-Score tĩnh bằng cách thiết lập thước đo Thời gian Dẫn trước (DLT) và áp dụng triệt để Chronological Split chống rò rỉ dữ liệu5.  
**Về Ứng dụng Công nghiệp (Industrial):** Mô hình trực tiếp giải cứu các trung tâm điều hành bảo mật (SOC) khỏi biển cảnh báo giả mù quáng, tiết kiệm hàng triệu giờ công phân tích của kỹ sư hệ thống, đồng thời tối ưu hóa chi phí API LLM nhờ cơ chế gọi có điều kiện8.

## **21\. Reproducibility**

Tính minh bạch và khả năng tái lập (Reproducibility) được cấu trúc tỉ mỉ trong từng chi tiết cấu hình, đảm bảo mọi nhà nghiên cứu độc lập đều có thể kiểm chứng lại kết quả:

* **Baseline/Version:** Mã nguồn LogOW nguyên thủy từ nhánh Zenodo (DOI: 10.5281/zenodo.14214083), không qua chỉnh sửa cấu trúc mạng17.  
* **Model/Version:** Llama-3-8B-Instruct (định dạng GGUF/AWQ 4-bit) hoặc Qwen2.5-7B, chạy cục bộ qua engine vLLM để tối đa hóa băng thông inference25.  
* **Prompt:** Mẫu lệnh (In-context learning template) được lưu trữ cứng trong tài liệu phụ lục.  
* **Dataset/Version:** BGL và Thunderbird (dữ liệu làm sạch từ kho Loghub).  
* **Preprocessing:** Drain parser cấu hình độ sâu cây phân tích cố định (depth=4).  
* **Seed:** Cố định siêu tham số ngẫu nhiên seed=42 cho toàn bộ PyTorch, Numpy và quá trình lấy mẫu LLM.  
* **Retrieval Config:** Kích thước phân mảnh tài liệu (chunk=512), Top-K=3, ngưỡng cosine similarity \> 0.75.  
* **Evaluation Protocol:** Chia cắt Chronological Split theo tỷ lệ thời gian (70% huấn luyện đầu, 30% thử nghiệm sau)14.  
* **Hardware/Software:** Quá trình huấn luyện mạng nhẹ và suy luận SLM được thực thi trên GPU Nvidia RTX 3090/4090 24GB VRAM, hệ sinh thái PyTorch 2.x, vLLM, và LangChain25.

## **22\. Final Checklist**

Sự đối chiếu cuối cùng xác nhận tính hoàn thiện của thiết kế nghiên cứu:

* \[x\] Một baseline Q1/Q2 trong giai đoạn 2023–2026 rõ ràng (LogOW, Q1 2024/25, *JSS*)2.  
* \[x\] Một confirmed limitation (Bão hòa cảnh báo giả do Context Deprivation khi gặp OOD logs)5.  
* \[x\] Một main targeted improvement (Conditional RAG-SLM Triage tại cổng quyết định)3.  
* \[x\] Baseline reproduction/reference (Kế thừa toàn vẹn từ Zenodo source code)17.  
* \[x\] Baseline vs Improved (Đối chứng tĩnh LogOW vs LogOW \+ RAG).  
* \[x\] Ablation phù hợp (Các thực nghiệm cắt lớp điều chỉnh ngưỡng Entropy và cấu hình RAG)3.  
* \[x\] Early Detection metrics (Định hình rõ ràng DLT, EWH qua nhãn thời gian vật lý)6.  
* \[x\] Controlled variables (Đóng băng trọng số mạng, Chronological split)3.  
* \[x\] Statistical validation khi cần (10 seeds, kiểm định Wilcoxon).  
* \[x\] Risk mitigation (Dual-path inference, Code-specific embeddings)5.  
* \[x\] Không tạo research topic mới (Bám sát tuyệt đối proposal).  
* \[x\] Không thêm technology chỉ vì trend (SLM chạy có điều kiện thay vì quét thô toàn bộ log).  
* \[x\] Khả thi 6–9 tháng (Can thiệp hậu xử lý tách rời, bỏ qua huấn luyện lại LLM/BNN).

*Tài liệu nghiên cứu được thiết kế để cung cấp một nền tảng thực chứng chặt chẽ, tối giản nhưng vô cùng mạnh mẽ, đảm bảo đạt chuẩn mực học thuật của IEEE/ACM trong ngành kỹ thuật phần mềm và hệ thống AIOps.*

#### **Works cited**

> 1. result-1.md  
> 2. Journal of Systems and Software, Volume 222 \- DBLP, [https://dblp.org/db/journals/jss/jss222](https://dblp.org/db/journals/jss/jss222)  
> 3. result-4.md  
> 4. Journal of Systems and Software \- Impact Factor (IF), Overall, [https://www.resurchify.com/impact/details/19309](https://www.resurchify.com/impact/details/19309)  
> 5. result-3.md  
> 6. result-2.md  
> 7. Out-of-Distribution Detection in LiDAR Semantic Segmentation, [https://arxiv.org/html/2510.08631v1](https://arxiv.org/html/2510.08631v1)  
> 8. (PDF) LogRAIL: A Retrieval-Augmented LLM Reverification Layer, [https://www.researchgate.net/publication/404570918\_LogRAIL\_A\_Retrieval-Augmented\_LLM\_Reverification\_Layer\_for\_Log\_Anomaly\_Detection](https://www.researchgate.net/publication/404570918_LogRAIL_A_Retrieval-Augmented_LLM_Reverification_Layer_for_Log_Anomaly_Detection)  
> 9. Boosting Your Anomaly Detection With LLMs | Towards Data Science, [https://towardsdatascience.com/boosting-your-anomaly-detection-with-llms/](https://towardsdatascience.com/boosting-your-anomaly-detection-with-llms/)  
> 10. The Hot Path Belongs to GBDTs, Agents Own the Cold Path, [https://towardsdatascience.com/the-hot-path-belongs-to-gbdts-agents-own-the-cold-path-a-payment-fraud-benchmark/](https://towardsdatascience.com/the-hot-path-belongs-to-gbdts-agents-own-the-cold-path-a-payment-fraud-benchmark/)  
> 11. pclaerhout \> news \- FeedLand, [https://feedland.com/?river=true\&screenname=pclaerhout](https://feedland.com/?river=true&screenname=pclaerhout)  
> 12. An environment-guided visual–temporal deep learning framework, [https://pmc.ncbi.nlm.nih.gov/articles/PMC13096088/](https://pmc.ncbi.nlm.nih.gov/articles/PMC13096088/)  
> 13. Wind Turbine Fault Detection Through Autoencoder-Based Neural, [https://www.mdpi.com/1424-8220/25/14/4499](https://www.mdpi.com/1424-8220/25/14/4499)  
> 14. Log-based Anomaly Detection Using Large Language Models \- arXiv, [https://arxiv.org/html/2411.08561v1](https://arxiv.org/html/2411.08561v1)  
> 15. IMU-Enhanced Vessel Trajectory Prediction: Overcoming Kinematic, [https://www.mdpi.com/2077-1312/14/5/461](https://www.mdpi.com/2077-1312/14/5/461)  
> 16. A note on the validity of cross-validation for evaluating, [https://www.researchgate.net/publication/321260315\_A\_note\_on\_the\_validity\_of\_cross-validation\_for\_evaluating\_autoregressive\_time\_series\_prediction](https://www.researchgate.net/publication/321260315_A_note_on_the_validity_of_cross-validation_for_evaluating_autoregressive_time_series_prediction)  
> 17. LogOW: A Semi-Supervised Log Anomaly Detection Model in Open, [https://zenodo.org/records/14214083](https://zenodo.org/records/14214083)  
> 18. Semi-supervised Log-based Anomaly Detection via Probabilistic, [https://xgdsmileboy.github.io/files/paper/plelog-icse21.pdf](https://xgdsmileboy.github.io/files/paper/plelog-icse21.pdf)  
> 19. An Uncertainty-aware Loss Function for Training Neural Networks, [https://arxiv.org/html/2110.03260v2](https://arxiv.org/html/2110.03260v2)  
> 20. Uncertainty Estimation in Machine Learning with Monte Carlo Dropout, [https://medium.com/biased-algorithms/uncertainty-estimation-in-machine-learning-with-monte-carlo-dropout-72377f5ee276](https://medium.com/biased-algorithms/uncertainty-estimation-in-machine-learning-with-monte-carlo-dropout-72377f5ee276)  
> 21. Two Simple Ways To Measure Your Model's Uncertainty, [https://towardsdatascience.com/2-easy-ways-to-measure-your-image-classification-models-uncertainty-1c489fefaec8/](https://towardsdatascience.com/2-easy-ways-to-measure-your-image-classification-models-uncertainty-1c489fefaec8/)  
> 22. Anomaly Detection for Multi-System Bug Triage \- Dallas \- SMU Scholar, [https://scholar.smu.edu/cgi/viewcontent.cgi?article=1314\&context=datasciencereview](https://scholar.smu.edu/cgi/viewcontent.cgi?article=1314&context=datasciencereview)  
> 23. Smart Overhead Crane Guide: IoT Sensors, Predictive ... \- Weiyuan, [https://chengduweiyuan.com/news/smart-overhead-crane-guide-iot-sensors-predictive-maintenance-real-time-load-monitoring-that-cut-downtime-by-40/](https://chengduweiyuan.com/news/smart-overhead-crane-guide-iot-sensors-predictive-maintenance-real-time-load-monitoring-that-cut-downtime-by-40/)  
> 24. LLMOps — Sudheesh Knowledge Base, [https://sudheeshreddy.com/ai-engineering/llmops/](https://sudheeshreddy.com/ai-engineering/llmops/)  
> 25. Leveraging Large Language Models for Scalable and Explainable, [https://usiena-air.unisi.it/retrieve/67c93bf8-0943-48a2-8393-69422dee7e8f/jcp-05-00055.pdf](https://usiena-air.unisi.it/retrieve/67c93bf8-0943-48a2-8393-69422dee7e8f/jcp-05-00055.pdf)  
> 26. SpecQuant: Spectral Decomposition and Adaptive Truncation for, [https://ojs.aaai.org/index.php/AAAI/article/view/40112/44073](https://ojs.aaai.org/index.php/AAAI/article/view/40112/44073)  
> 27. (PDF) A Zero-Touch Vulnerability Remediation Framework Based, [https://www.researchgate.net/publication/403045958\_A\_Zero-Touch\_Vulnerability\_Remediation\_Framework\_Based\_on\_OpenVAS\_Threat\_Intelligence\_and\_RAG-Enhanced\_Large\_Language\_Models](https://www.researchgate.net/publication/403045958_A_Zero-Touch_Vulnerability_Remediation_Framework_Based_on_OpenVAS_Threat_Intelligence_and_RAG-Enhanced_Large_Language_Models)  
> 28. LogICL: Distilling LLM Reasoning to Bridge the Semantic Gap in, [https://arxiv.org/html/2512.09627v1](https://arxiv.org/html/2512.09627v1)  
> 29. Uncertainty Estimation in NLG \- Emergent Mind, [https://www.emergentmind.com/topics/uncertainty-estimation-in-natural-language-generation](https://www.emergentmind.com/topics/uncertainty-estimation-in-natural-language-generation)  
> 30. LogOW: A Semi-Supervised Log Anomaly Detection Model in Open, [https://explore.openaire.eu/search/result?pid=10.5281/zenodo.14214083](https://explore.openaire.eu/search/result?pid=10.5281/zenodo.14214083)  
> 31. Log-based Anomaly Detection Using Large Language Models \- arXiv, [https://arxiv.org/html/2411.08561v4](https://arxiv.org/html/2411.08561v4)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAAWUlEQVR4XmNgGAXUBpxA7AzEHkDsBcUgtguyot1A/B8PdgUpygXixVANILARiCWQ+HBgjcYHmUAQsDAQqbAfiD+gC2IDINNAigkCkEIddEF0IM9ApPtGDgAA3ZITGuefBmUAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAYAAAAVibZIAAAAU0lEQVR4XmNgGAWjYFCAvegC1AD/0AWoAWyAuAxdkBrgHBCbowsiAxMy8S0g3sdAZfAXiBnRBSkB/9EFKAUTgJgdXZBS8BtdgBrAAF1gFIwCGgIAYTgLotElupAAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAAA7ElEQVR4Xu2UsQ4BURBFLxI1GjqtL9CoVQoJiSj9AR1f4Qd8hlCp1BK+QS8KIaFhniHZ3Mxu3tqlcpLb3DuZN2/ydoE/v2IuuseQN664Z3jcpGZ4oZSgEwfJQhvsyHfs2QhjIcqQN4I2bpOfF03JC2XIhnCEfeWCqMxmHKz9JiYHbbrhIATvG4yhjVscGKxEDdGVA4sT/Nfg6iqiKgcWvvstwq/uiXtOPvt9H+47BGbQwgH5FltRl80gHdEF+nYPL7k93xA9jcv4w0qFqEM/xk36lcZ90ZLNpDRFa+j7TY0J9Fd65iAN6mz8ieQBx8s+dop321EAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAaCAYAAABYQRdDAAAA4klEQVR4XmNgGAW0ApuB+D8JmCgAUhiGRQzdAA0sYliBEAPEpciAiQGi+QKaOAg8QhfABrYCMSOaWAEDxFB/NHE2IO5DE8MK8tEFgOA9A3ZvCgCxOLogsQBbeFIEmBkgBp5Bl6AElDNADPVGl6AEfGagstdBgOrhCUoyhMITlPxAqWMlAyTJRaBKY4LZDBBDE9DEkQGyL/4AsRUSHw6CgPgbA8T2t1AMCtdfDJjBUAPEd5D46PJkAZAhsWh8isFuIJaDsmcA8TEgDkdIkwdAGeMvAySouID4NxDPQlExCkY4AABaLDyvKAmy1gAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAH8AAAAaCAYAAACehIP6AAACoUlEQVR4Xu2Zu2sWQRTFbyIRYiHGRiEQW3vFwtSCoKgkEG0E0T8gNqL4qGxEQQsRREUxAcEiaXw0WokIokFR7MQikM4H+AJf6D3cXZ3vZvbbmdXdWZP7g8PHnjv77dndmdkXkWEYhmH85gurX5vGwucw6ydrThc8oF2ofmTrNMkNmp+jm1KTPK/750tVzaWHpM2g4/Vm3nPHA9dYN5XXBMgy5vH0gVvr8VKQNO9+1nHWMZI/f9VZ7uA0a53yxknW26H8Lay9yqublSQjySXvnE+VD2a10TDJ87q9Ke9xSxzPxdfz3pLfR4dars2auUUyO7mgcyPfduVjhkNnTknSvPtYp5zlEyQbfuF4LhjNGt8UBXxt6wazkOYd+fOtYK3SZsMkzevbSNHJ9IEZAm1ndKFFxOxPG2gkL24yzmmTOUuy8Ye64OEASdutuhDIZIEmWFdZV1iXWZdYF7N1Ysg752NdKOCfjqwKxOatTLfeFdr73lNYu1QcJMkXcgm6yxomed9RxvoIxRCTtzKbSUZWERhxCIED0o3QTpKKDxSeD+1Ws9bogodtEYohJm9lQjZQdmL7SOqPdCGCk5GKpWwfcgYorF3dhOatzEbWlDY9TJMEKWp7hKRe9XpfN3g0Qr6y62d+wGs/8CWE5MVjIZ4GrpM8Cu7qLJejdzZEPr6S1PBSoo3gBhH59ijfxxPWqDYbJiSvey6+kwzkYIZo/okN0RmszDxjfSR5sfM6+/1EEuR+1iYlI6zPJKPjTSZcR/OOWgRq+mVLE8TkPcp66SzrulGR/+FAIuNutWz8JfnHqrZzh2TmBudZD1g7/5SNKuCm6bY2WwheAOETOS4Ry1jfWBc6WhhRbGLdI3m+NxYRh0g+m+KG1ViEbNCGYRiGYSwAfgG+f/nSAdD23gAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAaCAYAAAAKYioIAAACNklEQVR4Xu2XP0jVURTHj/1FpAYLl8DFoU0kh1CkxSWooURbIgKFVltajJZcxMCgaI4iCoecpEFqKoQoF7VNdDFwkCBT0EjsfDn3B/d9ve953+/3fBDdD3x5/r7n/O479/c73nufSCKRqAM7qkY2/3dGVHuq7xwIgLxY7bp76k2Takashi+qhtJwPP5kTlDMB1+AnHOed8R5C54HXqumyasHqA31ZN1/xl2jzqq4qxpVPRAbYLk0XMKEqpO8YbH7rpF/RTVIHnOZjRqwpZok76tqm7wDwaT8v6Gjnufj52b8kLCPh32aTeKs6pdYd9UK1HKDvGypiGZI9ci7HhMb4Jvn+aALmOxhMqHccpxSralmpcB6oFwSq6WH/NvObya/LKEJlZtoCHQWcuc4kJNjqkXViuTbIbEsoJ4L5A84/yL5QdBuz9hUnooN8pkDAe6J5V7lQA34oPqpauFABR6K1dNO/nXn3yQ/SKWuiO2aDYnLK8IrsTNWGwcC3BGrp4P8fuf3kr8P7AYv2PR4LjbQew4QsQ+wCOMS/2+QrTFd5N9yvn/MCBIzmYMmfVwsjgPUYfBS9Vt1ngMVOClWU65dqVv1ls0AU2KDlcu9Lxav9fqCLsURAFt5HlDTE/LeOb8iWSdUoxB4m4hVfaIMgN0IR4QlsbdehFB34LqPvBJaZf+kY/QYNyvzqk2xN7ruPnHS/KP65HKqAVvyquojBwryRux3Gj5RP7bxfwrsFolEIpFIJBKJnPwF8CGkK5CYO60AAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAaCAYAAADSbo4CAAABV0lEQVR4Xu2UPUtDMRSGjwoi4iBddHIT/AEdHJ1cHAoiOgn+A91cHcSxo6CdijqIiyC6OCi4OuguDg4KfuBQ6OAH+r4kl54eAjaYdsoDD03ec9uce5NbkUymM07gT4Rdgz++GMjsolOBLBklcU9E0y9uwRuTkwcbpOIU9plsTVwjFZMPwqrJkrFqA/Au4S0YhWM27Cah89FzBsQ1cW0LvWZdXCNzthBgU9y107aQgobEbUvMtVHEno+YazuGr+df54Ov+hM8g3V4oWpD8A3uw0eVk1t4CF9MHqQmrpEVk2v0E/iAM348Iu21A7jlx8z5EhTjIPOwKe6/g3dDeU64iP3SHrxTc13/ggtqfgyP4A68V3kSuPCymYfGxXwSfkt7g0k4hxN+vA2v4JKf60bK8NWPL+Fsq5SmKe4z7/AZDsNPuOtr49I66Bs+K+DWcKv4ybOUyWT+zS+OiVpMaNcRhAAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAAAaCAYAAAAkJwuaAAACh0lEQVR4Xu2YS6hOURiGP5fcckvChAG5TAxEGBpJGSiJERkyYqBMDAxkQAyoU5i4lwwoMUEUmbhEMVCiJOSalHL3vn17s85rO3uv/e/tnL/WU29n7fdb+1//t/Za317/MUskEolEGeegnxHqVjSPvnQ9uycK3ri6wNNJm1PgdQuzoK/QyMCbZ57P/sAjT6At4pUywXxFhgw2H+Cu+OSpGi2xTI0OuQONEu+MeZ6cg5Dd0HTxSjkPDRJvs/kAK8QfBu0Vry0mQh+hkxqoyQ81rHjXkWtqVGGTGuC9FQ8wHpqsZsuMgV5CN+zvBx7DXDXMc/yuJtioRl3+9aT6k6HQffP6Fda5usw3z3GPBppiiPkAtzQwgLgMfYAmaSACljTmOU4DTbHVfIDlGihgh3nfxRr4TxyHPkMzNFCB1ncdC3zMADF9m2aX+fiLNFAB3vdNzSaJfVIxfZviKPQFmq2BinAH8XvzmNMKPN6U1Ue+OV9AF6Aj0JUgNgJ6a77lngc+uQedgl6LH8Ml6J350agTLlp5fWRpuwk9g/ZJrJRD5gOsFz8kXIFcFUuy9mjrHTsB7cza9PkSy9sx8G39AHoEDZdYXcp23ULzCczpq+9vVkKfzM+OXE0U6yQnST/gmHlCOWGc9WZVcH0WOg0dgB4HflV4xGEytQ7HBfC8yLy4ot+Y58u86fOlGcK8pmZt/sJhv0bhAGvluqidX880/6LhBFelzj1NEeZyGNoWXDcCa8u0rN1jvlrWZNfh4AvMnzq5Ci39E+rXCaqKLhD+Rn8VeB3DOscVxg/lh/O/KQez2BTzQfmi2p55Odza3Or8y1o60FkHPTRfOBug29DYXj0SiUQikUh0Kb8AOqqpIJgyS4oAAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAaCAYAAAA5WTUBAAAA2UlEQVR4XmNgGAWjYBTgB2boAgMB2ID4ARAfAWJGVCn6AyYgvgjE94GYE02OHGAFxG5A7AnEXlDaHYhNkBXhA9uB+BMQS6BLEAFAIfsfD/6HUEocmA/Ef4BYF10CDwBZxIfGpwpoZYAYZocugQZA0ciCxA8B4i1IfIpANgPEEZHoEgTAOyAOQhckFbQwQCx3QpcgEoD0kp3j5gLxbyDWRJcgAYDSEVnpYQcQvwdiUXQJMsBpBhIcAQquM0B8F4g50OQoASAHTEcXxAVAxTbZ8TYKRsEoGAW0BgAq8yWXy6yKNQAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEoAAAAaCAYAAAAQXsqGAAACl0lEQVR4Xu2YTYhOURjHH8bHWJh8lSKKjZWVRpqVJCyQLFjIhgXZWVgQq9koO2ayYMFOkZBC7BAp8hWi1MxiVvL9MRPh+c85xzzv/57zvvde6W1yfvXvvc//ee655557zj13RiSTyWQydTik+qj6qtpJuVacVP1SDaoWUg68V/WqFqgmqVao7jdUjBOeqa6b+Knqtomb8VO1xsQYsHUmDh5rb0NFm1nJRoQucR1n4M1gk8As4XPXRzzE+1WnVbso11auqt6qZnMiwkMp3hiAhyXVDNRgNjLwscwCP8xxJZaojsvYE1umuqDq/lNRncmqF6rXqqmUa0ZYCkzKtyB/g01x/lETfzfHpZmgeqxaJa7BAdVmn0ODp/xxWWaq3qjuiGu7KqkBSfkW5C+xKc6/YuIRVb/qg+qMz/eYfJSzqomqDeJOWGxyh71XhkWqYdV5TlQkNSApP4B7QD52ffivTIzddK2Jl4urmWW8Agf9710pduRcxGOwTLHT9HGiJqkBSfkW5PHKYODfZJNADQawJSh8HvFadQ5bMWoOcKImqWumfAvy19gU558wMd6fTJn2R0HR1og3RF6KMLOOcaIinyTe4diDZFCT2vXCvW338b6x9CilBirMCss273WS3wp8CX8Rt2zrsEWKfQHw8DAsPIsxSHxueP8Edvh4vvEAvJfkFcAOhUJ8nIHwYkSn6zJd3Gy8xYkS4Nq7TXzEe5Z33ttjPLyM+eFihvKfJ9zW5YgXJYzmE3/8WTWvoaI+HaoH4tqfQrkU08T1457qkbjdlD81lor7RmNWizv3orjBxCRg5oirwecBfr9Jsf0oKMZS+9f8zQxtOxul5LT738G/HMJan0u5jAFrGrveJim5TjOZTCaTGZf8BqtNtgh8KhRfAAAAAElFTkSuQmCC>