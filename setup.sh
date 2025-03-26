New-Item -ItemType Directory -Path $HOME\.streamlit -Force

Set-Content -Path $HOME\.streamlit\config.toml -Value @"
[server]
port = $env:PORT
enableCORS = false
headless = true
"@