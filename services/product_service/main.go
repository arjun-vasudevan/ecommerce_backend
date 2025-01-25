package main

import (
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/controllers"
    "github.com/gin-gonic/gin"
    "github.com/joho/godotenv"
    "os"
)

func main() {
    product_router := gin.Default()

    productRoutes := product_router.Group("/api/products")
    {
        productRoutes.GET("/", controllers.GetProducts)
        productRoutes.POST("/", controllers.CreateProduct)

        productRoutes.GET("/:id", controllers.GetProduct)
        productRoutes.PATCH("/:id", controllers.UpdateProduct)
        productRoutes.DELETE("/:id", controllers.DeleteProduct)
    }

    godotenv.Load()
    HOST := os.Getenv("HOST")
    product_router.Run(HOST)
}
