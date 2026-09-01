package models

import "time"

type Region struct {
	ID        int     `json:"id"`
	Name      string  `json:"name"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
	Country   string  `json:"country"`
}

type Subscriber struct {
	ID             int    `json:"id"`
	RegionID       int    `json:"region_id"`
	OrgName        string `json:"org_name"`
	ContactPhone   string `json:"contact_phone"`
	SubscriberType string `json:"subscriber_type"` // disaster_response, agriculture, telecom
}

type AlertPayload struct {
	RegionID          int       `json:"region_id"`
	RegionName        string    `json:"region_name"`
	RiskTier          string    `json:"risk_tier"` // LOW, MODERATE, SEVERE
	S4Index           float64   `json:"s4_index"`
	KpIndex           float64   `json:"kp_index"`
	RecommendedAction string    `json:"recommended_action"`
	Timestamp         time.Time `json:"timestamp"`
}
