# Use the official Redis image as the base image
FROM redis:latest

# Copy the redis.conf file into the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Create a directory for logs
RUN mkdir -p /var/log/redis/

# Set the ownership and permissions for the log directory
RUN chown redis:redis /var/log/redis/
RUN chmod 755 /var/log/redis/

# Start the Redis server using the provided configuration file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
