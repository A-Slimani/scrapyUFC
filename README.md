# UFC SCRAPER 
- Scrapes previous fights and fighter info

## TODO
- Make this run periodically in the background (with my server) <- Make sure this works
- Find a way to automatically add new fighters if they dont exist in the fighter table
    - Add their link to new_fighters.csv
- ufcall -> automatically skip the scripting if an event has been found?
    - Create the same script call it ufcupdate only run through events that are new
        - Get this from the events table
- Create a discord bot that provides updates for this
- Create a proper logger for it
    - Log only errors