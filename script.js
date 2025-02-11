async function getAccessToken() {
    const url = "https://test.api.amadeus.com/v1/security/oauth2/token";
    const clientId = "b4Yd0QrFGeZZCzkR9PdaT0b0SFObT0er";
    const clientSecret = "fJ4hGQnmuSMMhdwA";
    
    const params = new URLSearchParams();
    params.append("grant_type", "client_credentials");
    params.append("client_id", clientId);
    params.append("client_secret", clientSecret);
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: params
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Access Token:", data.access_token);
        return data.access_token;
    } catch (error) {
        console.error("Error fetching access token:", error);
    }
}

getAccessToken();
