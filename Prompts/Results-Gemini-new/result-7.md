# **Đặc Tả Thiết Kế Phần Mềm: Nền Tảng Phát Hiện Sớm Bất Thường Dữ Liệu Log Dựa Trên Sinh Tăng Cường Bằng Truy Xuất Có Điều Kiện**

Tài liệu Đặc tả Thiết kế Phần mềm (Software Design Specification \- SDS) này thiết lập một khuôn khổ kiến trúc kỹ thuật toàn diện nhằm chuyển đổi một mô hình học sâu đã được bình duyệt thành một hệ thống phần mềm nghiên cứu có khả năng tái lập hoàn toàn. Trọng tâm của kiến trúc này là giải quyết hiện tượng bão hòa cảnh báo giả (Alert Fatigue) trong môi trường hệ thống mở (Open-World), một rào cản nghiêm trọng đã được xác nhận trong các nghiên cứu thuộc phân nhóm Q11. Hệ thống phần mềm được thiết kế tuân thủ các tiêu chuẩn thực hành nghiêm ngặt nhất của kỹ thuật phần mềm (Software Engineering) kết hợp với kỷ luật thực nghiệm khoa học, đảm bảo mọi sự gia tăng về hiệu năng phát hiện sớm đều có thể được quy chiếu nhân-quả trực tiếp về mô-đun cải tiến.

## **1\. Kiểm tra Design Freeze**

Quá trình kiểm tra thiết kế đóng băng (Design Freeze Verification) đóng vai trò là chốt chặn học thuật và kỹ thuật đầu tiên, đảm bảo rằng nền tảng lý thuyết đã được phê duyệt sẽ được ánh xạ chính xác và trung thành vào các cấu trúc mã nguồn. Sự nghiêm ngặt trong khâu này ngăn chặn tuyệt đối hiện tượng trôi dạt phạm vi nghiên cứu (scope creep) và bảo vệ tính hợp lệ nội tại của mọi phép so sánh đối chứng1. Phương pháp cơ sở được lựa chọn là LogOW, một thuật toán học bán giám sát định lượng độ bất định được xuất bản chính thức trên tạp chí Q1 *Journal of Systems and Software* vào năm 2024/20251.

| Thành phần | Định nghĩa đã phê duyệt | Q1/Q2 & Publication Check | Diễn giải ở mức phần mềm |
| :---- | :---- | :---- | :---- |
| Baseline | Mô hình LogOW (A Semi-Supervised Log Anomaly Detection Model in Open-World Setting)1. | Tạp chí: *Journal of Systems and Software* (Q1, SJR 2024: 0.975). Năm: 2024\. Đã bình duyệt1. | Tái sử dụng nguyên vẹn trọng số mạng nơ-ron Bayes (BNN), cơ chế cửa sổ trượt, biểu diễn vector liên tục và Monte Carlo Dropout1. |
| Hạn chế | Bão hòa cảnh báo giả do cô lập tri thức khi hệ thống đối mặt với trượt dạt khái niệm1. | Bằng chứng học thuật xác nhận hạn chế này qua thực nghiệm luồng dữ liệu ngoài phân phối (OOD)1. | Mã nguồn gốc thiếu cơ chế tích hợp cấu hình ngoại vi, dẫn đến việc cắm cờ bất định sai lệch cho các sự kiện cập nhật hợp lệ. |
| Cải thiện có mục tiêu | Mô-đun RAG-SLM phân loại có điều kiện (Conditional RAG-SLM Triage)1. | Đảm bảo tính can thiệp tách rời (Decoupled Intervention)1. | Cấu trúc phần mềm thiết lập một cổng quyết định hậu xử lý. API truy vấn RAG/SLM chỉ được gọi khi mức Entropy vượt ngưỡng động ![][image1]1. |
| Thực nghiệm chính | Đối chứng trực tiếp giữa Original Baseline và Improved Baseline (LogOW \+ RAG-SLM)1. | Cấu trúc đối chứng phân chia thời gian thực (Chronological Split)1. | Các script thực nghiệm (Runner) được thiết kế để chạy tự động qua nhiều seed, khóa chặt biến số môi trường và ghi nhận log qua MLflow1. |
| Metric chính | DLT, EWH, DBF, FPR trên dữ liệu vùng biên, Latency1. | Thiết lập khung đo lường động học chống rò rỉ dữ liệu1. | Mô-đun đánh giá tính toán ![][image2], loại bỏ hoàn toàn các phương pháp đánh giá tĩnh thuần túy trên các phiên log đã hoàn tất1. |

Sự đối chiếu chi tiết này khẳng định kiến trúc phần mềm không tự ý mở rộng phạm vi hay phát minh ra các thuật toán không tồn tại trong thiết kế kỹ thuật. Mọi quyết định kiến trúc đều xoay quanh việc tạo ra một môi trường thực thi an toàn để đánh giá hiệu quả của mô-đun sinh tăng cường bằng truy xuất.

## **2\. Phạm vi Phần mềm**

Việc thiết lập các ranh giới hệ thống là bước thiết yếu để kiểm soát độ phức tạp của quy trình phát triển, đảm bảo phần mềm tập trung hoàn toàn vào việc phục vụ tính hợp lệ của nghiên cứu khoa học thay vì theo đuổi các mục tiêu thương mại hóa không cần thiết.

### **Trong phạm vi**

Kiến trúc phần mềm bao trùm toàn bộ các khối điện toán và vi kiến trúc cần thiết để tái lập phương pháp cơ sở LogOW từ mã nguồn gốc được cung cấp trên kho lưu trữ Zenodo, đồng thời triển khai cơ chế cải thiện độc lập. Các thành phần trong phạm vi bao gồm một hệ thống tải và tiền xử lý dữ liệu động tích hợp bộ phân tích cú pháp biểu thức chính quy (Drain parser) nhằm trích xuất các mẫu log cốt lõi1. Hệ thống cũng bao gồm việc thiết lập bộ chứa cơ sở dữ liệu vector cục bộ nhằm kiến tạo không gian truy xuất ngữ nghĩa lai (Hybrid Search) kết hợp giữa đối sánh từ khóa và vector dày đặc. Hơn nữa, kiến trúc bao hàm một công cụ suy luận (inference engine) chạy trên vi kiến trúc GPU nhằm gia tốc quá trình sinh ngôn ngữ của Mô hình Ngôn ngữ Nhỏ (SLM). Toàn bộ các mô-đun orchestrator để tự động hóa các kịch bản chạy thử nghiệm (Ablation, Baseline, Improved) và các bộ định lượng metric động học (DLT, FPR, Throughput) đều nằm trọn vẹn trong ranh giới thiết kế này1.

### **Ngoài phạm vi**

Nhằm duy trì bản chất là một phần mềm nghiên cứu tối thiểu nhưng có khả năng tái lập cao, kiến trúc từ chối tích hợp các thành phần thuộc nền tảng AIOps doanh nghiệp. Phần mềm không bao gồm các bảng điều khiển giao diện người dùng đồ họa (GUI/Dashboards) hay các công cụ trực quan hóa thời gian thực. Hệ thống không tích hợp cơ chế tự trị khắc phục sự cố vật lý (Autonomous Remediation) can thiệp ngược lại vào hệ điều hành của cụm máy chủ. Tương tự, hạ tầng phục vụ đa khách hàng (Multi-tenant Architecture), khả năng cân bằng tải mạng (Load Balancing), tính khả dụng cao (High Availability), hay các kịch bản triển khai trên cụm Kubernetes thương mại đều nằm ngoài phạm vi của kiến trúc này. Thiết kế giới hạn ở việc tạo ra một môi trường thực nghiệm khép kín, cô lập các yếu tố nhiễu loạn vận hành để chứng minh thuần túy giả thuyết khoa học.

## **3\. Kiến trúc Mã nguồn**

