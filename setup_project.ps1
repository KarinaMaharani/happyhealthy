# PowerShell script to generate all Happy Healthy project files

$baseDir = "c:\.FILES\..MY STUFF\..KARIN\.UI\code\happyhealthy"

# Create directories
$dirs = @(
    "templates",
    "templates\drug_checker",
    "templates\auth",
    "templates\main",
    "static",
    "static\css",
    "static\js",
    "static\images"
)

foreach ($dir in $dirs) {
    $path = Join-Path $baseDir $dir
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force
        Write-Host "Created directory: $path"
    }
}

Write-Host "`n=== Project structure created ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update .env file with your DrugBank API key"
Write-Host "2. Run: python manage.py makemigrations"
Write-Host "3. Run: python manage.py migrate"
Write-Host "4. Run: python manage.py runserver"
Write-Host "`nThen create the template and view files manually or use the code I'll provide next."
