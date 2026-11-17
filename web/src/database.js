import initSqlJs from 'sql.js';
import wasmUrl from 'sql.js/dist/sql-wasm.wasm?url';
let pending;
export function openDatabase(){return pending??=(async()=>{const SQL=await initSqlJs({locateFile:()=>wasmUrl});const response=await fetch('./data/market.sqlite');if(!response.ok)throw Error('The database could not be loaded. Please reload to retry.');return new SQL.Database(new Uint8Array(await response.arrayBuffer()))})()}
export function query(db,sql,params=[]){const statement=db.prepare(sql);try{statement.bind(params);const rows=[];while(statement.step())rows.push(statement.getAsObject());return rows}finally{statement.free()}}
export function priceRows(db,asset,start,end,offset=0,limit=25){const params=[asset,asset,start,end];const where="WHERE (?='ALL' OR ticker=?) AND date>=? AND date<=?";return {count:query(db,`SELECT COUNT(*) AS n FROM daily_prices ${where}`,params)[0].n,rows:query(db,`SELECT date,ticker,price FROM daily_prices ${where} ORDER BY date DESC,ticker ${limit?'LIMIT ? OFFSET ?':''}`,limit?[...params,limit,offset]:params)}}