Hệ thống mã nguồn được tổ chức theo triết lý phân tách mối quan tâm (Separation of Concerns), đảm bảo sự cô lập tuyệt đối giữa mã nguồn kế thừa của phương pháp cơ sở và logic cải thiện mới được tích hợp. Cấu trúc thư mục định tuyến rõ ràng các trách nhiệm chức năng, hỗ trợ tối đa cho việc kiểm chứng thực nghiệm.  
project/ ├── configs/  
├── data/  
├── baseline/  
├── improvement/  
├── knowledge/  
├── retrieval/  
├── models/  
├── prompts/  
├── detection/  
├── evaluation/  
├── experiments/  
├── tests/  
├── artifacts/  
└── docs/  
Từng mô-đun trong cấu trúc trên được gắn với một trạng thái vòng đời cụ thể nhằm kiểm soát rủi ro xâm lấn mã nguồn. Thư mục configs/ quản lý toàn bộ tham số dưới dạng YAML để đảm bảo tính tái lập. Thư mục data/ chịu trách nhiệm tải và phân mảnh dữ liệu BGL/Thunderbird theo kỹ thuật Chronological Split để loại bỏ rò rỉ tương lai1. Thư mục baseline/ mang trạng thái Inherited; đây là khu vực bị khóa băng (frozen) tuyệt đối, chứa mã nguồn LogOW nguyên thủy từ Zenodo, nghiêm cấm mọi hành vi tinh chỉnh lại mạng nơ-ron Bayes1. Thư mục improvement/ chứa logic rẽ nhánh luồng lạnh và cổng điều kiện Entropy, mang trạng thái New. Các thư mục knowledge/ và retrieval/ đóng vai trò là não bộ ngoại vi, tương tác với ChromaDB, trong khi models/ và prompts/ giao tiếp với vLLM engine để chạy SLM cục bộ1. Thư mục evaluation/ mang trạng thái Evaluation-only, độc lập hoàn toàn với quá trình ra quyết định của mô hình nhằm ngăn chặn rò rỉ nhãn (Label Leakage) khi tính toán các chỉ số động học. Cuối cùng, experiments/ lưu trữ các runner script thực thi tự động các kịch bản từ E1 đến E71.

## **4\. Đặc tả Module và Interface**

Sự tương tác giữa các vi dịch vụ nội bộ được điều phối thông qua các giao diện (Interfaces) định kiểu nghiêm ngặt. Việc thiết lập hợp đồng dữ liệu rõ ràng giữa các khối giúp ngăn chặn sự phụ thuộc vòng (Circular Dependency) và đảm bảo luồng thông tin một chiều theo dòng thời gian thực.

| Module | Trách nhiệm | Đầu vào | Đầu ra | Phụ thuộc | Trạng thái |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Dataset Loader | Trích xuất luồng sự kiện thô và áp đặt kỹ thuật cắt theo thời gian. | Tệp CSV/JSON log thô (BGL, Thunderbird). | Chuỗi sự kiện có nhãn thời gian và chia tập Train/Test. | Không | Modified |
| Log Parser | Chuẩn hóa ngôn ngữ máy thành từ vựng tính toán thông qua thuật toán Drain. | Chuỗi sự kiện thô. | Log templates (Keys) và tham số biến thiên. | Dataset Loader | Inherited |
| Window Generator | Phân mảnh luồng sự kiện theo bối cảnh cục bộ. | Log templates. | Sliding Context Windows. | Log Parser | Inherited |
| Baseline BNN | Chạy Monte Carlo Dropout để xấp xỉ Bayes và tính Entropy1. | Sliding Context Windows. | Điểm Predictive Entropy (![][image3]). | Window Generator | Inherited |
| Triage Gate | Điều phối luồng dữ liệu nóng/lạnh dựa trên ngưỡng động ![][image1]1. | Điểm Predictive Entropy (![][image3]). | Tín hiệu chuyển tiếp luồng nóng hoặc đóng băng luồng lạnh. | Baseline BNN | New |
| Retrieval | Khai thác ngữ cảnh ngoại vi bằng Tìm kiếm lai. | Cửa sổ log bất định (Query). | Top-K tài liệu vận hành (Context). | Triage Gate | New |
| SLM Adapter | Thực thi In-context Learning qua vLLM engine1. | System Prompt \+ Retrieved Context. | Cấu trúc JSON nhị phân (Benign/Anomaly). | Retrieval, Prompts | New |
| Early Detection | Tính toán thời gian dẫn trước từ dữ liệu cảnh báo. | Nhãn dự đoán \+ Nhãn sự cố vật lý ![][image4]. | Metric DLT, EWH, DBF, FPR1. | SLM Adapter | Eval-only |

Giao diện quan trọng nhất trong hệ thống là luồng giao tiếp tại cổng phân giải bất định (Triage Gate). Mục đích của giao diện này là khắc phục sự cô lập tri thức tại vùng biên phân phối dữ liệu. Schema đầu vào được yêu cầu là một đối tượng JSON chứa mảng các chuỗi log hiện tại, nhãn thời gian ![][image5], và ngưỡng độ tin cậy mong muốn. Trường ![][image5] là bắt buộc để kích hoạt bộ lọc tài liệu tương lai, ngăn chặn mô hình đọc các báo cáo sinh ra sau khi sự cố đã xảy ra. Schema đầu ra là một đối tượng JSON bao gồm cờ phân loại nhị phân is\_anomaly, nhãn phân lớp reason\_class, và mảng retrieved\_evidence chứa ID của tài liệu đối chứng. Trong các trường hợp lỗi như quá hạn thời gian (Timeout) hoặc SLM trả về JSON sai định dạng, giao diện được thiết kế để tự động thoái lui (Fallback) về quyết định cảnh báo bất thường mặc định của Baseline, qua đó duy trì tính an toàn bảo mật cấp cao (Fail-safe) cho toàn bộ đường ống giám sát.

## **5\. Tách biệt Baseline và Cải thiện**

Yêu cầu tiên quyết của đặc tả phần mềm là mô hình cơ sở phải duy trì khả năng chạy độc lập hoàn toàn để chứng minh đường cơ sở của rủi ro. Việc chạy song song hệ thống cũ và mới phải được cấu hình linh hoạt thông qua tham số khởi chạy của trình quản lý thực nghiệm. Phương pháp cơ sở LogOW, được xác nhận công bố trên tạp chí Q1, là đối tượng tham chiếu tuyệt đối và không thể bị xâm phạm cấu trúc nội tại1.  
Hệ thống phần mềm thiết lập các chế độ thực thi cốt lõi thông qua tham số môi trường: Trong chế độ baseline, hệ thống vận hành theo đúng thiết kế nguyên thủy. Khi Predictive Entropy vượt qua ngưỡng ![][image1], phần mềm xuất lệnh cảnh báo "Bất định" trực tiếp ra ngoài và chuyển sang quy trình phân tích lỗi truyền thống1. Mô-đun truy xuất tri thức ngoại vi bị ngắt kết nối hoàn toàn ở chế độ này, tạo điều kiện lý tưởng để hệ thống đo lường trực tiếp tình trạng bão hòa cảnh báo giả (Alert Fatigue) khi gặp dữ liệu OOD1. Trong chế độ improved, hệ thống kích hoạt luồng xử lý phân luồng kép (Dual-path Inference). Cổng Triage Gate sẽ chặn các tín hiệu bất định lại, triệu hồi kho tri thức vector cục bộ, sinh Prompt và chờ hồi đáp phân loại từ SLM trước khi đưa ra quyết định cuối cùng1. Trong chế độ ablation, hệ thống cho phép nhà nghiên cứu vô hiệu hóa từng thành phần đơn lẻ của mô-đun cải thiện1. Các kịch bản bao gồm việc gọi SLM nhưng không cung cấp Context từ Retrieval, hoặc loại bỏ thuật toán suy giảm trọng số theo thời gian (Time-decay). Chế độ này phục vụ việc định lượng mối quan hệ nhân-quả của từng thay đổi kiến trúc đối với sự gia tăng hiệu năng tổng thể.  
Dưới mọi hình thức, phần cải thiện bị nghiêm cấm việc âm thầm thay đổi bộ định nghĩa của các metric đánh giá tĩnh hoặc động học. Mạng nơ-ron cơ sở sử dụng cùng một tệp trọng số (frozen weights) được nạp từ đĩa cứng chung cho mọi chế độ, triệt tiêu hoàn toàn các thiên lệch do huấn luyện lại (Tuning Bias) giữa các lần so sánh đối chứng1.

## **6\. Đặc tả Cấu hình**

