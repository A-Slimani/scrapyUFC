from sqlalchemy.orm import sessionmaker
from scrapyUFC.models import Fighter, Fight, Event, create_table, db_connect 


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

        fight.id = item.id
        fight.left_status = item.left_status
        fight.right_status = item.right_status 
        fight.weight_class = item.weight_class
        fight.method = item.method
        fight.round = item.round
        fight.time = item.time

        # get the names of the fighters
        left_fighter_name = session.query(Fighter.name).filter_by(id=item.left_fighter_id).first()
        fight.left_fighter_name = left_fighter_name[0] if left_fighter_name else None

        right_fighter_name = session.query(Fighter.name).filter_by(id=item.right_fighter_id).first()
        fight.right_fighter_name = right_fighter_name[0] if right_fighter_name else None

        existing_fight = session.query(Fight.id).filter_by(id=item.id).first()
        if not existing_fight:
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
