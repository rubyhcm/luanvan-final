1. Làm sao để phân biệt sự cố bất thường đến từ Trí tuệ nhân tạo hay con người?
2. Các tiêu chí chọn dataset cho đề tài?
3. Tại sao chọn “Hệ thống mạng lớn”?

- Vì trong hệ thống mạng nhỏ, các công cụ giám sát truyền thống dựa trên static rules hoặc các phương pháp kiểm soát cơ bản vẫn hoạt động tốt => Người quản trị có thể tự viết rules, tự đọc log khi có sự cố
- Với hệ thống lớn như các hệ thống phân tán hiện nay, các hệ thống microservices thì các hành vi, log của hệ thống rất phức tạp => nếu dùng static rules sẽ sinh ra nhiều false positives => cần AI/LLM hiểu ngữ cảnh

4. Tại sao chọn LLM?

- Vì dữ liệu log lớn
- Các phương pháp truyền thống thường sử dụng Rule-based/Signature-based với điểm yếu là: chỉ bắt được những cuộc tấn công đã từng xảy ra và được ghi nhận; trong các hạ tầng hiện đại, phân tán ngày nay thì vòng đời của một dịch vụ rất ngắn, lưu lượng mạng và hành vi hệ thống thay đổi liên tục => việc dùng sức người để duy trì và cập nhật các bộ luật tĩnh là bất khả thi và dễ sinh ra vô số cảnh báo giả. Nhưng giải pháp sử dụng trí tuệ nhân tạo có khả năng tự động học hỏi từ dữ liệu lịch sử để tự động thiết lập một baseline về hành vi bình thường của hệ thống, từ đó thích ứng linh hoạt với sự thay đổi của hạ tầng mà không cần con người can thiệp cập nhật luật.
- Có khả năng phát hiện các mối đe dọa Zero-day: AI tập trung vào việc tìm ra sự sai lệch so với trạng thái hoạt động bình thường mà không cần biết là hành vi đó đã xảy ra hay chưa.
- LLM có khả năng hiểu ngữ nghĩa(mối liên kết giữa các log với nhau) còn các công cụ truyền thống sử dụng regex/key matching.

5. Mình chỉ quan tâm đến log bất thường do Trí tuệ nhân tạo gây ra?
   Do em thấy ở nội dung 1.

- **Nội dung 1:** Tìm hiểu các loại dữ liệu nhật kí và sự cố bất thường hệ thống liên quan đến trí tuệ nhân tạo và công cụ giám sát mã nguồn mở thu thập dữ liệu này.

6. Các bước chính trong pipeline xử lý log của đề tài?
   Log Collection -> Log Parsing -> Log Partitioning & Representation -> Detection -> Raise Alert
