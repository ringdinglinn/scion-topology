package main

import (
	"io"
	"log"
	"net/http"
	"strings"
)

func main() {

	// Serve static files from working directory
	http.Handle("/", http.FileServer(http.Dir(".")))

	// Proxy endpoint
	http.HandleFunc("/proxy", func(w http.ResponseWriter, r *http.Request) {

		target := r.URL.Query().Get("target")
		endpoint := r.URL.Query().Get("endpoint")
		method := r.URL.Query().Get("method")
		if method == "" {
			method = "GET"
		}

		if target == "" || endpoint == "" {
			http.Error(w, "Target and endpoint parameters are required", http.StatusBadRequest)
			return
		}

		if !strings.HasPrefix(endpoint, "/") {
			endpoint = "/" + endpoint
		}

		targetURL := "http://" + target + endpoint
		log.Println("Proxy ->", targetURL)

		var resp *http.Response
		var err error

		switch method {
		case "GET":
			resp, err = http.Get(targetURL)
		case "POST":
			contentType := r.Header.Get("Content-Type")
			resp, err = http.Post(targetURL, contentType, r.Body)
		default:
			http.Error(w, "Unsupported method", http.StatusBadRequest)
			return
		}

		if err != nil {
			http.Error(w, err.Error(), http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()

		for k, v := range resp.Header {
			for _, vv := range v {
				w.Header().Add(k, vv)
			}
		}

		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	})

	log.Println("Listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
