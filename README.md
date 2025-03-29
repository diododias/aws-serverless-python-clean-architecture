
# The Best Real-World Example of a Clean Architecture Project

This project provides a real-world, production-ready implementation of Clean Architecture, following industry best practices and modern software engineering principles. It offers a solid foundation for building scalable, maintainable, and testable applications.

---

## Key Architectural Concepts
- **SOLID Principles** – Ensures maintainable code.
- **Domain-Driven Design** – Business logic at the core.
- **Composition** – Flexible, reusable components.
- **Clean Architecture** – Effective separation of concerns.
- **Nano Services** – Lightweight approach to microservices.
- **Async & Event-Driven Architecture** – Enhanced scalability through decoupled components.
- **Advanced Python Typing** – Type safety for robust code.
- **Testability** – Designed for easy unit and integration testing.

---

## Tech Stack & Frameworks
- **AWS Power Tools** – Utilities for AWS Lambda.
- **Pydantic** – Data validation and parsing.
- **Boto3** – AWS SDK for service integration.
- **Lagom** – Dependency Injection framework.

---

## AWS Cloud Stack
- **AWS Lambda** (Python 3.12 runtime)
- **SNS / SQS Fanout** for event-driven processing
- **API Gateway** (sync and async calls)
- **DynamoDB** with LSI for optimized querying
- **CloudFormation** for infrastructure as code

This project demonstrates a practical implementation of Clean Architecture.

---

# Project Overview

### Problem Statement

High-demand events like concerts or sports games cause surge pricing in ride-hailing apps. Manually comparing fares across apps is time-consuming, with prices often rising while users search. This ride aggregator addresses the problem by providing a seamless way to compare prices in real-time and find the best deal.

### Solution

The platform allows users to enter their pickup and destination, then instantly compares prices across multiple ride services, presenting the most affordable option without the hassle of switching between apps.

---

# Features

## 1. Request Ride Planning

Users can request a ride plan by providing:
- **Origin Address** (pickup location)
- **Destination Address** (drop-off location)
- **Ride Time** (desired pickup time)

Upon submission, the service:
- Validates the request.
- Identifies the user through the received event, due to authentication at the gateway.
- Applies idempotency:
  1. Duplicate requests within 5 minutes return the same `ride_planning_id`.  
  2. If a duplicate request is made after 5 minutes, the previous request will be marked as `WAITING_FOR_EXPIRATION`, and the event `ride_planning_waiting_for_expiration` will be emitted. This event will later be processed by the `process_ride_planning_expiration` service.  
  3. A new `ride_planning_request` will be generated.
- Creates a DynamoDB entry with status `REQUESTED`.
- Emits a `ride_planning_requested` event, to be processed asynchronously via `process_ride_planning_request` service.
- Returns a `ride_planning_id`.

### API Endpoint
`HTTP POST /v1/ride-planning`

### Request Example
```json
{
  "address_from": {
    "street": "Rua Augusta, 321",
    "city": "Sao Paulo",
    "country": "Brazil",
    "postal_code": "03881100"
  },
  "address_to": {
    "street": "Avenida 25 de Marco, 322",
    "city": "Sao Paulo",
    "country": "Brazil",
    "postal_code": "03881100"
  },
  "departure_datetime": "2024-12-01T05:33:20.000Z"
}
```

### Response Example
```json
{
  "ride_planning_id": "475e81e79c7880f9b5caa35bec50279c459ad2f9"
}
```

---

## 2. Process Ride Planning Request

The `ride_planning_requested` event triggers backend processing to:
- Retrieve real-time pricing from multiple providers (e.g., Uber, 99 Taxi).
- Compare fare options.
- Update ride status to `WAITING_FOR_APPROVAL` when quotes are ready.

---

## 3. Get Ride Planning Status

Users can check the status of their ride planning request.

### Possible Statuses
- `REQUESTED`: Request created and being processed.
- `WAITING_FOR_APPROVAL`: Quotes are ready for user selection.
- `APPROVED`: User has selected a ride.
- `EXPIRED`: Request expired before approval.
- `REQUEST_FAILED`: Processing failed.
- `WAITING_FOR_EXPIRATION`: Pending expiration.

### API Endpoint
`HTTP GET /v1/ride-planning/{id}`


