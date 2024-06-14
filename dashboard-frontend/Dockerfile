# Use the official Node.js image.
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files and install dependencies
COPY package*.json ./
RUN npm install

# Globally install vite
RUN npm install -g vite

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5173
EXPOSE 5174

# Run the React application
CMD ["npm", "run", "dev"]
