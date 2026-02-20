package handler

import (
	"fmt"
	"scionctl/internal/api"
	"scionctl/internal/config"
	"scionctl/internal/pprinter"
	"strconv"
	"time"
)

// HandleConfigASList handles the logic for configuring AS blacklist on a node
//
// args: [node, AS1, AS2, ...] or [node, "delete"]
//
// Example usage: scionctl config aslist scion11 12 13 15
// Example usage: scionctl config aslist scion11 delete
func HandleConfigASList(args []string) {
	// Extract node name
	nodeName := args[0]
	node, exists := config.CmdNodeManager.GetNode(nodeName)

	if !exists {
		pprinter.PrintError(fmt.Errorf("node [%s] does not exist", nodeName))
		return
	}

	// Process AS list
	var asList []string

	// Check if user wants to delete/clear the blacklist
	if len(args) == 2 && args[1] == "delete" {
		asList = []string{} // Empty list
	} else {
		// Format each AS number to ffaa:<isd>:<as>
		for i := 1; i < len(args); i++ {
			asNum := args[i]

			// Validate it's a number
			num, err := strconv.Atoi(asNum)
			if err != nil {
				pprinter.PrintError(fmt.Errorf("invalid AS format: '%s' - must be a number", asNum))
				return
			}

			// Validate it's a positive number
			if num <= 0 {
				pprinter.PrintError(fmt.Errorf("invalid AS format: '%s' - must be a positive number", asNum))
				return
			}

			// Format to ffaa:<isd>:<as>
			formattedAS := fmt.Sprintf("ffaa:%d:%d", num / 10, num % 10)
			asList = append(asList, formattedAS)
		}
	}

	// Create API client
	c := api.NewClient(api.ClientConfig{
		BaseURL: "http://" + node.Addr + ":" + fmt.Sprint(node.Port),
		Timeout: time.Second * 5,
	})

	// Call API
	resp, err := c.ConfigureASList(asList)
	pprinter.HTTPResponseToStdout(resp, err)
}

func HandleConfigISDList(args []string) {
	// Extract node name
	nodeName := args[0]
	node, exists := config.CmdNodeManager.GetNode(nodeName)

	if !exists {
		pprinter.PrintError(fmt.Errorf("node [%s] does not exist", nodeName))
		return
	}

	// Process AS list
	var isdList []string

	// Check if user wants to delete/clear the blacklist
	if len(args) == 2 && args[1] == "delete" {
		isdList = []string{} // Empty list
	} else {
		// Format each ISD number to ffaa:1:<number>
		for i := 1; i < len(args); i++ {
			isdNum := args[i]

			// Validate it's a number
			num, err := strconv.Atoi(isdNum)
			if err != nil {
				pprinter.PrintError(fmt.Errorf("invalid ISD format: '%s' - must be a number", isdNum))
				return
			}

			// Validate it's a positive number
			if num <= 0 {
				pprinter.PrintError(fmt.Errorf("invalid ISD format: '%s' - must be a positive number", isdNum))
				return
			}

			isdList = append(isdList, isdNum)
		}
	}

	// Create API client
	c := api.NewClient(api.ClientConfig{
		BaseURL: "http://" + node.Addr + ":" + fmt.Sprint(node.Port),
		Timeout: time.Second * 5,
	})

	// Call API
	resp, err := c.ConfigureISDList(isdList)
	pprinter.HTTPResponseToStdout(resp, err)
}

// HandleConfigFile retrieves the path-policy configuration file from a node
//
// args: [node]
//
// Example usage: scionctl config file scion11
func HandleConfigFile(args []string) {
	// Extract node name
	nodeName := args[0]
	node, exists := config.CmdNodeManager.GetNode(nodeName)

	if !exists {
		pprinter.PrintError(fmt.Errorf("node [%s] does not exist", nodeName))
		return
	}

	// Create API client
	c := api.NewClient(api.ClientConfig{
		BaseURL: "http://" + node.Addr + ":" + fmt.Sprint(node.Port),
		Timeout: time.Second * 5,
	})

	// Call API
	resp, err := c.GetConfigFile()
	pprinter.HTTPResponseRawToStdout(resp, err)
}
