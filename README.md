# Cabo charge splitter

sheet: [pbl.link/cabo-sheet](http://pbl.link/cabo-sheet)
results: [pbl.link/cabo-results](http://pbl.link/cabo-results)

## Steps 

1. Create a csv list of charges with these columns
    * Time, Item Name, Payer, Price, Chargees
    * (see charges.csv for example)

2. place .csv and cabo.py in same folder

3. run `python cabo.py YOUR_CSV_NAME.csv >> OUTPUT_FILE_NAME`
    * ex: python cabo.py charges.csv >> results.txt`
    * results will list payers and how much people owe them
    * results also list owers and how much they owe each payer

## Details

a charge is represented as

```
{
  day: string,
  item: string,
  payer: string, 
  amount: float,
  num_chargees: int,
  chargees: list of strings,
}
```

names must be unique