Toàn bộ siêu tham số điều khiển vòng đời nghiên cứu được trừu tượng hóa vào các tệp YAML. Việc định nghĩa chặt chẽ miền giá trị hợp lệ loại trừ các lỗi runtime và đảm bảo khả năng lưu vết toàn vẹn cấu hình (Config snapshot) trong hệ thống quản lý artifact1.  
Tệp dataset.yaml định nghĩa nguồn luồng sự kiện phân tán. Trường dataset\_name là chuỗi văn bản với miền hợp lệ bao gồm bgl hoặc thunderbird1. Trường split\_method bị khóa cứng (Fixed) ở giá trị chronological nhằm thiết lập hàng rào chống rò rỉ dữ liệu thời gian tương lai1. Trường train\_ratio thiết lập tỷ lệ phân chia mặc định ở mức 0.7.  
Tệp baseline.yaml quy định các tham số nội tại của mạng nơ-ron và bộ phân tích. Trường parser\_depth được cố định ở giá trị 4 để thiết lập độ sâu của cây tìm kiếm Drain parser1. Trường mc\_dropout\_passes được cố định ở giá trị 10 trong các thực nghiệm chính, đại diện cho số vòng truyền ngẫu nhiên nhằm xấp xỉ mạng nơ-ron Bayes sinh phân phối dự đoán1.  
Tệp improvement.yaml chứa các tham số điều chỉnh sự nhạy cảm của luồng RAG. Trường triage\_threshold\_multiplier có giá trị mặc định 1.5, đóng vai trò là tham số có thể điều chỉnh (Tunable) trên tập validation, dùng làm hệ số nhân với độ lệch chuẩn Entropy để sinh ra ngưỡng chặn động ![][image1]1. Trường fallback\_action mặc định là anomaly, quyết định thái độ an toàn của hệ thống khi SLM gặp lỗi phân giải.  
Tệp model.yaml định nghĩa tác tử lập luận. Trường llm\_model tham chiếu định danh mô hình cục bộ, mặc định sử dụng llama-3-8b-instruct1. Trường quantization được chỉ định là 4-bit-awq nhằm tối ưu hóa dung lượng VRAM để tích hợp vào luồng thời gian thực1. Trường temperature bị khóa cứng (Fixed) ở giá trị 0.0, ép buộc quá trình sinh ngôn ngữ mang tính xác định (deterministic)1. Trường seed cung cấp giá trị ngẫu nhiên gốc, mặc định là 42\.  
Tệp retrieval.yaml điều khiển không gian vector. Trường chunk\_size khống chế độ dài phân mảnh tài liệu ở mức 512 token1. Trường top\_k mặc định là 3 tài liệu vận hành sẽ được đẩy vào ngữ cảnh của LLM1. Trường similarity\_threshold ở mức 0.75 đóng vai trò là ngưỡng cắt bỏ các tài liệu nhiễu trong chức năng tìm kiếm lai (Hybrid Search)1. Tệp evaluation.yaml cuối cùng định nghĩa mảng các metric mục tiêu như DLT, EWH, FPR, F1, và Latency.

## **7\. Thiết kế LLM / Prompt / Model**

Mô hình nền tảng (Foundation Model) được cấy ghép vào hệ thống không đóng vai trò như một cỗ máy phân tích dữ liệu toàn năng quét qua hàng triệu dòng log thô, mà hoạt động như một Tác tử Phân loại (Triage Agent) cấp cao chuyên biệt xử lý các điểm nghẽn logic vùng biên1. Để đảm bảo quá trình đối sánh công bằng, mọi lần chạy cải tiến hay cắt lớp đều phải nạp chung một cấu hình mô hình duy nhất.  
Giao diện hệ thống kết nối trực tiếp với vLLM, một engine phục vụ suy luận hiệu suất cao, giúp duy trì thông lượng tối đa thông qua kỹ thuật quản lý bộ nhớ PagedAttention1. Ranh giới giữa Provider và Adapter được thiết kế theo mẫu Adapter Pattern, cho phép mã nguồn chỉ giao tiếp với một giao diện trừu tượng, ẩn đi sự phức tạp của các tensor cục bộ. Metadata của phiên bản mô hình, ví dụ như cấu trúc Llama-3-8B-Instruct AWQ 4-bit, được lưu vết vĩnh viễn trong nhật ký chạy của nền tảng MLflow.  
Kiến trúc Trình tạo mẫu lệnh (Prompt Engine) đóng gói dữ liệu qua cấu trúc In-context Learning khắt khe nhằm ngăn chặn sự suy diễn vô căn cứ. Cấu trúc Prompt bao gồm bốn thành phần cốt lõi: Thứ nhất, System Instruction thiết lập định danh của tác tử là một chuyên gia AIOps, giới hạn nghiêm ngặt không gian suy luận chỉ nằm gọn trong tài liệu RAG vừa lấy được (Context-bound strictness), triệt tiêu sự bay bổng ngôn ngữ tự do để chống hiện tượng ảo giác (Hallucination)1. Thứ hai, Current Context trình bày cửa sổ trượt của luồng sự kiện đang bị mắc kẹt tại mạng Bayes do điểm Entropy vượt ngưỡng. Thứ ba, Retrieved Context liệt kê top các tài liệu thiết kế, Git commits hoặc cấu hình mạng liên quan nhất được nội suy từ cơ sở dữ liệu Vector1. Cuối cùng, Output Schema Specification ép buộc LLM trả về cấu trúc định dạng JSON chuẩn hóa, đảm bảo hệ thống tự động có thể phân tích cú pháp kết quả.  
Các tham số lấy mẫu như Temperature bị khóa ở giá trị 0.0. Thiết kế này triệt tiêu hoàn toàn sự biến thiên kết quả qua các lần chạy khác nhau, đảm bảo mọi phán quyết về tính hợp lệ của bản nâng cấp phần mềm đều đạt tính nhất quán cao nhất.

## **8\. Tính Toàn vẹn Dữ liệu và Thời gian**

Trong bài toán phát hiện sớm, kỷ luật thời gian là bức tường thành bảo vệ tính chân thực của khoa học. Bất kỳ sự vi phạm trật tự nhân-quả nào cũng sẽ gây ra rò rỉ dữ liệu tương lai (Data Leakage), tạo ra ảo giác hiệu năng và phá hủy toàn bộ hệ mét cảnh báo1. Kiến trúc phần mềm áp dụng chế độ phòng ngự nhiều lớp đối với nhãn thời gian (Timestamp).  
Cơ chế phân tách tập dữ liệu (Chronological Split) loại bỏ hoàn toàn các hàm xáo trộn thư viện tiêu chuẩn. Luồng dữ liệu được sắp xếp tuyệt đối theo thời gian tuyến tính của chuỗi sự kiện. Thuật toán phân mảnh bảo vệ nguyên vẹn các phiên (sessions) bắc cầu qua ngưỡng cắt thời gian 70% huấn luyện và 30% đánh giá. Điểm thời gian quan sát (Observation Time) trượt liên tục, và mô hình chỉ có quyền truy cập vào thông tin tại không gian lùi về quá khứ tính từ dấu mốc này. Thời điểm đưa ra quyết định dự đoán được mã hóa là ![][image5], trong khi thời điểm xảy ra sự cố vật lý thực sự được mã hóa là ![][image4]1.  
Tính toàn vẹn trong mô-đun sinh tăng cường được đảm bảo bởi bộ điều khiển Sẵn sàng Tri thức Thời gian (Temporal Availability Control). Mọi tài liệu ngoại vi nạp vào cơ sở dữ liệu Vector đều được gắn chặt với nhãn thời gian khởi tạo ![][image6]1. Tại thời điểm mạng nơ-ron đưa ra đánh giá tại ![][image5], phần mềm kích hoạt thuật toán lọc cứng (Strict Temporal Filter) ở lớp truy vấn1. Hệ thống bắt buộc tiêm thêm điều kiện lọc WHERE timestamp \< T\_alert vào truy vấn cơ sở dữ liệu. Thiết kế này ngăn chặn vĩnh viễn rủi ro RAG vô tình truy xuất các báo cáo khắc phục sự cố (post-mortem reports) được viết sau khi hệ thống đã sập để "dự đoán" ngược lại chính sự cố đó. Nhãn thời gian sụp đổ ![][image4] bị ẩn đi hoàn toàn trong môi trường chạy suy luận (Inference), và chỉ được nạp vào bộ nhớ khi script đánh giá cuối cùng bắt đầu hoạt động.

