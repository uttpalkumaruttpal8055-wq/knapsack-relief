# Knapsack: public signup and email/password server

This folder is a runnable single-instance Node.js authentication server. Keep its sibling `knapsack/` folder: it contains the actual website and generated background image. Node.js 20 or newer is required. There are no npm dependencies to install.

## Run locally

From this folder:

```powershell
node server.mjs
```

Open **http://127.0.0.1:3000** and create an account. Use a unique test passphrase at least 15 characters long. Public signup, login and sign-out are implemented. Opening the HTML through `file://` does not run this server; it retains the clearly labeled demo interface.

## Run on your domain

Use hosting that runs a persistent Node process, provides a persistent private disk, and terminates HTTPS. This server is not a Cloudflare Worker and cannot be deployed as a static-only Site. Do not upload it to a public static folder.

Set these environment values through the hosting dashboard:

```text
NODE_ENV=production
APP_ORIGIN=https://YOUR-EXACT-DOMAIN
DATA_DIR=/ABSOLUTE/PRIVATE/PERSISTENT/PATH/knapsack-auth
PORT=3000
```

`APP_ORIGIN` must match the final browser origin exactly, without a trailing slash. If your domain uses `www`, choose that origin and redirect other hostnames to it at the host. The app reads `PORT` when the host supplies a port. Route public HTTPS requests to this process using the host's reverse proxy. Add only the DNS A/CNAME records supplied by that host, then verify the HTTPS certificate. Registrar ownership alone does not deploy the application.

## What is implemented

- Public email/password signup; minimum password length 15 characters, maximum 256.
- Per-account random salts, PBKDF2-HMAC-SHA256 with 600,000 iterations and constant-time password comparison.
- Random opaque sessions stored only on the server; eight-hour expiry; session revocation on sign-out and rotation on sign-in. Server restarts end existing sessions.
- HttpOnly, SameSite=Strict cookies, and Secure `__Host-` cookies in production.
- Dashboard and its scripts are protected by the server. There is no authenticated dashboard/demo bypass route.
- Exact Origin enforcement for authentication POSTs, bounded request bodies, attempt limits and hashing concurrency limits.
- Only explicitly allowed website files can be served. Accounts are outside the website directory and are never served as static files.
- Account-specific browser-storage namespaces prevent different accounts on the same browser from sharing the demo ledger by accident. Demo records remain browser-local and are not synchronized across devices.

## Important operational limits

Email ownership verification, forgotten-password email recovery, MFA and administrator roles are not configured. Email addresses are login identifiers, not verified identities. The funding, fleet, warnings and SMS/WhatsApp remain hackathon simulations.

This low-volume server uses a private JSON account store and in-memory sessions/rate limits. Run one instance with private persistent storage; use a proper database, shared session store and audited identity service before scaling. Protect and back up the data directory. On Windows, apply private file ACLs through the hosting environment; Node permission flags do not replace Windows ACLs. No default administrator account or hardcoded password is supplied.

## Checks

```powershell
node --test auth.test.mjs
```

Tests exercise actual handler logic without opening network sockets: unauthorized routes, signup validation, password hashing, login, logout, persisted account login, protected assets, invalid origins and HTTPS-only production configuration with secure cookies. A deployed browser end-to-end test and HTTPS/DNS verification remain necessary after hosting is selected.

References: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html and https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

## Background

The realistic rescue boats, supply trucks and relief campus background is an AI-generated illustrative scene, not evidence of a real disaster. `../knapsack/BACKGROUND-PROMPT.txt` records the built-in ImageGen prompt and asset provenance.
