$PSQL_PATH = "C:\Program Files\PostgreSQL\16\bin\psql.exe"

Write-Host "Creating PostgreSQL Database..." -ForegroundColor Cyan
Write-Host ""

$password = Read-Host "Enter PostgreSQL password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$env:PGPASSWORD = $plainPassword

Write-Host ""
Write-Host "Creating database 'ai_readme_db'..." -ForegroundColor Yellow

& $PSQL_PATH -U postgres -c "CREATE DATABASE ai_readme_db;"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Database created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Updating backend/.env file..." -ForegroundColor Yellow
    
    $envContent = Get-Content "backend\.env" -Raw
    $envContent = $envContent -replace "DATABASE_URL=.*", "DATABASE_URL=postgresql://postgres:$plainPassword@localhost:5432/ai_readme_db"
    Set-Content "backend\.env" -Value $envContent
    
    Write-Host "✓ Configuration updated!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Failed to create database" -ForegroundColor Red
    Write-Host "The database might already exist or there was an authentication error" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
