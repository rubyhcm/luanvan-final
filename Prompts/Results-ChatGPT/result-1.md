# Sơ đồ tổng quan văn liệu

Chúng tôi tìm thấy rằng trong giai đoạn 2025–2026, các phương pháp phát hiện bất thường log ngày càng dựa trên **mô hình ngôn ngữ lớn (LLM)** và **retrieval-augmented generation (RAG)**. Một tổng quan hệ thống mới công bố năm 2025 nhận định rằng “kỹ thuật prompt engineering và RAG tăng cường độ chính xác và khả năng giải thích; các phương pháp dựa trên LLM vượt trội đáng kể so với phương pháp truyền thống về F1, precision, recall”. Ví dụ, Cabello et al. (2026) triển khai khung tự giám sát sử dụng LogBERT và đạt **độ chính xác cao** trong phân biệt log bình thường so với bất thường (xác định bất thường nếu >10% token bị dự đoán sai). Mặt khác, nhiều nghiên cứu mới (LogLLM, LogTinyLLM, LogLLaMA) tận dụng khả năng hiểu ngữ nghĩa của LLM để cải thiện phát hiện bất thường log.  

Các phương pháp truyền thống (ví dụ DeepLog, LogAnomaly dùng LSTM hay autoencoder) bị hạn chế trong việc nắm bắt ngữ nghĩa và luồng log, trong khi mô hình Transformer như LogBERT, NeuralLog đã cải thiện việc học ngữ cảnh. Xu hướng hiện nay tập trung vào kết hợp dữ liệu lịch sử, tri thức bổ trợ và suy luận nhiều bước. Ví dụ, khung **LogPipe** (ICSE 2026) dùng cơ sở tri thức động để hỗ trợ LLM, đạt F1 trung bình 97.5% và có khả năng giải thích kết quả. Các khung retrieval-augmented như **LogRAIL** (2026) hai giai đoạn sử dụng transformer và LLM để tái đánh giá cửa sổ log gần ngưỡng, cải thiện F1 so với chỉ dùng mạng đầu tiên. Các nghiên cứu entry-level như **EnrichLog** (2025) chứng minh rằng bổ sung thông tin ngữ cảnh (“corpus-specific” và “sample-specific” knowledge qua RAG) làm tăng đáng kể độ chính xác phát hiện. Tuy nhiên, hầu hết các công trình mới chỉ đo lường precision/recall cho nhãn bất thường sau khi xảy ra, chứ chưa có đánh giá riêng về “phát hiện sớm” (lead time). 

# Phân loại và xu hướng phương pháp

**Thuật toán truyền thống:** Các phương pháp cổ điển sử dụng học máy (One-Class SVM, KNN) hay mạng nơron tuần tự (LSTM trong DeepLog) và autoencoder (LogAnomaly). Chúng phân tích chuỗi log theo thứ tự thời gian nhưng thường thiếu ngữ nghĩa.  

**Deep learning và Transformer:** Phương pháp dựa trên mô hình học sâu (CNN, LSTM) và Transformer (LogBERT, NeuralLog) đã được phát triển từ 2017–2022. Ví dụ, LogBERT dùng kiến trúc BERT để nắm ngữ cảnh log; NeuralLog (2023) gán vector ngữ nghĩa cho log và huấn luyện phân lớp.  

**Mô hình nền tảng (Foundation Models):** Từ 2023 xuất hiện nhiều phương pháp tận dụng LLM (GPT, LLaMA, v.v.). Điển hình là LogLLM (2025) dùng BERT để trích xuất vector ngữ nghĩa và LLaMA để phân loại chuỗi log; LogLLaMA (2025) trực tiếp fine-tune LLaMA2 với học tăng cường để sinh và phát hiện log bất thường; LogTinyLLM (2025) sử dụng các LLM “nhỏ” (với LoRA/adapters) để cải thiện đáng kể so với LogBERT trên tập Thunderbird.  

**RAG và Kiến thức bổ sung:** Các phương pháp kết hợp truy hồi tri thức đang lên ngôi. Ví dụ, LogRAIL (2026) thêm một tầng LLM RAG để kiểm chứng lại các cửa sổ gần ngưỡng quyết định; EnrichLog (2025) gắn ngữ cảnh lịch sử và suy luận vào mỗi bản ghi log qua RAG mà không cần huấn luyện thêm, và báo cáo cải thiện hiệu năng trên nhiều benchmark. Mặt khác, LogPipe (ICSE 2026) xây dựng cơ sở tri thức động (mẫu log, từ điển mật độ,…) để hướng dẫn LLM phát hiện và giải thích.  

**Đại lý AI, bộ nhớ dài hạn, khác:** Chưa thấy công trình log anomaly cụ thể áp dụng agent hoặc hệ thống bộ nhớ chuyên biệt. Những ý tưởng như diễn giải đa bước (chain-of-thought) hay lưu trữ phiên đã được thử nghiệm trong các lĩnh vực khác nhưng ít được đề cập trực tiếp trong phát hiện bất thường log. Tuy nhiên, xu hướng tổng thể hướng đến tích hợp các thành phần này nếu có thể hỗ trợ lý giải và phát hiện sớm.

# Các phương pháp nổi bật (2025–2026)

