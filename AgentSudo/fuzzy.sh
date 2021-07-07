#!/bin/bash

IP=10.10.104.127
for i in A B C D E F
do
   curl $IP -A "$i" -L
   sleep 1
done