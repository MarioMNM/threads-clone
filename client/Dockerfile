# Use an official Node.js runtime as a parent image
FROM node:20.8.1-slim

# Set the working directory to /app
WORKDIR /client

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies (after copying files)
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the React application
RUN npm run build

# Expose a port (if needed) - you can change this as per your application's requirements
EXPOSE 5173

# Start the application
CMD ["npm", "start"]
