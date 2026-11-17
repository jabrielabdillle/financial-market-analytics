export const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
export const std=a=>{const average=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-average)**2,0)/(a.length-1))};
export const quantile=(a,q)=>{const b=[...a].sort((x,y)=>x-y),p=(b.length-1)*q,i=Math.floor(p);return b[i]+(b[Math.min(i+1,b.length-1)]-b[i])*(p-i)};
export function returns(p){return p.slice(1).map((v,i)=>v/p[i]-1)}
export function drawdowns(p){let high=p[0];return p.map(v=>{high=Math.max(v,high);return v/high-1})}
export function metrics(p,dates,rf=0){
 if(p.length<3||p.length!==dates.length||p.some(v=>!Number.isFinite(v)||v<=0)||!Number.isFinite(rf)||rf<=-1)throw Error('Provide at least three valid price dates and a valid risk-free rate.');
 const r=returns(p),s=std(r),years=(Date.parse(dates.at(-1))-Date.parse(dates[0]))/86400000/365.25;
 if(!(years>0))throw Error('The date range must increase.');
 const losses=r.map(v=>-v),v=quantile(losses,.95);
 return {observations:r.length,cumulative_return:p.at(-1)/p[0]-1,annualized_return:(p.at(-1)/p[0])**(1/years)-1,annualized_volatility:s*Math.sqrt(252),sharpe_ratio:s>1e-15?(mean(r)-((1+rf)**(1/252)-1))/s*Math.sqrt(252):null,maximum_drawdown:Math.min(...drawdowns(p)),daily_var95:v,daily_es95:mean(losses.filter(x=>x>=v))};
}
export function correlation(a,b){const ma=mean(a),mb=mean(b),sa=std(a),sb=std(b);return sa>1e-15&&sb>1e-15?a.reduce((s,v,i)=>s+(v-ma)*(b[i]-mb),0)/((a.length-1)*sa*sb):null}
export function rollingVol(p,window=63){const r=returns(p);return p.map((_,i)=>i<window?null:std(r.slice(i-window,i))*Math.sqrt(252))}
export function annualReturns(p,dates){const out={};returns(p).forEach((r,i)=>{const y=dates[i+1].slice(0,4);out[y]=(out[y]??1)*(1+r)});return Object.entries(out).map(([year,x])=>({year,value:x-1}))}
export function selectRange(data,start,end){const idx=data.dates.map((d,i)=>d>=start&&d<=end?i:-1).filter(i=>i>=0);if(idx.length<3)throw Error('Choose a date range containing at least three observations.');return {dates:idx.map(i=>data.dates[i]),prices:Object.fromEntries(data.assets.map(a=>[a.ticker,idx.map(i=>data.prices[a.ticker][i])]))}}
