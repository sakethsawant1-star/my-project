Write-Host "Phase 1: Fetching Zomato dataset from Hugging Face Datasets API (1,000 records)..."
$cleanedData = @()

for ($i = 0; $i -lt 10; $i++) {
    $offset = $i * 100
    $url = "https://datasets-server.huggingface.co/rows?dataset=ManikaSaini%2Fzomato-restaurant-recommendation&config=default&split=train&offset=$offset&length=100"
    
    Write-Host "Fetching batch $($i + 1)/10 (Offset: $offset)..."
    $response = Invoke-RestMethod -Uri $url -Method Get

    foreach ($item in $response.rows) {
        $row = $item.row
        
        # Missing Critical Fields Edge Case Handling
        if ([string]::IsNullOrWhiteSpace($row.name) -or [string]::IsNullOrWhiteSpace($row.location) -or [string]::IsNullOrWhiteSpace($row.cuisines)) {
            continue
        }

        # Extract and clean cost
        $costStr = $row.'approx_cost(for two people)'
        $cost = 500
        if (![string]::IsNullOrWhiteSpace($costStr)) {
            $costStr = $costStr -replace ',', ''
            $parsedCost = 0
            if ([int]::TryParse($costStr, [ref]$parsedCost)) { $cost = $parsedCost }
        }

        # Extract and clean rating
        $ratingStr = $row.rate
        $rating = 3.0
        if (![string]::IsNullOrWhiteSpace($ratingStr) -and $ratingStr -ne "NEW" -and $ratingStr -ne "-") {
            $r = $ratingStr.Split('/')[0]
            $parsedRating = 0.0
            if ([double]::TryParse($r, [ref]$parsedRating)) { $rating = $parsedRating }
        }

        # Data Transformation & Indexing payload
        $cleanedData += [PSCustomObject]@{
            id = $item.row_idx
            name = $row.name.Trim()
            location = $row.location.Trim()
            cuisines = $row.cuisines.Trim()
            costForTwo = $cost
            rating = $rating
            searchIndex = "$($row.name) $($row.location) $($row.cuisines)".ToLower()
        }
    }
}

# Sort by rating descending
$cleanedData = $cleanedData | Sort-Object -Property rating -Descending

$outputPath = Join-Path -Path $PSScriptRoot -ChildPath "zomato_cleaned.json"
$cleanedData | ConvertTo-Json -Depth 10 | Set-Content -Path $outputPath -Encoding UTF8

Write-Host "Phase 1 Complete: Successfully extracted, cleaned, and indexed $($cleanedData.Count) restaurants."
Write-Host "Data securely saved locally to: $outputPath"
