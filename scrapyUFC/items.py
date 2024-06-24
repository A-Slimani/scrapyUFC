from dataclasses import dataclass

@dataclass
class FightItem:
    event_title: str
    left_fighter: str
    left_status: str
    right_fighter: str
    right_status: str
    weight_class: str
    method: str
    round: int 
    time: str 
    left_fighter_url: str
    right_fighter_url: str

@dataclass
class FighterInfoItem:
    name: str
    nationality: str
    locality: str
    age: int
    weight_class: str
    wins: int
    wins_by_ko_tko: int
    wins_by_sub: int
    wins_by_dec: int
    losses: int
    losses_by_ko_tko: int
    losses_by_sub: int
    losses_by_dec: int
