from scrapyUFC.models import Fighter, Fight, Event, create_table, db_connect 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from hashlib import sha256
import re


class UfcPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates fighters table. 
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_fighters(self, item):
        """
        Save the info of the fighters into the database
        """
        session = self.Session()
        fighter = Fighter()

        fighter.id = item.id
        fighter.name = item.name
        fighter.nationality = item.nationality
        fighter.locality = item.locality
        fighter.age = item.age
        fighter.weight_class = item.weight_class
        fighter.wins = item.wins
        fighter.wins_by_ko_tko = item.wins_by_ko_tko
        fighter.wins_by_sub = item.wins_by_sub
        fighter.wins_by_dec = item.wins_by_dec
        fighter.losses = item.losses
        fighter.losses_by_ko_tko = item.losses_by_ko_tko
        fighter.losses_by_sub = item.losses_by_sub
        fighter.losses_by_dec = item.losses_by_dec

        existing_fighter = session.query(Fighter).filter_by(id=item.id).first()
        if not existing_fighter:
            try:
                session.add(fighter)
                session.commit()
            except:
                session.rollback()
                raise
        
        session.close()

        return item

    def process_fights(self, item):
        """
        Save the info of the fights into the database
        """
        session = self.Session()
        fight = Fight()

        # raw fields  
        fight.event_title = item.event_title
        fight.left_fighter_id = item.left_fighter_id
        fight.left_status = item.left_status
        fight.right_fighter_id = item.right_fighter_id
        fight.right_status = item.right_status 
        fight.weight_class = item.weight_class
        fight.fight_weight = item.fight_weight
        fight.method = item.method
        fight.round = item.round
        fight.time = item.time

        # clean the event title
        fight.event_title_cleaned = re.sub(r"\s*[-\.]\s*|\s+", '-', item.event_title)

        # get the names of the fighters based of id
        left_fighter_name = session.query(Fighter.name).filter_by(id=item.left_fighter_id).first()
        fight.left_fighter_name = left_fighter_name[0] if left_fighter_name else None
        right_fighter_name = session.query(Fighter.name).filter_by(id=item.right_fighter_id).first()
        fight.right_fighter_name = right_fighter_name[0] if right_fighter_name else None

        if left_fighter_name is None:
            with open('missing_fighters.csv', 'a') as file:
                file.write(f"/fighter/{item.left_fighter_id}\n")
        if right_fighter_name is None:
            with open('missing_fighters.csv', 'a') as file:
                file.write(f"/fighter/{item.right_fighter_id}\n")

        # generate the id for the fight
        fight.id = sha256(f'{item.left_fighter_id}{item.right_fighter_id}{item.event_title}'.encode('ascii')).hexdigest()

        existing_fight = session.query(Fight).filter_by(id=fight.id).first()
        if existing_fight:
            try:
                existing_fight.left_status = fight.left_status
                existing_fight.right_status = fight.right_status
                existing_fight.method = fight.method
                existing_fight.round = fight.round
                existing_fight.time = fight.time
                session.commit()
            except:
                session.rollback()
                raise
        else:
            try:
                session.add(fight)
                session.commit()
            except:
                session.rollback()
                raise
        
        session.close()

        return item
    
    def process_events(self, item):
        """
        Save the info of the events into the database
        """
        session = self.Session()
        event = Event()

        event.title = item.title
        event.date = item.date
        event.location = item.location

        existing_event = session.query(Event.title).filter_by(title=item.title).first()
        if not existing_event:
            try:
                session.add(event)
                session.commit()
            except:
                session.rollback()
                raise
        
        session.close()

        return item
