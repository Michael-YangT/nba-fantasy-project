from dataclasses import dataclass, field


@dataclass
class AppConfig:
    smtp_user: str = "623254916@qq.com"
    smtp_password: str = ""
    to_email: str = "623254916@qq.com"
    schedule_hour: int = 14
    schedule_minute: int = 0
    data_dir: str = "data"
    processed_dir: str = "processed"
    league_constraints: dict = field(default_factory=lambda: {
        "position_slots": {
            "PG": 1,
            "SG": 1,
            "SF": 1,
            "PF": 1,
            "C": 1,
            "G": 1,
            "F": 1,
            "UTIL": 2,
        },
        "max_players": 10,
    })
