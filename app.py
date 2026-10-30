import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Racing Sponsor AI | Prototype', page_icon='🏎️', layout='wide')

SEED = [
    {'company':'Atlas Automotive','sector':'Automotive','status':'Contacted','last_contact':'2026-10-15','notes':'Initial outreach sent.'},
    {'company':'Nova Energy','sector':'Energy','status':'Potential','last_contact':'2026-10-10','notes':'Prospective energy partner.'},
    {'company':'TechMotion','sector':'Electronics','status':'In Negotiation','last_contact':'2026-10-20','notes':'Discussing component support.'},
]
MEETING = '''29 October 2026 — Weekly Sponsorship Meeting (fictional demo)\n\nAtlas Automotive: The team received a positive response. A meeting is scheduled for next week.\nNova Energy: Initial sponsorship proposal sent. Follow up if no response within 7 days.\nTechMotion: Agreed to provide prototype sensors. Shipment date still needs confirmation.'''
SUGGESTIONS = [
    {'company':'Atlas Automotive','new_status':'Meeting Scheduled','next_action':'Prepare a sponsorship pitch deck and confirm meeting details.','evidence':'A meeting is scheduled for next week.'},
    {'company':'Nova Energy','new_status':'Contacted','next_action':'Follow up in 7 days if no response.','evidence':'Initial sponsorship proposal sent.'},
    {'company':'TechMotion','new_status':'Support Confirmed','next_action':'Confirm the shipment date for prototype sensors.','evidence':'Agreed to provide prototype sensors.'},
]
if 'crm' not in st.session_state:
    st.session_state.crm = pd.DataFrame(SEED)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'meeting' not in st.session_state:
    st.session_state.meeting = MEETING

st.title('🏎️ Racing Sponsor AI')
st.caption('Human-in-the-loop sponsorship CRM · Functional demo with fictional data')
st.info('Prototype mode: The suggestions below are pre-generated examples, not live AI analysis. No real sponsor or personal information is used.')

c1,c2,c3 = st.columns(3)
c1.metric('Sponsors',len(st.session_state.crm))
c2.metric('Proposed changes',len(SUGGESTIONS))
c3.metric('Approved changes',len(st.session_state.history))

t1,t2,t3 = st.tabs(['CRM Dashboard','Meeting → Suggestions','Audit History'])
with t1:
    st.subheader('Sponsor pipeline')
    st.dataframe(st.session_state.crm,hide_index=True,use_container_width=True)
    st.download_button('Export CRM (CSV)',st.session_state.crm.to_csv(index=False).encode('utf-8'),'sponsors.csv','text/csv')
with t2:
    st.subheader('Sample weekly meeting notes')
    st.text_area('Meeting transcript',value=st.session_state.meeting,height=220,disabled=True)
    st.caption('This fixed sample demonstrates the review workflow. Live document parsing and AI extraction are planned extensions.')
    st.subheader('Review proposed CRM updates')
    with st.form('review'):
        decisions = {}
        for item in SUGGESTIONS:
            matching = st.session_state.crm[st.session_state.crm.company==item['company']]
            old = matching.iloc[0]['status'] if not matching.empty else 'Not found'
            st.markdown(f"**{item['company']}** — `{old}` → `{item['new_status']}`")
            st.write(f"**Evidence:** {item['evidence']}")
            st.write(f"**Recommended action:** {item['next_action']}")
            decisions[item['company']] = st.checkbox(f"Approve update for {item['company']}",key=f"approve_{item['company']}")
            st.divider()
        submitted=st.form_submit_button('Apply selected updates',type='primary')
    if submitted:
        count=0
        for item in SUGGESTIONS:
            if not decisions[item['company']]:
                continue
            mask=st.session_state.crm.company==item['company']
            if not mask.any():
                continue
            old=st.session_state.crm.loc[mask,'status'].iloc[0]
            new=item['new_status']
            if old==new:
                continue
            st.session_state.crm.loc[mask,'status']=new
            st.session_state.crm.loc[mask,'notes']=item['next_action']
            st.session_state.history.append({'timestamp_utc':datetime.utcnow().isoformat(timespec='seconds')+'Z','company':item['company'],'previous_status':old,'approved_status':new,'evidence':item['evidence'],'next_action':item['next_action'],'source':'Fictional weekly meeting'})
            count+=1
        st.success(f'{count} update(s) approved and recorded. Open the CRM and Audit History tabs to inspect.')
with t3:
    st.subheader('Change history')
    if st.session_state.history:
        history_df=pd.DataFrame(st.session_state.history)
        st.dataframe(history_df,hide_index=True,use_container_width=True)
        st.download_button('Export history (CSV)',history_df.to_csv(index=False).encode('utf-8'),'sponsor_history.csv','text/csv')
    else:
        st.write('No updates approved yet. Approve changes in the Meeting tab.')
    st.caption('Demo data persists during the current Streamlit session only. Persistent SQLite storage is a planned extension.')
