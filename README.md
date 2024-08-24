# Python AWS Lambda example of Clean Architecture implementation

Some Conceptual techniques applied to this project:
- SOLID
- Domain Driven Design
- Composition
- Dependency Inversion Principle
- Clean Architecture
- Nano Services
- Async Architecture / Event Driven Architecture
- Advanced Python Typing
- Testable applications

Frameworks
- AWS Power Tools: Utilities for AWS Lambda`s
- Pydantic: Data Validation
- Boto3: AWS SDK to iterate with AWS Services
- Lagom: Dependency Injection

AWS Stack:
- Lambda, Python 3.12 runtime
- SNS / SQS Fanout
- API Gateway, sync and async calls
- DynamoDB, with LSI Index
- Cloudformation IaaS

## Big Feature: Ride Planning

explicar o caso de uso




### User Services

#### Request Ride Planning
#### Get Ride Planning
#### Accept Ride Planning

### Backend Services
#### Create Ride Planning



status:
- em processamento
- requisitada
- aceita
- falha
- 

Quando endereco de partida, endereco de chegada e horario de saida são iguais não deve-se permitir criar uma nova solicitacão quando as condicoes existirem: 
 1. status: em processamento
 2. status: requisitada
 3. criado em menos de 5 minutos 

