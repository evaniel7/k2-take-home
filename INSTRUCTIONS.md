# Decision Queue

### The problem

A small software studio receives product requests from several partners. Requests arrive faster than the team can act on them. The team needs one place to review requests and record decisions.

Build a small web application called **Decision Queue**.

### Time limit

Spend no more than six focused hours on this exercise. The time includes setup, implementation, tests, and documentation.

Stop when you reach the limit. An incomplete submission is acceptable. Document what you completed, what you left out, and what you would do next.

Your delivery email contains the release time and submission deadline.

### Functional requirements

A user can:

1. Create a request with a title, problem statement, expected impact, and urgency.
2. View all requests in a useful queue.
3. Filter or sort the queue by status and urgency.
4. Open one request and record a decision: accept, defer, or decline.
5. Add a short reason for the decision.
6. See the current state of the queue.

### Non-functional requirements

The application must:

- run locally with Docker Compose
- not be hosted or deployed
- include application and PostgreSQL containers
- persist data in the PostgreSQL database
- include migrations or another repeatable schema setup
- document commands to initialize from a clean checkout, run the application, run tests, and reset local data
- validate required input and show useful errors
- include meaningful automated tests for the core workflow
- use fictional sample data only

Authentication, analytics, and AI features are not required. Beyond Docker Compose and PostgreSQL, choose the frameworks and architecture that fit your approach.

### Tools

Docker Compose and PostgreSQL are the only required technology choices. You can choose the other languages, frameworks, and architecture.

You can use internet search, documentation, code completion, AI tools, and normal developer tools. You remain responsible for the submission and must understand the work that you submit.

Do not:

- copy another candidate's repository
- ask another person to design or implement the solution
- use private K2 code, partner data, credentials, or proprietary code from another source
- include real customer or candidate data

### Repository contents

Create a personal GitHub repository for your project. Keep it private during the work window.

Commit and push the complete project before the common deadline. Include these files in the repository:

#### `README.md`

Include:

- commands to initialize from a clean checkout, run the application, run tests, and reset local data
- completed requirements
- known gaps
- two or three important product or technical decisions
- total time spent

#### `AI_USE.md`

Include:

- the AI tools that you used
- the tasks that each tool assisted
- any intermediate artifacts generated through AI use
- important AI output that you checked or changed

Do not include full prompt transcripts. They can contain personal, account, or proprietary information.

### Submission

At the common deadline, make your repository public so K2 can clone and review it.

Submit:

- the public GitHub repository URL
- the final commit SHA
- the items requested in your delivery email

For project questions or a private accommodation request, contact kris@k2vp.com.
