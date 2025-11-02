$source = "Image Tampering\*"
$destination = "."

# Move all files (excluding directories)
Get-ChildItem -Path $source -File | ForEach-Object {
    $newPath = Join-Path -Path $destination -ChildPath $_.Name
    Write-Host "Moving $($_.Name) to $newPath"
    Move-Item -Path $_.FullName -Destination $newPath -Force
}

Write-Host "All files have been moved successfully!"
