# mocking-cdn
> This project simulates a **mini CDN** using Python, Flask, and Redis. The system has three main parts:  
> - **server.py** – runs the Flask server, serves files, fetches from other servers if missing, and caches locally.  
> - **client.py** – allows clients to request files from the server.  
> - **notification.py** – subscribes to Redis Pub/Sub and alerts when new files are added by the content provider.  
>  
> New files can be pushed into the system by the content provider, after which they are accessible to clients and automatically trigger real-time notifications.
