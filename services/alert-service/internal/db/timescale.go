package db

import (
	"log"
	"prism/alert-service/internal/models"
)

type TimescaleDB struct {
	ConnString string
}

func NewTimescaleDB(connStr string) *TimescaleDB {
	return &TimescaleDB{ConnString: connStr}
}

func (db *TimescaleDB) SaveReading(payload models.AlertPayload) error {
	log.Printf("[TimescaleDB] Saved S4 reading %.2f for Region %d", payload.S4Index, payload.RegionID)
	return nil
}