- **LogLLM (Guan et al., 2025):** Khung sử dụng BERT để tạo vector ngữ nghĩa từ bản ghi log, sau đó dùng LLaMA (decoder) để phân loại chuỗi log. Họ giới thiệu một quy trình huấn luyện ba giai đoạn với kỹ thuật oversampling các lớp ít gặp. Kết quả thử nghiệm trên 4 tập dữ liệu (HDFS, BGL, Liberty, Thunderbird) cho thấy LogLLM đạt F1 cao nhất (trung bình ~0.959, riêng HDFS đạt 0.997) so với các phương pháp SOTA trước đó.  

- **LogTinyLLM (Ocansey et al., 2025):** Nghiên cứu này sử dụng các LLM kích thước nhỏ (nhỏ hơn BERT/transformer) và huấn luyện bằng kỹ thuật parameter-efficient (LoRA, adapter) trên tập Thunderbird. Kết quả cho thấy LoRA-tuned LLM có độ chính xác 97.8–98.8%, cao hơn ~18–19% so với fine-tuning đầy đủ của LogBERT (79.37%).  

- **LogLLaMA (Yang & Harris, 2025):** Khung tiếp cận sinh (generative): đầu tiên fine-tune LLaMA2 trên log bình thường để nó học sinh tạo log tiếp theo, sau đó dùng học tăng cường (reinforcement learning) để điều chỉnh mô hình phát hiện log bất thường. Mô hình LogLLaMA được báo cáo “thắng” các SOTA trước đó trên các tập BGL, Thunderbird, HDFS.  

- **LogRAIL (Choi et al., 2026):** Hệ hai tầng: tầng 1 là transformer (đã được LogFormer) phân loại cửa sổ cố định của log (theo template) và cho điểm; những cửa sổ gần ngưỡng quyết định sẽ được tầng 2 (LLM có truy hồi) tái đánh giá. Tầng 2 có chế độ ưu tiên precision hoặc recall. Kết quả trên log Android thật cho thấy LogRAIL tăng F1 so với tầng 1 đơn thuần và cho ra giải thích ngắn gọn cho từng quyết định. Mã nguồn của LogRAIL đã được công khai (GitHub).  

- **LogPipe (Cabello et al., 2026):** Phương pháp kết hợp kiến thức: xây dựng động cơ sở tri thức bao gồm mẫu log thường gặp, từ điển mật độ, v.v. Trong khi một mô hình LLM (LogBERT tự giám sát) phát hiện bất thường, cơ sở tri thức sẽ gợi ý thêm sự kiện và ngữ cảnh có liên quan, nâng cao độ chính xác và giải thích. Trên 8 bộ dữ liệu công khai, LogPipe đạt F1 trung bình 97.5% và giảm đáng kể khối lượng truy vấn LLM.  

- **EnrichLog (Peng et al., 2025):** Khung RAG entry-based không cần huấn luyện: mỗi bản ghi log được bổ sung thông tin (ví dụ ví dụ lịch sử tương đồng, suy luận) thông qua RAG, sau đó dùng LLM để đánh giá bất thường. EnrichLog được thử trên 4 dataset lớn và đều cho thấy cải thiện hiệu năng phát hiện và độ tin cậy so với baseline.  

- **LogBERT tự giám sát (Cabello et al., 2026):** Mặc dù được công bố dưới hình thức một ứng dụng AIOps, nhóm Cabello sử dụng LogBERT tự giám sát (chỉ học từ log bình thường, không cần nhãn bất thường) với cửa sổ thời gian trượt 15s để phát hiện anomalous logs. Họ báo cáo mô hình này phân biệt bình thường/bất thường với độ chính xác rất cao. Đây là một baseline khả thi vì không đòi hỏi dữ liệu có nhãn và hỗ trợ thời gian thực.  

# Danh sách ứng viên baseline tiềm năng

Dựa trên tiêu chí: *Mới nhất (2025–2026)*, *hiệu năng cao*, *phù hợp bài toán phát hiện sớm*, *kiến trúc rõ ràng*, *có mã nguồn*, *bằng chứng về hạn chế*, *tiềm năng cải thiện*, chúng tôi đề xuất các ứng viên chính:

- **LogLLM (Guan et al., 2025)**: Hiệu năng vượt trội (F1 SOTA) trên các dataset chuẩn; sử dụng BERT+Llama rõ ràng; nhưng cần nhãn bất thường cho huấn luyện.  
- **LogTinyLLM (Ocansey et al., 2025)**: Kiến trúc LoRA-tuned LLM đơn giản; cho kết quả accuracy gần 98% trên tập Thunderbird; tuy nhiên mới đánh giá một benchmark và chưa có mã nguồn công khai.  
- **LogLLaMA (Yang & Harris, 2025)**: Học tăng cường với LLaMA2; thể hiện hiệu quả SOTA; kiến trúc phức tạp (RL); chưa rõ khả năng tái triển khai.  
- **LogRAIL (Choi et al., 2026)**: Mô hình hai tầng có mã nguồn mở; cải thiện rõ rệt precision/recall trên log Android; điểm hạn chế là phụ thuộc template và hiện chỉ thử nghiệm trên log Android.  
- **LogPipe (Cabello et al., 2026)**: Cơ chế tri thức phong phú, F1 cao (97.5%); cho kết quả giải thích tốt; nhưng chưa rõ mã nguồn và khả năng áp dụng rộng ra ngoài miền quân sự.  
- **EnrichLog (Peng et al., 2025)**: Phương pháp RAG entry-based không cần huấn luyện; cải thiện anomaly detection trên nhiều tập chứng thực; tuy nhiên chưa rõ hiệu năng so với các baseline trainable hay trên dữ liệu khác.  
- **LogBERT tự giám sát (Cabello et al., 2026)**: Đơn giản, chỉ dùng dữ liệu bình thường; đã được đánh giá có độ chính xác cao trong thực nghiệm nội bộ; phù hợp cho phát hiện online; nhưng chưa được báo cáo rộng rãi và không đo lường trực tiếp các chỉ số “phát hiện sớm”.

