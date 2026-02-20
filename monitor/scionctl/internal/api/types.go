package api

import (
	"fmt"
	"net"
	"os"
	"time"

	"github.com/scionproto/scion/pkg/addr"
)

// Define request and response types

type APIResponse struct {
	Status  string      `json:"status"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

type PingStartRequest struct {
	Dst   string `json:"dst"`
	Count *int   `json:"count,omitempty"`
}

type ConfigureASListRequest struct {
	ASList []string `json:"as_list"`
}

type ConfigureISDListRequest struct {
	ISDList []string `json:"isd_list"`
}

// More specific response which overrides interface{}
type FileInfosAPIResponse struct {
	APIResponse
	Data []FileInfo `json:"data,omitempty"` // Override the Data field
}

type StatusAPIResponse struct {
	APIResponse
	Data CommandState `json:"data,omitempty"`
}

// Structs used on node side

type ScionNode struct {
	Addr       string
	Name       string
	Port       int16
	ISD        int16
	AS         int16
	ScionDAddr string
}

type FileInfo struct {
	Index int32  `json:"index"`
	Name  string `json:"name"`
	Size  int64  `json:"size"`
}

type CommandState struct {
	InProgress bool      `json:"in_progress"`
	PID        int       `json:"pid,omitempty"`
	StartTime  time.Time `json:"start_time,omitempty"`
	OutputFile string    `json:"output_file,omitempty"`
}

func NodeToIP(node ScionNode) net.IPAddr {
	// Cast it to net.IPAddr
	return net.IPAddr{IP: net.IP(node.Addr)}
}

func NodeToScionAddress(node *ScionNode) string {
	// Scion address from node including validation
	var scionaddr = fmt.Sprintf("%d-ffaa:%d:%d,%s", node.ISD, node.ISD - 15, node.AS, node.ScionDAddr)
	_, err := addr.ParseAddr(scionaddr)
	fmt.Fprintf(os.Stderr, "[DEBUG] Generated SCION address: %s\n", scionaddr)
	if err != nil {
		fmt.Printf("error: {%v}", err)
		os.Exit(1)
	}
	return scionaddr
}
