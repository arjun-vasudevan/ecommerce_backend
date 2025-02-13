package schemas

import "time"

type ProductCreate struct {
	Name        string  `json:"name" binding:"required"`
	Description *string `json:"description"`
	Price       float32 `json:"price" binding:"required"`
	Stock       uint    `json:"stock" binding:"gte=0"`
	Category    *string `json:"category"`
}

type ProductUpdate struct {
	Name        *string  `json:"name"`
	Description *string  `json:"description"`
	Price       *float32 `json:"price"`
	Stock       *uint    `json:"stock"`
	Category    *string  `json:"category"`
}

type ProductResponse struct {
	ID          uint64    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Price       float32   `json:"price"`
	Stock       uint      `json:"stock"`
	Category    string    `json:"category"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}
