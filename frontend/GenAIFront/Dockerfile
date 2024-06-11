FROM node:14-slim AS build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci --no-optional
COPY . .
RUN npm run build

FROM nginx:1.24.0 AS release
RUN apt-get update && apt-get install -y nginx-extras
COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /usr/share/nginx/html
COPY --from=build /usr/src/app/dist ./
CMD ["nginx", "-g", "daemon off;"]