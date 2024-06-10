# Stage 1: Build the executable
FROM golang:1.21.10-alpine AS builder

WORKDIR /NotificationService

# Copy the source code
COPY . /NotificationService

# Build the Go binary
RUN go mod tidy && go build -o main .

# Stage 2: Create a minimal image to run the executable
FROM alpine

# Install ssmtp
RUN apk --no-cache add ssmtp

# Set up ssmtp configuration
COPY ssmtp.conf /etc/ssmtp/ssmtp.conf

# Expose port 3000 (if needed)
EXPOSE 3000
EXPOSE 8080

# Set the working directory
WORKDIR /app

# Copy the built executable from the previous stage
COPY --from=builder /NotificationService/main /app/main

# Copy the .env file
COPY --from=builder /NotificationService/.env /app/.env

# Set the executable as executable
RUN chmod +x /app/main

# Run the executable
CMD ./main

