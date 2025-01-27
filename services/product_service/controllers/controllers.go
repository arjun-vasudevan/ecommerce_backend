package controllers

import (
    "github.com/gin-gonic/gin"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/database"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/schemas"
    "github.com/jinzhu/copier"
    "net/http"
    "strconv"
    "time"
    "fmt"
)


func GetProducts(c *gin.Context) {
    // Retrieve all products from database
    var allProducts []models.Product
    if err := database.DB.Find(&allProducts).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    var productResponse []schemas.ProductResponse

    for _, product := range allProducts {
        // Copy product to response schema
        var productSchema schemas.ProductResponse
        if err := copier.Copy(&productSchema, &product); err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
            return
        }

        // Append product to response
        productResponse = append(productResponse, productSchema)
    }

    c.JSON(http.StatusOK, productResponse)
}


func CreateProduct(c *gin.Context) {
    // Validate request body
    var productData schemas.ProductCreate
    if err := c.ShouldBindJSON(&productData); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Create new product
    newProduct := models.Product{
        Name:        productData.Name,
        Description: "",
        Price:       productData.Price,
        Quantity:    productData.Quantity,
        Category:    "",
    }

    if productData.Description != nil {
        newProduct.Description = *productData.Description
    }

    if productData.Category != nil {
        newProduct.Category = *productData.Category
    }

    // Create new product in database
    if err := database.DB.Create(&newProduct).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    // Return new product
    var productResponse schemas.ProductResponse
    if err := copier.Copy(&productResponse, &newProduct); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, productResponse)
}


func GetProduct(c *gin.Context) {
    // Validate path parameter
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    // Retrieve product from database
    var product models.Product
    if err := database.DB.First(&product, productID).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"message": "Product not found"})
        return
        return
    }

    // Return product
    var productResponse schemas.ProductResponse
    if err := copier.Copy(&productResponse, &product); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, productResponse)
}


func UpdateProduct(c *gin.Context) {
    // Validate path parameter
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    // Validate request body
    var productData schemas.ProductUpdate
    if err := c.ShouldBindJSON(&productData); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Retrieve existing product from database
    var product models.Product
    if err := database.DB.First(&product, productID).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"message": "Product not found"})
        return
    }

    // Update product fields
    if productData.Name != nil {
        product.Name = *productData.Name
    }
    if productData.Description != nil {
        product.Description = *productData.Description
    }
    if productData.Price != nil {
        product.Price = *productData.Price
    }
    if productData.Quantity != nil {
        product.Quantity = *productData.Quantity
    }
    if productData.Category != nil {
        product.Category = *productData.Category
    }

    // Save updated product in database
    if err := database.DB.Save(&product).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    // Return updated product
    var productResponse schemas.ProductResponse
    if err := copier.Copy(&productResponse, &product); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, productResponse)
}


func DeleteProduct(c *gin.Context) {
    // Validate path parameter
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    // Delete product from database
    if err := database.DB.Delete(&models.Product{}, productID).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, gin.H{"message": fmt.Sprintf("Product with ID %d deleted", productID)})
}
