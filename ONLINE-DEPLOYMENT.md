# Knapsack Relief — Online deployment

The website is prepared for deployment, but has not been deployed publicly. A hosting account, chosen service and verification of its live HTTPS URL are still required. No domain registration or purchase is required to use a host-assigned URL.

Use a Node.js web-service host with a private persistent writable disk. This project is not a static-only website: do not upload only its HTML and expect login to work. Keep the two folders `knapsack/` and `knapsack-server/` side-by-side. Never upload the local `knapsack-server/data/` directory or real accounts to a public repository.

## Node hosting settings

Start command from the repository root:

```text
node knapsack-server/server.mjs
```

Set these environment variables in the host dashboard:

```text
NODE_ENV=production
HOST=0.0.0.0
APP_ORIGIN=https://YOUR-ACTUAL-HOST-ASSIGNED-NAME
DATA_DIR=/ABSOLUTE/PRIVATE/PERSISTENT/WRITABLE/DIRECTORY
```

The host supplies `PORT`; the app reads it. `APP_ORIGIN` must exactly match the HTTPS origin friends open, with no trailing slash. This exact match protects authentication requests against cross-origin submissions. Change it when changing domains. Do not invent the host URL before the host assigns it.

The account store needs a persistent disk. Render free web services do not offer persistent disks; do not rely on ephemeral storage to retain registrations. A persistent-storage service or database integration is needed for lasting accounts. No paid service has been selected or purchased for you.

Render reference: https://render.com/docs/deploy-node-express-app
Storage reference: https://render.com/docs/disks
Free tier limitations: https://render.com/docs/free

## Docker hosting alternative

The included Dockerfile packages only the website and server source. Set `APP_ORIGIN` when deploying, and mount a private persistent volume at `/app/private-data` writable by the container's `node` user. The image requires an HTTPS reverse proxy from the host. Docker build/deployment has not been executed in this workspace.

## Public website name

After deployment, share:

- `https://YOUR-ACTUAL-HOST-ASSIGNED-NAME/about` — public Knapsack Relief introduction.
- `https://YOUR-ACTUAL-HOST-ASSIGNED-NAME/auth` — public signup/login.
- `https://YOUR-ACTUAL-HOST-ASSIGNED-NAME/` — authenticated dashboard.

The browser titles and public introduction identify the website as **Knapsack Relief — Disaster Intelligence**. Appearing in Google search requires a publicly reachable site and search-engine indexing; a local address or title edit cannot guarantee it. `knapsackrelief.in` remains your intended, unregistered future domain.

## Same-Wi-Fi access before hosting

On the presenting laptop, obtain its Wi-Fi IPv4 address with `ipconfig`, then run the server with `HOST=0.0.0.0` and `APP_ORIGIN=http://YOUR-WIFI-IP:3001`, plus `PORT=3001`. Members open `http://YOUR-WIFI-IP:3001/auth`, not 127.0.0.1. Windows Firewall and Wi-Fi client isolation may prevent LAN access; allow only the trusted private network as needed. This LAN setup is not a public internet deployment.
