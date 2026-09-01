FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download || true

COPY . .
RUN go build -o alert-service ./cmd/main.go

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/alert-service .

CMD ["./alert-service"]
