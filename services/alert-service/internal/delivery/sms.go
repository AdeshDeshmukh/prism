package delivery

import (
	"fmt"
	"log"
	"prism/alert-service/internal/models"
)

type SMSGateway struct {
	APIKey string
}

func NewSMSGateway(apiKey string) *SMSGateway {
	return &SMSGateway{APIKey: apiKey}
}

func (s *SMSGateway) SendAlert(subscriber models.Subscriber, payload models.AlertPayload) error {
	msg := fmt.Sprintf("[PRISM ALERT - %s] S4: %.2f | Action: %s", payload.RiskTier, payload.S4Index, payload.RecommendedAction)
	log.Printf("[SMS] Dispatching to %s (%s): %s", subscriber.ContactPhone, subscriber.OrgName, msg)
	return nil
}
