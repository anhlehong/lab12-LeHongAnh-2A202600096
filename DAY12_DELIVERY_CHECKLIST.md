#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Lê Hồng Anh  
> **Student ID:** 2A202600096  
> **Date:** 17/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. API key hardcode trong code
2. Không có config management
3. Print thay vì proper logging
4. Không có health check endpoint
5. Port cố định — không đọc từ environment

### Exercise 1.3: Comparison table
| Feature | Basic (`app.py`) | Advanced (`production_app.py`) | Tại sao quan trọng? |
| :--- | :--- | :--- | :--- |
| **Config** | **Hardcoded**: Ghi trực tiếp API Key, DB URL vào mã nguồn. | **Environment Variables**: Đọc từ môi trường thông qua module `settings`. | **Bảo mật & Linh hoạt**: Tránh lộ secret key khi push code lên GitHub. Dễ dàng thay đổi thông số giữa các môi trường (Dev, Staging, Prod) mà không cần sửa code. |
| **Health check** | **Không có**: Chỉ có endpoint logic chính. | **Đầy đủ**: Có `/health` (liveness), `/ready` (readiness) và `/metrics`. | **Khả năng tự phục hồi**: Giúp các nền tảng (Railway, Docker, K8s) biết khi nào Agent bị "treo" để tự động khởi động lại, hoặc khi nào Agent đã sẵn sàng để bắt đầu nhận traffic. |
| **Logging** | **print()**: Dạng text đơn giản, log cả thông tin nhạy cảm (API Key). | **Structured JSON Logging**: Format chuẩn, không log secrets, có timestamp/level. | **Khả năng quan sát (Observability)**: JSON giúp các công cụ quản lý log (Datadog, ELK) dễ dàng phân tích và cảnh báo khi có lỗi. Việc không log secret giúp tuân thủ các chuẩn bảo mật dữ liệu. |
| **Shutdown** | **Đột ngột**: Tắt là chết ngay, không quan tâm request đang xử lý. | **Graceful Shutdown**: Xử lý `SIGTERM`, dùng `lifespan` để dọn dẹp tài nguyên. | **Tính toàn vẹn dữ liệu**: Đảm bảo các request đang chạy được hoàn tất và các kết nối Database được đóng sạch sẽ, tránh tình trạng dữ liệu bị nửa chừng hoặc treo kết nối. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions

1.  **Base image:** `python:3.11`
2.  **Working directory:** `/app`
3.  **Tại sao COPY requirements.txt trước:** Để tận dụng **Docker layer cache**. Khi bạn thay đổi code ở bước sau, Docker sẽ không phải chạy lại lệnh cài đặt thư viện (`pip install`), giúp tiết kiệm đáng kể thời gian build.
    
4.  **CMD vs ENTRYPOINT:**
    * **ENTRYPOINT:** Định nghĩa lệnh chính sẽ chạy khi container khởi động (thường không đổi).
    * **CMD:** Cung cấp các tham số mặc định cho lệnh đó. Tham số trong `CMD` có thể bị ghi đè dễ dàng bằng cách truyền thêm argument khi chạy lệnh `docker run`.
...

### Exercise 2.3: Image size comparison
- Develop:  1.66GB
- Production: 236MB
- Difference: 86.12%

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://deploy-railway-production-1cb0.up.railway.app/
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
4.1/ python 04-api-gateway/develop/app.py

**1. Trường hợp chưa có API Key:**

* **Server log:**
    ```text
    API Key: demo-key-change-in-production
    INFO: 127.0.0.1:47308 - "POST /ask HTTP/1.1" 401 Unauthorized
    ```
* **Client (curl):**
    ```json
    {"detail":"Missing API key. Include header: X-API-Key: <your-key>"}
    ```

---

**2. Trường hợp có API Key (`secret-key-123`):**

* **Server log:**
    ```text
    API Key: secret-key-123
    INFO: 127.0.0.1:46004 - "POST /ask HTTP/1.1" 200 OK
    ```
* **Client (curl):**
    ```json
    {
      "question": "Hello",
      "answer": "Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."
    }
    ```

### Exercise 4.4: Cost guard implementation
[Explain your approach]

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
```

---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:


```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
