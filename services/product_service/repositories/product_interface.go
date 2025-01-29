package repositories

import (
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
)


type ProductRepository interface {
    ListProducts() (*[]models.Product, error)
    Create(product *models.Product) error
    GetProductByID(id uint64) (*models.Product, error)
    Update(product *models.Product) error
    Delete(id uint64) error
}