## **9\. Phần mềm Knowledge / Retrieval**

Mô-đun truy xuất dữ liệu đóng vai trò kiến tạo không gian tri thức nội bộ, phân giải ranh giới giữa một lỗi phần cứng thực sự và một cấu hình hợp lệ mới được triển khai. Cơ sở hạ tầng dựa trên cơ sở dữ liệu ChromaDB vận hành cục bộ.  
Quá trình Nhập liệu và Quản lý Tri thức (Knowledge Ingestion) thu gom toàn bộ sổ tay kỹ thuật (Runbooks) và lịch sử Git Commits, sau đó tiến hành phân mảnh (Chunking) theo kích thước cố định 512 tokens để tương thích với cửa sổ nạp của SLM1. Lớp Metadata quản lý cấu trúc các trường bao gồm định danh chuỗi, phân loại tài liệu, và nhãn thời gian ![][image6]. Hệ thống lập chỉ mục phiên bản kho tri thức bằng hàm băm (MD5 Hash) để phục vụ quá trình tái lập. Tính hợp lệ thời gian quyết định sự tồn tại hợp pháp của tài liệu trong quá trình đối chiếu ngữ nghĩa.  
Hệ thống Tìm kiếm Lai (Hybrid Retrieval) được triển khai để chống lại rủi ro lệch chuẩn không gian nhúng (Embedding Mismatch). Hiện tượng này xảy ra khi các mô hình nhúng văn bản tự nhiên mã hóa sai lệch địa chỉ IP hoặc mã lỗi thập lục phân. Kiến trúc kết hợp điểm số tương đồng ngữ nghĩa bằng Cosine Similarity từ các bộ mã hóa chuyên biệt mã nguồn (Code-specific Dense Embeddings) với thuật toán đối sánh từ khóa rời rạc Sparse (BM25)1. Việc này cho phép hệ thống vừa nắm bắt ý định bảo trì tổng quát, vừa bắt khớp chính xác các chuỗi định danh mã lỗi.  
Khâu Xếp hạng và Xây dựng Ngữ cảnh (Context Builder) tổng hợp điểm số từ hệ thống lai. Để loại bỏ tri thức đã lỗi thời (Stale knowledge), phần mềm áp dụng hàm suy giảm trọng số theo thời gian (Timestamp-decay penalty)1. Tài liệu có ![][image6] càng cách xa ![][image5] về quá khứ sẽ bị trừ điểm tương đồng. Thuật toán tiếp tục loại bỏ các kết quả nhiễu bằng ngưỡng cắt similarity\_threshold \> 0.75 và thực thi cắt cụt (Truncation) để lấy Top-3 tài liệu tốt nhất1. Không gian ngữ cảnh cuối cùng bị khóa chặt, đảm bảo tổng lượng token bơm vào mô hình LLM không vượt qua giới hạn của hệ thống.

## **10\. Đặc tả Phần mềm Thực nghiệm**

Thực thi tự động hóa khoa học được quản lý thông qua một Experiment Runner đa luồng. Mô-đun này được thiết kế để cô lập từng biến số kiểm soát, phục vụ trực tiếp các bài kiểm tra được định nghĩa trong hồ sơ phê duyệt, liên kết với các giả thuyết từ H1 đến H31. Các hàm chạy thực nghiệm bao gồm 5 chế độ hoạt động chính:  
**Chế độ A — Baseline (E1):** Thực thi mạng nơ-ron Bayes LogOW trên luồng dữ liệu. Mục tiêu cốt lõi là tái lập mô hình cơ sở, ghi nhận điểm nghẽn Alert Fatigue khi tỷ lệ cảnh báo giả bùng nổ trên tập dữ liệu trượt phân phối, tạo lập hệ mét FPR cơ sở1.  
**Chế độ B — Improved (E2, E4):** Triển khai phân luồng kép. Phương sai dự đoán của BNN đóng vai trò chặn lọc, điều hướng các tín hiệu bất định sang luồng RAG-SLM Triage. Metric thu thập trọng tâm ở chế độ này là sự cải thiện của thời gian dẫn trước (DLT) và sự suy giảm của FPR tại các vùng biên phân phối1.  
**Chế độ C — Ablation (E3):** Chạy các cấu hình cắt lớp chuyên sâu. Cấu hình thứ nhất ép luồng log chạy trực tiếp qua SLM mà không có RAG để quan sát hiện tượng ảo giác (Hallucination), chứng minh sự cần thiết của RAG. Cấu hình thứ hai vô hiệu hóa tìm kiếm BM25 để đánh giá rủi ro không gian nhúng. Cấu hình thứ ba hủy bỏ cổng điều kiện Entropy để đẩy 100% dữ liệu qua SLM, phơi bày sự sụp đổ về độ trễ tính toán nếu thiếu mạng Bayes chặn lọc1.  
**Chế độ D — Robustness (E5):** Bơm nhiễu loạn nhân tạo vào dữ liệu, đẩy tỷ lệ log template mới lên 20-40% để kiểm tra giới hạn chịu tải cực đại của mô-đun RAG-SLM và mô hình BNN khi trượt dạt khái niệm xảy ra dồn dập1.  
**Chế độ E — Efficiency (E6):** Định lượng chi phí vận hành. Script giám sát tích hợp bộ đo thời gian vi giây, tính toán thông lượng hệ thống (Throughput \- Logs/giây) và độ trễ tính toán chênh lệch giữa luồng nóng (mạng nơ-ron cục bộ) và luồng lạnh (truy xuất RAG và gọi SLM API qua vLLM)1. Thực nghiệm E7 chạy song song để đánh giá mức độ tổng quát hóa trên đa hệ thống1.  
Mỗi phiên chạy lưu trữ một đối tượng dữ liệu hoàn chỉnh vào MLflow bao gồm: Experiment ID, Snapshot của các file cấu hình YAML, phiên bản Dataset (Hash MD5), thông số mô hình SLM, hạt giống ngẫu nhiên seed=42, siêu dữ liệu Metric chuỗi thời gian, và Artifacts (Confusion Matrix, JSON output).

## **11\. Phần mềm Đánh giá**

Việc đánh giá trong không gian hệ thống mở yêu cầu phần mềm định lượng động học thay vì các điểm số F1 tĩnh truyền thống. Sự đánh đồng giữa phát hiện lỗi sau sự kiện và cảnh báo sớm là điều bị nghiêm cấm trong cấu trúc phần mềm. Cùng một giao thức đánh giá được gắn cho mọi chế độ nhằm đảm bảo tính công bằng.  
Module Phát hiện Sớm (Early Detection) tập trung vào các hệ mét sau:

* **Time-to-Detection & Detection Lead Time (DLT):** Đây là thước đo sống còn của hệ thống. Thuật toán sẽ đối chiếu tập các cảnh báo sinh ra (![][image5]) với danh sách nhãn thời gian sụp đổ vật lý hệ thống (![][image4]). Công thức tính toán được định nghĩa là ![][image2]1. Thuật toán tự động loại bỏ bất kỳ cảnh báo nào có DLT âm (nghĩa là phát hiện trễ sau khi hệ thống đã sập) khỏi tính toán năng lực cảnh báo sớm.  
* **Early Warning Horizon (EWH):** Xác định khoảng quan sát thời gian thực tối đa mà mô hình duy trì độ tin cậy trước khi bị bão hòa bởi tín hiệu nhiễu1.  
* **Detection Before Failure (DBF):** Tỷ lệ phần trăm số sự cố sụp đổ được báo hiệu thành công trước mốc zero.

Module Phát hiện Thống kê (Detection) phân tích hiệu năng nhị phân:

* **False Positive Rate (FPR):** Phân hệ mã nguồn đặc biệt tập trung đo lường tỷ lệ cảnh báo giả trên nhóm luồng sự kiện chưa từng thấy (Out-of-Distribution). Sự sụt giảm chỉ số này trên tập OOD là minh chứng tuyệt đối cho năng lực của hệ thống RAG-SLM trong việc giải quyết Alert Fatigue1.  
* Các chỉ số Precision, Recall, F1, PR-AUC, ROC-AUC được trích xuất bằng thư viện Scikit-Learn tiêu chuẩn để đối chiếu tham chiếu với các bài báo nền tảng.

