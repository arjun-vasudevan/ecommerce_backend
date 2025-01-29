package main

import (
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/controllers"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/database"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/repositories"
    "github.com/gin-gonic/gin"
    "github.com/joho/godotenv"
    "os"
)


func main() {
    product_router := gin.Default()

    database.ConnectDB()
    productRepository := repositories.NewProductRepository(database.DB)
    productController := controllers.NewProductController(productRepository)

    productRoutes := product_router.Group("/api/products")
    {
        productRoutes.GET("/", productController.GetProducts)
        productRoutes.POST("/", productController.CreateProduct)

        productRoutes.GET("/:id", productController.GetProduct)
        productRoutes.PATCH("/:id", productController.UpdateProduct)
        productRoutes.DELETE("/:id", productController.DeleteProduct)
    }

    godotenv.Load()
    HOST := os.Getenv("HOST")
    product_router.Run(HOST)
}
