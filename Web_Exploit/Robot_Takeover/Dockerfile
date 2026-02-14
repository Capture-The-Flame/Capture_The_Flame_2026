# Stage 1: Build
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY Assets/package*.json Assets/tsconfig*.json ./
RUN npm install

# Copy the rest of the source code
COPY Assets/ ./

# Build the project
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy build output to nginx html folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
