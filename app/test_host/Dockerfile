# FROM ubuntu:latest

# # Install the OpenSSH server
# RUN apt-get update && \
#     apt-get install -y openssh-server && \
#     apt-get clean

# # Create the /root/.ssh/ directory and set permissions
# RUN mkdir -p /root/.ssh/ && \
#     chmod 700 /root/.ssh/

# # Define a build argument for the public key
# ARG PUBLIC_KEY

# # Copy the public key to the authorized_keys file using the build argument
# RUN echo "${PUBLIC_KEY}" > /root/.ssh/authorized_keys && \
#     chmod 600 /root/.ssh/authorized_keys

# # Create the privilege separation directory
# RUN mkdir -p /run/sshd

# # Run the SSH server
# CMD ["/usr/sbin/sshd", "-D", "-e"]


FROM ubuntu:latest

# Install OpenSSH server and any other necessary packages
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean

# Create the necessary directories and set permissions
    # cat /backend_idrsa_key.pub > /root/.ssh/authorized_keys && \
ARG PUBLIC_KEY
RUN mkdir -p /root/.ssh/ && \
    chmod 700 /root/.ssh/ && \
    echo "${PUBLIC_KEY}" > /root/.ssh/authorized_keys && \
    cat /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys && \
    mkdir -p /run/sshd

# Set the root password (replace "your_password" with the desired password)
RUN echo 'root:Thanksjose!' | chpasswd

# Expose the SSH port
EXPOSE 22

# Start the SSH server in the foreground with debug mode enabled for troubleshooting
CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]
