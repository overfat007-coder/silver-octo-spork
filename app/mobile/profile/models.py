"""Profile models."""

from dataclasses import dataclass


@dataclass
class Profile:
    user_id: str
    display_name: str
    bio: str = ""
