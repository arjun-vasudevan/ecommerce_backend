package database

import (
	"github.com/arjun-vasudevan/ecommerce_backend/services/product_service/models"
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"os"
)

var DB *gorm.DB

func ConnectDB() {
	godotenv.Load()
	dsn := os.Getenv("DATABASE_URL")

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}

	if err := db.AutoMigrate(&models.Product{}); err != nil {
		log.Fatalf("Error migrating database: %v", err)
	}

	DB = db
}