Đánh giá sơ bộ cho thấy các phương pháp LLM/RAG như LogLLM, LogRAIL, LogPipe… dẫn đầu về hiệu năng và khả năng mở rộng, nhưng đồng thời để lộ các giới hạn như cần dữ liệu có nhãn hoặc kiến trúc phức tạp, tạo cơ hội cho các cải tiến nhắm đúng điểm nghẽn.

# Phân tích thành phần của phương pháp baseline

Xét các thành phần chung trong pipeline phát hiện bất thường từ log:

- **Tiền xử lý:** Phần lớn phương pháp (LogRAIL, LogLLM, LogPipe, EnrichLog, v.v.) dùng log parser (Drain hoặc regex) để ánh xạ câu log thành template hoặc token; LogLLM còn trình bày không cần parser phức tạp, dùng biểu thức chính quy đơn giản.  
- **Biểu diễn:** Nhiều phương pháp dựa trên biểu diễn embedding ngữ nghĩa: LogLLM dùng BERT để rút vector từ log; LogLLaMA và LogTinyLLM mã hóa log với LLM; LogRAIL bình thường hóa thành template ID trước khi dùng transformer. Các cách biểu diễn này tốt hơn template thô truyền thống vì nắm bắt ngữ nghĩa.  
- **Ngữ cảnh / chuỗi:** Một số phương pháp kết hợp ngữ cảnh tuần tự: LogLLM phân tích chuỗi log liên tiếp; LogLLaMA dựa trên khả năng sinh chuỗi; LogRAIL chia log thành các cửa sổ cố định theo ngữ cảnh; LogBERT tự giám sát (Cabello) dùng cửa sổ trượt 15s. Các cửa sổ nhỏ (15s) giúp giảm độ trễ nhưng có thể bỏ sót ngữ cảnh dài hơn.  
- **Retrieval / Kiến thức:** Các thành phần truy hồi tri thức chỉ xuất hiện ở một số phương pháp: LogRAIL và EnrichLog dùng RAG để lấy ví dụ log tương tự hoặc thông tin liên quan; LogPipe duy trì cơ sở tri thức chứa mẫu log và ngữ nghĩa để hỗ trợ LLM.  Các phương pháp khác (LogLLM, LogTinyLLM, LogLLaMA) chưa dùng bổ sung tri thức bên ngoài.  
- **Bộ nhớ dài hạn:** Hiện chưa thấy phương pháp nào triển khai bộ nhớ lâu dài như experience replay hay memory network cho log. Có thể xem LogPipe phần nào như “lưu trữ” cơ sở tri thức, nhưng chưa có mục tiêu ghi nhớ theo thời gian.  
- **Suy luận:** Các LLM nội tại đã thực hiện suy luận ngữ nghĩa đơn giản khi phân lớp log. Tuy nhiên, các kỹ thuật suy luận nâng cao như Chain-of-Thought chưa được áp dụng rõ ràng. EnrichLog có tích hợp các suy luận lấy từ corpora, nhưng chưa thấy công trình nào dùng nhiều bước suy luận phức tạp với LLM trong log detection.  
- **Đánh giá bất thường & ngưỡng:** LogLLM, LogTinyLLM, LogRAIL ở tầng 1 đều đầu ra score hoặc xác suất, sau đó so với ngưỡng. Ví dụ, Cabello (2026) đánh dấu bất thường khi sai >10% token. LogRAIL có ngưỡng trung tâm (threshold) mà tầng 2 chỉ xử lý các cửa sổ gần ngưỡng này. Các phương pháp tự giám sát khác (autoencoder, DeepLog) dùng sai số tái tạo làm căn cứ. Việc lựa chọn ngưỡng thường cài đặt thủ công hoặc tự động tối ưu trên tập xác thực.  
- **Cập nhật (feedback):** Hầu hết các phương pháp khảo sát tính học offline; chưa thấy thiết kế cập nhật/trực tuyến nào (online learning) cho log mới phát sinh. LogPipe gợi ý “cập nhật cơ sở tri thức” là cần thiết khi logs thay đổi, nhưng đây là quá trình thủ công (refresh VDB).

Từ phân tích trên, các baseline mạnh như LogLLM/LogRAIL đã thực hiện tốt ở khâu biểu diễn và suy luận căn bản, nhưng còn yếu ở việc tận dụng tri thức lịch sử/dữ liệu bên ngoài, quản lý ngưỡng linh hoạt, và đặc biệt là phần đánh giá “sớm” (hiện chỉ xét anomaly như nhãn sau). Nhiều cải thiện trong văn liệu tập trung vào khắc phục chính xác những điểm này.

