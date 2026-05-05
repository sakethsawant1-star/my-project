$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()
Write-Host "Listening on port 8080..."
while ($listener.IsListening) {
    $context = $listener.GetContext()
    $response = $context.Response
    $content = [System.IO.File]::ReadAllBytes("c:\Project\chat.html")
    $response.ContentLength64 = $content.Length
    $response.ContentType = "text/html"
    $response.OutputStream.Write($content, 0, $content.Length)
    $response.Close()
}
