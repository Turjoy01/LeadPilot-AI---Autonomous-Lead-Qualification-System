# Build Frontend Script
Write-Host "🔨 Building Frontend..." -ForegroundColor Cyan
cd frontend
npm run build
Write-Host "✅ Frontend built successfully!" -ForegroundColor Green
Write-Host "📦 Dist folder created at: frontend/dist" -ForegroundColor Green
