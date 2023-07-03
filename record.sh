#!/bin/bash
nc 192.168.0.21 30003 | python3 record.py --token $(cat token.txt)
