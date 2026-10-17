import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import {Readable} from 'node:stream';import {fileURLToPath} from 'node:url';import {createApp} from './server.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../work/auth-tests');
test('signup, hashing, isolation, login, static protection, logout and origin checks',async()=>{
 const dataDir=await fs.mkdtemp(path.join(await fs.mkdir(root,{recursive:true}).then(()=>root),'test-'));
 let app=await createApp({dataDir});
 async function request(url,{method='GET',body,token,origin='http://127.0.0.1:3000'}={}){const req=Readable.from(body?[JSON.stringify(body)]:[]);Object.assign(req,{url,method,headers:{origin,'content-type':'application/json',...(token?{cookie:token}:{})},socket:{remoteAddress:'test-client'}});let status,headers,result;const res={writeHead(s,h){status=s;headers=h},end(b){result=b}};await app.handler(req,res);return {status,headers,body:Buffer.isBuffer(result)?result.toString():result}}
 const publicPage=await request('/about');assert.equal(publicPage.status,200);assert.ok(publicPage.body.includes('Knapsack Relief'));
 assert.equal((await request('/')).status,303);
 assert.equal((await request('/app.js')).status,303);
 assert.equal((await request('/auth/signup',{method:'POST',origin:'https://attacker.example',body:{}})).status,403);
 assert.equal((await request('/auth/signup',{method:'POST',body:{email:'test@example.com',password:'short'}})).status,400);
 const credentials={email:'test@example.com',password:'abc123'};
 const signup=await request('/auth/signup',{method:'POST',body:credentials});assert.equal(signup.status,200);
 assert.match(signup.headers['Set-Cookie'],/HttpOnly/);assert.match(signup.headers['Set-Cookie'],/SameSite=Strict/);
 const token=signup.headers['Set-Cookie'].split(';')[0];
 const file=await fs.readFile(path.join(dataDir,'accounts.json'),'utf8');assert.ok(!file.includes(credentials.password));const stored=JSON.parse(file)[0];assert.equal(stored.password.iterations,600000);assert.ok(stored.password.salt);
 const home=await request('/',{token});assert.equal(home.status,200);assert.ok(home.body.includes('/auth/backend.js'));
 assert.equal((await request('/auth/backend.js',{token})).status,200);
 const globe=await request('/earth-orbit.html',{token});assert.equal(globe.status,200);assert.equal(globe.headers['X-Frame-Options'],'SAMEORIGIN');
 assert.ok(home.body.indexOf('id="earth-orbit-section"')>home.body.indexOf('id="resources"'));
 assert.ok(home.body.indexOf('id="earth-orbit-section"')<home.body.indexOf('class="mainfooter"'));
 assert.equal((await request('/server.mjs',{token})).status,404);
 const image=await request('/auth/disaster-response-background.png');assert.equal(image.status,200);assert.equal(image.headers['Content-Type'],'image/png');
 assert.equal((await request('/auth/login',{method:'POST',body:{...credentials,password:'incorrect password'}})).status,401);
 assert.equal((await request('/auth/logout',{method:'POST',token})).status,200);
 assert.equal((await request('/',{token})).status,303);
 app=await createApp({dataDir});assert.equal((await request('/auth/login',{method:'POST',body:credentials})).status,200);
});
test('production requires HTTPS and sets secure host-only cookie',async()=>{
 const dataDir=await fs.mkdtemp(path.join(root,'prod-'));await assert.rejects(()=>createApp({production:true,origin:'http://example.com',dataDir}));
 const {handler}=await createApp({production:true,origin:'https://knapsack.example',dataDir});const req=Readable.from([JSON.stringify({email:'demo@example.com',password:'a different long passphrase'})]);Object.assign(req,{url:'/auth/signup',method:'POST',headers:{origin:'https://knapsack.example','content-type':'application/json'},socket:{remoteAddress:'test'}});let status,headers;await handler(req,{writeHead(s,h){status=s;headers=h},end(){}});assert.equal(status,200);assert.match(headers['Set-Cookie'],/^__Host-knapsack=/);assert.match(headers['Set-Cookie'],/; Secure/);
});
