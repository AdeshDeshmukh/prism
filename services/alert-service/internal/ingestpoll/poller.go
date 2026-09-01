package ingestpoll

import (
	"fmt"
	"log"
	"time"
)

type Poller struct {
	ScienceEngineURL string
	Interval         time.Duration
}

func NewPoller(url string, interval time.Duration) *Poller {
	return &Poller{
		ScienceEngineURL: url,
		Interval:         interval,
	}
}

func (p *Poller) Start() {
	log.Printf("[Poller] Starting space-weather polling loop against %s every %v", p.ScienceEngineURL, p.Interval)
	ticker := time.NewTicker(p.Interval)
	defer ticker.Stop()

	for range ticker.C {
		p.PollRegions()
	}
}

func (p *Poller) PollRegions() {
	fmt.Println("[Poller] Polling science engine for equatorial region risk scores...")
}
