# UFC SCRAPER 
- Scrapes previous fights and fighter info

## Steps
Run the scraper in this order
- ufcevents 
- ufcall
- ufcfighters

## TODO
- Make this run periodically in the background (with my server) <- Completed ensure it works
- Find a way to automatically add new fighters if they dont exist in the fighter table
    - Add their link to missing_fighters.csv <-- Complete: check if works 
- ufcall -> update existing records (somewhat works)

### Later
- Create a discord bot that provides updates when the script has run 
- Rewrite the scraper in go for faster scraping
  - Or use asynchronous requests or something of the sort
