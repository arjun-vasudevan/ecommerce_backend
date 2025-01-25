package controllers

import (
    "github.com/gin-gonic/gin"
)




func GetProducts(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "Get all products",
    })
}


func CreateProduct(c *gin.Context) {
    c.JSON(201, gin.H{
        "message": "Create a product",
    })
}


func GetProduct(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "Get a product",
    })
}


func UpdateProduct(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "Update a product",
    })
}


func DeleteProduct(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "Delete a product",
    })
}


