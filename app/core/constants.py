from app.models import SubscriptionLevel

# Değiştirilecek

SUBSCRIPTION_FEATURES = {
    SubscriptionLevel.FREE: {
        "max_users": 1,
        "storage_limit_gb": 1,
        "support": "none",
        "features": ["basic_dashboard"],
    },
    SubscriptionLevel.GOLD: {
        "max_users": 5,
        "storage_limit_gb": 10,
        "support": "email",
        "features": ["dashboard", "basic_reports"],
    },
    SubscriptionLevel.PREMIUM: {
        "max_users": 20,
        "storage_limit_gb": 50,
        "support": "priority_email",
        "features": ["advanced_dashboard", "team_collaboration", "analytics"],
    },
    SubscriptionLevel.PRO: {
        "max_users": 100,
        "storage_limit_gb": 200,
        "support": "24_7_support",
        "features": ["all_features", "custom_integrations", "dedicated_manager"],
    },
}
