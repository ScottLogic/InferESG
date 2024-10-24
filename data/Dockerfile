# Choose our version of Node
FROM neo4j:latest

# Set up a working directory
WORKDIR /data

# Copy the data content into the working directory
COPY . /data

# Copy the datasets into an import folder
COPY /datasets/* /import/

# Expose port for writing to the database and viewing the graph
EXPOSE 7474
EXPOSE 7687
