# Use official Node.js LTS image
FROM node:20-alpine

# Create app directory inside container
WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the application
COPY . .

# Expose the port your app runs on
# Change if your server uses a different port
EXPOSE 3000

# Start the server
CMD ["node", "server.js"]