# Bằng chứng về hạn chế

Dưới đây liệt kê các hạn chế đã được xác nhận bằng minh chứng (kết quả, thí nghiệm hoặc phân tích) trong baseline hoặc các tác phẩm liên quan:

- **Phụ thuộc dữ liệu có nhãn (LogLLM):** LogLLM tuy đạt F1 rất cao, nhưng như tác giả lưu ý, mô hình này được huấn luyện có sử dụng cả mẫu bất thường. Trên thực tế, các phương pháp “chỉ dùng log bình thường” (unsupervised) kém hiệu quả: ví dụ [49†L689-L697] chỉ ra các mô hình như DeepLog hay LogBERT tự giám sát có F1 trung bình rất thấp (<0.602). Điều này cho thấy LogLLM và các mô hình tương tự phụ thuộc mạnh vào nhãn dữ liệu, là hạn chế khi nhãn khó có sẵn.  
- **Thiếu đo lường thời gian phát hiện sớm:** Hầu hết các công bố chỉ báo cáo precision/recall trên nhãn anomaly, không có bất kỳ chỉ số “lead time” hay “time-to-detect”. Ví dụ, Cabello (2026) chỉ đưa ra accuracy/f1 trên log đã gán nhãn, và LogRAIL báo cáo F1 cải thiện đối với log Android. Khi không có phép đo thời gian phát hiện trước, không thể khẳng định các phương pháp này thực sự hỗ trợ cảnh báo sớm. Đây là một thiếu sót chung của cả lĩnh vực.  
- **Giới hạn của thiết kế hai tầng (LogRAIL):** Theo chính bài LogRAIL, phương pháp này phụ thuộc vào quy tắc tạo mẫu log (templating) cố định: nếu quy tắc này thay đổi, kết quả truy hồi và quyết định có thể sai lệch. Thêm nữa, LogRAIL mới được thử nghiệm trên log Android; áp dụng vào log server mạng hay hệ thống khác có thể không hiệu quả do cấu trúc khác biệt. Những luận điểm này giảm tính tổng quát của mô hình.  
- **Chi phí tính toán cao:** Các phương pháp dựa trên LLM (LogRAIL tầng 2, LogLLM, LogLLaMA) thường tốn tài nguyên (CPU/GPU, API calls). Mặc dù LogTinyLLM đề xuất mô hình nhỏ, nhưng không đề cập chi tiết chi phí so với LogBERT. Các tác giả báo cáo thời gian huấn luyện và đánh giá của nhiều phương pháp (bảng III của [49]) cho thấy LogBERT và NeuralLog tốn nhiều thời gian huấn luyện hơn phương pháp cổ điển, chưa kể chi phí chạy LLM. Các hệ thống sản xuất AIOps yêu cầu độ trễ thấp và tài nguyên giới hạn, đây là thách thức chưa được giải quyết triệt để.  
- **Tính khả biến trong dữ liệu:** Nhiều work nhấn mạnh rằng dữ liệu log trong thực tế liên tục thay đổi định dạng và mẫu do cập nhật phần mềm. Ví dụ, Cabello đề cập đến “Frequent shifts in operational conditions and log formats”. Các mô hình dự đoán sự cố có thể trở nên kém chính xác khi thay đổi lớn. Rõ ràng, khả năng **học liên tục** hoặc điều chỉnh online là điểm yếu, vì hầu hết phương pháp khảo sát vẫn giả thiết dữ liệu huấn luyện ổn định.  

Nhìn chung, các hạn chế trên đều có bằng chứng từ tài liệu (kết quả thí nghiệm, phân tích của tác giả) thay vì suy đoán. Hầu hết các bài chỉ ra điểm yếu của mình hoặc của baseline trước: ví dụ [49] nêu nhãn và dữ liệu sạch là yếu tố quyết định hiệu năng, [63] thảo luận chính xác hạn chế nội ngoại tại, [69] mô tả cân bằng dịch và ngữ cảnh. Các giới hạn này mở ra cơ hội cải tiến rõ ràng.

# Cơ hội cải tiến được chứng minh

Từ hạn chế có bằng chứng trên, chúng tôi xác định những hướng cải tiến khả thi sau:

