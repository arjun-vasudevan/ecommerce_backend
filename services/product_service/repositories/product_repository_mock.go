package repositories

import (
    "github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
    "github.com/stretchr/testify/mock"

)


type MockProductRepository struct {
    mock.Mock
}

// Ensure MockProductRepository satisfies ProductRepository interface
var _ ProductRepository = &MockProductRepository{}

func (m *MockProductRepository) ListProducts() (*[]models.Product, error) {
    args := m.Called()
    return args.Get(0).(*[]models.Product), args.Error(1)
}

func (m *MockProductRepository) Create(product *models.Product) error {
    args := m.Called(product)
    return args.Error(0)
}

func (m *MockProductRepository) GetProductByID(id uint64) (*models.Product, error) {
    args := m.Called(id)
    return args.Get(0).(*models.Product), args.Error(1)
}

func (m *MockProductRepository) Update(product *models.Product) error {
    args := m.Called(product)
    return args.Error(0)
}

func (m *MockProductRepository) Delete(id uint64) error {
    args := m.Called(id)
    return args.Error(0)
}
