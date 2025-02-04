FROM golang:1.23.5-alpine AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /product_service


FROM gcr.io/distroless/base-debian12 AS run-stage

WORKDIR /

COPY --from=build-stage /product_service /product_service

EXPOSE 8001

CMD ["/product_service"]