- **Kết hợp RAG và kiến thức ngữ cảnh:** Giống như SLR 2025 gợi ý, việc thêm cơ chế truy hồi ngoại cảnh có thể tăng độ chính xác và khả năng giải thích. Ví dụ, Baseline LogLLM hoặc LogLLaMA chỉ xử lý log thuần túy; một hướng cải thiện là cung cấp thêm ngữ cảnh sample/corpus (như EnrichLog hoặc LogPipe đã làm) để củng cố quyết định. Minh chứng: EnrichLog đã cải thiện độ tin cậy và hiệu năng nhờ thêm tri thức. Như vậy, một cải tiến hợp lý là áp dụng RAG cho LogLLM/LogLLaMA, hoặc bổ sung KG (từ điển lỗi, ontology) như một bước tiền xử lý, nhằm giảm phụ thuộc nhãn và nâng cao độ nhạy với ngữ cảnh.  
- **Học không giám sát với dữ liệu bình thường:** Vì LogLLM và nhiều LLM cần nhãn, một hướng cải thiện khác là chuyển sang học không giám sát để phát hiện sớm. Ví dụ, có thể fine-tune LLM trên log bình thường và dùng dự đoán nghịch (như Cabello) hoặc dự đoán mẫu tiếp theo; sau đó xác định bất thường qua sai số mô hình. Bài Cabello 2026 đã thể hiện khả năng tự giám sát và đạt độ chính xác cao. Bằng chứng liên quan là những phương pháp tự học (DeepLog, LogBERT) mặc dù kém hơn, nhưng nếu kết hợp với các kỹ thuật như interval training hoặc phát hiện concept drift có thể cải thiện.  
- **Cải thiện tính phổ biến giữa miền:** Do LogRAIL hiện chỉ trên Android, có thể thêm “adapter” hoặc fine-tune cho log máy chủ (HDFS, BGL) để mở rộng. Hoặc cân nhắc kiến trúc chung (ví dụ architecture như LogRAIL) nhưng sử dụng điểm neo (anchor) cho các dịch vụ khác. Hiện chưa có công trình nào xác nhận LogRAIL trên các DKB khác, nên đây là gap. Tuy nhiên, do LogPipe thử nghiệm trên 8 bộ dữ liệu khác nhau, ta biết kiến thức tri thức có thể có tác động chung – đây là bằng chứng gián tiếp cho thấy hướng xây dựng baseline “đa miền”.  
- **Tối ưu chi phí tính toán:** LogTinyLLM cho thấy có thể đạt độ chính xác cao với mô hình nhỏ hơn. Hướng cải tiến là áp dụng mô hình nhẹ (LoRA/adapters) cho các baseline nặng (như LogLLM), đặc biệt khi áp dụng trên đám mây hay thiết bị giới hạn. Cần kiểm chứng: mô hình nhẹ phải giữ được hiệu năng gần tương đương nhưng tiết kiệm tài nguyên. Niềm tin của cải tiến: kết quả của Ocansey et al. và chỉ ra chi phí LogBERT rất lớn (training 429 phút, testing 43 phút ở [49]) chứng tỏ cải thiện này là quan trọng.  
- **Thêm bộ nhớ/cập nhật liên tục:** Có thể bổ sung thành phần “bộ nhớ” để ghi nhận log đã xử lý và hiệu chỉnh ngưỡng theo thời gian. Ví dụ, Thresholding tĩnh (như 10% nhầm lẫn token) có thể làm tăng sai báo nếu log thay đổi. Việc theo dõi hiệu suất thực (feedback) để điều chỉnh ngưỡng hoặc mô hình (online learning) là hướng khả thi. Mặc dù chưa có bằng chứng rõ ràng trong tài liệu, ý tưởng này hợp lý dựa trên nguyên tắc AIOps: hệ thống cần thích nghi khi điều kiện vận hành thay đổi.  

Trong mỗi trường hợp, chuỗi bằng chứng có thể được liên kết: **Baseline** → **Hạn chế quan sát được** → **Bằng chứng (cáo lỗi, ablation)** → **Công trình liên quan (nếu có)** → **Chiến lược cải tiến hợp lý**. Ví dụ, *LogLLM (2025)* → *Cần nhãn cho training* → *Bảng III [49†L689-L697]* → *EnrichLog (2025) cho thấy RAG có thể hoạt động không cần nhãn* → *Áp dụng RAG hoặc học tự giám sát*. Quan trọng là dựa trên chứng cứ, không chỉ “hot trend”: ví dụ, đề xuất thêm “graph” hay “agent” thì phải chứng minh nó khắc phục hạn chế hiện tại (như *thêm tri thức* hay *học đa tác vụ*), chứ không chỉ đề cập xuông.

# Phân tích benchmark

Các tập dữ liệu benchmark quen thuộc vẫn chiếm ưu thế: **HDFS**, **BGL**, **Thunderbird**, **OpenStack**, **Spirit** được sử dụng rộng rãi để đánh giá phát hiện bất thường log. Ví dụ, LogLLM báo cáo trên 4 dataset gồm HDFS, BGL, Thunderbird và Liberty. Các dataset này có quy mô rất lớn (triệu bản ghi) và thuộc hệ thống tính toán phân tán (HDFS, BGL, Thunderbird là log của supercomputer/HPC); tỷ lệ bất thường thường rất thấp (thường <1%), gây mất cân bằng dữ liệu. Ngoài ra, các tập này chủ yếu là log hệ thống đã gán nhãn sau khi chạy, ít phản ánh việc đo lường sớm (không có nhãn sự kiện trước đó). Các tài liệu gần đây chưa giới thiệu bộ dữ liệu hoàn toàn mới cho phát hiện sớm log. Một số nghiên cứu (như Cabello 2026) thu thập log thực tế hàng tháng cho môi trường cụ thể, nhưng chưa công bố rộng rãi. 

Tóm lại, các benchmark hiện hành thường **không mô phỏng hoàn hảo** việc phát hiện sớm: chúng không cung cấp mốc thời gian lỗi hay cảnh báo, nên chỉ đánh giá phát hiện sau thực tế. Đặc điểm khác cần quan tâm là *rò rỉ dữ liệu* – khi sử dụng log theo dòng thời gian, rất cần chia train/test theo thời gian để tránh thông tin tương lai rò rỉ. Cuối cùng, do log thật thường đa dịch vụ và biến thiên, vẫn cần xét đến *khả năng tổng quát hóa chéo* (cross-dataset) – một số công trình như Zhao et al. (2025) đã thử nghiệm học meta để phát hiện bất thường chéo hệ thống (few-label to zero-label).

