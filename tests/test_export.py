import json
import sqlite3
import numpy as np
import pandas as pd
from src.export import export_dataset, generate_demo


def test_export_preserves_prices_and_provenance(tmp_path):
    p = pd.DataFrame({'A':[100.,80.,90.], 'B':[200.,202.,201.]},index=pd.bdate_range('2020-01-01',periods=3))
    meta=export_dataset(p,tmp_path,{'kind':'synthetic','source':'test'})
    d=json.loads((tmp_path/'market.json').read_text())
    assert meta['records']==6 and d['prices']['A']==[100,80,90]
    with sqlite3.connect(tmp_path/'market.sqlite') as c:
        assert c.execute('SELECT COUNT(*) FROM daily_prices').fetchone()[0]==6
        # SQL LAG independently recovers the first-day loss.
        r=c.execute("SELECT price / LAG(price) OVER (ORDER BY date)-1 FROM daily_prices WHERE ticker='A'").fetchall()
        assert np.isclose(r[1][0],-.2)
    again=export_dataset(p,tmp_path,{'kind':'synthetic','source':'test'})
    assert again['sha256']==meta['sha256']


def test_demo_is_reproducible_and_covers_six_assets():
    a,b=generate_demo(),generate_demo()
    pd.testing.assert_frame_equal(a,b)
    assert a.shape[1]==6 and a.size>30000
    assert np.isfinite(a.to_numpy()).all() and (a>0).all().all()
