## 📌 mocking-cdn
> This project simulates a **mini CDN** using Python, Flask, and Redis. https://github.com/srumonke/mocking-cdn/tree/main/redis-cdn The system has three main parts:  
> - **server.py** – runs the Flask server, serves files, fetches from other servers if missing, and caches locally.  
> - **client.py** – allows clients to request files from the server.  
> - **notification.py** – subscribes to Redis Pub/Sub and alerts when new files are added by the content provider.  
>  
> New files can be pushed into the system by the content provider, after which they are accessible to clients and automatically trigger real-time notifications.



## 📌 mocking-cdn concurrent access, duplicate detection adn file versioning

This project extends the distributed file management system using **Python** and the **Flask framework**, with added support for **concurrent access, duplicate detection, and file versioning**.  
- https://github.com/srumonke/mocking-cdn/tree/main/Additonal_feature
- https://github.com/srumonke/mocking-cdn/tree/main/Node1
- https://github.com/srumonke/mocking-cdn/tree/main/Node2
- https://github.com/srumonke/mocking-cdn/tree/main/Node3

### 🔹 Core Functionality  
- Clients request files from the server (`/read` endpoint).  
- Content providers add or update files (`/write` endpoint).  
- Duplicate files are detected using **SHA-256 hashing** of file contents to avoid storing identical files.  

### 🔹 File Versioning  
- Each update creates a new version instead of overwriting.  
- Versions are timestamped and stored in a history list per file.  
- Clients can request specific versions (`/read_version`) or revert to older ones.  

### 🔹 Concurrency Control  
- A **file lock** is used to manage concurrent writes.  
- Ricart–Agrawala–style distributed mutual exclusion was considered for coordination.  

### 🔹 Test Cases  
1. Single user requesting existing file(s).  
2. User requesting non-existent file.  
3. Multiple concurrent requests.  
4. Content provider adding new files.  
5. Adding duplicate files (detected and blocked).  
6. Duplicate detection across nodes.  

---

✅ This assignment demonstrates **resilient file storage**, **consistency across concurrent users**, and **historical version tracking**, making the system closer to a **basic distributed file system with CDN-like behavior**.  
