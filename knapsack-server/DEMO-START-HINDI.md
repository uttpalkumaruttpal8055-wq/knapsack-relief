# Website शुरू करें

1. `Start-Website.cmd` पर double-click करें। Console खुली रहने दें। Website पहले से चल रही हो तो दोबारा शुरू करने की जरूरत नहीं है।
2. Browser में `http://127.0.0.1:3000/auth` खोलें।
3. **New to Knapsack? Create an account** चुनें। अपना email और कम से कम 15 characters का unique password डालें, फिर confirm करें। पहली बार के लिए test account उपयोग करें।
4. Signup पूरा होने पर dashboard खुलेगा। अगली बार उसी email/password से login करें। **Sign out** से session समाप्त होगा।
5. Presentation में Overview → Risk atlas → Early warning → Central depot → Optimizer → Fleet & dispatch → Alert network → Project workflow दिखाएँ। Lucknow flood alert स्पष्ट रूप से demo है।

`index.html` सीधे खोलने पर केवल demo preview मिलता है; वास्तविक signup/login ऊपर वाले server URL पर चलता है। यह link इसी computer के लिए है, public internet link नहीं है।

Domain registration और online hosting अभी deferred हैं। Domain खरीदे बिना भी local presentation चलेगी। Website current form में official disaster prediction या वास्तविक SMS/WhatsApp broadcast नहीं करती।

Authentication passwords hashed form में `data/accounts.json` में stored होंगे। इस private data folder को share या publicly upload न करें। Email verification और password reset अभी configured नहीं हैं।
