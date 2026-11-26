"""Named losses, entrants and exits around each Medibank-interest site; APHA 2025 replication; national trend."""
import sys, numpy as np, pandas as pd
p = pd.read_csv(sys.argv[1], dtype={'prov': str, 'postcode': str}, parse_dates=['snapshot']); out = sys.argv[2]
S = sorted(p.snapshot.unique()); END = S[-1]
loc = p.sort_values('snapshot').groupby('prov')[['name','lat','lon','state','postcode','cat']].last()
wide = p.pivot(index='prov', columns='snapshot', values='agree')
MB = ['0017500W','0037140T','0017360L','0065780W','0095140A','0015550A','0056310K']
def hav(a,b,c,d):
    a,b,c,d = map(np.radians,[a,b,c,d]); x=np.sin((c-a)/2)**2+np.cos(a)*np.cos(c)*np.sin((d-b)/2)**2; return 12742*np.arcsin(np.sqrt(x))
loc['first']=wide.notna().idxmax(axis=1); loc['last']=wide.notna()[wide.columns[::-1]].idxmax(axis=1)
loc['agree_first']=[wide.at[i,loc.at[i,'first']] for i in loc.index]; loc['agree_last']=[wide.at[i,loc.at[i,'last']] for i in loc.index]
# every change event per hospital
ev=[]
for i,row in wide.iterrows():
    s=row.dropna(); prev=None
    for t,v in s.items():
        if prev is not None and v!=prev: ev.append(dict(prov=i,snapshot=t.date(),change='LOST' if v==0 else 'GAINED'))
        prev=v
ev=pd.DataFrame(ev).merge(loc[['name','state','postcode','cat','lat','lon']],left_on='prov',right_index=True)
sites={'0017500W':'East Sydney Private','0037140T':'Adeney Private','0017360L':'Macquarie Uni Hospital (TOI)','0065780W':'Western Hospital'}
rows=[]
for c,lab in sites.items():
    d=hav(loc.at[c,'lat'],loc.at[c,'lon'],loc.lat,loc.lon)
    for i in loc.index[(d<=50)&(~loc.index.isin(MB))]:
        base=dict(site=lab,km=round(d[i],1),prov=i,name=loc.at[i,'name'],cat=loc.at[i,'cat'],postcode=loc.at[i,'postcode'])
        for _,e in ev[ev.prov==i].iterrows(): rows.append({**base,'type':e.change,'date':e.snapshot})
        if loc.at[i,'first']>S[0]: rows.append({**base,'type':'ENTERED '+('with' if loc.at[i,'agree_first']==1 else 'WITHOUT')+' agreement','date':loc.at[i,'first'].date()})
        if loc.at[i,'last']<END: rows.append({**base,'type':'EXITED list ('+('had' if loc.at[i,'agree_last']==1 else 'no')+' agreement)','date':loc.at[i,'last'].date()})
det=pd.DataFrame(rows).sort_values(['site','date','km']); det.to_csv(f'{out}/events_within_50km.csv',index=False)
ev.to_csv(f'{out}/all_status_changes.csv',index=False)
# entrants: national vs within 50km of any MB surgical site
ent=loc[loc['first']>S[0]].copy(); ent=ent[~ent.index.isin(MB)]
near=np.zeros(len(ent),bool)
for c in sites: near|=hav(loc.at[c,'lat'],loc.at[c,'lon'],ent.lat,ent.lon).values<=50
ent['near']=near; ent['agree_now']=wide.loc[ent.index,END]
print('ENTRANTS: n, share with agreement at entry, share with agreement now (if still listed)')
print(ent.groupby('near').agg(n=('name','size'),at_entry=('agree_first','mean'),now=('agree_now','mean')).round(3))
print(ent.groupby(['near',ent.cat.isin(['A','B'])]).agg(n=('name','size'),at_entry=('agree_first','mean')).round(3))
# national trend by snapshot, count and by category group
nat=p.groupby('snapshot').agg(n=('agree','size'),rate=('agree','mean'))
nat['rate_excl_AB']=p[~p.cat.isin(['A','B'])].groupby('snapshot').agree.mean()
nat.to_csv(f'{out}/national_trend.csv'); print(nat.round(4).to_string())
# APHA 2025 replication: ESPH, Aug 2020 vs Jul 2025, all categories, by radius
d=hav(loc.at['0017500W','lat'],loc.at['0017500W','lon'],loc.lat,loc.lon)
print('APHA replication (all cats, excl ESPH):')
for r in [10,20,25,30,40,50,75,100,150,200]:
    ids=loc.index[(d<=r)&(loc.index!='0017500W')]
    a=wide.loc[ids,S[0]].dropna(); b=wide.loc[ids,pd.Timestamp('2025-07-01')].dropna()
    print(r,'km', f'{int(a.sum())}/{len(a)}={a.mean():.2%}', '->', f'{int(b.sum())}/{len(b)}={b.mean():.2%}')