# Đánh giá sớm (Early Detection)

Từ literature, nhiều phương pháp chỉ xếp hạng log là bất thường hay không, mà không đo lường khoảng thời gian “phát hiện trước lỗi”. Có thể phân biệt các nhiệm vụ:

- **Detection (phát hiện)**: Xác định các bản ghi log đã xảy ra lỗi. Ví dụ đa số phương pháp xét log nhãn sẵn.  
- **Classification (phân loại)**: Phân loại loại bất thường (root cause), thường cần dữ liệu có nhãn cụ thể.  
- **Diagnosis (chẩn đoán)**: Xác định nguyên nhân dựa trên log; thường liên quan đến “root cause analysis” (vd. OpenRCA, ICLR 2025).  
- **Failure Prediction / Early Warning**: Dự báo lỗi trước khi nó xảy ra, thường cần dữ liệu nhãn “thời điểm lỗi” để đo lead time.  
- **Early Anomaly Detection:** Phát hiện anomalous behavior càng sớm càng tốt, đo bằng các chỉ số như *Detection Lead Time* (khoảng thời gian tính từ khi bắt đầu bất thường đến khi phát hiện), *Time-to-Detect*. 

Đáng chú ý, hầu như không có paper mới nào trên log đo các chỉ số trên. Ví dụ, Cabello (2026) chỉ nêu accuracy cho phân loại log mà không báo lead time. Do vậy, các phương pháp đó thực chất là “Phát hiện bất thường log” thông thường, chứ không phải “Early Alert”. Nếu một công trình chỉ báo F1, precision, recall thì không thể được gán nhãn sớm. Một số nghiên cứu AIOps khác (không trong log) nhắc đến metric *lead time*, nhưng đối với log thì rất ít. Do vậy, một phần nghiên cứu trong dự án này là cân nhắc cách tích hợp các metric phát hiện sớm phù hợp (ví dụ sử dụng timestamp log so sánh với nhãn lỗi, hoặc đo **Time-to-Detect** trung bình) nếu dữ liệu cho phép.  

Tóm lại, các hướng sớm hiện vẫn thiếu chuẩn mực đo đạc; điều này phản ánh một khoảng trống (“research gap”) trong lĩnh vực: cần phát triển benchmark và tiêu chí đánh giá riêng cho phát hiện sớm trong log analysis.

# Định vị nghiên cứu

Mục tiêu chính của dự án luận văn là **cải tiến có mục tiêu** trên một phương pháp sẵn có (Level 2), chứ không phải đề xuất hẳn một kiến trúc mới. Điều này phù hợp với trend rằng nhiều công trình mới (2025–26) thực chất là **extension** các mô hình LLM/RAG hiện có (ví dụ LogRAIL mở rộng transformer với LLM, LogPipe mở rộng LogBERT với knowledge base). Chúng tôi sẽ tập trung vào cải tiến trên nền của một baseline mạnh, xác định bottleneck và sử dụng lý thuyết hỗ trợ. Cụ thể, nếu baseline là mô hình LLM phân loại, hướng cải tiến có thể là thêm retrieval hoặc memory, dựa trên bằng chứng của các công trình tương tự. 

# Đề xuất baseline và hướng cải tiến

## Baseline ưu tiên

Trong các ứng viên trên, phương pháp **LogLLM (2025)** nổi bật về hiệu năng SOTA và tính rõ ràng kiến trúc. Guan et al. báo cáo LogLLM đạt F1 lên đến 0.997 trên tập HDFS và vượt xa các phương pháp trước đó. Đồng thời, phương pháp này dùng hai thành phần (BERT + LLM) có thể triển khai lại dễ dàng. Mặc dù LogRAIL và LogPipe đều có mã nguồn (LogRAIL) hoặc F1 cao (LogPipe), nhưng LogLLM là một baseline thuần anomaly detection với dữ liệu chuẩn (không phụ thuộc domain Android) và được đánh giá trên các tập phổ biến. Việc LogLLM cần dữ liệu nhãn (như đã phân tích) không làm giảm giá trị nó như baseline, bởi cải tiến có thể hướng tới giảm yêu cầu đó. Vì thế, chúng tôi khuyến nghị chọn **LogLLM (Guan et al., 2025)** làm baseline chính. 

*Lý do chọn:*  
- **Hiệu năng cao:** F1 trung bình ~0.959 (cao hơn ~6.6% so với NeuralLog).  
- **Kiến trúc rõ ràng:** Kết hợp BERT và LLaMA có thể ghi đè hoặc thay model dễ dàng.  
- **Khả năng tái triển khai:** Mô hình sử dụng các thành phần phổ biến (BERT, Llama); dù hiện chỉ là arXiv, chúng có thể cài đặt được.  
- **Phù hợp vấn đề:** Là phân lớp bất thường trên log sequence, đúng ngữ cảnh.  
- **Tiềm năng cải tiến:** Rõ ràng là cần nhãn để huấn luyện (xem dưới), và chưa dùng tri thức bên ngoài; nên có nhiều cửa để cải thiện.  

