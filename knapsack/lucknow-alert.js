/* User-requested Lucknow alert draft. No external delivery or official verification. */
(()=>{
 const name='Lucknow · Uttar Pradesh';
 let index=zones.findIndex(z=>z[0]===name);
 if(index<0){index=zones.length;zones.push([name,26.8467,80.9462,'Red',0,0,0]);}
 ['weatherzone','destination','alertzone'].forEach(id=>{const select=document.getElementById(id);if(![...select.options].some(o=>o.value===String(index))){const option=document.createElement('option');option.value=index;option.textContent=name;select.append(option);}});
 renderZones();
 const message='DEMO ALERT — आधिकारिक चेतावनी नहीं\n\nलखनऊ, उत्तर प्रदेश के बाढ़ प्रभावित लोगों के लिए सूचना।\n\nआपके द्वारा बाढ़ की स्थिति बताई गई है; इसकी आधिकारिक पुष्टि लंबित है। प्रभावित इलाके और राहत केंद्रों की सत्यापित जानकारी के लिए स्थानीय प्रशासन के आधिकारिक अपडेट देखें।\n\nयह Knapsack hackathon का alert draft है। किसी वास्तविक SMS या WhatsApp संदेश की delivery नहीं हुई है।';
 document.getElementById('alertzone').value=String(index);
 document.getElementById('alertlevel').value='Red';
 document.getElementById('alertmessage').value=message;
 document.getElementById('alertchannel').value='Website only (local demo)';
 document.getElementById('alertpreview').innerHTML='<div class="phonehead">◈ KNAPSACK <small>LUCKNOW FLOOD · DEMO DRAFT</small></div><span class="riskbadge Red">Red · demo priority, not official severity</span><h3>Lucknow · Uttar Pradesh</h3><p>'+escape(message)+'</p><small>Draft only · 0 messages sent · no affected-area boundary verified</small>';
 document.getElementById('broadcastbody').insertAdjacentHTML('afterbegin','<p class="notice">Lucknow flood: user-reported situation, official verification pending. Red is a demo planning label. City coordinates are approximate and do not indicate a confirmed flood boundary.</p>');
 const alertId='lucknow-flood-demo';
 if(!state.alerts.some(a=>a.id===alertId)){
   state.alerts.push({id:alertId,area:name,message,level:'Red',time:'Demo scenario · official verification pending'});
   persist();
 }
 alertRender();
 const overview=document.getElementById('overview');
 if(!document.getElementById('lucknow-demo-alert')){
   const banner=document.createElement('article');
   banner.id='lucknow-demo-alert';
   banner.className='panel pad';
   banner.style.marginBottom='22px';
   banner.innerHTML='<span class="riskbadge Red">DEMO FLOOD ALERT · LUCKNOW</span><h2>लखनऊ, उत्तर प्रदेश — प्रभावित लोगों के लिए सूचना</h2><p>बाढ़ की स्थिति user-reported है; आधिकारिक पुष्टि लंबित है। स्थानीय प्रशासन के सत्यापित अपडेट देखें। Red label केवल demo planning priority है।</p><p class="fine">Hackathon simulation · 0 SMS/WhatsApp messages sent · प्रभावित इलाके की सीमा सत्यापित नहीं है।</p><button class="primary" data-view="broadcast">View alert →</button>';
   overview.prepend(banner);
 }
 view('overview');
})();
