import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomBytes,pbkdf2,timingSafeEqual,createHash} from 'node:crypto';
import {promisify} from 'node:util';
const derive=promisify(pbkdf2),base=path.dirname(fileURLToPath(import.meta.url));
const ttl=8*60*60*1000,iterations=600000;
export async function passwordHash(password,salt=randomBytes(24).toString('hex')){return {salt,hash:(await derive(password,salt,iterations,32,'sha256')).toString('hex'),iterations,algorithm:'pbkdf2-sha256'}}
export async function passwordMatches(password,record){const result=await derive(password,record.salt,record.iterations,32,'sha256');return timingSafeEqual(result,Buffer.from(record.hash,'hex'))}
export async function createApp({origin='http://127.0.0.1:3000',production=false,dataDir=path.join(base,'data'),siteDir=path.resolve(base,'../knapsack')}={}){
 if(new URL(origin).origin!==origin||(production&&!origin.startsWith('https://')))throw Error('APP_ORIGIN must be a bare origin; production requires https.');
 dataDir=path.resolve(dataDir);siteDir=path.resolve(siteDir);
 if(dataDir===siteDir||dataDir.startsWith(siteDir+path.sep))throw Error('Authentication data must be outside the public website directory.');
 await fs.mkdir(dataDir,{recursive:true,mode:0o700});const accountFile=path.join(dataDir,'accounts.json');let accounts=[];
 try{accounts=JSON.parse(await fs.readFile(accountFile,'utf8'))}catch(e){if(e.code!=='ENOENT')throw e}
 const sessions=new Map(),limits=new Map();let writes=Promise.resolve(),hashJobs=0;
 const cookieName=production?'__Host-knapsack':'knapsack_session';
 const cookie=(token,age=ttl/1000)=>`${cookieName}=${token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${age}${production?'; Secure':''}`;
 const digest=token=>createHash('sha256').update(token).digest('hex');
 const response=(res,code,data,headers={})=>{res.writeHead(code,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin','X-Frame-Options':'DENY',...(production?{'Strict-Transport-Security':'max-age=31536000'}:{}),...headers});res.end(typeof data==='string'||Buffer.isBuffer(data)?data:JSON.stringify(data))};
 const jsonBody=async req=>{let data='';for await(const chunk of req){data+=chunk;if(Buffer.byteLength(data)>4096)throw Error('Request too large')}return JSON.parse(data||'{}')};
 function getSession(req){const token=req.headers.cookie?.split(';').map(s=>s.trim()).find(s=>s.startsWith(cookieName+'='))?.slice(cookieName.length+1);if(!token||!/^[a-f0-9]{64}$/.test(token))return null;const key=digest(token),s=sessions.get(key);if(!s)return null;if(s.expiry<Date.now()){sessions.delete(key);return null}return {...s,key}}
 function limited(key){const now=Date.now();if(limits.size>5000){for(const [k,v]of limits)if(v.until<now)limits.delete(k);if(limits.size>5000)return true}let value=limits.get(key);if(!value||value.until<now){value={count:0,until:now+900000};limits.set(key,value)}return ++value.count>25}
 function newSession(req,res,user){const previous=getSession(req);if(previous)sessions.delete(previous.key);for(const [k,v]of sessions)if(v.expiry<Date.now())sessions.delete(k);if(sessions.size>=2000)throw Error('Session capacity reached');const token=randomBytes(32).toString('hex');sessions.set(digest(token),{userId:user.id,expiry:Date.now()+ttl});response(res,200,{ok:true},{'Set-Cookie':cookie(token)})}
 async function saveAccounts(){const operation=writes.then(async()=>{const tmp=accountFile+'.tmp';await fs.writeFile(tmp,JSON.stringify(accounts),{mode:0o600});await fs.rename(tmp,accountFile)});writes=operation.catch(()=>{});return operation}
 const publicFiles={'/auth/base.css':'style.css','/auth/login.css':'login.css','/auth/disaster-response-background.png':'disaster-response-background.png','/auth/signin.js':null};
 const protectedFiles=new Set(['earth-orbit.html','index.html','style.css','glass.css','command.css','annotations.css','login.css','app.js','command.js','annotations.js','lucknow-alert.js','login.js','disaster-response-background.png']);
 const mime=file=>file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':file.endsWith('.png')?'image/png':'text/html';
 async function handler(req,res){try{
   const url=new URL(req.url,origin),route=url.pathname;
   if(req.method==='POST'&&route.startsWith('/auth/')){
     if(req.headers.origin!==origin)return response(res,403,{error:'Request origin rejected.'});
     if(!String(req.headers['content-type']||'').startsWith('application/json'))return response(res,415,{error:'JSON required.'});
     if(limited('ip:'+req.socket.remoteAddress))return response(res,429,{error:'Too many attempts. Try again later.'},{'Retry-After':'900'});
     if(route==='/auth/logout'){const s=getSession(req);if(s)sessions.delete(s.key);return response(res,200,{ok:true},{'Set-Cookie':cookie('',0)})}
     if(!['/auth/login','/auth/signup'].includes(route))return response(res,404,{error:'Not found.'});
     let body;try{body=await jsonBody(req)}catch{return response(res,400,{error:'Invalid request.'})}
     const email=typeof body.email==='string'?body.email.trim().toLowerCase():'',password=body.password;
     if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||email.length>254||typeof password!=='string'||password.length>256)return response(res,400,{error:'Enter a valid email and password.'});
     if(limited('email:'+email))return response(res,429,{error:'Too many attempts. Try again later.'});
     if(route==='/auth/signup'&&password.length<6)return response(res,400,{error:'Use a password with at least 6 characters.'});
     if(hashJobs>=4)return response(res,503,{error:'Sign-in service is busy. Try again shortly.'});
     hashJobs++;
     try{
       if(route==='/auth/signup'){
         const record=await passwordHash(password);
         if(accounts.some(a=>a.email===email))return response(res,409,{error:'Unable to create this account. Sign in if you already registered.'});
         const user={id:randomBytes(16).toString('hex'),email,password:record,created:new Date().toISOString(),emailVerified:false};accounts.push(user);
         try{await saveAccounts()}catch(e){accounts=accounts.filter(a=>a.id!==user.id);throw e}
         return newSession(req,res,user);
       }
       const user=accounts.find(a=>a.email===email);
       const valid=await passwordMatches(password,user?.password||{salt:'knapsack-no-account-dummy-salt',iterations,hash:'0'.repeat(64)});
       if(!user||!valid)return response(res,401,{error:'Email or password is incorrect.'});
       return newSession(req,res,user);
     }finally{hashJobs--}
   }
   if(req.method!=='GET')return response(res,405,{error:'Method not allowed.'},{Allow:'GET, POST'});
   if(route==='/about')return response(res,200,await fs.readFile(path.join(base,'about.html'),'utf8'),{'Content-Type':'text/html; charset=utf-8'});
   if(route==='/auth')return response(res,200,await fs.readFile(path.join(base,'signin.html'),'utf8'),{'Content-Type':'text/html; charset=utf-8'});
   if(Object.hasOwn(publicFiles,route)){const file=publicFiles[route];return response(res,200,await fs.readFile(file?path.join(siteDir,file):path.join(base,'signin.js')),{'Content-Type':mime(file||'signin.js')})}
   const session=getSession(req);if(!session)return response(res,303,'',{'Location':'/auth','Content-Type':'text/plain'});
   if(route==='/auth/status')return response(res,200,{authenticated:true,emailVerified:false});
   if(route==='/auth/backend.js')return response(res,200,`window.KNAPSACK_SERVER_AUTH=true;window.KNAPSACK_STORAGE_PREFIX=${JSON.stringify('user-'+session.userId+':')};`,{'Content-Type':'text/javascript'});
   let file=route==='/'?'index.html':route.slice(1);if(!protectedFiles.has(file))return response(res,404,{error:'Not found.'});
   const body=await fs.readFile(path.join(siteDir,file));
   return response(res,200,file==='index.html'?body.toString().replace('<head>','<head><script src="/auth/backend.js"></script>'):body,{'Content-Type':mime(file)+'; charset=utf-8',...(file==='earth-orbit.html'?{'X-Frame-Options':'SAMEORIGIN'}:{})});
 }catch{return response(res,500,{error:'Server error. Please try again.'})}}
 return {handler};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const port=Number(process.env.PORT||3000),production=process.env.NODE_ENV==='production';
 if(production&&(!process.env.APP_ORIGIN||!process.env.DATA_DIR))throw Error('Set APP_ORIGIN and persistent DATA_DIR before production startup.');
 const {handler}=await createApp({origin:process.env.APP_ORIGIN||`http://127.0.0.1:${port}`,production,dataDir:process.env.DATA_DIR||path.join(base,'data')});
 http.createServer(handler).listen(port,process.env.HOST||(production?'0.0.0.0':'127.0.0.1'),()=>console.log(`Knapsack authentication server listening on port ${port}`));
}

