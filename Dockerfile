FROM node:24-bookworm-slim
WORKDIR /app
COPY knapsack/ ./knapsack/
COPY knapsack-server/server.mjs knapsack-server/signin.html knapsack-server/signin.js knapsack-server/about.html ./knapsack-server/
RUN mkdir -p /app/private-data && chown -R node:node /app
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000
ENV DATA_DIR=/app/private-data
USER node
EXPOSE 3000
CMD ["node", "knapsack-server/server.mjs"]
