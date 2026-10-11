/* Login interface. Real account authentication requires a connected hosted identity service. */
(()=>{
 if(window.KNAPSACK_SERVER_AUTH){
   document.body.classList.add('realistic-background');
   const button=document.createElement('button');button.className='logoutbtn';button.textContent='Sign out';
   button.onclick=async()=>{button.disabled=true;try{const r=await fetch('/auth/logout',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:'{}'});if(!r.ok)throw Error();location.assign('/auth')}catch{button.disabled=false;toast('Unable to sign out. Try again.')}};
   document.querySelector('main header>div:last-child').prepend(button);return;
 }
 const screen=document.createElement('section');screen.className='login-screen';screen.setAttribute('aria-label','Knapsack sign in');
 screen.innerHTML='<div class="login-story"><div class="login-brand">◈ Knapsack Relief</div><div class="eyebrow">DISASTER INTELLIGENCE</div><h1>Prepared together.<br><span>Resilient together.</span></h1><p>A shared command center for risk awareness, relief supplies and coordinated response.</p><div class="login-tags"><span>Risk intelligence</span><span>Relief coordination</span><span>Knapsack optimization</span></div><p class="background-credit">AI-generated illustrative disaster-response scene</p></div><div class="login-card"><span class="eyebrow">RESPONSE WORKSPACE</span><h2>Welcome back.</h2><p>Sign in to your Knapsack workspace.</p><form id="loginform"><label>Email<input id="loginemail" type="email" autocomplete="username" required placeholder="you@example.com"></label><label>Password<div class="passwordfield"><input id="loginpassword" type="password" autocomplete="current-password" required placeholder="Your password"><button type="button" id="showpassword">Show</button></div></label><button class="primary" type="submit">Sign in →</button><p id="loginfeedback" class="login-feedback" role="status"></p></form><div class="login-divider"></div><button class="secondary login-demo" id="enterdemo">Explore hackathon demo</button><p class="login-foot">Secure signup and login require the included Node server. Opening this HTML file directly is demo-only. Do not enter a real password here.</p></div>';
 document.body.append(screen);document.body.classList.add('realistic-background');
 const workspace=[...document.querySelectorAll('body>main,body>aside,.annotationbar,.annotationdrawer')];
 const setScreen=open=>{screen.hidden=!open;workspace.forEach(el=>el.inert=open);if(open)document.getElementById('loginemail').focus()};
 setScreen(true);
 const pass=document.getElementById('loginpassword');
 document.getElementById('showpassword').onclick=e=>{const reveal=pass.type==='password';pass.type=reveal?'text':'password';e.target.textContent=reveal?'Hide':'Show'};
 document.getElementById('loginform').onsubmit=e=>{e.preventDefault();pass.value='';document.getElementById('loginfeedback').textContent='Open through the included Node server for signup and login. This direct HTML preview is demo-only; no credentials were sent or saved.'};
 document.getElementById('enterdemo').onclick=()=>{setScreen(false);pass.value='';document.getElementById('loginemail').value='';toast('Demo workspace opened. No account authentication performed.')};
 const button=document.createElement('button');button.className='logoutbtn';button.textContent='Sign in';button.onclick=()=>{setScreen(true);document.getElementById('loginfeedback').textContent=''};
 document.querySelector('main header>div:last-child').prepend(button);
 document.querySelector('.mainfooter').insertAdjacentHTML('beforeend','<span class="background-credit">AI-generated background illustration</span>');
})();


