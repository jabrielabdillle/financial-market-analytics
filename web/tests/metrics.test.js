import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {metrics,annualReturns,correlation,selectRange} from '../src/metrics.js';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('first-day loss, tail risk, and partial years match hand calculations',()=>{const p=[100,80,120,90],d=['2020-12-30','2020-12-31','2021-01-04','2021-01-05'];const m=metrics(p,d);near(m.maximum_drawdown,-.25);near(m.daily_var95,.245);near(m.daily_es95,.25);const a=annualReturns(p,d);near(a[0].value,-.2);near(a[1].value,.125)});
test('constant prices and insufficient windows are handled',()=>{assert.equal(metrics([100,100,100],['2020-01-01','2020-01-02','2020-01-03']).sharpe_ratio,null);assert.equal(correlation([0,0,0],[1,2,3]),null);assert.throws(()=>selectRange({dates:['2020-01-01'],assets:[]},'2020-01-01','2020-01-02'))});
test('all browser metrics agree with Python reference outputs',()=>{const d=JSON.parse(fs.readFileSync('public/data/market.json','utf8'));for(const ref of d.metrics){const actual=metrics(d.prices[ref.ticker],d.dates);for(const k of Object.keys(actual)){if(ref[k]===null)assert.equal(actual[k],null);else near(actual[k],ref[k])}}});
