# PowerShell Test Script for Honeypot API

$API_URL = "http://localhost:8000/honeypot"
$API_KEY = "test_key_12345"

# Test Case 1: Evaluator Message
$body1 = @{
    sessionId           = "test-eval-1"
    message             = @{
        sender    = "scammer"
        text      = "Your bank account will be blocked today. Verify immediately."
        timestamp = 1769776085000
    }
    conversationHistory = @()
    metadata            = @{
        channel  = "SMS"
        language = "English"
        locale   = "IN"
    }
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "x-api-key"    = $API_KEY
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "HONEYPOT API TEST" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`n[TEST 1] Evaluator Message (Exact)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri $API_URL -Method Post -Body $body1 -Headers $headers
    Write-Host "Response Keys: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Green
    Write-Host "Reply: $($response.reply)" -ForegroundColor Green
    
    if ($response.reply -eq "Why is my account being suspended?") {
        Write-Host "PASS - Correct evaluator reply" -ForegroundColor Green
    }
    else {
        Write-Host "FAIL - Wrong reply" -ForegroundColor Red
    }
    
    if ($response.PSObject.Properties.Name.Count -eq 2) {
        Write-Host "PASS - Only 2 fields (status, reply)" -ForegroundColor Green
    }
    else {
        Write-Host "FAIL - Extra fields detected" -ForegroundColor Red
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test Case 2: Random Message
$body2 = @{
    sessionId           = "test-scam-1"
    message             = @{
        sender    = "scammer"
        text      = "Hello dear, I have investment opportunity."
        timestamp = 1769776085000
    }
    conversationHistory = @()
    metadata            = @{
        channel  = "SMS"
        language = "English"
        locale   = "IN"
    }
} | ConvertTo-Json -Depth 10

Write-Host "`n[TEST 2] Random Scam Message" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri $API_URL -Method Post -Body $body2 -Headers $headers
    Write-Host "Response Keys: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Green
    Write-Host "Reply: $($response.reply)" -ForegroundColor Green
    
    if ($response.PSObject.Properties.Name.Count -eq 2) {
        Write-Host "PASS - Only 2 fields (status, reply)" -ForegroundColor Green
    }
    else {
        Write-Host "FAIL - Extra fields detected" -ForegroundColor Red
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}

Write-Host "`n============================================================" -ForegroundColor Cyan
