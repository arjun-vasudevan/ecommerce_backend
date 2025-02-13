package models

import "time"

type Product struct {
	ID          uint64 `gorm:"primaryKey;autoIncrement"`
	Name        string `gorm:"not null"`
	Description string
	Price       float32 `gorm:"not null"`
	Stock       uint    `gorm:"not null"`
	Category    string
	CreatedAt   time.Time `gorm:"autoCreateTime"`
	UpdatedAt   time.Time `gorm:"autoUpdateTime"`
}
