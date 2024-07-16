from dataclasses import dataclass
from datetime import date
from typing import Optional 

@dataclass
class FightItem:
    event_title: str
    left_fighter_id: str
    left_status: Optional[str]
    right_fighter_id: str
    right_status: Optional[str]
    weight_class: str
    fight_weight: int 
    method: Optional[str]
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

@dataclass
class EventItem:
    title: str
    date: date 
    location: str
    url: str