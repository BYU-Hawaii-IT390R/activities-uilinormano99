# build-hv.ps1 – Automate VM creation and Windows installation using Hyper-V

# =============================
# Configuration
# =============================
$vmName     = "AutomatedWin10"
$vhdPath    = "C:\ISO Folder\AutomatedWin10.vhdx"
$windowsISO = "C:\ISO Folder\en-us_windows_10_consumer_editions_version_22h2_x64_dvd_8da72ab3.iso"
$answerISO  = "C:\ISO Folder\answer.iso"
$vmMemory   = 4GB
$vhdSize    = 40GB

# =============================
# Cleanup Existing VM or VHD
# =============================
if (Get-VM -Name $vmName -ErrorAction SilentlyContinue) {
    Write-Host "Existing VM '$vmName' found. Removing it..."
    Stop-VM -Name $vmName -Force -ErrorAction SilentlyContinue
    Remove-VM -Name $vmName -Force
}

if (Test-Path $vhdPath) {
    Write-Host "Existing VHDX '$vhdPath' found. Removing it..."
    Remove-Item -Path $vhdPath -Force
}

# =============================
# Create Virtual Hard Disk
# =============================
Write-Host "Creating virtual hard disk..."
New-VHD -Path $vhdPath -SizeBytes $vhdSize -Dynamic | Out-Null

# =============================
# Create the Virtual Machine
# =============================
Write-Host "Creating VM '$vmName'..."
New-VM -Name $vmName -Generation 2 -MemoryStartupBytes $vmMemory -VHDPath $vhdPath -SwitchName "Default Switch"

# =============================
# Disable Secure Boot
# =============================
Write-Host "Disabling Secure Boot..."
Set-VMFirmware -VMName $vmName -EnableSecureBoot Off

# =============================
# Add DVD Drives for ISOs
# =============================
Write-Host "Attaching Windows ISO..."
Add-VMDvdDrive -VMName $vmName -ControllerNumber 0 -ControllerLocation 1 -Path $windowsISO

Write-Host "Attaching Answer File ISO..."
Add-VMDvdDrive -VMName $vmName -ControllerNumber 0 -ControllerLocation 2 -Path $answerISO

# =============================
# Set Boot Order (Boot from DVD)
# =============================
$dvdDrive = Get-VMFirmware -VMName $vmName | Select-Object -ExpandProperty BootOrder | Where-Object { $_.BootDevice -eq "CD" }
Set-VMFirmware -VMName $vmName -FirstBootDevice $dvdDrive

# =============================
# Start the VM
# =============================
Write-Host "Starting the VM..."
Start-VM -Name $vmName

Write-Host "VM '$vmName' created and started successfully."
