# **The Best Real-World Example of a Clean Architecture Project You'll Find**  

Looking for a real-world, production-ready Clean Architecture implementation? This project is packed with industry best practices and modern software engineering principles, providing a solid foundation for building **scalable, maintainable, and testable applications**.  

---

## **Key Architectural Concepts Applied**  
✅ **SOLID** – Strong design principles for maintainable code  
✅ **Domain-Driven Design** – Business logic at the core  
✅ **Composition** – Flexible, reusable components  
✅ **Clean Architecture** – Separation of concerns at its best  
✅ **Nano Services** – A lightweight approach to microservices  
✅ **Async & Event-Driven Architecture** – Scalability through decoupled components  
✅ **Advanced Python Typing** – Type safety for robust code  
✅ **Testability** – Designed for easy unit and integration testing  

---

## **Tech Stack & Frameworks**  
🚀 **AWS Power Tools** – Utility suite for AWS Lambda  
🚀 **Pydantic** – Data validation and parsing  
🚀 **Boto3** – AWS SDK for seamless AWS service integration  
🚀 **Lagom** – Lightweight and powerful Dependency Injection  

---

## **AWS Cloud Stack**  
🔹 **AWS Lambda** (Python 3.12 runtime)  
🔹 **SNS / SQS Fanout** for event-driven processing  
🔹 **API Gateway** (supports both sync and async calls)  
🔹 **DynamoDB** with LSI for optimized querying  
🔹 **CloudFormation** for infrastructure as code  

This project isn’t just about theory—it’s a hands-on, real-world implementation of Clean Architecture done right. 🚀  

---

# **Understanding Our App Before Diving into the Technical Details**  

### **Never Overpay for a Ride Again!**  

Picture this: You’ve just left a packed concert or a major sports event. The streets are buzzing with people, and everyone is trying to book a ride home. You open your ride-hailing app—only to see **surge pricing** in full effect. The demand is high, and so are the fares.  

You’re on a budget and don’t want to spend a fortune just to get home. Sure, you could check multiple apps to find the cheapest option, but that takes time—**time in which prices could keep climbing**. By the time you switch back to the first app, the fare may have already skyrocketed.  

That’s where **our ride aggregator** comes in. Instead of manually searching through different apps, our platform does the work for you. Simply **enter your pickup and destination**, and we’ll instantly compare prices across multiple ride services, showing you the **best deal in real time**.  

**No more guessing. No more app switching. Just the fastest, most affordable ride home.**  

### **Ready to ride smarter? Let’s build it.**  

---

# **Features Overview**  

Our project is an **MVP**, so we’re focusing on core features that deliver immediate value. The goal is to provide users with a **seamless** way to compare and book the most affordable ride in real time.  

## **1. Request a Ride Planning** 🚖  

This feature kickstarts the user's journey by allowing them to request a ride plan. To do so, the user must provide:  
- **Origin Address** – Where the ride begins  
- **Destination Address** – Where the ride ends  
- **Ride Time** – When the ride is needed  

Once submitted, this service generates a **domain event** called `ride_planning_requested`. The request is processed asynchronously, ensuring **scalability and responsiveness**.  

- **API Endpoint:** `HTTP POST /v1/ride-planning`  
- **Response:** Returns a `request_id`, which the user can use to track the ride status.  

---

## **2. Create Ride Planning** 🔄  

Once the `ride_planning_requested` event is triggered, a **backend service** asynchronously processes the request. This service integrates with **multiple ride providers** (e.g., Uber, 99 Taxi) to fetch **real-time pricing**.  

- It **collects and compares** fare options across different platforms.  
- Once processing is complete, the ride status updates to **"Waiting for User Approval"**, meaning **ride options are ready for selection**.  

---

## **3. Get Ride Planning Status** 📊  

Users can check the **status** of their ride request at any time. By providing the `request_id`, they can retrieve the **current state** of their ride planning process.  

- **API Endpoint:** `HTTP GET /v1/ride-planning/{id}`  
- **Response:** Returns the ride request object, including its **status** and **available ride quotes** (if ready).  

### **Possible Statuses:**  
- `REQUESTED` – The request has been created and is being processed.  
- `WAITING_FOR_APPROVAL` – Ride quotes are ready for user selection.  
- `APPROVED` – The user has selected a ride.  
- `EXPIRED` – The request expired before approval.  
- `REQUEST_FAILED` – The request could not be processed.  
- `WAITING_FOR_EXPIRATION` – The request is pending but will soon expire.  

Once the status reaches **"Waiting for Approval"**, users can proceed to **choose their preferred ride**.  

---

## **4. Accept Ride** ✅  

Once ride options are available, users can **confirm** their selection by choosing the best ride.  

- **API Endpoint:** `HTTP POST /v1/ride-planning/{id}/accept`  
- **Required Data:**  
  - **Service ID** – The ride service provider (e.g., Uber, 99 Taxi).  
  - **Ride Option ID** – The specific ride choice within the service.  

### **Ride Acceptance Window ⏳**  
After the ride planning process is completed, the user has **5 minutes** to accept a ride. If the user does not confirm within this timeframe, the request will **expire**, and they will need to start a new ride planning request.  

Once a ride is accepted, the system finalizes the booking, ensuring users get the **most affordable and convenient** option available.  

---

# **Solution Architecture Overview**  
![Solutions Architecture](/docs/solution-architecutre.png)  

## **Frontend-Exposed API Routes**  

Our architecture exposes **three key API routes** to the frontend:  

- **`POST /v1/ride-planning`** – Initiates a ride planning request.  
- **`GET /v1/ride-planning/{id}`** – Retrieves the status and details of a ride request.  
- **`POST /v1/ride-planning/{id}/accept`** – Confirms and books a selected ride option.  

Each of these routes is handled by an **AWS Lambda function**, which processes user requests **synchronously** and interacts with a **central DynamoDB database** to manage ride planning and status updates.  

---

## **Backend Services**  

Our backend is designed to handle **event-driven processing** efficiently:  

- A **central SNS (Simple Notification Service)** is used to **broadcast domain events**.  
- Each backend service can attach its own **SQS (Simple Queue Service)** to **filter SNS events** and queue them for processing by an **AWS Lambda**.  
- A **Dead Letter Queue (DLQ)** is implemented to capture **poison messages** or **failed events**, ensuring **reliable event handling and debugging**.  
- The **Create Ride Planning** feature is a backend service that listens for `ride_planning_requested` events, integrates with ride-hailing services to fetch pricing, and updates the ride status to **"Waiting for User Approval"** once options are available.  

This architecture ensures **scalability, resilience, and seamless integration** between services.  

---
# **Project Requirements**  

1. **AWS CLI** – Command-line tool for managing AWS services.  
   📖 [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)  

2. **AWS SAM CLI** – Tool for building, testing, and deploying serverless applications.  
   📖 [Install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)  

3. **AWS CloudFormation** – Infrastructure as code service for provisioning AWS resources.  
   📖 [AWS CloudFormation Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)  

4. **Python 3.12+** – Required runtime for AWS Lambda and application development.  
   📖 [Install Python](https://www.python.org/downloads/)  

# **How to Deploy**
This repository follows a **monorepo** structure, where each folder represents a backend service.  

Inside each service folder, there is a `build/` directory containing the build and deployment scripts.  
Within the `build/` folder, you'll find a `deploy.sh` script that can be executed from the project root.  

🚀 **CI/CD Automation:** CI/CD is not fully automated yet. If you can contribute, feel free to submit a pull request—I’d be happy to review it!  

> ./get_ride_planning_repo/build/deploy.sh