RewindDay Mobile Starter (Expo)

1) Place these files inside apps/mobile of your RewindDay monorepo.
2) Initialize Expo:
   cd apps/mobile
   npx create-expo-app@latest . --template blank-typescript
   npm i axios
3) Run:
   npm run start
4) Ensure backend is running:
   docker compose -f infra/docker-compose.yml up --build
