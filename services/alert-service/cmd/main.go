package main

import (
	"log"
	"time"
	"prism/alert-service/internal/ingestpoll"
)

func main() {
	log.Println("Starting PRISM Alerting Service...")
	
	poller := ingestpoll.NewPoller("http://science-engine:8000", 30*time.Second)
	poller.Start()
}
