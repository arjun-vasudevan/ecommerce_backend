package tests

import (
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/controllers"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/schemas"
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/repositories"
    "github.com/jinzhu/copier"
    "github.com/stretchr/testify/assert"
    "time"
    "testing"
    "net/http"
    "net/http/httptest"
    "encoding/json"
    "github.com/gin-gonic/gin"
)


func TestGetProducts(t *testing.T) {
    now := time.Now().UTC()
    products := []models.Product{
        {
            ID: 1,
            Name: "Product 1",
            Description: "Description 1",
            Price: 100,
            Stock: 10,
            Category: "Category 1",
            CreatedAt: now,
            UpdatedAt: now,
        },
        {
            ID: 2,
            Name: "Product 2",
            Description: "Description 2",
            Price: 200,
            Stock: 20,
            Category: "",
            CreatedAt: now,
            UpdatedAt: now,
        },
    }

    var expectedResponse []schemas.ProductResponse
    copier.Copy(&expectedResponse, &products)

    mockRepo := new(repositories.MockProductRepository)
    mockRepo.On("ListProducts").Return(&products, nil)

    // Create a mock gin context
    w := httptest.NewRecorder()
    c, _ := gin.CreateTestContext(w)

    controller := controllers.NewProductController(mockRepo)
    controller.GetProducts(c)

    var response []schemas.ProductResponse
    err := json.Unmarshal(w.Body.Bytes(), &response)

    assert.Nil(t, err)
    assert.Equal(t, http.StatusOK, w.Code)
    assert.Equal(t, expectedResponse, response)
}
