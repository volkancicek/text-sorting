# syntax=docker/dockerfile:1
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG REACT_APP_ENV=production
ENV REACT_APP_ENV=${REACT_APP_ENV}

# Build for production
RUN if [ "$REACT_APP_ENV" = "production" ]; then npm run build; fi

# --- Production image ---
FROM nginx:alpine AS prod
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/public/robots.txt /usr/share/nginx/html/robots.txt
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# --- Development image ---
FROM node:18 AS dev
WORKDIR /app
COPY --from=build /app /app
EXPOSE 3000
CMD ["npm", "start"] 