### Response Example
```json
{
  "id": "d39d5e8ed9c04096a65f679468600db1",
  "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
  "address_from": {
    "street": "Rua Augusta, 321",
    "city": "Sao Paulo",
    "country": "Brazil",
    "postal_code": "03881100"
  },
  "address_to": {
    "street": "Rua Augusta, 321",
    "city": "Sao Paulo",
    "country": "Brazil",
    "postal_code": "03881100"
  },
  "departure_datetime": "2024-12-01 05:33:20+00:00",
  "created_at": "2024-08-30 01:38:09+00:00",
  "modified_at": "2024-08-30 01:38:09+00:00",
  "status": "WAITING_FOR_APPROVAL",
  "ride_options": [
    {
      "id": "3e60414669aeacba0c72ed9535b4d4ea95042e00",
      "provider_id": "dcdddd0d3b843628f21d95e0ef015dfade972412",
      "provider": "UBER",
      "tier": "PREMIUM",
      "price": 29.99,
      "accepted": false
    },
    {
      "id": "66908dc7866e366f3210657b82c76695deadf007",
      "provider_id": "0022ae5daadd82915ffa6f6f880c9392f756eb27",
      "provider": "99 TAXI",
      "tier": "ECONOMY",
      "price": 15.50,
      "accepted": false
    }
  ]
}

```
---

## 4. Accept Ride

Users confirm their ride selection by providing:
- **Service ID** – Provider identifier (e.g., Uber, 99 Taxi).
- **Ride Option ID** – Specific ride choice.

### Acceptance Window
Rides must be accepted within 5 minutes after processing completion. If not, the request expires and the process must be restarted.

### API Endpoint
`HTTP POST /v1/ride-planning/{ridePlanningId}/accept/{rideOptionId}`

---

## 5. Process Ride Planning Expiration

All services validate ride planning existence and validity. If invalid, a `WAITING_FOR_EXPIRATION` event is issued and processed by this service to update the status to `EXPIRED`. Once expired, an `EXPIRED` event is emitted for other services to react accordingly.

---

# Events life Cicle
![Events Life Cicle](/docs/ride-planning-life-cicle.png)  

1. ride-planning-requested: Event emmitted when a ride planning is requested by user
2. ride-planning-request-failed: Event emitted when an error ocurr in ride-planning-requested event and cant be processed
3. ride-planning-waiting-for-approval: Event emitted when an ride-planning-requested event is processed and the ride-planning is ready to be accepted by user
4. ride-planning-waiting-for-expiration: Event can be emitted by other services to service process-ride-planning-expiration can expired the ride planning
5. ride-planning-aprove-failed: Event emitted when the ride planning fail and canot be aceppted by the user
6. ride-planning-aproved: Event emitted when the user acepted a ride planning
7. ride-planning-expired: Event emitted when the ride-planning is expired


# **Solution Architecture Overview**  
![Solutions Architecture](/docs/solution-architecture.png)  

## **Frontend-Exposed API Routes**  

Our architecture exposes **three key API routes** to the frontend:  

- **`POST /v1/ride-planning`** – Initiates a ride planning request.  
- **`GET /v1/ride-planning/{id}`** – Retrieves the status and details of a ride request.  
- **`POST /v1/ride-planning/{id}/accept/{rideOptionId}`** – Confirms and books a selected ride option.  

Each of these routes is handled by an **AWS Lambda function**, which processes user requests **synchronously** and interacts with a **central DynamoDB database** to manage ride planning and status updates.  

---

## **Backend Services**

The backend uses an event-driven architecture with:
- **SNS (Simple Notification Service)** for broadcasting domain events.
- **SQS (Simple Queue Service)** for filtering events and queueing them for processing by AWS Lambda functions.
- **Dead Letter Queues (DLQ)** for reliable error handling.
- **DynamoDB** for persistence.

Services:
- **Process Ride Planning Request**: Handles `ride_planning_requested` events, integrates with ride-hailing services, and updates the status to `WAITING_FOR_APPROVAL`.
- **Process Ride Planning Expiration**: Processes `ride_planning_waiting_for_expiration` events, marks ride_planning as `EXPIRED`, and emits a `ride_planning_expired` event.

---

# **How to Deploy**
This repository follows a **monorepo** structure, where each folder represents a backend service.  

Inside each service folder, there is a `build/` directory containing the build and deployment scripts.  
Within the `build/` folder, you'll find a `deploy.sh` script that can be executed from the project root.  

**CI/CD Automation:** CI/CD is not fully automated yet. If you can contribute, feel free to submit a pull request—I’d be happy to review it!  

> ./get_ride_planning_repo/build/deploy.sh

---
# Features under development

- Accept ride planning service
- Authentication via AWS Cognito
- Static Front-end hosted on S3 with CloudFront
- Unit Test Coverage to 85%
- Integration Test
- CI/CD with GitHub Actions

---
*This documentation was AI-assisted, but the project was fully developed hands-on by a highly skilled software engineer.*
