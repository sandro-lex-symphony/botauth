package main

import (
    "bytes"
    "crypto/rsa"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "net/url"
    "net/http/httputil"
    "os"
    "strings"
    "time"
    "github.com/dgrijalva/jwt-go"
    "github.com/tkanos/gonfig"
)

type Configuration struct {
    POD_HOST string
    KEY_PATH string
    BOT_NAME string
}

var (
	signKey   *rsa.PrivateKey
)

func fatal(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

type TokenResult struct {
    Token string
}

// interacts with POD to authenticated
// gets session token and keyManagerToken
func auth(token string, podurl string) string {
    timeout := time.Duration(5 * time.Second)
    client := http.Client {
        Timeout : timeout,
    }
    jsonValue, _ := json.Marshal(map[string]string{
        "token": token,
    })
    request, err := http.NewRequest("POST", podurl, bytes.NewBuffer(jsonValue))
    fatal(err)
    request.Header.Set("Content-Type", "application/json")
    resp, err := client.Do(request)
    fatal(err)
    if resp.StatusCode != http.StatusOK {
        resp.Body.Close()
        fmt.Printf("failed %s", resp.Status)
        os.Exit(1)
    }
    var result TokenResult
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        resp.Body.Close()
        fatal(err)
        os.Exit(1)
    }

    resp.Body.Close()
    return result.Token
}

// gen JWT from private key
// the jwt is used to auth with pod
func genToken(path string, botname string) string {
    expirationTime := time.Now().Add(5 * time.Minute)
    claims := jwt.StandardClaims{
        ExpiresAt: expirationTime.Unix(),
        Subject: botname,
    }

    signBytes, err := ioutil.ReadFile(path)
    fatal(err)
    signKey, err = jwt.ParseRSAPrivateKeyFromPEM(signBytes)
    fatal(err)


    alg := jwt.GetSigningMethod("RS512")

    token := jwt.NewWithClaims(alg, claims)

    out, err := token.SignedString(signKey)
    fatal(err)
    return out
}

func handler(p *httputil.ReverseProxy, st string, kt string, host string) func(http.ResponseWriter, *http.Request) {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Println(r.URL)
        if strings.Contains(r.URL.RequestURI(), "/authenticate") {
            http.Error(w, "{\"token\": \"qweasd\"}", http.StatusOK)
            return
        }
        r.Header.Set("sessionToken", st)
        r.Header.Set("keyManagerToken", kt)
        r.Host = host
        p.ServeHTTP(w,r)
    }
}

func main() {
    configuration := Configuration{}
    err := gonfig.GetConf("./config.json", &configuration)

    pod_url := "https://" + configuration.POD_HOST
    remote, err := url.Parse(pod_url)
    fatal(err)

    token := genToken(configuration.KEY_PATH, configuration.BOT_NAME)
    sessionToken := auth(token, pod_url + "/login/pubkey/authenticate")
    kmToken := auth(token, pod_url + "/relay/pubkey/authenticate")
    fmt.Println(sessionToken)
    fmt.Println(kmToken)

    rproxy := httputil.NewSingleHostReverseProxy(remote)
    http.HandleFunc("/", handler(rproxy, sessionToken, kmToken, configuration.POD_HOST))
    err = http.ListenAndServe(":8888", nil)
    fatal(err)
}