## Hạn chế chính đã xác nhận

Với LogLLM, bằng chứng từ [49] chỉ ra hạn chế **phụ thuộc dữ liệu nhãn**. Cụ thể, tác giả nhấn mạnh rằng nhóm phương pháp *có sử dụng mẫu bất thường* (log anomalies) mới đạt F1 cao; trái lại các phương pháp chỉ dùng log bình thường cho việc học cho kết quả rất kém. Điều này đồng nghĩa LogLLM không hoạt động “label-free”. Ngoài ra, theo quan sát chung, LogLLM cũng chưa tích hợp bất kỳ kỹ thuật retrieval hay memory nào, và không đo lường bất kỳ chỉ số phát hiện sớm nào. Những hạn chế này được minh chứng bằng kết quả trong tài liệu và thực nghiệm đã công bố. 

## Cơ hội cải tiến

**Hướng cải tiến được đề xuất:** Tích hợp cơ chế **Retrieval-Augmented Generation (RAG)** và kiến thức ngữ cảnh vào LogLLM. Cụ thể, cho mỗi chuỗi log đầu vào, ngoài việc đưa vào mô hình LogLLM hiện tại, chúng ta có thể truy vấn một cơ sở tri thức (ví dụ corpora log hoặc kho kiến thức chuyên ngành) để lấy các log/ví dụ tương tự và bổ sung vào đầu vào LLM. Việc này có thể giúp giảm sự phụ thuộc vào nhãn huấn luyện, vì các tham chiếu tương tự cung cấp bằng chứng cho quyết định. Đây là ý tưởng dựa trên kết quả của EnrichLog: họ bổ sung cả *corpus-specific* và *sample-specific* knowledge thông qua RAG, và nhận thấy “model confidence và detection accuracy” đều tăng lên đáng kể. Ngoài ra, SLR của De la Cruz Cabello et al. cũng ghi nhận RAG nâng cao độ chính xác và khả năng giải thích cho phát hiện bất thường log. 

Với LogLLM, cụ thể, chúng có thể triển khai như sau: sử dụng một kho truy hồi (vector DB) các log mẫu đã được ghi nhãn (hoặc log bình thường) làm knowledge base. Khi có chuỗi log mới, ta truy hồi các bản ghi tương tự, gộp cùng prompt để Llama xử lý. Hoặc xây dựng một chế độ prompting thân thiện hơn (few-shot/CoT) tận dụng ví dụ từ kho. Hy vọng kết quả: khả năng tổng quát của mô hình tăng lên (tốt cả precision và recall), đồng thời giảm sự phụ thuộc vào nhãn vì LLM có thêm thông tin ngữ cảnh. Một số nghiên cứu tiền nghiệm (EnrichLog, LogPipe) chứng minh lợi ích của cách làm này. Rủi ro: overhead thêm truy hồi và phải quản lý kho tri thức, nhưng lợi ích là rõ ràng dựa trên các dẫn chứng đã có. 

## Vị trí đóng góp và khả năng thực nghiệm

Hướng cải thiện này phù hợp với mức “Mở rộng có mục tiêu” (Level 2): chúng tôi giữ nguyên cốt lõi LogLLM, thêm một thành phần retrieval mà các công trình khác đã đề xuất. Đây không phải là một kiến trúc hoàn toàn mới, mà là nâng cấp dựa trên bằng chứng. Về mặt thực nghiệm, có thể tái hiện LogLLM (hoặc dùng mô hình tương đương) và triển khai thêm module RAG, sau đó so sánh kết quả. Các metric đánh giá sẽ bao gồm Precision/Recall/F1 như chuẩn mực, và nếu dữ liệu cho phép, sẽ thử xác định **Detection Lead Time** bằng cách đánh dấu thời điểm phát hiện so với nhãn (nếu có) để kiểm chứng mục tiêu sớm (ví dụ so sánh thời điểm log đầu tiên bị mark anomaly với lúc báo động). Tính khả thi: LogLLM đã có thông số (có thể cài Llama + BERT), RAG có thể dùng giải pháp mã nguồn mở (pinecone, FAISS) để thử nghiệm, và các so sánh với baseline là khả thi trong khuôn khổ luận văn (có thể dùng một trong các tập công khai để đánh giá).

# Kết quả chính và gợi ý

