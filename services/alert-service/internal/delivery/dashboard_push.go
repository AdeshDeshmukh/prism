package delivery

import (
	"log"
	"prism/alert-service/internal/models"
)

func PushDashboardEvent(payload models.AlertPayload) {
	log.Printf("[DashboardPush] Event emitted for region %s: Tier %s", payload.RegionName, payload.RiskTier)
}
