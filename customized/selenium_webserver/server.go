package main

import (
	"flag"
	"fmt"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
	"net/http"
	"os"
	"repute.net/selenium_webserver/handlers"
	"time"
)

// about contains build details and uptime details about the service
// Version,MinVersion and BuildTime are set on build
type about struct {
	Version    string
	MinVersion string
	BuildTime  string
	StartedAt  time.Time
	Uptime     string
}

var serverDetails about

// Version details to be filled un build itself
var (
	Version    string
	MinVersion string
	BuildTime  string
)

var (
	host = flag.String("host", "0.0.0.0", "Host ip")
	port = flag.String("port", "8080", "Host port")
	// ServiceDirectory the directory where the service runs
	ServiceDirectory string
)

func main() {
	flag.Parse()
	e := echo.New()
	e.Use(middleware.BodyLimit("10M"))
	e.Use(middleware.Secure())
	e.Use(middleware.RemoveTrailingSlash())
	e.Use(CORSMiddlewareWrapper)
	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: `${host} ${remote_ip} ${time_rfc3339_nano} ${id} ${method} ${uri} ${status} "${user_agent}" ${latency} ${bytes_in} ${bytes_out}` + "\n",
	}))

	// API's which doesn't need Authorization
	e.GET("/", func(ctx echo.Context) error {
		return ctx.JSON(http.StatusOK, Heartbeat())
	})
	e.GET("/echo/path", handlers.EchoPath)
	e.GET("/vnc/restart", handlers.VncRestart)
	e.GET("/vnc/stop", handlers.VncStop)
	e.GET("/sessions/clear", handlers.ClearChromeSessions)

	if err := e.Start(fmt.Sprintf("%s:%s", *host, *port)); err != nil {
		fmt.Println("Failed to start server!", err)
		os.Exit(1)
	}
	return
}

func init() {
	serverDetails = about{Version: Version, MinVersion: MinVersion, BuildTime: BuildTime, StartedAt: time.Now()}
}

// Heartbeat returns details of the instance running
func Heartbeat() interface{} {
	uptime := time.Since(serverDetails.StartedAt)
	serverDetails.Uptime = fmt.Sprintf("%d days %s", uptime/(time.Hour*24), time.Time{}.Add(uptime).Format("15:04:05"))
	return serverDetails
}

// CORSMiddlewareWrapper for browser
func CORSMiddlewareWrapper(next echo.HandlerFunc) echo.HandlerFunc {
	return func(ctx echo.Context) error {
		req := ctx.Request()
		dynamicCORSConfig := middleware.CORSConfig{
			AllowCredentials: true,
			AllowOrigins:     []string{req.Header.Get("Origin")},
			AllowHeaders:     []string{"Authorization", "Accept", "Cache-Control", "Content-Type", "X-Requested-With"},
		}
		dynamicCORSConfig.AllowOrigins = []string{req.Header.Get("Origin")}

		CORSMiddleware := middleware.CORSWithConfig(dynamicCORSConfig)
		CORSHandler := CORSMiddleware(next)
		return CORSHandler(ctx)
	}
}
