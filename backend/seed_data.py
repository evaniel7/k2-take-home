"""Seed script to populate the database with sample data."""
import uuid
from datetime import datetime, timedelta

from app.database import SessionLocal, engine, Base
from app.models import Request, RequestStatus

# Sample requests data
SAMPLE_REQUESTS = [
    # New requests (pending decision)
    {
        "title": "Add dark mode support",
        "problem_statement": "Users have been requesting a dark theme option for the application. Eye strain during nighttime usage is a common complaint, and many competing products already offer this feature.",
        "expected_impact": "Improved user satisfaction and accessibility. Expected to increase evening usage sessions by 20% based on user surveys.",
        "urgency": 3,
        "status": RequestStatus.NEW,
    },
    {
        "title": "Implement SSO with Google Workspace",
        "problem_statement": "Enterprise customers need single sign-on integration with Google Workspace. Currently, users must manage separate credentials which creates friction and security concerns.",
        "expected_impact": "Will unlock 3 pending enterprise deals worth approximately $150k ARR. Reduces onboarding time for new team members.",
        "urgency": 4,
        "status": RequestStatus.NEW,
    },
    {
        "title": "Add CSV export for reports",
        "problem_statement": "Finance teams need to export report data to CSV for analysis in Excel. Currently they must manually copy data which is error-prone and time-consuming.",
        "expected_impact": "Saves finance users approximately 2 hours per week. Reduces data entry errors in downstream reporting.",
        "urgency": 2,
        "status": RequestStatus.NEW,
    },
    {
        "title": "Mobile app push notifications",
        "problem_statement": "Users miss important updates because they don't check the app regularly. Competitors offer push notifications for critical alerts.",
        "expected_impact": "Increase mobile engagement by 35%. Faster response times to urgent items.",
        "urgency": 3,
        "status": RequestStatus.NEW,
    },
    {
        "title": "Bulk import tool for inventory",
        "problem_statement": "New customers with large existing inventories spend days manually entering items. This slows onboarding and creates frustration.",
        "expected_impact": "Reduce average onboarding time from 5 days to 1 day. Improve first-week retention rate.",
        "urgency": 2,
        "status": RequestStatus.NEW,
    },

    # Accepted requests
    {
        "title": "Two-factor authentication",
        "problem_statement": "Security-conscious customers require 2FA before they can adopt the platform. This is blocking several healthcare and financial services deals.",
        "expected_impact": "Unlocks regulated industry verticals. Required for SOC 2 compliance which is on our roadmap.",
        "urgency": 4,
        "status": RequestStatus.ACCEPTED,
        "decision_reason": "Critical for enterprise sales and compliance. Aligns with Q2 security initiative. Engineering has capacity starting next sprint.",
    },
    {
        "title": "Webhook integrations",
        "problem_statement": "Power users want to connect our platform to their automation tools like Zapier and Make. Currently no way to trigger external workflows.",
        "expected_impact": "Enables integration ecosystem. Reduces churn among technical users by 15%.",
        "urgency": 3,
        "status": RequestStatus.ACCEPTED,
        "decision_reason": "Strong demand from power users segment. Relatively low engineering effort with high value. Scheduled for next month.",
    },
    {
        "title": "Improved search functionality",
        "problem_statement": "Search is basic and doesn't support filters or advanced queries. Users with large datasets struggle to find specific items.",
        "expected_impact": "Reduce time-to-find by 60%. Address top support ticket category.",
        "urgency": 3,
        "status": RequestStatus.ACCEPTED,
        "decision_reason": "Top requested feature in last NPS survey. Will significantly improve UX for power users.",
    },

    # Deferred requests
    {
        "title": "Native desktop application",
        "problem_statement": "Some users prefer a native desktop experience over the web app. They want offline access and system tray integration.",
        "expected_impact": "Would appeal to a subset of power users. Estimated 5% of user base would adopt.",
        "urgency": 1,
        "status": RequestStatus.DEFERRED,
        "decision_reason": "Interesting idea but low priority given current web-first strategy. Will revisit in Q4 after mobile app launch.",
    },
    {
        "title": "AI-powered suggestions",
        "problem_statement": "Users want intelligent recommendations based on their usage patterns. Competitors are adding AI features rapidly.",
        "expected_impact": "Could differentiate product in market. Potential to increase engagement metrics.",
        "urgency": 2,
        "status": RequestStatus.DEFERRED,
        "decision_reason": "Exciting opportunity but requires significant R&D investment. Deferring until we have dedicated ML resources in Q3.",
    },
    {
        "title": "Custom branding for enterprise",
        "problem_statement": "Enterprise customers want to white-label the platform with their own logos and colors for internal use.",
        "expected_impact": "Potential upsell opportunity for enterprise tier. 2 customers have specifically requested this.",
        "urgency": 2,
        "status": RequestStatus.DEFERRED,
        "decision_reason": "Valid enterprise need but only 2 requests so far. Will implement when we have 5+ committed customers.",
    },

    # Declined requests
    {
        "title": "Cryptocurrency payment option",
        "problem_statement": "A few users have asked to pay subscriptions using Bitcoin or Ethereum.",
        "expected_impact": "Would appeal to crypto-enthusiast segment. Unclear size of demand.",
        "urgency": 1,
        "status": RequestStatus.DECLINED,
        "decision_reason": "Very niche request with significant implementation complexity and regulatory considerations. Does not align with target customer profile.",
    },
    {
        "title": "Windows XP support",
        "problem_statement": "One enterprise customer still uses Windows XP on some legacy machines and cannot access the web app properly.",
        "expected_impact": "Would retain one specific customer account worth $2k/year.",
        "urgency": 1,
        "status": RequestStatus.DECLINED,
        "decision_reason": "Cannot justify engineering effort for unsupported OS. Security implications are unacceptable. Offered customer migration assistance instead.",
    },
    {
        "title": "Remove all analytics tracking",
        "problem_statement": "Privacy-focused user requests option to disable all analytics and telemetry completely.",
        "expected_impact": "Would satisfy small privacy-conscious segment.",
        "urgency": 1,
        "status": RequestStatus.DECLINED,
        "decision_reason": "Analytics are essential for product improvement and already GDPR compliant. We've documented our privacy practices transparently.",
    },
]


def seed_database():
    """Seed the database with sample data."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if data already exists
        existing = db.query(Request).count()
        if existing > 0:
            print(f"Database already has {existing} requests. Skipping seed.")
            return

        # Create sample requests with staggered timestamps
        base_time = datetime.utcnow() - timedelta(days=14)

        for i, data in enumerate(SAMPLE_REQUESTS):
            request = Request(
                id=uuid.uuid4(),
                title=data["title"],
                problem_statement=data["problem_statement"],
                expected_impact=data["expected_impact"],
                urgency=data["urgency"],
                status=data["status"],
                decision_reason=data.get("decision_reason"),
                created_at=base_time + timedelta(days=i * 0.5),
                updated_at=base_time + timedelta(days=i * 0.5 + 1),
            )
            db.add(request)

        db.commit()
        print(f"Successfully seeded {len(SAMPLE_REQUESTS)} sample requests.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