Module Đo lường Hiệu năng (Efficiency) tính toán độ trễ (Latency) trung bình cho luồng nóng (\< 5ms) và luồng lạnh (500ms \- 1200ms)1. Hệ thống cũng thu thập Token Cost (chi phí sinh ngôn ngữ) và Memory footprint bằng các tiện ích cấu hình CUDA.

## **12\. Logging và Xử lý Lỗi**

Chức năng Logging được thiết kế chuyên biệt để phục vụ tính minh bạch của nghiên cứu khoa học, không hướng đến khả năng quan sát (observability) của nền tảng sản xuất đám mây.  
Quá trình theo dõi hệ thống được tích hợp trực tiếp với MLflow tracking API để lưu thông số cấu hình và các mốc thời gian thực thi. Log mô hình và truy xuất ghi nhận độ dài tài liệu ngữ cảnh trả về và tính điểm Context Relevance dựa trên sự tương đồng Cosine. Toàn bộ JSON thô được SLM sinh ra cũng được ghi vết vào ổ đĩa cứng. Các ngoại lệ liên quan đến việc nạp tệp hay vỡ cấu trúc CUDA Out-Of-Memory (OOM) được ném ra với định dạng Error Level nghiêm trọng.  
Chiến lược Xử lý Ngoại lệ (Fault Tolerance) giải quyết rủi ro từ các mô hình sinh ngôn ngữ lớn, vốn chứa đựng sự không ổn định trong cấu trúc đầu ra. Khi SLM trả về một đoạn chuỗi không hợp lệ với JSON schema, hoặc API gặp hiện tượng quá hạn thời gian (Timeout), cơ chế Fallback được kích hoạt ngay lập tức. Hệ thống sẽ tự động thoái lui về quyết định cảnh báo Anomaly mặc định của baseline BNN. Giải pháp "Fail-safe" này đảm bảo hệ thống phân tích luồng thời gian thực không bao giờ bị nghẽn (Blocking) do độ trễ mạng hay ảo giác văn bản. Các trường hợp thiếu dữ liệu đầu vào hoặc lỗi truy xuất ChromaDB đều sẽ trả về mảng ngữ cảnh rỗng, ép SLM phải đánh giá dựa trên đặc trưng chuỗi hiện tại, qua đó duy trì tính trơn tru của quy trình đánh giá độ trễ.

## **13\. Chiến lược Kiểm thử**

Mỗi dòng mã phục vụ khoa học phải trải qua các bài kiểm định khắt khe nhằm xác lập mức độ tin cậy tuyệt đối vào dữ liệu được công bố trong luận văn.

* **Unit Test:** Được triển khai bằng PyTest cho các hàm xử lý chuỗi Drain Parser, hàm trượt cửa sổ (windowing), các hàm tính toán khoảng cách cosine trong hệ thống hybrid retrieval, và kiểm tra độ chính xác toán học của các công thức tính DLT, EWH.  
* **Integration Test:** Đảm bảo luồng giao tiếp giữa dữ liệu và baseline BNN được thông suốt. Các bài kiểm thử xác minh việc truyền tải Query từ mạng Bayes sang ChromaDB và việc tiêm Context vào Prompt LLM hoạt động tương thích, sinh JSON chuẩn định dạng.  
* **End-to-End Test:** Vận hành một chu trình chạy rút gọn qua tất cả các mô-đun trên một tập mẫu BGL mini (khoảng 1000 dòng log). Xác minh chuỗi Pipeline tổng thể từ lúc nạp dữ liệu đến lúc xuất Report MLflow hoạt động không có điểm nghẽn.  
* **Regression Test:** Đảm bảo mã nguồn sau khi được tái cấu trúc thành khuôn khổ phần mềm mới không làm thay đổi các hệ mét nền tảng của phương pháp LogOW gốc1.  
* **Research Validity Test:** Cơ chế Assertion logic nội bộ kiểm tra chéo liên tục. Hệ thống sẽ tự động dừng nếu phát hiện tập train và test có sự trùng lặp thời gian (vi phạm future leakage), hoặc nếu trọng số của Baseline BNN bị biến đổi sau khi nạp (vi phạm nguyên tắc Fixed Weights), hoặc nếu nhãn sự cố sụp đổ vô tình xuất hiện trong Prompt của LLM.

## **14\. Quản lý Artifact và Phiên bản**

Tính tái lập (Reproducibility) được cấu trúc hóa trong kỹ thuật đóng gói Artifact. Triết lý thiết kế đòi hỏi bất kỳ nhà nghiên cứu độc lập nào cũng có thể tải về hệ thống và khôi phục lại kết quả chỉ qua một lệnh thực thi duy nhất.  
Mỗi đợt chạy (Experiment Run) sẽ bảo lưu vĩnh viễn trên ổ cứng các siêu dữ liệu sau:

* Toàn bộ tệp cấu hình YAML làm chứng tích.  
* Mã băm định danh (Hash) của bộ dữ liệu BGL và Thunderbird đã phân tách thời gian, đảm bảo sử dụng chung một tập dataset reference.  
* Định danh mô hình SLM, cấu hình hệ số Prompt và Retrieval Settings.  
* Dữ liệu thô của DLT và FPR trên từng tệp CSV kết quả, cùng biểu đồ (Plots) đường cong PR/ROC và Ma trận Nhầm lẫn (Confusion Matrices).  
* Tệp Log chi tiết luồng làm việc của vLLM.

Quản trị phiên bản mã nguồn kiểm soát chặt chẽ trạng thái của thư mục baseline/. Mã nguồn LogOW kế thừa từ nhánh lưu trữ trên nền tảng khoa học Zenodo (chứa 1.4 GB dữ liệu) bị khóa cứng phiên bản1. Mọi phiên bản chỉnh sửa thông số cải thiện đều được sinh thành một nhánh Run mới trong MLflow, không bao giờ cho phép phần mềm ghi đè hoặc sửa đổi một Artifact đã được dán nhãn "freeze".

## **15\. Bảo mật và Quyền riêng tư**

Tính chuyên biệt của môi trường nghiên cứu trên dữ liệu IT telemetry quy mô lớn tiềm ẩn nhiều rủi ro nếu rò rỉ thông tin cá nhân.

* **Bảo vệ quyền riêng tư:** Dữ liệu log thô (Raw Logs) mang theo địa chỉ IP thực, UserID, hoặc thông tin phiên làm việc nhạy cảm. Hệ thống thiết lập quy tắc Redaction ở lớp Dataset Loader để tự động che giấu (Masking) các trường này bằng chuỗi hash hoặc ký tự thay thế chung (Ví dụ: \[IP\_ADDRESS\]). Quy trình này được thực thi ngay trước khi văn bản đi vào các API của mô hình ngôn ngữ lớn, dù cho quá trình xử lý hoàn toàn diễn ra cục bộ.  
* **Quản trị Bí mật:** Nếu việc tải các LLM nhỏ yêu cầu chứng thực HuggingFace Token, các thông tin định danh API Secrets được bảo quản qua tệp .env môi trường, được khai báo rõ ràng vào .gitignore. Cấm tuyệt đối việc nhúng (hardcode) mật khẩu vào các tệp cấu hình JSON/YAML hoặc đính kèm vào các kho lưu trữ Artifact gửi lên mạng.

## **16\. Phạm vi Triển khai**

Kiến trúc triển khai vật lý được đóng khung trong năng lực giới hạn của một thiết lập phòng thí nghiệm để chứng minh tính khả thi của nghiên cứu.

* **Bắt buộc:** Triển khai một môi trường nghiên cứu Python cô lập cục bộ (thông qua Conda hoặc Virtualenv). Năng lực xử lý đồ họa phần cứng (GPU) là yêu cầu bắt buộc. Khuyến nghị cấu hình tối thiểu là card đồ họa Nvidia RTX 3090 hoặc 4090 với 24GB VRAM để chứa trọn vẹn mô hình ngôn ngữ Llama-3-8B phiên bản 4-bit và gia tốc đường truyền PyTorch của mạng nơ-ron Bayes cùng lúc1. Script suy luận theo bó (Batch Inference) vận hành tuyến tính.  
* **Tùy chọn:** Đóng gói toàn bộ kiến trúc (LogOW \+ vLLM \+ ChromaDB) thành các Container qua hệ thống Docker Compose. Cung cấp API giao tiếp bằng chuẩn REST thông qua FastAPI để chứng minh tính tách rời của kiến trúc trong mô phỏng truyền phát luồng dữ liệu (streaming prototype).  
* **Ngoài phạm vi:** Như đã định nghĩa, hệ thống từ chối triển khai Enterprise Orchestration qua Kubernetes, không thiết lập bảo mật IAM nâng cao cho người dùng đa tổ chức, hay kết nối trực tiếp vào luồng dữ liệu Kafka thương mại của doanh nghiệp.

