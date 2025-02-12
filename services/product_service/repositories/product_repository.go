package repositories

import (
	"github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
	"gorm.io/gorm"
)

type productRepository struct {
	db *gorm.DB
}

func NewProductRepository(db *gorm.DB) ProductRepository {
	return &productRepository{db: db}
}

func (pr *productRepository) ListProducts() (*[]models.Product, error) {
	var allProducts []models.Product
	if err := pr.db.Find(&allProducts).Error; err != nil {
		return nil, err
	}

	return &allProducts, nil
}

func (pr *productRepository) Create(product *models.Product) error {
	return pr.db.Create(product).Error
}

func (pr *productRepository) GetProductByID(id uint64) (*models.Product, error) {
	var product models.Product
	if err := pr.db.First(&product, id).Error; err != nil {
		return nil, err
	}

	return &product, nil
}

func (pr *productRepository) Update(product *models.Product) error {
	return pr.db.Save(product).Error
}

func (pr *productRepository) Delete(id uint64) error {
	result := pr.db.Delete(&models.Product{}, id)

	if result.RowsAffected == 0 {
		return gorm.ErrRecordNotFound
	}

	return result.Error
}