- **Xu hướng nổi bật:** Năm 2025–2026, phương pháp phát hiện bất thường log lệ thuộc nhiều vào **LLM và RAG**. Các mô hình như LogLLM, LogLLaMA, LogTinyLLM cho thấy LLM có thể bắt kịp ngữ nghĩa log, còn LogRAIL, EnrichLog, LogPipe chứng minh RAG/KB cải thiện hiệu năng. Thông tin từ SLR cho thấy rõ ràng LLM vượt trội về độ chính xác so với mô hình DL truyền thống.  
- **Khoảng trống (gap):** Một lỗ hổng đáng chú ý là hầu hết nghiên cứu chưa tập trung đo lường “phát hiện sớm” thực sự (lead time). Ngoài ra, hầu hết các baseline đều yêu cầu nhãn anomaly hoặc thiếu sử dụng tri thức ngoại sinh, tạo ra nhu cầu bổ sung RAG/knowledge. Ví dụ, nhu cầu dữ liệu nhãn của LogLLM được chứng minh là hạn chế, trong khi EnrichLog và LogPipe cung cấp bằng chứng cho khả năng khắc phục bằng RAG.  
- **Baseline được đề xuất:** *LogLLM (2025)* được chọn làm baseline vì độ mạnh đã kiểm chứng (F1 SOTA), tính rõ ràng và cập nhật (chỉ mới 2025). Phương pháp này hiện vẫn có hạn chế rõ ràng (dựa vào nhãn, chưa dùng RAG).  
- **Hướng cải tiến:** Tích hợp thành phần RAG/kiến thức vào LogLLM, dựa trên bằng chứng từ EnrichLog (2025) và LSR AIOps (2025) về lợi ích của RAG. Cải thiện mong đợi là tăng độ nhạy, độ chính xác và khả năng giải thích mà không cần nhiều nhãn.  
- **Đóng góp kỳ vọng:** Công trình sẽ ở mức **mở rộng có mục tiêu** (improvement/extension của LogLLM 2025), không phải phát kiến phương pháp hoàn toàn mới. Chúng tôi sẽ chứng minh thông qua thí nghiệm (so sánh baseline vs baseline+RAG) rằng hướng cải tiến có cơ sở khoa học và thực tiễn.  
- **Khả thi thí nghiệm:** Đề xuất về cơ bản khả thi trong khuôn khổ luận văn: LogLLM và các dataset công khai có sẵn; RAG có thể thử trên tập train/test hiện có hoặc xây dựng kho tri thức từ logs. So sánh tính năng (F1, độ trễ) giữa các cấu hình sẽ đánh giá hiệu quả. Ngoài ra, có thể phân tích ablation (ví dụ tắt RAG, thay đổi kích thước ngữ cảnh) để hiểu rõ đóng góp từng thành phần.

# Các kết luận quan trọng

1. **LLM và RAG là xu hướng chủ đạo:** Đa số công trình mới đều sử dụng mô hình ngôn ngữ lớn, thêm thành phần truy hồi tri thức hoặc cơ sở tri thức. Điều này giúp nắm bắt ngữ nghĩa log và cải thiện chất lượng phát hiện.  
2. **Hiệu năng baseline rất cao nhưng có giới hạn:** Các baseline như LogLLM (2025) ghi nhận F1 gần tuyệt đối trên các dataset chuẩn, tuy nhiên chúng thường phải sử dụng dữ liệu bất thường có nhãn. Trong khi đó, phương pháp như LogBERT tự giám sát (2026) có thể phát hiện với độ chính xác cao mà không cần nhãn. Mỗi cách tiếp cận có ưu/nội hạn riêng, tạo cơ hội cho cải tiến kết hợp hai hướng.  
3. **Cần metric “sớm”:** Thực nghiệm hiện nay chưa đo thời gian lead time. Mục tiêu của “phát hiện sớm” đòi hỏi tái cấu trúc đánh giá: cần xác định thời điểm phát hiện so với mốc lỗi. Bước đầu có thể là bổ sung những đo lường này trong thiết kế thí nghiệm tương lai.  
4. **Cơ hội cải tiến dựa trên bằng chứng:** Hướng tích hợp RAG vào mô hình hiện có có bằng chứng hỗ trợ. LogRAIL hay EnrichLog đã minh chứng ý tưởng tái kiểm tra với ngữ cảnh; LogPipe và EnrichLog chỉ ra tính hiệu quả của kiến thức bổ sung. Dựa trên chúng, đề xuất cải tiến LogLLM bằng RAG được hậu thuẫn vững chắc.  
5. **Xu hướng nghiên cứu:** Các công bố SOTA chủ yếu là “extension” (mở rộng) các mô hình đã có, thay vì kiến trúc hoàn toàn mới. Điều này phản ánh một quan điểm chung: tập trung cải thiện hẹp hơn trên một baseline mạnh, thay vì tạo “phương pháp mới tinh”.  

## Works Cited

- De la Cruz Cabello et al., “Log anomaly detection in AIOps: A real-world implementation using Large Language Models” (Systems and Soft Computing, 2026).  
- De la Cruz Cabello, “AIOps for log anomaly detection in the era of LLMs: A systematic literature review” (Intelligent Systems with Applications, 2025).  
- Choi et al., “LogRAIL: A Retrieval-Augmented LLM Reverification Layer for Log Anomaly Detection” (IEEE Access, 2026).  
- Guan et al., “LogLLM: Log-based Anomaly Detection Using Large Language Models” (ArXiv 2025).  
- Ocansey et al., “LogTinyLLM: Tiny Large Language Models Based Contextual Log Anomaly Detection” (ArXiv 2025).  
- Yang & Harris, “LogLLaMA: Transformer-based log anomaly detection with LLaMA” (ArXiv 2025).  
- Peng et al., “Log Anomaly Detection with Large Language Models via Knowledge-Enriched Fusion” (preprint 2025).  
- Xu et al., “EnrichLog: Entry-Based Anomaly Detection Framework with Retrieval-Augmented Generation” (Dec 2025).  
- Cabello et al., “Log anomaly detection in AIOps” (final pub. 2026).  
- Li et al., “LogPipe: An LLM-augmented Log Anomaly Detection Framework with Dynamic Knowledge Base” (ICSE 2026).