## **17\. Lộ trình Phát triển**

Quá trình kiến tạo phần mềm bám sát mô hình Agile với vòng lặp Sprints, nhằm rà soát tính khả thi ở từng nút thắt cổ chai kỹ thuật. Các mốc phát triển được phân chia rõ ràng:

* **Mốc 1 — Môi trường & Thiết lập:** Tạo lập kho mã nguồn, file cấu hình dependencies (requirements.txt), và cấu hình hệ thống MLflow cục bộ. Cài đặt các kịch bản Unit test cốt lõi. Giao phẩm: Một môi trường Python sẵn sàng biên dịch mã nguồn PyTorch và vLLM mà không gặp xung đột thư viện.  
* **Mốc 2 — Baseline:** Tải và xử lý dữ liệu BGL/Thunderbird. Áp dụng nghiêm ngặt kỹ thuật Chronological Split. Tích hợp mã nguồn nguyên thủy của LogOW. Chạy vòng lặp Validation. Tiêu chí nghiệm thu: Tái lập thành công điểm FPR của thuật toán gốc trên dữ liệu tĩnh1.  
* **Mốc 3 — Improvement:** Xây dựng hệ thống ChromaDB cục bộ. Triển khai phương thức Tìm kiếm lai (Hybrid Search). Cấu hình Prompt Engineering cho SLM. Thiết lập nút rẽ nhánh Entropy điều hướng luồng dữ liệu nóng và lạnh. Khởi chạy thử nghiệm (smoke tests).  
* **Mốc 4 — Thực nghiệm Chính:** Kết nối mạch suy luận toàn trình. Chạy tự động đối chứng (Baseline vs Improved) thông qua các runner lặp lại nhiều lần. Thu thập dữ liệu JSON và chỉ số phân loại vùng biên OOD1.  
* **Mốc 5 — Ablation/Robustness:** Chạy các cấu hình tùy biến (Direct SLM, No Time-decay) và bơm nhiễu 20-40% OOD logs vào luồng thực thi để kiểm tra giới hạn chịu tải của hệ thống1. Trích xuất biểu đồ phân tích lỗi mô hình.  
* **Mốc 6 — Artifact cuối & Tài liệu:** Trích xuất các hệ mét DLT, EWH. Thực hiện phân tích ý nghĩa thống kê bằng kiểm định Wilcoxon signed-rank. Đóng băng toàn bộ Artifacts, dọn dẹp mã nguồn, cập nhật tài liệu README.md để đảm bảo khả năng tái lập cho cộng đồng nghiên cứu.

## **18\. Tiêu chí Chấp nhận**

Sự trưởng thành của phần mềm được đo lường bằng việc hoàn thành các rào cản kỹ thuật định tính và định lượng, đảm bảo nghiên cứu đủ điều kiện xuất bản học thuật.

* **Đối với Baseline:** Phần mềm thực thi độc lập quá trình tải, huấn luyện và suy luận LogOW mà không vấp lỗi kỹ thuật. Hệ mét tham chiếu cơ sở, đặc biệt là tỷ lệ cảnh báo giả (FPR) trên các chuỗi tĩnh, phải phản ánh được sát với công bố nguyên thủy của tác giả (sai số tolerance trong mức cho phép ngẫu nhiên)1.  
* **Đối với Improvement:** Mô-đun não bộ RAG-SLM phải vận hành tách rời. Cổng Entropy giám sát chính xác luồng truyền, chỉ khi ngưỡng ![][image1] bị phá vỡ mới tạo ra lệnh gọi API truy xuất. Việc bật/tắt luồng RAG phải trơn tru thông qua cấu hình YAML. JSON Schema trả về phải chuẩn hóa và cơ chế Fallback (khi Timeout) phải bắt được Exception để trả về cảnh báo gốc mà không gây sập phần mềm. Sự can thiệp tuyệt đối không thay đổi chu trình toán học bên trong mạng BNN.  
* **Đối với Thực nghiệm chính:** Môi trường thí nghiệm duy trì tính bất biến của các Controlled Variables (Data Split, Model Weights, Dropouts). Metrics thu thập qua nhiều đợt chạy lặp lại hiển thị đầy đủ trong Dashboard MLflow.  
* **Đối với Artifact:** Tệp cấu hình, thông số Hash phiên bản mã nguồn, dữ liệu JSON đánh giá và lịch sử thực thi được đóng gói gọn gàng. Phần mềm đạt chứng nhận khả năng truy xuất (Traceability) khi toàn bộ chuỗi nhân-quả được quy kết chính xác.

## **19\. Ma trận Truy vết**

Kiến trúc phần mềm là tấm gương phản chiếu của logic nghiên cứu. Ma trận truy vết (Traceability Matrix) dưới đây neo chặt từng dòng lệnh, mô-đun và thực nghiệm với các câu hỏi và giả thuyết khoa học gốc, đảm bảo mọi chi tiết kỹ thuật đều phục vụ việc xác thực lý thuyết1.

| Research Element | TDS Element | Software Module | Experiment | Metric |
| :---- | :---- | :---- | :---- | :---- |
| **RQ1:** Giới hạn của xấp xỉ Bayes (LogOW) trước bản cập nhật phần mềm (Concept Drift)?1 | Baseline BNN & Thresholding Gate. | baseline/, evaluation/ | E1 (Reproduction), E5 (Robustness)1. | Tỷ lệ FPR đo lường trên luồng OOD logs. |
| **RQ2:** RAG-SLM phân định cập nhật an toàn và cảnh báo sớm thế nào?1 | Improvement Module (SLM Triage & Prompt Engine)1. | improvement/, prompts/, models/ | E2 (Main Test), E3 (Ablation)1. | Hệ mét DLT, EWH, và FPR tại vùng biên bất định1. |
| **RQ3:** Ảnh hưởng của RAG-SLM lên kiến trúc thời gian thực?1 | Luồng phân giải kép (Dual-path Inference). | detection/, configs/ | E6 (Efficiency)1. | Latency (ms), Throughput (Logs/s). |
| **H1:** Bão hòa cảnh báo bắt nguồn từ sự cô lập tri thức1. | Lớp truy vấn ngữ cảnh nội bộ (Vector DB). | knowledge/, retrieval/ | E3 (Ablation: SLM w/o RAG)1. | Context Relevance, độ gia tăng FPR khi thiếu RAG. |
| **H2:** Tối ưu độ trễ bằng kích hoạt RAG có điều kiện (Entropy threshold)1. | Cổng Triage Gate (Kiểm tra ![][image1]). | improvement/ | E6 (Efficiency)1. | Token Cost, VRAM Memory, Tỷ lệ điều hướng luồng lạnh (\< 5%). |
| **H3:** Sự cải thiện ổn định của DLT trên dữ liệu động học1. | Khung thiết kế Temporal Data Design1. | data/, evaluation/ | E4 (Early Detection), E7 (Generalization)1. | DLT (phút/giờ) trước ![][image4]. |

## **19A. Final Baseline Eligibility Verification**

Trước khi tiến hành khóa sổ thiết kế phần mềm, cổng kiểm duyệt rào chắn xác minh (Final Baseline Eligibility Verification) đánh giá lại thông tin của phương pháp cơ sở LogOW để đảm bảo không vi phạm bất kỳ tiêu chuẩn chất lượng nào1.

* \[x\] Baseline được công bố trong giai đoạn 2023–2026 (LogOW công bố online 2024, bản in 2025\)1.  
* \[x\] Là journal article chính thức1.  
* \[x\] Đã trải qua peer-review.  
* \[x\] Journal là Q1 hoặc Q2 (*Journal of Systems and Software*, Q1)1.  
* \[x\] Có nguồn xác minh quartile (SCImago/JCR 2024\)1.  
* \[x\] Có DOI và metadata publication chính thức (10.1016/j.jss...)1.  
* \[x\] Đây chính là baseline đã được phê duyệt trong hồ sơ thiết kế kỹ thuật gốc1.  
* \[x\] Không tự ý thay baseline bằng paper khác.  
* \[x\] Định nghĩa Baseline, Hạn chế (Alert Fatigue/Context Deprivation), và Cải thiện (Conditional RAG-SLM Triage) được bảo toàn nguyên vẹn ngoài vòng Design Freeze1.

