from dataclasses import dataclass
from typing import Optional 

@dataclass
class FightItem:
    id: str
    event_title: str
    left_fighter_id: str
    left_status: str
    right_fighter_id: str
    right_status: str
    weight_class: str
    method: str
    round: Optional[int] 
    time: Optional[str] 

@dataclass
class FighterItem:
    id: str
    name: str
    nationality: Optional[str]
    locality: Optional[str]
    age: Optional[int]
    weight_class: Optional[str]
    wins: int
    wins_by_ko_tko: int
    wins_by_sub: int
    wins_by_dec: int
    losses: int
    losses_by_ko_tko: int
    losses_by_sub: int
    losses_by_dec: int
