---
name: cover_letter
description: Viết cover letter khi apply job Data/Analytics Engineer, dựa trên JD (text dán trực tiếp, link, hoặc file PDF) đối chiếu với resume.md trong repo này. Dùng khi user đưa JD và muốn có thư xin việc giới thiệu bản thân + lý do interest với job/công ty đó.
---

# Cover letter writer — apply job Data/Analytics Engineer

## Input được chấp nhận

- JD dán thẳng dạng text trong tin nhắn.
- Link JD — dùng WebFetch để lấy nội dung. Nếu trang chỉ trả về listing preview (kiểu ITviec search page), thử fetch thẳng URL job detail (bỏ query string), rồi mới báo user paste text nếu vẫn không ra full JD.
- File PDF JD — dùng Read tool, Read đọc được PDF trực tiếp, không cần convert.

## Nguồn sự thật về ứng viên

- Luôn đọc `resume.md` trong repo này trước khi viết — đây là NGUỒN DUY NHẤT về kinh nghiệm/kỹ năng thật. Không bịa thêm kỹ năng/kinh nghiệm không có trong đó.
- Nếu JD đòi công nghệ mà resume.md không có (vd Spark, Databricks, MLOps) — KHÔNG giả vờ có kinh nghiệm đó. Framing bằng nền tảng gần nhất + sẵn sàng học nhanh, không liệt kê keyword giả cho khớp ATS.
- Nếu gap kỹ năng đáng kể (JD lệch hẳn khỏi profile, kiểu Senior DE/Databricks so với AE/DE hiện tại), nói thẳng gap đó với user trước khi viết, đừng tự lao vào viết như thể khớp hoàn toàn — để user quyết có vẫn muốn apply job đó không.

## Quy trình

1. Parse JD: rút tên công ty, tên role, seniority, 4-6 skill/tech bắt buộc quan trọng nhất, trách nhiệm chính, và điểm đặc biệt (domain, quy mô team, sản phẩm).
2. Đối chiếu với resume.md: chọn ra những điểm khớp THẬT — ưu tiên bullet có số liệu/impact cụ thể hơn liệt kê tech suông.
3. Đoạn "tại sao interest với công ty này" phải có lý do cụ thể, không sáo rỗng kiểu "I'm passionate about your innovative mission". Nếu không đủ thông tin để cá nhân hóa (không rõ sản phẩm/mission công ty), hỏi user 1 câu ngắn trước khi viết đoạn này, đừng tự bịa.
4. Ngôn ngữ: JD tiếng Anh → mặc định viết tiếng Anh trừ khi user yêu cầu khác; JD tiếng Việt → hỏi hoặc mặc định tiếng Việt. Không tự ý đổi ngôn ngữ giữa chừng.

## Cấu trúc thư (mặc định ~250-350 từ)

1. Mở đầu: chào + nêu rõ tên role + tên công ty đang apply. Không dùng câu mở chung chung kiểu "I am writing to apply for a position."
2. Đoạn 1: Kiêm là ai (title hiện tại + số năm kinh nghiệm) + 1 câu định vị mạnh nhất khớp với JD, rút từ resume.md.
3. Đoạn 2: 1-2 bằng chứng cụ thể ánh xạ trực tiếp vào 2-3 yêu cầu quan trọng nhất của JD — trích ý từ resume.md, không liệt kê lại toàn bộ CV.
4. Đoạn 3: lý do interest thật với công ty/role. Nếu có gap kỹ năng đáng kể, nhắc ngắn gọn và framing tích cực thay vì né tránh hoàn toàn.
5. Kết: câu hành động ngắn (sẵn sàng phỏng vấn/trao đổi thêm) + cảm ơn.

## Việc KHÔNG làm

- Không liệt kê lại toàn bộ resume dưới dạng bullet trong cover letter.
- Không nhồi nhét keyword JD (ATS keyword stuffing) — chỉ dùng keyword thật sự khớp với kinh nghiệm đã có.
- Không viết câu mở/kết sáo rỗng kiểu "I am a highly motivated professional" — luôn cụ thể, gắn với role/công ty đang apply.
- Không tự bịa số liệu nếu resume.md không có — nếu cần số để thuyết phục mà chưa có, hỏi user thay vì đoán.
