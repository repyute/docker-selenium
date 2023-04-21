package handlers

import (
	"fmt"
	"github.com/google/uuid"
	"github.com/labstack/echo"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

type VncRestartForm struct {
	Password *string `json:"password"`
	Output   *string `json:"output"`
}

func EchoPath(c echo.Context) error {
	out, err := Execute("echo $PATH")
	if err != nil {
		fmt.Println(err.Error())
		return c.JSON(http.StatusInternalServerError, err.Error())
	}
	return c.String(http.StatusOK, out)
}

func ClearChromeSessions(c echo.Context) error {
	uid := uuid.New().String()
	out1, err := Execute("kill $(ps aux | grep 'chromium' | awk '{print $2}')")
	if err != nil {
		fmt.Println(err.Error())
		return c.JSON(http.StatusInternalServerError, err.Error())
	}

	out2, err := Execute("kill $(ps aux | grep 'chrome' | awk '{print $2}')")
	if err != nil {
		fmt.Println(err.Error())
		return c.JSON(http.StatusInternalServerError, err.Error())
	}

	out := out1 + " " + out2
	return c.JSON(http.StatusOK, VncRestartForm{
		Password: &uid,
		Output:   &out,
	})
}

func VncRestart(c echo.Context) error {
	uid := uuid.New().String()
	out1, err := Execute("kill $(ps aux | grep 'x11vnc' | awk '{print $2}')")
	if err != nil {
		fmt.Println(err.Error())
	}

	out2, err := Execute("x11vnc -storepasswd " + uid + " /home/seluser/.vnc/passwd")
	if err != nil {
		fmt.Println(err.Error())
		return c.JSON(http.StatusInternalServerError, err.Error())
	}

	out3, err := ExecuteBackground("x11vnc -usepw -forever")
	if err != nil {
		fmt.Println(err.Error())
		return c.JSON(http.StatusInternalServerError, err.Error())
	}

	out := out1 + "\n" + out2 + "\n" + out3
	return c.JSON(http.StatusOK, VncRestartForm{
		Password: &uid,
		Output:   &out,
	})
}

func VncStop(c echo.Context) error {
	uid := uuid.New().String()
	out, err := Execute("-c", "kill $(ps aux | grep 'x11vnc' | awk '{print $2}')")
	if err != nil {
		fmt.Println(err.Error())
		c.Error(err)
	}

	return c.JSON(http.StatusOK, VncRestartForm{
		Password: &uid,
		Output:   &out,
	})
}

func Execute(args ...string) (string, error) {
	args = append([]string{"-c"}, args...)
	cmd := exec.Command("/bin/sh", args...)
	fmt.Println(cmd)
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}
	return string(out), nil
}

func ExecuteBackground(args ...string) (string, error) {
	args = append([]string{"-c"}, args...)
	//args = append(args, ">/dev/null", "2>&1", "&")
	cmd := exec.Command("/bin/sh", args...)
	log := filepath.Join("/home/seluser", "nohup.out")
	fmt.Println(cmd)

	f, err := os.Create(log)
	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}

	cmd.Stdout = f
	cmd.Stderr = f

	// start command (and let it run in the background)
	err = cmd.Start()
	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}
	return "", nil
}
