package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"

	"golang.org/x/sys/windows/svc"
	"golang.org/x/sys/windows/svc/eventlog"
)

// port mapping: local port -> target VNC server
var vncServers = map[string]string{
	"5901": "192.168.1.1:5900", 		//  NATALIJA
	"5902": "192.168.1.2:5900:5900", 	//  WEISS
	"5903": "192.168.1.3:5900:5900", 	//  HEINOLA
	"5904": "192.168.1.4:5900:5900", 	//  Manipulacja
	"5905": "192.168.1.5:5900:5900",  	//  Valutec
}


type vncService struct{}

func (m *vncService) Execute(args []string, r <-chan svc.ChangeRequest, s chan<- svc.Status) (svcSpecificEC bool, exitCode uint32) {
	// registry in Event Log
	elog, err := eventlog.Open("VNCJumpHost")
	if err != nil {
		log.Fatalf("Coud not open Event Log: %v", err)
	}
	defer elog.Close()

	// run the service
	s <- svc.Status{State: svc.StartPending}
	elog.Info(1, "VNC JumHost run as a Windows Service")
	s <- svc.Status{State: svc.Running, Accepts: svc.AcceptStop | svc.AcceptShutdown}

	// run the server
	go startServer(elog)

	// Monitor the system requests (e.g., Stop)
	for {
		select {
		case c := <-r:
			switch c.Cmd {
			case svc.Stop, svc.Shutdown:
				elog.Info(1, "Stopping VNC JumpHost service")
				s <- svc.Status{State: svc.StopPending}
				return false, 0
			}
		}
	}
}

// Starting the TCP servers for each VNC target
func startServer(elog *eventlog.Log) {
	for port, target := range vncServers {
		go func(port, target string) {
			listener, err := net.Listen("tcp", ":"+port)
			if err != nil {
				elog.Error(1, fmt.Sprintf("Could not start server on port %s: %v", port, err))
				return
			}
			defer listener.Close()
			elog.Info(1, fmt.Sprintf("JumpHost listening on %s -> %s", port, target))
			for {
				client, err := listener.Accept()
				if err != nil {
					elog.Warning(1, fmt.Sprintf("Error connecting: %v", err))
					continue
				}
				go handleConnection(client, target)
			}
		}(port, target)
	}

	// prevent the main function from exiting
	for {
		time.Sleep(time.Hour)
	}
}

// Kopiuje dane między klientem a serwerem VNC
func handleConnection(client net.Conn, target string) {
	defer client.Close()
	server, err := net.Dial("tcp", target)
	if err != nil {
		log.Println("Error connecting to VNC server:", err)
		return
	}
	defer server.Close()
	go io.Copy(server, client)
	io.Copy(client, server)
}

// Główna funkcja - startuje jako usługa lub aplikacja testowa
func main() {
	isService, err := svc.IsWindowsService()
	if err != nil {
		log.Fatalf("Error checking service: %v", err)
	}

	if isService {
		// Run as Windows Service
		err = svc.Run("VNCJumpHost", &vncService{})
		if err != nil {
			log.Fatalf("Error running service: %v", err)
		}
	} else {
		// Run in test mode as an application
		log.Println("Running JumpHost as an application...")
		startServer(nil)
	}
}
