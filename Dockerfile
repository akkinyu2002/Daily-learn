FROM node:18-alpine

# Install git (needed for GitHub commits)
RUN apk add --no-cache git

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./
COPY packages/backend/package.json ./packages/backend/
COPY packages/shared/package.json ./packages/shared/

# Install dependencies
RUN npm install

# Copy source code
COPY packages/ ./packages/

# Build all packages
RUN npm run build

# Expose port
EXPOSE 3001

# Start the backend server
CMD ["npm", "run", "start", "--", "--workspace", "packages/backend"]
