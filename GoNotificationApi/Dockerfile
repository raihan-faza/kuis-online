FROM golang:1.21.10-alpine

WORKDIR /NotificationService

COPY . /NotificationService

RUN go mod tidy && go build -o main .

EXPOSE 3000

CMD ./main
