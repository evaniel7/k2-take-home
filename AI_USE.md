# AI use

Complete this file before submission. If a section does not apply, write `None`.

## Tools used

Repeat this section for each AI tool.

### [Tool name]

- **Tasks the tool assisted:** [Describe the tasks.]
- **Intermediate artifacts generated through AI use:** [List generated plans, drafts, code, tests, or other artifacts.]
- **Important output checked or changed:** [Describe what you reviewed, tested, corrected, rejected, or rewrote.]

### Claude code

- **Tasks the tool assisted:**
    - Generating boiler plate code for frontend/, backend/, pytests, docker-compose.yml, and README.md.
    - Helped resolve unintended errors from batch tests after testing individually myself.
    - Generated seed_data.py with 14 sample records
    - Added status dropdown to queue page (RequestList.tsx)
    - Improved sort controls- combined sort field/order into single dropdown
    - Renamed "Archived" to "Declined" across frontend
    - Updated color scheme (green/purple accents)
- **Intermediate artifacts generated through AI use:**
    - backend/
    - frontend/
    - first draft of README.md
    - docker-compose.yml
    - seed_data.py
    - decisions.md UUID implementation note
- **Important output checked or changed:**
    - Problem with pytest batch test- fixed by editing backend/app/models.py to use SQLAlchemy 2.0's cross-database Uuid type
    - GET endpoint wasn't filtering out soft-deleted requests. Made an addition at line 103-106 in app/routers/requests.py
    - Added dropdown in frontend/src/pages/RequestDetail.tsx and RequestList.tsx
    - README.md detail- clarified bulk operations are used and updated Technical Point 3 to be more accurate.

## Final review

- [x] I understand the important AI-assisted work in this repository.
- [x] I checked or changed important AI output before submission.
- [x] I did not include private or proprietary information in this file.

Do not include full prompt transcripts. They can contain personal, account, private, or proprietary information.