## **20\. Q1/Q2 Ranking và Publication Verification**

Bảo chứng học thuật cho phần mềm được xây dựng hoàn toàn dựa trên uy tín của nền tảng LogOW. Phân tích chi tiết các thông số xuất bản chứng minh rằng thuật toán cơ sở đủ tầm vóc để trở thành hệ quy chiếu cho kỹ thuật phần mềm tiên tiến:  
> **Journal:** Journal of Systems and Software | **Year:** 2024 | **Ranking Source:** SCImago/JCR 24 | **Quartile:** Q1 | **Official Publication Status:** Published | **DOI:** Được xác minh qua ấn bản gốc và mã nguồn trên Zenodo (DOI: 10.5281/zenodo.14214083) chứa 1.4GB dữ liệu chuẩn hóa1.  
Cổng xác minh này khẳng định toàn bộ quy trình thiết kế bám sát chuẩn mực khắt khe nhất của nghiên cứu học thuật quốc tế, mang lại bằng chứng vững chắc cho việc tiếp nhận một bản đồ quy hoạch phần mềm hệ thống hoàn chỉnh.

## **21\. Chốt Thiết kế Phần mềm**

Tài liệu Đặc tả Thiết kế Phần mềm (SDS) này chính thức chốt lại một Software Design duy nhất để bước vào giai đoạn cài đặt (Implementation):  
Kiến trúc phần mềm bám chặt vào baseline Q1/2024 là LogOW, một công bố đã được bình duyệt chính thức trên Journal of Systems and Software1. Thành phần cải thiện nhắm mục tiêu (Targeted Improvement) được triển khai thông qua cơ chế Conditional RAG-SLM Triage, thiết lập một luồng xử lý kép được điều hướng bởi ngưỡng phương sai dự đoán của mạng Bayes1. Hệ thống giữ nguyên hoàn toàn (Frozen/Inherited) thuật toán Drain Parser, ma trận biểu diễn ngữ nghĩa, trọng số mạng nơ-ron học bán giám sát, thông số Monte Carlo Dropout, và kỷ luật phân tách dữ liệu Chronological Split1.  
Ngược lại, hệ thống sửa đổi và thêm mới (Modified/New) cổng rẽ nhánh luồng dữ liệu, tích hợp ChromaDB cho chức năng Tìm kiếm lai (Hybrid Search) tích hợp hàm suy giảm thời gian (Time-decay), mô-đun sinh Prompt In-context, công cụ SLM chạy cục bộ, và thiết lập một khung đánh giá động học chuyên biệt để tính toán ![][image7]1. Hệ thống tổ chức các chế độ thực nghiệm baseline, improved, ablation, robustness, và efficiency qua MLflow nhằm cô lập biến số và đo lường nhân quả chuẩn xác nhất cho nghiên cứu1. Việc lưu trữ toàn vẹn các cấu hình YAML, logs, JSON output và biểu đồ sẽ đóng vai trò như các artifacts không thể chối cãi phục vụ tính tái lập (Reproducibility) của cộng đồng khoa học. Dựa trên đặc tả này, mã nguồn hệ thống sẽ được kiến tạo để chứng minh giá trị của tri thức ngoại vi trong việc bảo vệ hệ thống giám sát AIOps khỏi thảm họa cảnh báo giả.

#### **Works cited**

