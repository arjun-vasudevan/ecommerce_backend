package controllers

import (
    "github.com/gin-gonic/gin"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/schemas"
    "net/http"
    "strconv"
    "time"
    "fmt"
)


var allProducts = []schemas.ProductResponse{
    {
        ID:          1,
        Name:        "product1",
        Description: "description1",
        Price:       10.00,
        Quantity:    10,
        Category:    "category1",
        CreatedAt:   time.Date(2021, 7, 1, 0, 0, 0, 0, time.UTC),
        UpdatedAt:   time.Date(2021, 7, 1, 0, 0, 0, 0, time.UTC),
    },
    {
        ID:          2,
        Name:        "product2",
        Description: "description2",
        Price:       20.00,
        Quantity:    20,
        Category:    "category2",
        CreatedAt:   time.Date(2021, 7, 2, 0, 0, 0, 0, time.UTC),
        UpdatedAt:   time.Date(2021, 7, 2, 0, 0, 0, 0, time.UTC),
    },
}


func GetProducts(c *gin.Context) {
    c.JSON(http.StatusOK, allProducts)
}


func CreateProduct(c *gin.Context) {
    var productData schemas.ProductCreate
    if err := c.BindJSON(&productData); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    newProduct := schemas.ProductResponse{
        ID:          uint64(len(allProducts) + 1),
        Name:        productData.Name,
        Description: "",
        Price:       productData.Price,
        Quantity:    productData.Quantity,
        Category:    "",
        CreatedAt:   time.Now(),
        UpdatedAt:   time.Now(),
    }

    if productData.Description != nil {
        newProduct.Description = *productData.Description
    }

    if productData.Category != nil {
        newProduct.Category = *productData.Category
    }

    allProducts = append(allProducts, newProduct)
    c.JSON(http.StatusCreated, newProduct)
}


func GetProduct(c *gin.Context) {
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    if productID > uint64(len(allProducts)) {
        c.JSON(http.StatusNotFound, gin.H{"message": "Product not found"})
        return
    }

    c.JSON(http.StatusOK, allProducts[productID-1])
}


func UpdateProduct(c *gin.Context) {
    // Check if valid path parameter
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    // Check if productID is valid
    if productID > uint64(len(allProducts)) {
        c.JSON(http.StatusNotFound, gin.H{"message": "Product not found"})
        return
    }

    // Check if request body is valid
    var productData schemas.ProductUpdate
    if err := c.BindJSON(&productData); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    productID--

    if productData.Name != nil {
        allProducts[productID].Name = *productData.Name
    }
    if productData.Description != nil {
        allProducts[productID].Description = *productData.Description
    }
    if productData.Price != nil {
        allProducts[productID].Price = *productData.Price
    }
    if productData.Quantity != nil {
        allProducts[productID].Quantity = *productData.Quantity
    }
    if productData.Category != nil {
        allProducts[productID].Category = *productData.Category
    }
    allProducts[productID].UpdatedAt = time.Now()

    c.JSON(http.StatusOK, allProducts[productID])
}


func DeleteProduct(c *gin.Context) {
    // Check if valid path parameter
    productID, err := strconv.ParseUint(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid product ID"})
        return
    }

    // Check if productID is valid
    if productID > uint64(len(allProducts)) {
        c.JSON(http.StatusNotFound, gin.H{"message": "Product not found"})
        return
    }

    allProducts = append(allProducts[:productID - 1], allProducts[productID:]...)
    c.JSON(http.StatusOK, gin.H{"message": fmt.Sprintf("Product with ID %d deleted", productID)})
}


