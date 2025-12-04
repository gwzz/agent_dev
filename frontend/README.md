# Agent Frontend

Agent Frontend is a Next.js 16 (App Router + Turbopack) UI for interacting with multiple AI agents. It ships with a responsive chat surface, model/temperature controls, a history drawer, and shadcn/Radix UI components that keep the experience consistent across light and dark themes.

## Features
- Chat interface with streaming indicator, markdown + code highlighting, and attachment placeholders.
- Agent sidebar for choosing models, temperature, and max token limits.
- Conversation history drawer with rename/delete actions persisted via Zustand storage.
- API service layer (`src/lib/api.ts`) that routes chat input to backend agent endpoints.

## Prerequisites
- Node.js 18.18+ (or any version supported by Next 16).
- npm 9+ (yarn/pnpm/bun also work, but the repo is configured for npm).
- A running backend that exposes REST endpoints for the AI agents (see below).

## Local Development
```bash
npm install           # install dependencies once
npm run dev           # start Next.js (defaults to http://localhost:3000)

# other useful scripts
npm run build         # production build
npm start             # run the built app locally
npm run lint          # eslint
```

> ℹ️ If port `3000` is busy, Next.js automatically falls back to the next free port and prints it in the terminal.

## Connecting to the Backend
The frontend talks to the backend through `NEXT_PUBLIC_BACKEND_URL` (default `http://localhost:8000`). Each chat request is proxied through the helper methods in `src/lib/api.ts`, which currently expect the backend to expose:

- `POST /city-info`
- `POST /crypto`
- `POST /law`

Each endpoint should accept a JSON payload like `{ "query": "your prompt" }` and respond with `{ "status": "success", "result": { "content": "..." } }`.

### Configure the URL
1. Create a `.env.local` file in the project root (ignored by git) and set the backend origin:
	```bash
	NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
	```
	Replace the value with the host/port where your backend runs (https, different host, etc.).
2. Restart `npm run dev` (Next.js only reads env vars on startup).

### Verify the connection
1. Start your backend server and confirm the endpoints above return 200 locally (e.g., via `curl` or Postman).
2. Start `npm run dev` for the frontend.
3. Open the app in the browser, enter a prompt, and check the network tab: you should see calls heading to `${NEXT_PUBLIC_BACKEND_URL}/city-info` (or other agents if you wire them up). Any fetch errors bubble to the chat window.

If you later add routing logic to `apiService.sendMessage`, keep the README in sync so backend integrators know which endpoints are required.

## Deployment
When you are ready to deploy, build the app with `npm run build` and deploy the generated `.next` output to any platform that supports Next.js 16 (Vercel, Netlify, Docker, etc.). Make sure `NEXT_PUBLIC_BACKEND_URL` is set in the target environment so the app can reach your backend agents.