> 1. 

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAYCAYAAAAh8HdUAAAAiUlEQVR4XmNgGAXDHnAA8Vcg/o8D+yCUQgAjVGIREFcA8U4kdhkQ5yOUIgDIBiYk/g8kNk5gjcYH2UoSYGHArekPEAuhC4JAPxB/QBeEAlyGgSVAGpHBK6g4DGMAkKAOuiAQ9DFgGgYG8gw4TAKCvww4/IMP4DIMJ0AO0SvIEoTAFyC+jC44SAEAmbAiVVx88fwAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMsAAAAaCAYAAAAZmai5AAAFOUlEQVR4Xu2baahuUxjH/+ZcMmUKyZRkCCHCB3OUDEnmfDCEUmQo8YFSMkVEhnDNQzJ0iRKuOco1z8O9+WDKPM88f89a3uc8Z629333O8Q7d51f/zl7Ps9d+1157zWsdIAiCIAiCIAiCYHy4QPSt6O+kn0VfOdtb/909mU1FX6J3L/WL6FN7U+IUTLyvTcPAp6FJT6c4QY8vMDmfmjSWNCX+V9R9mR/Qfg/9ZxRsPt6SBdsg2FD0u2hpY9sSmpbLjY3MF53qbIHm1TYF21/Odqzoe2cbG/hCT3pjYlmo/2xnt5QKvafU25QykrQ96/9gnmiWs90LTctKzn6haD1nW9jZBzp6sGwOzb9LnX0Z0U3ONhYcDH2hnb3D0FYZ6HvBGw2nidZ1ti2g8S5xdsKCO2hqlbb03k95Q4CvvUG4D5p/Kzr7rtDKNXa8iXKBsNQKDTkB6tvLOwzHeINwPzTeCt4hbOUNA2Azb4Cm709vFI73hgDHeQPq5YZ5vYg3jgO1F7I03fMZ6r4mmp45CrDCMn0Xe0fQN7XGZmzhC831RsMe0Htqq2JTLfSM84c39snNDbpRNFt0veg60bWiDf6N1Y0HoWlc3jsqrOYNCzmc6DP/LvKOcSXPV3Zydst70HtW9Q5oV0pfbb6ypjcktoXG40R5VOnSCPC+10R7e0eFHaHDUMK53Euid3rugbJ1B3XhIXRrbDJLiOag/7wfGPxAbYmiv9aVngj11woJl2JL5IxczjtGiH57vgOhBb/LPIZDvDVM+HnRESY8SDjR7ldd6NLYeM6Hjgqmw1R/u0rbC+XJ/6LekcgbkiXYojzhjYm2322Dm6ldtIlG65vtoOnrp+d7WbSfN3ZkOnkxqvTb2JRgvLW9sSMznqd8YG1/5Ryon7v0NZoKPe2llS5CX623GgUegaaxbQiR35/iyQXL1aJbRM9g4lIzd7l9IbJ5uCd0yfVoY7N59bDoddEVolsxcT72vugO6AmMYbID9J2a5iscwnO5+U7RvtApQcaXqaWgJ0tuQG+4yhVWDl85PHxR9HGy22/inzNlzoQ+bHdnZyvJzK4NoTKrQ+O/4uzcnW1K6OFQ32xnHyWa0u8p3XeX6KR0zT2FH9N13lPylYOFPMPvcgB6iy6c3+QCwspBcnz+ZUGzNnKeuR4GeUSyjrNbbHrZeGyfrvMmeIZDdRt+Nv29R3Sy6KMUtvfMQy9fpsWV0JYqFwiKieWxFp4NY2vIIyc1Noa2oozDjTz7HPssu2u7MjTON9ChG/Vdus++5DBhnvAIBlswtv5s9X5K9nPNfZ5S+q2NO9VnmTA36GxP8ZzoMBMm/N3cYzwqOtL4NsLkoyJ3Q/P3MWjF7DrsnAkug/42843fl/nIY1BsdFmuLMwP20DY/GJF5wpmhic/2GtwBPS5aBXj+wS6WOQpfZNgyOwPHQpYWPDtx+K1bXw4mT/EhEsf1se33CY63dlYuY5ytlGG72QXNOw7snKtZcL0rW/CFp83mZo9GCJc4vSrYKwYH6ZrHsrMH45DBpLD7AVsmEOvTLblpXmSFxEYXjxdZ27HxHNZh5rrUYRzwjyBvwo6tDoohfP75sOr7FXsiQ676FKqFLugtyc43zqC4cKPxX0Bz+PQ4RWPgHD/hRPQzNuiBSbMyfq7Jkw4rGIcLqF+IHrD+H4z15YF0ArIwsUJ8SizGHQoyiHbLGhvck3yPSB6NV1nOLybC50LZXbD5AOaGeaR7/GDIcHFDRbIUssWBIGBlYTdvZ17BEFQIf6fJQiCIAiCIAhmnn8AE7qbgeaJjr8AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAWCAYAAAAmaHdCAAAAxklEQVR4Xu2SMQ6BQRCFn0Kh4TgqlQoJpcQVlBKF0gXcwAmcgYhCKPSOQEShkCiE2cz8az12tYr/S16z30tmMlkg5xdTyUXyCHIwV5AcyZ0lTfMfZKVvLKCuzCLETXSlHQsjNcDTh5baLAznbvzIuBvEJtWgbsyCydbtSFrQwzUsG3Ml347gSnvJgDI0F9vSM4OWKiyEItStWDCpSSOoq7NgXOnOj8YV8QGeKrQ0YWGktkRXssWrdJLMA7/E+3dfS3qBz/lrnpPzPWIrQV/aAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAXCAYAAACrggdNAAACGUlEQVR4Xu2XTyhlURzHf0asZuFfsdGzEhvJYjaS1TTJYkShJEpWCiusKAtZDJazYGFKWUv+JElYWMifJBuZmmQWw1Dyn/j+/M7N8XPfc715pvv0PvWp3+937rvnnnvOuQeiGDFivAXj8O4VRgX8oJUuNT2AHJeaL0khmSmbDyQPv67qzC9d8CMTME7VWkkG9VXVE2G/qvmSFl0AR+S+zJJgui5GC277KaqJJxnQim4IQlTMXDvJoEp1gwuzsBBe6oYQ8NJ2+Eb/aUWckPeO+LoMGNANIdB72Gtf/4TX/ZRM3q4LRQnc1cVIw59sL/vJGbjbC+DB8hKbg2UkBzbTBbdgrsmZZVhr5X/gjZX3wnwTb8BrkvuNwW3nIlAFD+A0LLDqDwySPGS9qruxBitUjc87e5AcJ5i4DvbBgcfmJ9e2udTsOA8ew2ZYTTJAZhiOmJjhfU7l8Izk7R4aeV9d0fNZsOE2fWjzDYesXP/+pfyjqul2nTNcmyJZxvbgwiJYB5kmziJ5WQ68LG+t/AvcsXLmB+w2MX9V96w2JlifEUEvM4dTK16FPfC7yedhDew0+QzJMl80ObMJi03M+60Jjpq8kWRGNPo5eO+FBa/pSV0EaSRnFm/aVPgXNpi2IpIPhfPQAfiTZMYc+OA/J/mjmWf8N/xs2pZgtolt+L4XcJ/kYxQW3MkCyfn0Lugg+XfEXmbvgk+64DfuAehliHlnyx+AAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAaCAYAAADMp76xAAABmklEQVR4Xu2WzytEURTHjx8hK9nYWSsbtv4ByUJZICEla8rChrUdW/EHoOzERlmSkoTdULKwUJL8SH5/T+fe5nTm1sybV28m3U99e+987513zzv3zJ0hikT+BzvQbwJVHE5iKODZ5DoCXua0klRYU0uS2JnxmVtrZM0uVGO8WZKEB4zfAC0bL3NmrAEeKbz1LVCbNauBUP9WLXUkyZ7YgWplniThfjtQAmtUgZ15pvIX7YOurZmQL5KTq2TS9O8xNGHNhCRam4+tYv3LRyCfIlskx96IGgstdgVtQk8u7oL2oGmSFzx3/j3lixV6TpB1ksmTxtfoh/H29ajYLqTjJXflxLqhHxfrOXzGr6g4yCD0RlK1Byfu4w8qTGCBpGIePd4L5VS8Db1DB9Ar1KnGuOL85bZ8U8L+LQYnOG5izxE0pmIuwpSKNfy5emtSYYFSsw+1u/tV6BAadrFf7MJdN6A5d8+MqvtQYvwC3r/UA2ngHxXeNm6fZuiT5OxlFkmqzH+cPDckLXEHNTqvCTr1EwwvlH/hSCQSKYM/3JRrd53NpBYAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAaCAYAAADSbo4CAAABV0lEQVR4Xu2UPUtDMRSGjwoi4iBddHIT/AEdHJ1cHAoiOgn+A91cHcSxo6CdijqIiyC6OCi4OuguDg4KfuBQ6OAH+r4kl54eAjaYdsoDD03ec9uce5NbkUymM07gT4Rdgz++GMjsolOBLBklcU9E0y9uwRuTkwcbpOIU9plsTVwjFZMPwqrJkrFqA/Au4S0YhWM27Cah89FzBsQ1cW0LvWZdXCNzthBgU9y107aQgobEbUvMtVHEno+YazuGr+df54Ov+hM8g3V4oWpD8A3uw0eVk1t4CF9MHqQmrpEVk2v0E/iAM348Iu21A7jlx8z5EhTjIPOwKe6/g3dDeU64iP3SHrxTc13/ggtqfgyP4A68V3kSuPCymYfGxXwSfkt7g0k4hxN+vA2v4JKf60bK8NWPL+Fsq5SmKe4z7/AZDsNPuOtr49I66Bs+K+DWcKv4ybOUyWT+zS+OiVpMaNcRhAAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIEAAAAaCAYAAACQAT/QAAADnklEQVR4Xu2ZWaiNURTH/8YSMoei60koQuJB8mBKZCwUogwpZXhBEkWkTI8ScknIm2RIQoZQZokHUTKUecg8rn/r25191t3n3O90b/ec6+xf/evba3/fd/aw9trr2weIRCKRSCQSyXBU9LcARbJpiqpjlE/D9bHSgg2bErDZCe8RsEWAA6KrxnYEOlbtjZ22BsZWdNpCI4FPQ2hjbxk7eWINkeDCCC0iErIVnWOo6plLoI0db+wMe1uNrdxpItpjjdDx+22NKFEnWGwNwjuEG9ta1NEay5ye1iD0g45faMEssoZSJVcoi6TDJdpcNPWSRtAOXLMVOYiRoSr1fhEth3ZgjK0IcFo0WPTdVuSBW41jM4o3WL1FA1KqRfJMWtinX9aYgnXQZzvbigJpbg2F8gnpJ4b3dRJV2Io82Bwk7W/VNiNF41KqQ/JMGgZB+7TJVqSkpuMxFuGvuoJIG8raIN19+RgtemSN9ZyT0HFpZStS0BI1H9OboonWWAju5Ku6fMA5Sshh6BwM+WdEE6AHTGSN6B6ys+krople+RWyw+hGUd/k+rboJ/R9PIi5724SpopeQyegv2cvBqExsewQ7RddEl3w7Ozvbq9MVoseQufEOdYN0Ufol0alaIaoF7Ln5FByb8HshL5gtrGHoMdNNjaeN/gDwGt+R5NZoi2ibZnqrHuXBWz+dR/Re2jHp0EdglRCB9TBPKVY+MfHuTgMPYchw0SfvTr2qYtXviOa65VXieYl1/wN5ioPkHtMUzNJ9AW6et8kYl7wA/lfyDp7yMQJ2OWV7fPVldmpXE4QKhPaTkC3Fd8Z6hJGrw/QsWNEorN+Ff2Bhngfvw/7oBPr8OvcVxqj20vRBq+OhMaC+UuN84FCCDWCtq7JdTeoczm4TfgnaKOgYc5nr2htcs2vjqdeHcn1m/WF6ajq5IwexC6AgabsM1903Bqh2wQXdZ1gw77DD21sEL13e1I+Bx0E7nHkFHTb8ffEu6KhyTXzhYWig0mZYZAr3mLbwdyhVOGEu0S4GTJtXypaCd3a+Jno8PvWGJl84Rn0K8Ti7md+YCNQrcM9OeSJ/MeMZwYMie1Eb0Vzkroh0MTQTXKF6DE0IjgYAhlG+ScVI8oL0Yik7qKoe3Ltw/d+Ez2HJp+lzlnRZdECqNNfT+xcWNxS/O2B9zBZ5lbNMXdYx3esh77f5mq1DiflPPR8IFKGrIAmHn7Yj5QhTFgikUgkEon8X/wDawz4y3li8m0AAAAASUVORK5CYII=>