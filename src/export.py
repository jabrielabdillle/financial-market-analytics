"""Export a reproducible research dataset to JSON, CSV, and SQLite.

Default is deterministic synthetic data; --prices requires explicit source metadata.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
from .metrics import calculate_metrics, period_returns, validate_prices

ASSETS = {'US_EQ':'US equity model','TECH':'Technology equity model','SMALL':'Small-cap equity model',
          'INTL':'International equity model','BONDS':'Bond model','GOLD':'Gold model'}

def generate_demo() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.bdate_range('2006-01-02','2025-12-31')
    n = len(dates)-1
    common = rng.normal(0, 1, n)
    stress = np.zeros(n, dtype=bool)
    # Arbitrary synthetic intervals; not fitted to historical market events.
    stress[550:680] = True
    stress[2450:2550] = True
    stress[4400:4520] = True
    factors = common * np.where(stress, 2.4, 1.0)
    values = {}
    for name, drift, sigma, beta in zip(ASSETS, [.07,.09,.06,.05,.025,.035], [.16,.23,.21,.18,.055,.14], [.8,.85,.75,.7,-.15,.1]):
        z = beta*factors + np.sqrt(1-beta**2)*rng.normal(0,1,n)
        daily = (drift-.5*sigma**2)/252 + sigma/np.sqrt(252)*z - stress*.001*max(beta,0)
        values[name] = np.r_[100., 100*np.exp(np.cumsum(daily))]
    return pd.DataFrame(values,index=dates).round(6)

def export_dataset(prices, output, metadata):
    prices = validate_prices(prices)
    output = Path(output); output.mkdir(parents=True,exist_ok=True)
    prices.index.name = 'date'
    csv = prices.to_csv(float_format='%.6f', lineterminator='\n')
    (output/'prices.csv').write_text(csv)
    metadata = {**metadata, 'start':str(prices.index[0].date()),'end':str(prices.index[-1].date()),
        'dates':len(prices),'records':int(prices.size),'assets':len(prices.columns),
        'sha256':hashlib.sha256(csv.encode()).hexdigest(),'risk_free_rate':0,
        'annualization':'CAGR: calendar days / 365.25; volatility and Sharpe: 252 sessions',
        'missing_policy':'Reject missing/non-positive/non-finite prices; no implicit filling.'}
    payload = {'metadata':metadata, 'assets':[{'ticker':t,'name':ASSETS.get(t,t)} for t in prices],
        'dates':prices.index.strftime('%Y-%m-%d').tolist(), 'prices':{t:prices[t].tolist() for t in prices},
        'metrics':json.loads(calculate_metrics(prices).to_json(orient='records')),
        'annual_returns':json.loads(period_returns(prices,'Y').rename_axis('year').reset_index().assign(year=lambda d:d.year.astype(str)).to_json(orient='records'))}
    (output/'market.json').write_text(json.dumps(payload,allow_nan=False,separators=(',',':')))
    calculate_metrics(prices).to_csv(output/'metrics.csv',index=False)
    period_returns(prices,'Y').to_csv(output/'annual_returns.csv')
    (output/'provenance.json').write_text(json.dumps(metadata,indent=2))
    db_path = output/'market.sqlite'
    db_path.unlink(missing_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute('CREATE TABLE daily_prices(date TEXT NOT NULL,ticker TEXT NOT NULL,price REAL NOT NULL CHECK(price>0),PRIMARY KEY(date,ticker))')
        conn.executemany('INSERT INTO daily_prices VALUES (?,?,?)', ((d.strftime('%Y-%m-%d'),t,float(v)) for d,row in prices.iterrows() for t,v in row.items()))
        conn.execute('CREATE INDEX prices_by_asset ON daily_prices(ticker,date)')
        conn.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
        conn.executemany('INSERT INTO metadata VALUES (?,?)', ((k,json.dumps(v)) for k,v in metadata.items()))
    return metadata

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prices',type=Path)
    parser.add_argument('--source')
    parser.add_argument('--adjustment')
    parser.add_argument('--output',type=Path,default=Path('web/public/data'))
    args=parser.parse_args()
    if args.prices:
        if not args.source or not args.adjustment: parser.error('--prices requires --source and --adjustment')
        prices=pd.read_csv(args.prices,index_col='date',parse_dates=True)
        meta={'kind':'user-supplied','source':args.source,'adjustment':args.adjustment,'note':'User supplied prices; verify source rights and data quality before publication.'}
    else:
        prices=generate_demo()
        meta={'kind':'synthetic','source':'NumPy PCG64, seed 42; factor simulation v1','adjustment':'Synthetic price levels; no corporate actions',
              'note':'All displayed prices and results are simulated. No actual ETF performance. Weekdays include exchange holidays; stress intervals are arbitrary.'}
    print(json.dumps(export_dataset(prices,args.output,meta),indent=2))

if __name__=='__main__': main()
