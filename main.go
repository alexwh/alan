package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
)

func main() {
	ip := flag.String("ip", "127.0.0.1", "Remote IP to connect to")
	port := flag.String("port", "10001", "Remote port to connect to")
	lport := flag.String("lport", "10000", "Local port to listen on")
	flag.Parse()

	fmt.Println("Launching server...")
	ln, err := net.Listen("tcp", fmt.Sprintf(":%v", *lport))
	if err != nil {
		log.Print(err)
	}
	lconn, _ := ln.Accept()

	rconn, _ := net.Dial("tcp", fmt.Sprintf("%v:%v", *ip, *port))

	for {
		lmessage, _ := bufio.NewReader(lconn).ReadString('\n')
		fmt.Printf("Message Received: %#v", string(lmessage))
		// lconn.Write([]byte(lmessage + "\n"))

		fmt.Fprintf(rconn, lmessage+"\n")
		rmessage, _ := bufio.NewReader(rconn).ReadString('\n')
		fmt.Print("Message from remote server: " + rmessage)
	}
}
