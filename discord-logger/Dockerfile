FROM golang:1.23.4-alpine AS BUILDER
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o main ./src


# FROM build AS TEST
# WORKDIR /app/src
# RUN go test -v ./...


FROM alpine:latest as BUILD
WORKDIR /root/
COPY --from=build /app/main .
EXPOSE 8080
CMD ["./main"]